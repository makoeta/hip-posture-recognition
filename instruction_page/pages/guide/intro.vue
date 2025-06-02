<script setup lang="ts">
definePageMeta({
  layout: "guide",
});
</script>

<template>
  <div class="px-8 text-2xl">
    <div class="text-4xl">Hallo!</div>
    <br />
    <div>
      Dieses Open-Source-Projekt hilft dabei, die Körperhaltung von Patientinnen
      und Patienten automatisch zu erkennen. Ziel ist es, Pflegekräfte oder
      Angehörige bei der Betreuung zu unterstützen. Mit einem einfachen Setup
      auf einem Raspberry Pi kann das System schnell in Betrieb genommen werden.
      Diese Anleitung zeigt Schritt für Schritt, wie das geht – ganz ohne
      spezielles Vorwissen.
    </div>
    <br />
    <div>
      In dieser Anleitung sind weiterführende Informationen oder benötigte
      Dateien als Links hinterlegt. Solche Links erkennen Sie daran, dass der
      Text fett dargestellt ist und sich beim Darüberfahren mit der Maus
      unterstreicht. Ein Klick darauf führt Sie direkt zur jeweiligen Webseite
      oder Ressource.
    </div>
    <div>
      Zum Beispiel
      <NuxtLink to="/guide/intro">
        <div class="tooltip" data-tip="Klickbarer Link">
          <span class="font-bold hover:underline">hier</span>
        </div> </NuxtLink
      >.
    </div>
  </div>
</template>

<style scoped></style>
