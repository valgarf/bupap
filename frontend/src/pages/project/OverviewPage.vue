<template>
  <q-page class="column q-px-md q-pt-lg" :style-fn="qPageStyleFnForTabs">
    <q-breadcrumbs
      v-if="parents != null && parents.length > 0"
      class="self-center q-mb-md"
    >
      <q-breadcrumbs-el
        v-for="proj in parents"
        :key="proj.dbId"
        :label="proj.name"
        class="select-none cursor-pointer"
        @click="openProject(proj.dbId)"
      />
      <q-breadcrumbs-el :label="result?.project?.name" />
    </q-breadcrumbs>
    <div v-if="result" class="self-center text-h5 q-mb-lg text-weight-bold">
      {{ result?.project?.name }}
    </div>
    <div class="row q-gutter-md items-center">
      <q-input
        v-model="search"
        outlined
        placeholder="Search not yet implemented"
        class="col-grow"
      >
        <template v-slot:append>
          <q-icon name="search" />
        </template>
      </q-input>
      <q-btn
        outline
        icon="add"
        tooltip="add team"
        class="text-black object-center m-auto"
      />
    </div>
    <div v-if="!loading && projects != null">
      <q-tree
        :nodes="projects"
        node-key="dbId"
        no-connectors
        v-model:selected="selected"
        @update:selected="openProject"
        class="tree-base q-mt-md"
      >
        <template v-slot:default-header="prop">
          <div class="text-subtitle1 text-weight-bold q-py-md">
            {{ prop.node.label }}
          </div>
        </template>
      </q-tree>
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>

<style scoped>
:deep(.q-tree__node-header) {
  padding-top: 0px;
  padding-bottom: 0px;
  margin-top: 0px;
}
</style>

<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute, useRouter } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { computed, ref, watchEffect } from 'vue';
import { listToTree } from 'src/common/tree';
import { qPageStyleFnForTabs } from 'src/common/helper';

const route = useRoute();
const router = useRouter();

const selected = ref(null);
const search = ref('');

const { result, loading, error } = useQuery(
  gql`
    query getProject($dbId: Int!) {
      project: dbNode(typename: "Project", dbId: $dbId) {
        ... on Project {
          name
          children(recursive: true) {
            dbId
            name
            parent {
              dbId
            }
          }
          parents {
            dbId
            name
          }
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id),
  }
);

const projects = computed(() => {
  if (result == null) {
    return null;
  }
  const transformed = result.value.project.children.map((p) => {
    return { dbId: p.dbId, label: p.name, parent: p.parent };
  });
  const tree = listToTree(transformed);
  return tree;
});

const parents = computed(() => {
  return result.value?.project?.parents?.toReversed();
});

function openProject(proj) {
  router.push(`/project/${proj}/`);
  selected.value = null;
}
</script>