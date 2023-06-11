from __future__ import annotations

import heapq
from dataclasses import dataclass, field
from datetime import date, datetime, time, timezone
from enum import Enum, Flag, auto
from typing import TYPE_CHECKING, Any, Iterator
from zoneinfo import ZoneInfo

import sqlalchemy as sa
from dateutil.rrule import (
    DAILY,
    FR,
    MO,
    MONTHLY,
    SA,
    SU,
    TH,
    TU,
    WE,
    WEEKLY,
    YEARLY,
    rrule,
    rruleset,
)
from more_itertools import peekable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, InheritanceBase, InheritanceFK, intfk, str_30, str_50, text

if TYPE_CHECKING:
    from .user import User


class Weekdays(Flag):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()

    def to_rrule(self):
        if len(self) == 0:
            return None
        match self:
            case Weekdays.MONDAY:
                return MO
            case Weekdays.TUESDAY:
                return TU
            case Weekdays.WEDNESDAY:
                return WE
            case Weekdays.THURSDAY:
                return TH
            case Weekdays.FRIDAY:
                return FR
            case Weekdays.SATURDAY:
                return SA
            case Weekdays.SUNDAY:
                return SU
            case _:
                return [f.to_rrule() for f in self]


class Frequency(Enum):
    WEEKLY = WEEKLY
    DAILY = DAILY
    MONTHLY = MONTHLY
    YEARLY = YEARLY


class WeekdaysType(sa.types.TypeDecorator):
    impl = sa.types.Integer

    cache_ok = True

    def process_bind_param(self, value, dialect):
        return value.value

    def process_result_value(self, value, dialect):
        return Weekdays(value)


class RRuleDate(InheritanceBase, Base):
    # rrule input
    freq: Mapped[Frequency]
    byweekday: Mapped[Weekdays] = mapped_column(WeekdaysType)
    interval: Mapped[int]
    dtstart: Mapped[date]
    until: Mapped[date | None]

    def to_rrule(self):
        return rrule(
            freq=self.freq.value,
            dtstart=datetime.combine(self.dtstart, time(), tzinfo=None),
            interval=self.interval,
            byweekday=self.byweekday.to_rrule(),
            until=self.until,
        )


class ScheduleRule(InheritanceFK, RRuleDate):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    timezone: Mapped[str_30]
    start: Mapped[time]
    end: Mapped[time]

    user: Mapped[User] = relationship(back_populates="schedule")


class Absence(InheritanceFK, RRuleDate):
    user_id: Mapped[intfk] = mapped_column(sa.ForeignKey("User.id"))
    reason: Mapped[str_50 | None]

    user: Mapped[User] = relationship(back_populates="absence")


@dataclass
class _Schedule:
    rule: ScheduleRule
    rruleset: rruleset = field(
        init=False,
    )
    timezone: ZoneInfo = field(
        init=False,
    )
    naive: bool = False  # if true, datetimes are returned as naive times after converting to UTC

    def __post_init__(self):
        self.rruleset = rruleset()
        self.rruleset.rrule(self.rule.to_rrule())
        self.timezone = ZoneInfo(self.rule.timezone)
        for absence in self.rule.user.absence:
            self.rruleset.exrule(absence.to_rrule())

    def xafter(self, start: date) -> Iterator[tuple[datetime, datetime]]:
        for day in self.rruleset.xafter(datetime.combine(start, time(), tzinfo=None), inc=True):
            start = datetime.combine(day, self.rule.start, tzinfo=self.timezone)
            end = datetime.combine(day, self.rule.end, tzinfo=self.timezone)
            if self.naive:
                start = start.astimezone(timezone.utc).replace(tzinfo=None)
                end = end.astimezone(timezone.utc).replace(tzinfo=None)
            yield (start, end)


def iterate_schedule(user, start: date, naive: bool = False) -> Iterator[tuple[datetime, datetime]]:
    schedule_data = [_Schedule(rule=rule, naive=naive) for rule in user.schedule]
    return heapq.merge(*[el.xafter(start) for el in schedule_data])
