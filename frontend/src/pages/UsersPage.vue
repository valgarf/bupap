<template>
  <q-page class="column q-px-md q-pt-lg">
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
    <div v-if="!loading && result != null">
      <q-list separator class="q-mt-sm">
        <q-separator />
        <q-item
          clickable
          v-for="user in result.users"
          :key="user.dbId"
          :to="`/user/${user.dbId}`"
        >
          <q-item-section>
            <div class="row items-center">
              <div
                v-html="user.renderedAvatar"
                style="height: 80px; width: 80px"
                class="q-pa-sm"
              />
              <div class="column">
                <div class="text-subtitle1 text-weight-bold">
                  {{ user.fullName }}
                </div>
                <div class="text-body2 text-blue-grey-5">@{{ user.name }}</div>
              </div>
            </div>
          </q-item-section>
        </q-item>
        <q-separator />
      </q-list>
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>

<script setup lang="ts">
import { ref } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import QueryStatus from 'components/QueryStatus.vue';

const search = ref<string>('');
const { result, loading, error } = useQuery(gql`
  query getUsers {
    users {
      dbId
      name
      fullName
      renderedAvatar
    }
  }
`);
</script>
