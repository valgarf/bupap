<template>
  <q-scroll-area ref="scrollArea" class="fit col-grow">
    <div
      class="row q-pa-md no-wrap items-stretch q-gutter-md"
      :style="scrollContentStyle"
      @drop="drop"
      @dragover.prevent="(evt) => {}"
    >
      <q-card
        v-for="lane in kanban.lane_order"
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
                lane_refs[lane.id] = r;
              }
            "
          >
            <KanbanList
              :parent_id="null"
              :nodes="lane.top_level_nodes"
              :depth="0"
              :detached_parent="false"
              :priorities="kanban.priorities"
              @toggle_expand="toggle_expand"
              @dragging_ref="dragging_ref"
              @dragstart_card="dragstart_card"
              @open_link="open_link"
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

 <!-- <div v-for="card in flat_cards(lane)" :class="card_div_classes(card)" :key="card.id" @dragenter="(evt) => dragenter(card, evt)" @dragover="(evt) => dragover(card, evt)" @dragstart="(evt) => dragstart(card, evt)" @dragend="(evt) => dragend(card, evt)">
                        <nicegui-kanban_card draggable="true" :class="card_classes(card)" :card="card"/>
                    </div> -->

<script setup lang='ts'>
import KanbanList from './KanbanList.vue';
import {
  computed,
  defineProps,
  defineEmits,
  ref,
  watchEffect,
  getCurrentInstance,
  nextTick,
} from 'vue';

const props = defineProps(['initial_data']);
const emit = defineEmits(['moved_cards', 'open_link']);
const kanban = ref<any>(null);
const lane_refs = {};
watchEffect(() => {
  kanban.value = compute_kanban(props.initial_data);
});

const nodes = computed(() => kanban.value.nodes);
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

const scrollHeight = ref(0);
function onResize() {
  scrollHeight.value = scrollArea.value.$el.clientHeight;
}
const ro = new ResizeObserver(onResize);
watchEffect(() => {
  if (scrollArea.value != null) {
    ro.observe(scrollArea.value.$el);
  }
});

const scrollContentStyle = computed(() => {
  if (scrollHeight.value == 0) {
    return {};
  }
  return { height: `${scrollHeight.value}px !important` };
});

function open_link(val) {
  emit('open_link', val);
}

function compute_kanban(initial_data) {
  let nodes = {};
  for (let [k, v] of Object.entries(initial_data.cards)) {
    let intk = parseInt(k);
    nodes[intk] = {
      parent: null,
      children: [],
      id: intk,
      card: v,
      expanded: false,
      dragged: false,
      _lane: null,
      get lane() {
        return this.top_level ? this._lane : this.parent.lane;
      },
      set lane(value) {
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
      },
      get top_level() {
        return this.detached || this.parent == null;
      },
      get detached() {
        return this.card.detached;
      },
      set detached(value) {
        this.card.detached = value;
      },
      recursive_children(attached_only) {
        let result = [];
        for (let c of this.children) {
          if (!attached_only || !c.detached) {
            result.push(c, ...c.recursive_children(attached_only));
          }
        }
        return result;
      },
      get recursive_parents() {
        let result = [];
        let p = this.parent;
        while (p != null) {
          result.push(p);
          if (p.detached) {
            break;
          }
          p = p.parent;
        }
        return result;
      },
      get recursive_parent_ids() {
        return this.recursive_parents.map((p) => p.id);
      },
    };
  }

  for (let n of Object.values(nodes)) {
    n.children = n.card.children_order.map((cid) => nodes[cid]);
    let p = nodes[n.card.parent_id];
    if (p != undefined) {
      n.parent = p;
    }
  }

  let lanes = {};
  for (let [k, v] of Object.entries(initial_data.lanes)) {
    let all_nodes = v.card_order.map((cid) => nodes[cid]);

    let lane = {
      id: v.id,
      title: v.title,
      finished_sorted: v.finished_sorted,
      priority_sorted: v.priority_sorted,
      top_level_nodes: [],
      get nodes() {
        let result = [];
        for (let n of this.top_level_nodes) {
          result.push(n, ...n.recursive_children(true));
        }
        return result;
      },
      top_level_nodes: all_nodes.filter((n) => {
        return n.detached || n.parent == null;
      }),
    };
    lanes[k] = lane;
    for (let node of lane.top_level_nodes) {
      node._lane = lane;
    }
  }

  let lane_order = initial_data.lane_order.map((lid) => lanes[lid]);

  return { nodes, lanes, lane_order, priorities: initial_data.priorities };
}

function toggle_expand(node) {
  // TODO: cannot change computed value!
  var n = kanban.value.nodes[node.id];
  n.expanded = !n.expanded;
}
function acceptable_above(orig_card, target_card, target_lane, target_idx) {
  return true;
  // return (target_card.parent_id == null || orig_card.parent_id == target_card.parent_id)
}
function acceptable_below(orig_card, target_card, target_lane, target_idx) {
  return true;
  // if (target_lane.card_order.length <= target_idx + 1) {
  //     return true
  // }
  // target_card = this.kanban.cards[target_lane.card_order[target_idx+1]]
  // return this.acceptable_above(orig_card, target_card, target_lane, target_idx+1)
}

