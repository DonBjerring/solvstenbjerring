# Sølvsten Bjerring Website Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a static Astro + Tailwind family website (Danish) for www.solvstenbjerring.dk with Forside, Trivan placeholder, Markus (Forløb / Galleri / Diplomer), and Om familien — empty content structures ready for Markdown and image drops, deployable to GitHub Pages.

**Architecture:** Astro static site. Updates live in an Astro Content Collection (`src/content/opdateringer/`). Galleri and Diplomer images live under `public/images/...` and are discovered at build time via `fs.readdirSync`. Shared `BaseLayout` + `Header`/`Footer`. GitHub Actions publishes `dist/` to GitHub Pages.

**Tech Stack:** Astro 7, Tailwind CSS 4 (`@tailwindcss/vite`), TypeScript, GitHub Pages + Actions.

**Spec:** `docs/superpowers/specs/2026-08-04-solvstenbjerring-website-design.md`

**Clarifications locked for implementation (from spec review):**
- `/markus/` hub = short Danish intro + links to Forløb, Galleri, Diplomer
- Galleri/Diplomer = drop files into `public/images/...`; pages read the folder at build time; sort by filename; no captions in v1
- Forløb Markdown may embed images via paths like `/images/markus/forloeb/fil.jpg` (store those files under `public/images/markus/forloeb/`)

---

## File map

| Path | Responsibility |
|------|----------------|
| `package.json`, `astro.config.mjs`, `tsconfig.json` | Project tooling and Pages `site` URL |
| `src/styles/global.css` | Tailwind import + CSS variables (coastal blue-grey) |
| `src/content/config.ts` | `opdateringer` collection schema |
| `src/content/opdateringer/.gitkeep` | Empty collection folder (no sample posts) |
| `src/layouts/BaseLayout.astro` | HTML shell, fonts, global CSS |
| `src/components/Header.astro` | Top nav + Markus dropdown + mobile menu |
| `src/components/Footer.astro` | Simple footer |
| `src/components/UpdateCard.astro` | Card/row for one update on the list page |
| `src/components/GalleryGrid.astro` | Image grid or empty state |
| `src/lib/gallery.ts` | `listPublicImages(subdir)` helper |
| `src/pages/index.astro` | Forside |
| `src/pages/trivan.astro` | Kommer senere |
| `src/pages/om-familien.astro` | Family text |
| `src/pages/markus/index.astro` | Markus hub |
| `src/pages/markus/forloeb/index.astro` | Update list |
| `src/pages/markus/forloeb/[slug].astro` | Single update |
| `src/pages/markus/galleri.astro` | Gallery |
| `src/pages/markus/diplomer.astro` | Diplomas gallery |
| `public/images/hjem/.gitkeep` | House photo folder |
| `public/images/markus/galleri/.gitkeep` | Gallery folder |
| `public/images/markus/diplomer/.gitkeep` | Diplomas folder |
| `public/images/markus/forloeb/.gitkeep` | Images embedded in updates |
| `.github/workflows/deploy.yml` | Build + Pages deploy |
| `README.md` | How to add updates and images |
| `CNAME` | Optional; add when DNS is ready (`www.solvstenbjerring.dk`) |

---

### Task 1: Scaffold Astro + Tailwind

**Files:**
- Create: `package.json`, `astro.config.mjs`, `tsconfig.json`, `src/styles/global.css`, `src/env.d.ts`, `.gitignore` (extend), `public/favicon.svg`

- [ ] **Step 1: Create the Astro project in the repo root**

The repo already has `.gitignore`, `docs/`, and a git commit. Scaffold manually (do **not** run `npm create astro` into a non-empty dir without care). From repo root:

```bash
npm init -y
npm install astro@^7 @tailwindcss/vite@^4 tailwindcss@^4
npm pkg set type=module
npm pkg set scripts.dev="astro dev"
npm pkg set scripts.build="astro build"
npm pkg set scripts.preview="astro preview"
```

- [ ] **Step 2: Write `astro.config.mjs`**

```js
import { defineConfig } from 'astro/config';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://www.solvstenbjerring.dk',
  output: 'static',
  vite: {
    plugins: [tailwindcss()],
  },
});
```

- [ ] **Step 3: Write `tsconfig.json`**

