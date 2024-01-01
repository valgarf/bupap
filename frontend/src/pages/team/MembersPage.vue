<template>
  <q-page class="column q-px-md q-pt-lg" :style-fn="qPageStyleFnForTabs">
    <div v-for="role in groups" :key="'role-' + role.dbId">
      <div class="q-py-lg text-h5 text-weight-bold">{{ role.name }}</div>
      <div class="row q-gutter-x-lg">
        <user-card
          v-for="user in role.users"
          :key="'user-' + user.dbId"
          :user="user"
        />
      </div>
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template> 
<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { computed } from 'vue';
import { groupBy } from 'src/common/helper';
import UserCard from 'src/components/UserCard.vue';
import { qPageStyleFnForTabs } from 'src/common/helper';
const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getTeam($dbId: Int!) {
      team: dbNode(typename: "Team", dbId: $dbId) {
        ... on Team {
          name
          dbId
          assignedRoles {
            role {
              dbId
              name
            }
            user {
              dbId
              name
              fullName
              renderedAvatar
            }
          }
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id),
  }
);

const groups = computed(() => {
  if (result.value?.team == null) {
    return [];
  }
  const grouped = groupBy(result.value.team.assignedRoles, (r) => {
    return r?.role?.dbId;
  });
  return Object.values(grouped).map((roles) => {
    return {
      name: roles[0].role.name,
      dbId: roles[0].role.dbId,
      users: roles.map((r) => {
        return r.user;
      }),
    };
  });
});
</script>