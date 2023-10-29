<template>
    <div :class="column_classes()">
        <div v-for="node in list_entries()" 
                :class="card_div_classes(node)" :key="node_key(node)" 
                @dragover.prevent="(evt) => dragover(node, evt)" 
                @dragstart="(evt) => dragstart(node, evt)">
            <template v-if="node.card.detached && this.depth==0">
                <nicegui-kanban_card_sfc class="mt-0" :class="card_classes(node.parent)" :card="node.parent.card" :detached="true"/>
                <!-- <nicegui-kanban_card_sfc draggable="true" class="ml-10 mt-1" :class="card_classes(node)" :card="node.card" :detached="false"/> -->
                <div class="nicegui-row items-stretch gap-0 mt-[-3pt]">
                    <div class="w-10" ></div>
                    <nicegui-kanban_list_sfc 
                            class="grow" :parent_id="node.parent.id" :nodes="[node]" :depth="depth+1" :detached_parent="true"
                            @toggle_expand="toggle_expand" 
                            @dragstart_card="dragstart_card" 
                            @dragover_card="dragover_card"/>
                </div>
            </template>
            <template v-else>
                <nicegui-kanban_card_sfc :draggable="!node_is_detached(node)" :class="card_classes(node)" :card="node.card" :detached="node_is_detached(node)"/>
                <div v-if="node.children.length>0 && !(node.card.detached && this.depth>0 &&!this.detached_parent)" class="nicegui-row items-stretch gap-0 mt-[-3pt]">
                    <q-btn :class="toggle_btn_classes(node)" @click="(evt)=>toggle_expand(node)">{{toggle_btn_text(node)}}</q-btn>
                    <nicegui-kanban_list_sfc v-if="node.expanded && !node.dragged" 
                            class="grow" :parent_id="node.id" :nodes="node.children" :depth="depth+1" :detached_parent="false"
                            @toggle_expand="toggle_expand" 
                            @dragstart_card="dragstart_card" 
                            @dragover_card="dragover_card"/>
                </div>
            </template>            
        </div>
    </div>
</template>



<script>
export default {
    // @dragend="(evt) => dragend(node, evt)"
    data() {
        return {
            parent_id: this.parent_id,
            nodes: this.nodes,
            depth: this.depth,
            detached_parent: this.detached_parent
        }
    },
    methods: {
        list_entries() {
            return this.nodes
        },
        node_key(node) {
            return this.depth+"-"+this.parent_id+"-"+node.id+"-"+this.detached_parent+"-"+node.card.detached
        },
        node_is_detached(node) {
            return node.card.detached && this.depth>0 && !this.detached_parent
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
                return "ml-10 h-5 grow mt-2"
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
            return !node.dragged || this.node_is_detached(node)
            // return (this.dragged.entry == null || this.dragged.entry.id != card.id);
        },
        toggle_expand(node) {
            this.$emit("toggle_expand", node)
        },
        dragover(node, evt) {
            // console.log("over", node, evt);
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
            if (node.id == parent_id) {
                // direct parent, do not create an event
                evt.stopPropagation()
                return
            }
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
            // console.log("over parent id", parent_id, this.parent_id, drag_data)
            this.dragover_card(node.id, node_ids, evt.x, evt.y)
        },
        dragstart(node, evt) {
            evt.dataTransfer.clearData()
            let drag_data = {parent_id: node.parent == null ? null : node.parent.id, node_ids: [node.id]}
            // console.log("set drag data", drag_data)
            evt.dataTransfer.setData("application/json", JSON.stringify(drag_data))
            // TODO: set task url
            evt.stopPropagation()
            this.dragstart_card([node.id], evt.x, evt.y)          
        },
        dragover_card(target_node_id, node_ids,x, y) {
            this.$emit("dragover_card", target_node_id, node_ids,x,y)
        },
        dragstart_card(node_ids,x,y) {
            this.$emit("dragstart_card", node_ids,x,y)
        },
    },
    props: {
        parent_id: null,
        nodes: null,
        depth: 0,
        detached_parent: false,
    }
}
</script>

