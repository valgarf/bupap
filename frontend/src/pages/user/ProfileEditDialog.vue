<template>
  <q-dialog ref="dialog" v-model="value">
    <q-card v-if="!loading && !error">
      <q-card-section v-if="localUser.avatar != null">
        <AvatarEdit v-model="localUser.avatar" />
      </q-card-section>
      <q-card-section>
        <q-input
          label="Username"
          outline
          class="full-width"
          v-model="localUser.name"
        />
        <q-input
          label="Display Name"
          outline
          class="full-width"
          v-model="localUser.fullName"
        />
      </q-card-section>
      <q-card-actions>
        <q-btn
          label="Save"
          color="primary"
          class="col-grow"
          :loading="saving"
        />
        <q-btn
          label="Cancel"
          color="negative"
          class="col-grow"
          @click="dialog.hide"
        />
      </q-card-actions>
    </q-card>
    <q-card v-else>
      <query-status :loading="loading" :error="error" />
    </q-card>
  </q-dialog>
</template>

<script setup>
import { defineEmits, defineProps, computed, ref, watchEffect } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import QueryStatus from 'components/QueryStatus.vue';
import AvatarEdit from 'components/AvatarEdit.vue';

const props = defineProps({
  modelValue: Boolean,
  user: { default: { name: '', fullName: '', avatar: null } },
});
const emit = defineEmits(['update:modelValue']);
const localUser = ref(props.user);
const dialog = ref(null);
const saving = ref(false);
const { result, loading, error } =
  localUser.value.avatar == null
    ? useQuery(
        gql`
          query randomAvatar {
            avatarApi {
              random {
                top {
                  name
                }
                accessory {
                  name
                }
                eyebrows {
                  name
                }
                eyes {
                  name
                }
                nose {
                  name
                }
                mouth {
                  name
                }
                beard {
                  name
                }
                clothing {
                  name
                }
                graphic {
                  name
                }
                skinColor
                hairColor
                beardColor
                hatColor
                clothingColor
                backgroundColor
                shirtText
              }
            }
          }
        `,
        null,
        { fetchPolicy: 'no-cache' }
      )
    : { result: { value: null }, loading: false, error: null };

watchEffect(() => {
  if (result.value?.avatarApi?.random != null) {
    localUser.value.avatar = result.value.avatarApi.random;
  }
});

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});
</script>
