<template>
    <div :class="column_classes()">
        <div v-for="node in list_entries()" :class="card_div_classes(node)" :key="node.id" @dragenter="(evt) => dragenter(node, evt)" @dragover="(evt) => dragover(node, evt)" @dragstart="(evt) => dragstart(node, evt)" @dragend="(evt) => dragend(node, evt)" @dragleave="(evt) => dragleave(node, evt)">
            <nicegui-kanban_card_sfc draggable="true" :class="card_classes(node)" :card="node.card"/>
            <div v-if="node.children.length>0" class="nicegui-row items-stretch gap-0">
                <q-btn :class="toggle_btn_classes(node)" @click="(evt)=>toggle_expand(node)">{{toggle_btn_text(node)}}</q-btn>
                <nicegui-kanban_list_sfc v-if="node.expanded && !node.dragged" class="grow" :parent_id="node.id" :nodes="node.children" :depth="depth+1" v-on="$listeners"/>      
                <!-- for v-on="$listeners" see https://v2.vuejs.org/v2/api/#vm-listeners -->
            </div>
        </div>
    </div>
</template>



<script>
export default {
    //@toggle_expand="toggle_expand" @dragstart_card="dragstart_card" @dragend_card="dragend_card" @dragover_card="dragover_card" @dragleave_card="dragleave_card"/>
    data() {
        return {
            parent_id: this.parent_id,
            nodes: this.nodes,
            depth: this.depth
        }
    },
    methods: {
        list_entries() {
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
        card_div_classes(node) {
            var result = []
            // if (card.depth > 0)
                // result.push("mt-[-4pt]")
            if (!this.show_card(node)) {
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
            let num = node.children.length
            return num + " " + (num > 1 ? "subtasks": "subtask")
        
        },
        show_card(node) {
            return !node.dragged
            // return (this.dragged.entry == null || this.dragged.entry.id != card.id);
        },
        toggle_expand(node) {
            this.$emit("toggle_expand", node)
        },
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
        dragover(node, evt) {
            console.log("over", node, evt);
            let drag_data_str = evt.dataTransfer.getData("application/json")
            if (drag_data_str == null) {
                // not a drag event for us
                return
            }
            try {
                var drag_data = JSON.parse(drag_data_str)
            } catch(err) {
                console.warn("Failed to decode json from drag object:", drag_data_str)
                return
            }
            if (drag_data["node_ids"] == null) {
                // not a drag event for us
                return
            }
            let parent_id = drag_data["parent_id"]
            if (this.parent_id != null && this.parent_id != parent_id) {
                // wrong list, parent does not match
                return
            }
            evt.stopPropagation()
            
            let node_ids = drag_data["node_ids"]
            if (node_ids.indexOf(node.id) != -1) {
                // draggeed over itself, ignore
                return
            }
            this.dragover_card(node.id, node_ids, evt.x, evt.y)
        },
        dragenter(node, evt) {
            // console.log("enter", node, evt);
        },
        dragstart(node, evt) {
            evt.dataTransfer.clearData()
            evt.dataTransfer.setData("application/json", JSON.stringify({parent_id: node.parent_id, node_ids: [node.id]}))
            // TODO: set task url
            evt.stopPropagation()
            this.dragstart_card([node.id], evt.x, evt.y)          
        },
        dragleave(node, evt) {
            // let drag_data_str = evt.dataTransfer.getData("application/json")
            // if (drag_data_str == null) {
            //     // not a drag event for us
            //     return
            // }
            // try {
            //     var drag_data = JSON.parse(drag_data_str)
            // } catch(err) {
            //     console.warn("Failed to decode json from drag object:", drag_data_str)
            //     return
            // }
            // if (drag_data["node_ids"] == null) {
            //     // not a drag event for us
            //     return
            // }
            // let parent_id = drag_data["parent_id"]
            // if (this.parent_id != null && this.parent_id != parent_id) {
            //     // wrong list, parent does not match
            //     return
            // }
            // evt.stopPropagation()
            
            // let node_ids = drag_data["node_ids"]
            // if (node_ids.indexOf(node.id) != -1) {
            //     // draggeed over itself, ignore
            //     return
            // }
            // this.dragleave_card(node.id)//, node_ids)
            // // console.log("leave", node, evt);
        },
        dragend(node, evt) {
            evt.stopPropagation()
            this.dragend_card([node.id])
        },
        dragover_card(target_node_id, node_ids,x, y) {
            this.$emit("dragover_card", target_node_id, node_ids,x,y)
        },
        dragstart_card(node_ids,x,y) {
            this.$emit("dragstart_card", node_ids,x,y)
        },
        dragend_card(node_ids) {
            this.$emit("dragend_card", node_ids)
        },
        dragleave_card(node_id) {
            this.$emit("dragleave_card", node_id)
        }
    },
    props: {
        parent_id: null,
        nodes: null,
        depth: 0
    }
}
</script>

