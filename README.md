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

## Tilføj en opdatering (Forløb)

1. Opret en ny fil i `src/content/opdateringer/`, fx `foerste-uge.md`
2. Start filen med:

```markdown
---
title: "Første uge"
date: 2026-08-01
summary: "En kort teaser til listen"
---

Her skriver I brødteksten. I kan bruge **fed**, lister og billeder.
```

3. Valgfrit billede i indlægget: læg filen i `public/images/markus/forloeb/` og indsæt i Markdown:

```markdown
![Beskrivelse](/images/markus/forloeb/mit-billede.jpg)
```

4. Commit og push til `main` — siden opdateres automatisk.

## Tilføj billeder til galleri

Læg billedfiler (`.jpg`, `.jpeg`, `.png`, `.webp`, …) i:

`public/images/markus/galleri/`

De vises automatisk på Galleri-siden (sorteret efter filnavn). Ingen billedtekster i v1.

## Tilføj diplomer

Læg billeder i:

`public/images/markus/diplomer/`

## Forsidebillede (huset)

Læg husbilledet i:

`public/images/hjem/`

Det første billede (alfabetisk efter filnavn) bruges på forsiden. Fx `hus.jpg`.

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

- Forside
- Trivan (kommer senere)
- Markus → Oversigt, Forløb, Galleri, Diplomer
- Om familien
