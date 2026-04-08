# Domo Deck Theme Reference

Complete CSS, HTML skeleton, and patterns for Domo-branded slide decks. This file is the single source of truth — copy the skeleton below and start adding content.

## Domo Logo

The actual Domo logo PNG is at `assets/domologo.png` (relative to this skill). For inline embedding so the HTML works without external files, read the full base64 data URI from `assets/logo-data-uri.txt` and use it in `<img src="...">` tags.

**Critical**: Every content slide footer AND the cover slide must show the Domo logo. Replace every `LOGO_DATA_URI` placeholder below with the contents of `assets/logo-data-uri.txt`.

## Complete CSS

Paste this entire `<style>` block into the `<head>` of the deck HTML.

```css
*, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

:root {
  --domo-blue: #7BAED4;
  --domo-blue-dark: #5A92BA;
  --title-black: #1E1E1E;
  --subtitle-blue: #7BAED4;
  --content-bg: #DDE5ED;
  --text-dark: #2C2C2C;
  --text-mid: #4A4A4A;
  --text-light: #6B6B6B;
  --white: #FFFFFF;
  --slide-w: 1024px;
  --slide-h: 576px;
  --accent-green: #6BBF8A;
  --accent-orange: #E8A44A;
  --accent-coral: #E07A6A;
  --accent-purple: #9B8EC4;
}

body {
  font-family: 'Open Sans', sans-serif;
  background: #E8E8E8;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 32px;
  padding: 32px 0;
  -webkit-font-smoothing: antialiased;
}

.slide {
  width: var(--slide-w);
  height: var(--slide-h);
  background: var(--white);
  position: relative;
  overflow: hidden;
  flex-shrink: 0;
  box-shadow: 0 4px 24px rgba(0,0,0,0.12);
}

/* --- FOOTER (every content slide) --- */
.slide-footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 52px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 32px;
}
.slide-footer .confidential {
  font-size: 8px;
  font-weight: 600;
  letter-spacing: 2.5px;
  text-transform: uppercase;
  color: #AAAAAA;
}
.slide-footer .footer-line {
  flex: 1;
  height: 1px;
  background: #D0D0D0;
  margin: 0 24px;
}
.slide-footer .domo-badge {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}
.slide-footer .domo-badge img {
  height: 28px;
  width: auto;
  border-radius: 3px;
}
.slide-footer .page-num {
  font-size: 9px;
  font-weight: 600;
  color: #B0B0B0;
  margin-bottom: 2px;
  letter-spacing: 0.5px;
}

/* --- HEADER --- */
.slide-header {
  padding: 28px 40px 0 40px;
}
.slide-header h1 {
  font-size: 26px;
  font-weight: 700;
  color: var(--title-black);
  line-height: 1.2;
}
.slide-header .subtitle {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--subtitle-blue);
  margin-top: 4px;
}
.slide-header .header-line {
  height: 1px;
  background: #D0D0D0;
  margin-top: 14px;
}

/* --- CONTENT AREA --- */
.slide-content {
  padding: 20px 40px 0 40px;
}
.slide-content.has-bg {
  position: absolute;
  top: 90px; left: 0; right: 0; bottom: 52px;
  padding: 24px 40px;
  background: var(--content-bg);
  display: flex;
  flex-direction: column;
  justify-content: center;
}

/* --- COVER SLIDE --- */
.cover-slide {
  background: linear-gradient(135deg, #E8DFF0 0%, #D4DEF0 25%, #E0E8F4 40%, #EDE4F0 55%, #D8E4F2 75%, #E4DDF0 100%);
}
.cover-slide::before {
  content: '';
  position: absolute;
  inset: 0;
  background:
    radial-gradient(2px 2px at 15% 25%, rgba(255,255,255,0.8), transparent),
    radial-gradient(3px 3px at 35% 60%, rgba(255,255,255,0.6), transparent),
    radial-gradient(2px 2px at 55% 15%, rgba(255,255,255,0.7), transparent),
    radial-gradient(4px 4px at 70% 45%, rgba(255,255,255,0.5), transparent),
    radial-gradient(2px 2px at 25% 80%, rgba(255,255,255,0.6), transparent),
    radial-gradient(3px 3px at 85% 70%, rgba(255,255,255,0.4), transparent),
    radial-gradient(150px 150px at 20% 40%, rgba(255,255,255,0.15), transparent),
    radial-gradient(200px 200px at 60% 70%, rgba(200,180,220,0.12), transparent),
    radial-gradient(180px 180px at 80% 30%, rgba(180,200,230,0.1), transparent);
  pointer-events: none;
}
.cover-logo { position: absolute; top: 28px; left: 40px; }
.cover-logo img { height: 112px; width: auto; border-radius: 10px; }
.cover-body {
  position: absolute; inset: 0;
  display: flex;
  padding: 0 40px;
}
.cover-left {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-top: 20px;
}
.cover-left h1 {
  font-size: 38px;
  font-weight: 800;
  color: var(--title-black);
  line-height: 1.15;
  max-width: 480px;
}
.cover-left .cover-sub {
  font-size: 14px;
  color: var(--text-mid);
  margin-top: 14px;
  max-width: 400px;
  line-height: 1.5;
}
.cover-left .cover-bullets {
  list-style: none; padding: 0; margin-top: 20px;
}
.cover-left .cover-bullets li {
  font-size: 13px;
  color: var(--text-dark);
  padding-left: 14px;
  position: relative;
  margin-bottom: 5px;
}
.cover-left .cover-bullets li::before {
  content: '\2022';
  position: absolute; left: 0;
  color: var(--text-mid);
}
.cover-right {
  width: 310px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 12px;
  padding: 48px 0 48px 24px;
}
.cover-card {
  background: var(--white);
  border-radius: 6px;
  padding: 22px;
  border-left: 5px solid transparent;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.cover-card .cc-title { font-size: 18px; font-weight: 700; color: var(--title-black); }
.cover-card .cc-sub {
  font-size: 9px; font-weight: 700; letter-spacing: 2.5px;
  text-transform: uppercase; color: var(--text-light); margin-top: 5px;
}
.cover-footer {
  position: absolute;
  bottom: 12px; left: 0; right: 0;
  text-align: center;
  font-size: 8px; font-weight: 600; letter-spacing: 3px;
  text-transform: uppercase; color: #AAAAAA;
}

/* --- TYPOGRAPHY --- */
.label {
  font-size: 9px; font-weight: 700; letter-spacing: 2px;
  text-transform: uppercase; color: var(--subtitle-blue); margin-bottom: 8px;
}
.section-label { font-size: 15px; font-weight: 700; color: var(--title-black); margin-bottom: 6px; }
.body-text { font-size: 13px; color: var(--text-dark); line-height: 1.65; }

/* --- TABLE --- */
.deck-table { width: 100%; border-collapse: collapse; font-size: 11px; margin-top: 8px; }
.deck-table th {
  text-align: left; font-weight: 700; font-size: 9px; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--subtitle-blue);
  padding: 7px 10px; border-bottom: 1.5px solid #C8D4DF;
}
.deck-table td {
  padding: 7px 10px; color: var(--text-dark);
  border-bottom: 1px solid #E8ECF0; vertical-align: top; line-height: 1.5;
}
.deck-table tr:last-child td { border-bottom: none; }

/* --- CARDS --- */
.card-row { display: flex; gap: 14px; margin-top: 12px; }
.card {
  flex: 1; background: var(--white); border-radius: 6px;
  padding: 16px; border: 1px solid #D8DFE6;
}
.card .card-title { font-size: 12px; font-weight: 700; color: var(--title-black); margin-bottom: 6px; }
.card .card-body { font-size: 10.5px; color: var(--text-mid); line-height: 1.55; }

/* --- BULLET LIST --- */
.bullet-list { list-style: none; padding: 0; }
.bullet-list li {
  position: relative; padding-left: 16px; margin-bottom: 7px;
  font-size: 12px; color: var(--text-dark); line-height: 1.55;
}
.bullet-list li::before {
  content: ''; position: absolute; left: 0; top: 7px;
  width: 6px; height: 6px; border-radius: 50%; background: var(--domo-blue);
}

/* --- FLOW DIAGRAM --- */
.flow-row { display: flex; align-items: center; justify-content: center; gap: 0; margin: 24px 0 16px; }
.flow-box { width: 170px; padding: 18px 16px; border-radius: 6px; text-align: center; }
.flow-box .flow-num { font-size: 10px; font-weight: 700; letter-spacing: 2px; text-transform: uppercase; opacity: 0.7; margin-bottom: 4px; }
.flow-box .flow-title { font-size: 16px; font-weight: 700; margin-bottom: 4px; }
.flow-box .flow-desc { font-size: 10px; line-height: 1.4; opacity: 0.8; }
.flow-arrow { font-size: 22px; color: #B0B0B0; margin: 0 4px; }
.fb-intake  { background: #E3F0FA; color: #2A6FA0; }
.fb-review  { background: #FFF3E0; color: #B87A1A; }
.fb-optimize{ background: #E8F5E9; color: #3A7D44; }
.fb-amplify { background: #F3E5F5; color: #7B3F9E; }

/* --- SECTION DIVIDER --- */
.section-slide {
  display: flex; flex-direction: column; justify-content: center; padding: 0 64px;
}
.section-slide .section-num {
  font-size: 14px; font-weight: 700; letter-spacing: 3px;
  text-transform: uppercase; color: var(--domo-blue); margin-bottom: 8px;
}
.section-slide h1 { font-size: 36px; font-weight: 800; color: var(--title-black); line-height: 1.15; }
.section-slide .section-desc {
  font-size: 15px; color: var(--text-mid); margin-top: 12px; max-width: 640px; line-height: 1.6;
}
.section-slide .section-accent {
  width: 48px; height: 3px; background: var(--domo-blue); margin-top: 20px; border-radius: 2px;
}

/* --- SCORE BAR --- */
.score-row { display: flex; align-items: center; margin-bottom: 6px; }
.score-label { width: 150px; font-size: 11px; font-weight: 600; color: var(--text-dark); flex-shrink: 0; }
.score-bar-track { flex: 1; height: 14px; background: #E8ECF0; border-radius: 7px; overflow: hidden; margin: 0 10px; }
.score-bar-fill { height: 100%; border-radius: 7px; background: var(--domo-blue); }
.score-value { width: 36px; font-size: 12px; font-weight: 700; color: var(--title-black); text-align: right; flex-shrink: 0; }

/* --- QUICK WIN TABLE --- */
.qw-table { width: 100%; border-collapse: collapse; font-size: 11.5px; margin-top: 10px; }
.qw-table th {
  text-align: left; font-weight: 700; font-size: 9px; letter-spacing: 1.5px;
  text-transform: uppercase; color: var(--white); background: var(--domo-blue); padding: 8px 12px;
}
.qw-table th:first-child { border-radius: 4px 0 0 0; }
.qw-table th:last-child { border-radius: 0 4px 0 0; }
.qw-table td { padding: 8px 12px; color: var(--text-dark); border-bottom: 1px solid #E8ECF0; vertical-align: top; line-height: 1.5; }
.qw-table tr:nth-child(even) td { background: #F6F8FA; }

/* --- PRINT --- */
@media print {
  body { background: white; gap: 0; padding: 0; }
  .slide { box-shadow: none; page-break-after: always; page-break-inside: avoid; }
  *, *::before, *::after { box-shadow: none !important; -webkit-box-shadow: none !important; }
}
```

