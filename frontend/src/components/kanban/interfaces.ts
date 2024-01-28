export interface Tag {
  key?: string;
  text: string;
  color: string;
}

export interface Progress {
  0: number;
  1: number;
  2: number;
}

export interface Card {
  id: number;
  title: string;
  progress?: Progress;
  laneId: string;
  depth: number;
  link: boolean;
  active: boolean;
  finishedAt?: string;
  tags: Tag[];
  priority: string;
  detached: boolean;
  childrenOrder: number[];
  parentId?: number;
}

export interface CardProps {
  card: Card;
  detached: boolean;
  dragged: boolean;
  priorities: Tag[];
}

export interface Lane {
  id: string;
  title: string;
  finishedSorted: boolean;
  prioritySorted: boolean;
  cardOrder: number[];
}

export interface KanbanListProps {
  parentId: string;
  nodes: KanbanNode[];
  depth: number;
  detachedParent: boolean;
  priorities: Tag[];
}

export interface KanbanPropsData {
  priorities: Tag[];
  lanes: { [key: string]: Lane };
  laneOrder: string[];
  cards: { [key: number]: Card };
}

export interface KanbanProps {
  initialData: KanbanPropsData;
}

export class KanbanNode {
  parent: KanbanNode | null;
  children: KanbanNode[];
  id: number;
  card: Card;
  expanded: boolean;
  dragged: boolean;
  private _lane: KanbanLaneNode | null; // Replace 'any' with more specific type if known

  constructor(id: number, card: Card) {
    this.parent = null;
    this.children = [];
    this.id = id;
    this.card = card;
    this.expanded = false;
    this.dragged = false;
    this._lane = null;
  }

  get lane(): KanbanLaneNode {
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    return this.topLevel ? this._lane! : this.parent!.lane;
  }

  set lane(value: KanbanLaneNode) {
    // Replace 'any' with more specific type if known
    if (this.detached || this.parent == null) {
      this._lane = value;
    } else {
      if (value.id != this.lane.id) {
        console.error(
          'Setter called with unexpected lane.',
          this,
          this.lane,
          value
        );
      }
    }
  }

  get topLevel(): boolean {
    return this.detached || this.parent == null;
  }

  get detached(): boolean {
    return this.card.detached;
  }

  set detached(value: boolean) {
    this.card.detached = value;
  }

  recursiveChildren(attachedOnly: boolean): KanbanNode[] {
    const result: KanbanNode[] = [];
    for (const child of this.children) {
      if (!attachedOnly || !child.detached) {
        result.push(child, ...child.recursiveChildren(attachedOnly));
      }
    }
    return result;
  }

  get recursiveParents(): KanbanNode[] {
    const result: KanbanNode[] = [];
    let p: KanbanNode | null = this.parent;
    while (p != null) {
      result.push(p);
      if (p.detached) {
        break;
      }
      p = p.parent;
    }
    return result;
  }

  get recursiveParentIds(): number[] {
    return this.recursiveParents.map((p) => p.id);
  }
}

export class KanbanLaneNode {
  id: string;
  title: string;
  finishedSorted: boolean;
  prioritySorted: boolean;
  topLevelNodes: KanbanNode[];

  constructor(lane: Lane, allNodes: KanbanNode[]) {
    this.id = lane.id;
    this.title = lane.title;
    this.finishedSorted = lane.finishedSorted;
    this.prioritySorted = lane.prioritySorted;
    this.topLevelNodes = allNodes.filter((n) => n.detached || n.parent == null);
  }

  get nodes(): KanbanNode[] {
    const result: KanbanNode[] = [];
    for (const node of this.topLevelNodes) {
      result.push(node, ...node.recursiveChildren(true));
    }
    return result;
  }
}
