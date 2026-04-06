# Domo Deck Theme Reference

Complete CSS, HTML patterns, and inline assets for Domo-branded slide decks. Referenced by the main SKILL.md during Phase 1.

## Inline Domo Logo (SVG)

Use this SVG directly in `<img>` tags via a data URI. No external file needed.

```html
<img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 120 120'%3E%3Crect width='120' height='120' rx='12' fill='%237BAED4'/%3E%3Ctext x='60' y='72' text-anchor='middle' font-family='Arial,Helvetica,sans-serif' font-weight='700' font-size='36' fill='white' letter-spacing='2'%3EDOMO%3C/text%3E%3C/svg%3E" alt="Domo">
```

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

/* --- FOOTER --- */
.slide-footer {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 52px;
  display: flex;
  align-items: center;
  padding: 0 40px;
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

/* --- PRINT --- */
@media print {
  body { background: white; gap: 0; padding: 0; }
  .slide { box-shadow: none; page-break-after: always; page-break-inside: avoid; }
  *, *::before, *::after { box-shadow: none !important; -webkit-box-shadow: none !important; }
}
```

## HTML Head

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DECK_TITLE</title>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;600;700;800&display=swap" rel="stylesheet">
<style>
  /* Paste Complete CSS here */
</style>
</head>
<body>
```

## Cover Slide Pattern

The cover slide uses a gradient background with subtle sparkle effects, a large Domo logo top-left, title + bullets on the left, and optional summary cards on the right.

```html
<div class="slide cover-slide">
  <div class="cover-logo">
    <img src="DATA_URI_LOGO" alt="Domo">
  </div>
  <div class="cover-body">
    <div class="cover-left">
      <h1>Deck Title<br>Goes Here</h1>
      <div class="cover-sub">
        A one-line description of this deck's purpose.
      </div>
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
      <div class="cover-card" style="border-left-color: var(--accent-coral);">
        <div class="cc-title">Section Four</div>
        <div class="cc-sub">SHORT DESCRIPTOR</div>
      </div>
    </div>
  </div>
  <div class="cover-footer">Confidential</div>
</div>
```

Replace `DATA_URI_LOGO` with the inline SVG data URI from the top of this file.

## Content Slide Pattern

```html
<div class="slide">
  <div class="slide-header">
    <h1>Slide Title</h1>
    <div class="subtitle">UPPERCASE SUBTITLE</div>
  </div>
  <div class="slide-content" style="position:absolute; top:100px; left:0; right:0; bottom:52px; padding:24px 48px; display:flex; flex-direction:column;">
    <!-- slide body -->
  </div>
  <div class="slide-footer">
    <span class="confidential">Confidential</span>
    <span class="footer-line"></span>
    <span class="domo-badge">
      <span class="page-num">2</span>
      <img src="DATA_URI_LOGO" alt="Domo">
    </span>
  </div>
</div>
```

## Content Slide with Background

Use `has-bg` class for slides that need the light blue-gray content area:

```html
<div class="slide">
  <div class="slide-header">
    <h1>Slide Title</h1>
    <div class="subtitle">UPPERCASE SUBTITLE</div>
  </div>
  <div class="slide-content has-bg">
    <!-- content auto-fills from top:90px to bottom:52px with #DDE5ED background -->
  </div>
  <div class="slide-footer">
    <span class="confidential">Confidential</span>
    <span class="footer-line"></span>
    <span class="domo-badge">
      <span class="page-num">3</span>
      <img src="DATA_URI_LOGO" alt="Domo">
    </span>
  </div>
</div>
```

## Flow Diagram Pattern

Four-phase pipeline with arrows:

```html
<div class="flow-row">
  <div class="flow-box fb-intake">
    <div class="flow-num">Phase 1</div>
    <div class="flow-title">Intake</div>
    <div class="flow-desc">Description text here.</div>
  </div>
  <span class="flow-arrow">&#9654;</span>
  <div class="flow-box fb-review">
    <div class="flow-num">Phase 2</div>
    <div class="flow-title">Review</div>
    <div class="flow-desc">Description text here.</div>
  </div>
  <span class="flow-arrow">&#9654;</span>
  <div class="flow-box fb-optimize">
    <div class="flow-num">Phase 3</div>
    <div class="flow-title">Optimize</div>
    <div class="flow-desc">Description text here.</div>
  </div>
  <span class="flow-arrow">&#9654;</span>
  <div class="flow-box fb-amplify">
    <div class="flow-num">Phase 4</div>
    <div class="flow-title">Amplify</div>
    <div class="flow-desc">Description text here.</div>
  </div>
</div>
```

## Accent Color Usage

| Element | Color variable | Hex |
|---------|---------------|-----|
| Primary / headers / links | `--domo-blue` | `#7BAED4` |
| Phase 1 / Intake | `--accent-orange` | `#E8A44A` |
| Phase 2 / Review | `--accent-green` | `#6BBF8A` |
| Phase 3 / Optimize | `--accent-coral` | `#E07A6A` |
| Phase 4 / Amplify | `--accent-purple` | `#9B8EC4` |
| Titles | `--title-black` | `#1E1E1E` |
| Body text | `--text-dark` | `#2C2C2C` |
| Secondary text | `--text-mid` | `#4A4A4A` |
| Muted text | `--text-light` | `#6B6B6B` |
