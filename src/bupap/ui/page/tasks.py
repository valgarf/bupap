from __future__ import annotations

from datetime import datetime, timedelta
from functools import partial

import sqlalchemy as sa
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui
from plotly import graph_objects as go
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.ui import component
from bupap.ui.common import format_date, format_timedelta, get_user
from bupap.ui.component import CPlotly, RequestInfo, Router
from bupap.ui.crud.task import get_estimate


def create_tasks_page():
    @Router.add("/task/{task_id:int}/{tab}")
    def task_page(info: RequestInfo, session: sa.orm.Session):
        shown_task: db.Task | None = session.scalars(
            sa.select(db.Task).where(db.Task.id == info.params["task_id"])
        ).first()
        if not shown_task:
            raise HTTPException(
                status_code=404, detail=f"Task {info.params.get('task_id')} not found"
            )

        with ui.tabs() as tabs:
            ui.tab("Overview")
            ui.tab("Activity")

        with ui.tab_panels(tabs, value=info.params.get("tab", "Overview")).on(
            "transition", Router.tab_transition_event
        ).classes(
            "grow flex flex-col flex-nowrap [&>div]:grow [&>div]:flex [&>div]:flex-col [&>div]:flex-nowrap"
        ):
            with ui.tab_panel("Overview"):
                _task_page_overview(session, shown_task)
            with ui.tab_panel("Activity"):
                _task_page_activity(session, shown_task)

    def _task_page_overview_assignee_overview(task: db.Task):
        with ui.row().classes("self-center items-center"):
            if not task.finished_at:
                component.user_card(task.scheduled_assignee)
                with ui.column().classes("gap-0"):
                    estimate = get_estimate(task.scheduled_assignee, task)
                    logger.warning(
                        f"{estimate.id=}, {estimate.user_id=}, {estimate.task_id=}\n    {estimate.expectation_optimistic=}\n    {estimate.expectation_average=}\n    {estimate.expectation_pessimistic=}"
                    )
                    s_end_opt = format_date(task.scheduled_optimistic_end)
                    s_end_pes = format_date(task.scheduled_pessimistic_end)
                    s_end_avg = format_date(task.scheduled_average_end)
                    if s_end_opt != s_end_pes:
                        lest = ui.label(
                            f"Estimated Completion: {s_end_opt} - {s_end_pes} (expected: {s_end_avg})"
                        )
                    else:
                        lest = ui.label(f"Estimated Completion: {s_end_avg}")
                    s_dur_opt = format_timedelta(estimate.expectation_optimistic)
                    s_dur_pes = format_timedelta(estimate.expectation_pessimistic)
                    s_dur_avg = format_timedelta(estimate.expectation_average)
                    ldur = ui.label(
                        f"Estimated Duration: {s_dur_opt} - {s_dur_pes} (expected: {s_dur_avg})"
                    )
                    now = datetime.utcnow()
                    work = timedelta()
                    for wp in task.work_periods:
                        work += ((wp.ended_at or now) - wp.started_at)
                    s_work = format_timedelta(work)
                    lwork = ui.label(
                        f"Spent time: {s_work}"
                    )
                    now = datetime.utcnow()
                    lest.classes("text-base")
                    ldur.classes("text-base")
                    lwork.classes("text-base")
            else:
                work = {}
                users = {}
                for wp in task.work_periods:
                    if wp.ended_at:
                        work[wp.user_id] = wp.duration + work.get(
                            wp.user_id, timedelta()
                        )
                        users[wp.user_id] = wp.user
                columns = [
                    {
                        "name": "name",
                        "label": "Name",
                        "field": "name",
                        "required": True,
                        "align": "left",
                    },
                    {
                        "name": "duration",
                        "label": "Duration",
                        "field": "duration",
                        "required": True,
                        "align": "right",
                        "sortOrder": "da",
                    },
                ]
                rows = [
                    {
                        "name": "@" + users[uid].name,
                        "duration": format_timedelta(work[uid]),
                    }
                    for uid in work.keys()
                ]
                if len(rows) > 1:
                    rows += [
                        {
                            "name": "TOTAL",
                            "duration": format_timedelta(sum(work.values())),
                        }
                    ]

                ui.table(columns=columns, rows=rows, row_key="name")

    def _task_page_overview(session: sa.orm.Session, task: db.Task):
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("place-items-center gap-0 items-stretch grow") as col:
                # component.Avatar(shown_team).classes("h-40")
                ui.label(task.name).classes("font-bold text-xl mt-5 self-center")
                with ui.row().classes("m-2 self-center"):
                    ui.badge(task.task_priority.name, color="green").classes("p-1 m-1 text-sm")
                    ui.badge(task.task_state.name, color="blue").classes("p-1 m-1 text-sm")
                if task.scheduled_assignee:
                    _task_page_overview_assignee_overview(task)
                else:
                    ui.label("Not yet scheduled").classes("text-base self-center")
                ui.markdown(task.description).classes().classes("mt-5")

                if task.history:
                    now = datetime.utcnow()
                    x = [h.date for h in task.history]
                    y = [h.scheduled_average_end for h in task.history]
                    y_low = [h.scheduled_optimistic_end for h in task.history]
                    y_high = [h.scheduled_pessimistic_end for h in task.history]
                    if task.finished_at:
                        x.append(task.finished_at)
                        y.append(task.finished_at)
                        y_low.append(task.finished_at)
                        y_high.append(task.finished_at)
                    elif task.scheduled_average_end:
                        x.append(now)
                        y.append(task.scheduled_average_end)
                        y_low.append(task.scheduled_optimistic_end)
                        y_high.append(task.scheduled_pessimistic_end)
                    xaxis_min = task.created_at
                    xaxis_max = max(x)
                    xaxis_size = xaxis_max - xaxis_min
                    xaxis_max += xaxis_size * 0.02
                    xaxis_min -= xaxis_size * 0.02
                    yaxis_min = task.created_at
                    yaxis_max = max(y_high + y)
                    yaxis_size = yaxis_max - yaxis_min
                    yaxis_max += yaxis_size * 0.2
                    yaxis_min -= yaxis_size * 0.05
                    fig = go.Figure()
                    fig.add_trace(
                        go.Scatter(
                            x=x, y=y_high, line=dict(color="rgba(0,0,0,0)"), name="pessimistic"
                        )
                    )
                    fig.add_trace(
                        go.Scatter(
                            x=x,
                            y=y_low,
                            line=dict(color="rgba(0,0,0,0)"),
                            fill="tonexty",
                            fillcolor="#81d4fa",
                            name="optimistic",
                        )
                    )
                    fig.add_trace(go.Scatter(x=x, y=y, line=dict(color="#646464"), name="average"))
                    fig.add_vline(x=task.created_at, line_width=3, line_color="#646464")
                    for wp in task.work_periods:
                        fig.add_vrect(x0=wp.started_at, x1=wp.ended_at or now, line_width=0, fillcolor="#9181fa", opacity=0.3)
                    fig.update_layout(
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis_range=[xaxis_min, xaxis_max],
                        yaxis_range=[yaxis_min, yaxis_max],
                        showlegend=False,
                        hovermode="closest"
                    )
                    # def ic_args(event):
                        # ic(event)
                    CPlotly(fig).classes("w-full h-40") # .on("data_click", ic_args)
                # ui.label("@" + shown_team.name).classes("text-slate-500")

    def _task_page_activity(session: sa.orm.Session, task: db.Task):
        # ui.label("TBD").classes("absolute-center")
        entries = []
        if task.finished_at:
            entries.append({"at": task.finished_at, "short": "finished"})
        for estimate in task.estimates:
            dur_opt = format_timedelta(estimate.expectation_optimistic)
            dur_pes = format_timedelta(estimate.expectation_pessimistic)
            dur_avg = format_timedelta(estimate.expectation_average)
            dur_orig = format_timedelta(estimate.estimated_duration)
            entries.append(
                {
                    "at": estimate.created_at,
                    "short": f"User @{estimate.user.name} added estimate",
                    "details": f"{estimate.estimate_type.name}, estimate: {dur_opt} - {dur_pes} (expectation: {dur_avg}), input estimate: {dur_orig}",
                }
            )
        for wp in task.work_periods:
            # s_start = format_date(wp.started_at)
            if wp.ended_at is not None:
                s_dur = format_timedelta(wp.duration)
                short = f"User @{wp.user.name} worked on task for {s_dur}"
            else:
                short = f"User @{wp.user.name} started working on task."
            entries.append({"at": wp.started_at, "short": short})
        entries.append({"at": task.created_at, "short": "created"})
        entries.sort(key=lambda el: el["at"], reverse=True)
        with ui.element("q-timeline").props("layout=comfortable"):
            for el in entries:
                s_title = el["short"]
                s_subtitle = format_date(el["at"])
                with ui.element("q-timeline-entry").props(
                    f'title="{s_title}" subtitle="{s_subtitle}"'
                ):
                    ui.element("div")._text = el.get("details")
