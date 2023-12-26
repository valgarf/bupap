<template>
  <div class="column items-center fulll-width">
    <div class="rendered">
      <q-spinner v-if="renderedSvg == null" />
      <div v-else v-html="renderedSvg" />
    </div>
    <div>
      <div v-if="partDict != null" class="row q-mt-lg">
        <q-btn color="secondary">
          <div v-html="partDict.top[renderInput.top]" class="part-button" />
        </q-btn>
      </div>
      <query-status :loading="loadingParts" :error="errorParts" />
    </div>
  </div>
</template>

<style scoped>
.rendered {
  width: 300px;
  height: 300px;
}
.part-button {
  width: 80px;
  height: 80px;
}
.part-button :deep(svg) {
  width: 80px;
  height: 80px;
}
</style>
<script setup>
import { defineEmits, defineProps, computed, ref, watchEffect } from 'vue';
import { useQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import QueryStatus from 'components/QueryStatus.vue';

const props = defineProps(['modelValue']);

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});

const renderInput = computed(() => {
  return {
    top: value.value.top.name,
    accessory: value.value.accessory.name,
    eyebrows: value.value.eyebrows.name,
    eyes: value.value.eyes.name,
    nose: value.value.nose.name,
    mouth: value.value.mouth.name,
    beard: value.value.beard.name,
    clothing: value.value.clothing.name,
    graphic: value.value.graphic.name,
    skinColor: value.value.skinColor,
    hairColor: value.value.hairColor,
    beardColor: value.value.beardColor,
    hatColor: value.value.hatColor,
    clothingColor: value.value.clothingColor,
    backgroundColor: value.value.backgroundColor,
    shirtText: value.value.shirtText,
  };
});
watchEffect(() => {
  console.log(renderInput.value);
});
const {
  result: resultRendered,
  loading: loadingRendered,
  error: errorRendered,
} = useQuery(
  gql`
    query renderedAvatar($avatar: AvatarInput!) {
      avatarApi {
        create(avatar: $avatar) {
          svg
        }
      }
    }
  `,
  {
    avatar: renderInput,
  }
);
const renderedSvg = computed(() => {
  return resultRendered.value?.avatarApi?.create?.svg;
});

const {
  result: resultParts,
  loading: loadingParts,
  error: errorParts,
} = useQuery(
  gql`
    query avatarParts {
      avatarApi {
        tops {
          ...avatarPart
        }
      }
    }
    fragment avatarPart on AvatarPart {
      name
      svg
    }
  `,
  {
    avatar: renderInput,
  }
);

function partListtoDict(pl) {
  return Object.assign({}, ...pl.map((p) => ({ [p.name]: p.svg })));
}

const partDict = computed(() => {
  if (resultParts.value == null) {
    return null;
  }
  return {
    top: partListtoDict(resultParts.value.avatarApi.tops),
  };
});

watchEffect(() => {
  console.log(partDict.value, renderInput.value.top);
  console.log(partDict.value?.[renderInput.value.top]);
});
</script>
