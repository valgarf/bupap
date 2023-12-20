import strawberry

from ..common.db_type import DBType, map_to_db


@strawberry.type
class User(DBType):
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    full_name: str = map_to_db()
    rendered_avatar: str = map_to_db()
