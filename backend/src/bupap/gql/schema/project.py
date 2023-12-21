from __future__ import annotations

import strawberry

from bupap import db

from ..common.db_type import DBType, map_to_db


@strawberry.type
class Project(DBType, strawberry.relay.Node):
    _db_table = db.Project
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    parent: Project | None = map_to_db()
    children: list[Project] = map_to_db()
