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
          node-key="dbId"
          no-connectors
          v-model:selected="selected"
          @update:selected="openProject"
          class="tree-base q-mt-md"
        >
            <template v-slot:default-header="prop">
                <div class = "text-subtitle1 text-weight-bold q-py-md">
                    {{prop.node.label}}
                </div>
            </template>
        </q-tree>
    </div>
    <query-status :loading="loading" :error="error"/>
  </q-page>
</template>

<style scoped>
.line {
    height: 1px;
    border: 0px;
    margin: 0px;
    padding: 0px;
    background-color: red;
}
:deep(.q-tree__node-header) {
    padding-top: 0px;
    padding-bottom: 0px;
    margin-top: 0px;
}
</style>


<script setup lang="ts">
import { computed, ref } from 'vue';
import { useQuery } from '@vue/apollo-composable'
import { gql } from '@apollo/client/core'
import { listToTree } from 'src/common/tree'
import QueryStatus from 'components/QueryStatus.vue'

const selected = ref(null)
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

function openProject(proj) {
    selected.value = null
    console.log('Opening project',proj);
}

</script>
