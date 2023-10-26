<template>
    <div class="nicegui-row p-4 overflow-x-auto grow flex-nowrap items-stretch">
        <q-card v-for="lane in lanes()" :key="lane.id" class="nicegui-card min-w-[350pt] items-stretch">
            <div class="font-bold text-xl mt-5">{{lane.title}}</div>
            <q-scroll-area class="m-0 p-0 pr-2 max-w-[330] grow">
                    <!-- <div v-for="node in nodes_lane(lane)" :key="node.id">
                        {{node.card.id}}{{node.card.title}}
                    </div> -->
                <div class="p-2"><nicegui-kanban_list_sfc :nodes="nodes_lane(lane)" :depth="0" @toggle_expand="toggle_expand"/></div>
            </q-scroll-area>
        </q-card>
    </div>
</template>

 <!-- <div v-for="card in flat_cards(lane)" :class="card_div_classes(card)" :key="card.id" @dragenter="(evt) => dragenter(card, evt)" @dragover="(evt) => dragover(card, evt)" @dragstart="(evt) => dragstart(card, evt)" @dragend="(evt) => dragend(card, evt)">
                        <nicegui-kanban_card draggable="true" :class="card_classes(card)" :card="card"/>
                    </div> -->

<script>
export default {
    data() {
        return {
            kanban: this.initial_data,
            nodes: this.compute_nodes(this.initial_data),
            dragged: {x:0,y:0,entry:null},
        }
    },
    methods: {
        // open_link(val) {
        //     console.log(val);
        // },
        lanes() {
            var lanes = this.kanban.lane_order.map((lid) => {return this.kanban.lanes[lid]});
            return lanes
        },
        compute_nodes(kanban) {
            var nodes = {}
            for (let [k, v] of Object.entries(kanban.cards)) {
                let intk = parseInt(k)
                nodes[intk] = {"parent": null, "children": [], "id": intk, "card": v, "lane_id": null, expanded: false}
            }
            for (let n of Object.values(nodes)) {
                n.children = n.card.children_order.map((cid) => nodes[cid])
                var p = nodes[n.card.parent_id]
                if (p!= undefined) {
                    n.parent = p
                }
            }
            for (let n of Object.values(nodes)) {
                if (n.parent != null && n.parent.children.indexOf(n) == -1) {
                    console.error(n, n.parent)
                }
            }
            return nodes
        },
        nodes_lane(lane) {
            return lane.card_order.map((cid) => this.nodes[cid]).filter((n) => n!=undefined && n!=null && (n.parent==null || n.card.detached));
        },
        toggle_expand(node) {
            var n = this.nodes[node.id]
            n.expanded = !n.expanded
        }
        // cards(lane) {
        //     return lane.card_order.map((cid) => {return this.kanban.cards[cid]}).filter((c) => c.parent_id==null || c.detached);
        // },
        // // _recursive_children(card) {
        // //     [card] + card.children_order.map((cid) =>{return _recursive_children(this.kanban.cards[cid])})
        // // },
        // card_div_classes(card) {
        //     var result = ["pl-" + 5*card.depth]
        //     if (card.depth > 0)
        //         result.push("mt-[-4pt]")
        //     if (!this.show_card(card)) {
        //         result.push("invisible")
        //     }
        //     return result
        // },
        // card_classes(card) {
        //     var result = []
        //     // if (!this.show_card(card)) {
        //     //     result.push("invisible")
        //     // }
        //     return result
        // },
        // show_card(card) {
        //     return (this.dragged.entry == null || this.dragged.entry.id != card.id);
        // },
        // flat_cards(lane) {
        //     return lane.card_order.map((cid) => {return this.kanban.cards[cid]}).filter((c) => c.depth <=3);
        // },

        // children(card) {
        //     return card.children_order.map((cid) =>{return this.kanban.cards[cid]})
        // },
        // dragenter(card, evt) {
        //     // console.log(card, evt);
        // },
        // acceptable_above(orig_card, target_card, target_lane, target_idx) {
        //     return (target_card.parent_id == null || orig_card.parent_id == target_card.parent_id)
        // },
        // acceptable_below(orig_card, target_card, target_lane, target_idx) {
        //     if (target_lane.card_order.length <= target_idx + 1) {
        //         return true
        //     }
        //     target_card = this.kanban.cards[target_lane.card_order[target_idx+1]]
        //     return this.acceptable_above(orig_card, target_card, target_lane, target_idx+1)
        // },
        // dragover(card, evt) {
        //     if (this.dragged.entry == null) {
        //         return
        //     }
        //     if (card.id != this.dragged.entry.id) {
        //         var orig_lane = this.kanban.lanes[this.dragged.entry.lane_id]
        //         var target_lane = this.kanban.lanes[card.lane_id]
        //         if (orig_lane == target_lane) {
        //             var lane = orig_lane
        //             var card_idx = lane.card_order.indexOf(card.id)
        //             var dragged_idx = lane.card_order.indexOf(this.dragged.entry.id)
        //             if (dragged_idx>card_idx && this.acceptable_above(this.dragged.entry, card, lane, card_idx)) {
        //                 lane.card_order.splice(dragged_idx, 1)
        //                 lane.card_order.splice(card_idx, 0, this.dragged.entry.id)
        //                 console.log(card, evt, "up", dragged_idx, card_idx);
        //             }
        //             else if (dragged_idx < card_idx && this.acceptable_below(this.dragged.entry, card, lane, card_idx)) {
        //                 lane.card_order.splice(card_idx+1, 0, this.dragged.entry.id)
        //                 lane.card_order.splice(dragged_idx, 1)
        //                 console.log(card, evt, "down", dragged_idx, card_idx);
        //             }
        //         }
                
        //     }
        // },
        // dragstart(card, evt) {
        //     var self = this
        //     // Note: setting the dragged entry will set it to invisible and it will not be shown 
        //     // during the drag operation. Delaying the invisibility by one frame will generate a 
        //     // drag image and then hide the original card.
        //     window.requestAnimationFrame(function() {
        //         self.dragged.entry = card;
        //     });
            
        // },
        // dragend() {
        //     this.dragged.entry = null
        // },
        // move(event) {
        //     this.dragged.x = event.offsetX;
        //     this.dragged.y = event.offsetY;
        // },
    },
    props: {
        initial_data: null,
    }
}
</script>

<style scoped>
nicegui-kanban_card * {
    pointer-events: none;
}
</style>