<script lang="ts" setup>
definePageMeta({
  layout: "guide",
});

</script>

<template>
  <GuideChecklist label="System vorbereiten:">
    <GuideChecklistItem
        title="Bildschirmkabel anschließen"
    >
      <br>
      <div class="text-xl">
        Schließen Sie den microHDMI-Adapter an das HDMI Kabel an.
      </div>
      <br>
      <div class="text-xl">
        Schließen Sie anschließend das HDMI Kabel an Ihren Bildschirm an.
      </div>
      <br>
      <div class="text-xl">
        Zuletzt stecken Sie den microHDMI-Adapter in den RaspberryPi.
      </div>
      <br>
    </GuideChecklistItem>

    <GuideChecklistItem
        title="Webcam anschließen"
    >
      <div class="text-xl">
        Packen Sie die Webcam aus und schließen Sie diese an den RaspberryPi an.
        Montieren Sie die Webcam an Ihrem Monitor.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem
        title="Stromkabel anschließen"
    >
      <div class="text-xl">
        Stecken Sie das Stromkabel zunächst in die Steckdose, dann in den
        RaspberryPi.
      </div>
      <div class="text-xl">Der RaspberryPi startet anschließend.</div>
    </GuideChecklistItem>
  </GuideChecklist>
</template>

<style scoped></style>
