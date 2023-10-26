from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable, List, Optional

from nicegui import ui

from .model import KanbanCardData


class KanbanCard(ui.element, component="kanban_card_sfc.vue"):
    def __init__(
        self,
        card: KanbanCardData,
        on_open_link: Callable[[KanbanCardData], None | Awaitable[None]] | None = None,
    ) -> None:
        super().__init__()
        self._props["card"] = card
        self.on("open_link", self._open_link)
        self._on_open_link = on_open_link

    async def _open_link(self, evt):
        print(evt.args)
        # self.date = date.fromisoformat(evt.args)
        # if self._on_change:
        #     result = self._on_change(date.fromisoformat(evt.args))
        #     if isawaitable(result):
        #         await result
