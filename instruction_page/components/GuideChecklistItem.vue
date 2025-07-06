<script lang="ts" setup>
import {
  checkedCheckListItemCounter,
  checkListItemCounter,
} from "~/composables/checkListItemComposables";

defineProps<{
  title: string;
}>();

const isChecked = ref(false);

const emits = defineEmits<{
  (e: "box-check", value: boolean): void;
}>();

onMounted(() => {
  const counter = checkListItemCounter();

  counter.value = counter.value + 1;

  console.log("counter: " + counter.value);
});

onUnmounted(() => {
  const counter = checkListItemCounter();
  const checkedCounter = checkedCheckListItemCounter();
  checkedCounter.value = 0;
  counter.value = 0;

  console.log("counter: " + counter.value);
});

watch(isChecked, (checked) => {
  emits("box-check", checked);
  const checkedCounter = checkedCheckListItemCounter();

  if (checked) {
    checkedCounter.value = checkedCounter.value + 1;
  } else {
    checkedCounter.value = checkedCounter.value - 1;
  }

  console.log("checkedCounter: " + checkedCounter.value);
});
</script>

<template>
  <li class="list-row">
    <div class="text-4xl font-thin tabular-nums">
      <input v-model="isChecked" class="checkbox checkbox-lg" type="checkbox" />
    </div>
    <div class="list-col-grow">
      <div class="text-3xl">
        <slot name="label" />
      </div>
      <div class="text-xl">
        <slot name="description" />
      </div>
    </div>
  </li>
</template>

<style scoped></style>
