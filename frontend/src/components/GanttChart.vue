<template>
  <div class="gantt-grid">
    <div class="g-1-1">
      <div class="text-subtitle1 text-weight-bold">{{ title }}</div>
      <!-- <div class="text-sm">{{dt_start}}</div> -->
    </div>
    <!-- <div class="g-2-1"> -->
    <q-scroll-area
      class="g-2-1"
      ref="qscroll21"
      @scroll="onscroll"
      delay="0"
      :visible="false"
    >
      <svg
        ref="gantt-timeline"
        version="1.1"
        :width="calc_image_width()"
        height="70"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g v-for="mark in get_hour_marks()" :key="mark">
          <!-- <line :x1="calc_dt_to_x(mark)" :x2="calc_dt_to_x(mark)" :y1="geom.timeline_height-30" :y2="geom.timeline_height" stroke="black"/> -->
          <text
            :x="calc_dt_to_x(mark)"
            :y="geom.timeline_height - 50"
            class="text-body1"
            text-anchor="middle"
          >
            {{ format_hour_mark(mark) }}
          </text>
        </g>
      </svg>
    </q-scroll-area>
    <!-- </div> -->
    <q-scroll-area
      class="g-1-2"
      ref="qscroll12"
      @scroll="onscroll"
      delay="0"
      :visible="false"
    >
      <svg
        ref="gantt-names"
        version="1.1"
        width="250"
        :height="calc_image_height()"
        xmlns="http://www.w3.org/2000/svg"
      >
        <g v-for="row in rows" :key="row.key">
          <text x="10" :y="calc_row_center(row.idx) + 8" class="text-subtitle1">
            {{ row.name }}
          </text>
        </g>
        <line
          x1="0"
          :y1="calc_row_top(0)"
          x2="100%"
          :y2="calc_row_top(0)"
          stroke="black"
        />
        <g v-for="row in rows" :key="row.key">
          <line
            x1="0"
            :y1="calc_row_bottom(row.idx)"
            x2="100%"
            :y2="calc_row_bottom(row.idx)"
            stroke="black"
          />
        </g>
        <line
          x1="100%"
          :y1="geom.pad_top"
          x2="100%"
          :y2="geom.row_height * rows.length + geom.pad_top"
          stroke="black"
        />
      </svg>
    </q-scroll-area>
    <!-- <div class="g-2-2"> -->
    <q-scroll-area class="g-2-2" ref="qscroll22" @scroll="onscroll">
      <svg
        ref="gantt"
        version="1.1"
        :width="calc_image_width()"
        :height="calc_image_height()"
        xmlns="http://www.w3.org/2000/svg"
      >
        <rect
          x="0"
          :y="geom.pad_top"
          width="100%"
          :height="geom.row_height * rows.length"
          :fill="colors.default_bg"
        />
        <g v-for="row in rows" :key="row.key">
          <g v-for="bg in row.bg" :key="bg.key">
            <rect
              :x="calc_bar_start(bg)"
              :y="calc_row_top(row.idx)"
              :width="calc_bar_length(bg)"
              :height="geom.row_height"
              :fill="bg.color"
            />
          </g>
        </g>
        <g v-for="mark in get_hour_marks()" :key="mark">
          <line
            :x1="calc_dt_to_x(mark)"
            :x2="calc_dt_to_x(mark)"
            :y1="0"
            :y2="calc_image_height() - geom.pad_bottom"
            stroke="black"
          />
        </g>
        <g v-if="dt_now > dt_start && dt_now < dt_end">
          <line
            :x1="calc_dt_to_x(dt_now)"
            :x2="calc_dt_to_x(dt_now)"
            :y1="calc_row_top(0) - 5"
            :y2="calc_image_height() - geom.pad_bottom + 5"
            stroke="grey"
            stroke-width="5"
            stroke-linecap="round"
          />
        </g>
        <g v-if="dragged.entry != null">
          <rect
            x="0"
            :y="calc_row_top(dragged_row)"
            width="100%"
            :height="geom.row_height"
            :fill="colors.highlight"
            style="opacity: 0.5"
          />
        </g>
        <g v-for="row in rows" :key="row.key">
          <g v-for="bar in row.bar" :key="bar.key">
            <!-- style="cursor: grab" @mousedown.left="drag(bar)" -->
            <rect
              :x="calc_bar_start(bar)"
              :y="calc_bar_top(row.idx)"
              :width="calc_bar_length(bar)"
              :height="calc_bar_height()"
              :rx="geom.bar_round"
              :fill="bar.color"
              stroke="#505050"
            />
            <svg
              :x="calc_bar_start(bar) + (geom.bar_round * 2) / 3"
              :y="calc_bar_top(row.idx)"
              :width="calc_bar_length(bar) - (geom.bar_round * 4) / 3"
              :height="calc_bar_height()"
            >
              <text
                :y="geom.row_height / 2"
                class="text-body2"
                :fill="bar.text_color"
                text-anchor="left"
              >
                {{ bar.text }}
              </text>
            </svg>
            <foreignObject
              :x="calc_bar_start(bar)"
              :y="calc_bar_top(row.idx)"
              :width="calc_bar_length(bar)"
              :height="calc_bar_height()"
            >
              <q-tooltip anchor="top middle" self="center middle">
                {{ bar.text }}<br /> {{ format_dt(bar.start) }} -
                {{ format_dt(bar.end) }}
              </q-tooltip>
              <q-menu touch-position context-menu>
                <q-list style="min-width: 100px">
                  <q-item clickable v-close-popup @click="open_item(bar.key)">
                    <q-item-section>Details</q-item-section>
                  </q-item>
                </q-list>
              </q-menu>
            </foreignObject>
          </g>
          <g v-for="fg in row.fg" :key="fg.key">
            <rect
              :x="calc_bar_start(fg)"
              :y="calc_row_top(row.idx)"
              :width="calc_bar_length(fg)"
              :height="geom.row_height"
              :fill="fg.color"
            />
          </g>
        </g>
        <line
          x1="0"
          :y1="calc_row_top(0)"
          x2="100%"
          :y2="calc_row_top(0)"
          stroke="black"
        />
        <g v-for="row in rows" :key="row.key">
          <line
            x1="0"
            :y1="calc_row_bottom(row.idx)"
            x2="100%"
            :y2="calc_row_bottom(row.idx)"
            stroke="black"
          />
        </g>
        <g
          v-if="dragged.entry != null"
          @mouseup.left="drop"
          style="cursor: grabbing; opacity: 0.5"
        >
          <rect
            :x="dragged_x"
            :y="dragged_y"
            :rx="geom.bar_round"
            :width="calc_bar_length(dragged.entry)"
            :height="calc_bar_height()"
            :fill="dragged.entry.color"
          />
          <text
            :x="dragged_x + (geom.bar_round * 2) / 3"
            :y="dragged_y + geom.row_height / 2"
            class="text-body2"
            :fill="dragged.entry.text_color"
            text-anchor="left"
          >
            {{ dragged.entry.text }}
          </text>
        </g>
      </svg>
    </q-scroll-area>
    <!-- </div> -->
  </div>
