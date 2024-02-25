# future
from __future__ import annotations

# stl
from datetime import datetime
from typing import TYPE_CHECKING

# third-party
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

# local
from .base import Base, intfk

if TYPE_CHECKING:
    # local
    from .task import Task
    from .user import User


class TaskHistory(Base):
    date: Mapped[datetime]
    task_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Task.id"))
    assignee_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"), nullable=True)
    scheduled_average_end: Mapped[datetime]
    scheduled_optimistic_end: Mapped[datetime]
    scheduled_pessimistic_end: Mapped[datetime]

    task: Mapped[Task] = relationship(back_populates="history")
    assignee: Mapped[User] = relationship()
