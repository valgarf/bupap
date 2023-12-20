<template>
  <q-page class="row items-center justify-evenly">
    <q-card v-if="user.name!=null">
      <q-card-section>
        Hello {{user.fullName}}!
      </q-card-section>
    </q-card>
  </q-page>
</template>

<script setup lang="ts">
import { Todo, Meta } from 'components/models';
import ExampleComponent from 'components/ExampleComponent.vue';
import { ref } from 'vue';
import {useActiveUserStore} from 'src/stores/active-user'

const user = useActiveUserStore()

</script>
