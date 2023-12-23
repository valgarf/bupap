from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated

import sqlalchemy as sa
import strawberry

from bupap import db
from bupap.common import toUTC

from ..common.db_type import DBConvExtension, DBType, map_to_db
from .common import Timedelta
from .estimate import EstimateStatistics

if TYPE_CHECKING:
    from .project import Project


@strawberry.type
class UserActivity:
    at: datetime
    short: str
    details: str = ""
    order: strawberry.Private[int] = 0


@strawberry.type
class UserProjectSummary:
    project: Annotated["Project", strawberry.lazy(".project")] = strawberry.field(
        extensions=[DBConvExtension()]
    )
    total_duration: Timedelta
    num_tasks_open: int
    num_tasks_done: int


@strawberry.type
class User(DBType, strawberry.relay.Node):
    _db_table = db.User
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    full_name: str = map_to_db()
    rendered_avatar: str = map_to_db()

    @strawberry.field
    def activity(self) -> list[UserActivity]:
        return resolve_activity(self)

    @strawberry.field
    def project_summaries(self) -> list[UserProjectSummary]:
        return resolve_project_summaries(self)

    @strawberry.field
    def estimate_statistics(self) -> list[EstimateStatistics]:
        return resolve_estimate_statistics(self)


def format_timedelta(td: timedelta):
    m = round(td.total_seconds() / 60)
    h = m // 60
    m -= h * 60
    result = f"{h}:{m:02}"
    return result


def resolve_project_summaries(user: User) -> list[UserProjectSummary]:
    db_user: db.User = user.db_obj

    project_data = {}

    def _get_task_data(task):
        return project_data.setdefault(
            task.project.id,
            {
                "project": task.project,
                "total_duration": timedelta(),
                "task_open_ids": set(),
                "task_done_ids": set(),
            },
        )

    for wp in db_user.work_periods:
        if isinstance(wp, db.WorkPeriodTask):
            data = _get_task_data(wp.task)
            if wp.duration is not None:
                data["total_duration"] += wp.duration
            if wp.task.task_state in [
                # db.TaskState.IN_PROGRESS,
                db.TaskState.PLANNING,
                db.TaskState.SCHEDULED,
            ]:
                data["task_open_ids"].add(wp.task.id)
            if wp.task.task_state in [db.TaskState.DONE]:
                data["task_done_ids"].add(wp.task.id)
    for task in db_user.tasks:
        if task.task_state in [db.TaskState.DONE]:
            continue
        _get_task_data(task)["task_open_ids"].add(task.id)

    projects = sorted(project_data.values(), key=lambda data: data["total_duration"], reverse=True)

    return [
        UserProjectSummary(
            project=p["project"],
            total_duration=p["total_duration"],
            num_tasks_open=len(p["task_open_ids"]),
            num_tasks_done=len(p["task_done_ids"]),
        )
        for p in projects
    ]


def resolve_activity(user: User) -> list[UserActivity]:
    # ui.label("TBD").classes("absolute-center")
    entries: list[UserActivity] = []

    for wp in user.db_obj.work_periods:
        # s_start = format_date(wp.started_at)
        if isinstance(wp, db.WorkPeriodTask):
            if wp.ended_at is not None:
                s_dur = format_timedelta(wp.duration)
                short = f"Worked on task {wp.task.name} for {s_dur}"
            else:
                short = f"Started working on task {wp.task.name}."
            entries.append(UserActivity(at=toUTC(wp.started_at), short=short))
        elif isinstance(wp, db.WorkPeriodWorking):
            entries.append(
                UserActivity(at=toUTC(wp.started_at), short="Started working", order=-10)
            )
            if wp.ended_at is not None:
                entries.append(
                    UserActivity(at=toUTC(wp.ended_at), short="Stopped working", order=10)
                )
        elif isinstance(wp, db.WorkPeriodTimesink):
            if wp.ended_at is not None:
                s_dur = format_timedelta(wp.duration)
                short = f"Spent {s_dur} on {wp.timesink.name}."
            else:
                short = f"Started with {wp.timesink.name}."
            entries.append(UserActivity(at=toUTC(wp.started_at), short=short))
    entries.sort(key=lambda el: (el.at, el.order), reverse=True)
    return entries


def resolve_estimate_statistics(
    user: User,
) -> EstimateStatistics | None:
    result = []
    db_user: db.User = user.db_obj
    session = sa.inspect(db_user).session
    for db_estimate_type in session.scalars(sa.select(db.EstimateType)):
        existing = [s for s in db_user.estimate_statistics if s.estimate_type == db_estimate_type]
        if not existing:
            continue
            # we could still show the data
        existing.sort(key=lambda s: s.evaluated)
        result.append(EstimateStatistics(existing[-1]))
    return result
