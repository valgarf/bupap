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
    <div v-if="!loading && projects!=null">
        <q-tree
        :nodes="projects"
        node-key="label"
        />
        <!-- <q-list separator class="q-mt-sm">
            <q-separator/>
            <q-item clickable v-for="user in result.users" :key="user.dbId">
                <q-item-section>
                    <div class="row items-center">
                        <div v-html="user.renderedAvatar" style="height:80px;width:80px;" class="q-pa-sm"/>
                        <div class="column">
                            <div class="text-subtitle1 text-weight-bold">{{user.fullName}}</div>
                            <div class="text-body2 text-blue-grey-5">@{{user.name}}</div>
                        </div>
                    </div>
                </q-item-section>
            </q-item>
            <q-separator/>
        </q-list> -->
    </div>
    <div v-if="loading" class="self-center col-grow column justify-center">
        <q-spinner v-if="loading"
            color="primary"
            size="3em"
            class="vertical-middle"
        />
    </div>
    <div v-if="error" class="text-subtitle1 text-weight-bold q-pa-md bg-negative text-white">
        Failed to load data.
    </div>
  </q-page>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue';
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'
import { listToTree } from 'src/common/tree'


const search = ref<string>('');
const { result, loading, error } = useQuery(gql`
    query getProjects {
        projects {
            dbId
            name
            parent {dbId}
        }
    }
`);

const projects = computed(()=> {
    if (result == null) {
        return null;
    }
    const transformed = result.value.projects.map((p) => {return {dbId: p.dbId, label: p.name, parent: p.parent}})
    const tree = listToTree(transformed);
    console.log(transformed, tree);
    return tree
})



</script>
