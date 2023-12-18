from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class KanbanTag:
    text: str
    color: str
    text_color: str


@dataclass
class KanbanCardData:
    id: str
    title: str
    tags: list[KanbanTag]
    detached: bool
    link: bool
    depth: int
    priority: str
    children_order: list[str] = field(default_factory=list)
    lane_id: str | None = None
    parent_id: str | None = None
    progress: tuple[float, float, float] | None = None
    active: bool = False
    finished_at: datetime | None = None


@dataclass
class KanbanLaneData:
    id: str
    title: str
    priority_sorted: bool = False
    finished_sorted: bool = False
    card_order: list[str] = field(default_factory=list)


@dataclass
class KanbanData:
    lanes: dict[str, KanbanLaneData] = field(default_factory=dict)
    cards: dict[str, KanbanCardData] = field(default_factory=dict)
    priorities: list[KanbanTag] = field(default_factory=list)
    lane_order: list[str] = field(default_factory=list)

    def lane_for_card(self, card: KanbanCardData) -> KanbanLaneData | None:
        for l in self.lanes:
            if l.id == card.lane_id:
                return l
        return None
