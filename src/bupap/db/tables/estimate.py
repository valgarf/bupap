from __future__ import annotations

from datetime import datetime, timedelta
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, intfk, str_20, text

if TYPE_CHECKING:
    from .project import Project
    from .task import Task
    from .user import User


class EstimateType(Base):
    name: Mapped[str_20] = mapped_column(unique=True)
    description: Mapped[text]
    relative: Mapped[bool]

    # shifts are either given in seconds (non-relative estimate type) or as multipliers (relative
    # estimate type)
    default_shift_optimistic: Mapped[float]
    default_shift_pessimistic: Mapped[float]
    default_shift_average: Mapped[float]
    min_datapoints: Mapped[int]
    max_datapoints: Mapped[int]

    estimates: Mapped[List[Estimate]] = relationship(back_populates="estimate_type")
    estimate_statistics: Mapped[List[EstimateStatistics]] = relationship(
        back_populates="estimate_type"
    )

    @property
    def shift_optimistic(self):
        return self.default_shift_optimistic

    @property
    def shift_pessimistic(self):
        return self.default_shift_pessimistic

    @property
    def shift_average(self):
        return self.default_shift_average


class Estimate(Base):
    task_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Task.id"))
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    created_at: Mapped[datetime]
    estimate_type_id: Mapped[intfk] = mapped_column(sa.ForeignKey("EstimateType.id"))
    estimated_duration: Mapped[timedelta]
    expectation_optimistic: Mapped[timedelta]
    expectation_pessimistic: Mapped[timedelta]
    expectation_average: Mapped[timedelta]

    task: Mapped[Task] = relationship(back_populates="estimates")
    user: Mapped[User] = relationship(back_populates="estimates")
    estimate_type: Mapped[EstimateType] = relationship(back_populates="estimates")


class EstimateStatistics(Base):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    estimate_type_id: Mapped[intfk] = mapped_column(sa.ForeignKey("EstimateType.id"))

    num_datapoints: Mapped[int]
    evaluated: Mapped[datetime]

    # shifts are either given in seconds (non-relative estimate type) or as multipliers (relative
    # estimate type)
    shift_optimistic: Mapped[float]
    shift_pessimistic: Mapped[float]
    shift_average: Mapped[float]

    user: Mapped[User] = relationship(back_populates="estimate_statistics")
    estimate_type: Mapped[EstimateType] = relationship(back_populates="estimate_statistics")
