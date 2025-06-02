<script lang="ts" setup xmlns="http://www.w3.org/1999/html">
definePageMeta({
  layout: "guide",
});


const isImagerStartedCheck = ref(false);
const isHprInstalledCheck = ref(false);

function startImagerCheck(val: boolean): void {
  isImagerStartedCheck.value = val;
}

function hprInstalledCheck(val: boolean): void {
  isHprInstalledCheck.value = val;
}
</script>

<template>
  <GuideChecklist label="HPR Software installieren:">
    <GuideChecklistItem
        title="Öffnen Sie das zuvor installierte Programm"
        @box-check="startImagerCheck"
    >
      <div class="text-xl">
        Starten Sie das Programm "Raspberry Pi Imager" auf Ihrem PC.
      </div>
      <div class="text-xl">
        Sie haben den Imager in
        <NuxtLink target="_blank" to="/guide/software/imager">
          <span class="font-bold hover:underline"
          >diesem Schritt</span
          ></NuxtLink
        >&nbsp;heruntergeladen.
      </div>
    </GuideChecklistItem>

    <GuideChecklistItem
        title="Um die HPR Software zu installieren müssen drei Einstellungen
        vorgenommen werden:"
        @box-check="hprInstalledCheck"
    >
      <br>
      <div class="text-xl">
        Klicken Sie als erstes auf "MODELL WÄHLEN". Klicken Sie anschließend auf
        "RaspberryPi 5".
      </div>
      <br>
      <div class="text-xl">
        Als nächstes Klicken Sie auf "OS WÄHLEN". Scrollen Sie hier bis zum Ende
        der Liste und klicken Sie auf "Use custom". Wählen Sie dann die
        <NuxtLink target="_blank" to="/guide/software/imager">
          <span class="font-bold hover:underline"
          >zuvor heruntergeladene Image Datei</span
          ></NuxtLink
        >&nbsp;aus.
      </div>
      <br>
      <div class="text-xl">
        Zuletzt klicken Sie auf "SD-KARTE WÄHLEN". Wählen Sie anschließend die
        zuvor eingesteckte SD-Karte aus.
      </div>
    </GuideChecklistItem>
  </GuideChecklist>

  <div
      v-if="isImagerStartedCheck && isHprInstalledCheck"
      v-auto-animate
      class="mt-4 text-2xl"
  >
    Sie können nun fortfahren.
    <span class="text-xl">(Klicken Sie auf weiter)</span>
  </div>
</template>

<style scoped></style>
