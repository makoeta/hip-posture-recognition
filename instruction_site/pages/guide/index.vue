<script setup lang="ts">
definePageMeta({
  layout: "guide-overview",
});

interface MenuItem {
  label: string;
  url: string;
  subItems?: MenuItem[];
}

const topics = ref<MenuItem[]>([
  {
    label: "Einführung",
    url: "/guide/intro",
    subItems: [{ label: "Einführung", url: "/guide/intro" }],
  },
  {
    label: "Hardware",
    url: "/guide/hardware",
    subItems: [
      { label: "Materialien", url: "/guide/hardware/materials" },
      { label: "Montage: Lüfter", url: "/guide/hardware/fan" },
      { label: "Montage: Gehäuse", url: "/guide/hardware/case" },
    ],
  },
  {
    label: "Software",
    url: "/guide/software",
    subItems: [
      { label: "Imager installieren", url: "/guide/software/imager" },
      { label: "MicroSD Karte", url: "/guide/software/sdcard" },
      { label: "Image herunterladen", url: "/guide/software/image" },
      { label: "Image installieren", url: "/guide/software/install" },
    ],
  },
  {
    label: "Installation",
    url: "/guide/installation",
    subItems: [
      { label: "Verkabelung", url: "/guide/install/setup" },
      { label: "Benutzen", url: "/guide/install/use" },
    ],
  },
]);
</script>

<template>
  <div class="flex flex-col">
    <div class="text-8xl font-bold">Inhalt</div>
    <div class="flex flex-col text-5xl">
      <div
        class="bg-base-100 border-base-300 collapse flex flex-col"
        v-for="(topic, index) in topics"
        :key="topic.label"
      >
        <div class="bg-base-100 border-base-300 collapse">
          <input type="radio" name="my-accordion-1" :checked="index == 0" />
          <div class="collapse-title flex font-semibold hover:underline">
            {{ index + 1 }}.&nbsp;
            <div class="hover:underline">
              {{ topic.label }}
            </div>
          </div>
          <div class="collapse-content text-3xl">
            <div
              class="mb-3 flex"
              v-for="(subItem, subIndex) in topic.subItems"
              :key="subItem.label"
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
