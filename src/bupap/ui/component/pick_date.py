from dataclasses import asdict, dataclass
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum, auto
from functools import lru_cache
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Optional

from loguru import logger
from nicegui import ui

from .errors import Errors

# register_component("pick_date", __file__, "pick_date.vue")


class PickDate(ui.element, component="pick_date.vue"):
    def __init__(
        self,
        initial: date | None = None,
        on_change: Callable[[date], None | Awaitable[None]] | None = None,
    ) -> None:
        super().__init__()
        if initial is None:
            initial = date.today()
        self._props["initial"] = initial
        self.on("changed", self._changed)
        self._on_change = on_change
        self.date = initial

    async def _changed(self, evt):
        self.date = date.fromisoformat(evt.args)
        if self._on_change:
            result = self._on_change(date.fromisoformat(evt.args))
            if isawaitable(result):
                await result

    def set_date(self, date: date, emit: bool = True):
        self.date = date
        self.run_method("update_date", date.isoformat(), emit)
