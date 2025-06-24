<script lang="ts" setup>
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
  {
    label: "FAQ",
    url: "/guide/faq",
    subItems: [{ label: "FAQ", url: "/guide/faq" }],
  },
]);
</script>

<template>
  <div class="flex min-h-max flex-col">
    <div class="text-5xl font-bold 2xl:text-8xl">Inhalt</div>
    <div class="flex flex-col text-3xl 2xl:text-5xl">
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
          <div class="collapse-content text-xl 2xl:text-3xl">
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
