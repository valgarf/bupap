from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timedelta, timezone
from enum import Enum, auto
from functools import partial

import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import background_tasks, ui
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.permissions import default_team_roles
from bupap.ui import component
from bupap.ui.common import get_user
from bupap.ui.component import Errors, RequestInfo, Router


@dataclass
class GanttState:
    date: datetime

class ScheduleMode(Enum):
    PESSIMISTIC = auto()
    AVERAGE = auto()
    OPTIMISTIC = auto()

@dataclass
class Info:
    schedule_mode: ScheduleMode = ScheduleMode.AVERAGE

def create_teams_page():
    @Router.add("/teams")
    def teams_page(info: RequestInfo, session: sa.orm.Session):
        adduser_dialog = component.AddUser(cb_on_create=on_create)
        with ui.row():
            search_input = (
                ui.input(placeholder="Search not yet implemented").classes("grow").props("outlined")
            )
            with search_input.add_slot("append"):
                ui.icon("search")
            ui.button(on_click=adduser_dialog.open).props("icon=add").tooltip("add team").props(
                "outline"
            ).classes("text-black object-center m-auto")
        component.separator_line()
        for team in session.scalars(sa.select(db.Team).order_by(db.Team.name)):
            with ui.row().classes("p-4 hover:bg-slate-200").on(
                "click", partial(Router.get().open, f"/team/{team.id}/Overview")
            ):
                ui.element("div").classes("m-0 p-0")
                # for some reason the label sometimes is displayed without text if it is the first element in the row
                ui.label(team.name).classes("text-lg font-bold")
            component.separator_line()

    @Router.add("/team/{team_id:int}/{tab}")
    async def team_page(info: RequestInfo, session: sa.orm.Session):
        shown_team: db.Team | None = session.scalars(
            sa.select(db.Team).where(db.Team.id == info.params["team_id"])
        ).first()
        if not shown_team:
            raise HTTPException(
                status_code=404, detail=f"Team {info.params.get('team_id')} not found"
            )

        with ui.tabs() as tabs:
            ui.tab("Overview")
            ui.tab("Members")
            ui.tab("Schedule")

        with ui.tab_panels(tabs, value=info.params.get("tab", "Overview")).on(
            "transition", Router.tab_transition_event
        ).classes(
            "grow flex flex-col flex-nowrap [&>div]:grow [&>div]:flex [&>div]:flex-col [&>div]:flex-nowrap"
        ):
            with ui.tab_panel("Overview"):
                _team_page_overview(session, shown_team)
            with ui.tab_panel("Members"):
                _team_page_members(session, shown_team)
            with ui.tab_panel("Schedule").classes("p-0 grow flex flex-col flex-nowrap"):
                _team_page_schedule(session, shown_team, info)

    def _team_page_overview(session: sa.orm.Session, team: db.Team):
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("place-items-center gap-0"):
                # component.Avatar(shown_team).classes("h-40")
                ui.label(team.name).classes("font-bold text-xl mt-5")
                # ui.label("@" + shown_team.name).classes("text-slate-500")

    def _team_page_members(session: sa.orm.Session, team: db.Team):
        role_users = {}
        for arole in team.assigned_roles:
            role = arole.role
            role_users.setdefault(role.id, []).append(arole.user)
        roles = [session.get(db.Role, rid) for rid in role_users.keys()]
        role_ids = list(default_team_roles.keys())
        roles.sort(key=lambda r: role_ids.index(r.name))

        for role in roles:
            with ui.row().classes("p-4"):
                ui.element("div").classes("m-0 p-0")
                # for some reason the label sometimes is displayed without text if it is the first element in the row
                ui.label(role.name).classes("text-xl font-bold")
                component.separator_line()
            with ui.row().classes("p-4"):
                for user in role_users[role.id]:
                    component.user_card(user)

    @Errors.wrap_error("Failed to fetch Team Schedule Data")
    def _get_gantt_data(info: Info,  mode: component.GanttMode, start: datetime, end: datetime, user_data):
        now = datetime.utcnow()
        with db.session() as session:
            team_id = user_data["team_id"]
            team: db.Team = session.get(db.Team, team_id)
            users = set()
            for r in team.assigned_roles:
                if r.role.name == "Developer":
                    users.add(r.user)
            work_periods = session.scalars(
                sa.select(db.WorkPeriod)
                .join(db.User)
                .join(db.AssignedTeamRole)
                .join(db.Role)
                .where(db.WorkPeriod.started_at < end)
                .where(sa.or_(db.WorkPeriod.ended_at > start, db.WorkPeriod.ended_at == None))
                .where(db.AssignedTeamRole.team_id == team_id)
                .where(db.Role.name == "Developer")
            ).all()
            def _filter_on_schedule_mode(query):
                match info.schedule_mode:
                    case ScheduleMode.PESSIMISTIC:
                        return query.where(db.Task.scheduled_pessimistic_start < end).where(db.Task.scheduled_pessimistic_end > max(start, now))
                    case ScheduleMode.AVERAGE:
                        return query.where(db.Task.scheduled_average_start < end).where(db.Task.scheduled_average_end > max(start, now))
                    case ScheduleMode.OPTIMISTIC:
                        return query.where(db.Task.scheduled_optimistic_start < end).where(db.Task.scheduled_optimistic_end > max(start, now))
            scheduled: list[db.Task] = session.scalars(
                _filter_on_schedule_mode(sa.select(db.Task)
                .join(db.User, onclause=db.User.id == db.Task.scheduled_assignee_id)
                .join(db.AssignedTeamRole)
                .join(db.Role))
                .where(db.Task.task_state == db.TaskState.SCHEDULED)
                .where(db.AssignedTeamRole.team_id == team_id)
                .where(db.Role.name == "Developer")
            ).all()
            logger.debug(f"Schedule for team {team_id} found {len(work_periods)} entries")
            wps_by_user = {}
            sch_by_user: dict[db.User, list[db.Task]] = {}
            for wp in work_periods:
                wps_by_user.setdefault(wp.user, []).append(wp)
            for task in scheduled:
                sch_by_user.setdefault(task.scheduled_assignee, []).append(task)
            ordered_users = sorted(users, key=lambda u: u.name)
            data = component.GanttData(row_names=[], row_data=[], now=now)
            for idx, user in enumerate(ordered_users):
                data.row_names.append(user.full_name)
                row_data = component.GanttRowData(idx=idx, key=f"user#{user.id}", entries=[])
                data.row_data.append(row_data)
                for wp in wps_by_user.get(user, []):
                    text = ""
                    color = "#0000FF"
                    entry_type = component.GanttEntryType.BAR
                    if isinstance(wp, db.WorkPeriodTask):
                        text = wp.task.name
                        color = wp.task.project.color
                    if isinstance(wp, db.WorkPeriodTimesink):
                        text = wp.timesink.name
                        color = wp.timesink.color
                    if isinstance(wp, db.WorkPeriodWorking):
                        entry_type = component.GanttEntryType.BG
                        color = "#FFFFFF"
                    wp_ended = wp.ended_at or data.now
                    if wp_ended > start:
                        row_data.entries.append(
                            component.GanttEntryData(
                                key=f"WP#{wp.id}#",
                                start=wp.started_at,
                                end=wp_ended,
                                color=color,
                                text=text,
                                type_=entry_type,
                            )
                        )
                working_schedule = []
                for idx, (sch_start, sch_end) in enumerate(
                    db.iterate_schedule(user, max(start - timedelta(days=1), now).date())
                ):
                    sch_start = max(
                        sch_start.astimezone(timezone.utc).replace(tzinfo=None), start, now
                    )
                    if sch_start >= end:
                        break
                    sch_end = min(sch_end.astimezone(timezone.utc).replace(tzinfo=None), end)
                    if sch_start < sch_end:
                        row_data.entries.append(
                            component.GanttEntryData(
                                key=f"SCHEDULE#{idx}#",
                                start=sch_start,
                                end=sch_end,
                                color="#FFFFFF",
                                text="",
                                type_=component.GanttEntryType.BG,
                            )
                        )
                        working_schedule.append((sch_start, sch_end))

                for task in sch_by_user.get(user, []):
                    entry_type = component.GanttEntryType.BAR
                    text = task.name
                    color = task.project.color
                    match info.schedule_mode:
                        case ScheduleMode.PESSIMISTIC:
                            task_start = max(task.scheduled_pessimistic_start, now)
                            task_end = task.scheduled_pessimistic_end
                        case ScheduleMode.AVERAGE:
                            task_start = max(task.scheduled_average_start, now)
                            task_end = task.scheduled_average_end
                        case ScheduleMode.OPTIMISTIC:
                            task_start = max(task.scheduled_optimistic_start, now)
                            task_end = task.scheduled_optimistic_end
                        case _:
                            assert False
                    for idx, work_period in enumerate(working_schedule):
                        sch_start = max(task_start, work_period[0])
                        sch_end = min(task_end, work_period[1])
                        if sch_start < sch_end:
                            row_data.entries.append(
                                component.GanttEntryData(
                                    key=f"TASK#{task.id}#{idx}",
                                    start=sch_start,
                                    end=sch_end,
                                    color=color,
                                    text=text,
                                    type_=entry_type,
                                )
                            )

            return data

    def _open_clicked_item(key: str):
        class_name, db_id, idx = key.split("#")
        with db.session() as session:
            if class_name == "WP":
                wp = session.get(db.WorkPeriod, int(db_id))
                Router.get().open(f"/task/{wp.task.id}/Overview")
            elif class_name == "TASK":
                Router.get().open(f"/task/{db_id}/Overview")

    def _team_page_schedule(session: sa.orm.Session, team: db.Team, info: RequestInfo):
        el_gantt = None
        el_pick_date = None
        initial_isoformat = info.query_data.get("day")
        info = Info()
        if not initial_isoformat:
            initial_date = date.today()
        else:
            if isinstance(initial_isoformat, list):
                initial_isoformat = initial_isoformat[0]
            initial_date = date.fromisoformat(initial_isoformat)
        logger.info(initial_date)

        async def change_date(d: date):
            logger.warning(d)
            assert el_gantt is not None
            await Router.push_history_callable(query_data_update={"day": d.isoformat()})()
            el_gantt.set_day(d)

        def btn_left(_):
            assert el_pick_date is not None
            el_pick_date.set_date(el_pick_date.date - timedelta(days=1))

        def btn_right(_):
            assert el_pick_date is not None
            el_pick_date.set_date(el_pick_date.date + timedelta(days=1))

        def update(_):
            assert el_gantt is not None
            el_gantt.set_day(el_pick_date.date)

        with ui.row().classes("flex-nowrap items-center justify-center"):
            ui.button(on_click=btn_left).props("icon=keyboard_arrow_left flat")
            el_pick_date = component.PickDate(on_change=change_date, initial=initial_date)
            ui.button(on_click=btn_right).props("icon=keyboard_arrow_right flat")
            ui.toggle({ScheduleMode.OPTIMISTIC: "optimistic", ScheduleMode.AVERAGE:"average", ScheduleMode.PESSIMISTIC: "pessimistic"}, value=info.schedule_mode).bind_value(info, "schedule_mode").on("update:model-value", update)
            # .props(options=[
            #     {"label": 'One', "value": 'one'},
            #     {"label": 'Two', "value": 'two'},
            #     {"label": 'Three', "value": 'three'}
            # ], toggle_color="primary")
        el_gantt = component.Gantt(
            team.name, initial_date, {"team_id": team.id}, partial(_get_gantt_data, info), _open_clicked_item
        )
        el_gantt.classes("grow")
        el_gantt.set_day(initial_date)
        el_pick_date.set_date(initial_date, emit=False)

    def on_create():
        logger.info("reload")
        Router.get().reload()
