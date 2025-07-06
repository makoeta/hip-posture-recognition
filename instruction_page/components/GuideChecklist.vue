<script lang="ts" setup>
defineProps<{
  label: string;
}>();
</script>

<template>
  <ul class="list">
    <li class="p-4 pb-2 text-3xl font-bold tracking-wide">
      <slot name="label" />
    </li>
    <slot name="items" />
  </ul>
</template>

<style scoped></style>
