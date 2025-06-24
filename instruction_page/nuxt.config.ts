// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: true },
  modules: [
    "@nuxt/eslint",
    "@formkit/auto-animate",
    "@nuxtjs/i18n",
    "@nuxt/icon",
    "@nuxt/content",
  ],
  css: ["~/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },
  app: {
    head: {
      title: "HPR Setup Guide",
    },
  },
  content: {
    preview: {
      api: "https://api.nuxt.studio",
    },
  },
});
