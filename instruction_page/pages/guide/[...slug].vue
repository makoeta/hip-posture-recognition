<script lang="ts" setup>
import { useGuidePath } from "~/composables/useGuidePath";

definePageMeta({
  layout: "guide",
});

const route = useRoute();
const usePath = useGuidePath();

const guideData = useAsyncData(() =>
  queryCollection("guide").path(usePath.value).first(),
);

onMounted(() => {
  const oldPath = usePath.value;
  const newPath = route.path;
  usePath.value = route.path;
  if (newPath !== oldPath) {
    guideData.refresh();
    return;
  }
});

const item = computed(() => guideData.data.value);
</script>

<template>
  <div v-if="item">
    <ContentRenderer :key="route.fullPath" :value="item" />
  </div>
</template>
