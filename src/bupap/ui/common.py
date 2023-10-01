from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Callable, Dict, Generic, Hashable, Iterable, TypeVar
from zoneinfo import ZoneInfo

import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import Request

# def is_authenticated(request: Request) -> bool:
#     return session_info.get(request.session.get('id'), {}).get('authenticated', False)
from loguru import logger
from nicegui import globals, ui

from bupap import db

T_co = TypeVar("T_co", covariant=True)


class LoginRequiredException(RuntimeError):
    pass


def get_db_session(request: Request) -> sa.orm.Session:
    return request.state.session


def get_user(request: Request, required: bool = True) -> db.User:
    result = None
    user_session_id = request.session.get("id")
    if user_session_id:
        db_session = get_db_session(request)
        result = db_session.scalars(
            sa.select(db.User).where(db.User.session_id == user_session_id)
        ).first()
    logger.debug(
        "user retrieval for session {} -> {}", user_session_id, result.name if result else None
    )
    if required and result is None:
        raise LoginRequiredException()
    return result


def client_data() -> Dict[Any, Any]:
    return globals.index_client._custom_data


def format_timedelta(td: timedelta):
    m = round(td.total_seconds() / 60)
    h = m // 60
    m -= h * 60
    result = f"{h}:{m:02}"
    return result


def format_date(dt: datetime):
    dt_tzaware = dt.replace(tzinfo=timezone.utc)
    dt_converted = (
        dt_tzaware.astimezone()
    )  # TODO: should user user's timezone. This is server timezone
    return dt_converted.date().isoformat()


def format_time(dt: datetime):
    dt_tzaware = dt.replace(tzinfo=timezone.utc)
    dt_converted = (
        dt_tzaware.astimezone()
    )  # TODO: should user user's timezone. This is server timezone
    t = dt_converted.time()
    return f"{t.hour: 2}:{t.minute:02}"


async def get_timezone_from_browser():
    return ZoneInfo(await ui.run_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone"))


@dataclass
class TreeNode(Generic[T_co]):
    value: T_co
    children: list[TreeNode[T_co]]
    parent: T_co | None
    tree: Tree[T_co]
    user_data: Any
    depth: int

    def __init__(self, tree: Tree[T_co], value: T_co, depth: int, parent: Tree[T_co] | None = None):
        self.tree = tree
        self.value = value
        self.depth = depth
        self.children = []
        self.parent = parent
        self.user_data = None


@dataclass
class Tree(Generic[T_co]):
    def __init__(
        self,
        elements: Iterable[T_co],
        parent_func: Callable[[T_co], T_co | None] = lambda value: value.parent,
        id_func: Callable[[T_co], Hashable] = lambda value: value,
    ) -> Tree[T_co]:
        roots = []

        value_to_node: Dict[Hashable, TreeNode[T_co]] = {}
        remaining = list(elements)
        while remaining:
            orig_no_remaining = len(remaining)
            elements = remaining
            remaining = []
            for element in elements:
                element_id = id_func(element)
                if element_id in value_to_node:
                    raise RuntimeError("Cannot construct tree. Duplicate ids")
                parent = parent_func(element)
                if parent is None:
                    node = TreeNode(self, element, 0)
                    value_to_node[element_id] = node
                    roots.append(node)
                else:
                    parent_node = value_to_node.get(id_func(parent))
                    if parent_node is None:
                        remaining.append(element)
                    else:
                        node = TreeNode(self, element, parent_node.depth + 1)
                        value_to_node[element_id] = node
                        parent_node.children.append(node)
                        node.parent = parent_node

            if len(remaining) >= orig_no_remaining:
                raise RuntimeError(
                    "Cannot construct tree. Cycles or nonexistant parent objects in data"
                )
        self.children = roots

    def breadth_first(self) -> Iterable[TreeNode[T_co]]:
        stack: list[TreeNode[T_co]] = list(self.children)
        while stack:
            element = stack.pop(0)
            stack.extend(element.children)
            yield element

    def depths_first(self) -> Iterable[TreeNode[T_co]]:
        stack: list[TreeNode[T_co]] = self.children[::-1]
        while stack:
            element = stack.pop(-1)
            stack.extend(reversed(element.children))
            yield element
