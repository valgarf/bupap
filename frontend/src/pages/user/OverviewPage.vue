<template>
  <q-page class="column q-px-md q-pt-lg items-center justify-start">
    <div
      v-if="result?.user != null"
      v-html="result.user.renderedAvatar"
      class="avatar q-mb-md"
    />
    <div v-if="result" class="self-center text-h6 text-weight-bold">
      {{ result?.user?.fullName }}
    </div>
    <div v-if="result" class="self-center text-body2 text-blue-grey-5">
      @{{ result?.user?.name }}
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>
<style scoped>
.avatar {
  height: 160px;
  width: 160px;
}
</style>
<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getUser($dbId: Int!) {
      user: dbNode(typename: "User", dbId: $dbId) {
        ... on User {
          name
          fullName
          renderedAvatar
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id),
  }
);
</script>