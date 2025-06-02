<script setup lang="ts">
defineProps<{
  title: string;
}>();

const isChecked = ref(false);

const emits = defineEmits<{
  (e: "box-check", value: boolean): void;
}>();

watch(isChecked, (checked) => {
  emits("box-check", checked);
});
</script>

<template>
  <li class="list-row">
    <div class="text-4xl font-thin tabular-nums">
      <input type="checkbox" class="checkbox checkbox-lg" v-model="isChecked" />
    </div>
    <div class="list-col-grow">
      <div class="text-3xl">{{ title }}</div>
      <slot />
    </div>
  </li>
</template>

<style scoped></style>
