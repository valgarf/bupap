<template>
  <q-page
    class="column q-px-md q-pt-lg items-center justify-start"
    :style-fn="qPageStyleFnForTabs"
  >
    <q-timeline layout="comfortable">
      <q-timeline-entry
        v-for="entry in timeline"
        :key="entry.idx"
        :title="entry.title"
        :subtitle="entry.at"
      >
        <div>{{ entry.details }}</div>
      </q-timeline-entry>
    </q-timeline>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>
<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { computed } from 'vue';
import { DateTime } from 'luxon';
import { qPageStyleFnForTabs } from 'src/common/helper';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getUserActivity($dbId: Int!) {
      user: dbNode(typename: "User", dbId: $dbId) {
        ... on User {
          activity {
            at
            short
            details
          }
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id),
  }
);

const timeline = computed(() => {
  const timeline = [];
  if (result.value?.user == null) {
    return timeline;
  }

  var prev_el = null;
  var prev_date = null;
  var prev_time = null;
  var idx = 0;
  for (const el of result.value.user.activity) {
    const d = DateTime.fromISO(el.at);
    const s_date = d.toISODate();
    const s_time = d.diff(d.startOf('day')).toFormat('hh:mm');
    if (prev_date == s_date && prev_el != null) {
      prev_el.at = prev_time;
    }
    prev_date = s_date;
    prev_time = s_time;
    const at = `${s_date} ${s_time}`;
    prev_el = { idx: idx, at: at, title: el.short, details: el.details };
    timeline.push(prev_el);
    idx += 1;
  }

  return timeline;
});
</script>