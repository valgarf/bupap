from functools import partial
from typing import Iterable

from nicegui import ui

from bupap import db
from bupap.ui.common import Tree, TreeNode

from .router import Router
from .separator_line import separator_line


def recursive_create_list(project_node: TreeNode[db.Project]):
    project = project_node.value
    children_pane: ui.element = None
    icon: ui.icon = None

    # NOTE: 16: left padding for depth 0; 25: size of arrow icon; 56: inset per level
    inset_padding = 16 + 25 + project_node.depth * 56
    separator_line()  # .classes(f"ml-[{inset_padding-56-16}px]")
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


def project_tree(projects: Iterable[db.Project], root: set[db.Project] | None = None):
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

    project_tree = Tree(projects, root_elements=root)
    for root_project in project_tree.children:
        recursive_create_list(root_project)
    separator_line()
