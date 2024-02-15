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


@strawberry.enum
class TaskState(Enum):
    REQUEST = auto()
    PLANNING = auto()
    DEFERRED = auto()
    SCHEDULED = auto()
    # IN_PROGRESS = auto()
    DONE = auto()
    DISCARDED = auto()
    HOLD = auto()

    @property
    def text(self):
        return self.name.replace("_", " ")

    @property
    def default_color(self):
        return "purple-4"


@strawberry.enum
class TaskType(Enum):
    FEATURE = auto()
    BUG = auto()
    ADHOC = auto()

    @property
    def text(self):
        return self.name.replace("_", " ")

    @property
    def default_color(self):
        match (self):
            case TaskType.BUG:
                result = "red-8"
            case TaskType.FEATURE:
                result = "indigo-8"
            case TaskType.ADHOC:
                result = "cyan-8"
            case _:
                assert False
        return result


@strawberry.enum
class TaskPriority(Enum):
    VERY_HIGH = auto()
    HIGH = auto()
    MEDIUM = auto()
    LOW = auto()
    VERY_LOW = auto()

    @property
    def default_color(self):  # TODO: make configurable
        match (self):
            case TaskPriority.VERY_HIGH:
                result = "red-11"
            case TaskPriority.HIGH:
                result = "deep-purple-11"
            case TaskPriority.MEDIUM:
                result = "green-11"
            case TaskPriority.LOW:
                result = "teal-11"
            case TaskPriority.VERY_LOW:
                result = "blue-11"
            case _:
                assert False
        return result

    @property
    def text(self):
        return self.name.replace("_", " ")

    @property
    def default_text_color(self):
        match (self):
            case TaskPriority.VERY_HIGH:
                result = "white"
            case TaskPriority.HIGH:
                result = "white"
            case TaskPriority.MEDIUM:
                result = "black"
            case TaskPriority.LOW:
                result = "black"
            case TaskPriority.VERY_LOW:
                result = "black"
            case _:
                assert False
        return result
