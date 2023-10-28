<template>
    <div class="nicegui-row p-4 overflow-x-auto grow flex-nowrap items-stretch">
        <q-card v-for="lane in lanes()" :key="lane.id" class="nicegui-card min-w-[350pt] items-stretch">
            <div class="font-bold text-xl mt-5">{{lane.title}}</div>
            <q-scroll-area class="m-0 p-0 pr-2 max-w-[330] grow">
                <div class="p-2">
                    <nicegui-kanban_list_sfc 
                            :parent_id="null" :nodes="nodes_lane(lane)" :depth="0" :detached_parent="false"
                            @toggle_expand="toggle_expand" 
                            @dragstart_card="dragstart_card" 
                            @dragend_card="dragend_card" 
                            @dragover_card="dragover_card"/>
                </div>
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
            dragged: {x:0,y:0, target:null, count: 0},
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
                nodes[intk] = {parent: null, children: [], id: intk, card: v, expanded: true, dragged: false}
            }
            this.update_node_hierachy(nodes)
            // console.log(nodes)
            return nodes
        },
        update_node_hierachy(nodes) {
            for (let n of Object.values(nodes)) {
                n.children = n.card.children_order.map((cid) => nodes[cid])
                var p = nodes[n.card.parent_id]
                if (p!= undefined) {
                    n.parent = p
                }
            }
            // for (let n of Object.values(nodes)) {
            //     if (n.parent != null && n.parent.children.indexOf(n) == -1) {
            //         console.error(n, n.parent)
            //     }
            // }
        },
        nodes_lane(lane) {
            let result = lane.card_order.map((cid) => this.nodes[cid]).filter((n) => n!=undefined && n!=null && (n.parent==null || n.card.detached));
            // console.log(lane.id, result)
            return result
        },
        toggle_expand(node) {
            var n = this.nodes[node.id]
            n.expanded = !n.expanded
        },
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
        acceptable_above(orig_card, target_card, target_lane, target_idx) {
            return true
            // return (target_card.parent_id == null || orig_card.parent_id == target_card.parent_id)
        },
        acceptable_below(orig_card, target_card, target_lane, target_idx) {
            return true
            // if (target_lane.card_order.length <= target_idx + 1) {
            //     return true
            // }
            // target_card = this.kanban.cards[target_lane.card_order[target_idx+1]]
            // return this.acceptable_above(orig_card, target_card, target_lane, target_idx+1)
        },

        dragover_card(target_node_id, node_ids, x, y) {
            let target_node = this.nodes[target_node_id]
            // if (this.dragged.target != null && this.dragged.target.id == target_node_id) {
            //     // console.log("enter identical", this.dragged.target, this.dragged.target.count, target_node_id)
            //     this.dragged.count += 1
            //     return
            // }
            // else {
            //     // console.log("enter other", this.dragged.target, this.dragged.target == null ? null : this.dragged.target.count, target_node_id)
            //     this.dragged.target = target_node
            //     this.dragged.count = 0
            // }
            let change = false
            let nodes = node_ids.map((nid) => this.nodes[nid])
            let target_lane = this.kanban.lanes[target_node.card.lane_id]
            for (let dragged_node of nodes) {
                let is_same_parent = target_node.parent == dragged_node.parent && target_node.parent != null
                let orig_lane = this.kanban.lanes[dragged_node.card.lane_id]
                let orig_list = is_same_parent ? target_node.parent.card.children_order : orig_lane.card_order
                let dragged_idx = orig_list.indexOf(dragged_node.id)
                if (dragged_idx == -1) {
                    console.error("Could not determine dragging target idx for parent", dragged_node.parent, "and child", dragged_node)
                    continue
                }

                let target_list = is_same_parent ? target_node.parent.card.children_order : target_lane.card_order
                let target_idx = target_list.indexOf(target_node.id)
                if (target_idx == -1) {
                    console.error("Could not determine dragging target idx for parent", target_node.parent, "and child", target_node)
                    return
                }

                let down = y > this.dragged.y // movement direction is down
                let up = !down && (y < this.dragged.y || orig_lane !== target_lane) // movement direction is up
                if (!up && !down) {
                    // no movement
                    continue
                }
                if (orig_list == target_list) {
                    if ((up && target_idx == dragged_idx + 1) || (down && target_idx == dragged_idx - 1)) {
                        continue // would not move
                    }
                    if (dragged_idx <= target_idx) {
                        // we remove before inserting, we need to fix the target idx
                        // console.log("updated target idx (same list):", target_idx, target_idx-1)
                        target_idx -= 1
                    }
                }
                change = true
                // console.log("drag op:", up? "up" : "down", dragged_idx, down ? target_idx+1: target_idx, "orig parent", dragged_node.parent, "new parent", target_node.parent)
                orig_list.splice(dragged_idx, 1) // remove from original position
                if (down) {
                    target_idx += 1 // next node should be inserted below
                }
                target_list.splice(target_idx, 0, dragged_node.id)
                if (dragged_node.card.parent_id != null) {
                    dragged_node.card.detached = (target_node.parent == null)
                }

                // if (orig_list === target_list && dragged_idx <= target_idx) {
                //     // we removed one from 
                // }
                // if (y > this.dragged.y) {
                    
                //     // dragging down (insert after)
                // }
                // else if (y < this.dragged.y) {
                //     // dragging up or lane change without y change (insert before) 
                // }

                // if (orig_lane == target_lane && nodes.length == 1) {
                //     let lane = orig_lane
                    
                //     if (dragged_idx>target_idx && y<this.dragged.y && this.acceptable_above(dragged_node, target_node, lane, target_idx)) {
                //         lane.card_order.splice(dragged_idx, 1)
                //         lane.card_order.splice(target_idx, 0, dragged_node.id)
                //         console.log(dragged_node, "up", dragged_idx, target_idx);
                //     }
                //     else if (dragged_idx<target_idx && y>this.dragged.y && this.acceptable_below(dragged_node, target_node, lane, target_idx)) {
                //         lane.card_order.splice(target_idx+1, 0, dragged_node.id)
                //         lane.card_order.splice(dragged_idx, 1)

                //         console.log(dragged_node, "down", dragged_idx, target_idx);
                //     }
                // }
            }
            // TODO: if change, emit event
            if (change) {
                this.update_node_hierachy(this.nodes)
            }
            this.dragged.x = x
            this.dragged.y = y 
                       
        },
        dragstart_card(node_ids, x, y) {
            this.dragged.x = x
            this.dragged.y = y
            var self = this
            // Note: setting the dragged entry will set it to invisible and it will not be shown 
            // during the drag operation. Delaying the invisibility by one frame will generate a 
            // drag image and then hide the original card.
            window.requestAnimationFrame(function() {
                for (let node_id of node_ids) {
                    self.nodes[node_id].dragged = true
                }
            });
        },
        dragleave_card(target_node_id) {
            // if (this.dragged.target != null && this.dragged.target.id == target_node_id) {
            //     // console.log("leave", this.dragged.target, this.dragged.target == null ? null : this.dragged.target.count, target_node_id)
            //     this.dragged.count -= 1
            //     if (this.dragged.count <= 0) {
            //         this.dragged.target = null
            //     }
            //     return
            // }
        },
        dragend_card(node_ids) {
            for (let node_id of node_ids) {
                this.nodes[node_id].dragged = false
            }
        },
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