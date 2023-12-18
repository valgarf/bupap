<template>
    <div :class="column_classes()">
        <div v-for="node in list_entries()" 
                :class="card_div_classes(node)" :key="node_key(node)" 
                @dragstart="(evt) => dragstart(node, evt)">
            <template v-if="node.card.detached && this.depth==0">
                <nicegui-kanban_card_sfc 
                        class="mt-0" :class="card_classes(node.parent)" :card="node.parent.card" 
                        :detached="true" :dragged="false" :priorities="this.priorities"
                        @open_link="open_link"/>
                <div class="nicegui-row items-stretch gap-0 mt-[-3pt]">
                    <div class="w-10" ></div>
                    <nicegui-kanban_list_sfc 
                            class="grow" :parent_id="node.parent.id" :nodes="[node]" 
                            :depth="depth+1" :detached_parent="true" :priorities="this.priorities"
                            @toggle_expand="toggle_expand" 
                            @dragging_ref="dragging_ref"
                            @dragstart_card="dragstart_card"
                            @open_link="open_link" />
                </div>
            </template>
            <template v-else>
                <nicegui-kanban_card_sfc 
                        :draggable="!node_is_detached(node)" :class="card_classes(node)" 
                        :card="node.card" :detached="node_is_detached(node)" 
                        :dragged="node_is_drag_target(node)" :priorities="this.priorities"
                        @dragging_ref="dragging_ref" @open_link="open_link"/>
                <div v-if="node.children.length>0 && !(node.card.detached && this.depth>0 &&!this.detached_parent)" class="nicegui-row items-stretch gap-0 mt-[-3pt]">
                    <q-btn :class="toggle_btn_classes(node)" @click="(evt)=>toggle_expand(node)">{{toggle_btn_text(node)}}</q-btn>
                    <nicegui-kanban_list_sfc v-if="node.expanded && !node.dragged" 
                            class="grow" :parent_id="node.id" :nodes="node.children" 
                            :depth="depth+1" :detached_parent="false" :priorities="this.priorities"
                            @toggle_expand="toggle_expand" 
                            @dragging_ref="dragging_ref"
                            @dragstart_card="dragstart_card"
                            @open_link="open_link"/>
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
            detached_parent: this.detached_parent,
            priorities: this.priorities
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
        node_is_drag_target(node) {
            return node.dragged && !this.node_is_detached(node)
        },
        // open_link(val) {
        //     console.log(val);
        // },
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
        dragstart(node, evt) {
            evt.dataTransfer.clearData()
            let drag_data = {parent_id: node.parent == null ? null : node.parent.id, node_ids: [node.id]}
            evt.dataTransfer.setData("application/json", JSON.stringify(drag_data))
            // TODO: set task url
            evt.stopPropagation()
            this.dragstart_card([node.id], evt.x, evt.y)          
        },
        dragstart_card(node_ids,x,y) {
            this.$emit("dragstart_card", node_ids,x,y)
        },
        dragging_ref(ref) {
            this.$emit("dragging_ref", ref)
        },
        open_link(val) {
            this.$emit("open_link", val)
        }
    },
    props: {
        parent_id: null,
        nodes: null,
        depth: 0,
        detached_parent: false,
        priorities: null
    }
}
</script>

