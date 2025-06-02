<script setup lang="ts">
definePageMeta({
  layout: "guide",
});

const isUnpacked = ref(false);
const isFanMounted = ref(false);

function handleUnpackCheck(val: boolean): void {
  isUnpacked.value = val;
}

function handleFanMountedCheck(val: boolean): void {
  isFanMounted.value = val;
}
</script>

<template>
  <GuideChecklist label="Lüfter montieren:">
    <GuideChecklistItem title="Kit auspacken" @box-check="handleUnpackCheck">
      <div class="text-xl">Entpacken Sie das RaspberryPi 5 Kit.</div>
      <div class="text-xl">
        Entnehmen Sie dafür die einzelnen Komponenten (Raspberry Pi und Lüfter)
        aus dem Paket.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem
      title="Lüfter anbringen"
      @box-check="handleFanMountedCheck"
    >
      <div class="text-xl">Bringen Sie den Lüfter an den RaspberryPi an.</div>
      <div class="text-xl">
        Die offizielle Anleitung dafür finden Sie
        <NuxtLink
          to="https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-product-brief.pdf"
          target="_blank"
          external
        >
          <span class="font-bold hover:underline">hier</span> </NuxtLink
        >.
      </div>
    </GuideChecklistItem>
  </GuideChecklist>

  <div class="mt-4 text-2xl" v-if="isUnpacked && isFanMounted" v-auto-animate>
    Sie haben den Lüfter montiert. Sie können nun fortfahren.
    <span class="text-xl">(Klicken Sie auf weiter)</span>
  </div>
</template>

<style scoped></style>
