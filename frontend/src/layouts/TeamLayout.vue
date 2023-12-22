<template>
  <div>
    <q-tabs>
      <q-route-tab label="Overview" to="overview" />
      <q-route-tab label="Members" to="members" />
      <q-route-tab label="Schedule" to="schedule" />
    </q-tabs>
    <router-view v-slot="{ Component }" class="full-height">
      <Transition :name="route.meta.transition || fade" :mode="route.meta.mode">
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
import { useRoute, useRouter } from 'vue-router';

const route = useRoute();
const router = useRouter();
router.afterEach((to, from) => {
  const order = ['overview', 'members', 'schedule'];

  function extract_path(p: string) {
    return from.path.split('/')[3];
  }
  const idx_from = order.indexOf(extract_path(from.path));
  const idx_to = order.indexOf(extract_path(to.path));
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
