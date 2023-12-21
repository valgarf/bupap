from __future__ import annotations

from enum import Enum, auto
from typing import TYPE_CHECKING, List

import sqlalchemy as sa
import sqlalchemy.types
from sqlalchemy.orm import Mapped, mapped_column, relationship

from bupap.common.enums import RoleType
from bupap.permissions import Permission

from .base import Base, intfk, str_50

if TYPE_CHECKING:
    from .project import Project
    from .team import Team
    from .user import User


class PermissionType(sa.types.TypeDecorator):
    impl = sa.types.BigInteger

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return Permission(value)


class Role(Base):
    name: Mapped[str_50] = mapped_column(unique=True, index=True)
    permissions: Mapped[Permission] = mapped_column(PermissionType, unique=True, index=True)
    role_type: Mapped[RoleType]
    builtin: Mapped[bool]
    global_assignments: Mapped[List[AssignedGlobalRole]] = relationship(back_populates="role")
    team_assignments: Mapped[List[AssignedTeamRole]] = relationship(back_populates="role")
    project_assignments: Mapped[List[AssignedProjectRole]] = relationship(back_populates="role")


class AssignedGlobalRole(Base):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    role_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Role.id"))

    user: Mapped[User] = relationship(back_populates="global_roles")
    role: Mapped[Role] = relationship(back_populates="global_assignments")


class AssignedTeamRole(Base):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    role_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Role.id"))
    team_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Team.id"))
    user: Mapped[User] = relationship(back_populates="team_roles")
    role: Mapped[Role] = relationship(back_populates="team_assignments")
    team: Mapped[Team] = relationship(back_populates="assigned_roles")


class AssignedProjectRole(Base):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    role_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Role.id"))
    project_id: Mapped[intfk] = mapped_column(sa.ForeignKey("Project.id"))
    user: Mapped[User] = relationship(back_populates="project_roles")
    role: Mapped[Role] = relationship(back_populates="project_assignments")
    project: Mapped[Project] = relationship(back_populates="assigned_roles")
