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
        <table v-if="timesheet != null" class="self-center q-mt-md">
            <tr v-for="user in timesheet" :key="user.id">
                <td class="q-py-xs">
                    <user-card :user="user"></user-card>
                </td>
                <td class="q-pl-md text-body2">
                    <div v-if="user.endAverage != null" class="text-weight-bold">Estimated end: {{
                        formatDatetimeDate(user.endOptimistic) }} - {{
        formatDatetimeDate(user.endPessimistic) }}
                        (expected: {{ formatDatetimeDate(user.endAverage) }})
                    </div>
                    <div v-if="user.estimateName != null">{{ user.estimateName }} estimate: {{
                        user.expectationOptimistic?.toFormat('hh:mm') }} - {{
        user.expectationPessimistic?.toFormat('hh:mm') }}
                        (expected: {{ user.expectationAverage?.toFormat('hh:mm') }})
                    </div>
                    <div>Worked Duration: {{ user.workedDuration.toFormat('hh:mm') }}</div>
                </td>
            </tr>
        </table>
        <div v-if="task != null" class="q-mt-md self-stretch row justify-center description-outer">
            <div class="rounded-borders q-pa-sm self-stretch description-inner text-body2">{{
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
<script lang="ts">
interface Avatar {
    svg: string;
}
interface UserData {
    id: string;
    name: string;
    fullName: string;
    avatar: Avatar;
    idx: number;
    workedDuration: Duration
    endOptimistic?: DateTime
    endAverage?: DateTime
    endPessimistic?: DateTime
    renderedAvatar?: string
    estimatedDuration?: Duration
    expectationAverage?: Duration
    expectationOptimistic?: Duration
    expectationPessimistic?: Duration
    estimateName?: string
}
interface UsersDict {
    [key: string]: UserData;
}
</script>
<script setup lang="ts">
import { computed, watchEffect } from 'vue';
import { useRoute } from 'vue-router';
import { useQuery } from '@vue/apollo-composable';
import QueryStatus from 'src/components/QueryStatus.vue';
import { gql } from '@apollo/client/core';
import { qPageStyleFnForTabsFixed } from 'src/common/helper';
import { graphql } from 'src/gql'
import { parseTimedelta, formatDatetimeDate, textColorFromBackground } from 'src/common/helper'
import { DateTime, Duration } from 'luxon'
import UserCard from 'src/components/UserCard.vue'
import { kMaxLength } from 'buffer';
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
                workPeriods {
                    startedAt
                    endedAt
                    duration
                    user {
                        id
                        name
                        fullName
                        avatar {svg}
                    }
                }
                schedule {
                    assignee {
                        id
                        name
                        fullName
                        avatar {svg}
                    }
                    average {
                        start
                        end
                    }
                    optimistic {
                        start
                        end
                    }
                    pessimistic {
                        start
                        end
                    }
                }
                estimates {
                    user {
                        id
                        name
                        fullName
                        avatar {svg}
                    }
                    estimatedDuration
                    expectationAverage
                    expectationOptimistic
                    expectationPessimistic
                    estimateType {name}
                }
            }
        }
    }
  `);

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


const timesheet = computed(() => {
    if (task.value == null || task.value.__typename != "Task" || task.value.project == null) {
        return []
    }
    const usersDict: UsersDict = {}
    let idx = 0
    if (task.value.schedule != null) {
        let schedule = task.value?.schedule
        usersDict[schedule.assignee.id] = {
            ...schedule.assignee, idx: idx, workedDuration: Duration.fromMillis(0),
            endOptimistic: DateTime.fromISO(schedule.optimistic.end),
            endAverage: DateTime.fromISO(schedule.average.end),
            endPessimistic: DateTime.fromISO(schedule.pessimistic.end),
        }
        idx++;
    }
    for (let wp of task.value.workPeriods) {
        if (wp.duration != null) {
            if (!(wp.user.id in usersDict)) {
                usersDict[wp.user.id] = { ...wp.user, idx: idx, workedDuration: Duration.fromMillis(0) }
                idx++;
            }
            usersDict[wp.user.id].workedDuration = usersDict[wp.user.id].workedDuration.plus(parseTimedelta(wp.duration))
        }
    }
    for (let est of task.value.estimates) {
        if (!(est.user.id in usersDict)) {
            usersDict[est.user.id] = { ...est.user, idx: idx, workedDuration: Duration.fromMillis(0) }
            idx++;
        }
        usersDict[est.user.id].estimatedDuration = parseTimedelta(est.estimatedDuration)
        usersDict[est.user.id].expectationAverage = parseTimedelta(est.expectationAverage)
        usersDict[est.user.id].expectationOptimistic = parseTimedelta(est.expectationOptimistic)
        usersDict[est.user.id].expectationPessimistic = parseTimedelta(est.expectationPessimistic)
        usersDict[est.user.id].estimateName = est.estimateType.name
    }
    for (let v of Object.values(usersDict)) {
        v.renderedAvatar = v.avatar.svg
    }
    return Object.values(usersDict).sort((lhs, rhs) => lhs.idx - rhs.idx)
})

watchEffect(() => {
    console.log(task.value)
})

watchEffect(() => {
    console.log(timesheet.value)
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