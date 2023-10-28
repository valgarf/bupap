<template>
    <q-card class="nicegui-card" :flat="this.detached" :bordered="this.detached" :class="classes()" @click="open_link(card)">
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
            detached: this.detached
        }
    },
    methods: {
        open_link(val) {
            console.log(val);
        },
        classes() {
            if (this.detached) {
                return ["text-gray-400", "bg-gray-100", "border-dashed", "pt-2", "pb-2", "mt-0.5"]
            }
            else {
               return ["hover:bg-slate-200", "cursor-pointer"] 
            }
        }
    },
    props: {
        card: null,
        detached: false
    }
}
</script>