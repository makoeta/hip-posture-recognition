<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
import GuidePaginator from "~/components/GuidePaginator.vue";
</script>

<template>
  <div class="">
    <div
      class="top-0 flex min-h-screen flex-col items-center justify-between font-mono"
    >
      <div class="flex w-full flex-col sm:w-[auto] sm:max-w-[50%]">
        <div class="flex justify-center">
          <guide-header />
        </div>

        <div class="mt-8 mb-4 grow px-4">
          <slot />
        </div>
      </div>
      <div class="bottom-1">
        <GuidePaginator />
      </div>
    </div>
    <div class="bottom-0">
      <Footer />
    </div>
  </div>
</template>

<style scoped></style>
