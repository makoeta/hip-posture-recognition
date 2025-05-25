<script setup lang="ts">
definePageMeta({
  layout: "guide",
});

interface MenuItem {
  label: string;
  url: string;
}

const topics = ref<MenuItem[]>([
  { label: "Einführung", url: "/guide/intro" },
  { label: "Hardware", url: "/guide/hardware" },
  { label: "Software", url: "/guide/software" },
  { label: "Installation", url: "/guide/installation" },
]);
</script>

<template>
  <div class="flex flex-col">
    <div class="text-8xl font-bold">Inhalt</div>
    <div class="mt-6 ml-4 flex flex-col gap-4 text-5xl">
      <div
        v-for="(topic, index) in topics"
        :key="topic.label"
        class="flex w-fit"
      >
        {{ index + 1 }}.&nbsp;
        <NuxtLink class="hover:underline" :to="topic.url">
          {{ topic.label }}
        </NuxtLink>
      </div>
    </div>
  </div>
</template>
