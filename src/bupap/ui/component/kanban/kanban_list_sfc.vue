<template>
    <div :class="column_classes()">
        <div v-for="node in list_entries()" :class="card_div_classes(node.card)" :key="node.id" @dragenter="(evt) => dragenter(node, evt)" @dragover="(evt) => dragover(node, evt)" @dragstart="(evt) => dragstart(node, evt)" @dragend="(evt) => dragend(node, evt)">
            <nicegui-kanban_card_sfc draggable="true" :class="card_classes(node.card)" :card="node.card"/>
            <div v-if="node.children.length>0" class="nicegui-row items-stretch gap-0">
                <q-btn :class="toggle_btn_classes(node)" @click="(evt)=>toggle_expand(node)">{{toggle_btn_text(node)}}</q-btn>
                <nicegui-kanban_list_sfc v-if="node.expanded" class="grow" :nodes="node.children" :depth="depth+1" @toggle_expand="toggle_expand"/>
            </div>
        </div>
    </div>
</template>



<script>
export default {
    template:"#tpl-kanban_list",
    data() {
        return {
            nodes: this.nodes,
            depth: this.depth
        }
    },
    methods: {
        list_entries() {
            // console.log(this.nodes)
            return this.nodes
        },
        // open_link(val) {
        //     console.log(val);
        // },
        // // _recursive_children(card) {
        // //     [card] + card.children_order.map((cid) =>{return _recursive_children(this.kanban.cards[cid])})
        // // },
        column_classes() {
            var result = ["nicegui-column", "p-0", "m-0", "items-stretch"]
            if (this.depth == 0) {
                result.push("gap-2")
            }
            else {
                result.push("mt-2")
                result.push("gap-1")
            }
            return result
        },
        toggle_btn_classes(node) {
            if (node.expanded) {
                return ["w-10", "mt-2", "mr-1"]
            }
            else {
                return "ml-10 h-5 grow mt-0"
            }
        },
        card_div_classes(card) {
            var result = []
            // if (card.depth > 0)
                // result.push("mt-[-4pt]")
            if (!this.show_card(card)) {
                result.push("invisible")
            }
            return result
        },
        card_classes(card) {
            var result = []
            // if (!this.show_card(card)) {
            //     result.push("invisible")
            // }
            return result
        },
        toggle_btn_text(node) {
            if (node.expanded) {
                return ""
            }
            else if (node.children.length == 1) {
                return "1 child"
            }
            else {
                return node.children.length + " children"
            }
        },
        show_card(card) {
            return true
            // return (this.dragged.entry == null || this.dragged.entry.id != card.id);
        },
        toggle_expand(node) {
            this.$emit("toggle_expand", node)
        }
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
        nodes: null,
        depth: 0
    }
}
</script>

