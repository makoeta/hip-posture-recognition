<script lang="ts" setup>
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
      <input v-model="isChecked" class="checkbox checkbox-lg" type="checkbox" />
    </div>
    <div class="list-col-grow">
      <div class="text-3xl">{{ title }}</div>
      <slot />
    </div>
  </li>
</template>

<style scoped></style>
