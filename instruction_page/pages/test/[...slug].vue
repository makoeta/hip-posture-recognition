<template>
  <div>
    <div v-if="item">
      <GuideChecklist :label="item.body.label">
        <GuideChecklistItem
          v-for="(checkListItem, index) in item.body.items"
          :key="index"
          :title="checkListItem.label"
          @click="toggleCheckBox(index)"
        >
          <div class="text-xl">
            {{ checkListItem.text }}
          </div>
        </GuideChecklistItem>
      </GuideChecklist>

      <div
        v-if="checkedItems.length == item.body.items.length"
        class="mt-4 text-2xl"
      >
        {{ item.body.successMessage }}
        <span class="text-xl">(Klicken Sie auf weiter)</span>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { useRoute } from "#imports";

definePageMeta({
  layout: "guide",
});

const route = useRoute();
const slug = Array.isArray(route.params.slug)
  ? route.params.slug.join("/")
  : route.params.slug;

const { data: item } = await useAsyncData("test", () => {
  return queryCollection("test")
    .path("/test/" + slug)
    .first();
});

let checkedItems = ref<number[]>([]);

const toggleCheckBox = (index: number) => {
  if (checkedItems.value.includes(index)) {
    checkedItems.value = checkedItems.value.filter((n) => n !== index);
    return;
  }
  checkedItems.value = [...checkedItems.value, index];
};
</script>
