from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .assocs import assoc_project_team
from .base import Base, InheritanceBase, InheritanceFK, intfk, str_10, str_20, str_30, text

if TYPE_CHECKING:
    from .role import AssignedTeamRole
    from .task import Task
    from .user import User


class WorkPeriod(InheritanceBase, Base):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    started_at: Mapped[datetime]
    ended_at: Mapped[datetime | None]
    comment: Mapped[text] = mapped_column(default="")

    user: Mapped[User] = relationship(back_populates="work_periods")

    @property
    def exclusive(self):
        raise NotImplementedError()

    @property
    def duration(self) -> timedelta | None:
        if self.ended_at is None:
            return None
        return self.ended_at - self.started_at


class WorkPeriodTask(InheritanceFK, WorkPeriod):
    task_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Task.id"))

    task: Mapped[Task] = relationship(back_populates="work_periods")

    @property
    def exclusive(self):
        return True


class WorkPeriodTimesink(InheritanceFK, WorkPeriod):
    timesink_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Timesink.id"))

    timesink: Mapped[Timesink] = relationship(back_populates="work_periods")

    @property
    def exclusive(self):
        return True


class WorkPeriodWorking(InheritanceFK, WorkPeriod):
    @property
    def exclusive(self):
        return False


class WorkPeriodNotWorking(InheritanceFK, WorkPeriod):
    """
    Holidays, sick, breaks. Anything that would not be counted towards working hours.
    """

    @property
    def exclusive(self):
        return True


class Timesink(Base):
    name: Mapped[str_30] = mapped_column(unique=True)
    color: Mapped[str_10]

    work_periods: Mapped[List[WorkPeriodTimesink]] = relationship(back_populates="timesink")
