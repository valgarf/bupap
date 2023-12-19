import strawberry

from ..common.db_type import DBType, map_to_db


@strawberry.type
class Team(DBType):
    name: str = map_to_db()
    db_id: int = map_to_db("id")
