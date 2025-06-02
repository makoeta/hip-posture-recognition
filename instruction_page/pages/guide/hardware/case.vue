<script lang="ts" setup>
definePageMeta({
  layout: "guide",
});

const isUnpacked = ref(false);
const isCaseDone = ref(false);

function handleUnpackCheck(val: boolean): void {
  isUnpacked.value = val;
}

function handleFanMountedCheck(val: boolean): void {
  isCaseDone.value = val;
}
</script>

<template>
  <div>
    <GuideChecklist label="Gehäuse montieren:">
      <GuideChecklistItem
        title="Gehäuse auspacken"
        @box-check="handleUnpackCheck"
      >
        <div class="text-xl">
          Entnehmen Sie die Box mit dem Gehäuse aus dem Paket.
        </div>
      </GuideChecklistItem>

      <GuideChecklistItem
        title="Lüfter anbringen"
        @box-check="handleFanMountedCheck"
      >
        <div class="text-xl">Bauen Sie das Gehäuse um den RaspberryPi.</div>
        <span class="text-xl">
          Die offizielle Anleitung dafür finden Sie
          <NuxtLink
            external
            target="_blank"
            to="https://datasheets.raspberrypi.com/case/case-for-raspberry-pi-5-product-brief.pdf"
          >
            <span class="font-bold hover:underline">hier</span></NuxtLink
          >.
        </span>
      </GuideChecklistItem>
    </GuideChecklist>

    <div v-if="isUnpacked && isCaseDone" v-auto-animate class="mt-4 text-2xl">
      Sie haben das Gehäuse montiert und schließend hiermit den Hardwareteil der
      Anleitung ab. Sie können nun fortfahren.
      <span class="text-xl">(Klicken Sie auf weiter)</span>
    </div>
  </div>
</template>

<style scoped></style>
