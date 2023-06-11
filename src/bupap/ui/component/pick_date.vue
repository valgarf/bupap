<template>
    <div class="q-pa-md" style="max-width: 300px">
    <q-input filled v-model="date" mask="####-##-##" :rules="[validate]" v-on:change="changed" class="p-0">
        <template v-slot:append>
        <q-icon name="event" class="cursor-pointer">
            <q-popup-proxy cover transition-show="scale" transition-hide="scale" v-on:hide="changed">
                <q-date v-model="date" mask="YYYY-MM-DD">
                    <div class="row items-center justify-end">
                        <q-btn v-close-popup label="Close" color="primary" flat />
                    </div>
                </q-date>
            </q-popup-proxy>
        </q-icon>
        </template>
    </q-input>
    </div>
</template>


<script>
export default {
  data() {
    return {
        date: this.initial,
        last_sent: this.initial
    }
  },
  methods: {
    validate(val) {
        return !isNaN((new Date(this.date)).valueOf())
    },
    update_date(val, emit) {
        this.date = val
        if (emit) {
            this.changed()
        }
    },
    changed(_) {
        if (this.date != this.last_sent && this.validate(this.date)) {
            this.last_sent = this.date
            this.$emit("changed",this.last_sent)
        }
    }
  },
  props: {
    initial: String,
  },
}
</script>