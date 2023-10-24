from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum, auto
from functools import lru_cache
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Dict, List, Optional

from loguru import logger
from nicegui import ui

from ..errors import Errors
from .card import KanbanCard
from .model import KanbanCardData, KanbanData, KanbanLaneData, KanbanTag


class Kanban(ui.element, component="kanban_board.vue"):
    def __init__(
        self,
        data: KanbanData,
        on_card_change: Callable[[KanbanCardData | None, KanbanCardData], None | Awaitable[None]]
        | None = None,
        on_open_link: Callable[[KanbanCardData], None | Awaitable[None]] | None = None,
    ) -> None:
        super().__init__()
        self._props["initial_data"] = data
        self.on("card_changed", self._card_changed)
        self.on("open_link", self._open_link)
        self._on_card_change = on_card_change
        self._on_open_link = on_open_link

    async def _card_changed(self, evt):
        print(evt.args)
        # self.date = date.fromisoformat(evt.args)
        # if self._on_change:
        #     result = self._on_change(date.fromisoformat(evt.args))
        #     if isawaitable(result):
        #         await result

    async def _open_link(self, evt):
        print(evt.args)
        # self.date = date.fromisoformat(evt.args)
        # if self._on_change:
        #     result = self._on_change(date.fromisoformat(evt.args))
        #     if isawaitable(result):
        #         await result
