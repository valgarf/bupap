from typing import TYPE_CHECKING, Annotated

import strawberry

from bupap import db
from bupap.gql.common.context import InfoContext

from ..common.db_type import DBType, map_to_db
from .schedule import Schedule, ScheduleRequest, get_schedule

if TYPE_CHECKING:
    from .role import AssignedTeamRole


@strawberry.type
class Team(DBType, strawberry.relay.Node):
    _db_table = db.Team
    name: str = map_to_db()
    db_id: int = map_to_db("id")
    assigned_roles: list[Annotated["AssignedTeamRole", strawberry.lazy(".role")]] = map_to_db()

    @strawberry.field
    def schedule(self, input: ScheduleRequest) -> Schedule:
        return get_schedule(self.db_obj, input)
