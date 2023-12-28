<template>
  <q-page class="column q-px-md q-pt-lg">
    <div v-if="result" class="self-center text-h4 text-weight-bold">
      {{ result?.dbNode?.name }}
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>
<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getProject($dbId: Int!) {
      dbNode(typename: "Project", dbId: $dbId) {
        ... on Project {
          name
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id),
  }
);
</script>