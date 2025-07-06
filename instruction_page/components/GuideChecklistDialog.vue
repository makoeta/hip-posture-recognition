<script lang="ts" setup>
import { checkedCheckListItemCounter, checkListItemCounter } from "#imports";

const itemCounter = checkListItemCounter();
const checkedItemCounter = checkedCheckListItemCounter();

const showDialog = computed(() => {
  console.log(itemCounter.value, checkedItemCounter.value);
  return (
    checkedItemCounter.value === itemCounter.value && itemCounter.value > 0
  );
});
</script>

<template>
  <div v-if="showDialog" class="mt-10 text-2xl">
    <slot />
  </div>
</template>
