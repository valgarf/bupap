<template>
  <div class="column items-center fulll-width" v-if="renderInput != null">
    <!-- Avatar Image -->
    <div class="rendered q-mb-xl">
      <q-spinner v-if="renderedSvg == null" />
      <div v-else v-html="renderedSvg" />
    </div>
    <!-- Randomize Button -->
    <q-btn
      label="random"
      color="primary"
      @click="loadRandom() || refetchRandom()"
    />
    <!-- Part Selection  -->
    <div v-if="partDict != null" class="row q-mt-lg q-gutter-md items-center">
      <q-btn
        v-for="part in Object.keys(partDict)"
        :key="'btn-' + part"
        color="secondary"
        class="q-pa-sm"
        :disable="
          part == 'graphic' && renderInput['clothing'] != 'GRAPHIC_SHIRT'
        "
      >
        <div
          v-html="partDict[part][renderInput[part]] || 'None'"
          class="part-button column justify-center"
          @click="openDialog[part] = true"
        />
      </q-btn>
      <q-input
        v-model="shirtText"
        label="Shirt Text"
        class="part-input"
        debounce="250"
        :disable="
          renderInput['graphic'] != 'CUSTOM_TEXT' ||
          renderInput['clothing'] != 'GRAPHIC_SHIRT'
        "
      />
      <q-dialog
        v-for="part in Object.keys(partDict)"
        :key="'dialog-' + part"
        v-model="openDialog[part]"
      >
        <q-card class="part-card">
          <q-card-section class="q-gutter-md">
            <q-btn
              v-for="pkey in Object.keys(partDict[part])"
              :key="part + '-' + pkey"
              class="q-pa-sm"
              color="secondary"
              v-close-popup
              @click="updateRenderInput(part, pkey)"
            >
              <div
                v-html="partDict[part][pkey] || 'None'"
                class="part-button column justify-center"
              />
            </q-btn>
          </q-card-section>
        </q-card>
      </q-dialog>
    </div>
    <!-- Part Color Selection -->
    <div
      v-if="partDict != null"
      class="row q-mt-lg q-gutter-sm items-center justify-stretch"
    >
      <q-btn
        v-for="colPart in [
          'skin',
          'hair',
          'beard',
          'hat',
          'clothing',
          'background',
        ]"
        :key="colPart"
        :label="colPart"
        class="q-px-md col-grow"
        :style="{
          backgroundColor: renderInput[colPart + 'Color'],
          color: textColorFromBackground(renderInput[colPart + 'Color']),
        }"
      >
        <q-popup-proxy>
          <q-color
            :model-value="renderInput[colPart + 'Color']"
            @change="(val) => updateRenderInput(colPart + 'Color', val)"
            style="max-width: 250px"
          />
        </q-popup-proxy>
      </q-btn>
    </div>
    <query-status :loading="loadingParts" :error="errorParts" />
  </div>
</template>

<style lang="scss" scoped>
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
.part-card {
  width: min(100vw, 800px);
  max-width: min(100vw, 800px);
}
.part-input {
  width: 96px;
}
</style>
<script setup>
import { defineEmits, defineProps, computed, ref, watchEffect } from 'vue';
import { useQuery, useLazyQuery } from '@vue/apollo-composable';
import { gql } from '@apollo/client/core';
import QueryStatus from 'components/QueryStatus.vue';
import { lastNonNull, textColorFromBackground } from 'src/common/helper';

const props = defineProps(['modelValue']);
const emit = defineEmits(['update:modelValue']);
const openDialog = ref({});

const value = computed({
  get() {
    return props.modelValue;
  },
  set(value) {
    emit('update:modelValue', value);
  },
});

const renderInput = computed({
  get() {
    if (value.value == null) {
      return null;
    }
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
  },
  set(newValue) {
    value.value = Object.assign(value.value, {
      top: { name: newValue.top },
      accessory: { name: newValue.accessory },
      eyebrows: { name: newValue.eyebrows },
      eyes: { name: newValue.eyes },
      nose: { name: newValue.nose },
      mouth: { name: newValue.mouth },
      beard: { name: newValue.beard },
      clothing: { name: newValue.clothing },
      graphic: { name: newValue.graphic },
      skinColor: newValue.skinColor,
      hairColor: newValue.hairColor,
      beardColor: newValue.beardColor,
      hatColor: newValue.hatColor,
      clothingColor: newValue.clothingColor,
      backgroundColor: newValue.backgroundColor,
      shirtText: newValue.shirtText,
    });
  },
});

const shirtText = computed({
  get() {
    return renderInput.value?.shirtText;
  },
  set(newValue) {
    updateRenderInput('shirtText', newValue);
  },
});
const {
  result: resultRenderedDirect,
  // loading: loadingRendered,
  // error: errorRendered,
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
  },
  {
    enabled: computed(() => renderInput.value != null),
  }
);
const resultRendered = lastNonNull(resultRenderedDirect);

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
        accessories {
          ...avatarPart
        }
        eyebrows {
          ...avatarPart
        }
        eyes {
          ...avatarPart
        }
        noses {
          ...avatarPart
        }
        mouths {
          ...avatarPart
        }
        beards {
          ...avatarPart
        }
        clothings {
          ...avatarPart
        }
        graphics {
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

function updateRenderInput(key, value) {
  renderInput.value = Object.assign(renderInput.value, { [key]: value });
}
const partDict = computed(() => {
  if (resultParts.value == null) {
    return null;
  }
  return {
    top: partListtoDict(resultParts.value.avatarApi.tops),
    accessory: partListtoDict(resultParts.value.avatarApi.accessories),
    eyebrows: partListtoDict(resultParts.value.avatarApi.eyebrows),
    eyes: partListtoDict(resultParts.value.avatarApi.eyes),
    nose: partListtoDict(resultParts.value.avatarApi.noses),
    mouth: partListtoDict(resultParts.value.avatarApi.mouths),
    beard: partListtoDict(resultParts.value.avatarApi.beards),
    clothing: partListtoDict(resultParts.value.avatarApi.clothings),
    graphic: partListtoDict(resultParts.value.avatarApi.graphics),
  };
});

const {
  onResult: onResultRandom,
  load: loadRandom,
  refetch: refetchRandom,
  // loading: loadingRandom,
  // error: errorRandom,
} = useLazyQuery(
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
);
onResultRandom((newValue) => {
  value.value = newValue.data.avatarApi.random;
});

watchEffect(() => {
  if (props.modelValue == null) {
    loadRandom() || refetchRandom();
  }
});
</script>
