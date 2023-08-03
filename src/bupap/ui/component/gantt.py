from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum, auto
from functools import lru_cache
from typing import Any, Callable, Optional

from loguru import logger
from nicegui import ui

from .errors import Errors


class GanttMode(Enum):
    DAY = auto()


class GanttEntryType(Enum):
    BAR = auto()
    BG = auto()
    FG = auto()


@dataclass
class GanttEntryData:
    key: str
    start: datetime
    end: datetime
    color: str
    text: str
    type_: GanttEntryType


@dataclass
class GanttRowData:
    key: str
    idx: int
    entries: list[GanttEntryData]


def _remainder_dt_td(dt: datetime, td: timedelta) -> timedelta:
    time_of_day = dt - dt.replace(hour=0, minute=0, second=0, microsecond=0) + timedelta(days=1)
    return time_of_day - td * (time_of_day // td)


@dataclass
class GanttData:
    row_names: list[str]
    row_data: list[GanttRowData]
    now: datetime

    def start(self, start_min: datetime, start_default: datetime, rounding: timedelta):
        start = min(
            [entry.start for row in self.row_data for entry in row.entries], default=start_default
        )
        start -= _remainder_dt_td(start, rounding)
        start -= rounding / 2
        return max(start, start_min)

    def end(self, end_max: datetime, end_default: datetime, rounding: timedelta):
        end = (
            max([entry.end for row in self.row_data for entry in row.entries], default=end_default)
            + rounding / 2
        )
        r = _remainder_dt_td(end, rounding)
        if r.total_seconds() > 0:
            end += rounding - r
        end += rounding / 2
        return min(end, end_max)


@lru_cache()
def _calc_text_color(col: str):
    assert col.startswith("#")
    assert len(col) == 7
    r = int(col[1:3], 16)
    g = int(col[3:5], 16)
    b = int(col[5:7], 16)
    # formulat taken from https://stackoverflow.com/questions/3942878/how-to-decide-font-color-in-white-or-black-depending-on-background-color
    return "#000000" if (r * 0.299 + g * 0.587 + b * 0.114) > 186 else "#ffffff"


class Gantt(ui.element, component="gantt.vue"):
    def __init__(
        self,
        title: str,
        initial_date: date,
        user_data: Any,
        get_data: Callable[[GanttMode, datetime, datetime, Any], GanttData],
        open_item: Callable[[str], None],
        *,
        on_change: Optional[Callable] = None
    ) -> None:
        super().__init__()
        self._props["title"] = title
        self.on("change", on_change)
        self._get_data = get_data
        start = datetime.combine(initial_date, time(0, 0))
        end = datetime.combine(initial_date, time(23, 59))
        self.user_data = user_data
        self.on(
            "load_data",
            lambda evt: self._set_new_data(
                self._get_data(GanttMode.DAY, start, end, user_data), start, end
            ),
        )
        self.on("open_item", lambda evt: open_item(evt["args"]))

    def set_day(self, day: date):
        start = datetime.combine(day, time(0, 0))
        end = datetime.combine(day, time(23, 59))
        self._set_new_data(self._get_data(GanttMode.DAY, start, end, self.user_data), start, end)

    @Errors.wrap_error("Failed to send Gantt Data")
    def _set_new_data(self, gantt_data: GanttData, start: datetime, end: datetime):
        data = asdict(gantt_data)
        start = gantt_data.start(start, start + (end - start) * 0.4, timedelta(hours=1))
        end = gantt_data.end(end, start + (end - start) * 0.6, timedelta(hours=1))

        def _convert_dt(dt: datetime):
            return (dt - start).total_seconds()

        for row, name in zip(data["row_data"], gantt_data.row_names):
            row["bg"] = []
            row["fg"] = []
            row["bar"] = []
            row["name"] = name
            for entry in row["entries"]:
                entry["start"] = entry["start"].replace(tzinfo=timezone.utc)
                entry["end"] = entry["end"].replace(tzinfo=timezone.utc)
                entry["text_color"] = _calc_text_color(entry["color"])
                row[entry["type_"].name.lower()].append(entry)
            del row["entries"]
        del data["row_names"]
        data["start"] = start.replace(tzinfo=timezone.utc)
        data["end"] = end.replace(tzinfo=timezone.utc)
        data["now"] = gantt_data.now.replace(tzinfo=timezone.utc)

        # logger.debug(data)
        self.run_method("set_new_data", data)

    def random(self) -> None:
        self.run_method("random")


# ["2de1c2","f25757","63474d","d4b2d8","edae49"]
