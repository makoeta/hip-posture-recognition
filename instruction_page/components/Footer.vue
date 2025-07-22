<script lang="ts" setup></script>

<template>
  <div>
    <footer
      class="footer footer-horizontal footer-center bg-base-200 text-base-content rounded p-10"
    >
      <nav class="grid grid-flow-col gap-4">
        <NuxtLink class="link link-hover" to="/">Home</NuxtLink>
        <NuxtLink
          class="link link-hover"
          external
          target="_blank"
          to="https://www.hs-heilbronn.de/de/unitylab"
          >Über UniTyLab
        </NuxtLink>
        <NuxtLink
          class="link link-hover"
          external
          target="_blank"
          to="https://www.hs-heilbronn.de/"
          >Über HHN
        </NuxtLink>
        <NuxtLink class="link link-hover" to="/legal"
          >Impressum (Legal)</NuxtLink
        >
      </nav>
      <aside>
        <p>Made by UniTyLab & HHN</p>
      </aside>
    </footer>
  </div>
</template>

<style scoped></style>
