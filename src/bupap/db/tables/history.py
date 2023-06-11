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
    from .project import Project
    from .task import Task


class TaskHistory(Base):
    date: Mapped[datetime]
    task_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Task.id"))
    scheduled_average_end: Mapped[datetime]
    scheduled_optimistic_end: Mapped[datetime]
    scheduled_pessimistic_end: Mapped[datetime]

    task: Mapped[Task] = relationship(back_populates="history")
