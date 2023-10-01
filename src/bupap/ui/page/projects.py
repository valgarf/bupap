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
from bupap.ui.common import Tree, TreeNode, get_user
from bupap.ui.component import RequestInfo, Router

# def recursive_create_list(project_node: TreeNode[db.Project]):
#     project = project_node.value
#     children_pane: ui.element = None
#     icon: ui.icon = None

#     def toggle_children(*_):
#         assert children_pane is not None
#         assert icon is not None
#         visible = not children_pane.visible
#         children_pane.set_visibility(visible)
#         if visible:
#             icon.props["name"] = "arrow_drop_down"
#         else:
#             icon.props["name"] = "arrow_right"

#     with ui.row().classes("p-0 items-center gap-0"):
#         if project_node.children:
#             icon = (
#                 ui.icon("arrow_right", color="primary", size="xl")
#                 .classes("m-0 p-0")
#                 .on("click", toggle_children)
#             )
#         else:
#             ui.element("div").classes("h-[48px] w-[48px]")
#         with ui.row().classes("p-4 pl-0 hover:bg-slate-200 flex-1").on(
#             "click", partial(Router.get().open, f"/project/{project.id}/Overview")
#         ):
#             ui.element("div").classes("m-0 p-0")
#             # for some reason the label sometimes is displayed without text if it is the first element in the row
#             ui.label(project.name).classes("text-lg font-bold")
#     component.separator_line()
#     if project_node.children:
#         with ui.element("div").classes("p-0 pl-8 gap-0") as children_pane:
#             for child in project_node.children:
#                 recursive_create_list(child)


def recursive_create_list(project_node: TreeNode[db.Project]):
    project = project_node.value
    children_pane: ui.element = None
    icon: ui.icon = None

    # NOTE: 16: left padding for depth 0; 56: size of arrow icon; 56: inset per level
    inset_padding = 16 + 56 + project_node.depth * 56
    component.separator_line().classes(f"ml-[{inset_padding-56-16}px]")
    if project_node.children:
        with ui.expansion(project.name) as header:
            header.props(
                f"expand-icon-toggle dense-toggle switch-toggle-side header-inset-level={project_node.depth}"
            )
            header.classes("p-0 m-0")
            # header.on("click", partial(Router.get().open, f"/project/{project.id}/Overview"))
            with header.add_slot("header"):
                with ui.row().classes("p-4 pl-0 hover:bg-slate-200 flex-1").on(
                    "click", partial(Router.get().open, f"/project/{project.id}/Overview")
                ):
                    ui.element("div").classes("m-0 p-0")
                    # for some reason the label sometimes is displayed without text if it is the first element in the row
                    ui.label(project.name).classes("text-lg font-bold")
            for idx, child in enumerate(project_node.children):
                recursive_create_list(child)
    else:
        with ui.row().classes(f"p-4 pl-[{inset_padding}px] hover:bg-slate-200").on(
            "click", partial(Router.get().open, f"/project/{project.id}/Overview")
        ):
            ui.element("div").classes("m-0 p-0")
            # for some reason the label sometimes is displayed without text if it is the first element in the row
            ui.label(project.name).classes("text-lg font-bold")


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

        project_tree = Tree(session.scalars(sa.select(db.Project).order_by(db.Project.name)))
        for root_project in project_tree.children:
            recursive_create_list(root_project)
        component.separator_line()
        # for project_node in project_tree.depths_first():
        #     project = project_node.value
        #     with ui.row().classes("p-4 hover:bg-slate-200").on(
        #         "click", partial(Router.get().open, f"/project/{project.id}/Overview")
        #     ):
        #         ui.element("div").classes("m-0 p-0")
        #         # for some reason the label sometimes is displayed without text if it is the first element in the row
        #         ui.label(project.name).classes("text-lg font-bold")
        #     component.separator_line()

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
