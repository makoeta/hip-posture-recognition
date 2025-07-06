<script setup>
definePageMeta({
  layout: "faq",
});
const backToOverview = () => {
  navigateTo("/guide");
};
const { data: faq } = await useAsyncData("faq", () => {
  return queryCollection("faq").first();
});
</script>

<template>
  <div>
  <div class="text-xl font-bold">
    Hier gibt’s Antworten auf die Fragen, die am häufigsten auftauchen. Schnell
    gelesen, schnell verstanden!
  </div>
  <div class="mt-6 space-y-6">
    <div class="text-4xl">Häufige Fragen</div>
    <div v-if="faq">
      <div
        v-for="(item, index) in faq.body[0].entries"
        :key="index"
        class="collapse-arrow bg-base-100 border-base-300 collapse mb-2 border"
      >
        <input :checked="index === 0" name="my-accordion-2" type="radio" />
        <div class="collapse-title text-xl font-semibold">
          {{ item.question }}
        </div>
        <div class="collapse-content text-lg">
          {{ item.answer }}
        </div>
      </div>
    </div>

    <div class="flex justify-center">
      <div class="btn btn-xl btn-wide" @click="backToOverview()">
        Zurück zur Übersicht
      </div>
    </div>
  </div>

  </div>
</template>
