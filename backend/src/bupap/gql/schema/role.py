from typing import TYPE_CHECKING, Annotated

import strawberry

from bupap import db
from bupap.common.enums import RoleType

from ..common.db_type import DBType, map_to_db

if TYPE_CHECKING:
    from .team import Team
    from .user import User


@strawberry.type
class Role(DBType, strawberry.relay.Node):
    _db_table = db.Role
    name: str = map_to_db()
    db_id: int = map_to_db("id")
    builtin: bool = map_to_db()
    role_type: RoleType = map_to_db()


@strawberry.type
class AssignedTeamRole(DBType, strawberry.relay.Node):
    _db_table = db.AssignedTeamRole
    db_id: int = map_to_db("id")
    role: Role = map_to_db()
    user: Annotated["User", strawberry.lazy(".user")] = map_to_db()
    team: Annotated["Team", strawberry.lazy(".team")] = map_to_db()
