<script setup lang="ts">
defineProps<{
  label: string;
}>();
</script>

<template>
  <ul class="list">
    <li class="p-4 pb-2 text-3xl font-bold tracking-wide">
      {{ label }}
    </li>

    <slot />
  </ul>
</template>

<style scoped></style>
