<script setup lang="ts">
definePageMeta({
  layout: "guide",
});

const isImageDownloadedCheck = ref(false);

function handleImageDownloadCheck(val: boolean): void {
  isImageDownloadedCheck.value = val;
}
</script>

<template>
  <div>
    <GuideChecklist label="Image herunterladen:">
      <GuideChecklistItem
        title="Image herunterladen"
        @box-check="handleImageDownloadCheck"
      >
        <div class="text-xl">
          Laden Sie die Hip Posture Recognition Software herunter.
        </div>
        <div class="text-xl">
          Der offizielle Download finden Sie
          <NuxtLink to="https://www.github.com/" target="_blank" external>
            <span class="font-bold hover:underline">hier</span> </NuxtLink
          >.
        </div>
      </GuideChecklistItem>
    </GuideChecklist>

    <div class="mt-4 text-2xl" v-if="isImageDownloadedCheck" v-auto-animate>
      Sie können nun fortfahren.
      <span class="text-xl">(Klicken Sie auf weiter)</span>
    </div>
  </div>
</template>

<style scoped></style>
