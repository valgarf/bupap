from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from zoneinfo import ZoneInfo

import sqlalchemy as sa
import sqlalchemy.orm
from fastapi import Request

# def is_authenticated(request: Request) -> bool:
#     return session_info.get(request.session.get('id'), {}).get('authenticated', False)
from loguru import logger
from nicegui import globals, ui

from bupap import db


class LoginRequiredException(RuntimeError):
    pass


def get_db_session(request: Request) -> sa.orm.Session:
    return request.state.session


def get_user(request: Request, required: bool = True) -> db.User:
    result = None
    user_session_id = request.session.get("id")
    if user_session_id:
        db_session = get_db_session(request)
        result = db_session.scalars(
            sa.select(db.User).where(db.User.session_id == user_session_id)
        ).first()
    logger.debug(
        "user retrieval for session {} -> {}", user_session_id, result.name if result else None
    )
    if required and result is None:
        raise LoginRequiredException()
    return result


def client_data() -> Dict[Any, Any]:
    return globals.index_client._custom_data


def format_timedelta(td: timedelta):
    m = round(td.total_seconds() / 60)
    h = m // 60
    m -= h * 60
    result = f"{h}:{m:02}"
    return result


def format_date(dt: datetime):
    dt_tzaware = dt.replace(tzinfo=timezone.utc)
    dt_converted = (
        dt_tzaware.astimezone()
    )  # TODO: should user user's timezone. This is server timezone
    return dt_converted.date().isoformat()


def format_time(dt: datetime):
    dt_tzaware = dt.replace(tzinfo=timezone.utc)
    dt_converted = (
        dt_tzaware.astimezone()
    )  # TODO: should user user's timezone. This is server timezone
    t = dt_converted.time()
    return f"{t.hour: 2}:{t.minute:02}"


async def get_timezone_from_browser():
    return ZoneInfo(await ui.run_javascript("Intl.DateTimeFormat().resolvedOptions().timeZone"))
