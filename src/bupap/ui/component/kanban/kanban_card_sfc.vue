<template>
    <q-card ref="card" class="nicegui-card" flat="this.detached" :bordered="this.detached" :class="classes()" @click="open_link(card)">
        <div class="text-base font-bold select-none">{{card.title}}</div>
        <div v-if="!this.detached" class="nicegui-row">
            <q-badge v-for="tag in card.tags" :key="card.id+tag.text+tag.color" :color="tag.color" :text-color="tag.text_color" class="p-1 m-1 select-none">{{tag.text}}</q-badge>
        </div>
    </q-card>
</template>


<script>
export default {
    data() {
        return {
            card: this.card,
            detached: this.detached,
            dragged: this.dragged
        }
    },
    mounted() {
        this.check_dragged()
    },
    updated() {
        this.check_dragged()
    },
    methods: {
        check_dragged() {
            if (this.dragged) {
                let ref = this.$refs["card"]
                if (ref != null) {
                    ref = ref._.subTree.el
                    this.$emit("dragging_ref", ref)
                }
            }
        },
        open_link(val) {
            console.log(val);
        },
        classes() {
            if (this.detached) {
                var result = ["text-gray-400", "bg-gray-100", "border-dashed", "pt-2", "pb-2", "mt-0.5"]
            }
            else {
                var result = ["hover:bg-slate-200", "cursor-pointer"] 
            }
            return result
        }
    },
    props: {
        card: null,
        detached: false,
        dragged: false
    }
}
</script>