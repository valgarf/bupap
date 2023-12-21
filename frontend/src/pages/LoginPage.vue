<template>
    <div class="row absolute-center text-subtitle1">
        <q-card>
            <q-card-section>
                <q-form @submit="login">
                    <q-input label="Username" class="full-width q-mb-md" v-model="name"/>
                    <q-input password label="Password" class="full-width q-mb-md" v-model="password" :type="isPwd ? 'password' : 'text'">
                        <template v-slot:append>
                            <q-icon
                                :name="isPwd ? 'visibility_off' : 'visibility'"
                                class="cursor-pointer"
                                @click="isPwd = !isPwd"
                            />
                        </template>
                    </q-input>
                    <div class="row justify-center full-width q-mt-md">
                        <q-btn color="primary" type="submit" :loading="user.state==UserState.LOGGING_IN" label="Login"/>
                    </div>
                </q-form>
            </q-card-section>
        </q-card>
    </div>
</template>

<script setup>
import {useActiveUserStore, UserState} from 'src/stores/active-user'
import {ref, watchEffect} from 'vue'
import { useRouter } from 'vue-router'
import {useQuasar} from 'quasar'
const $q = useQuasar()
const user = useActiveUserStore()
const name = ref('')
const password = ref('')
const isPwd = ref(true)
const router = useRouter()
function login() {
    // we need to use a value here, otherwise the query is repeated on every keystroke
    user.login(name.value, password.value)
    watchEffect(() => {
        if (user.lastLoginFailed) {
            // login failed
            $q.notify({
                message: 'Login failed',
                color: 'negative',
                caption: 'Username or password are incorrect',
                actions: [
                    { icon: 'close', round: true, color: 'white', handler: () => { /* ... */ } }
                ]
            })
            user.lastLoginFailed = false
        }
    })
}
watchEffect(() => {
    // reroute if logged in (will also reroute if already logged in)
    if (user.name != null) {
        router.push("/")
    }
})
</script>