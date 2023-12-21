from typing import Self

import strawberry

from bupap import db

from ..common.db_type import DBType, map_to_db


@strawberry.type
class Project(DBType, strawberry.relay.Node):
    _db_table = db.Project
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    parent: Self | None = map_to_db()
    children: list[Self] = map_to_db()
