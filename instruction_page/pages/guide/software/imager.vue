<script setup lang="ts">
definePageMeta({
  layout: "guide",
});

const isInstallerDownloaded = ref(false);
const isImagerInstalled = ref(false);

function handleUnpackCheck(val: boolean): void {
  isInstallerDownloaded.value = val;
}

function handleFanMountedCheck(val: boolean): void {
  isImagerInstalled.value = val;
}
</script>

<template>
  <GuideChecklist label="Imager installieren:">
    <GuideChecklistItem
      title="Installer herunterladen"
      @box-check="handleUnpackCheck"
    >
      <div class="text-xl">Laden Sie die offizielle Software herunter.</div>
      <div class="text-xl">
        Der offizielle Download finden Sie
        <NuxtLink
          to="https://www.raspberrypi.com/software/"
          target="_blank"
          external
        >
          <span class="font-bold hover:underline">hier</span> </NuxtLink
        >.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem
      title="Imager installieren"
      @box-check="handleFanMountedCheck"
    >
      <div class="text-xl">
        Klicken Sie anschließend um die heruntergeladene Datei um das Programm
        zu installieren.
      </div>
    </GuideChecklistItem>
  </GuideChecklist>

  <div
    class="mt-4 text-2xl"
    v-if="isInstallerDownloaded && isImagerInstalled"
    v-auto-animate
  >
    Sie können nun fortfahren.
    <span class="text-xl">(Klicken Sie auf weiter)</span>
  </div>
</template>

<style scoped></style>
