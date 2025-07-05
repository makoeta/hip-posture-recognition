import { defineCollection, defineContentConfig, z } from "@nuxt/content";

const checkListItem = z.object({
  checklist: z.object({
    label: z.string(),
    description: z.string(),
    successMessage: z.string(),
    items: z.array(
      z.object({
        label: z.string(),
        text: z.string(),
      }),
    ),
  }),
});
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
    test: defineCollection({
      type: "page",
      source: "**/*.yml",
      schema: checkListItem,
    }),
  },
});
