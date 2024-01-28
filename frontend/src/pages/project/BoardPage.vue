<template>
  <q-page class="q-px-md q-pt-lg column" :style-fn="qPageStyleFnForTabsFixed">
    <!-- <div v-if="result" class="self-center text-h4 text-weight-bold">
      {{ result?.project?.name }}
    </div> -->
    <KanbanBoard v-if="kanbanData != null" :initial-data="kanbanData" />
    <query-status
      :loading="loading || (kanbanData == null && error == null)"
      :error="error"
    />
  </q-page>
</template>

<script setup lang='ts'>
import { useQuery } from '@vue/apollo-composable';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { DateTime } from 'luxon'; 
import { computed } from 'vue';
import KanbanBoard from 'src/components/kanban/KanbanBoard.vue';
import { qPageStyleFnForTabsFixed } from 'src/common/helper';
import { KanbanPropsData, Card } from 'src/components/kanban/interfaces'
import { graphql } from 'src/gql'

const route = useRoute();
const { result, loading, error } = useQuery(
  graphql(`
    query getProjectBoard($dbId: Int!) {
      project: dbNode(typename: "Project", dbId: $dbId) {
        __typename
        ... on Project {
          name
          tasks {
            id
            dbId
            name
            parent {
              dbId
            }
            tags {
              text
              color
            }
            state
            finishedAt
            orderId
            attached
            progress {
              pessimistic
              average
              optimistic
              active
            }
            priority
          }
          priorities {
            key
            text
            color
          }
        }
      }
    }
  `),
  {
    dbId: parseInt(route.params.id as string),
  }
);

const kanbanData = computed(() => {
  if (result.value?.project == null) {
    return null;
  }

  if (result.value.project.__typename != 'Project') {
    return null; // throw? should never happen
  }

  let proj = result.value.project;

  const data: KanbanPropsData = {
    priorities: [],
    lanes: {},
    laneOrder: [
      'REQUEST',
      'PLANNING',
      'DEFERRED',
      'SCHEDULED',
      'DONE',
      'DISCARDED',
      'HOLD',
    ],
    cards: {},
  };

  data.priorities = proj.priorities.map((prio) => {
    return { key: prio.key ?? undefined, text: prio.text, color: prio.color };
  });

  function addLane(state: string) {
    const lane = {
      title: state,
      id: state,
      prioritySorted: false,
      finishedSorted: false,
      cardOrder: [],
    };
    if (['REQUEST', 'PLANNING', 'SCHEDULED'].includes(state)) {
      lane.prioritySorted = true;
    }
    if (['DONE'].includes(state)) {
      lane.finishedSorted = true;
    }
    data.lanes[state] = lane;
  }

  for (let lane of data.laneOrder) {
    addLane(lane);
  }

  for (let task of proj.tasks) {
    let lane = data.lanes[task.state];
    const card: Card = {
      title: task.name,
      id: task.dbId,
      laneId: lane.id,
      parentId: task.parent?.dbId,
      depth: 0,
      tags: [],
      detached: !task.attached,
      progress: [
        task.progress.pessimistic,
        task.progress.average,
        task.progress.optimistic,
      ],
      active: task.progress.active,
      priority: task.priority,
      link: true,
      finishedAt: DateTime.fromISO(task.finishedAt).toISODate(),
      childrenOrder: [],
    };
    lane.cardOrder.push(card.id);
    data.cards[card.id] = card;
  }

  for (let card of Object.values(data.cards)) {
    if (card.parentId != null) {
      if (data.cards[card.parentId] == null) {
        console.warn(`Unknown card id ${card.parentId}`);
        delete data.cards[card.id];
      } else {
        data.cards[card.parentId].childrenOrder.push(card.id);
      }
    }
  }

  function setDepthRec(card: Card, value = 0) {
    card.depth = value;
    for (let childId of card.childrenOrder) {
      setDepthRec(data.cards[childId], value + 1);
    }
  }

  for (let card of Object.values(data.cards)) {
    if (card.parentId == null) {
      setDepthRec(card);
    }
  }

  return data;
});
</script>