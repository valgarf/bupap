from typing import Type, TypeVar, overload

import sqlalchemy as sa

from bupap import db

T = TypeVar("T", bound=db.Base)


@overload
def return_obj_or_id(
    external_session: db.Session, session: db.Session, obj: T, always_flush: bool = False
) -> T:
    ...


@overload
def return_obj_or_id(
    external_session: None, session: db.Session, obj: T, always_flush: bool = False
) -> int:
    ...


def return_obj_or_id(external_session, session, obj, always_flush=False):
    if external_session is None:
        session.flush()
        return obj.id
    else:
        if always_flush:
            session.flush()
        return obj


def get_from_id(session: db.Session, cls: Type[T], entry_id: int) -> T:
    db_result = session.get(cls, entry_id)
    if db_result is None:
        raise RuntimeError(
            f"{cls.__name__} with id '{entry_id}' could not be found in the database."
        )
    return db_result


def _insert_tasks_at(tasks: db.Task, state: db.TaskState, index: int, session: db.Session):
    project = tasks[0].project
    assert all(t.project == project for t in tasks[1:])
    session.execute(
        sa.update(db.Task)
        .where(db.Task.project_id == project.id)
        .where(db.Task.task_state == state)
        .where(db.Task.order_id >= index)
        .values(order_id=db.Task.order_id + len(tasks))
    )
    for t in tasks:
        t.order_id = index
        index += 1


def _find_order_of_last_task_for_prio(
    proj_id: int,
    state: db.TaskState,
    prio: db.TaskPriority,
    external_session: db.Session | None = None,
) -> int:
    with db.use_or_open_session(external_session) as session:
        order_id = session.scalars(
            sa.select(db.Task.order_id)
            .where(db.Task.project_id == proj_id)
            .where(db.Task.task_state == state)
            .where(db.Task.task_priority == prio)
            .order_by(sa.desc(db.Task.order_id))
        ).first()
        if order_id is not None:
            return order_id
        if prio.value > 1:
            return _find_order_of_last_task_for_prio(
                proj_id, state, db.TaskPriority(prio.value - 1), session
            )
        return -1


def set_task_state(db_task: db.Task, state: db.TaskState, session: db.Session | None = None):
    set_tasks_state([db_task], state, session)


def set_tasks_state(
    db_tasks: list[db.Task], state: db.TaskState, session: db.Session | None = None
):
    if session is None:
        session = db.Session.object_session(db_tasks[0])

    project = db_tasks[0].project
    assert all(t.project == project for t in db_tasks[1:])
    db_tasks = [t for t in db_tasks if t.task_state != state]

    index_map = {}
    prio_cache = {}
    for db_task in db_tasks:
        if db_task.attached and db_task.parent is not None and db_task.parent.task_state != state:
            db_task.attached = False
        if db_task.attached and db_task.parent is not None:
            if db_task.parent.children == [db_task]:
                idx = db_task.parent.order_id
            else:
                idx = max(c.order_id for c in db_task.parent.children)
            index_map.setdefault(idx + 1, ([], []))[0].append(0, db_task)
        else:
            if db_task.task_priority in prio_cache:
                idx = prio_cache[db_task.task_priority]
            else:
                idx = _find_order_of_last_task_for_prio(
                    project.id, state, db_task.task_priority, session
                )
                prio_cache[db_task.task_priority] = idx
            index_map.setdefault(idx + 1, ([], []))[1].append(db_task)

    offset = 0
    for idx in sorted(index_map.keys()):
        all_tasks = index_map[idx][0] + index_map[idx][1]
        all_tasks = [t for task in all_tasks for t in [task] + list(task.get_recursive_children())]
        _insert_tasks_at(all_tasks, state, idx + offset, session)
        offset += len(all_tasks)

    for db_task in db_tasks:
        db_task.task_state = state
        for db_child in db_task.get_recursive_children():
            db_child.task_state = state
