from datetime import datetime, timedelta
from typing import NewType

import strawberry

from bupap.common import toUTC


def serialize_timedelta(td: timedelta) -> str:
    """
    Convert a timedelta object to a string in the format "HH:MM:SS[.sss]".

    Milliseconds are omitted if they are 0.

    :param td: The timedelta object to serialize.
    :returns: A string representation of the timedelta object.
    """
    s = td.total_seconds()
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    result = f"{int(h):02}:{int(m):02}:{s:06.3f}"
    if result.endswith(".000"):
        result = result[:-4]
    return result


def deserialize_timedelta(v: str) -> timedelta:
    """
    Deserialize a string representing a duration into a timedelta object.

    :param v: The string in the format "HH[:MM[:SS[.sss]]]".
    """
    h, m, s = [*v.split(":"), 0, 0, 0][:3]
    return timedelta(hours=int(h), minutes=int(m), seconds=float(s))


Timedelta = strawberry.scalar(
    NewType("Duration", timedelta),
    serialize=serialize_timedelta,
    parse_value=deserialize_timedelta,
    description="Duration in format HH:MM:SS[.sss]",
)


@strawberry.type
class Period:
    """Timeperiod with `start` and `end` timestamp."""

    start: datetime
    end: datetime

    def __init__(self, start: datetime, end: datetime):
        self.start = toUTC(start)
        self.end = toUTC(end)


@strawberry.type
class MutationResult:
    success: bool
