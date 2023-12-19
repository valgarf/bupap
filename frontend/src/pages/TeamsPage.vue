<template>
  <q-page class="col q-px-md q-pt-lg">
    <div class="row q-gutter-md items-center">
        <q-input v-model="search" outlined class="col-grow">
            <template v-slot:append>
                <q-icon name="search"/>
            </template>
        </q-input>
        <q-btn outline icon="add" tooltip="add team" class="text-black object-center m-auto"/>
    </div>
    <hr class="my-1 bg-grey-5 no-border" style="height:1px;"/>
    <div v-for="team in teams" :key="team.db_id">
        <div class="text-lg font-bold">
            {{team.name}}
        </div>
        <hr class="my-1 bg-grey-5 no-border" style="height:1px;"/>
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { Team } from 'components/models';

const search = ref<string>('Search not yet implemented');
const teams = ref<Team[]>([]);
console.log(search, teams);
</script>
