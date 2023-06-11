from dataclasses import dataclass, field
from datetime import datetime, timedelta

from bupap import db


@dataclass
class TaskStart:
    task_id: int
    user_id: int
    started_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TimesinkStart:
    timesink_id: int
    user_id: int
    started_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ClockIn:
    user_id: int
    started_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TaskEnd:
    task_id: int
    user_id: int
    ended_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class TimesinkEnd:
    timesink_id: int
    user_id: int
    ended_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ClockOut:
    user_id: int
    ended_at: datetime = field(default_factory=datetime.utcnow)


@dataclass
class WorkPeriodEnd:
    work_period_id: int
    ended_at: datetime = field(default_factory=datetime.utcnow)
