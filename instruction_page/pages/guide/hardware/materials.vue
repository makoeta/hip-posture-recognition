<script setup lang="ts">
import Guide from "~/layouts/guide.vue";

definePageMeta({
  layout: "guide",
});

const isKitChecked = ref(false);
const isWebCamChecked = ref(false);

function handleKitCheck(val: boolean) {
  isKitChecked.value = val;
}

function handleCamCheck(val: boolean) {
  isWebCamChecked.value = val;
}
</script>

<template>
  <GuideChecklist label="Benötigte Materialien">
    <GuideChecklistItem title="Raspberry Pi Kit" @box-check="handleKitCheck">
      <div class="text-xl">
        Das Kit beinhaltet alle benötigten Komponenten rund um das Kernsystem
        des Raspberry Pis.
      </div>
      <div class="text-xl">
        Sie erhalten das Kit
        <NuxtLink
          to="https://www.berrybase.de/raspberry-pi-5-8gb-ram-light-starter-kit-weiss"
          target="_blank"
          external
        >
          <span class="font-bold hover:underline">hier</span> </NuxtLink
        >.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem title="WebCam" @box-check="handleCamCheck">
      <div class="text-xl">
        Die WebCam ist die einzige Komponente, welche nicht im Kit inkludiert
        ist. Sie wird verwendet um das Live-Video des Patienten aufzuzeichnen.
      </div>
      <div class="text-xl">
        Sie erhalten deine geeignete Webcam
        <NuxtLink
          to="https://www.amazon.de/eMeet-Full-Webcam-automatischer-Lichtkorrektur/dp/B0002HAHUY/ref=sr_1_1_sspa?crid=226C3XYN4OWH7&dib=eyJ2IjoiMSJ9.J9i4X7I6VBGPjzo74qqSM6e-ynHbfhgQvVuvelkj0KxReZPxdS4gidUwGIV5pT3mn0l99cncHNukbjSBFo7Pa3QI7_OWV54r5hOmK917-qF9DmIlLVgOiqxijh8RgMZgL0Xz5SjuQffHLlNjNvmnKAGN5u8qwDX7x2FKB3wXnvAkDfjpVoYxnhBRVFD4w6-y62DAZUqmCHr-C-MaiNyrM4EgsaUgMiq5S7pfLpd-xe4.HObug2tarkTEg11DWUBy1yC9GcXloHtSKbIvORzDSZ4&dib_tag=se&keywords=jelly%2Bcomb%2B1080p%2Bhd%2Bwebcam&qid=1748801499&sprefix=webcam%2B1080p%2Bj%2Caps%2C95&sr=8-1-spons&sp_csd=d2lkZ2V0TmFtZT1zcF9hdGY&th=1"
          target="_blank"
          external
        >
          <span class="font-bold hover:underline">hier</span> </NuxtLink
        >.
      </div>
    </GuideChecklistItem>
  </GuideChecklist>

  <div
    class="mt-4 text-2xl"
    v-if="isWebCamChecked && isKitChecked"
    v-auto-animate
  >
    Sie haben alle benötigten Komponenten. Sie können nun fortfahren.
    <span class="text-xl">(Klicken Sie auf weiter)</span>
  </div>
</template>

<style scoped></style>
