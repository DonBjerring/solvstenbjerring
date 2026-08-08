# FSB Sanghæfte (hymns) — Design

**Date:** 2026-08-07  
**Status:** Approved  

## Purpose

A family songbook (“FSB Sanghæfte” = Familien Sølvsten Bjerring Sanghæfte) listing songs Markus is typically sung, with readable lyric pages. Internal project name: `hymns`.

## Navigation

- Menu label: **Sanghæfte**
- Placement: after Markus, before Om familien (same level as Trivan)
- Paths: `/hymns/` (list), `/hymns/[slug]/` (song)

## Content

Astro Content Collection `hymns` in `src/content/hymns/*.md`:

| Field | Required | Notes |
|-------|----------|--------|
| `title` | yes | Song title |
| `section` | yes | `songs` or `lullabies` |
| `note` | no | Short note (e.g. “Godnatsang”, “fra mormor”) |
| body | yes | Lyrics (markdown; preserve line breaks in display) |

## List page

- H1: FSB Sanghæfte
- Short intro
- Two sections: **Sange** then **Godnatsange**
- Each section sorted alphabetically by title (da locale)
- Each item links to the song page; show optional note as secondary text

## Song page

- Back link to `/hymns/`
- Title, optional note, lyrics
- Visual language matches existing story/list pages (`max-w-3xl`, sand/sea/deep)

## Authoring

Add a markdown file under `src/content/hymns/`, commit and push.
