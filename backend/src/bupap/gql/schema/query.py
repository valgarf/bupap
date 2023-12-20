import sqlalchemy as sa
import strawberry

from bupap import db
from bupap.gql.common.context import InfoContext

from .project import Project
from .team import Team
from .user import User


def get_active_user(root, info):
    if info.context.user is None:
        return None
    return User(info.context.user)


def get_all_teams(root, info: InfoContext):
    return [
        Team(db_obj)
        for db_obj in info.context.db_session.scalars(sa.select(db.Team).order_by(db.Team.name))
    ]


def get_all_users(root, info: InfoContext):
    return [
        User(db_obj)
        for db_obj in info.context.db_session.scalars(sa.select(db.User).order_by(db.User.name))
    ]


def get_all_projects(root, info: InfoContext, toplevel: bool = False):
    query = sa.select(db.Project).order_by(db.Project.name)
    if toplevel:
        query = query.when(db.Project.parent == None)
    return [Project(db_obj) for db_obj in info.context.db_session.scalars(query)]


@strawberry.type
class Query:
    active_user: User | None = strawberry.field(resolver=get_active_user)
    teams: list[Team] = strawberry.field(resolver=get_all_teams)
    users: list[User] = strawberry.field(resolver=get_all_users)
    projects: list[Project] = strawberry.field(resolver=get_all_projects)
