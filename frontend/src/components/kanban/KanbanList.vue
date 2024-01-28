<template>
  <div :class="columnClasses()">
    <div
      v-for="node in listEntries()"
      :class="cardDivClasses(node)"
      :key="nodeKey(node)"
      @dragstart="(evt) => dragstart(node, evt)"
    >
      <template v-if="node.card.detached && depth == 0">
        <KanbanCard
          class="q-mt-none"
          :card="node.parent.card"
          :detached="true"
          :dragged="false"
          :priorities="priorities"
          @open-link="openLink"
        />
        <div class="row items-stretch">
          <div style="width: 32px"></div>
          <KanbanList
            class="col-grow"
            :parent-id="node.parent.id"
            :nodes="[node]"
            :depth="depth + 1"
            :detached-parent="true"
            :priorities="priorities"
            @toggle-expand="toggleExpand"
            @dragging-ref="draggingRef"
            @dragstart-card="dragstartCard"
            @open-link="openLink"
          />
        </div>
      </template>
      <template v-else>
        <KanbanCard
          :draggable="!nodeIsDetached(node)"
          :card="node.card"
          :detached="nodeIsDetached(node)"
          :dragged="nodeIsDragTarget(node)"
          :priorities="priorities"
          @dragging-ref="draggingRef"
          @open-link="openLink"
        />
        <div
          v-if="
            node.children.length > 0 &&
            !(node.card.detached && depth > 0 && !detachedParent)
          "
          class="row items-stretch"
        >
          <q-btn
            :class="toggleBtnClasses(node)"
            @click="(evt) => toggleExpand(node)"
            >{{ toggleBtnText(node) }}</q-btn
          >
          <KanbanList
            v-if="node.expanded && !node.dragged"
            class="col-grow"
            :parent-id="node.id"
            :nodes="node.children"
            :depth="depth + 1"
            :detached-parent="false"
            :priorities="priorities"
            @toggle-expand="toggleExpand"
            @dragging-ref="draggingRef"
            @dragstart-card="dragstartCard"
            @open-link="openLink"
          />
        </div>
      </template>
    </div>
  </div>
</template>

<script lang='ts'>
// import type {KanbanCardData} from './KanbanCard.vue'
// export interface KanbanListData {

// }

</script>

<script setup lang='ts'>
import { defineProps, defineEmits } from 'vue';
import KanbanCard from './KanbanCard.vue';

const props = defineProps([
  'parentId',
  'nodes',
  'depth',
  'detachedParent',
  'priorities',
]);
const emit = defineEmits([
  'dragstartCard',
  'draggingRef',
  'openLink',
  'toggleExpand',
]);
function listEntries() {
  return props.nodes;
}
function nodeKey(node) {
  return (
    props.depth +
    '-' +
    props.parentId +
    '-' +
    node.id +
    '-' +
    props.detachedParent +
    '-' +
    node.card.detached
  );
}
function nodeIsDetached(node) {
  return node.card.detached && props.depth > 0 && !props.detachedParent;
}
function nodeIsDragTarget(node) {
  return node.dragged && !nodeIsDetached(node);
}
// open_link(val) {
//     console.log(val);
// },
function columnClasses() {
  var result = ['column', 'q-pa-none', 'q-ma-none', 'items-stretch'];
  if (props.depth == 0) {
    result.push('q-gutter-md');
  } else {
    // result.push('q-mt-none');
    result.push('q-gutter-sm');
  }
  return result;
}
function toggleBtnClasses(node) {
  if (node.expanded) {
    return ['q-mt-sm', 'q-mr-xs'];
  } else {
    return 'q-ml-xl col-grow q-mt-sm';
  }
}
function cardDivClasses(node) {
  var result = [];
  // if (card.depth > 0)
  // result.push("mt-[-4pt]")
  if (!showCard(node)) {
    result.push('invisible');
  }
  return result;
}
function toggleBtnText(node) {
  if (node.expanded) {
    return '';
  }
  let num = node.children.length;
  return num + ' ' + (num > 1 ? 'subtasks' : 'subtask');
}
function showCard(node) {
  return !node.dragged || nodeIsDetached(node);
  // return (this.dragged.entry == null || this.dragged.entry.id != card.id);
}
function toggleExpand(node) {
  emit('toggleExpand', node);
}
function dragstart(node, evt) {
  evt.dataTransfer.clearData();
  let dragData = {
    parentId: node.parent == null ? null : node.parent.id,
    nodeIds: [node.id],
  };
  evt.dataTransfer.setData('application/json', JSON.stringify(dragData));
  // TODO: set task url
  evt.stopPropagation();
  dragstartCard([node.id], evt.x, evt.y);
}
function dragstartCard(nodeIds, x, y) {
  emit('dragstartCard', nodeIds, x, y);
}
function draggingRef(ref) {
  emit('draggingRef', ref);
}
function openLink(val) {
  emit('openLink', val);
}
</script>

