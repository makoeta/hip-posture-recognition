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
  <GuideChecklist label="System vorbereiten:">
    <GuideChecklistItem
      title="Bildschirmkabel anschließen"
      @box-check="handleUnpackCheck"
    >
      <br />
      <div class="text-xl">
        Schließen Sie den microHDMI-Adapter an das HDMI Kabel an.
      </div>
      <br />
      <div class="text-xl">
        Schließen Sie anschließend das HDMI Kabel an Ihren Bildschirm an.
      </div>
      <br />
      <div class="text-xl">
        Zuletzt stecken Sie den microHDMI-Adapter in den RaspberryPi.
      </div>
      <br />
    </GuideChecklistItem>

    <GuideChecklistItem
      title="Webcam anschließen"
      @box-check="handleUnpackCheck"
    >
      <div class="text-xl">
        Packen Sie die Webcam aus und schließen Sie diese an den RaspberryPi an.
        Montieren Sie die Webcam an Ihrem Monitor.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem
      title="Stromkabel anschließen"
      @box-check="handleUnpackCheck"
    >
      <div class="text-xl">
        Stecken Sie das Stromkabel zunächst in die Steckdose, dann in den
        RaspberryPi.
      </div>
      <div class="text-xl">Der RaspberryPi startet anschließend.</div>
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
