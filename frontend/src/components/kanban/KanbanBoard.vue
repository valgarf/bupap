<template>
  <q-scroll-area ref="scrollArea" class="fit col-grow">
    <div
      class="row q-pa-md no-wrap items-stretch q-gutter-md"
      :style="scrollContentStyle"
      @drop="drop"
      @dragover.prevent="(evt) => {}"
    >
      <q-card
        v-for="lane in kanban.laneOrder"
        :key="lane.id"
        class="items-stretch lane-card column"
        @dragover.prevent="(evt) => dragover(lane, evt)"
      >
        <div class="text-weight-bold text-h6 q-mt-md q-ml-md">
          {{ lane.title }}
        </div>
        <q-scroll-area
          class="q-ma-none q-pa-none q-pr-sm col-grow"
          :visible="true"
        >
          <div
            class="q-pa-md"
            :ref="
              (r) => {
                laneRefs[lane.id] = r;
              }
            "
          >
            <KanbanList
              :parent-id="null"
              :nodes="lane.topLevelNodes"
              :depth="0"
              :detached-parent="false"
              :priorities="kanban.priorities"
              @toggle-expand="toggleExpand"
              @dragging-ref="draggingRef"
              @dragstart-card="dragstartCard"
              @open-link="openLink"
            />
          </div>
        </q-scroll-area>
      </q-card>
    </div>
  </q-scroll-area>
</template>


<style scoped>
.lane-card {
  min-width: 500px;
}
</style>

<script lang="ts">
interface KanbanState {
  nodes: { [key: number]: KanbanNode };
  lanes: { [key: string]: KanbanLaneNode };
  laneOrder: KanbanLaneNode[];
  priorities: Tag[];
}
</script>
<script setup lang='ts'>
import KanbanList from './KanbanList.vue';
import {
  computed,
  defineProps,
  defineEmits,
  ref,
  watchEffect,
  nextTick,
} from 'vue';
import {useElementSize} from '@vueuse/core'
import { KanbanNode, KanbanLaneNode, KanbanProps, KanbanPropsData, Tag } from './interfaces';

const props = defineProps<KanbanProps>();
const emit = defineEmits(['movedCards', 'openLink']);
const kanban = ref<KanbanState | null>(null);
const laneRefs = {};
watchEffect(() => {
  kanban.value = computeKanban(props.initialData);
});

const nodes = computed(() => kanban.value?.nodes);
const dragged = ref({
  x: 0,
  y: 0,
  target: null,
  count: 0,
  ref: null,
  blocked: false,
  nodes: [],
});

const scrollArea = ref(null);
const { height: scrollAreaHeight }=useElementSize(scrollArea)
const scrollContentStyle = computed(() => {
  if (scrollAreaHeight.value == 0) {
    return {};
  }
  return { height: `${scrollAreaHeight.value}px !important` };
});

function openLink(val) {
  emit('openLink', val);
}

function computeKanban(initialData: KanbanPropsData):KanbanState {
  let nodes: {[key: number]: KanbanNode} = {};
  for (let [k, v] of Object.entries(initialData.cards)) {
    let intk = parseInt(k);
    nodes[intk] = new KanbanNode(intk, v);
  }

  for (let n of Object.values(nodes)) {
    n.children = n.card.childrenOrder.map((cid) => nodes[cid]);
    if (n.card.parentId != null) {
      let p = nodes[n.card.parentId];
      if (p != undefined) {
        n.parent = p;
      }
    }
  }

  let lanes: { [key: string]: KanbanLaneNode } = {};
  
  for (let [k, v] of Object.entries(initialData.lanes)) {
    let allNodes = v.cardOrder.map((cid) => nodes[cid]);

    let lane = new KanbanLaneNode(v, allNodes);
    lanes[k] = lane;
    for (let node of lane.topLevelNodes) {
      node.lane = lane;
    }
  }

  let laneOrder = initialData.laneOrder.map((lid) => lanes[lid]);

  return { nodes, lanes, laneOrder, priorities: initialData.priorities };
}

function toggleExpand(node: KanbanNode) {
  // TODO: cannot change computed value!
  var n = kanban.value?.nodes[node.id];
  if (n != null) {
    n.expanded = !n.expanded;
  }
}

