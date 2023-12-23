<template>
  <q-page class="column q-px-md q-pt-lg items-center justify-start">
    <!-- User data -->
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
    <!-- Project summaries -->
    <div v-if="result" class="row justify-center items-start summaries">
      <q-card
        v-for="ps in result.user.projectSummaries"
        :key="ps.project.dbId"
        class="q-ma-md"
      >
        <q-card-section>
          <div class="text-h6">{{ ps.project.name }}</div>
        </q-card-section>
        <q-card-section class="row justify-center">
          <div class="column items-end">
            <div class="q-mr-xs">spent time:</div>
            <div class="q-mr-xs">tasks open:</div>
            <div class="q-mr-xs">tasks done:</div>
          </div>
          <div class="column items-start">
            <div>{{ format_duration(ps.totalDuration) }}</div>
            <div>{{ ps.numTasksOpen }}</div>
            <div>{{ ps.numTasksDone }}</div>
          </div>
        </q-card-section>
      </q-card>
    </div>
    <!-- Statistics -->
    <div v-for="stat in estimateStatistics" :key="stat.name">
      <q-table
        :rows="stat.rows"
        :columns="tableColumns"
        :pagination="{ rowsPerPage: 0 }"
        flat
        row-key="taskId"
      />
    </div>
    <!-- Query loading / error information -->
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>
<style scoped>
.avatar {
  height: 160px;
  width: 160px;
}
.summaries {
  max-width: max(50%, 500px);
}
</style>
<script setup>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { Duration, DateTime } from 'luxon';
import { parseTimedelta, formatDatetimeMinutes } from 'src/common/helper';
import { computed } from 'vue';

const route = useRoute();

const { result, loading, error } = useQuery(
  gql`
    query getUser($dbId: Int!) {
      user: dbNode(typename: "User", dbId: $dbId) {
        ... on User {
          name
          fullName
          renderedAvatar
          projectSummaries {
            project {
              id
              dbId
              name
            }
            totalDuration
            numTasksOpen
            numTasksDone
          }
          estimateStatistics {
            evaluated
            numDatapoints
            shiftOptimistic
            shiftAverage
            shiftPessimistic
            estimateType {
              name
              description
              minDatapoints
              maxDatapoints
            }
            sufficient
            datapoints {
              value
              actualWork
              numWorkPeriods
              start
              end
              estimate {
                dbId
                task {
                  dbId
                  name
                }
                estimatedDuration
              }
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

function convertDatapoint(dp) {
  console.log(dp.estimate.estimatedDuration);
  return {
    taskId: dp.estimate.task.dbId,
    taskName: dp.estimate.task.name,
    value: Math.round(dp.value * 100) / 100,
    estimate: parseTimedelta(dp.estimate.estimatedDuration),
    actualWork: parseTimedelta(dp.actualWork),
    start: DateTime.fromISO(dp.start),
    end: DateTime.fromISO(dp.end),
  };
}

function convertEstimateStatistics(stat) {
  const rows = stat.datapoints.map(convertDatapoint);
  return { rows, name: stat.estimateType.name };
}

const estimateStatistics = computed(() => {
  if (result.value?.user?.estimateStatistics == null) {
    return [];
  }

  return result.value.user.estimateStatistics.map(convertEstimateStatistics);
});

const tableColumns = [
  {
    label: 'Task Id',
    name: 'taskId',
    field: 'taskId',
    align: 'left',
    sortable: true,
  },
  {
    label: 'Task Name',
    name: 'taskName',
    field: 'taskName',
    align: 'left',
    sortable: true,
  },
  {
    label: 'Value',
    name: 'value',
    field: 'value',
    align: 'right',
    sortable: true,
  },
  {
    label: 'Estimated Duration',
    name: 'estimate',
    field: (row) => row.estimate.toFormat('hh:mm'),
    align: 'right',
    sortable: true,
  },
  {
    label: 'Worked Duration',
    name: 'actualWork',
    field: (row) => row.actualWork.toFormat('hh:mm'),
    align: 'right',
    sortable: true,
  },
  {
    label: 'Start',
    name: 'start',
    field: (row) => formatDatetimeMinutes(row.start),
    align: 'right',
    sortable: true,
  },
  {
    label: 'End',
    name: 'end',
    field: (row) => formatDatetimeMinutes(row.end),
    align: 'right',
    sortable: true,
  },
];

function format_duration(v) {
  v = v.split('.')[0]; // remove any milliseconds
  var [h, m, s] = v.split(':').map((el) => parseInt(el));
  // round to minutes
  m = m || 0;
  if (s != null && s >= 30) {
    m += 1;
  }
  const d = Duration.fromObject({ hours: h, minutes: m });
  return d.normalize().rescale().toHuman();
}
</script>