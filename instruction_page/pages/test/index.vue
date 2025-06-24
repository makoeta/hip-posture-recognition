<script lang="ts" setup>
const { data: home } = await useAsyncData(() =>
  queryCollection("faq").path("/**.yml").first(),
);

useSeoMeta({
  title: home.value?.title,
  description: home.value?.description,
});
</script>

<template>
  <ContentRenderer v-if="home" :value="home" />
  <div v-else>Home not found</div>
</template>
