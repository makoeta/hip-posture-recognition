<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
</script>

<template>
  <div class="flex flex-col">
    <div
      class="flex min-h-screen flex-col items-center overflow-y-scroll font-mono"
    >
      <div class="flex w-full flex-col lg:w-[50%]">
        <div class="flex justify-center">
          <guide-header />
        </div>

        <div class="mt-8 mb-4 overflow-y-scroll px-4">
          <slot />
        </div>
      </div>

      <div class="mt-4 flex w-full justify-between font-mono">
        <div />
        <div class="join h-fit">
          <NuxtLink class="tooltip" data-tip="Anfangen" to="/guide/intro">
            <div class="join-item btn btn-ghost h-fit text-4xl">
              Zum Starten hier drücken!
            </div>
          </NuxtLink>
        </div>
        <div />
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped></style>
