<script lang="ts" setup></script>

<template>
  <div class="flex flex-col items-center justify-center text-2xl">
    <div class="mb-4">
      <slot name="text" />
    </div>

    <div class="mt-12">
      <NuxtLink
        external
        to="https://github.com/makoeta/hip-posture-recognition"
      >
        <button class="btn btn-xl">
          <slot name="toProjectLabel" />
        </button>
      </NuxtLink>
    </div>

    <div class="mt-6">
      <NuxtLink to="/guide/faq">
        <button class="btn btn-xl">
          <slot name="toFaqLabel" />
        </button>
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped></style>
