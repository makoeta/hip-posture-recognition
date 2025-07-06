<script lang="ts" setup>
import {
  useCheckedCheckListItemCounter,
  useCheckListItemCounter,
} from "~/composables/useChecklist";

const isChecked = ref(false);

const emits = defineEmits<{
  (e: "box-check", value: boolean): void;
}>();

onMounted(() => {
  const counter = useCheckListItemCounter();

  counter.value = counter.value + 1;
});

onUnmounted(() => {
  const counter = useCheckListItemCounter();
  const checkedCounter = useCheckedCheckListItemCounter();
  checkedCounter.value = 0;
  counter.value = 0;
});

watch(isChecked, (checked) => {
  emits("box-check", checked);
  const checkedCounter = useCheckedCheckListItemCounter();

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
