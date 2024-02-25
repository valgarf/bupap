<template>
    <q-page class="q-px-md q-pt-lg" :style-fn="qPageStyleFnForTabsFixed">
        <q-scroll-area style="height:100%; width:100%">
            <div style="height:100%; width:100%" class="column">
                <div v-if="task != null" class="self-center text-h6 text-weight-bold">
                    {{ task.name }}
                </div>
                <div v-if="tags.length > 0" class="row self-center q-gutter-sm">
                    <q-badge v-for="tag in tags" :key="tag.key + tag.text + tag.color" :color="tag.color"
                        :text-color="textColorFromBackground(tag.color)"
                        class="select-none q-px-sm text-weight-bold text-body2">{{
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
                <div v-if="task != null" class="q-my-md self-stretch row justify-center description-outer">
                    <div class="rounded-borders q-pa-sm self-stretch description-inner text-body2">{{
                        task.description }}
                    </div>
                </div>
                <apexchart v-if="plot_data != null" height="300" type="rangeArea" :options="plot_data.options"
                    :series="plot_data.series">
                </apexchart>
                <query-status :loading="loading" :error="error" />
            </div>
        </q-scroll-area>
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
import { parseTimedelta, formatDatetimeMinutes, formatDatetimeDate, textColorFromBackground } from 'src/common/helper'
import { DateTime, Duration } from 'luxon'
import UserCard from 'src/components/UserCard.vue'
import { kMaxLength } from 'buffer';
import Apexchart from 'vue3-apexcharts';

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
                finishedAt
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
                history {
                    date
                    scheduledOptimisticEnd
                    scheduledAverageEnd
                    scheduledPessimisticEnd
                }
            }
        }
    }
  `);

const { result, loading, error } = useQuery(TASK_OVERVIEW_QUERY, {
    dbId: parseInt(route.params.id as string),
});

const task = computed(() => result.value?.task);

const plot_data = computed(() => {
    const day_ms = 24 * 3600 * 100;
    if (task.value == null || task.value.__typename != "Task" || task.value.history.length == 0) {
        return null
    }
    const converted = task.value.history.map((el) => {
        return {
            date: DateTime.fromISO(el.date),
            scheduledOptimisticEnd: DateTime.fromISO(el.scheduledOptimisticEnd),
            scheduledAverageEnd: DateTime.fromISO(el.scheduledAverageEnd),
            scheduledPessimisticEnd: DateTime.fromISO(el.scheduledPessimisticEnd),
        }
    })
    let result = {}
    result.options = {
        title: {
            text: 'History of estimated finished dates',
            align: 'center',
        },
        chart: {
            id: 'apex-history',
            height: 350,
            type: 'rangeArea',
        },
        colors: ['#33b2df', '#33b2df'],
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'straight',
            width: [0, 5]
        },
        // legend: {
        //     show: false,
        //     //   customLegendItems: ['Team B', 'Team A'],
        //     //   inverseOrder: true
        // },
        // markers: {
        //     hover: {
        //         sizeOffset: 5
        //     }
        // },
        xaxis: {
            type: 'datetime',
            // labels: {
            //     formatter: (v, value) => {
            //         console.log(v, value)
            //         return formatDatetimeMinutes(DateTime.fromMillis(value))
            //     }
            // }
        },
        yaxis: {
            labels: {
                formatter: (value) => {
                    return formatDatetimeMinutes(DateTime.fromMillis(value * day_ms))
                }
            }
        },
    }
    result.series = [
        {
            type: 'rangeArea',
            name: 'range',
            data: converted.map((el) => {
                return {
                    x: el.date.toMillis(),
                    y: [el.scheduledOptimisticEnd.toMillis() / day_ms, el.scheduledPessimisticEnd.toMillis() / day_ms]
                }
            })
        },
        {
            type: 'line',
            name: 'average',
            data: converted.map((el) => {
                return {
                    x: el.date.toMillis(),
                    y: el.scheduledAverageEnd.toMillis() / day_ms
                }
            })
        },

    ]
    if (task.value.finishedAt != null) {
        const dtFinished = DateTime.fromISO(task.value.finishedAt)
        result.series[1].data.push({ x: dtFinished.toMillis(), y: dtFinished.toMillis() / day_ms })
        result.series[0].data.push({ x: dtFinished.toMillis(), y: [dtFinished.toMillis() / day_ms, dtFinished.toMillis() / day_ms] })
    }
    const xmillis = result.series[1].data.map((el) => { return el.x })
    const minx = Math.min(...xmillis)
    const maxx = Math.max(...xmillis)
    const offsetx = Math.max(0.1 * (maxx - minx), 12 * 3600 * 1000)
    result.options.xaxis.min = minx - offsetx
    result.options.xaxis.max = maxx + offsetx
    result.options.xaxis.forceNiceScale = true
    const min_ymillis = result.series[0].data.map((el) => { return el.y[0] })
    const max_ymillis = result.series[0].data.map((el) => { return el.y[1] })
    let miny = Math.min(...min_ymillis)
    let maxy = Math.max(...max_ymillis)
    const offsety = Math.max(0.1 * (maxy - miny), 0.5)
    miny = (miny - offsety)
    maxy = (maxy + offsety)
    let round_factor = 0.25;
    if (maxy - miny > 4) {
        round_factor = 1
    }
    result.options.yaxis.min = Math.floor((miny - offsety) / round_factor) * round_factor
    result.options.yaxis.max = Math.ceil((maxy + offsety) / round_factor) * round_factor
    result.options.yaxis.forceNiceScale = true
    return result
})


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

// watchEffect(() => {
//     console.log(task.value)
// })

// watchEffect(() => {
//     console.log(timesheet.value)
// })

watchEffect(() => {
    console.log(plot_data)
})

</script>