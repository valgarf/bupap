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
    separator_line().classes("w-full")
    if project_node.children:
        with ui.expansion(project.name) as header:
            header.props(
                f"expand-icon-toggle dense-toggle switch-toggle-side header-inset-level={project_node.depth}"
            )
            header.classes("w-full p-0 m-0 [&>div>div]:!gap-0 [&>div>div]:!pr-0")
            # NOTE: [&>div>div] will reach the content container, setting gap values for the sublist
            # But it also reaches the header row, so we have to be careful what we set here

            # header.on("click", partial(Router.get().open, f"/project/{project.id}/Overview"))
            with header.add_slot("header"):
                with ui.row().classes(
                    "px-0 py-4 min-h-0 hover:bg-slate-200 flex-1 cursor-pointer"
                ).on("click", partial(Router.get().open, f"/project/{project.id}/Overview")):
                    ui.element("div").classes("m-0 p-0")
                    # for some reason the label sometimes is displayed without text if it is the first element in the row
                    ui.label(project.name).classes("text-lg font-bold select-none")
            for idx, child in enumerate(project_node.children):
                recursive_create_list(child)
    else:
        with ui.row().classes(
            f"py-4 pl-[{inset_padding}px] hover:bg-slate-200 cursor-pointer w-full"
        ).on("click", partial(Router.get().open, f"/project/{project.id}/Overview")):
            ui.element("div").classes("m-0 p-0")
            # for some reason the label sometimes is displayed without text if it is the first element in the row
            ui.label(project.name).classes("text-lg font-bold select-none")


def project_tree(projects: Iterable[db.Project], root: set[db.Project] | None = None):
    with ui.row().classes("w-full"):
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

    with ui.column().classes("gap-0 w-full"):
        project_tree = Tree(projects, root_elements=root)
        for root_project in project_tree.children:
            recursive_create_list(root_project)
        separator_line()
