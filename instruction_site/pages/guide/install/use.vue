<script setup lang="ts">
definePageMeta({
  layout: "guide",
});
</script>

<template>
  <div class="flex flex-col items-center justify-center text-2xl">
    <div class="mb-4">
      Das System ist nun vollständig eingerichtet und einsatzbereit. Sie können
      es ab sofort nutzen, um die Körperhaltung automatisch zu erfassen und
      entsprechende Rückmeldungen zu erhalten. Wenn Sie das Projekt erweitern
      oder an Ihre individuellen Anforderungen anpassen möchten, finden Sie im
      Repository weiterführende Informationen und Beispiele. Bei Fragen oder
      Problemen steht Ihnen die Community gerne zur Seite – besuchen Sie dazu
      einfach die Projektseite.
    </div>
    <div>Vielen Dank, dass Sie dieses Open-Source-Projekt verwenden!</div>

    <div class="mt-12">
      <NuxtLink to="https://www.github.com" target="_blank" external>
        <button class="btn btn-xl">Zur Projektseite</button>
      </NuxtLink>
    </div>
  </div>
</template>

<style scoped></style>
