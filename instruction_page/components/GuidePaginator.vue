<script lang="ts" setup>
import { guideSequence } from "~/services/contentflow.service";
import { useAllGuideItemsChecked } from "#imports";

const backToOverview = () => {
  navigateTo("/guide");
};
const highLightNextBtn = useAllGuideItemsChecked();
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
  <div class="mb-5 flex w-full justify-between">
    <div />
    <div class="join h-fit">
      <NuxtLink :to="urls[0]">
        <button
          :class="{ 'btn-disabled': urls[0] == '' }"
          class="join-item btn btn-outline border-r-neutral-content text-xl"
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
            height="1em"
            viewBox="0 0 24 24"
            width="1em"
            xmlns="http://www.w3.org/2000/svg"
          >
            <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
            <path
              d="M3 18h18v-2H3zm0-5h18v-2H3zm0-7v2h18V6z"
              fill="currentColor"
            />
          </svg>
        </button>
      </div>
      <NuxtLink :to="urls[1]">
        <button
          :class="{ 'btn-disabled': urls[1] == '', horny: highLightNextBtn }"
          class="join-item btn btn-outline border-l-neutral-content text-xl"
        >
          Weiter
        </button>
      </NuxtLink>
    </div>
    <div />
  </div>
</template>

<style scoped>
.horny {
  animation: gradient 5s ease infinite;
}

@keyframes gradient {
  0%,
  100% {
    background-color: #339651;
  }
  25%,
  75% {
    background-color: #22c051;
  }
  30%,
  70% {
    background-color: #02ea48;
  }
}
</style>
