<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
</script>

<template>
  <div>
    <div class="flex h-screen flex-col items-center font-mono">
      <div class="flex h-screen flex-col sm:w-[auto] sm:max-w-[50%]">
        <div class="flex justify-center">
          <guide-header />
        </div>

        <div class="mt-8 mb-4 grow overflow-y-scroll px-4">
          <slot />
        </div>
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped></style>
