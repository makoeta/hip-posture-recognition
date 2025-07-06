<script lang="ts" setup>
import { useAllGuideItemsChecked } from "#imports";

const showDialog = useAllGuideItemsChecked();
</script>

<template>
  <div v-if="showDialog" class="mt-10 text-2xl">
    <slot />
  </div>
</template>