```json
{
  "extends": "astro/tsconfigs/strict",
  "include": [".astro/types.d.ts", "**/*"],
  "exclude": ["dist"]
}
```

- [ ] **Step 4: Write `src/env.d.ts`**

```ts
/// <reference types="astro/client" />
```

- [ ] **Step 5: Write `src/styles/global.css`**

```css
@import "tailwindcss";

@theme {
  --font-display: "Fraunces", Georgia, serif;
  --font-sans: "Source Sans 3", "Segoe UI", sans-serif;

  --color-sand: #f4f6f8;
  --color-mist: #e4ebf0;
  --color-sea: #6b8499;
  --color-deep: #2c3a45;
  --color-foam: #ffffff;
  --color-drift: #8a9aaa;
}

html {
  scroll-behavior: smooth;
}

body {
  @apply bg-sand text-deep font-sans antialiased;
}

h1,
h2,
h3 {
  @apply font-display;
}

.prose p {
  @apply mb-4;
}

.prose img {
  @apply my-6 w-full h-auto rounded-sm;
}

.prose a {
  @apply text-sea underline;
}
```
- [ ] **Step 6: Extend `.gitignore`**

Ensure these entries exist (keep existing `.superpowers/`):

```
.superpowers/
node_modules/
dist/
.astro/
.DS_Store
```

- [ ] **Step 7: Add a minimal `public/favicon.svg`**

Simple blue-grey circle mark (inline SVG file).

- [ ] **Step 8: Verify install**

Run: `npx astro --version`  
Expected: Astro 7.x prints.

- [ ] **Step 9: Commit**

```bash
git add package.json package-lock.json astro.config.mjs tsconfig.json src/styles/global.css src/env.d.ts .gitignore public/favicon.svg
git commit -m "Scaffold Astro 7 with Tailwind CSS 4"
```

---

### Task 2: Base layout, header, footer

**Files:**
- Create: `src/layouts/BaseLayout.astro`, `src/components/Header.astro`, `src/components/Footer.astro`

- [ ] **Step 1: Create `src/layouts/BaseLayout.astro`**

```astro
---
import '../styles/global.css';
import Header from '../components/Header.astro';
import Footer from '../components/Footer.astro';

interface Props {
  title: string;
  description?: string;
}

const {
  title,
  description = 'Familiehjemmeside for familien Sølvsten Bjerring.',
} = Astro.props;
const pageTitle = title === 'Sølvsten Bjerring' ? title : `${title} · Sølvsten Bjerring`;
---

<!doctype html>
<html lang="da">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <meta name="description" content={description} />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link rel="preconnect" href="https://fonts.googleapis.com" />
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
    <link
      href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,600&family=Source+Sans+3:wght@400;500;600&display=swap"
      rel="stylesheet"
    />
    <title>{pageTitle}</title>
  </head>
  <body class="min-h-screen flex flex-col">
    <Header />
    <main class="flex-1">
      <slot />
    </main>
    <Footer />
  </body>
</html>
```

- [ ] **Step 2: Create `src/components/Header.astro`**

Desktop: links Forside, Trivan, Markus (details/summary or hover dropdown with Forløb, Galleri, Diplomer), Om familien.  
Mobile: button toggles a panel with the same links (small inline `<script>` is fine).

Brand text in header: **Sølvsten Bjerring** (link to `/`). Keep brand visible but not competing with page content — on Forside the page itself carries the main brand moment.

Mark active route with `Astro.url.pathname` (prefix match for `/markus`).

- [ ] **Step 3: Create `src/components/Footer.astro`**

```astro
---
const year = new Date().getFullYear();
---
<footer class="border-t border-mist mt-16">
  <div class="mx-auto max-w-3xl px-4 py-8 text-sm text-sea">
    <p>© {year} Familien Sølvsten Bjerring</p>
  </div>
</footer>
```

- [ ] **Step 4: Temporary smoke page `src/pages/index.astro`**

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
---
<BaseLayout title="Sølvsten Bjerring">
  <div class="mx-auto max-w-3xl px-4 py-16">
    <h1 class="text-4xl text-deep">Sølvsten Bjerring</h1>
    <p class="mt-4 text-sea">Layout smoke test</p>
  </div>
