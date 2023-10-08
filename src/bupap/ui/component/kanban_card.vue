<template>
    <q-card class="nicegui-card hover:bg-slate-200 cursor-pointer" @click="open_link(card)">
        <div class="text-base font-bold select-none">{{card.title}}</div>
        <div class="nicegui-row">
            <q-badge v-for="tag in card.tags" :key="card.id+tag.text+tag.color" :color="tag.color" class="p-1 m-1 select-none">{{tag.text}}</q-badge>
        </div>
    </q-card>
</template>


<script>
export default {
    data() {
        return {
            card: this.card
        }
    },
    methods: {
        open_link(val) {
            console.log(val);
        },
    },
    props: {
        card: null,
    }
}
</script>