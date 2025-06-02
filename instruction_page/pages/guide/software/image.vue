<script lang="ts" setup>
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
        <span class="text-xl">
          Der offizielle Download finden Sie
          <NuxtLink external target="_blank" to="https://www.github.com/">
            <span class="font-bold hover:underline">hier</span></NuxtLink
          >.
        </span>
      </GuideChecklistItem>
    </GuideChecklist>

    <div v-if="isImageDownloadedCheck" v-auto-animate class="mt-4 text-2xl">
      Sie können nun fortfahren.
      <span class="text-xl">(Klicken Sie auf weiter)</span>
    </div>
  </div>
</template>

<style scoped></style>
