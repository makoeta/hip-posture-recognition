<script lang="ts" setup>
import procedure from "~/content/overview.json";

definePageMeta({
  layout: "guide-overview",
});

interface MenuItem {
  label: string;
  url: string;
  subItems?: MenuItem[];
}

const topics = ref<MenuItem[]>(procedure);
</script>

<template>
  <div class="flex min-h-max flex-col">
    <div class="text-5xl font-bold 2xl:text-7xl">Inhalt</div>
    <div class="flex flex-col text-3xl 2xl:text-4xl">
      <div
        v-for="(topic, index) in topics"
        :key="topic.label"
        class="bg-base-100 border-base-300 collapse flex flex-col"
      >
        <div class="bg-base-100 border-base-300 collapse-arrow collapse">
          <input :checked="index == 0" name="my-accordion-1" type="radio" />
          <div class="collapse-title flex font-semibold hover:underline">
            {{ index + 1 }}.&nbsp;
            <div class="hover:underline">
              {{ topic.label }}
            </div>
          </div>
          <div class="collapse-content text-xl 2xl:text-2xl">
            <div
              v-for="(subItem, subIndex) in topic.subItems"
              :key="subItem.label"
              class="mb-3 flex"
            >
              {{ index + 1 }}.{{ subIndex + 1 }}.&nbsp;
              <NuxtLink :to="subItem.url">
                <div class="hover:underline">
                  {{ subItem.label }}
                </div>
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
