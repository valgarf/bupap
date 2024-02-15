from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated, Self

import strawberry

from bupap import db
from bupap.ui.crud.task import get_estimate

from ...common.enums import TaskPriority, TaskState, TaskType
from ..common.db_type import DBConvExtension, DBType, map_to_db
from .common import Timedelta
from .tag import Tag

if TYPE_CHECKING:
    from .estimate import Estimate
    from .project import Project
    from .user import User


@strawberry.interface
class TaskActivity:
    timestamp: datetime


@strawberry.type
class TaskActivityCreated(TaskActivity):
    pass


@strawberry.type
class TaskActivityFinished(TaskActivity):
    pass


@strawberry.type
class TaskActivityWorkperiod(TaskActivity):
    duration: Timedelta | None
    user: Annotated["User", strawberry.lazy(".user")] = strawberry.field(
        extensions=[DBConvExtension()]
    )


@strawberry.type
class TaskActivityEstimateAdded(TaskActivity):
    estimate: Annotated["Estimate", strawberry.lazy(".estimate")] = strawberry.field(
        extensions=[DBConvExtension()]
    )
    user: Annotated["User", strawberry.lazy(".user")] = strawberry.field(
        extensions=[DBConvExtension()]
    )


@strawberry.type
class TaskProgress:
    active: bool
    pessimistic: int
    average: int
    optimistic: int


@strawberry.type
class Task(DBType, strawberry.relay.Node):
    _db_table = db.Task
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    description: str = map_to_db()
    parent: Self | None = map_to_db()
    children: list[Self] = map_to_db()
    state: TaskState = map_to_db("task_state")
    type: TaskType = map_to_db("task_type")
    priority: TaskPriority = map_to_db("task_priority")
    finished_at: datetime | None = map_to_db()
    created_at: datetime | None = map_to_db()
    order_id: int | None = map_to_db()
    attached: bool = map_to_db()
    project: Annotated["Project", strawberry.lazy(".project")] = map_to_db("project")

    @strawberry.field()
    def active(self) -> bool:
        pass

    @strawberry.field()
    def progress(self) -> TaskProgress:
        active = False
        progress = [0, 0, 0]
        db_obj: db.Task = self.db_obj
        if db_obj.scheduled_assignee and db_obj.finished_at is None:
            total_work = timedelta(0)
            for wp in db_obj.work_periods:
                if wp.ended_at:
                    total_work += wp.duration
                else:
                    active = True
            if total_work:
                est = get_estimate(db_obj.scheduled_assignee, db_obj)
                progress = (
                    total_work / est.expectation_pessimistic,
                    total_work / est.expectation_average,
                    total_work / est.expectation_optimistic,
                )
                progress = tuple(int(min(p, 1) * 100) for p in progress)
        return TaskProgress(
            active=active, pessimistic=progress[0], average=progress[1], optimistic=progress[2]
        )

    @strawberry.field()
    def activity(self) -> list[TaskActivity]:
        db_obj: db.Task = self.db_obj
        result = []
        result.append(TaskActivityCreated(timestamp=db_obj.created_at))
        if db_obj.finished_at:
            result.append(TaskActivityFinished(timestamp=db_obj.finished_at))
        for estimate in db_obj.estimates:
            result.append(
                TaskActivityEstimateAdded(
                    timestamp=estimate.created_at, estimate=estimate, user=estimate.user
                )
            )
        for wp in db_obj.work_periods:
            result.append(
                TaskActivityWorkperiod(
                    timestamp=wp.ended_at if wp.ended_at is not None else wp.started_at,
                    duration=wp.duration if wp.ended_at is not None else None,
                    user=estimate.user,
                )
            )

        def _sort_key(t):
            return (
                t.timestamp,
                [
                    TaskActivityCreated,
                    TaskActivityEstimateAdded,
                    TaskActivityWorkperiod,
                    TaskActivityFinished,
                ].index(type(t)),
            )

        result.sort(key=_sort_key, reverse=True)
        return result

    @strawberry.field()
    def tags() -> list[Tag]:
        return []
        # TODO
