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
            <q-item clickable v-for="team in result.teams" :key="team.dbId">
                <q-item-section class="text-subtitle1 text-weight-bold q-pa-md">
                    {{team.name}}
                </q-item-section>
            </q-item>
            <q-separator/>
        </q-list>
<!--             
        <hr class="bg-grey-5 q-mx-none q-mb-none q-mt-sm no-border" style="height:1px;"/>
        <div v-for="team in result.teams" :key="team.dbId">
            <div class="text-subtitle1 text-weight-bold q-pa-md q-hoverable">
                {{team.name}}
            </div>
            <hr class="bg-grey-5 q-ma-none no-border" style="height:1px;"/>
        </div> -->
    </div>
    <div v-if="loading" class="self-center col-grow column justify-center">
        <q-spinner v-if="loading"
            color="primary"
            size="3em"
            class="vertical-middle"
        />
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'

const search = ref<string>('');
const { result, loading } = useQuery(gql`
    query getTeams {
        teams {
            name
            dbId
        }
    }
`);

</script>
