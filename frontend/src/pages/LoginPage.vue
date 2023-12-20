<template>
    <div class="row absolute-center text-subtitle1">
        <q-card>
            <q-card-section>
                <q-input label="Username" class="full-width q-mb-md" v-model="name"/>
                <q-input password label="Password" class="full-width q-mb-md" v-model="password" :type="isPwd ? 'password' : 'text'" @keydown.enter="login">
                    <template v-slot:append>
                        <q-icon
                            :name="isPwd ? 'visibility_off' : 'visibility'"
                            class="cursor-pointer"
                            @click="isPwd = !isPwd"
                        />
                    </template>
                </q-input>
                <div class="row justify-center full-width q-mt-md">
                    <q-btn color="primary" label="Login" @click="login"/>
                </div>
            </q-card-section>
        </q-card>
    </div>
</template>

<script setup>
import {useActiveUserStore} from 'src/stores/active-user'
import {ref, watchEffect} from 'vue'
import { useRouter } from 'vue-router'

const user = useActiveUserStore()
const name = ref('')
const password = ref('')
const isPwd = ref(true)
const router = useRouter()
function login() {
  user.login(name, password)
}
watchEffect(() => {
    if (user.name != null) {
        router.push("/")
    }
})
</script>