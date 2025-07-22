<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";
import GuidePaginator from "~/components/GuidePaginator.vue";
</script>

<template>
  <div>
    <div class="flex h-screen flex-col items-center justify-between font-mono">
      <div class="flex w-full flex-col lg:w-[50%]">
        <div class="flex justify-center">
          <guide-header />
        </div>

        <div class="mt-8 mb-4 grow overflow-y-scroll px-4">
          <slot />
        </div>
      </div>
      <div class="bottom-1">
        <GuidePaginator />
      </div>
    </div>
    <Footer/>
  </div>
</template>

<style scoped></style>
