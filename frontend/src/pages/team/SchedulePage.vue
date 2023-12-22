<template>
  <q-page class="column q-ma-md">
    <div class="row no-wrap items-center justify-start">
      <q-btn icon="keyboard_arrow_left" flat @click="prev_day" />
      <q-input
        filled
        v-model="day"
        mask="####-##-##"
        class="q-pt-md"
        error-message="Please enter a valid date."
        :error="!dateIsValid"
      >
        <template v-slot:append>
          <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy
              cover
              transition-show="scale"
              transition-hide="scale"
            >
              <q-date no-unset v-model="day" mask="YYYY-MM-DD">
                <div class="row items-center justify-end">
                  <q-btn v-close-popup label="Close" color="primary" flat />
                </div>
              </q-date>
            </q-popup-proxy>
          </q-icon>
        </template>
      </q-input>
      <q-btn icon="keyboard_arrow_right" flat @click="next_day" />
      <q-spinner v-if="loading" color="primary" size="3em" />
    </div>
    <gantt-chart v-if="ganttData != null" class="col-grow" :data="ganttData" />
    <query-status :loading="false" :error="error" />
  </q-page>
</template>
<style scoped lang="scss">
.q-page {
  height: calc(100vh - 148px) !important;
  min-height: 0px !important;
}
</style>
<script setup lang = "ts">
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { onBeforeRouteUpdate, useRoute, useRouter } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import {
  default as GanttChart,
  GanttBar,
  GanttRow,
  GanttData,
} from 'src/components/GanttChart.vue';
import { computed, ref, watchEffect } from 'vue';
import { useRouteQuery } from 'vue-use-route-query';

const route = useRoute();

const day = useRouteQuery('day', new Date().toISOString().split('T')[0], {
  mode: 'push',
});

function prev_day() {
  const d = new Date(day.value);
  d.setDate(d.getDate() - 1);
  day.value = d.toISOString().split('T')[0];
}

function next_day() {
  const d = new Date(day.value);
  d.setDate(d.getDate() + 1);
  day.value = d.toISOString().split('T')[0];
}

const dateIsValid = computed(() => {
  return !isNaN(new Date(day.value));
});

const dayStart = computed(() => {
  if (!dateIsValid.value) {
    return null;
  }
  const d = new Date(day.value);
  d.setHours(0, 0, 0, 0);
  return d;
});

const queryStart = computed(() => {
  if (dayStart.value == null) {
    return null;
  }
  const d = new Date(dayStart.value.getTime() - 2 * 3600 * 1000);
  return d.toISOString();
});
const queryEnd = computed(() => {
  if (dayStart.value == null) {
    return null;
  }
  const d = new Date(dayStart.value.getTime() + 26 * 3600 * 1000);
  return d.toISOString();
});

const { result, loading, error } = useQuery(
  gql`
    query schedule(
      $start: DateTime!
      $end: DateTime!
      $mode: ScheduleMode!
      $dbId: Int!
    ) {
      team: dbNode(typename: "Team", dbId: $dbId) {
        __typename
        ... on Team {
          id
          dbId
          name
          schedule(input: { start: $start, end: $end, mode: $mode }) {
            now
            covers {
              start
              end
            }
            actual {
              start
              end
            }
            userSchedules {
              user {
                fullName
              }
              workingPeriods {
                start
                end
              }
              timesinks {
                period {
                  start
                  end
                }
                color
                text
              }
              workedTasks {
                period {
                  start
                  end
                }
                color
                text
              }
              scheduledTasks {
                period {
                  start
                  end
                }
                color
                text
              }
            }
          }
        }
      }
    }
  `,
  {
    start: queryStart,
    end: queryEnd,
    mode: 'AVERAGE',
    dbId: parseInt(route.params.id),
  },
  () => ({
    enabled: dateIsValid.value,
  })
);

function convert_dt(dt: string): Date {
  return new Date(dt);
}
function convert_work_period(period, idx): GanttBar {
  return {
    idx: idx,
    key: 'wp-' + idx,
    start: convert_dt(period.start),
    end: convert_dt(period.end),
    color: '#ffffff',
  };
}
function convert_task(task, idx): GanttBar {
  return {
    idx: idx,
    key: 'wp-' + idx,
    start: convert_dt(task.period.start),
    end: convert_dt(task.period.end),
    color: task.color,
    text: task.text,
  };
}

function convert_user_schedule(userSchedule, idx): GanttRow {
  const tasks = userSchedule.timesinks
    .concat(userSchedule.workedTasks)
    .concat(userSchedule.scheduledTasks);
  return {
    idx: idx,
    key: 'row-' + idx,
    name: userSchedule.user.fullName,
    bg: userSchedule.workingPeriods.map(convert_work_period),
    fg: [],
    bars: tasks.map(convert_task),
  };
}
function convert_result(data): GanttData {
  const rows = data.team.schedule.userSchedules.map(convert_user_schedule);
  const covers_start = convert_dt(data.team.schedule.covers.start).getTime();
  const covers_end = convert_dt(data.team.schedule.covers.end).getTime();
  const actual_start = convert_dt(data.team.schedule.actual.start).getTime();
  const actual_end = convert_dt(data.team.schedule.actual.end).getTime();
  const start = new Date(Math.max(actual_start - 3600000, covers_start));
  const end = new Date(Math.min(actual_end + 3600000, covers_end));

  const result: GanttData = {
    title: data.team.name,
    rows: rows,
    now: convert_dt(data.team.schedule.now),
    start: start,
    end: end,
  };
  return result;
}

const ganttDataConverted = computed(() => {
  if (result.value?.team?.schedule == null) {
    return null;
  }
  return convert_result(result.value);
});

// caching logic
const ganttData = ref(null);
watchEffect(() => {
  if (ganttDataConverted.value != null && error.value == null) {
    ganttData.value = ganttDataConverted.value;
  }
  if (error.value != null) {
    ganttData.value = null;
  }
});
</script>