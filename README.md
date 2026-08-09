# Sølvsten Bjerring

Familiehjemmeside til www.solvstenbjerring.dk — bygget med Astro og Tailwind CSS, hostet på GitHub Pages.

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

## Tilføj en opdatering (Indlæggelsesforløb)

1. Læg evt. billede i `public/images/markus/story/` (gerne `YYYYMMDD-HHMMSS.jpg` via rename-scriptet)
2. Opret en fil i `src/content/story/`, fx `foerste-dag.md`:

```markdown
---
image: 20260513-160309.jpg
text: |
  Her er teksten til indlægget.
  Den kan fylde flere linjer.
# title: "Valgfri overskrift"
# summary: "Kort teaser til listen"
# date: 2026-05-13              # kun nødvendigt hvis der ikke er billede
---
```

Alle felter er valgfrie. `title` er kun en overskrift — uden den vises kun datoen (fra billedet).

3. Commit og push til `main` — siden opdateres automatisk.

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

`section` skal være `songs` eller `lullabies`. Enkelte linjeskift i teksten bevares på sangsiden. `melody` og `lyrics` vises som “Melodi: … · Tekst: …” under titlen.

Lydfil (valgfri): læg fx `elefantens-vuggevise.mp3` i `public/audio/hymns/` og sæt `audio:` i frontmatter. Afspilleren vises kun, når feltet er sat. Brug kun lyd I har ret til at dele.

2. Commit og push til `main`.

## Tilføj billeder til galleri

Læg billedfiler (`.jpg`, `.jpeg`, `.png`, `.webp`, …) i:

`public/images/markus/gallery/`

De vises automatisk på Galleri-siden (sorteret efter filnavn). Ingen billedtekster i v1.

### Omdøb efter dato

For ens filnavne (`YYYYMMDD-HHMMSS.jpg`):

```bash
# Se hvad der vil ske
python3 scripts/rename-images-by-date.py public/images/markus/gallery

# Udfør omdøbning
python3 scripts/rename-images-by-date.py public/images/markus/gallery --apply
```

Virker også på andre mapper, fx `public/images/markus/diplomas`.

## Tilføj diplomer

Læg billeder i:

`public/images/markus/diplomas/`

Nummerér filerne for at styre rækkefølgen, fx:

```
01-first.jpg
02-second.jpg
03-third.jpg
```

De sorteres efter filnavn. Klik på et billede for at se det større.

## Forsidebillede

Læg billedet i:

`public/images/home/`

Det første billede (alfabetisk efter filnavn) bruges på forsiden.

## Publicering (GitHub Pages)

1. Push til `main`
2. På GitHub: **Settings → Pages → Source: GitHub Actions**
3. Brug kun workflowen **Deploy to GitHub Pages** (`.github/workflows/deploy.yml`) — ikke “Deploy static content”
4. Siden ligger på: https://sølvstenbjerring.dk (`www` redirecter hertil)

Custom domain er sat via `public/CNAME` og DNS hos DanDomain (A-records til GitHub Pages + CNAME for `www` → `donbjerring.github.io`).

## Menustruktur

- Forside → `/`
- Trivan → `/trivan/`
- Markus → `/markus/` (Indlæggelsesforløb `/markus/story/`, Galleri `/markus/gallery/`, Diplomer `/markus/diplomas/`)
- Sanghæfte → `/hymns/`
- Om familien → `/about/`
