from datetime import datetime
from typing import Self

import sqlalchemy as sa
import strawberry
from pytz import UTC

from bupap import db
from bupap.common.enums import TaskState
from bupap.ui.crud.task import task_done
from bupap.ui.viewmodel.task import TaskDone

from ..common.context import InfoContext
from ..common.db_type import DBConvExtension, DBType, map_to_db
from .common import MutationResult
from .tag import Tag
from .task import Task


def _task_sort_key(db_task: db.Task):
    result = [
        db_task.task_state.name,
    ]
    if db_task.task_state in [db.TaskState.DONE, db.TaskState.DISCARDED]:
        result.append(db_task.finished_at)
    else:
        result.append(-db_task.order_id or 0)
    return tuple(result)


@strawberry.type
class Project(DBType, strawberry.relay.Node):
    _db_table = db.Project
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    parent: Self | None = map_to_db()

    @strawberry.field(extensions=[DBConvExtension()])
    def tasks(self) -> list[Task]:
        return sorted(self.db_obj.tasks, key=_task_sort_key, reverse=True)

    @strawberry.field()
    def children(self, recursive: bool = False) -> list[Self]:
        db_self: db.Project = self.db_obj
        if recursive:
            result = list(db_self.recursive_children)
        else:
            result = list(db_self.children)
        return [Project(db_child) for db_child in result]

    @strawberry.field()
    def parents(self) -> list[Self]:
        result = []
        p = self.db_obj.parent
        while p != None:
            result.append(Project(p))
            p = p.parent
        return result

    @strawberry.field()
    def priorities(self) -> list[Tag]:
        result = []
        for prio in db.TaskPriority:
            result.append(
                Tag(
                    key=prio.name,
                    text=prio.text,
                    color=prio.default_color,
                )
            )
        return result


@strawberry.input
class MovedTaskInput:
    task_db_id: int
    order_id: int
    detached: bool


@strawberry.type
class ProjectMutation:
    @strawberry.field
    def moved_tasks(
        self, info: InfoContext, project_db_id: int, state: TaskState, tasks: list[MovedTaskInput]
    ) -> MutationResult:
        return resolve_moved_tasks(info, project_db_id, state, tasks)


def resolve_moved_tasks(info, project_db_id: int, state: TaskState, cards: list[MovedTaskInput]):
    session = info.context.db_session
    stmt = (
        sa.select(db.Task)
        .where(db.Task.project_id == project_db_id)
        .where(db.Task.task_state == state)
    )
    lane_order = session.scalars(stmt)
    tasks = {
        c.task_db_id: (c.order_id, c.detached, session.get(db.Task, c.task_db_id)) for c in cards
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
    return MutationResult(success=True)