</BaseLayout>
```

- [ ] **Step 5: Run dev server and verify nav renders**

Run: `npm run dev`  
Expected: Page loads; nav shows four top items; Markus submenu lists three links.

- [ ] **Step 6: Commit**

```bash
git add src/layouts src/components src/pages/index.astro
git commit -m "Add base layout with header and footer navigation"
```

---

### Task 3: Content collection + gallery helper + image folders

**Files:**
- Create: `src/content/config.ts`, `src/content/opdateringer/.gitkeep`, `src/lib/gallery.ts`, `public/images/hjem/.gitkeep`, `public/images/markus/galleri/.gitkeep`, `public/images/markus/diplomer/.gitkeep`, `public/images/markus/forloeb/.gitkeep`

- [ ] **Step 1: Create `src/content/config.ts`**

```ts
import { defineCollection, z } from 'astro:content';

const opdateringer = defineCollection({
  type: 'content',
  schema: z.object({
    title: z.string(),
    date: z.coerce.date(),
    summary: z.string(),
  }),
});

export const collections = { opdateringer };
```

- [ ] **Step 2: Create empty collection folder**

`src/content/opdateringer/.gitkeep` (no sample Markdown in v1).

- [ ] **Step 3: Create `src/lib/gallery.ts`**

```ts
import fs from 'node:fs';
import path from 'node:path';

const IMAGE_EXT = new Set(['.jpg', '.jpeg', '.png', '.webp', '.gif', '.avif']);

/** List image files under public/images/<subdir>, sorted by filename. */
export function listPublicImages(subdir: string): { src: string; name: string }[] {
  const dir = path.join(process.cwd(), 'public', 'images', subdir);
  if (!fs.existsSync(dir)) return [];

  return fs
    .readdirSync(dir)
    .filter((name) => IMAGE_EXT.has(path.extname(name).toLowerCase()))
    .sort((a, b) => a.localeCompare(b, 'da'))
    .map((name) => ({
      name,
      src: `/images/${subdir.replace(/\\/g, '/')}/${name}`,
    }));
}
```

- [ ] **Step 4: Create image directories with `.gitkeep`**

Paths listed above.

- [ ] **Step 5: Create `src/components/UpdateCard.astro`**

```astro
---
interface Props {
  title: string;
  date: Date;
  summary: string;
  href: string;
}

