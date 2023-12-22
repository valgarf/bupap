from datetime import datetime
from typing import TYPE_CHECKING

import strawberry

from bupap import db
from bupap.common import toUTC

from ..common.db_type import DBType, map_to_db


@strawberry.type
class Period:
    start: datetime
    end: datetime

    def __init__(self, start: datetime, end: datetime):
        self.start = toUTC(start)
        self.end = toUTC(end)
