<script setup>
import { useRoute } from "vue-router";
const route = useRoute();
definePageMeta({
  layout: "guide",
});
const page = route.params.page;

const components = {
  1: defineAsyncComponent(
    () => import("@/components/guide/pages/hardware/page1.vue"),
  ),
  2: defineAsyncComponent(
    () => import("@/components/guide/pages/hardware/page2.vue"),
  ),
};

const currentComponent = components[page] || components[1];
</script>

<template>
  <div>
    <component :is="currentComponent" />
  </div>
</template>