function dragover(lane: KanbanLaneNode, evt) {
  if (dragged.value.blocked || dragged.value.ref == null) {
    return;
  }
  let x = evt.y;
  let y = evt.y;
  let down = y > dragged.value.y; // movement direction is down
  let up =
    !down &&
    (y < dragged.value.y ||
      dragged.value.nodes.some((node) => node.lane.id != lane.id)); // movement direction is up
  dragged.value.x = x;
  dragged.value.y = y;
  if (!up && !down) {
    return;
  }
  if (dragged.value.nodes.every((node) => node.lane.id == lane.id)) {
    if (lane.finishedSorted) {
      return;
    }
    for (let node of dragged.value.nodes) {
      if (up) {
        moveUp(node, y);
      }
      if (down) {
        moveDown(node, y);
      }
    }
  } else {
    for (let node of dragged.value.nodes) {
      changeLane(node, lane, y);
    }
  }
}
function changeLane(node, lane, y) {
  // TODO cannot simply modify a computed variable
  if (node.lane.id == lane.id) {
    return;
  }
  if (node.topLevel) {
    let index = node.lane.topLevelNodes.indexOf(node);
    node.lane.topLevelNodes.splice(index, 1);
  }
  // try to find correct index
  if (lane.finishedSorted) {
    if (node.parent?.lane.id == lane.id) {
      node.detached = false;
    } else {
      lane.topLevelNodes.splice(0, 0, node);
      node.detached = node.parent != null;
    }
    node.lane = lane;
  } else {
    let index = -1;
    let childIdx = 0;
    let children = laneRefs[lane.id]?.children[0]?.children; // depends on layout!
    for (const child of children) {
      if (child.getBoundingClientRect().top > y) {
        index = childIdx;
        break;
      }
      childIdx += 1;
    }
    if (index == -1) {
      lane.topLevelNodes.push(node);
    } else {
      lane.topLevelNodes.splice(index, 0, node);
    }

    node.detached = node.parent != null;
    node.lane = lane;

    dragged.value.blocked = true;
    nextTick(() => {
      nextTick(() => {
        moveUp(node, y);
      });
    });
  }
}
function moveUp(node, y) {
  dragged.value.blocked = false;

  if (dragged.value.ref.getBoundingClientRect().top <= y) {
    // above mouse, stop movement
    return;
  }

  if (node.topLevel) {
    let index = node.lane.topLevelNodes.indexOf(node);
    if (index == 0) {
      // top of list
      return;
    }
    let nodeAbove = node.lane.topLevelNodes[index - 1];
    node.lane.topLevelNodes.splice(index, 1);
    if (
      node.recursiveParentIds.includes(nodeAbove.id) &&
      node.recursiveParents.every((n) => n.expanded)
    ) {
      // move into parent
      node.lane = null;
      node.detached = false;
      let index = node.parent.children.indexOf(node);
      node.parent.children.splice(index, 1);
      node.parent.children.push(node);
    } else {
      // switch with node above
      node.lane.topLevelNodes.splice(index - 1, 0, node);
    }
  } else {
    let index = node.parent.children.indexOf(node);
    if (index > 0) {
      // switch with node above
      node.parent.children.splice(index, 1);
      node.parent.children.splice(index - 1, 0, node);
    } else {
      // top of list, put above parent node
      let lane = node.lane;
      let index = node.lane.topLevelNodes.indexOf(
        node.recursiveParents.at(-1)
      );
      if (index == -1) {
        console.error(
          "could not determine node's root parent index",
          node,
          node.recursiveParents.at(-1),
          node.lane.topLevelNodes
        );
        return;
      }
      lane.topLevelNodes.splice(index, 0, node);
      node.detached = true;
      node.lane = lane;
    }
  }

  dragged.value.blocked = true;
  nextTick(() => {
    nextTick(() => {
      moveUp(node, y);
    });
  });
}
function moveDown(node, y) {
  dragged.value.blocked = false;

  if (dragged.value.ref.getBoundingClientRect().bottom >= y) {
    // below mouse, stop movement
    return;
  }

  if (node.topLevel) {
    let index = node.lane.topLevelNodes.indexOf(node);
    if (index + 1 == node.lane.topLevelNodes.length) {
      // bottom of list
      return;
    }
    let nodeBelow = node.lane.topLevelNodes[index + 1];
    node.lane.topLevelNodes.splice(index, 1);
    if (
      node.recursiveParentIds.includes(nodeBelow.id) &&
      node.recursiveParents.every((n) => n.expanded)
    ) {
      // move into parent
      node.lane = null;
      node.detached = false;
      let index = node.parent.children.indexOf(node);
      node.parent.children.splice(index, 1);
      node.parent.children.splice(0, 0, node);
    } else {
      // switch with node below
      node.lane.topLevelNodes.splice(index + 1, 0, node);
    }
  } else {
    let index = node.parent.children.indexOf(node);
    if (index + 1 < node.parent.children.length) {
      // switch with node below
      node.parent.children.splice(index, 1);
      node.parent.children.splice(index + 1, 0, node);
    } else {
      // bottom of list, put below parent node
      let lane = node.lane;
      let index = lane.topLevelNodes.indexOf(node.recursiveParents.at(-1));
      if (index == -1) {
        console.error(
          "could not determine node's root parent index",
          node,
          node.recursiveParents.at(-1),
          node.lane.topLevelNodes
        );
        return;
      }
      lane.topLevelNodes.splice(index + 1, 0, node);
      node.detached = true;
      node.lane = lane;
    }
  }

  dragged.value.blocked = true;
  nextTick(() => {
    nextTick(() => {
      moveDown(node, y);
    });
  });
}
function dragstartCard(nodeIds, x, y) {
  dragged.value.x = x;
  dragged.value.y = y;
  dragged.value.nodes = nodeIds.map((nid) => nodes.value[nid]);
  // Note: setting the dragged entry will set it to invisible and it will not be shown
  // during the drag operation. Delaying the invisibility by one frame will generate a
  // drag image and then hide the original card.
  window.requestAnimationFrame(function () {
    for (let nodeId of nodeIds) {
      kanban.value.nodes[nodeId].dragged = true;
    }
  });
}
function drop(evt) {
  let dragDataStr = evt.dataTransfer.getData('application/json');
  if (dragDataStr == null) {
    // not a drag event for us
    return;
  }
  try {
    var dragData = JSON.parse(dragDataStr);
  } catch (err) {
    console.warn('Failed to decode json from drag object:', dragDataStr);
    return;
  }
  if (dragData['nodeIds'] == null) {
    // not a drag event for us
    return;
  }
  let nodeIds = dragData['nodeIds'];
  evt.stopPropagation();
  let nodes = nodeIds.map((nid) => kanban.value.nodes[nid]);
  let lane = nodes[0].lane;
  let orderedNodes = lane.nodes;
  emit('movedCards', {
    lane: lane.id,
    cards: nodes.map((n) => {
      return {
        id: n.id,
        order: orderedNodes.indexOf(n),
        detached: n.detached,
      };
    }),
  });
  for (let node of nodes) {
    node.dragged = false;
  }
  dragged.value.nodes = [];
  dragged.value.ref = null;
}
function draggingRef(ref) {
  dragged.value.ref = ref;
}
</script>