</template>

<style scoped>
.gantt-grid {
  display: grid;
  grid-template-columns: 250px auto;
  grid-template-rows: 70px auto;
  gap: 0;
  width: 100%;
}
.g-1-1 {
  grid-column: 1;
  grid-row: 1;
  text-align: center;
  line-height: 70px;
}
.g-2-1 {
  grid-column: 2;
  grid-row: 1;
}
.g-1-2 {
  grid-column: 1;
  grid-row: 2;
}
.g-2-2 {
  grid-column: 2;
  grid-row: 2;
}
</style>

<script setup>
import { computed, onMounted, ref } from 'vue';

const gantt = ref(null);
// const qscroll11 = ref(null);
const qscroll12 = ref(null);
const qscroll21 = ref(null);
const qscroll22 = ref(null);

const title = 'Test';
const start = new Date();
const dt_start = start;
const dt_end = new Date(start.getTime() + 1000 * 3600 * 24);
console.log(dt_start, dt_end);
console.log(dt_end - dt_start);
const dt_now = start;
const rows = [
  {
    idx: 0,
    name: 'sr',
    key: 'sr',
    bg: [],
    fg: [],
    bar: [
      {
        key: 'sr1',
        start: start,
        end: new Date(start.getTime() + 1000 * 2 * 3600),
        color: '#2de1c2',
      },
      { key: 'sr2', start: 160 / 5000, end: 250 / 5000, color: '#f25757' },
    ],
  },
  {
    idx: 1,
    name: 'te',
    key: 'te',
    bg: [],
    fg: [],
    bar: [
      {
        key: 'te1',
        start: new Date(start.getTime() + 1000 * 0.5 * 3600),
        end: new Date(start.getTime() + 1000 * 1.5 * 3600),
        color: '#63474d',
      },
      { key: 'te2', start: 160 / 5000, end: 250 / 5000, color: '#d4b2d8' },
    ],
  },
  {
    idx: 2,
    name: 'jbw',
    key: 'jbw',
    bg: [],
    fg: [],
    bar: [
      {
        key: 'jbw1',
        start: new Date(start.getTime() - 1000 * 1 * 3600),
        end: new Date(start.getTime() + 1000 * 2 * 3600),
        color: '#63474d',
      },
      { key: 'jbw1', start: 160 / 5000, end: 250 / 5000, color: '#d4b2d8' },
    ],
  },
];
const dragged = { x: 0, y: 0, entry: null };
const geom = {
  pad_top: 32,
  pad_bottom: 12,
  width_per_second: 5000 / 24 / 3600,
  row_height: 50,
  bar_inset: 5,
  timeline_height: 100,
  bar_round: 5,
};
const colors = {
  highlight: 'lightblue',
  default_bg: '#dedede',
};
var _ignore_scroll = [];

