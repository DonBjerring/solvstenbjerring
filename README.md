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

1. Opret en ny fil i `src/content/story/`, fx `first-week.md`
2. Start filen med:

```markdown
---
title: "Første uge"
date: 2026-08-01
summary: "En kort teaser til listen"
---

Her skriver I brødteksten. I kan bruge **fed**, lister og billeder.
```

3. Valgfrit billede i indlægget: læg filen i `public/images/markus/story/` og indsæt i Markdown (husk base-path på GitHub Pages):

```markdown
![Beskrivelse](/solvstenbjerring/images/markus/story/my-photo.jpg)
```

Når det egne domæne er koblet på (`base: '/'`), brug i stedet:

```markdown
![Beskrivelse](/images/markus/story/my-photo.jpg)
```

4. Commit og push til `main` — siden opdateres automatisk.

## Tilføj billeder til galleri

Læg billedfiler (`.jpg`, `.jpeg`, `.png`, `.webp`, …) i:

`public/images/markus/gallery/`

De vises automatisk på Galleri-siden (sorteret efter filnavn). Ingen billedtekster i v1.

## Tilføj diplomer

Læg billeder i:

`public/images/markus/diplomas/`

## Forsidebillede

Læg billedet i:

`public/images/home/`

Det første billede (alfabetisk efter filnavn) bruges på forsiden.

## Publicering (GitHub Pages)

1. Push til `main`
2. På GitHub: **Settings → Pages → Source: GitHub Actions**
3. Brug kun workflowen **Deploy to GitHub Pages** (`.github/workflows/deploy.yml`) — ikke “Deploy static content”
4. Siden ligger midlertidigt på: `https://donbjerring.github.io/solvstenbjerring/`

### Domæne senere (`www.solvstenbjerring.dk`)

Når DNS er klar:

1. I `astro.config.mjs`: sæt `base: '/'` og `site: 'https://www.solvstenbjerring.dk'`
2. Opret filen `CNAME` i repo-roden med indholdet `www.solvstenbjerring.dk`
3. Peg DNS hos domæneudbyderen til GitHub Pages

## Menustruktur

- Forside → `/`
- Trivan → `/trivan/`
- Markus → `/markus/` (Indlæggelsesforløb `/markus/story/`, Galleri `/markus/gallery/`, Diplomer `/markus/diplomas/`)
- Om familien → `/about/`
