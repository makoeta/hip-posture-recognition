<script lang="ts" setup></script>

<template>
  <div class="flex flex-col items-center justify-center text-2xl">
    <div class="mb-4">
      <slot name="text" />
    </div>

    <div class="mt-12">
      <NuxtLink external target="_blank" to="https://www.github.com">
        <button class="btn btn-xl">
          <slot name="btnLabel" />
        </button>
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped></style>
