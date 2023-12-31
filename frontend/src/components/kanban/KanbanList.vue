<template>
  <div :class="column_classes()">
    <div
      v-for="node in list_entries()"
      :class="card_div_classes(node)"
      :key="node_key(node)"
      @dragstart="(evt) => dragstart(node, evt)"
    >
      <template v-if="node.card.detached && this.depth == 0">
        <KanbanCard
          class="q-mt-none"
          :class="card_classes(node.parent)"
          :card="node.parent.card"
          :detached="true"
          :dragged="false"
          :priorities="this.priorities"
          @open_link="open_link"
        />
        <div class="row items-stretch">
          <div style="width: 32px"></div>
          <KanbanList
            class="col-grow"
            :parent_id="node.parent.id"
            :nodes="[node]"
            :depth="depth + 1"
            :detached_parent="true"
            :priorities="this.priorities"
            @toggle_expand="toggle_expand"
            @dragging_ref="dragging_ref"
            @dragstart_card="dragstart_card"
            @open_link="open_link"
          />
        </div>
      </template>
      <template v-else>
        <KanbanCard
          :draggable="!node_is_detached(node)"
          :class="card_classes(node)"
          :card="node.card"
          :detached="node_is_detached(node)"
          :dragged="node_is_drag_target(node)"
          :priorities="this.priorities"
          @dragging_ref="dragging_ref"
          @open_link="open_link"
        />
        <div
          v-if="
            node.children.length > 0 &&
            !(node.card.detached && this.depth > 0 && !this.detached_parent)
          "
          class="row items-stretch"
        >
          <q-btn
            :class="toggle_btn_classes(node)"
            @click="(evt) => toggle_expand(node)"
            >{{ toggle_btn_text(node) }}</q-btn
          >
          <KanbanList
            v-if="node.expanded && !node.dragged"
            class="col-grow"
            :parent_id="node.id"
            :nodes="node.children"
            :depth="depth + 1"
            :detached_parent="false"
            :priorities="this.priorities"
            @toggle_expand="toggle_expand"
            @dragging_ref="dragging_ref"
            @dragstart_card="dragstart_card"
            @open_link="open_link"
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
import { computed, defineProps, defineEmits, ref } from 'vue';
import KanbanCard from './KanbanCard.vue';

const props = defineProps([
  'parent_id',
  'nodes',
  'depth',
  'detached_parent',
  'priorities',
]);
const emit = defineEmits([
  'dragstart_card',
  'dragging_ref',
  'open_link',
  'toggle_expand',
]);
function list_entries() {
  return props.nodes;
}
function node_key(node) {
  return (
    props.depth +
    '-' +
    props.parent_id +
    '-' +
    node.id +
    '-' +
    props.detached_parent +
    '-' +
    node.card.detached
  );
}
function node_is_detached(node) {
  return node.card.detached && props.depth > 0 && !props.detached_parent;
}
function node_is_drag_target(node) {
  return node.dragged && !node_is_detached(node);
}
// open_link(val) {
//     console.log(val);
// },
function column_classes() {
  var result = ['nicegui-column', 'p-0', 'm-0', 'items-stretch'];
  if (props.depth == 0) {
    result.push('gap-2');
  } else {
    result.push('mt-2');
    result.push('gap-1');
  }
  return result;
}
function toggle_btn_classes(node) {
  if (node.expanded) {
    return ['w-10', 'mt-2', 'mr-1'];
  } else {
    return 'ml-10 h-5 grow mt-2';
  }
}
function card_div_classes(node) {
  var result = [];
  // if (card.depth > 0)
  // result.push("mt-[-4pt]")
  if (!show_card(node)) {
    result.push('invisible');
  }
  return result;
}
function card_classes(card) {
  var result = [];
  // if (!this.show_card(card)) {
  //     result.push("invisible")
  // }
  return result;
}
function toggle_btn_text(node) {
  if (node.expanded) {
    return '';
  }
  let num = node.children.length;
  return num + ' ' + (num > 1 ? 'subtasks' : 'subtask');
}
function show_card(node) {
  return !node.dragged || this.node_is_detached(node);
  // return (this.dragged.entry == null || this.dragged.entry.id != card.id);
}
function toggle_expand(node) {
  emit('toggle_expand', node);
}
function dragstart(node, evt) {
  evt.dataTransfer.clearData();
  let drag_data = {
    parent_id: node.parent == null ? null : node.parent.id,
    node_ids: [node.id],
  };
  evt.dataTransfer.setData('application/json', JSON.stringify(drag_data));
  // TODO: set task url
  evt.stopPropagation();
  dragstart_card([node.id], evt.x, evt.y);
}
function dragstart_card(node_ids, x, y) {
  emit('dragstart_card', node_ids, x, y);
}
function dragging_ref(ref) {
  emit('dragging_ref', ref);
}
function open_link(val) {
  emit('open_link', val);
}
</script>

