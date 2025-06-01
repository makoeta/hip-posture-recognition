<script setup lang="ts">
import GuideHeader from "~/components/GuideHeader.vue";

const backToOverview = () => {
  navigateTo("/guide");
};
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
          <button class="join-item btn btn-outline">Zurück</button>
          <div class="tooltip" data-tip="Inhaltsverzeichnis">
            <button
              class="join-item btn btn-outline btn-ghost text-2xl"
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
          <button class="join-item btn btn-outline">Weiter</button>
        </div>
        <div />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
