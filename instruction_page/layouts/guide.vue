<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
import GuidePaginator from "~/components/GuidePaginator.vue";
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
    <GuidePaginator />
  </div>
</template>

<style scoped></style>
