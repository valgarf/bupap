from __future__ import annotations

import base64
import hashlib
from typing import TYPE_CHECKING, List

import bcrypt
import sqlalchemy as sa
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bupap.avatar import deserialize_avatar
from bupap.permissions import Permission

from .base import Base, intfk, str_20, str_50, str_60, text
from .work import WorkPeriod, WorkPeriodWorking

if TYPE_CHECKING:
    from .estimate import Estimate, EstimateStatistics
    from .project import Project
    from .role import AssignedGlobalRole, AssignedProjectRole, AssignedTeamRole
    from .schedule import Absence, ScheduleRule
    from .task import Task
    from .team import Team


class User(Base):
    name: Mapped[str_20] = mapped_column(unique=True, index=True)
    full_name: Mapped[str_50] = mapped_column(index=True)
    password: Mapped[bytes] = mapped_column(sa.BINARY(60))
    avatar: Mapped[text]
    # TODO: this is not really a good idea. But we are currently missing a "session storage" like
    # redis. This has to suffice for now
    session_id: Mapped[str_60 | None] = mapped_column(index=True)
    interrupted_task_id: Mapped[intfk | None] = mapped_column(
        sa.ForeignKey("Task.id", use_alter=True)
    )

    global_roles: Mapped[List[AssignedGlobalRole]] = relationship(back_populates="user")
    team_roles: Mapped[List[AssignedTeamRole]] = relationship(back_populates="user")
    project_roles: Mapped[List[AssignedProjectRole]] = relationship(back_populates="user")
    estimates: Mapped[List[Estimate]] = relationship(back_populates="user")
    estimate_statistics: Mapped[List[EstimateStatistics]] = relationship(back_populates="user")
    tasks: Mapped[List[Task]] = relationship(
        back_populates="scheduled_assignee", foreign_keys="Task.scheduled_assignee_id"
    )
    work_periods: Mapped[List[WorkPeriod]] = relationship(back_populates="user")
    schedule: Mapped[List[ScheduleRule]] = relationship(back_populates="user")
    absence: Mapped[List[Absence]] = relationship(back_populates="user")
    interrupted_task: Mapped[Task | None] = relationship(
        foreign_keys=interrupted_task_id, post_update=True
    )

    def set_password(self, password: str):
        self.password = bcrypt.hashpw(
            base64.b64encode(hashlib.sha256(password.encode()).digest()), bcrypt.gensalt()
        )

    def check_password(self, password: str) -> True:
        return bcrypt.checkpw(
            base64.b64encode(hashlib.sha256(password.encode()).digest()), self.password
        )

    def global_permissions(self) -> Permission:
        result = Permission(0)
        for r in self.global_roles:
            result |= r.permissions
        return result

    def team_permissions(self, team: Team) -> Permission:
        result = Permission(0)
        for r in self.team_roles:
            if r.team_id == team.id:
                result |= r.permissions
        return result | self.global_permissions()

    def project_permissions(self, project: Project) -> Permission:
        result = Permission(0)
        for r in self.project_roles:
            if r.project_id == project.id:
                result |= r.permissions
        return result | self.global_permissions()

    @property
    def active_work_period(self) -> WorkPeriod | None:
        session = sa.orm.object_session(self)
        # TODO: can we do better than using cls_name here? generalize this somewhat?
        return session.scalars(
            sa.select(WorkPeriod)
            .where(WorkPeriod.user == self)
            .where(WorkPeriod.ended_at == None)
            .where(WorkPeriod.cls_name != WorkPeriodWorking.__name__)
        ).first()

    @property
    def active_working(self) -> WorkPeriodWorking | None:
        session = sa.orm.object_session(self)
        # TODO: can we do better than using cls_name here? generalize this somewhat?
        return session.scalars(
            sa.select(WorkPeriodWorking)
            .where(WorkPeriodWorking.user == self)
            .where(WorkPeriodWorking.ended_at == None)
        ).first()

    @property
    def rendered_avatar(self) -> str:
        return deserialize_avatar(self.avatar).render()
