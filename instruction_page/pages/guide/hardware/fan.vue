<script lang="ts" setup>
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
  <div>
    <GuideChecklist label="Lüfter montieren:">
      <GuideChecklistItem title="Kit auspacken" @box-check="handleUnpackCheck">
        <div class="text-xl">Entpacken Sie das RaspberryPi 5 Kit.</div>
        <div class="text-xl">
          Entnehmen Sie dafür die einzelnen Komponenten (Raspberry Pi und
          Lüfter) aus dem Paket.
        </div>
      </GuideChecklistItem>

      <GuideChecklistItem
          title="Lüfter anbringen"
          @box-check="handleFanMountedCheck"
      >
        <div class="text-xl">Bringen Sie den Lüfter an den RaspberryPi an.</div>
        <span class="text-xl">
          Die offizielle Anleitung dafür finden Sie

          <NuxtLink
              class="font-bold hover:underline"
              external
              target="_blank"
              to="https://datasheets.raspberrypi.com/cooling/raspberry-pi-active-cooler-product-brief.pdf"
          >
            hier</NuxtLink
          >.
        </span>
      </GuideChecklistItem>
    </GuideChecklist>

    <div v-if="isUnpacked && isFanMounted" class="mt-4 text-2xl">
      Sie haben den Lüfter montiert. Sie können nun fortfahren.
      <span class="text-xl">(Klicken Sie auf weiter)</span>
    </div>
  </div>
</template>

<style scoped></style>
