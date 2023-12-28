from datetime import datetime, timedelta
from typing import TYPE_CHECKING, NewType

import strawberry

from bupap import db
from bupap.common import toUTC

from ..common.db_type import DBType, map_to_db


def serialize_timedelta(td: timedelta):
    s = td.total_seconds()
    m, s = s // 60, s % 60
    h, m = m // 60, m % 60
    return f"{h:02.0f}:{m:02.0f}:{s:02.4f}"


def deserialize_timedelta(v: str):
    h, m, s = (v.split(":") + [0, 0, 0])[:3]
    return timedelta(hours=int(h), minutes=int(m), seconds=float(s))


Timedelta = strawberry.scalar(
    NewType("Base64", timedelta),
    serialize=serialize_timedelta,
    parse_value=deserialize_timedelta,
)


@strawberry.type
class Period:
    start: datetime
    end: datetime

    def __init__(self, start: datetime, end: datetime):
        self.start = toUTC(start)
        self.end = toUTC(end)


@strawberry.type
class MutationResult:
    success: bool
