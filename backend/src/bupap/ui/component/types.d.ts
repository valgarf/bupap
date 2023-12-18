// Generated using py-ts-interfaces.
// See https://github.com/cs-cordero/py-ts-interfaces

interface KanbanTag {
    text: string;
    color: string;
}

interface KanbanCardData {
    id: string;
    title: string;
    tags: Array<KanbanTag>;
    detached: boolean;
    link: boolean;
    children_order: Array<string>;
    lane_id: string | null;
    parent_id: string | null;
    depth: number;
}

interface KanbanLane {
    id: string;
    title: string;
    card_order: Array<string>;
}

interface KanbanData {
    lanes: Record<string, KanbanLane>;
    cards: Record<string, KanbanCard>;
    lane_order: Array<string>;
}
