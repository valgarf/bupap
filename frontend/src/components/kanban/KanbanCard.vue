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
      @click="openLink(card)"
      class="q-ma-none q-px-sm q-py-none q-mb-md"
    >
      <div
        class="row items-center no-wrap text-subtitle1 text-weight-bold select-none"
      >
        <div class="text-center">
          {{ card.title }}
        </div>
        <q-icon right name="launch" color="blue-grey-4" size="1em" />
      </div>
    </q-btn>
    <div
      v-if="progress != null && progress[2] > 0"
      class="row items-center full-width q-gutter-xs q-pl-sm"
    >
      <span class="dot" :class="{ invisible: !active }" style=""></span>
      <svg
        v-if="progress != null"
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
      <div>~{{ progress[1] }}% ({{ progress[0] }}% - {{ progress[2] }}%)</div>
    </div>
    <div v-if="finishedAt != null" class="q-pl-sm">
      Finished: {{ finishedAt }}
    </div>
    <div v-if="!detached" class="row q-pl-sm q-mt-sm">
      <q-badge
        v-for="tag in tags"
        :key="card.id + tag.text + tag.color"
        :color="tag.color"
        :text-color="textColorFromBackground(tag.color)"
        class="q-pa-xs select-none"
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
  key: string;
  text: string;
  color: string;
}

export interface Progress {
    0: number;
    1: number;
    2: number;
}


export interface Card {
  id: string;
  title: string;
  progress: Progress | null;
  active: boolean;
  finishedAt: string | null;
  tags: Tag[];
  priority: string;
  // Other possible properties of Card go here.
}

export interface CardProps {
  card: Card;
  detached: boolean;
  dragged: boolean;
  priorities: Tag[];
}

// export interface KanbanCardData {}
</script>

<script setup lang="ts">
import {
  computed,
  defineProps,
  defineEmits,
  ref,
  onMounted,
  onUpdated,
} from 'vue';
import { textColorFromBackground } from 'src/common/helper';
const props = withDefaults(defineProps<CardProps>(), { priorities: () => [], dragged: false, detached: false })

const cardElement = ref(null);
const progressSvg = ref(null);
const emit = defineEmits(['draggingRef', 'openLink']);

onMounted(() => {
  checkDragged();
});
onUpdated(() => {
  checkDragged();
});

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
const finishedAt = computed(() => props.card.finishedAt);
const tags = computed(() => {
  var tags = [...props.card.tags];
  if (props.priorities != null) {
    for (var p of props.priorities) {
      if (props.card.priority == p.key) {
        tags.splice(0, 0, p);
      }
    }
  }
  return tags;
});

function checkDragged() {
  if (props.dragged) {
    if (cardElement.value != null) {
      let refEl = cardElement.value._.subTree.el;
      emit('draggingRef', refEl);
    }
  }
}
function openLink(val: Card) {
  emit('openLink', val);
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
    var result = ['hoverable', 'cursor-pointer', 'q-pa-md'];
  }
  return result;
}
</script>