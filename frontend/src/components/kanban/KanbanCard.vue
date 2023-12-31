<template>
  <q-card
    ref="cardElement"
    :flat="detached"
    :bordered="detached"
    :class="classes()"
  >
    <q-btn
      flat
      no-caps
      @click="open_link(card)"
      class="q-ma-none q-px-sm q-py-none"
    >
      <div
        class="row items-center no-wrap text-subtitle2 text-weight-bold select-none"
      >
        <div class="text-center">
          {{ card.title }}
        </div>
        <q-icon right name="launch" color="blue-grey-4" size="1em" />
      </div>
    </q-btn>
    <div
      v-if="this.progress != null"
      class="row items-center full-width q-gutter-xs q-pl-sm"
    >
      <span class="dot" :class="{ invisible: !this.active }" style=""></span>
      <svg
        v-if="this.progress != null"
        ref="progressSvg"
        version="1.1"
        width="50%"
        height="4"
        viewBox="0 0 100 10"
        preserveAspectRatio="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <defs>
          <linearGradient id="Gradient1">
            <stop stop-color="#67FFAE" offset="0%" />
            <stop stop-color="#67A9FF" offset="100%" />
          </linearGradient>
          <linearGradient id="Gradient2">
            <stop stop-color="#67A9FF" offset="0%" />
            <stop stop-color="grey" offset="100%" />
          </linearGradient>
        </defs>
        <rect x="0" y="0" width="100" height="10" fill="grey" />
        <rect x="0" y="0" :width="progress[0]" height="10" fill="#67FFAE" />
        <rect
          :x="progress[0]"
          y="0"
          :width="progress[1] - progress[0]"
          height="10"
          style="fill: url(#Gradient1); stroke-width: 0"
        />
        <rect
          :x="progress[1]"
          y="0"
          :width="progress[2] - progress[1]"
          height="10"
          style="fill: url(#Gradient2); stroke-width: 0"
        />
        <!-- <rect :x="progress[1]-1" y="0" :width="2" height="10" style="fill:yellow;stroke-width:0;"/> -->
      </svg>
      <div>
        ~{{ this.progress[1] }}% ({{ this.progress[0] }}% -
        {{ this.progress[2] }}%)
      </div>
    </div>
    <div v-if="this.finished_at != null">
      {{ this.finished_at }}
    </div>
    <div v-if="!this.detached" class="row">
      <q-badge
        v-for="tag in this.tags"
        :key="card.id + tag.text + tag.color"
        :color="tag.color"
        :text-color="textColorFromBackground(tag.color)"
        class="q-pa-xs q-ma-xs select-none"
        >{{ tag.text }}</q-badge
      >
    </div>
  </q-card>
</template>

<style lang="scss" scoped>
.hoverable:hover {
  background-color: $blue-grey-3;
}
.dot {
  height: 6px;
  width: 6px;
  border-radius: 9999px;
  display: inline-block;
  background-color: #67ffae;
}
</style>

<script lang='ts'>
export interface Tag {
  text: string;
  color: string;
}

// export interface KanbanCardData {}
</script>

<script setup lang="ts">
import { computed, defineProps, defineEmits, ref } from 'vue';
import { textColorFromBackground } from 'src/common/helper';
const props = defineProps({
  card: { type: Object as () => Tag },
  detached: Boolean,
  dragged: Boolean,
  priorities: { type: Array<Tag>, default: [] },
});
const cardElement = ref(null);
const progressSvg = ref(null);
const emit = defineEmits(['dragging_ref', 'open_link']);

function mounted() {
  check_dragged();
}
function updated() {
  check_dragged();
}

const progress = computed(() => {
  if (props.card.progress == null) {
    return null;
  }
  return [
    Math.round(props.card.progress[0]),
    Math.round(props.card.progress[1]),
    Math.round(props.card.progress[2]),
  ];
});

const active = computed(() => props.card.active);
const finished_at = computed(() => props.card.finished_at);
const tags = computed(() => {
  var tags = [...props.card.tags];
  if (props.priorities != null) {
    for (var p of props.priorities) {
      if (props.card.priority == p.text) {
        tags.splice(0, 0, p);
      }
    }
  }
  return tags;
});

function check_dragged() {
  if (props.dragged) {
    if (cardElement.value != null) {
      let refEl = cardElement.value._.subTree.el;
      emit('dragging_ref', refEl);
    }
  }
}
function open_link(val) {
  emit('open_link', val);
}
function classes() {
  if (props.detached) {
    var result = [
      'text-grey-4',
      'bg-grey-2',
      'border-dashed',
      'q-py-sm',
      'q-mt-xs',
    ];
  } else {
    var result = ['hoverable', 'cursor-pointer'];
  }
  return result;
}
</script>