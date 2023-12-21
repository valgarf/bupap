<template>
    <q-card class="card">
        <q-card-section class="row items-center">
            <div v-html="user.renderedAvatar" style="height:60px;width:60px;"/>
            <div class="column q-ml-md">
                <div class="text-body1 text-weight-bold">{{user.fullName}}</div>
                <div class="text-body2 text-blue-grey-5">@{{user.name}}</div>
            </div>
        </q-card-section>
    </q-card>
</template>

<style scoped lang="scss">
.card:hover {
    background-color: $blue-grey-1;
}
</style>

<script setup>
defineProps(['user'])
</script>