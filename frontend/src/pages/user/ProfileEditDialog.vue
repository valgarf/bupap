<template>
  <q-dialog ref="dialog" v-model="value">
    <q-card v-if="!loading && user != null && !error" class="dialog-card">
      <q-card-section>
        <AvatarEdit v-model="user.avatar" />
      </q-card-section>
      <q-card-section>
        <q-input
          label="Username"
          outline
          class="full-width"
          v-model="user.name"
        />
        <q-input
          label="Display Name"
          outline
          class="full-width"
          v-model="user.fullName"
        />
      </q-card-section>
      <q-card-actions>
        <q-btn
          label="Save"
          color="primary"
          class="col-grow"
          :loading="saving"
          @click="save"
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
<style scoped lang="scss">
.dialog-card {
  width: min(100vw, 576px);
  max-width: min(100vw, 576px);
}
</style>

<script setup>
import { defineEmits, defineProps, computed, ref, watchEffect } from 'vue';
import { useQuery, useMutation } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import QueryStatus from 'components/QueryStatus.vue';
import AvatarEdit from 'components/AvatarEdit.vue';

const props = defineProps({
  modelValue: Boolean,
  userId: Number,
});
const emit = defineEmits(['update:modelValue', 'success']);
const dialog = ref(null);
const user = ref(null);

const { result, loading, error } = useQuery(
  gql`
    query user($userId: Int!) {
      user: dbNode(typename: "User", dbId: $userId) {
        ... on User {
          name
          fullName
          avatar {
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
    }
  `,
  { userId: props.userId },
  { enabled: computed(() => props.userId != null) }
);

watchEffect(() => {
  if (props.userId == null) {
    user.value = { name: '', fullName: '', avatar: null };
  } else if (result.value != null) {
    user.value = {
      name: result.value.user.name,
      fullName: result.value.user.fullName,
      avatar: { ...result.value.user.avatar },
    };
  }
  return null;
});

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});

const {
  mutate,
  onDone,
  loading: saving,
} = useMutation(
  gql`
    mutation saveUser($userId: Int!, $user: UserInput!) {
      user {
        update(userId: $userId, user: $user) {
          success
        }
      }
    }
  `,
  { userId: props.userId }
);

function save() {
  onDone(() => {
    emit('success');
    dialog.value.hide();
  });
  mutate({
    userId: props.userId,
    user: {
      name: user.value.name,
      fullName: user.value.fullName,
      avatar: {
        top: user.value.avatar.top.name,
        accessory: user.value.avatar.accessory.name,
        eyebrows: user.value.avatar.eyebrows.name,
        eyes: user.value.avatar.eyes.name,
        nose: user.value.avatar.nose.name,
        mouth: user.value.avatar.mouth.name,
        beard: user.value.avatar.beard.name,
        clothing: user.value.avatar.clothing.name,
        graphic: user.value.avatar.graphic.name,
        skinColor: user.value.avatar.skinColor,
        hairColor: user.value.avatar.hairColor,
        beardColor: user.value.avatar.beardColor,
        hatColor: user.value.avatar.hatColor,
        clothingColor: user.value.avatar.clothingColor,
        backgroundColor: user.value.avatar.backgroundColor,
        shirtText: user.value.avatar.shirtText,
      },
    },
  });
}
</script>
