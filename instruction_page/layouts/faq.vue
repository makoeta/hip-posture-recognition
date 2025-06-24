<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
import { guideSequence } from "~/services/contentflow.service";

const backToOverview = () => {
  navigateTo("/guide");
};
const sequence = guideSequence;
const route = useRoute();

const urls = computed<string[]>(() => {
  const currentIndex = sequence.urls.indexOf(route.fullPath);

  if (currentIndex === -1) {
    return ["", ""];
  }

  return [
    currentIndex > 0 ? sequence.urls[currentIndex - 1] : "",
    currentIndex < sequence.urls.length - 1
      ? sequence.urls[currentIndex + 1]
      : "",
  ];
});
</script>

<template>
  <div class="flex h-screen flex-col items-center font-mono">
    <div class="flex h-screen w-[50%] flex-col">
      <div class="flex justify-center">
        <guide-header />
      </div>

      <div class="mt-8 mb-4 grow overflow-y-scroll px-4">
        <slot />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
