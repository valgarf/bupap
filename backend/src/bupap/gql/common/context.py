from dataclasses import dataclass
from functools import cached_property
from typing import Any, TypeAlias

from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import Response
from starlette.websockets import WebSocket
from strawberry.types import Info

from bupap import db


@dataclass
class Context:
    request: Request | WebSocket
    response: Response | None

    @cached_property
    def db_session(self) -> Session:
        return self.request["db_session"]

    @property
    def user_session(self) -> dict[str, Any]:
        return self.request["session"]

    @cached_property
    def user(self) -> db.User | None:
        user_id = self.user_session.get("user_id", None)
        if user_id is None:
            return None
        user = self.db_session.get(db.User, user_id)
        if user is not None and user.session_id == self.user_session["session_id"]:
            return user
        return None


InfoContext: TypeAlias = Info[Context, Any]
