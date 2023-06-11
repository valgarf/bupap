from __future__ import annotations

from datetime import datetime, timedelta
from enum import Enum, auto
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, column_property, mapped_column, relationship

from .base import Base, intfk, str_50, text
from .work import WorkPeriodTask

if TYPE_CHECKING:
    from .estimate import Estimate
    from .history import TaskHistory
    from .project import Project
    from .user import User


class TaskState(Enum):
    REQUEST = auto()
    PLANNING = auto()
    DEFERRED = auto()
    SCHEDULED = auto()
    IN_PROGRESS = auto()
    DONE = auto()
    DISCARDED = auto()
    HOLD = auto()


class TaskType(Enum):
    FEATURE = auto()
    BUG = auto()
    ADHOC = auto()


class TaskPriority(Enum):
    VERY_HIGH = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    VERY_LOW = auto()


class Task(Base):
    name: Mapped[str_50]
    description: Mapped[text]
    project_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Project.id"))
    parent_id: Mapped[intfk | None] = mapped_column(sa.ForeignKey("Task.id"))

    order_id: Mapped[int | None]
    task_state: Mapped[TaskState]
    task_type: Mapped[TaskType]
    task_priority: Mapped[TaskPriority]
    created_at: Mapped[datetime]
    finished_at: Mapped[datetime | None]

    # scheduling data
    scheduled_average_start: Mapped[datetime | None]
    scheduled_average_end: Mapped[datetime | None]
    scheduled_optimistic_start: Mapped[datetime | None]
    scheduled_optimistic_end: Mapped[datetime | None]
    scheduled_pessimistic_start: Mapped[datetime | None]
    scheduled_pessimistic_end: Mapped[datetime | None]
    scheduled_assignee_id: Mapped[intfk | None] = mapped_column(sa.ForeignKey("User.id"))
    automatic_schedule: Mapped[bool]

    parent: Mapped[Task] = relationship(back_populates="children", remote_side="Task.id")
    children: Mapped[List[Task]] = relationship(back_populates="parent")

    project: Mapped[Project] = relationship(back_populates="tasks")
    scheduled_assignee: Mapped[User | None] = relationship(
        back_populates="tasks", foreign_keys=scheduled_assignee_id
    )

    estimates: Mapped[List[Estimate]] = relationship(back_populates="task")
    work_periods: Mapped[List[WorkPeriodTask]] = relationship(back_populates="task")
    history: Mapped[list[TaskHistory]] = relationship(back_populates="task")

    @property
    def open_work_period(self) -> WorkPeriodTask | None:
        session = sa.orm.object_session(self)
        return session.scalars(
            sa.select(WorkPeriodTask)
            .where(WorkPeriodTask.ended_at == None)
            .where(WorkPeriodTask.task == self)
        ).first()
