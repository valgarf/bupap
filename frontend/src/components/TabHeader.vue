<template>
  <div>
    <q-tabs>
      <q-route-tab
        v-for="route in routes"
        :label="route.label"
        :to="route.to"
        :key="route.to"
      />
    </q-tabs>
    <router-view v-slot="{ Component }" class="full-height">
      <Transition
        :name="route.meta.transition || 'fade'"
        :mode="route.meta.mode"
      >
        <component :is="Component" :key="route.path" />
      </Transition>
    </router-view>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.slide-left-enter-active,
.slide-right-enter-active {
  transition: transform 0.2s ease-out;
}

.slide-left-leave-active,
.slide-right-leave-active {
  transition: transform 0.2s ease-in;
}
.slide-left-enter-from,
.slide-right-leave-to {
  transform: translate(100%, 0);
}
.slide-right-enter-from,
.slide-left-leave-to {
  transform: translate(-100%, 0);
}
</style>

<script setup lang="ts">
import { useRouter, useRoute } from 'vue-router';
import { computed } from 'vue';

const props = defineProps(['depth', 'routes']);
const route = useRoute();
const router = useRouter();
const order = computed(() => props.routes.map((r) => r.to));

function extract_path(p: string) {
  return p.split('/')[props.depth];
}

router.afterEach((to, from) => {
  const idx_from = order.value.indexOf(extract_path(from.path));
  const idx_to = order.value.indexOf(extract_path(to.path));
  if (idx_from == idx_to || idx_from == -1 || idx_to == -1) {
    to.meta.transition = 'fade';
    to.meta.mode = 'out-in';
  } else if (idx_from < idx_to) {
    to.meta.transition = 'slide-left';
    to.meta.mode = 'out-in';
  } else {
    to.meta.transition = 'slide-right';
    to.meta.mode = 'out-in';
  }
});
</script>
