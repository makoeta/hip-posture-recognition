<script setup lang="ts">
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
  <div class="flex flex-col items-center font-mono">
    <div class="flex h-screen w-[50%] flex-col">
      <div class="flex justify-center">
        <guide-header />
      </div>

      <div class="mt-8 mb-4 grow px-4">
        <slot />
      </div>

      <div class="mb-5 flex w-full justify-between">
        <div />
        <div class="join h-fit">
          <NuxtLink :to="urls[0]">
            <button
              class="join-item btn btn-outline border-r-neutral-content text-xl"
              :class="{ 'btn-disabled': urls[0] == '' }"
            >
              Zurück
            </button>
          </NuxtLink>
          <div class="tooltip" data-tip="Inhaltsverzeichnis">
            <button
              class="join-item btn btn-outline btn-ghost text-xl"
              @click="backToOverview()"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                width="1em"
                height="1em"
                viewBox="0 0 24 24"
              >
                <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
                <path
                  fill="currentColor"
                  d="M3 18h18v-2H3zm0-5h18v-2H3zm0-7v2h18V6z"
                />
              </svg>
            </button>
          </div>
          <NuxtLink :to="urls[1]">
            <button
              class="join-item btn btn-outline border-l-neutral-content text-xl"
              :class="{ 'btn-disabled': urls[1] == '' }"
            >
              Weiter
            </button>
          </NuxtLink>
        </div>
        <div />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
