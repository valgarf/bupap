<template>
  <tab-header
    depth="3"
    :routes="[
      { label: 'Overview', to: 'overview' },
      { label: 'Board', to: 'board' },
    ]"
  />
</template>

<script setup lang="ts">
import TabHeader from 'src/components/TabHeader.vue';
</script>
