<template>
  <q-card
    ref="card"
    class="nicegui-card"
    flat="this.detached"
    :bordered="this.detached"
    :class="classes()"
  >
    <q-btn flat no-caps @click="open_link(card)" class="m-0 px-1 py-0 p-0">
      <div class="row items-center no-wrap text-base font-bold select-none">
        <div class="text-center">
          {{ card.title }}
        </div>
        <q-icon right name="launch" color="neutral-400" size="1em" />
      </div>
    </q-btn>
    <div
      v-if="this.progress != null"
      class="nicegui-row items-center w-full gap-1 pl-1"
    >
      <span
        class="h-2 w-2 rounded-full"
        :class="{ invisible: !this.active }"
        style="display: inline-block; background-color: #67ffae"
      ></span>
      <svg
        v-if="this.progress != null"
        ref="progress"
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
    <div v-if="!this.detached" class="nicegui-row">
      <q-badge
        v-for="tag in this.tags"
        :key="card.id + tag.text + tag.color"
        :color="tag.color"
        :text-color="tag.text_color"
        class="p-1 m-1 select-none"
        >{{ tag.text }}</q-badge
      >
    </div>
  </q-card>
</template>


<script>
export default {
  data() {
    return {
      card: this.card,
      detached: this.detached,
      dragged: this.dragged,
      priorities: this.priorities,
    };
  },
  mounted() {
    this.check_dragged();
  },
  updated() {
    this.check_dragged();
  },
  computed: {
    progress() {
      if (this.card.progress == null) {
        return null;
      }
      return [
        Math.round(this.card.progress[0]),
        Math.round(this.card.progress[1]),
        Math.round(this.card.progress[2]),
      ];
    },
    active() {
      return this.card.active;
    },
    finished_at() {
      return this.card.finished_at;
      // return luxon.DateTime(this.card.finished_at).toFormat("yyyy-LL-dd HH:mm")
    },
    tags() {
      var tags = [...this.card.tags];
      if (this.priorities != null) {
        for (var p of this.priorities) {
          if (this.card.priority == p.text) {
            tags.splice(0, 0, p);
          }
        }
      }
      return tags;
    },
  },
  methods: {
    check_dragged() {
      if (this.dragged) {
        let ref = this.$refs["card"];
        if (ref != null) {
          ref = ref._.subTree.el;
          this.$emit("dragging_ref", ref);
        }
      }
    },
    open_link(val) {
      this.$emit("open_link", val);
    },
    classes() {
      if (this.detached) {
        var result = [
          "text-gray-400",
          "bg-gray-100",
          "border-dashed",
          "pt-2",
          "pb-2",
          "mt-0.5",
        ];
      } else {
        var result = ["hover:bg-slate-200", "cursor-pointer"];
      }
      return result;
    },
  },
  props: {
    card: null,
    detached: false,
    dragged: false,
    priorities: null,
  },
};
</script>