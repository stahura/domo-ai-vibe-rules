---
name: html-deck
description: Build a professional HTML slide deck from source content and convert it to a pixel-perfect PDF. Covers slide architecture, layout patterns, print-safe CSS, Puppeteer PDF conversion, and quality verification. Use when creating presentation decks, converting documents to slide format, or generating PDF decks from HTML.
---

# HTML Slide Deck to PDF Workflow

Build polished, presentation-ready HTML slide decks and convert them to razor-sharp PDFs using headless Chrome.

## When to use

- Creating a new slide deck from program documentation, notes, or outlines.
- Converting rough content into a professional presentation.
- Generating a PDF version of an HTML deck with exact page dimensions.
- Building decks that include app screenshots or product visuals.

## Progress checklist

```
Deck Build Progress:
- [ ] Phase 1: Slide skeleton (HTML + CSS foundation)
- [ ] Phase 2: Content population (slides from source material)
- [ ] Phase 3: Visual polish (spacing, typography, layout fixes)
- [ ] Phase 4: Print-safe CSS
- [ ] Phase 5: PDF converter script
- [ ] Phase 6: Verification (screenshot comparison)
```

## Phase 1 — Slide skeleton

### Use the Domo theme

Read [domo-theme.md](domo-theme.md) for the complete Domo-branded CSS, inline SVG logo, and HTML patterns. It contains:

- **Full CSS** — all variables (`--domo-blue`, `--accent-green`, etc.), component classes (`.slide`, `.slide-header`, `.slide-footer`, `.cover-slide`, `.deck-table`, `.card`, `.flow-box`, etc.), and the print-safe `@media print` block.
- **Inline Domo logo** — an SVG data URI so no external image file is needed. Use it in both the cover logo and every slide footer.
- **Cover slide pattern** — gradient background with sparkle effects, large Domo logo top-left, title + bullets left, summary cards right.
- **Content slide pattern** — header/content/footer anatomy with page numbers.
- **Content slide with background** — the `has-bg` variant with `#DDE5ED` background.
- **Flow diagram pattern** — four-phase pipeline with colored boxes and arrows.
- **Accent color table** — which color to use for each element type.

### Dimensions

Standard 16:9 widescreen. All sizing flows from two CSS variables:

```css
:root { --slide-w: 1024px; --slide-h: 576px; }
```

### Slide anatomy

Every slide has three layers. The content area must respect header and footer bounds.

```html
<div class="slide">
  <div class="slide-header">
    <h1>Slide Title</h1>
    <div class="subtitle">UPPERCASE SUBTITLE</div>
  </div>
  <div class="slide-content" style="position:absolute; top:100px; left:0; right:0; bottom:52px; padding:24px 48px;">
    <!-- content -->
  </div>
  <div class="slide-footer">
    <span class="confidential">Confidential</span>
    <span class="footer-line"></span>
    <span class="domo-badge"><span class="page-num">1</span><img src="DATA_URI_LOGO" alt="Domo"></span>
  </div>
</div>
```

**Content area positioning**: Use `position:absolute` with `top` (below header) and `bottom:52px` (above footer). This prevents content–footer overlap.

**Domo logo**: Replace `DATA_URI_LOGO` with the inline SVG data URI from [domo-theme.md](domo-theme.md).

## Phase 2 — Content population

### Slide type patterns

**Table slide** — Use a styled `<table>` with labeled column headers. Keep cell padding tight (`6px 10px`) on dense slides.

**Flow/pipeline slide** — Horizontal flex row of boxes with arrow separators (`&#9654;`). Use colored left borders or top borders to differentiate phases.

**Card grid** — Flex row of equal-width cards. Use `flex:1` on each card, consistent padding, and subtle background colors (`#F6F8FA`).

**Architecture diagram** — Nested flex containers. Label each layer (e.g. "INTELLIGENCE LAYER", "STORAGE", "COMPUTE") with colored card groups.

**Screenshot showcase** — One hero image centered, or two side-by-side with `max-width:48%`. Apply `border-radius:8px` for polish. No `box-shadow` (removed by print CSS anyway).

**Info boxes** — Paired boxes below main content. Use `display:flex; gap:32px` with `flex:1` on each.

### Typography scale

| Element | Size | Weight |
|---------|------|--------|
| Slide title (h1) | 28px | 800 |
| Subtitle | 11px | 700 |
| Section label | 10px | 700, uppercase, letter-spacing 2px |
| Body text | 13–14px | 400 |
| Table text | 11–13px | 400 |
| Fine print / captions | 9–10px | 400 |

### Color conventions

Use CSS variables for consistency. Define brand colors, accent colors, and text shades in `:root`.

## Phase 3 — Visual polish

### Spacing rules

1. **Content must never touch the footer.** The `bottom:52px` on `.slide-content` creates a 52px exclusion zone. If content still overlaps, reduce `margin-top`, `padding`, `gap`, `font-size`, or `line-height` on the offending elements.

2. **Header–content gap.** The `top` value on `.slide-content` controls clearance below the header. Typical: `88–100px`. Increase if subtitle text collides with content.

3. **Dense slides.** When a slide has both a table and info boxes, use compact values:
   - Table cell padding: `4px 10px`
   - Info box padding: `5px 12px`
   - Gaps between cards: `3–5px`
   - Font size: step down 1px from defaults

4. **`justify-content:center` caution.** Vertical centering can push tall content past `bottom`. Remove it on content-heavy slides and let content flow from top.

### Image handling

