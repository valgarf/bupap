<template>
  <q-page class="column q-px-md q-pt-lg">
    <div v-if="result" class="self-center text-h4 text-weight-bold">
      {{ result?.dbNode?.name }}
    </div>
    <query-status :loading="loading" :error="error" />
  </q-page>
</template>

<script setup lang='ts'>
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import { useRoute } from 'vue-router';
import QueryStatus from 'src/components/QueryStatus.vue';

const route = useRoute();
const { result, loading, error } = useQuery(
  gql`
    query getProject($dbId: Int!) {
      dbNode(typename: "Project", dbId: $dbId) {
        ... on Project {
          name
        }
      }
    }
  `,
  {
    dbId: parseInt(route.params.id as string),
  }
);

// data = KanbanData()
//         for prio in db.TaskPriority:
//             data.priorities.append(
//                 KanbanTag(
//                     prio.text,
//                     prio.default_color,
//                     prio.default_text_color,
//                 )
//             )
//         for state in db.TaskState:
//             lane = KanbanLaneData(state.name, state.name)
//             data.lanes[lane.id] = lane
//             data.lane_order.append(lane.id)
//             if state in [db.TaskState.REQUEST, db.TaskState.PLANNING, db.TaskState.SCHEDULED]:
//                 lane.priority_sorted = True
//             if state in [db.TaskState.DONE, db.TaskState.DONE]:
//                 lane.finished_sorted = True
//             tasks = [t for t in project.tasks if t.task_state == state]
//             if not lane.finished_sorted:
//                 tasks.sort(key=lambda t: t.order_id or 0)
//             else:
//                 tasks.sort(key=lambda t: t.finished_at, reverse=True)
//             for t in tasks:
//                 active = False
//                 progress = None
//                 if t.scheduled_assignee and t.finished_at is None:
//                     total_work = timedelta(0)
//                     for wp in t.work_periods:
//                         if wp.ended_at:
//                             total_work += wp.duration
//                         else:
//                             active = True
//                     if total_work:
//                         est = get_estimate(t.scheduled_assignee, t)
//                         progress = (
//                             total_work / est.expectation_pessimistic,
//                             total_work / est.expectation_average,
//                             total_work / est.expectation_optimistic,
//                         )
//                         progress = tuple(int(min(p, 1) * 100) for p in progress)
//                 card = KanbanCardData(
//                     title=t.name,
//                     id=t.id,
//                     lane_id=lane.id,
//                     parent_id=t.parent_id,
//                     depth=0,
//                     tags=[],
//                     detached=not t.attached,
//                     progress=progress,
//                     active=active,
//                     priority=t.task_priority.text,
//                     link=True,
//                     finished_at=t.finished_at,
//                 )
//                 lane.card_order.append(card.id)
//                 data.cards[card.id] = card
//         for card in list(data.cards.values()):
//             if card.parent_id is not None:
//                 if not card.parent_id in data.cards:
//                     print(f"Unkown card id {card.parent_id}")
//                     del data.cards[card.id]
//                 else:
//                     data.cards[card.parent_id].children_order.append(card.id)

// def _set_depth_rec(card, value: int = 0):
//             card.depth = value
//             for child_id in card.children_order:
//                 _set_depth_rec(data.cards[child_id], value + 1)

//         for card in data.cards.values():
//             if card.parent_id != None:
//                 continue
//             _set_depth_rec(card)

//         kanban = Kanban(data=data)
</script>