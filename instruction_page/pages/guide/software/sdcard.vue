<script lang="ts" setup>
definePageMeta({
  layout: "guide",
});

const isAdapterCheck = ref(false);
const isInPcCheck = ref(false);


function handleAdapterCheck(val: boolean): void {
  isAdapterCheck.value = val;
}

function handlePcCheck(val: boolean): void {
  isInPcCheck.value = val;
}
</script>

<template>
  <div>
    <GuideChecklist label="MicroSD Karte mit PC verbinden:">
      <GuideChecklistItem
          title="microSD in Adapter"
          @box-check="handleAdapterCheck"
      >
        <div class="text-xl">
          Stecken Sie die MicroSD-Karte in den Adapter. (Siehe Abb. 1)
        </div>
      </GuideChecklistItem>

      <GuideChecklistItem title="Adapter in PC" @box-check="handlePcCheck">
        <div class="text-xl">
          Stecken Sie den Adapter mit MicroSD-Karte in Ihren PC. (Siehe Abb. 2)
        </div>
      </GuideChecklistItem>
    </GuideChecklist>

    <div
        v-if="isAdapterCheck && isInPcCheck"
        v-auto-animate
        class="mt-4 text-2xl"
    >
      Sie können nun fortfahren.
      <span class="text-xl">(Klicken Sie auf weiter)</span>
    </div>
  </div>
</template>

<style scoped></style>
