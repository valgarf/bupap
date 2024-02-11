<template>
    <q-page class="q-px-md q-pt-lg column" :style-fn="qPageStyleFnForTabsFixed">
        <q-timeline layout="comfortable">
            <q-timeline-entry v-for="event in taskActivity" :key="event.timestamp" :dot-color="getDotColor(event)"
                :title="getLabel(event)" :subtitle="formatTimestamp(event.timestamp)">
                <div v-if="event.__typename === 'TaskActivityEstimateAdded'">
                    {{ event.estimate.estimateType.name }}, estimate: {{
                        formatDuration(event.estimate.expectationOptimistic) }} - {{
        formatDuration(event.estimate.expectationPessimistic) }} (expectation: {{
        formatDuration(event.estimate.expectationAverage) }}), input estimate: {{
        formatDuration(event.estimate.estimatedDuration) }}
                </div>
            </q-timeline-entry>
        </q-timeline>
        <query-status :loading="loading" :error="error" />
    </q-page>
</template>
  
<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import QueryStatus from 'src/components/QueryStatus.vue';
import { gql } from '@apollo/client/core';
import { qPageStyleFnForTabsFixed } from 'src/common/helper';
import { graphql } from 'src/gql'
import { parseTimedelta, formatDatetimeMinutes } from 'src/common/helper'
import { DateTime } from 'luxon'

// DateTime.fromISO(task.finishedAt).toISODate()
//.toFormat('hh:mm')
const route = useRoute();
const TASK_ACTIVITY_QUERY = graphql(`
    query getTaskActivity($dbId: Int!) {
        dbNode(typename: "Task", dbId: $dbId) {
            ... on Task {
                activity {
                    __typename
                    timestamp
                    ... on TaskActivityEstimateAdded {
                        estimate { 
                            estimateType { name } 
                            estimatedDuration
                            expectationOptimistic
                            expectationPessimistic
                            expectationAverage
                        }
                        user {
                            name
                            fullName
                        }
                    }
                    ... on TaskActivityWorkperiod {
                        duration
                        user {
                            name
                            fullName
                        }
                    }
                }
            }
        }
    }
  `,);

const { result, loading, error } = useQuery(TASK_ACTIVITY_QUERY, {
    dbId: parseInt(route.params.id as string),
});

const taskActivity = computed(() => result.value?.dbNode?.activity ?? []);

watchEffect(() => {
    console.log(taskActivity.value)
})

const getDotColor = (event) => {
    // Implement your logic to determine the dot color based on the activity
    // Example: return activity.finished ? 'green' : 'blue';
    return 'blue';
};

const getLabel = (event) => {
    // Implement your logic to determine the label based on the activity
    // Example: return activity.name;
    if (event.__typename == "TaskActivityCreated") {
        return "Created"
    }
    if (event.__typename == "TaskActivityFinished") {
        return "Finished"
    }
    if (event.__typename == "TaskActivityWorkperiod") {
        if (event.duration != null) {
            let s_dur = formatDuration(event.duration)
            return `${event.user?.fullName} worked on task for ${s_dur}`
        }
        else {
            return `${event.user?.fullName} started working on task`
        }
    }
    if (event.__typename == "TaskActivityEstimateAdded") {
        return `${event.user?.fullName} added estimate`
    }
    return "<TBD>"
};

const formatTimestamp = (timestamp) => {
    // Format the timestamp to your desired format
    return formatDatetimeMinutes(DateTime.fromISO(timestamp))
};
const formatDuration = (dur) => {
    return parseTimedelta(dur).toFormat("hh:mm")
}
</script>