- URL-encode spaces in `src` paths: `Sample%20Assets/file.png`.
- Avoid special Unicode characters in filenames. Copy to clean filenames if needed.
- Use `max-width:100%; max-height:100%` with `object-fit:contain` to auto-size within the content area.

## Phase 4 — Print-safe CSS

PDF rendering through Chromium's print pipeline treats `box-shadow` differently than screen rendering. Shadows appear as heavy dark blocks in PDF output.

**Required rule** (already in the skeleton above):

```css
@media print {
  *, *::before, *::after {
    box-shadow: none !important;
  }
}
```

This strips all shadows for print only. The HTML browser view retains its shadows.

Additional print considerations:
- `page-break-after: always` on `.slide` — one slide per page.
- `page-break-inside: avoid` — prevent mid-slide splits.
- `background: white` on body — no gray viewer background.

## Phase 5 — PDF converter

Use `puppeteer-core` with the system Chrome installation. Do not bundle Chromium — it avoids download issues and cache path mismatches.

```javascript
const puppeteer = require("puppeteer-core");
const path = require("path");
const fs = require("fs");

const SLIDE_W = 1024;
const SLIDE_H = 576;

function findChrome() {
  const candidates = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ];
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  return null;
}

async function convertToPdf(inputHtml, outputPdf) {
  const htmlPath = path.resolve(inputHtml);
  const outputPath = outputPdf || htmlPath.replace(/\.html?$/i, ".pdf");
  const chromePath = findChrome();

  const browser = await puppeteer.launch({
    headless: true,
    executablePath: chromePath,
    args: ["--no-sandbox"],
  });

  const page = await browser.newPage();
  await page.setViewport({ width: SLIDE_W, height: SLIDE_H, deviceScaleFactor: 2 });
  await page.goto(`file://${htmlPath}`, { waitUntil: "networkidle0", timeout: 30000 });
  await page.evaluate(() => document.fonts.ready);
  await new Promise((r) => setTimeout(r, 500));

  await page.pdf({
    path: outputPath,
    width: `${SLIDE_W}px`,
    height: `${SLIDE_H}px`,
    margin: { top: 0, right: 0, bottom: 0, left: 0 },
    printBackground: true,
    preferCSSPageSize: false,
    displayHeaderFooter: false,
  });

  await browser.close();
}
```

**Key settings:**
- `deviceScaleFactor: 2` — retina-crisp text.
- `printBackground: true` — preserves colored backgrounds.
- `margin: { top: 0, ... }` — no extra whitespace around slides.
- `width/height` must match `--slide-w`/`--slide-h` exactly.
- Wait for `document.fonts.ready` before capturing — Google Fonts must finish loading.

### package.json setup

```json
{
  "scripts": { "pdf": "node convert-to-pdf.js" },
  "dependencies": { "puppeteer-core": "latest" }
}
```

Use `puppeteer-core` (not `puppeteer`) to avoid downloading bundled Chromium.

## Phase 6 — Verification

Screenshot each HTML slide and each PDF page, then compare visually.

### Quick verification script

```javascript
// Screenshot slide N from the HTML
const box = await page.evaluate((idx) => {
  const el = document.querySelectorAll(".slide")[idx];
  const r = el.getBoundingClientRect();
  return { x: r.x, y: r.y, width: r.width, height: r.height };
}, slideIndex);

await page.screenshot({ path: `html_slide_${n}.png`, clip: box });
```

### What to check

- [ ] Page count matches slide count.
- [ ] No content clipped by footer on any slide.
- [ ] Fonts loaded (not fallback serif/sans-serif).
- [ ] All images render (no broken-image icons or alt text).
- [ ] No dark hue/shadow blocks around cards or images.
- [ ] Background colors and gradients preserved.
- [ ] Page edges are razor-sharp (no extra margin or whitespace).

## Common pitfalls

| Symptom | Cause | Fix |
|---------|-------|-----|
| Content overlaps footer | `bottom` not set or `justify-content:center` on tall content | Set `bottom:52px` on `.slide-content`; remove vertical centering on dense slides |
| Dark blocks around elements in PDF | `box-shadow` renders differently in print | Add `@media print { * { box-shadow: none !important; } }` |
| Images don't load | Spaces or Unicode in file paths | URL-encode spaces (`%20`); copy files to clean filenames |
| Fonts fallback to serif | `networkidle0` not waited or fonts blocked | Wait for `document.fonts.ready`; ensure Google Fonts URL is correct |
| Chrome not found | Puppeteer can't locate browser | Use `puppeteer-core` + `executablePath` to system Chrome |
| Extra whitespace around pages | PDF margin not zeroed | Set `margin: { top: 0, right: 0, bottom: 0, left: 0 }` |
| Blurry text in PDF | Low device scale factor | Set `deviceScaleFactor: 2` in viewport |

## Checklist

- [ ] Slide dimensions match `--slide-w` and `--slide-h` CSS variables
- [ ] Every `.slide-content` has `bottom:52px` to clear the footer
- [ ] `@media print` block strips all `box-shadow` values
- [ ] `page-break-after: always` set on `.slide` for print
- [ ] Converter uses `puppeteer-core` with system Chrome path
- [ ] `printBackground: true` and zero margins in PDF options
- [ ] `deviceScaleFactor: 2` for retina quality
- [ ] Font loading awaited before PDF capture
- [ ] Image paths URL-encoded (no raw spaces)
- [ ] Visual verification done on cover, dense slides, and screenshot slides
