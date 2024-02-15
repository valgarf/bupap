<template>
    <q-page class="q-px-md q-pt-lg column" :style-fn="qPageStyleFnForTabsFixed">
        <div v-if="task != null" class="self-center text-h6 text-weight-bold">
            {{ task.name }}
        </div>
        <div v-if="tags.length > 0" class="row self-center q-gutter-sm">
            <q-badge v-for="tag in tags" :key="tag.key + tag.text + tag.color" :color="tag.color"
                :text-color="textColorFromBackground(tag.color)" class="select-none q-px-sm text-weight-bold text-body2">{{
                    tag.text
                }}</q-badge>
        </div>
        <div v-if="task != null" class="q-mt-md self-stretch row justify-center description-outer">
            <div class="rounded-borders q-pa-sm self-stretch description-inner">{{
                task.description }}
            </div>
        </div>
        <query-status :loading="loading" :error="error" />
    </q-page>
</template>

<style lang="scss">
.description-outer {
    flex-basis: 200px
}

.description-inner {
    flex-basis: 800px;
    border: 1px solid $blue-grey-2
}
</style>
<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import QueryStatus from 'src/components/QueryStatus.vue';
import { gql } from '@apollo/client/core';
import { qPageStyleFnForTabsFixed } from 'src/common/helper';
import { graphql } from 'src/gql'
import { parseTimedelta, formatDatetimeMinutes, textColorFromBackground } from 'src/common/helper'
import { DateTime } from 'luxon'
// DateTime.fromISO(task.finishedAt).toISODate()
//.toFormat('hh:mm')
const route = useRoute();
const TASK_OVERVIEW_QUERY = graphql(`
    query getTaskOverview($dbId: Int!) {
        task: dbNode(typename: "Task", dbId: $dbId) {
            __typename
            ... on Task {
                name
                description
                state
                priority
                type
                project {
                    priorities {
                        key
                        text
                        color
                    }
                    taskStates {
                        key
                        text
                        color
                    }
                    taskTypes {
                        key
                        text
                        color
                    }
                }
                tags {
                    text
                    color
                }
            }
        }
    }
  `,);

const { result, loading, error } = useQuery(TASK_OVERVIEW_QUERY, {
    dbId: parseInt(route.params.id as string),
});

const task = computed(() => result.value?.task);

const tags = computed(() => {
    if (task.value == null || task.value.__typename != "Task" || task.value.project == null) {
        return []
    }
    let result = [];
    for (const p of task.value.project.taskTypes) {
        if (task.value.type == p.key) {
            result.push(p)
        }
    }
    for (const p of task.value.project.priorities) {
        if (task.value.priority == p.key) {
            result.push(p)
        }
    }
    for (const p of task.value.project.taskStates) {
        if (task.value.state == p.key) {
            result.push(p)
        }
    }
    result.push(...task.value.tags)
    return result
})
watchEffect(() => {
    console.log(task.value)
})

// const getDotColor = (event) => {
//     // Implement your logic to determine the dot color based on the activity
//     // Example: return activity.finished ? 'green' : 'blue';
//     return 'blue';
// };

// const getLabel = (event) => {
//     // Implement your logic to determine the label based on the activity
//     // Example: return activity.name;
//     if (event.__typename == "TaskActivityCreated") {
//         return "Created"
//     }
//     if (event.__typename == "TaskActivityFinished") {
//         return "Finished"
//     }
//     if (event.__typename == "TaskActivityWorkperiod") {
//         if (event.duration != null) {
//             let s_dur = formatDuration(event.duration)
//             return `${event.user?.fullName} worked on task for ${s_dur}`
//         }
//         else {
//             return `${event.user?.fullName} started working on task`
//         }
//     }
//     if (event.__typename == "TaskActivityEstimateAdded") {
//         return `${event.user?.fullName} added estimate`
//     }
//     return "<TBD>"
// };

// const formatTimestamp = (timestamp) => {
//     // Format the timestamp to your desired format
//     return formatDatetimeMinutes(DateTime.fromISO(timestamp))
// };
const formatDuration = (dur) => {
    return parseTimedelta(dur).toFormat("hh:mm")
}
</script>