function dragover(lane, evt) {
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
    if (lane.finished_sorted) {
      return;
    }
    for (let node of dragged.value.nodes) {
      if (up) {
        move_up(node, y);
      }
      if (down) {
        move_down(node, y);
      }
    }
  } else {
    for (let node of dragged.value.nodes) {
      change_lane(node, lane, y);
    }
  }
}
function change_lane(node, lane, y) {
  // TODO cannot simply modify a computed variable
  if (node.lane.id == lane.id) {
    return;
  }
  if (node.top_level) {
    let index = node.lane.top_level_nodes.indexOf(node);
    node.lane.top_level_nodes.splice(index, 1);
  }
  // try to find correct index
  if (lane.finished_sorted) {
    if (node.parent?.lane.id == lane.id) {
      node.detached = false;
    } else {
      lane.top_level_nodes.splice(0, 0, node);
      node.detached = node.parent != null;
    }
    node.lane = lane;
  } else {
    let index = -1;
    let child_idx = 0;
    let children = lane_refs[lane.id]?.children[0]?.children; // depends on layout!
    for (const child of children) {
      if (child.getBoundingClientRect().top > y) {
        index = child_idx;
        break;
      }
      child_idx += 1;
    }
    if (index == -1) {
      lane.top_level_nodes.push(node);
    } else {
      lane.top_level_nodes.splice(index, 0, node);
    }

    node.detached = node.parent != null;
    node.lane = lane;

    dragged.value.blocked = true;
    nextTick(() => {
      nextTick(() => {
        move_up(node, y);
      });
    });
  }
}
function move_up(node, y) {
  dragged.value.blocked = false;

  if (dragged.value.ref.getBoundingClientRect().top <= y) {
    // above mouse, stop movement
    return;
  }

  if (node.top_level) {
    let index = node.lane.top_level_nodes.indexOf(node);
    if (index == 0) {
      // top of list
      return;
    }
    let node_above = node.lane.top_level_nodes[index - 1];
    node.lane.top_level_nodes.splice(index, 1);
    if (
      node.recursive_parent_ids.includes(node_above.id) &&
      node.recursive_parents.every((n) => n.expanded)
    ) {
      // move into parent
      node.lane = null;
      node.detached = false;
      let index = node.parent.children.indexOf(node);
      node.parent.children.splice(index, 1);
      node.parent.children.push(node);
    } else {
      // switch with node above
      node.lane.top_level_nodes.splice(index - 1, 0, node);
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
      let index = node.lane.top_level_nodes.indexOf(
        node.recursive_parents.at(-1)
      );
      if (index == -1) {
        console.error(
          "could not determine node's root parent index",
          node,
          node.recursive_parents.at(-1),
          node.lane.top_level_nodes
        );
        return;
      }
      lane.top_level_nodes.splice(index, 0, node);
      node.detached = true;
      node.lane = lane;
    }
  }

  dragged.value.blocked = true;
  nextTick(() => {
    nextTick(() => {
      move_up(node, y);
    });
  });
}
function move_down(node, y) {
  dragged.value.blocked = false;

  if (dragged.value.ref.getBoundingClientRect().bottom >= y) {
    // below mouse, stop movement
    return;
  }

  if (node.top_level) {
    let index = node.lane.top_level_nodes.indexOf(node);
    if (index + 1 == node.lane.top_level_nodes.length) {
      // bottom of list
      return;
    }
    let node_below = node.lane.top_level_nodes[index + 1];
    node.lane.top_level_nodes.splice(index, 1);
    if (
      node.recursive_parent_ids.includes(node_below.id) &&
      node.recursive_parents.every((n) => n.expanded)
    ) {
      // move into parent
      node.lane = null;
      node.detached = false;
      let index = node.parent.children.indexOf(node);
      node.parent.children.splice(index, 1);
      node.parent.children.splice(0, 0, node);
    } else {
      // switch with node below
      node.lane.top_level_nodes.splice(index + 1, 0, node);
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
      let index = lane.top_level_nodes.indexOf(node.recursive_parents.at(-1));
      if (index == -1) {
        console.error(
          "could not determine node's root parent index",
          node,
          node.recursive_parents.at(-1),
          node.lane.top_level_nodes
        );
        return;
      }
      lane.top_level_nodes.splice(index + 1, 0, node);
      node.detached = true;
      node.lane = lane;
    }
  }

  dragged.value.blocked = true;
  nextTick(() => {
    nextTick(() => {
      move_down(node, y);
    });
  });
}
function dragstart_card(node_ids, x, y) {
  dragged.value.x = x;
  dragged.value.y = y;
  dragged.value.nodes = node_ids.map((nid) => nodes.value[nid]);
  // Note: setting the dragged entry will set it to invisible and it will not be shown
  // during the drag operation. Delaying the invisibility by one frame will generate a
  // drag image and then hide the original card.
  window.requestAnimationFrame(function () {
    for (let node_id of node_ids) {
      kanban.value.nodes[node_id].dragged = true;
    }
  });
}
function drop(evt) {
  let drag_data_str = evt.dataTransfer.getData('application/json');
  if (drag_data_str == null) {
    // not a drag event for us
    return;
  }
  try {
    var drag_data = JSON.parse(drag_data_str);
  } catch (err) {
    console.warn('Failed to decode json from drag object:', drag_data_str);
    return;
  }
  if (drag_data['node_ids'] == null) {
    // not a drag event for us
    return;
  }
  let node_ids = drag_data['node_ids'];
  evt.stopPropagation();
  let nodes = node_ids.map((nid) => kanban.value.nodes[nid]);
  let lane = nodes[0].lane;
  let ordered_nodes = lane.nodes;
  emit('moved_cards', {
    lane: lane.id,
    cards: nodes.map((n) => {
      return {
        id: n.id,
        order: ordered_nodes.indexOf(n),
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
function dragging_ref(ref) {
  dragged.value.ref = ref;
}
</script>