## Complete Skeleton HTML

Copy this entire HTML file as your starting point. **Every content slide uses `has-bg` (gray background) by default.** This is the Domo slide look — do NOT use plain white slides unless specifically requested. Content is automatically vertically centered. Replace every `LOGO_DATA_URI` with the contents of `references/assets/logo-data-uri.txt`.

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DECK_TITLE</title>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
  /* Paste the Complete CSS block above here */
</style>
</head>
<body>

<!-- SLIDE: Standard content slide — USE THIS FOR EVERY CONTENT SLIDE -->
<div class="slide">
  <div class="slide-header">
    <h1>Slide Title</h1>
    <div class="subtitle">SLIDE SUBTITLE OR DESCRIPTION</div>
    <div class="header-line"></div>
  </div>
  <div class="slide-content has-bg">
    <!-- Content is vertically centered in the #DDE5ED gray area automatically -->
  </div>
  <div class="slide-footer">
    <span class="confidential">Confidential</span>
    <span class="footer-line"></span>
    <span class="domo-badge">
      <img src="LOGO_DATA_URI" alt="Domo">
    </span>
  </div>
</div>

</body>
</html>
```

## Slide Anatomy — Mandatory Elements

Every content slide MUST have all three layers. Missing any one breaks the layout.

| Layer | Element | Purpose |
|-------|---------|---------|
| **Header** | `<div class="slide-header">` with `<h1>`, `.subtitle`, and **`.header-line`** | Title + blue subtitle + thin gray separator |
| **Content** | `<div class="slide-content has-bg">` — **always use `has-bg`** | Gray background, vertically centered content |
| **Footer** | `<div class="slide-footer">` with `.confidential`, `.footer-line`, `.domo-badge` + `<img>` | "CONFIDENTIAL" left, gray line center, **Domo logo bottom-right** |

**The `.header-line` div is required** — it produces the thin gray separator visible in every slide.

**The Domo logo `<img>` in `.domo-badge` is required** — bottom-right of every content slide.

## Cover Slide Pattern

Insert as the first slide. Uses the same `LOGO_DATA_URI`.

```html
<div class="slide cover-slide">
  <div class="cover-logo">
    <img src="LOGO_DATA_URI" alt="Domo">
  </div>
  <div class="cover-body">
    <div class="cover-left">
      <h1>Deck Title<br>Goes Here</h1>
      <div class="cover-sub">One-line description of this deck's purpose.</div>
      <ul class="cover-bullets">
        <li>Key point one.</li>
        <li>Key point two.</li>
        <li>Key point three.</li>
      </ul>
    </div>
    <div class="cover-right">
      <div class="cover-card" style="border-left-color: var(--accent-orange);">
        <div class="cc-title">Section One</div>
        <div class="cc-sub">SHORT DESCRIPTOR</div>
      </div>
      <div class="cover-card" style="border-left-color: var(--accent-green);">
        <div class="cc-title">Section Two</div>
        <div class="cc-sub">SHORT DESCRIPTOR</div>
      </div>
      <div class="cover-card" style="border-left-color: var(--domo-blue);">
        <div class="cc-title">Section Three</div>
        <div class="cc-sub">SHORT DESCRIPTOR</div>
      </div>
    </div>
  </div>
  <div class="cover-footer">Confidential</div>
