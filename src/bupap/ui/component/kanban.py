from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import date, datetime, time, timedelta, timezone
from enum import Enum, auto
from functools import lru_cache
from inspect import isawaitable
from typing import Any, Awaitable, Callable, Dict, List, Optional

from loguru import logger
from nicegui import ui
from py_ts_interfaces import Interface

from .errors import Errors
from .kanban_card import KanbanCard, KanbanCardData, KanbanTag


@dataclass
class KanbanLane(Interface):
    id: str
    title: str
    card_order: List[str] = field(default_factory=list)


@dataclass
class KanbanData(Interface):
    lanes: Dict[str, KanbanLane] = field(default_factory=dict)
    cards: Dict[str, KanbanCardData] = field(default_factory=dict)
    lane_order: List[str] = field(default_factory=list)

    def lane_for_card(self, card: KanbanCardData) -> KanbanLane | None:
        for l in self.lanes:
            if l.id == card.lane_id:
                return l
        return None


class Kanban(ui.element, component="kanban.vue"):
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
