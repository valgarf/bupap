from datetime import datetime, timedelta, timezone
from typing import TYPE_CHECKING, Annotated

import pytz
import sqlalchemy as sa
import strawberry
from loguru import logger
from sqlalchemy import inspect

from bupap import db
from bupap.common import nowUTC, toUTC
from bupap.common.enums import ScheduleMode

from ..common.context import InfoContext
from ..common.db_type import DBType, map_to_db
from .common import Period
from .user import User


@strawberry.input
class ScheduleRequest:
    start: datetime
    end: datetime
    mode: ScheduleMode = ScheduleMode.AVERAGE


@strawberry.type
class SchedulePeriod:
    period: Period
    color: str
    text: str


@strawberry.type
class ScheduleUser:
    user: User
    working_periods: list[Period]
    timesinks: list[SchedulePeriod]
    worked_tasks: list[SchedulePeriod]
    scheduled_tasks: list[SchedulePeriod]


@strawberry.type
class Schedule:
    now: datetime
    covers: Period

    @strawberry.field
    def actual(self) -> Period:
        min_start = self.covers.end
        max_end = self.covers.start
        for sch in self.user_schedules:
            for per in sch.timesinks + sch.worked_tasks + sch.scheduled_tasks:
                min_start = min(min_start, per.period.start)
                max_end = max(max_end, per.period.end)
        min_start = max(min_start, self.covers.start)
        max_end = min(max_end, self.covers.end)
        return Period(min_start, max_end)

    user_schedules: list[ScheduleUser]


def get_schedule(team: db.Team, request: ScheduleRequest) -> Schedule:
    now = nowUTC()
    request.start = toUTC(request.start)
    request.end = toUTC(request.end)
    session = inspect(team).session
    users = set()
    for r in team.assigned_roles:
        if r.role.name == "Developer":
            users.add(r.user)
    ordered_users = sorted(users, key=lambda u: u.name)
    user_schedules = [
        ScheduleUser(
            user=User(user), working_periods=[], timesinks=[], worked_tasks=[], scheduled_tasks=[]
        )
        for user in ordered_users
    ]
    result = Schedule(
        now=now, covers=Period(request.start, request.end), user_schedules=user_schedules
    )

    # Get already worked periods
    work_periods = session.scalars(
        sa.select(db.WorkPeriod)
        .join(db.User)
        .join(db.AssignedTeamRole)
        .join(db.Role)
        .where(db.WorkPeriod.started_at < request.end)
        .where(sa.or_(db.WorkPeriod.ended_at > request.start, db.WorkPeriod.ended_at == None))
        .where(db.AssignedTeamRole.team_id == team.id)
        .where(db.Role.name == "Developer")
    ).all()

    def _filter_on_schedule_mode(query):
        match request.mode:
            case ScheduleMode.PESSIMISTIC:
                return query.where(db.Task.scheduled_pessimistic_start < request.end).where(
                    db.Task.scheduled_pessimistic_end > max(request.start, now)
                )
            case ScheduleMode.AVERAGE:
                return query.where(db.Task.scheduled_average_start < request.end).where(
                    db.Task.scheduled_average_end > max(request.start, now)
                )
            case ScheduleMode.OPTIMISTIC:
                return query.where(db.Task.scheduled_optimistic_start < request.end).where(
                    db.Task.scheduled_optimistic_end > max(request.start, now)
                )

    # get future tasks
    scheduled: list[db.Task] = session.scalars(
        _filter_on_schedule_mode(
            sa.select(db.Task)
            .join(db.User, onclause=db.User.id == db.Task.scheduled_assignee_id)
            .join(db.AssignedTeamRole)
            .join(db.Role)
        )
        .where(db.Task.task_state == db.TaskState.SCHEDULED)
        .where(db.AssignedTeamRole.team_id == team.id)
        .where(db.Role.name == "Developer")
    ).all()
    logger.debug(f"Schedule for team {team.id} found {len(work_periods)} entries")
    wps_by_user = {}
    sch_by_user: dict[db.User, list[db.Task]] = {}
    for wp in work_periods:
        wps_by_user.setdefault(wp.user, []).append(wp)
    for task in scheduled:
        sch_by_user.setdefault(task.scheduled_assignee, []).append(task)

    # add tasks / working periods into user schedules
    for user, sch_user in zip(ordered_users, result.user_schedules):
        # add already worked periods
        for wp in wps_by_user.get(user, []):
            period = Period(wp.started_at, wp.ended_at or now)
            if period.end <= period.start:
                continue
            if isinstance(wp, db.WorkPeriodTask):
                sch_user.worked_tasks.append(
                    SchedulePeriod(period=period, text=wp.task.name, color=wp.task.project.color)
                )
            if isinstance(wp, db.WorkPeriodTimesink):
                sch_user.timesinks.append(
                    SchedulePeriod(period=period, text=wp.timesink.name, color=wp.timesink.color)
                )
            if isinstance(wp, db.WorkPeriodWorking):
                sch_user.working_periods.append(period)

        # add scheduled working times
        for idx, (sch_start, sch_end) in enumerate(
            db.iterate_schedule(user, max(request.start - timedelta(days=1), now).date())
        ):
            sch_start = max(toUTC(sch_start), request.start, now)
            if sch_start >= request.end:
                break
            sch_end = min(toUTC(sch_end), request.end)
            if sch_start < sch_end:
                sch_user.working_periods.append(Period(sch_start, sch_end))

        # add scheduled tasks
        for task in sch_by_user.get(user, []):
            match request.mode:
                case ScheduleMode.PESSIMISTIC:
                    task_start = max(toUTC(task.scheduled_pessimistic_start), now)
                    task_end = toUTC(task.scheduled_pessimistic_end)
                case ScheduleMode.AVERAGE:
                    task_start = max(toUTC(task.scheduled_average_start), now)
                    task_end = toUTC(task.scheduled_average_end)
                case ScheduleMode.OPTIMISTIC:
                    task_start = max(toUTC(task.scheduled_optimistic_start), now)
                    task_end = toUTC(task.scheduled_optimistic_end)
                case _:
                    assert False
            # for each task, only add periods overlapping with working schedule
            for idx, work_period in enumerate(sch_user.working_periods):
                period = Period(max(task_start, work_period.start), min(task_end, work_period.end))
                if period.end <= period.start:
                    continue
                sch_user.scheduled_tasks.append(
                    SchedulePeriod(period=period, text=task.name, color=task.project.color)
                )

    return result
