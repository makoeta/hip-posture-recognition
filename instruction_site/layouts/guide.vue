<script setup lang="ts">
import GuideHeader from "~/components/GuideHeader.vue";

const page = ref(1);
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
          <button class="join-item btn btn-ghost">{{ page }}</button>
          <button class="join-item btn btn-outline">Weiter</button>
        </div>
        <theme-controller />
      </div>
    </div>
  </div>
</template>

<style scoped></style>
