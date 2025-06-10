<script lang="ts" setup>
definePageMeta({
  layout: "guide",
});
</script>

<template>
  <div class="px-8 text-xl  2xl:text-2xl">
    <div class="cursor typewriter-animation text-2xl 2xl:text-4xl">Hallo!</div>
    <br>
    <div>
      Dieses Open-Source-Projekt hilft dabei, die Körperhaltung von Patientinnen
      und Patienten automatisch zu erkennen. Ziel ist es, Pflegekräfte oder
      Angehörige bei der Betreuung zu unterstützen. Mit einem einfachen Setup
      auf einem Raspberry Pi kann das System schnell in Betrieb genommen werden.
      Diese Anleitung zeigt Schritt für Schritt, wie das geht – ganz ohne
      spezielles Vorwissen.
    </div>
    <br>
    <div>
      In dieser Anleitung sind weiterführende Informationen oder benötigte
      Dateien als Links hinterlegt. Solche Links erkennen Sie daran, dass der
      Text fett dargestellt ist und sich beim Darüberfahren mit der Maus
      unterstreicht. Ein Klick darauf führt Sie direkt zur jeweiligen Webseite
      oder Ressource.
    </div>
    <span>
      Zum Beispiel
      <NuxtLink to="/guide/intro">
        <div class="tooltip" data-tip="Klickbarer Link">
          <span class="font-bold hover:underline">hier</span>
        </div>
      </NuxtLink>.
    </span>
  </div>
</template>

<style scoped>
/* Cursor */
.cursor {
  width: 24em;
  border-right: 2px solid rgba(255, 255, 255, 0.75);
  font-size: 30px;
  white-space: nowrap;
  overflow: hidden;
}

/* Animation */
.typewriter-animation {
  animation: typewriter 2s steps(50) 1s 1 normal both,
  blinkingCursor 500ms steps(50) infinite normal;
}

@keyframes typewriter {
  from {
    width: 0;
  }
  to {
    width: 100%;
  }
}

@keyframes blinkingCursor {
  from {
    border-right-color: rgba(255, 255, 255, 0.75);
  }
  to {
    border-right-color: transparent;
  }
}
</style>
