import uuid
from typing import Any

import sqlalchemy as sa
import strawberry
from strawberry.types import Info

from bupap import db

from ..common.context import Context, InfoContext
from .user import User


def login(root, info: InfoContext, username: str, password: str):
    session = info.context.db_session
    user: db.User = session.scalars(sa.select(db.User).where(db.User.name == username)).first()
    if user and user.check_password(password):
        session_id = str(uuid.uuid4())
        user.session_id = session_id
        info.context.user_session["session_id"] = session_id
        info.context.user_session["user_id"] = user.id
        return User(user)
    return None


@strawberry.type
class Mutation:
    login: User | None = strawberry.field(resolver=login)