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
- [ ] Phase 5: PDF conversion (use bundled script; do not reimplement)
- [ ] Phase 6: Verification (screenshot comparison)
```

## Phase 1 — Slide skeleton

### Use the Domo theme — MANDATORY FIRST STEP

1. Read [references/domo-theme.md](references/domo-theme.md) — it contains a **complete, copy-paste-ready HTML skeleton** that produces slides matching the Domo template exactly.
2. Read [references/assets/logo-data-uri.txt](references/assets/logo-data-uri.txt) — it contains the actual Domo logo as a base64 PNG data URI. Replace every `LOGO_DATA_URI` placeholder in the skeleton with this value.
3. The logo PNG is also at [references/assets/domologo.png](references/assets/domologo.png).

**Do not skip this step.** Copy the complete skeleton from the theme file, then build slides into it. Every content slide MUST have:

- **Header**: `<div class="slide-header">` with `<h1>`, `.subtitle`, and **`.header-line`** (thin gray separator — required)
- **Content**: `<div class="slide-content has-bg">` — **always use `has-bg`** for the gray `#DDE5ED` background (this is the Domo look; content is vertically centered automatically)
- **Footer**: `<div class="slide-footer">` with `.confidential` (left), `.footer-line` (center), and `.domo-badge` with **`<img src="LOGO_DATA_URI">`** (bottom-right — required)

### Dimensions

Standard 16:9 widescreen: `--slide-w: 1024px; --slide-h: 576px;`

### Content area positioning

The `has-bg` class handles positioning automatically (`position:absolute; top:90px; bottom:52px`) with vertical centering (`display:flex; justify-content:center`). Do not override these with inline styles.

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

**Do not rewrite the converter from scratch.** This skill ships a maintained script: [references/convert-to-pdf.js](references/convert-to-pdf.js). Copy it into the user’s project or run it by path from the skill directory after install.

```bash
npm install puppeteer-core
node convert-to-pdf.js path/to/deck.html path/to/deck.pdf
# optional second arg omitted => writes next to the HTML with .pdf extension
```

The script uses `puppeteer-core` with the **system Chrome** binary (not bundled Chromium), matching the approach below.

**Key settings** (implemented in the script; change only if you have a deliberate reason):
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

Use `puppeteer-core` (not `puppeteer`): the full `puppeteer` package downloads its own Chromium on install (~hundreds of MB) and uses that browser; `puppeteer-core` is the automation library only and expects you to pass `executablePath` to an existing Chrome/Chromium (this script finds system Chrome). Smaller install, one browser to update, fewer CI/cache issues.

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
