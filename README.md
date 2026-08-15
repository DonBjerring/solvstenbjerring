# Sølvsten Bjerring

Familiehjemmeside til [https://sølvstenbjerring.dk](https://sølvstenbjerring.dk) — Astro 7 + Tailwind CSS 4, statisk build, hostet på GitHub Pages.

Indhold tilføjes som Markdown og billed-/lydfiler.

## Kom i gang lokalt

```bash
npm install
npm run dev
```

Åbn den adresse, terminalen viser (typisk http://localhost:4321).

```bash
npm run build    # byg til mappen dist/
npm run preview  # forhåndsvis det byggede site
```

## Menustruktur

| Menu | URL |
|------|-----|
| Forside | `/` |
| Trivan | `/trivan/` |
| Markus → Oversigt | `/markus/` |
| Markus → Indlæggelsesforløb | `/markus/story/` |
| Markus → Galleri | `/markus/gallery/` |
| Markus → Diplomer | `/markus/diplomas/` |
| Sanghæfte | `/hymns/` |
| Om familien | `/about/` |

## Mapper (hurtigt overblik)

```
src/content/story/          ← indlæggelsesforløb (Markdown)
src/content/hymns/          ← sanghæfte (Markdown)
public/images/home/         ← forsidebillede
public/images/trivan/       ← Trivan-billede
public/images/markus/story/ ← billeder til indlæg
public/images/markus/gallery/
public/images/markus/diplomas/
public/audio/hymns/         ← valgfrie melodier til sange
scripts/rename-images-by-date.py
```

## Tilføj et indlæg (Indlæggelsesforløb)

1. Læg evt. billede i `public/images/markus/story/` (gerne `YYYYMMDD-HHMMSS.jpg` via rename-scriptet).
2. Opret en fil i `src/content/story/`, fx `20260814.md`:

```markdown
---
image: 20260814-074319.jpg
date: 2026-08-14
title: Valgfri overskrift
summary: Kort teaser til listen
text: |
  Her er teksten til indlægget.
  Den kan fylde flere linjer.
---
```

Alle felter er valgfrie:

- **`image`** — filnavn i `public/images/markus/story/`. Listen viser et lille billedikon ud for datoen, når feltet er sat.
- **`date`** — styrer sortering og dato på siden. Hvis den mangler, udledes datoen fra billedfilnavnet, når det er muligt.
- **`title`** — overskrift. Uden den vises kun datoen.
- **`summary`** — teaser på oversigten.
- **`text`** — brødtekst (kan også skrives som markdown-body under frontmatter).

På indlægssiden er der forrige/næste-navigation. Billeder har skeleton-loading mens de hentes.

3. Commit og push til `main`.

## Tilføj en sang (Sanghæfte)

1. Opret en fil i `src/content/hymns/`, fx `elefantens-vuggevise.md`:

```markdown
---
title: Elefantens vuggevise
section: lullabies   # songs = Sange, lullabies = Godnatsange
melody: Navn på komponist   # valgfri
lyrics: Navn på tekstforfatter  # valgfri
note: Godnatsang            # valgfri personlig note
audio: elefantens-vuggevise.mp3  # valgfri — fil i public/audio/hymns/
---

Første linje
Anden linje
Tredje linje
```

- `section` skal være `songs` eller `lullabies`.
- Listen er alfabetisk inden for hver sektion; notes vises kun på sangsiden.
- Linjeskift i teksten bevares.
- `melody` / `lyrics` vises som “Melodi: … · Tekst: …” under titlen.

**Lyd (valgfri):** læg fx `elefantens-vuggevise.mp3` i `public/audio/hymns/` og sæt `audio:` i frontmatter. Så vises “Hør melodi”. Brug kun lyd I har ret til at dele.

**På sangsiden:** “Jeg synger” (holder skærmen vågen) + valgfri autoscroll (Ingen / Langsom / Middel / Hurtig), forrige/næste-sang, og melodi-knap når `audio` er sat.

2. Commit og push til `main`.

## Tilføj billeder til galleri

Læg filer (`.jpg`, `.jpeg`, `.png`, `.webp`, …) i:

`public/images/markus/gallery/`

De vises automatisk (sorteret efter filnavn). Klik for større visning. Skeleton-loading mens billederne hentes.

### Omdøb efter dato

```bash
# Se hvad der vil ske
python3 scripts/rename-images-by-date.py public/images/markus/gallery

# Udfør omdøbning
python3 scripts/rename-images-by-date.py public/images/markus/gallery --apply
```

Virker også på andre mapper, fx `public/images/markus/diplomas` og `public/images/markus/story`.

## Tilføj diplomer

Læg billeder i `public/images/markus/diplomas/`.

Nummerér filerne for at styre rækkefølgen, fx:

```
01-first.jpg
02-second.jpg
03-third.jpg
```

Sorteres efter filnavn. Klik for større visning.

## Forside- og Trivan-billede

| Side | Mappe | Regel |
|------|--------|--------|
| Forside | `public/images/home/` | Første fil (alfabetisk) bruges |
| Trivan | `public/images/trivan/` | Første fil (alfabetisk) bruges |

## Publicering (GitHub Pages)

1. Push til `main` (eller kør workflowen manuelt).
2. På GitHub: **Settings → Pages → Source: GitHub Actions**.
3. Brug workflowen **Deploy to GitHub Pages** (`.github/workflows/deploy.yml`).
4. Live: [https://sølvstenbjerring.dk](https://sølvstenbjerring.dk)

Custom domain står i `public/CNAME`. DNS går via Cloudflare til GitHub Pages (`www` kan redirecte til apex).

Deploy afbryder en igangværende deploy ved ny push (`cancel-in-progress: true`), så den nyeste version kommer hurtigere live.
