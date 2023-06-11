from __future__ import annotations

from functools import partial

import sqlalchemy as sa
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.ui import component
from bupap.ui.common import get_user
from bupap.ui.component import RequestInfo, Router


def create_projects_page():
    @Router.add("/projects")
    def projects_page(info: RequestInfo, session: sa.orm.Session):
        # adduser_dialog = component.AddUser(cb_on_create=on_create)
        with ui.row():
            search_input = (
                ui.input(placeholder="Search not yet implemented").classes("grow").props("outlined")
            )
            with search_input.add_slot("append"):
                ui.icon("search")
            ui.button(
                # on_click=adduser_dialog.open
            ).props("icon=add").tooltip("add project").props("outline").classes(
                "text-black object-center m-auto"
            )
        component.separator_line()
        for project in session.scalars(sa.select(db.Project).order_by(db.Project.name)):
            with ui.row().classes("p-4 hover:bg-slate-200").on(
                "click", partial(Router.get().open, f"/project/{project.id}/Overview")
            ):
                ui.element("div").classes("m-0 p-0")
                # for some reason the label sometimes is displayed without text if it is the first element in the row
                ui.label(project.name).classes("text-lg font-bold")
            component.separator_line()

    @Router.add("/project/{project_id:int}/{tab}")
    def project_page(info: RequestInfo, session: sa.orm.Session):
        shown_project: db.Project | None = session.scalars(
            sa.select(db.Project).where(db.Project.id == info.params["project_id"])
        ).first()
        if not shown_project:
            raise HTTPException(
                status_code=404, detail=f"Project {info.params.get('project_id')} not found"
            )

        with ui.tabs() as tabs:
            ui.tab("Overview")
            ui.tab("Board")

        with ui.tab_panels(tabs, value=info.params.get("tab", "Overview")).on(
            "transition", Router.tab_transition_event
        ).classes(
            "grow flex flex-col flex-nowrap [&>div]:grow [&>div]:flex [&>div]:flex-col [&>div]:flex-nowrap"
        ):
            with ui.tab_panel("Overview"):
                _project_page_overview(session, shown_project)
            with ui.tab_panel("Board").classes(
                "p-0 grow flex flex-col flex-nowrap"
            ):  # flex flex-col flex-nowrap [&>div]:flex  [&>div]:flex-ol  [&>div]:flex-nowrap"):
                _project_page_tasks(session, shown_project)

    def _project_page_overview(session: sa.orm.Session, project: db.Project):
        with ui.row().classes("w-full justify-center"):
            with ui.column().classes("place-items-center gap-0"):
                # component.Avatar(shown_team).classes("h-40")
                ui.label(project.name).classes("font-bold text-xl mt-5")
                # ui.label("@" + shown_team.name).classes("text-slate-500")

    def _project_page_tasks(session: sa.orm.Session, project: db.Project):
        with ui.row().classes("p-4 overflow-x-auto grow flex-nowrap items-stretch"):
            for state in db.TaskState:
                tasks = [t for t in project.tasks if t.task_state == state]
                with ui.card().classes("min-w-[350pt] items-stretch"):
                    ui.label(state.name).classes("font-bold text-xl mt-5")
                    with ui.element("q-scroll-area").classes("m-0 p-0 pr-2 max-w-[330] grow"):
                        with ui.column().classes("p-0 m-1 gap-2 items-stretch"):
                            for task in tasks:
                                with ui.card().classes("hover:bg-slate-200").on(
                                    "click", partial(Router.get().open, f"/task/{task.id}/Overview")
                                ):
                                    ui.label(task.name).classes("text-base font-bold")
                                    with ui.row():
                                        ui.badge(task.task_priority.name, color="green").classes(
                                            "p-1 m-1"
                                        )
