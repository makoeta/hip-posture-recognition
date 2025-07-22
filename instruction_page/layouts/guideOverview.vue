<script lang="ts" setup>
import GuideHeader from "~/components/GuideHeader.vue";

const startGuide = () => {
  navigateTo("/guide/intro");
};
</script>

<template>
  <div>
    <div class="flex h-screen flex-col items-center font-mono">
      <div class="flex w-[50%] flex-col">
        <div class="flex justify-center">
          <guide-header />
        </div>

        <div class="mt-8 mb-4 overflow-y-scroll px-4">
          <slot />
        </div>
      </div>

      <div class="flex w-full justify-between font-mono">
        <div />
        <div class="join h-fit">
          <div class="tooltip" data-tip="Anfangen">
            <button
              class="join-item btn btn-ghost text-4xl"
              @click="startGuide()"
            >
              <div>Zum Starten hier drücken!</div>
            </button>
          </div>
        </div>
        <div />
      </div>
    </div>
    <Footer />
  </div>
</template>

<style scoped></style>
