"""GraphQL schema for a Task."""

# future
from __future__ import annotations

# stl
from datetime import datetime, timedelta
from typing import TYPE_CHECKING, Annotated, Self

# third-party
import strawberry

# first-party
from bupap import db
from bupap.common.enums import TaskPriority, TaskState, TaskType  # noqa: TCH001
from bupap.gql.common.db_type import DBConvExtension, DBType, map_to_db
from bupap.ui.crud.task import get_estimate

# local
from .common import Period, Timedelta
from .tag import Tag  # noqa: TCH001

if TYPE_CHECKING:
    # first-party

    # local
    from .estimate import Estimate
    from .project import Project
    from .user import User


@strawberry.interface
class TaskActivity:
    """Interface of a single activity for a task."""

    timestamp: datetime


@strawberry.type
class TaskActivityCreated(TaskActivity):
    """The creation of the task."""


@strawberry.type
class TaskActivityFinished(TaskActivity):
    """The completion of the task."""


@strawberry.type
class TaskActivityWorkperiod(TaskActivity):
    """A work period for a task with an optional duration (if finished) and associated user."""

    duration: Timedelta | None
    user: Annotated[User, strawberry.lazy(".user")] = strawberry.field(
        extensions=[DBConvExtension()]
    )


@strawberry.type
class TaskActivityEstimateAdded(TaskActivity):
    """The addition of an estimate with the associated estimate and user."""

    estimate: Annotated[Estimate, strawberry.lazy(".estimate")] = strawberry.field(
        extensions=[DBConvExtension()]
    )
    user: Annotated[User, strawberry.lazy(".user")] = strawberry.field(
        extensions=[DBConvExtension()]
    )


@strawberry.type
class TaskProgress:
    """The progress of a task with different levels of estimation."""

    active: bool
    pessimistic: int
    average: int
    optimistic: int


@strawberry.interface
class WorkPeriod(DBType):
    _db_table = db.WorkPeriod
    """A time period a user worked. Subclasses define the work type."""

    user: Annotated[User, strawberry.lazy(".user")] = map_to_db()
    started_at: datetime = map_to_db()
    ended_at: datetime | None = map_to_db()

    @strawberry.field()
    def duration(self) -> Timedelta | None:
        if self.db_obj.ended_at is None:
            return None
        return self.db_obj.ended_at - self.db_obj.started_at


@strawberry.type
class WorkPeriodTask(WorkPeriod, DBType, strawberry.relay.Node):
    _db_table = db.WorkPeriodTask

    task: Annotated[Task, strawberry.lazy(".task")] = map_to_db()


@strawberry.type
class WorkPeriodTimesink(WorkPeriod, DBType, strawberry.relay.Node):
    _db_table = db.WorkPeriodTimesink


@strawberry.type
class WorkPeriodWorking(WorkPeriod, DBType, strawberry.relay.Node):
    _db_table = db.WorkPeriodWorking


@strawberry.type
class TaskSchedule:
    """Scheduled user and possible execution periods."""

    optimistic: Period
    average: Period
    pessimistic: Period
    assignee: Annotated[User, strawberry.lazy(".user")] = strawberry.field(
        extensions=[DBConvExtension()]
    )


@strawberry.type
class TaskHistory(DBType, strawberry.relay.Node):
    """Single entry in the task history."""

    _db_table = db.TaskHistory
    date: datetime = map_to_db()

    scheduled_average_end: datetime = map_to_db()
    scheduled_optimistic_end: datetime = map_to_db()
    scheduled_pessimistic_end: datetime = map_to_db()

    task: Annotated[Task, strawberry.lazy(".task")] = map_to_db()
    assignee: Annotated[User, strawberry.lazy(".user")] = map_to_db()


@strawberry.type
class Task(DBType, strawberry.relay.Node):
    """A single task to be estimated, scheduled and executed by a user / developer."""

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
    project: Annotated[Project, strawberry.lazy(".project")] = map_to_db()
    work_periods: list[WorkPeriodTask] = map_to_db()
    estimates: list[Annotated[Estimate, strawberry.lazy(".estimate")]] = map_to_db()
    history: list[TaskHistory] = map_to_db()

    @strawberry.field()
    def schedule(self) -> TaskSchedule | None:
        """Retrieve the schedule of the task if available."""
        db_obj: db.Task = self.db_obj
        if (
            db_obj.scheduled_assignee is None
            or db_obj.scheduled_optimistic_start is None
            or db_obj.scheduled_optimistic_end is None
            or db_obj.scheduled_average_start is None
            or db_obj.scheduled_average_end is None
            or db_obj.scheduled_pessimistic_start is None
            or db_obj.scheduled_pessimistic_end is None
        ):
            return None
        return TaskSchedule(
            pessimistic=Period(
                db_obj.scheduled_pessimistic_start, db_obj.scheduled_pessimistic_end
            ),
            average=Period(db_obj.scheduled_average_start, db_obj.scheduled_average_end),
            optimistic=Period(db_obj.scheduled_optimistic_start, db_obj.scheduled_optimistic_end),
            assignee=db_obj.scheduled_assignee,
        )

    @strawberry.field()
    def progress(self) -> TaskProgress:
        """Calculate and returns the task progress based on work periods and estimates."""
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
        """Return a list of task activities, latest first."""
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
        """Get the task's tags."""
        return []
        # TODO(Stefan): implement
