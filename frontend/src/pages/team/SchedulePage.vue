<template>
  <q-page class="column q-ma-md">
    <div class="row justify-between">
      <div>LEFT</div>
      <div>Schedule</div>
      <div>RIGHT</div>
    </div>
    <gantt-chart class="col-grow" />
  </q-page>
</template>
<style scoped lang="scss">
.q-page {
  height: calc(100vh - 148px) !important;
  min-height: 0px !important;
}
</style>
<script setup>
import GanttChart from 'src/components/GanttChart.vue';
</script>