</div>
```

## Adding Page Numbers

To show a page number above the logo in the footer:

```html
<span class="domo-badge">
  <span class="page-num">2</span>
  <img src="LOGO_DATA_URI" alt="Domo">
</span>
```

## `has-bg` Is the Default — Always

**Use `has-bg` on every content slide.** This is the Domo branded look — the gray `#DDE5ED` content area with vertically centered content. The `has-bg` class provides `position:absolute`, correct `top`/`bottom` bounds, `display:flex`, `flex-direction:column`, and `justify-content:center` automatically.

Do NOT use plain white slides unless the user explicitly requests it. The wealth-deck and initiatives-deck examples both demonstrate that every content slide should have the gray background.

## Accent Color Reference

| Element | Variable | Hex |
|---------|----------|-----|
| Primary / headers / links | `--domo-blue` | `#7BAED4` |
| Phase 1 / Intake | `--accent-orange` | `#E8A44A` |
| Phase 2 / Success | `--accent-green` | `#6BBF8A` |
| Phase 3 / Warnings | `--accent-coral` | `#E07A6A` |
| Phase 4 / Advanced | `--accent-purple` | `#9B8EC4` |
| Titles | `--title-black` | `#1E1E1E` |
| Body text | `--text-dark` | `#2C2C2C` |
| Secondary text | `--text-mid` | `#4A4A4A` |
| Muted text | `--text-light` | `#6B6B6B` |
| Content background | `--content-bg` | `#DDE5ED` |
