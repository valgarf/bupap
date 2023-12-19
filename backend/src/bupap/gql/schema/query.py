import sqlalchemy as sa
import strawberry

from bupap import db
from bupap.gql.common.context import InfoContext

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


@strawberry.type
class Query:
    active_user: User | None = strawberry.field(resolver=get_active_user)
    teams: list[Team] = strawberry.field(resolver=get_all_teams)