const { title, date, summary, href } = Astro.props;
const formatted = date.toLocaleDateString('da-DK', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
---
<a href={href} class="block py-6 border-b border-mist hover:bg-mist/40 transition-colors -mx-2 px-2 rounded-sm">
  <time class="text-sm text-sea" datetime={date.toISOString()}>{formatted}</time>
  <h2 class="mt-1 text-2xl text-deep">{title}</h2>
  <p class="mt-2 text-deep/80 leading-relaxed">{summary}</p>
</a>
```

- [ ] **Step 6: Create `src/components/GalleryGrid.astro`**

```astro
---
interface Props {
  images: { src: string; name: string }[];
  emptyMessage: string;
}

const { images, emptyMessage } = Astro.props;
---
{images.length === 0 ? (
  <p class="text-sea text-lg py-12">{emptyMessage}</p>
) : (
  <ul class="grid grid-cols-1 sm:grid-cols-2 gap-4 list-none p-0 m-0">
    {images.map((image) => (
      <li>
        <figure>
          <img
            src={image.src}
            alt=""
            class="w-full h-auto object-cover rounded-sm"
            loading="lazy"
          />
        </figure>
      </li>
    ))}
  </ul>
)}
```

(Alt text empty in v1 — no captions; keep decorative. Prefer `alt={image.name}` only if filename is human-readable; default empty is OK for unlabeled family snaps.)

- [ ] **Step 7: Commit**

```bash
git add src/content src/lib src/components/UpdateCard.astro src/components/GalleryGrid.astro public/images
git commit -m "Add content collection schema, gallery helper, and image folders"
```

---

### Task 4: All pages

**Files:**
- Modify: `src/pages/index.astro`
- Create: `src/pages/trivan.astro`, `src/pages/om-familien.astro`, `src/pages/markus/index.astro`, `src/pages/markus/forloeb/index.astro`, `src/pages/markus/forloeb/[slug].astro`, `src/pages/markus/galleri.astro`, `src/pages/markus/diplomer.astro`

Shared page shell pattern: `mx-auto max-w-3xl px-4 py-12` (galleries may use `max-w-5xl`).

- [ ] **Step 1: Forside `src/pages/index.astro`**

- Large brand heading: **Sølvsten Bjerring**
- One short paragraph explaining the site (Danish): private family site for updates and photos
- Full-bleed or near full-width house image: try `/images/hjem/hus.jpg` (document filename in README). If missing, show a calm mist-colored placeholder block with text “Billede kommer snart” — do **not** break the build

Implementation tip for optional image without fs in the page:

```astro
---
import BaseLayout from '../layouts/BaseLayout.astro';
import { listPublicImages } from '../lib/gallery';

const homeImages = listPublicImages('hjem');
const hero = homeImages[0];
---
<BaseLayout title="Sølvsten Bjerring" description="Velkommen til familiens hjemmeside.">
  <section class="relative">
    {hero ? (
      <img src={hero.src} alt="Vores hus" class="w-full max-h-[70vh] object-cover" />
    ) : (
      <div class="w-full min-h-[40vh] bg-mist flex items-center justify-center text-sea">
        Billede kommer snart
      </div>
    )}
  </section>
  <section class="mx-auto max-w-2xl px-4 py-12 text-center">
    <h1 class="text-4xl md:text-5xl text-deep">Sølvsten Bjerring</h1>
    <p class="mt-4 text-lg text-sea leading-relaxed">
      Hvad sker der egentlig for tiden hos familien Sølvsten Bjerring? Det er hemmeligt! 
      Så hvis du har fundet vej herind, så hold det for dig selv!
    </p>
  </section>
</BaseLayout>
```

Adjust composition so brand is hero-level (per design preference): image first or soft background; keep first viewport to brand + one sentence + image — no extra marketing blocks.

- [ ] **Step 2: `src/pages/trivan.astro`**

Title Trivan; body only: “Kommer senere.”

- [ ] **Step 3: `src/pages/om-familien.astro`**

Short placeholder Danish paragraphs (editable later) about the family — a few sentences, not lorem ipsum Latin. Empty-ish but readable.

- [ ] **Step 4: `src/pages/markus/index.astro`**

Short intro about Markus + three clear links to Forløb, Galleri, Diplomer.

- [ ] **Step 5: `src/pages/markus/forloeb/index.astro`**

```astro
---
import { getCollection } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';
import UpdateCard from '../../../components/UpdateCard.astro';

const posts = (await getCollection('opdateringer')).sort(
  (a, b) => b.data.date.valueOf() - a.data.date.valueOf(),
);
---
<BaseLayout title="Forløb" description="Opdateringer om Markus’ forløb.">
  <div class="mx-auto max-w-3xl px-4 py-12">
    <h1 class="text-4xl text-deep">Forløb</h1>
    <p class="mt-3 text-sea">Løbende opdateringer om Markus.</p>
    {posts.length === 0 ? (
      <p class="mt-10 text-sea text-lg">Ingen opdateringer endnu.</p>
    ) : (
      <div class="mt-8">
        {posts.map((post) => (
          <UpdateCard
            title={post.data.title}
            date={post.data.date}
            summary={post.data.summary}
            href={`/markus/forloeb/${post.slug}/`}
          />
        ))}
      </div>
    )}
  </div>
</BaseLayout>
```

- [ ] **Step 6: `src/pages/markus/forloeb/[slug].astro`**

```astro
---
import { getCollection, render } from 'astro:content';
import BaseLayout from '../../../layouts/BaseLayout.astro';

export async function getStaticPaths() {
  const posts = await getCollection('opdateringer');
  return posts.map((post) => ({
    params: { slug: post.slug },
    props: { post },
  }));
}

const { post } = Astro.props;
const { Content } = await render(post);
const formatted = post.data.date.toLocaleDateString('da-DK', {
  year: 'numeric',
  month: 'long',
  day: 'numeric',
});
---
<BaseLayout title={post.data.title} description={post.data.summary}>
  <article class="mx-auto max-w-2xl px-4 py-12">
    <p class="text-sm text-sea">
      <a href="/markus/forloeb/" class="hover:underline">← Forløb</a>
    </p>
    <time class="mt-6 block text-sm text-sea" datetime={post.data.date.toISOString()}>
      {formatted}
    </time>
    <h1 class="mt-2 text-4xl text-deep">{post.data.title}</h1>
    <div class="prose prose-lg mt-8 max-w-none text-deep/90 leading-relaxed">
      <Content />
    </div>
  </article>
</BaseLayout>
```

Prose styles are already in `global.css` from Task 1 — do not add `@tailwindcss/typography`.

- [ ] **Step 7: `src/pages/markus/galleri.astro` and `diplomer.astro`**

Use `listPublicImages('markus/galleri')` / `listPublicImages('markus/diplomer')` + `GalleryGrid` with empty messages “Ingen billeder endnu.” / “Ingen diplomer endnu.”

- [ ] **Step 8: Build verification**

Run: `npm run build`  
Expected: Success; `dist/` contains `index.html`, `trivan/`, `om-familien/`, `markus/`, `markus/forloeb/`, `markus/galleri/`, `markus/diplomer/`. No forløb slug pages until posts exist (OK).

- [ ] **Step 9: Commit**

```bash
git add src/pages src/styles/global.css
git commit -m "Add all site pages with empty content states"
```

---

### Task 5: GitHub Pages deploy + README

**Files:**
- Create: `.github/workflows/deploy.yml`, `README.md`
- Optionally defer `CNAME` until DNS is ready (document in README)

- [ ] **Step 1: Create `.github/workflows/deploy.yml`**

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [main]
  workflow_dispatch:

permissions:
  contents: read
  pages: write
  id-token: write

concurrency:
  group: pages
  cancel-in-progress: false

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run build
      - uses: actions/upload-pages-artifact@v3
        with:
          path: dist

  deploy:
    needs: build
    runs-on: ubuntu-latest
    environment:
      name: github-pages
      url: ${{ steps.deployment.outputs.page_url }}
    steps:
      - id: deployment
        uses: actions/deploy-pages@v4
```

- [ ] **Step 2: Write `README.md` (Danish)**

Must cover:
1. Local: `npm install`, `npm run dev`, `npm run build`
2. Add update: create `src/content/opdateringer/mit-indlaeg.md` with frontmatter `title`, `date`, `summary` + Markdown body; optional images in `public/images/markus/forloeb/` referenced as `/images/markus/forloeb/fil.jpg`
3. Add gallery photo: drop into `public/images/markus/galleri/`
4. Add diploma: drop into `public/images/markus/diplomer/`
5. Homepage house photo: put file in `public/images/hjem/` (first image by filename is used)
6. Push to `main` → GitHub Actions deploys
7. Domain: enable GitHub Pages (Source: GitHub Actions); add `CNAME` with `www.solvstenbjerring.dk` and point DNS when ready

- [ ] **Step 3: Final build**

Run: `npm run build`  
Expected: PASS

- [ ] **Step 4: Commit**

```bash
git add .github/workflows/deploy.yml README.md
git commit -m "Add GitHub Pages workflow and content authoring README"
```

---

### Task 6: Sanity check with one temporary post (optional, delete before finish)

- [ ] **Step 1: Add a temporary Markdown post, build, confirm `/markus/forloeb/<slug>/` exists, then delete the post and rebuild** so the shipped tree stays empty of sample content (per spec: empty structures).

- [ ] **Step 2: If any fix was needed, commit the fix**

```bash
git commit -m "Fix forløb rendering edge case"
```

---

## Self-review checklist

- [x] Spec routes covered by Task 4
- [x] Content collection + empty states covered
- [x] Gallery drop-folder via `listPublicImages` covered
- [x] Coastal blue-grey tokens in global.css
- [x] Deploy + README covered
- [x] Out of scope (i18n, Trivan content, homepage latest updates, auth) not planned
- [x] No TBD/placeholder steps remaining

---

## Execution handoff

Plan complete and saved to `docs/superpowers/plans/2026-08-04-solvstenbjerring-website.md`.

**Two execution options:**

1. **Subagent-Driven (recommended)** — fresh subagent per task, review between tasks  
2. **Inline Execution** — implement in this session with checkpoints  

Which approach?
