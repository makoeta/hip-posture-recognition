import { defineCollection, defineContentConfig, z } from "@nuxt/content";

export default defineContentConfig({
  collections: {
    faq: defineCollection({
      type: "page",
      source: "faq/faq.yml",
      schema: z.object({
        entries: z.array(
          z.object({
            question: z.string(),
            answer: z.string(),
          }),
        ),
      }),
    }),
  },
});
