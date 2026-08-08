import { defineCollection } from 'astro:content';
import { glob } from 'astro/loaders';
import { z } from 'astro/zod';

const story = defineCollection({
  loader: glob({ base: './src/content/story', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    /** Optional title. If omitted, no heading is shown (date still appears when available). */
    title: z.string().optional(),
    /** Optional date override when there is no image (or to control sorting). */
    date: z.coerce.date().optional(),
    /** Optional teaser for the list page. */
    summary: z.string().optional(),
    /** Filename in public/images/markus/story/ */
    image: z.string().optional(),
    /** Optional body text (can also use the markdown body). */
    text: z.string().optional(),
  }),
});

const hymns = defineCollection({
  loader: glob({ base: './src/content/hymns', pattern: '**/*.{md,mdx}' }),
  schema: z.object({
    title: z.string(),
    /** `songs` = almindelige sange, `lullabies` = godnatsange */
    section: z.enum(['songs', 'lullabies']),
    /** Optional composer / melody credit */
    melody: z.string().optional(),
    /** Optional lyricist credit */
    lyrics: z.string().optional(),
    /** Optional short personal note */
    note: z.string().optional(),
  }),
});

export const collections = { story, hymns };
