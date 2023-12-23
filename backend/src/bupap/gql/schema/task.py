from typing import Self

import strawberry

from bupap import db

from ..common.db_type import DBType, map_to_db


@strawberry.type
class Task(DBType, strawberry.relay.Node):
    _db_table = db.Task
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    description: str = map_to_db()
