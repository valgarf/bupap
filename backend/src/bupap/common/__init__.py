from datetime import datetime

import pytz


def toUTC(dt: datetime) -> datetime:
    if dt.tzinfo == pytz.utc:
        return dt
    if dt.tzinfo is None:
        return pytz.utc.localize(dt)
    return dt.astimezone(pytz.utc)


def nowUTC() -> datetime:
    return datetime.now(tz=pytz.utc)