const dragged_x = computed(() => {
  if (dragged.entry == null) {
    return 0;
  }
  return dragged.x - calc_bar_length(dragged.entry) / 2;
});
const dragged_y = computed(() => {
  if (dragged.entry == null) {
    return 0;
  }
  return dragged.y - 20;
});

const dragged_row = computed(() => {
  return Math.floor((dragged.y - geom.bar_inset) / geom.row_height);
});
function handle_click() {
  value += 1;
  $emit('change', value);
}
function set_new_data(data) {
  for (var row of data.row_data) {
    for (var el of row.bg) {
      el['start'] = new Date(el['start']);
      el['end'] = new Date(el['end']);
    }
    for (el of row.fg) {
      el['start'] = new Date(el['start']);
      el['end'] = new Date(el['end']);
    }
    for (el of row.bar) {
      el['start'] = new Date(el['start']);
      el['end'] = new Date(el['end']);
    }
  }
  rows = data.row_data;
  dt_start = new Date(data.start);
  dt_end = new Date(data.end);
  dt_now = new Date(data.now);
}
function get_hour_marks() {
  var marks = [];
  var c = new Date(dt_start);
  c.setHours(c.getHours() + 1);
  c.setMinutes(0, 0, 0);
  while (c < dt_end) {
    marks.push(new Date(c));
    c.setHours(c.getHours() + 1);
  }
  return marks;
}
function _padZero(num) {
  var result = num.toString();
  if (result.length < 2) {
    result = '0' + result;
  }
  return result;
}
function format_hour_mark(dt) {
  return _padZero(dt.getHours()) + ':' + _padZero(dt.getMinutes());
}
function format_dt(dt) {
  return format_hour_mark(dt);
}
function calc_dt_to_x(dt) {
  return ((dt - dt_start) / 1000) * geom.width_per_second;
}
function calc_image_width() {
  return calc_dt_to_x(dt_end);
}
function calc_bar_top(idx) {
  return calc_row_top(idx) + geom.bar_inset;
}
function calc_row_top(idx) {
  return idx * geom.row_height + geom.pad_top;
}
function calc_row_center(idx) {
  return (idx + 0.5) * geom.row_height + geom.pad_top;
}
function calc_row_bottom(idx) {
  return (idx + 1) * geom.row_height + geom.pad_top;
}
function calc_bar_start(entry) {
  return calc_dt_to_x(entry.start);
}
function calc_bar_length(entry) {
  return ((entry.end - entry.start) / 1000) * geom.width_per_second;
}
function calc_image_height() {
  return geom.row_height * rows.length + geom.pad_top + geom.pad_bottom;
}
function calc_bar_height() {
  return geom.row_height - 2 * geom.bar_inset;
}
function drag(entry) {
  dragged.entry = entry;
}
function drop() {
  dragged.entry = null;
}
function move(event) {
  dragged.x = event.offsetX;
  dragged.y = event.offsetY;
}
function open_item(key) {
  $emit('open_item', key);
}
function onscroll(evt) {
  // console.log(evt)
  if (_ignore_scroll.indexOf(evt.ref) != -1) {
    _ignore_scroll = _ignore_scroll.filter((item) => item !== evt.ref);
    // console.log("scroll event ignored")
    return;
  }
  var h = null;
  var v = null;
  if (evt.ref === qscroll22.value || evt.ref === qscroll12.value) {
    v = evt.verticalPosition;
  }
  if (evt.ref === qscroll22.value || evt.ref === qscroll21.value) {
    h = evt.horizontalPosition;
  }
  // console.log("scroll event", h, v)
  if (v !== null) {
    if (
      qscroll12.value.getScrollPosition().top != v &&
      evt.ref != qscroll12.value
    ) {
      _ignore_scroll.push(qscroll12.value);
      qscroll12.value.setScrollPosition('vertical', v);
      // console.log("scroll 12 v to ", v)
    }
    if (
      qscroll22.value.getScrollPosition().top != v &&
      evt.ref != qscroll22.value
    ) {
      _ignore_scroll.push(qscroll22.value);
      qscroll22.value.setScrollPosition('vertical', v);
      // console.log("scroll 22 v to ", v)
    }
  }
  if (h !== null) {
    if (
      qscroll21.value.getScrollPosition().left != h &&
      evt.ref != qscroll21.value
    ) {
      _ignore_scroll.push(qscroll21.value);
      qscroll21.value.setScrollPosition('horizontal', h);
      // console.log("scroll 21 h to ", h)
    }
    if (
      qscroll22.value.getScrollPosition().left != h &&
      evt.ref != qscroll22.value
    ) {
      _ignore_scroll.push(qscroll22.value);
      qscroll22.value.setScrollPosition('horizontal', h);
      // console.log("scroll 22 h to ", h)
    }
  }
}

onMounted(() => {
  gantt.value.addEventListener('mousemove', move);
});
</script>