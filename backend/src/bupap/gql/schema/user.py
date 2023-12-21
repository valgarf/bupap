import strawberry

from bupap import db

from ..common.db_type import DBType, map_to_db


@strawberry.type
class User(DBType, strawberry.relay.Node):
    _db_table = db.User
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    full_name: str = map_to_db()
    rendered_avatar: str = map_to_db()
