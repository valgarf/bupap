from __future__ import annotations

from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .assocs import assoc_project_team
from .base import Base, str_30

if TYPE_CHECKING:
    from .project import Project
    from .role import AssignedTeamRole


class Team(Base):
    name: Mapped[str_30]
    assigned_roles: Mapped[List[AssignedTeamRole]] = relationship(back_populates="team")

    projects: Mapped[List[Project]] = relationship(
        secondary=assoc_project_team, back_populates="teams"
    )
