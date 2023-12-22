from enum import Enum, auto

import strawberry


@strawberry.enum
class RoleType(Enum):
    GLOBAL = auto()
    TEAM = auto()
    PROJECT = auto()


@strawberry.enum
class ScheduleMode(Enum):
    PESSIMISTIC = auto()
    AVERAGE = auto()
    OPTIMISTIC = auto()
