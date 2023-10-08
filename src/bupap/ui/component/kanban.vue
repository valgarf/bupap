<template>
    <div class="nicegui-row p-4 overflow-x-auto grow flex-nowrap items-stretch">
        <q-card v-for="lane in lanes()" :key="lane.id" class="nicegui-card min-w-[350pt] items-stretch">
            <div class="font-bold text-xl mt-5">{{lane.title}}</div>
            <q-scroll-area class=",-0 p-0 pr-2 max-w-[330] grow">
                <div class="nicegui-column p-0 m-1 gap-2 items-stretch">
                    <template v-for="card in cards(lane)" >
                        <nicegui-kanban_card :key="card.id" :card="card"/>
                        <div v-for="card in children(card)" :key="card.id" class="pl-5 mt-[-4pt]">
                            <nicegui-kanban_card :card="card" />
                            <div v-for="card in children(card)" :key="card.id" class="pl-10 mt-[-4pt]">
                                <nicegui-kanban_card :card="card" />
                            </div>
                        </div>
                    </template>
                </div>
            </q-scroll-area>
        </q-card>
    </div>
</template>


<script>
export default {
    components: { kanban_card },
    data() {
        return {
            kanban: this.initial_data
        }
    },
    methods: {
        open_link(val) {
            console.log(val);
        },
        lanes() {
            var lanes = this.kanban.lane_order.map((lid) => {return this.kanban.lanes[lid]});
            return lanes
        },
        cards(lane) {
            return lane.card_order.map((cid) => {return this.kanban.cards[cid]}).filter((c) => c.parent_id==null || c.detached);
        },
        children(card) {
            return card.children_order.map((cid) =>{return this.kanban.cards[cid]})
        }
    },
    props: {
        initial_data: null,
    }
}
</script>