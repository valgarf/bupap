import sqlalchemy as sa

from .base import Base

assoc_project_team = sa.Table(
    "assoc_project_team",
    Base.metadata,
    sa.Column("project_id", sa.ForeignKey("Project.id"), primary_key=True),
    sa.Column("team_id", sa.ForeignKey("Team.id"), primary_key=True),
)
