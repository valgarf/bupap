<template>
    <div v-if="loading" class="self-center col-grow column justify-center">
        <q-spinner v-if="loading"
            color="primary"
            size="3em"
            class="vertical-middle"
        />
    </div>
    <div v-else-if="error" class="text-subtitle1 text-weight-bold q-pa-md bg-negative text-white">
        Failed to load data.
    </div>
</template>

<script setup>
defineProps(['loading', 'error'])
</script>