<template>
  <q-page class="column q-px-md q-pt-lg">
    <div class="row q-gutter-md items-center">
        <q-input v-model="search" outlined placeholder="Search not yet implemented" class="col-grow">
            <template v-slot:append>
                <q-icon name="search"/>
            </template>
        </q-input>
        <q-btn outline icon="add" tooltip="add team" class="text-black object-center m-auto"/>
    </div>
    <div v-if="!loading && result!=null">
        <q-list separator class="q-mt-sm">
            <q-separator/>
            <q-item clickable v-for="team in result.teams" :key="team.dbId" @click="open(team)">
                <q-item-section class="text-subtitle1 text-weight-bold q-pa-md">
                    {{team.name}}
                </q-item-section>
            </q-item>
            <q-separator/>
        </q-list>
    </div>
    <query-status :loading="loading" :error="error"/>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'
import { useRouter } from 'vue-router';
import QueryStatus from 'components/QueryStatus.vue'
const search = ref<string>('');
const { result, loading, error } = useQuery(gql`
    query getTeams {
        teams {
            name
            dbId
        }
    }
`);

const router=useRouter()
function open(team) {
    router.push(`/team/${team.dbId}/`)
}


</script>
