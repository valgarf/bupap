from __future__ import annotations

import math
from dataclasses import asdict
from datetime import timedelta
from functools import partial

import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui
from plotly import graph_objects as go
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.ui import component
from bupap.ui.common import format_date, format_time, format_timedelta, get_user
from bupap.ui.component import RequestInfo, Router
from bupap.ui.crud.task import get_estimate_statistics


def round_td(td, delta):
    return round(td.total_seconds() / delta.total_seconds()) * delta.total_seconds()


def format_td(td):
    h = td // timedelta(seconds=3600)
    m = (td - h * timedelta(seconds=3600)) // timedelta(seconds=60)
    return f"{h:02}:{m:02}"


def create_users_page():
    @Router.add("/users")
    def users_page(info: RequestInfo, session: sa.orm.Session):
        adduser_dialog = component.AddUser(cb_on_create=on_create)
        with ui.row():
            search_input = (
                ui.input(placeholder="Search not yet implemented").classes("grow").props("outlined")
            )
            with search_input.add_slot("append"):
                ui.icon("search")
            ui.button(on_click=adduser_dialog.open).props("icon=add").tooltip("add user").props(
                "outline"
            ).classes("text-black object-center m-auto")
        component.separator_line()
        for user in session.scalars(sa.select(db.User).order_by(db.User.full_name)):
            with ui.row().classes("p-4 hover:bg-slate-200").on(
                "click", partial(Router.get().open, f"/user/{user.id}/Overview")
            ):
                component.Avatar(user).classes("h-14")
                with ui.column().classes("gap-0 mt-2"):
                    ui.label(user.full_name).classes("text-base font-bold")
                    ui.label("@" + user.name).classes("text-sm text-slate-500")
            component.separator_line()

    def on_create():
        logger.info("reload")
        Router.get().reload()

    @Router.add("/user/{user_id:int}/{tab}")
    def user_page(info: RequestInfo, session: sa.orm.Session):
        shown_user: db.User | None = session.scalars(
            sa.select(db.User).where(db.User.id == info.params["user_id"])
        ).first()
        if not shown_user:
            raise HTTPException(status_code=404, detail="Item not found")

        with ui.tabs() as tabs:
            ui.tab("Overview")
            ui.tab("Activity")

        with ui.tab_panels(tabs, value=info.params.get("tab", "Overview")).on(
            "transition", Router.tab_transition_event
        ).classes(
            "grow flex flex-col flex-nowrap [&>div]:grow [&>div]:flex [&>div]:flex-col [&>div]:flex-nowrap"
        ):
            with ui.tab_panel("Overview"):
                _user_page_overview(session, shown_user)
            with ui.tab_panel("Activity"):
                _user_page_activity(session, shown_user)

    def _user_page_overview(session: sa.orm.Session, user: db.User):
        modify_user_dialog = component.ModifyUser(user, cb_on_modify=on_create)
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("place-items-center gap-0"):
                component.Avatar(user).classes("h-40")
                ui.label(user.full_name).classes("font-bold text-xl mt-5")
                ui.label("@" + user.name).classes("text-slate-500 mb-5")
                ui.button("Edit Profile", on_click=modify_user_dialog.open)
        project_data = {}
        for wp in user.work_periods:
            if isinstance(wp, db.WorkPeriodTask):
                data = project_data.setdefault(
                    wp.task.project.id,
                    {
                        "project": wp.task.project,
                        "total_duration": timedelta(),
                        "task_open_ids": set(),
                        "task_done_ids": set(),
                    },
                )
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
        project_list = sorted(
            project_data.values(), key=lambda data: data["total_duration"], reverse=True
        )

        with ui.column().classes("items-center mt-5"):
            with ui.grid(columns=3).classes("mb-10").style(
                "grid-template-columns: minmax(0px, 1fr) auto minmax(0px, 1fr)"
            ):
                for project_data in project_list:
                    project = project_data["project"]
                    with ui.card() as card:
                        card.classes("p-4 hover:bg-slate-200")
                        card.on(
                            "click", partial(Router.get().open, f"/project/{project.id}/Overview")
                        )
                        ui.label(project.name).classes("text-lg font-bold")
                    with ui.column().classes("gap-0 py-2 pl-2 items-end"):
                        dur = project_data["total_duration"]
                        dur -= timedelta(seconds=dur.total_seconds() % 60)
                        num_tasks_todo = len(project_data["task_open_ids"])
                        num_tasks_finished = len(project_data["task_done_ids"])
                        ui.label(f"time spent:")
                        ui.label(f"tasks open:")
                        ui.label(f"tasks done:")
                    with ui.column().classes("gap-0 py-2 items-start"):
                        dur = project_data["total_duration"]
                        dur -= timedelta(seconds=dur.total_seconds() % 60)
                        num_tasks_todo = len(project_data["task_open_ids"])
                        num_tasks_finished = len(project_data["task_done_ids"])
                        ui.label(f"{dur}")
                        ui.label(f"{num_tasks_todo}")
                        ui.label(f"{num_tasks_finished}")

            for db_estimate_type in session.scalars(sa.select(db.EstimateType)):
                existing = [
                    s for s in user.estimate_statistics if s.estimate_type == db_estimate_type
                ]
                latest = None
                if existing:
                    existing = existing[0]
                    latest = existing.evaluated
                else:
                    existing = db_estimate_type
                stat = get_estimate_statistics(user.id, db_estimate_type.id, latest, session)
                if stat and len(stat.data) > 5:
                    plot_data = [el.value for el in stat.data]
                    if not stat.relative:
                        plot_data = [el / 3600 for el in plot_data]
                    # plot
                    with ui.row().classes("g-5"):
                        with ui.column().classes("gap-0"):
                            ui.label(stat.estimate_type_name).classes("text-lg text-bold my-5")
                            o, p, a = (
                                existing.shift_optimistic,
                                existing.shift_pessimistic,
                                existing.shift_average,
                            )
                            unit = ""
                            if stat.relative:
                                ui.label(f"range: {o:.2} - {p:.2}")
                                ui.label(f"average: {a:.2}")
                            if not stat.relative:
                                o, p, a = [
                                    format_td(
                                        round_td(timedelta(seconds=el), timedelta(seconds=60))
                                    )
                                    for el in [o, p, a]
                                ]
                                ui.label(f"range: {o} - {p} hours")
                                ui.label(f"average: {a}")
                            if isinstance(existing, db.EstimateStatistics):
                                ui.label(f"#datapoints: {existing.num_datapoints} ")
                                ui.label(f"{existing.evaluated.strftime(r'%Y-%m-%d %H:%M')} ")
                            else:
                                ui.label(f"default values, not enough data")

                        mean = sum(plot_data) / len(plot_data)
                        stddev = math.sqrt(
                            sum((el - mean) ** 2 for el in plot_data) / len(plot_data)
                        )
                        size = stddev / len(plot_data) ** 0.4
                        nbins = None
                        if size > 0:
                            nbins = math.ceil((max(plot_data) - min(plot_data)) / size)
                        if nbins == 0:
                            nbins = None
                        fig = go.Figure(go.Histogram(x=plot_data, nbinsx=nbins))
                        fig.update_layout(
                            margin=dict(l=0, r=0, t=0, b=0),
                            xaxis_title="factor" if stat.relative else "hours",
                        )
                        ui.plotly(fig).classes("w-80 h-60")

                    # data table
                    with ui.expansion("Data").classes("text-base text-lg").style(
                        "width: 100vw; max-width: min(100%,800px)"
                    ) as expansion:
                        # columns = [
                        #     {'name': 'task_id', 'label': 'Task Id', 'field': 'task_id', 'sortable': False, 'required': True, 'aligned': 'left'},
                        #     {'name': 'task_name', 'label': 'Task Name', 'field': 'task_name', 'sortable': False, 'required': True, 'aligned': 'left'},
                        #     {'name': 'estimate', 'label': 'Estimated Time', 'field': 'estimate', 'sortable': True, 'required': True, 'aligned': 'right'},
                        #     {'name': 'actual_work', 'label': 'Worked Time', 'field': 'actual_work', 'sortable': True, 'required': True, 'aligned': 'right'},
                        #     {'name': 'start', 'label': 'Start', 'field': 'start', 'sortable': True, 'required': True, 'aligned': 'right'},
                        #     {'name': 'end', 'label': 'End', 'field': 'end', 'sortable': True, 'required': True, 'aligned': 'right'},
                        #     {'name': 'value', 'label': 'Value', 'field': 'value', 'sortable': True, 'required': True, 'aligned': 'right'},
                        # ]
                        columns = [
                            {"headerName": "Task Id", "field": "task_id", "sortable": True},
                            {"headerName": "Task Name", "field": "task_name", "sortable": True},
                            {
                                "headerName": "Value",
                                "field": "value",
                                "type": "rightAligned",
                                "sortable": True,
                            },
                            {
                                "headerName": "Estimated Time",
                                "field": "estimate",
                                "type": "rightAligned",
                                "sortable": True,
                            },
                            {
                                "headerName": "Worked Time",
                                "field": "actual_work",
                                "type": "rightAligned",
                                "sortable": True,
                            },
                            {
                                "headerName": "Start",
                                "field": "start",
                                "type": "rightAligned",
                                "sortable": True,
                            },
                            {
                                "headerName": "End",
                                "field": "end",
                                "type": "rightAligned",
                                "sortable": True,
                            },
                        ]
                        rows = [asdict(el) for el in stat.data]
                        for r in rows:
                            r["start"] = r["start"].strftime(r"%Y-%m-%d %H:%M")
                            r["end"] = r["end"].strftime(r"%Y-%m-%d %H:%M")
                            r["estimate"] = format_td(r["estimate"])
                            r["actual_work"] = format_td(r["actual_work"])
                            r["value"] = round(r["value"], 2)
                        # tbl = ui.table(columns=columns, rows=rows, row_key='task_id')
                        # with ui.row():#.style("max-width: 500px; width: 100vw"):
                        tbl = ui.aggrid(
                            {"columnDefs": columns, "rowData": rows, "domLayout": "autoHeight"}
                        )
                        tbl.classes("")

                        @component.Errors.wrap_error("Failed to navigate to task")
                        def handle_click(evt):
                            logger.info(evt)
                            task_id = evt.args["data"]["task_id"]
                            component.Router.get().open(f"/task/{task_id}/Overview")

                        tbl.on("cellClicked", handle_click)

                        # TODO: resize expansion size to table?
                        async def on_show(self, *args):
                            logger.info(args)
                            ui.run_javascript(
                                f"""
                                getElement({tbl.id}).gridOptions.columnApi.autoSizeAllColumns();
                            """
                            )

                        expansion.on("afterShow", on_show)

    def _user_page_activity(session: sa.orm.Session, user: db.Task):
        # ui.label("TBD").classes("absolute-center")
        entries = []

        for wp in user.work_periods:
            # s_start = format_date(wp.started_at)
            if isinstance(wp, db.WorkPeriodTask):
                if wp.ended_at is not None:
                    s_dur = format_timedelta(wp.duration)
                    short = f"Worked on task {wp.task.name} for {s_dur}"
                else:
                    short = f"Started working on task {wp.task.name}."
                entries.append({"at": wp.started_at, "short": short})
            elif isinstance(wp, db.WorkPeriodWorking):
                entries.append({"at": wp.started_at, "short": "Started working", "order": -10})
                if wp.ended_at is not None:
                    entries.append({"at": wp.ended_at, "short": "Stopped working", "order": 10})
            elif isinstance(wp, db.WorkPeriodTimesink):
                if wp.ended_at is not None:
                    s_dur = format_timedelta(wp.duration)
                    short = f"Spent {s_dur} on {wp.timesink.name}."
                else:
                    short = f"Started with {wp.timesink.name}."
                entries.append({"at": wp.started_at, "short": short})
        entries.sort(key=lambda el: (el["at"], el.get("order", 0)), reverse=True)
        with ui.element("q-timeline").props("layout=comfortable"):
            previous_el = None
            previous_date = None
            previous_time = None
            for el in entries:
                s_title = el["short"]
                s_date = format_date(el["at"])
                s_time = format_time(el["at"])
                if previous_date == s_date and previous_el is not None:
                    previous_el.props(f'subtitle="{previous_time}"')
                previous_date = s_date
                previous_time = s_time
                s_subtitle = f"{s_date} {s_time}"
                with ui.element("q-timeline-entry") as el_timeline_entry:
                    el_timeline_entry.props(f'title="{s_title}" subtitle="{s_subtitle}"')
                    previous_el = el_timeline_entry
                    ui.element("div")._text = el.get("details")
