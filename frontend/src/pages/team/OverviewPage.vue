<template>
  <q-page class="column" :style-fn="qPageStyleFnForTabs">
    <div v-if="result" class="self-center text-h4 text-weight-bold q-pt-lg">
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
import { qPageStyleFnForTabs } from 'src/common/helper';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getTeam($dbId: Int!) {
      dbNode(typename: "Team", dbId: $dbId) {
        ... on Team {
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