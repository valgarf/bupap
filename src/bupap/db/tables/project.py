from __future__ import annotations

from typing import TYPE_CHECKING, List

import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .assocs import assoc_project_team
from .base import Base, intfk, str_10, str_30, text

if TYPE_CHECKING:
    from .role import AssignedProjectRole
    from .task import Task
    from .team import Team


class Project(Base):
    name: Mapped[str_30]
    description: Mapped[text]
    parent_id: Mapped[intfk | None] = mapped_column(sa.ForeignKey("Project.id"))
    color: Mapped[str_10]

    assigned_roles: Mapped[List[AssignedProjectRole]] = relationship(back_populates="project")
    parent: Mapped[Project | None] = relationship(
        back_populates="children", remote_side="Project.id"
    )
    children: Mapped[List[Project]] = relationship(back_populates="parent")
    tasks: Mapped[List[Task]] = relationship(back_populates="project")

    teams: Mapped[List[Team]] = relationship(
        secondary=assoc_project_team, back_populates="projects"
    )

    @property
    def recursive_children(self):
        todo = list(self.children)
        result = list(self.children)
        while todo:
            el = todo.pop(0)
            todo.extend(el.children)
            result.extend(el.children)
        return result
