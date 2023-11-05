<template>
    <div class="nicegui-row p-4 overflow-x-auto grow flex-nowrap items-stretch" @drop="drop" @dragover.prevent="(evt)=>{}">
        <q-card v-for="lane in this.kanban.lane_order" 
                :key="lane.id" class="nicegui-card min-w-[350pt] items-stretch"
                @dragover.prevent="(evt) => dragover(lane, evt)">
            <div class="font-bold text-xl mt-5">{{lane.title}}</div>
            <q-scroll-area class="m-0 p-0 pr-2 max-w-[330] grow">
                <div class="p-2">
                    <nicegui-kanban_list_sfc 
                            :parent_id="null" :nodes="lane.top_level_nodes" :depth="0" :detached_parent="false"
                            @toggle_expand="toggle_expand" 
                            @dragging_ref="dragging_ref"
                            @dragstart_card="dragstart_card" 
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
        let kanban = this.compute_kanban(this.initial_data)
        console.log(kanban)
        return {
            kanban: kanban,
            nodes: kanban.nodes,
            dragged: {x:0,y:0, target:null, count: 0, ref: null, blocked: false, nodes: []},
        }
    },
    // updated() {
    //     if (this.dragged.ref != null) {
    //         console.log(this.dragged.ref.getBoundingClientRect());
    //     }
    // },
    methods: {
        // open_link(val) {
        //     console.log(val);
        // },

        compute_kanban(initial_data) {
            let nodes = {}
            for (let [k, v] of Object.entries(initial_data.cards)) {
                let intk = parseInt(k)
                nodes[intk] = {parent: null, children: [], id: intk, card: v, expanded: true, dragged: false, _lane: null,
                    get lane() {return this.top_level? this._lane : this.parent.lane},
                    set lane(value) {
                        if (this.detached || this.parent == null) {
                            this._lane = value;
                        } else {
                            if (value.id != this.lane.id) {
                                console.error("Setter called with unexpected lane.", this, this.lane, value);
                            }
                        }
                    },
                    get top_level() {return this.detached || this.parent==null},
                    get detached() {return this.card.detached}, 
                    set detached(value) {this.card.detached = value},
                    recursive_children(attached_only) {
                        let result = []
                        for (let c of this.children) {
                            if (!attached_only || !c.detached) {
                                result.push(c, ...c.recursive_children(attached_only))
                            }
                        }
                        return result;
                    },
                    get recursive_parents() {
                        let result = []
                        let p = this.parent
                        while (p!=null) {
                            result.push(p)
                            p = p.parent
                        }
                        return result
                    },
                    get recursive_parent_ids() {
                        return this.recursive_parents.map((p) => p.id)
                    }
                }
            }

            // console.log(nodes)

            for (let n of Object.values(nodes)) {
                n.children = n.card.children_order.map((cid) => nodes[cid])
                let p = nodes[n.card.parent_id]
                if (p!= undefined) {
                    n.parent = p
                }
            }

            let lanes = {}
            for (let [k,v] of Object.entries(initial_data.lanes)) {
                let all_nodes = v.card_order.map((cid) => nodes[cid])

                let lane = {id: v.id, title: v.title, top_level_nodes: [],
                    get nodes() {
                        let result = []
                        for (let n of this.top_level_nodes) {
                            result.push(n, ...n.recursive_children(true))
                        }
                        return result
                    },
                    top_level_nodes: all_nodes.filter((n) => {return n.detached || n.parent == null})
                }
                lanes[k] = lane
                for (let node of lane.top_level_nodes) {
                    node._lane = lane
                }
            }

            let lane_order = this.initial_data.lane_order.map((lid) => lanes[lid])

            return {nodes, lanes, lane_order}
        },
        toggle_expand(node) {
            var n = this.nodes[node.id]
            n.expanded = !n.expanded
        },
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

        dragover(lane, evt) {
            if (this.dragged.blocked) {
                return
            }
            let x = evt.y
            let y = evt.y
            let down = y > this.dragged.y // movement direction is down
            let up = !down && (y < this.dragged.y || this.dragged.nodes.some((node) => node.lane.id !== lane.id)) // movement direction is up
            console.log(y, this.dragged.y, up, down, this.dragged.nodes, evt)
            this.dragged.x = x
            this.dragged.y = y 
            if (!up && !down) {
                return
            }
            for (let node of this.dragged.nodes) {
                if (up) {
                    this.move_up(node, y);
                }
                if (down) {
                    this.move_down(node, y);
                }
            }
        },
        move_up(node, y) {
            this.dragged.blocked = false;

            if (this.dragged.ref.getBoundingClientRect().top <= y){
                // above mouse, stop movement
                return
            }

            if (node.top_level) {
                let index = node.lane.top_level_nodes.indexOf(node)
                if (index == 0) {
                    // top of list
                    return
                }
                let node_above = node.lane.top_level_nodes[index-1]
                node.lane.top_level_nodes.splice(index, 1)
                if (node.recursive_parent_ids.includes(node_above.id) && node.recursive_parents.every((n) => n.expanded)) {
                    // move into parent
                    node.lane = null
                    node.detached = false
                    let index = node.parent.children.indexOf(node)
                    node.parent.children.splice(index, 1)
                    node.parent.children.push(node)
                }
                else {
                    // switch with node above
                    node.lane.top_level_nodes.splice(index-1, 0, node)
                }
            }
            else {
                let index = node.parent.children.indexOf(node)
                if (index > 0) {
                    // switch with node above
                    node.parent.children.splice(index, 1)
                    node.parent.children.splice(index-1, 0, node)
                }
                else {
                    // top of list, put above parent node
                    let lane = node.lane
                    let index = node.lane.top_level_nodes.indexOf(node.recursive_parents.at(-1))
                    if (index == -1) {
                        console.error("could not determine node's root parent index", node, node.recursive_parents.at(-1), node.lane.top_level_nodes)
                        return
                    }
                    lane.top_level_nodes.splice(index-1, 0, node)
                    node.detached = true
                    node.lane = lane
                }
            }
            
            this.dragged.blocked = true;
            this.$nextTick(() => {
                this.$nextTick(() => {
                    this.move_up(node, y)
                })
            })
        },
        move_down(node, y) {
            this.dragged.blocked = false;
            
            if (this.dragged.ref.getBoundingClientRect().bottom >= y){
                // below mouse, stop movement
                return
            }

            if (node.top_level) {
                let index = node.lane.top_level_nodes.indexOf(node)
                if (index + 1 ==  node.lane.top_level_nodes.length) {
                    // bottom of list
                    return
                }
                let node_below = node.lane.top_level_nodes[index+1]
                node.lane.top_level_nodes.splice(index, 1)
                if (node.recursive_parent_ids.includes(node_below.id) && node.recursive_parents.every((n) => n.expanded)) {
                    // move into parent
                    node.lane = null
                    node.detached = false
                    let index = node.parent.children.indexOf(node)
                    node.parent.children.splice(index, 1)
                    node.parent.children.splice(0, 0, node)
                }
                else {
                    // switch with node below
                    node.lane.top_level_nodes.splice(index+1, 0, node)
                }
            }
            else {
                let index = node.parent.children.indexOf(node)
                if (index + 1 < node.parent.children.length) {
                    // switch with node below
                    node.parent.children.splice(index, 1)
                    node.parent.children.splice(index+1, 0, node)
                }
                else {
                    // bottom of list, put below parent node
                    let lane = node.lane
                    let index = lane.top_level_nodes.indexOf(node.recursive_parents.at(-1))
                    if (index == -1) {
                        console.error("could not determine node's root parent index", node, node.recursive_parents.at(-1), node.lane.top_level_nodes)
                        return
                    }
                    lane.top_level_nodes.splice(index+1, 0, node)
                    node.detached = true
                    node.lane = lane
                }
            }
            
            this.dragged.blocked = true;
            this.$nextTick(() => {
                this.$nextTick(() => {
                    this.move_down(node, y)
                })
            })
        },
        dragover_card(target_node_id, node_ids, x, y) {
            // let target_node = this.nodes[target_node_id]
            // // if (this.dragged.target != null && this.dragged.target.id == target_node_id) {
            // //     // console.log("enter identical", this.dragged.target, this.dragged.target.count, target_node_id)
            // //     this.dragged.count += 1
            // //     return
            // // }
            // // else {
            // //     // console.log("enter other", this.dragged.target, this.dragged.target == null ? null : this.dragged.target.count, target_node_id)
            // //     this.dragged.target = target_node
            // //     this.dragged.count = 0
            // // }
            // this.$nextTick(() => {
            //     if (this.dragged.ref != null) {
            //         console.log("before", this.dragged.ref.getBoundingClientRect());
            //     }
            //     this.$nextTick(() => {
            //         if (this.dragged.ref != null) {
            //             console.log("after", this.dragged.ref.getBoundingClientRect());
            //         }
            //     })
            // })
            // let change = false
            // let nodes = node_ids.map((nid) => this.nodes[nid])
            // let target_lane = target_node.lane
            // for (let dragged_node of nodes) {
            //     let is_same_parent = target_node.parent == dragged_node.parent && target_node.parent != null
            //     let orig_lane = dragged_node.lane
            //     let orig_list = is_same_parent ? target_node.parent.children : dragged_node.top_level ? orig_lane.top_level_nodes : null
            //     let dragged_idx = orig_list?.indexOf(dragged_node)
            //     if (dragged_idx == -1) {
            //         console.error("Could not determine dragging source idx for parent", dragged_node.parent, "and child", dragged_node, "info:", {is_same_parent: is_same_parent, orig_lane: orig_lane, target_lane: target_lane, target_node: target_node})
            //         continue
            //     }

            //     let target_list = is_same_parent ? target_node.parent.children : target_lane.top_level_nodes
            //     let target_idx = target_list.indexOf(target_node)
            //     if (target_idx == -1) {
            //         console.error("Could not determine dragging target idx for parent", target_node.parent, "and child", target_node, "info:", {is_same_parent: is_same_parent, orig_lane: orig_lane, target_lane: target_lane, target_node: target_node})
            //         return
            //     }

            //     let down = y > this.dragged.y // movement direction is down
            //     let up = !down && (y < this.dragged.y || orig_lane !== target_lane) // movement direction is up
            //     if (!up && !down) {
            //         // no movement
            //         continue
            //     }
            //     if (orig_list == target_list) {
            //         if ((up && target_idx == dragged_idx + 1) || (down && target_idx == dragged_idx - 1)) {
            //             continue // would not move
            //         }
            //         if (dragged_idx <= target_idx) {
            //             // we remove before inserting, we need to fix the target idx
            //             // console.log("updated target idx (same list):", target_idx, target_idx-1)
            //             target_idx -= 1
            //         }
            //     }
            //     change = true
            //     // console.log("drag op:", up? "up" : "down", dragged_idx, down ? target_idx+1: target_idx, "info:", {is_same_parent: is_same_parent, orig_lane: orig_lane, target_lane: target_lane, target_node: target_node})
            //     if (dragged_idx != null) {
            //         orig_list.splice(dragged_idx, 1) // remove from original position
            //     }
            //     if (down) {
            //         target_idx += 1 // next node should be inserted below
            //     }
            //     target_list.splice(target_idx, 0, dragged_node)
            //     if (dragged_node.parent != null) {
            //         dragged_node.detached = (target_node.parent == null)
            //     }
            //     if (!is_same_parent) {
            //         // we might have changed the lane here, update the card's lane_id
            //         dragged_node.lane = target_node.lane
            //     }
            // }
            // // TODO: if change, emit event

            // this.dragged.x = x
            // this.dragged.y = y 
                       
        },
        dragstart_card(node_ids, x, y) {
            this.dragged.x = x
            this.dragged.y = y
            this.dragged.nodes = node_ids.map((nid) => this.nodes[nid])
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
        drop(evt) {
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
            let node_ids = drag_data["node_ids"]
            evt.stopPropagation()
            for (let node_id of node_ids) {
                this.nodes[node_id].dragged = false
            }
            this.dragged.nodes = []
            this.dragged.ref = null
        },
        dragging_ref(ref) {
            this.dragged.ref = ref
            console.log("new ref:", this.dragged.ref.getBoundingClientRect())
        }
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