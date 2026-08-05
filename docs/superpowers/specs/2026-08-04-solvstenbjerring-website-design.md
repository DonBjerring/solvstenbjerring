# Sølvsten Bjerring — Family Website Design

**Date:** 2026-08-04  
**Status:** Approved  
**Domain:** www.solvstenbjerring.dk  

## Purpose

A simple, warm, personal family website for sharing photos and ongoing updates with close family and friends. Initial focus is Markus (newborn son) and his hospital journey, but the site structure supports other family sections (e.g. Trivan) later.

Not a business or corporate site. No database, no backend, no login.

## Audience and language

- **Audience:** Close family and friends (publicly reachable URL; warm, private tone)
- **Language:** Danish first; English left as a future option (no bilingual UI in v1)

## Approach

Astro static site + Tailwind CSS + Astro Content Collections for updates. Images in `public/`. Hosted free on GitHub Pages via GitHub Actions. Content is added by committing Markdown files and image files; a README documents the workflow.

## Site map and navigation

### Top-level nav

| Label | Route | Role |
|-------|-------|------|
| Forside | `/` | Short site intro + large house photo |
| Trivan | `/trivan/` | Placeholder: “Kommer senere” |
| Markus | `/markus/` (+ submenu) | Son’s section hub |
| Om familien | `/om-familien/` | Family text page |

### Markus submenu

| Label | Route | Role |
|-------|-------|------|
| Indlæggelsesforløb | `/markus/forloeb/` | Timeline/list of all updates |
| (single update) | `/markus/forloeb/[slug]/` | One update post |
| Galleri | `/markus/galleri/` | Photo gallery |
| Diplomer | `/markus/diplomer/` | Diploma/certificate images (gallery layout) |

### Homepage scope (v1)

Only a short explanation of the website and a large house image. No “latest updates” teaser on the homepage in v1.

## Content model

### Updates (`indlæggelsesforløb`)

- Stored as Markdown in `src/content/opdateringer/`
- Astro Content Collection with frontmatter:

```yaml
title: string
date: date
summary: string
```

- Body is Markdown
- Listed newest-first on `/markus/forloeb/`
- Empty state when no posts: calm “Ingen opdateringer endnu”

### Images

```
public/images/
  hjem/                 # house photo for homepage
  markus/galleri/       # gallery photos
  markus/diplomer/      # diploma/certificate images
```

- Galleri and Diplomer show empty states until files are added
- Homepage uses a designated house image path (documented in README); placeholder if missing

### Static pages

- Forside, Trivan, Markus hub, Om familien: Astro pages with Danish copy (editable in source)
- Trivan: only “Kommer senere” content in v1

## Technical architecture

### Stack

- Astro (static output)
- Tailwind CSS
- TypeScript where Astro scaffolding expects it
- GitHub Pages + GitHub Actions deploy on push to `main`

### Suggested file structure

```
src/
  layouts/BaseLayout.astro
  components/
    Header.astro
    Footer.astro
    UpdateCard.astro
    GalleryGrid.astro
  pages/
    index.astro
    trivan.astro
    om-familien.astro
    markus/
      index.astro
      forloeb/
        index.astro
        [slug].astro
      galleri.astro
      diplomer.astro
  content/
    config.ts
    opdateringer/
  styles/global.css
public/
  images/
    hjem/
    markus/galleri/
    markus/diplomer/
.github/workflows/deploy.yml
CNAME                          # www.solvstenbjerring.dk (when domain is wired)
README.md
astro.config.mjs
package.json
```

### GitHub Pages

- `astro.config.mjs`: `site` set to the production URL; `base` as needed for Pages (custom domain → typically `/`)
- Workflow builds with `npm ci` / `npm run build` and publishes `dist/`
- Custom domain via `CNAME` + DNS at registrar (setup after first deploy; not a blocker for local build)

## Visual design

- **Mood:** Soft coastal blue-grey — airy, calm, Nordic; warm and personal, not corporate
- **Palette (starting point, easy to tweak):** Cool off-white / soft blue-grey backgrounds; deep slate text; muted blue-grey accent
- **Typography:** Serif for headings; clean sans for body
- **Layout:** Generous whitespace; readable measure for update text; large images; mobile-first
- **Nav:** Desktop top nav with Markus dropdown; mobile hamburger
- **Empty states:** Quiet messaging, no broken-looking empty grids

Avoid: startup/purple gradients, dense dashboards, card-heavy corporate layouts.

## Content authoring workflow

Documented in README:

1. Add a new `.md` file under `src/content/opdateringer/` with required frontmatter
2. Add gallery/diploma images under the matching `public/images/...` folder
3. Commit and push to `main` → GitHub Actions publishes

No CMS, no database.

## Out of scope (v1)

- Comments, auth, search
- English UI / i18n
- Trivan real content
- Newsletter / contact forms
- Password protection
- Homepage “latest updates” section
- Backend or serverless APIs

## Success criteria

- Responsive on mobile and desktop
- Navigation works for all listed routes
- Empty Indlæggelsesforløb / Galleri / Diplomer are clear and calm
- New update = one Markdown file + push
- New gallery/diploma images = drop files in folder + push
- Site builds statically and is deployable to GitHub Pages
- Tone feels personal and family-oriented, not corporate
