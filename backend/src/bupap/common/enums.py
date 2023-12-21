from enum import Enum, auto

import strawberry


@strawberry.enum
class RoleType(Enum):
    GLOBAL = auto()
    TEAM = auto()
    PROJECT = auto()
