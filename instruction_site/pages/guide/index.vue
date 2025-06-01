<script setup lang="ts">
definePageMeta({
  layout: "guide",
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
          <input type="radio" name="my-accordion-1" />
          <div class="collapse-title font-semibold">
            {{ index + 1 }}.&nbsp;
            <NuxtLink class="hover:underline" :to="topic.url">
              {{ topic.label }}
            </NuxtLink>
          </div>
          <div class="collapse-content text-xl">
            <div v-for="(subItem, subIndex) in topic.subItems">
              <NuxtLink :to="subItem.url">
                {{ index + 1 }}.{{ subIndex + 1 }}.&nbsp;{{ subItem.label }}
              </NuxtLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
