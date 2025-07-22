// https://nuxt.com/docs/api/configuration/nuxt-config
import tailwindcss from "@tailwindcss/vite";

export default defineNuxtConfig({
  compatibilityDate: "2025-05-15",
  devtools: { enabled: false },
  modules: [
    "@nuxt/eslint",
    "@formkit/auto-animate",
    "@nuxtjs/i18n",
    "@nuxt/icon",
    "@nuxt/content",
    "@nuxtjs/mdc",
  ],
  css: ["~/assets/css/main.css"],
  vite: {
    plugins: [tailwindcss()],
  },
  app: {
    baseURL:
      process.env.NODE_ENV === "production" ? "/hip-posture-recognition/" : "/",
    head: {
      title: "HPR Setup Guide",
    },
  },
  content: {
    preview: {
      api: "https://api.nuxt.studio",
    },
    experimental: {},
  },
});
