from __future__ import annotations

from datetime import UTC, datetime, timedelta
from functools import partial

import sqlalchemy as sa
from fastapi import Request
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse
from loguru import logger
from nicegui import ui
from starlette.middleware.sessions import SessionMiddleware

from bupap import db
from bupap.db.database import get_database
from bupap.ui import component
from bupap.ui.common import Tree, TreeNode, get_user
from bupap.ui.component import RequestInfo, Router, project_tree
from bupap.ui.component.kanban import Kanban, KanbanCardData, KanbanData, KanbanLaneData, KanbanTag
from bupap.ui.crud.task import TaskDone, get_estimate, task_done

# from bupap.ui.component.kanban_card import KanbanCard


def create_projects_page():
    @Router.add("/projects")
    def projects_page(info: RequestInfo, session: sa.orm.Session):
        project_tree(session.scalars(sa.select(db.Project).order_by(db.Project.name)))

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
                if project.parent:
                    with ui.element("q-breadcrumbs"):
                        for p in project.parents:
                            ui.element("q-breadcrumbs-el").props(f'label="{p.name}"').classes(
                                "select-none cursor-pointer"
                            ).on("click", partial(Router.get().open, f"/project/{p.id}/Overview"))
                        ui.element("q-breadcrumbs-el").props(f'label="{project.name}"')
                # component.Avatar(shown_team).classes("h-40")
                ui.label(project.name).classes("font-bold text-xl mt-5")
                # ui.label("@" + shown_team.name).classes("text-slate-500")
        direct_children = project.children
        if direct_children:
            project_tree(project.recursive_children, root=direct_children)

    def _project_page_tasks(session: sa.orm.Session, project: db.Project):
        pass
        data = KanbanData()
        for prio in db.TaskPriority:
            data.priorities.append(
                KanbanTag(
                    prio.text,
                    prio.default_color,
                    prio.default_text_color,
                )
            )
        for state in db.TaskState:
            lane = KanbanLaneData(state.name, state.name)
            data.lanes[lane.id] = lane
            data.lane_order.append(lane.id)
            if state in [db.TaskState.REQUEST, db.TaskState.PLANNING, db.TaskState.SCHEDULED]:
                lane.priority_sorted = True
            if state in [db.TaskState.DONE, db.TaskState.DONE]:
                lane.finished_sorted = True
            tasks = [t for t in project.tasks if t.task_state == state]
            if not lane.finished_sorted:
                tasks.sort(key=lambda t: t.order_id or 0)
            else:
                tasks.sort(key=lambda t: t.finished_at, reverse=True)
            for t in tasks:
                active = False
                progress = None
                if t.scheduled_assignee and t.finished_at is None:
                    total_work = timedelta(0)
                    for wp in t.work_periods:
                        if wp.ended_at:
                            total_work += wp.duration
                        else:
                            active = True
                    if total_work:
                        est = get_estimate(t.scheduled_assignee, t)
                        progress = (
                            total_work / est.expectation_pessimistic,
                            total_work / est.expectation_average,
                            total_work / est.expectation_optimistic,
                        )
                        progress = tuple(int(min(p, 1) * 100) for p in progress)
                card = KanbanCardData(
                    title=t.name,
                    id=t.id,
                    lane_id=lane.id,
                    parent_id=t.parent_id,
                    depth=0,
                    tags=[],
                    detached=not t.attached,
                    progress=progress,
                    active=active,
                    priority=t.task_priority.text,
                    link=True,
                    finished_at=t.finished_at,
                )
                lane.card_order.append(card.id)
                data.cards[card.id] = card
        for card in list(data.cards.values()):
            if card.parent_id is not None:
                if not card.parent_id in data.cards:
                    print(f"Unkown card id {card.parent_id}")
                    del data.cards[card.id]
                else:
                    data.cards[card.parent_id].children_order.append(card.id)

        def _set_depth_rec(card, value: int = 0):
            card.depth = value
            for child_id in card.children_order:
                _set_depth_rec(data.cards[child_id], value + 1)

        for card in data.cards.values():
            if card.parent_id != None:
                continue
            _set_depth_rec(card)

        kanban = Kanban(data=data)

        project_id = project.id

        def moved_cards(data):
            with get_database().session() as session:
                state = db.TaskState[data.args["lane"]]
                stmt = (
                    sa.select(db.Task)
                    .where(db.Task.project_id == project_id)
                    .where(db.Task.task_state == state)
                )
                lane_order = session.scalars(stmt)
                tasks = {
                    c["id"]: (c["order"], c["detached"], session.get(db.Task, c["id"]))
                    for c in data.args["cards"]
                }
                changed_tasks = sorted(tasks.values())
                changed_task_keys = set(tasks.keys())
                changed_task_children_ids = {
                    rc.id for t in tasks.values() for rc in t[2].get_recursive_children()
                }
                lane_order = [
                    t
                    for t in lane_order
                    if t.id not in changed_task_keys and t.id not in changed_task_children_ids
                ]
                lane_order.sort(key=lambda t: t.order_id or 0)
                for tdata in changed_tasks:
                    idx = tdata[0]
                    lane_order.insert(idx, tdata[2])
                    tdata[2].task_state = state
                    for rc in tdata[2].get_recursive_children():
                        idx += 1
                        rc.task_state = state
                        lane_order.insert(idx, rc)
                for idx, t in enumerate(lane_order, start=0):
                    # msg = f"{t.id}: {t.order_id} -> {idx}"
                    t.order_id = idx

                    if t.id in changed_task_keys:
                        # msg += f" ({t.attached} -> {not tasks[t.id][1]})"
                        t.attached = not tasks[t.id][1]
                    # msg += f" {t.name}"
                    # print(msg)
                if state in [db.TaskState.DONE, db.TaskState.DISCARDED]:
                    for tdata in changed_tasks:
                        tdone = TaskDone(tdata[2].id, datetime.now(UTC))
                        task_done(tdone, session, discarded=(state == db.TaskState.DISCARDED))
                else:
                    # TODO wrap in crud function
                    def _unset_finished(t):
                        if t.finished_at is not None:
                            t.finished_at = None
                        for c in t.children:
                            if c.attached:
                                _unset_finished(c)

                    for tdata in changed_tasks:
                        _unset_finished(tdata[2])

                # session.rollback()
                # TODO: do we need to close the gaps in the order id in the source lane?

            # print(data)

        kanban.on("moved_cards", moved_cards)

        def open_link(evt):
            task_id = evt.args["id"]
            Router.get().open(f"/task/{task_id}/Overview")

        kanban.on("open_link", open_link)
