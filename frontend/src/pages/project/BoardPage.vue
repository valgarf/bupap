<template>
  <q-page class="q-px-md q-pt-lg column" :style-fn="qPageStyleFnForTabsFixed">
    <!-- <div v-if="result" class="self-center text-h4 text-weight-bold">
      {{ result?.project?.name }}
    </div> -->
    <KanbanBoard v-if="kanbanData != null" :initial_data="kanbanData" />
    <query-status
      :loading="loading || (kanbanData == null && error == null)"
      :error="error"
    />
  </q-page>
</template>

<script setup lang='ts'>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';
import { DateTime } from 'luxon';
import { computed } from 'vue';
import KanbanBoard from 'src/components/kanban/KanbanBoard.vue';
import { qPageStyleFnForTabsFixed } from 'src/common/helper';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getProject($dbId: Int!) {
      project: dbNode(typename: "Project", dbId: $dbId) {
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
  `,
  {
    dbId: parseInt(route.params.id as string),
  }
);

const kanbanData = computed(() => {
  if (result.value?.project == null) {
    return null;
  }

  console.log(result.value);

  let proj = result.value.project;

  const data = {
    priorities: [],
    lanes: {},
    lane_order: [
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
    return { ...prio };
  });

  function addLane(state: str) {
    const lane = {
      title: state,
      id: state,
      priority_sorted: false,
      finished_sorted: false,
      card_order: [],
    };
    if (['REQUEST', 'PLANNING', 'SCHEDULED'].includes(state)) {
      lane.priority_sorted = true;
    }
    if (['DONE'].includes(state)) {
      lane.finished_sorted = true;
    }
    data.lanes[state] = lane;
  }

  for (let lane of data.lane_order) {
    addLane(lane);
  }

  for (let task of proj.tasks) {
    let lane = data.lanes[task.state];
    const card = {
      title: task.name,
      id: task.dbId,
      lane_id: lane.id,
      parent_id: task.parent?.dbId,
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
      finished_at: DateTime.fromISO(task.finishedAt).toISODate(),
      children_order: [],
    };
    lane.card_order.push(card.id);
    data.cards[card.id] = card;
  }

  for (let card of Object.values(data.cards)) {
    if (card.parent_id != null) {
      if (data.cards[card.parent_id] == null) {
        console.warn(`Unknown card id ${card.parent_id}`);
        data.cards[card.id] = undefined;
      } else {
        data.cards[card.parent_id].children_order.push(card.id);
      }
    }
  }

  function set_depth_rec(card, value = 0) {
    card.depth = value;
    for (let child_id of card.children_order) {
      set_depth_rec(data.cards[child_id], value + 1);
    }
  }

  for (let card of Object.values(data.cards)) {
    if (card.parent_id == null) {
      set_depth_rec(card);
    }
  }

  console.log(data);
  return data;
});
</script>