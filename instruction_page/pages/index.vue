<script lang="ts" setup></script>

<template>
  <div class="flex h-screen w-screen flex-col">
    <div class="mt-10 ml-5 text-5xl font-bold lg:text-8xl">
      Hip Posture Recognition
    </div>
    <div class="flex grow items-center justify-center">
      <NuxtLink
        class="btn btn-xl btn-outline h-[8rem] w-[20rem] text-3xl lg:h-[15rem] lg:w-[35rem] lg:text-6xl"
        to="/guide"
      >
        <div class="flex flex-col items-center">
          <div class="text-6xl lg:text-9xl">
            <svg
              height="1em"
              viewBox="0 0 24 24"
              width="1em"
              xmlns="http://www.w3.org/2000/svg"
            >
              <!-- Icon from Google Material Icons by Material Design Authors - https://github.com/material-icons/material-icons/blob/master/LICENSE -->
              <path
                d="M21 5c-1.11-.35-2.33-.5-3.5-.5c-1.95 0-4.05.4-5.5 1.5c-1.45-1.1-3.55-1.5-5.5-1.5S2.45 4.9 1 6v14.65c0 .25.25.5.5.5c.1 0 .15-.05.25-.05C3.1 20.45 5.05 20 6.5 20c1.95 0 4.05.4 5.5 1.5c1.35-.85 3.8-1.5 5.5-1.5c1.65 0 3.35.3 4.75 1.05c.1.05.15.05.25.05c.25 0 .5-.25.5-.5V6c-.6-.45-1.25-.75-2-1m0 13.5c-1.1-.35-2.3-.5-3.5-.5c-1.7 0-4.15.65-5.5 1.5V8c1.35-.85 3.8-1.5 5.5-1.5c1.2 0 2.4.15 3.5.5z"
                fill="currentColor"
              />
              <path
                d="M17.5 10.5c.88 0 1.73.09 2.5.26V9.24c-.79-.15-1.64-.24-2.5-.24c-1.7 0-3.24.29-4.5.83v1.66c1.13-.64 2.7-.99 4.5-.99M13 12.49v1.66c1.13-.64 2.7-.99 4.5-.99c.88 0 1.73.09 2.5.26V11.9c-.79-.15-1.64-.24-2.5-.24c-1.7 0-3.24.3-4.5.83m4.5 1.84c-1.7 0-3.24.29-4.5.83v1.66c1.13-.64 2.7-.99 4.5-.99c.88 0 1.73.09 2.5.26v-1.52c-.79-.16-1.64-.24-2.5-.24"
                fill="currentColor"
              />
            </svg>
          </div>

          Anleitung
        </div>
      </NuxtLink>
    </div>
    <div class="mr-5 mb-5 self-end">by UniTyLab & HHN</div>
  </div>
</template>

<style scoped></style>
