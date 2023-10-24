from dataclasses import dataclass, field


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
    children_order: list[str] = field(default_factory=list)
    lane_id: str | None = None
    parent_id: str | None = None


@dataclass
class KanbanLaneData:
    id: str
    title: str
    card_order: list[str] = field(default_factory=list)


@dataclass
class KanbanData:
    lanes: dict[str, KanbanLaneData] = field(default_factory=dict)
    cards: dict[str, KanbanCardData] = field(default_factory=dict)
    lane_order: list[str] = field(default_factory=list)

    def lane_for_card(self, card: KanbanCardData) -> KanbanLaneData | None:
        for l in self.lanes:
            if l.id == card.lane_id:
                return l
        return None
