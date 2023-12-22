from datetime import datetime, timedelta

import strawberry

from bupap import db
from bupap.common import toUTC

from ..common.db_type import DBType, map_to_db


@strawberry.type
class UserActivity:
    at: datetime
    short: str
    details: str = ""
    order: strawberry.Private[int] = 0


@strawberry.type
class User(DBType, strawberry.relay.Node):
    _db_table = db.User
    db_id: int = map_to_db("id")
    name: str = map_to_db()
    full_name: str = map_to_db()
    rendered_avatar: str = map_to_db()

    @strawberry.field
    def activity(self) -> list[UserActivity]:
        return resolve_activity(self)


def format_timedelta(td: timedelta):
    m = round(td.total_seconds() / 60)
    h = m // 60
    m -= h * 60
    result = f"{h}:{m:02}"
    return result


def resolve_activity(user: User) -> list[UserActivity]:
    # ui.label("TBD").classes("absolute-center")
    entries: list[UserActivity] = []

    for wp in user.db_obj.work_periods:
        # s_start = format_date(wp.started_at)
        if isinstance(wp, db.WorkPeriodTask):
            if wp.ended_at is not None:
                s_dur = format_timedelta(wp.duration)
                short = f"Worked on task {wp.task.name} for {s_dur}"
            else:
                short = f"Started working on task {wp.task.name}."
            entries.append(UserActivity(at=toUTC(wp.started_at), short=short))
        elif isinstance(wp, db.WorkPeriodWorking):
            entries.append(
                UserActivity(at=toUTC(wp.started_at), short="Started working", order=-10)
            )
            if wp.ended_at is not None:
                entries.append(
                    UserActivity(at=toUTC(wp.ended_at), short="Stopped working", order=10)
                )
        elif isinstance(wp, db.WorkPeriodTimesink):
            if wp.ended_at is not None:
                s_dur = format_timedelta(wp.duration)
                short = f"Spent {s_dur} on {wp.timesink.name}."
            else:
                short = f"Started with {wp.timesink.name}."
            entries.append(UserActivity(at=toUTC(wp.started_at), short=short))
    entries.sort(key=lambda el: (el.at, el.order), reverse=True)
    return entries
