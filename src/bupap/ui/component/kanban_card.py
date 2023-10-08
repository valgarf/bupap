from __future__ import annotations

from dataclasses import dataclass, field
from typing import Awaitable, Callable, List, Optional

from nicegui import ui
from py_ts_interfaces import Interface


@dataclass
class KanbanTag(Interface):
    text: str
    color: str
    text_color: str


@dataclass
class KanbanCardData(Interface):
    id: str
    title: str
    tags: List[KanbanTag]
    detached: bool
    link: bool
    children_order: List[str] = field(default_factory=list)
    lane_id: Optional[str] = None
    parent_id: Optional[str] = None


class KanbanCard(ui.element, component="kanban_card.vue"):
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
