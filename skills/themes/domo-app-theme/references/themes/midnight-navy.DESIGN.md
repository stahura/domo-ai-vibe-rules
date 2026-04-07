# Midnight Navy — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Steel blue & sky blue · **Mood**: Commanding, precise, institutional trust

---

## 1. Visual Theme and Atmosphere

**Personality**: A **defense- and finance-grade** light shell—ice-blue canvas (`#F0F4F8`), white intelligence cards, and a **deep navy** sidebar that signals authority without resorting to novelty gradients. Steel blue (`#3B6FA0`) is the operational accent; sky blue (`#8FBCDB`) provides secondary emphasis and wayfinding suited to regulated environments.

**Density**: Medium-high. Cool neutrals tolerate tight grids; keep **16px** gutters and **20px** card padding so dense operational views stay scannable. Prefer **shadow** over visible card frames except where tables require structure.

**Philosophy**: **Condensed headings, Sans body.** `f1` and `f2` use **Condensed** so long entity names and fiscal periods fit executive headers; everything else stays **Sans** for chart axes, filters, and tables. Hue belongs in **data** and **accent chrome**—not in arbitrary borders.

**Atmosphere cues**:
- Canvas reads as **polar ice**, not saturated hospital blue—chroma stays low on `#F0F4F8`
- Hover on white returns to **`#E4EAF0`**, aligned with institutional calm
- **Deep navy nav** (`#0A1628`) pairs with **white** (`c2`) typography—never **`c58`** on **`c4`**
- Shadows pick up **`#1A2030`** (navy text) at low alpha so depth stays **blue-cool**, not warm charcoal
- Sky blue (`c31`) is for **secondary emphasis**—sparklines, subtle fills, and nav indicators—not full-width marketing hero backgrounds
- When showing **maps or geo cards**, keep baselines neutral (`c46`/`c47`) so steel blue (`c29`) remains the “selected” semantic

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#F0F4F8` | `oklch(0.965 0.007 247.9)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c2` | `--surface` |
| Surface hover | `#E4EAF0` | `oklch(0.934 0.010 247.9)` | `c3` | `--surface-hover` |
| Navigation background | `#0A1628` | `oklch(0.200 0.040 258.3)` | `c4` | `--nav-bg` |
| Navigation active | `#142840` | `oklch(0.273 0.052 254.0)` | `c5` | `--nav-active` |
| Navigation hover | `#0E1E34` | `oklch(0.234 0.048 256.7)` | `c32` | `--nav-hover` |
| Header background | `#E8EEF4` | `oklch(0.946 0.010 247.9)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c7` | `--input-bg` |
| Tab default surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab active fill | `#3B6FA0` | `oklch(0.528 0.096 248.8)` | `c9` | `--tab-active-bg` |
| Table header background | `#DCE8F0` | `oklch(0.924 0.017 236.7)` | `c10` | `--table-header-bg` |
| Table row stripe | `#F5F8FB` | `oklch(0.978 0.005 247.9)` | `c11` | `--table-stripe` |
| Table row hover | `#EDF2F8` | `oklch(0.959 0.010 252.8)` | `c12` | `--table-row-hover` |
| Accent | `#3B6FA0` | `oklch(0.528 0.096 248.8)` | `c29` | `--accent` |
| Accent pressed | `#2D5A88` | `oklch(0.458 0.090 250.9)` | `c30` | `--accent-pressed` |
| Secondary (sky blue) | `#8FBCDB` | `oklch(0.774 0.065 238.8)` | `c31` | `--accent-secondary` |
| Border | `#B4C4D4` | `oklch(0.813 0.029 248.2)` | `c46` | `--border` |
| Border light | `#D0DCE8` | `oklch(0.889 0.021 248.1)` | `c47` | `--border-light` |
| Input border | `#B4C4D4` | `oklch(0.813 0.029 248.2)` | `c46` | `--input-border` |
| Grayscale 1 (near black) | `#0A0E14` | `oklch(0.162 0.014 258.4)` | `c40` | `--gray-950` |
| Grayscale 2 | `#191D24` | `oklch(0.230 0.015 261.6)` | `c41` | `--gray-900` |
| Grayscale 3 | `#292E34` | `oklch(0.299 0.013 253.0)` | `c42` | `--gray-850` |
| Grayscale 4 | `#3A3F45` | `oklch(0.365 0.012 253.0)` | `c43` | `--gray-800` |
| Grayscale 5 | `#4D5157` | `oklch(0.433 0.011 258.4)` | `c44` | `--gray-750` |
| Grayscale 6 | `#5F646A` | `oklch(0.501 0.011 252.9)` | `c45` | `--gray-700` |
| Grayscale 7 | `#73787E` | `oklch(0.570 0.011 252.9)` | `c48` | `--gray-600` |
| Grayscale 8 | `#878C91` | `oklch(0.638 0.010 248.0)` | `c49` | `--gray-500` |
| Grayscale 9 | `#9CA1A6` | `oklch(0.706 0.009 248.0)` | `c50` | `--gray-400` |
| Grayscale 10 | `#B1B6BB` | `oklch(0.774 0.009 247.9)` | `c51` | `--gray-300` |
| Grayscale 11 | `#C7CBD0` | `oklch(0.840 0.008 253.9)` | `c52` | `--gray-200` |
| Grayscale 12 | `#DDE2E6` | `oklch(0.910 0.008 241.7)` | `c53` | `--gray-150` |
| Grayscale 13 (near white) | `#F4F8FC` | `oklch(0.977 0.007 247.9)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#F0F4F8` | `oklch(0.965 0.007 247.9)` | `c56` | `--bg` |
| Primary text (FONT) | `#1A2030` | `oklch(0.246 0.032 268.2)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#5A6A7A` | `oklch(0.517 0.032 248.4)` | `c59` | `--text-secondary` |
| Automatic (App Studio) | — | — | `c60` | `AUTOMATIC_COLOR` |

**Slot notes**: `c56` mirrors the App Studio page background. On **dark navy** chrome, bind nav typography to **`c2`**, not `c58` or `c60`. **`c60`** is reserved—**never** set manually in theme JSON or agent-authored tokens.

### 2.2 Status Colors

| Status | Primary | Background | Text | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------|-----------------|--------------|
| On track | `#4A8AB4` | `#E8F2FA` | `#1E4A78` | `oklch(0.608 0.092 239.4)` | `--status-on-track` |
| At risk | `#6AA0C8` | `#EAF4FB` | `#2D5A88` | `oklch(0.684 0.082 241.5)` | `--status-at-risk` |
| Behind / alert | `#2D5A88` | `#E4EDF6` | `#0A1628` | `oklch(0.458 0.090 250.9)` | `--status-alert` |
| Complete / info | `#8FBCDB` | `#EAF4FB` | `#1E4A78` | `oklch(0.774 0.065 238.8)` | `--status-complete` |

### 2.3 Shadows

Blue-cool tint from **`c58`** (`#1A2030`) at restrained opacity—crisp depth for white cards on ice canvas.

```css
--shadow:
  0px 0px 0px 1px oklch(0.246 0.032 268.2 / 0.055),
  0px 1px 3px -1px oklch(0.246 0.032 268.2 / 0.045),
  0px 4px 14px 0px oklch(0.246 0.032 268.2 / 0.038);
--shadow-hover:
  0px 0px 0px 1px oklch(0.246 0.032 268.2 / 0.085),
  0px 3px 8px -1px oklch(0.246 0.032 268.2 / 0.065),
  0px 8px 22px 0px oklch(0.246 0.032 268.2 / 0.048);
```

---

## 3. Typography

### 3.1 Font System

```css
/* f1–f2 condensed titles (App Studio "Condensed") */
font-family: "SF Pro Display", "Helvetica Neue Condensed", "Arial Narrow", "Franklin Gothic Medium", Arial, sans-serif;
/* f3–f8 operational UI */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio JSON maps **`f1` / `f2` → Condensed**; **`f3`–`f8` → Sans**. Pro-code apps should mirror the mapping so dense headers align with native cards.

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | Condensed; `text-wrap: balance`; tighter tracking than Sans |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Condensed; keep line length under ~56ch where possible |
| Body / descriptions | 13px | Regular | 400 | `f3` | Sans; line-height **1.5**; `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | Sans; uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | Sans; SVG `fill`; align numerics to tabular where supported |
| Badges / status | 11px | SemiBold | 600 | `f6` | Sans; uppercase; use Section 2.2 tints |
| KPI numbers | 28px | SemiBold | 600 | `f7` | Sans; `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | Sans; uppercase; color `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Condensed titles, KPI values, badges, primary action labels
- **Regular (400)**: Body, labels, chart axes, table cells, default links (Sans)
- **Light (300)**: KPI labels and timeframe captions—must recede behind the metric
- Avoid **Bold (700+)** in dashboard chrome; Condensed already gains presence from width
- **Numerals**: Always **tabular** on KPIs and financial tables; never mix proportional figures in comparison columns
- **Tracking**: Do not artificially tighten Sans body; Condensed slots carry density

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | 20px | Title `f2` Condensed; chart `f5`; accent `c29` |
| `ca2` | Filters / controls | `c2` | `c58` | 8px | Standard | 16px | Filter chips hover on `c3` |
| `ca3` | Narrative / policy | `c2` | `c58` | 10px | Soft | 16px | Methodology, footnotes, audit text |
| `ca4` | Compact | `c2` | `c58` | 6px | None | 12px | Dense selectors, mobile |
| `ca5` | KPI hero | `c2` | `c58` | 12px | Standard | 16px | Optional **4px left** in `c29` or `c31` |
| `ca6` | Muted metric | `c3` | `c58` | 8px | None | 12px | Secondary read on ice canvas |
| `ca7` | Highlight strip | `c31` @ **12%** on `c2` | `c58` | 10px | Standard | 16px | Sky wash—not solid fill |
| `ca8` | Full-bleed strip | `c56` | `c58` | 0 | None | 12px | Page-level compliance banners |
| `ca9` | Comparison / pair | `c2` | `c58` | 10px | Standard | 16px | A|B with `c47` divider |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#0A1628` deep navy | `c4` |
| Active background | `#142840` | `c5` |
| Hover background | `#0E1E34` | `c32` |
| Title font color | `#FFFFFF` | `c2` |
| Link font color | `#FFFFFF` | `c2` |
| Active link font color | `#FFFFFF` | `c2` |
| Active indicator | `#8FBCDB` sky blue | `c31` |
| Title font | 22px SemiBold **Condensed** | `f1` |
| Link font | 13px Regular **Sans** | `f3` |
| Divider | `1px solid` `#0E1E34` | `c32` at ~**0.55** opacity over `c4` |
| Drop shadow | false | — |

**Critical**: Do not place **`c58`** on **`c4`**. **`c60`** is not a substitute for explicit light text on dark chrome.

**Implementation notes for agents**:

- **Logos** on navy should use **monochrome white** assets; drop color logos onto `c2` circular plate if brand requires hue.
- **Collapsed rail** icons: `c2` glyphs; pressed state may use `c5` background with same icon color.
- **Keyboard focus**: 2px outline using `c31` on `c4` for WCAG-visible focus that still feels on-brand.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#3B6FA0` | `oklch(0.528 0.096 248.8)` | Steel blue / primary brand |
| 2 | `#8FBCDB` | `oklch(0.774 0.065 238.8)` | Sky blue / secondary |
| 3 | `#2D5A88` | `oklch(0.458 0.090 250.9)` | Accent pressed / deep steel |
| 4 | `#6AA0C8` | `oklch(0.684 0.082 241.5)` | Mid steel |
| 5 | `#4A8AB4` | `oklch(0.608 0.092 239.4)` | Operational blue |
| 6 | `#1E4A78` | `oklch(0.403 0.092 252.0)` | Navy anchor |

**Chart chrome**: Grid `c47` @ **0.45** opacity; axis lines `c46`; ticks and legend **`f5`** in `c59`; tooltips **`c2`**, `var(--shadow)`, `c58` / `c59` text.

**Waterfall / variance**: Positive bars may map to **`#4A8AB4`**; negative to **`#2D5A88`**; totals in **`c58`**. Forecast dashed series uses **`c31`** at **70%** opacity.

---

## 7. Agent Prompt Guide

### Do's

- Align **`c1`** and **`c56`** to **`#F0F4F8`**; keep cards on **`c2`**
- Use **Condensed** only for **`f1`–`f2`**; operational UI stays **Sans**
- Use **`c29` / `c30`** for primary interactive emphasis; **`c31`** for secondary sparkline/nav indicator color
- On **dark nav**, bind typography to **`c2`**, never **`c58`**
- Tint shadows from **`c58`** at low alpha stacks
- Apply **`font-variant-numeric: tabular-nums`** to all financial KPIs and table numbers

### Don'ts

- Do not set **`c60`** manually in JSON or hand-authored CSS variables
- Do not place **warm terracotta or rose** borders from unrelated themes—use **`c46` / `c47`**
- Do not fill entire cards with **`c29`** behind **`c58`** body copy without checking contrast (prefer white surfaces)
- Do not switch **`f1`–`f2`** to Sans “for readability”**—** use shorter labels instead

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #F0F4F8     Card surface → c2   #FFFFFF
Hover        → c3        #E4EAF0     Nav bg       → c4   #0A1628
Nav active   → c5        #142840     Nav hover    → c32  #0E1E34
Header       → c6        #E8EEF4     Input fill   → c7   #FFFFFF
Accent       → c29       #3B6FA0     Accent ↓     → c30  #2D5A88
Secondary    → c31       #8FBCDB     Border       → c46  #B4C4D4
Border light → c47       #D0DCE8     Primary text → c58  #1A2030 (FONT)
Secondary    → c59       #5A6A7A (FONT)   Nav text (dark chrome) → c2
Grayscale ramp → c40–c45, c48–c54 (13 steps); c46–c47 reserved for borders
Never manual → c60       AUTOMATIC_COLOR
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#3B6FA0',
  primaryPressed: '#2D5A88',
  secondary: '#8FBCDB',
  surface: '#FFFFFF',
  bg: '#F0F4F8',
  text: '#1A2030',
  textMuted: '#5A6A7A',
  border: '#B4C4D4',
  borderLight: '#D0DCE8',
  navBg: '#0A1628',
  navActive: '#142840',
  navHover: '#0E1E34',
  onLightChrome: '#1A2030',
  onDarkChrome: '#FFFFFF',
  series: ['#3B6FA0', '#8FBCDB', '#2D5A88', '#6AA0C8', '#4A8AB4', '#1E4A78']
};
```

### Example Agent Prompts

- **“Ice canvas + white intel cards”**: Page `c56`, cards `c2`, `var(--shadow)`; borders only on inputs/tables.
- **“Condensed executive header”**: Page title `f1` Condensed 22 SemiBold; section titles `f2` 16 SemiBold.
- **“Navy command sidebar”**: Nav `c4`, type `c2`, active `c5`, sky indicator `c31`.
- **“Steel primary button”**: Fill `c29`, hover `c30`, label `c2`; focus ring `c31`.
- **“Risk register table”**: Header `c10`, striping `c11`, hover `c12`, gridlines `c47`.
- **“YoY line chart (6 series)”**: Stroke widths 2px / 2px / 2.5px for primary; use `COLORS.series` order; grid `c47` @ 0.45 alpha.
- **“Compliance footer strip”**: Full-width `ca8` on `c56`, text `f4` in `c59`, with a single `c29` inline link.

### Pro-code and App Studio sync

- Import JSON, then verify **navigation** and **tabs** previews: dark chrome must remain **`c2`** type.
- Pro-code cards embedded in App Studio should use **transparent** outer backgrounds when the platform card supplies **`c2`**.
- Mirror semantic CSS names (`--accent`, `--border`, `--text-primary`) so token swaps stay mechanical when cloning to a dark theme document later.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Midnight Navy",
  "colors": [
    { "index": 1, "value": "#F0F4F8", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#E4EAF0", "tag": "PRIMARY" },
    { "index": 4, "value": "#0A1628", "tag": "PRIMARY" },
    { "index": 5, "value": "#142840", "tag": "PRIMARY" },
    { "index": 6, "value": "#E8EEF4", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#3B6FA0", "tag": "SECONDARY" },
    { "index": 10, "value": "#DCE8F0", "tag": "PRIMARY" },
    { "index": 11, "value": "#F5F8FB", "tag": "PRIMARY" },
    { "index": 12, "value": "#EDF2F8", "tag": "PRIMARY" },
    { "index": 29, "value": "#3B6FA0", "tag": "SECONDARY" },
    { "index": 30, "value": "#2D5A88", "tag": "SECONDARY" },
    { "index": 31, "value": "#8FBCDB", "tag": "SECONDARY" },
    { "index": 32, "value": "#0E1E34", "tag": "SECONDARY" },
    { "index": 40, "value": "#0A0E14", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#191D24", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#292E34", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#3A3F45", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#4D5157", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#5F646A", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#B4C4D4", "tag": "CUSTOM" },
    { "index": 47, "value": "#D0DCE8", "tag": "CUSTOM" },
    { "index": 48, "value": "#73787E", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#878C91", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#9CA1A6", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B1B6BB", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C7CBD0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#DDE2E6", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F4F8FC", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#F0F4F8", "tag": "PRIMARY" },
    { "index": 58, "value": "#1A2030", "tag": "FONT" },
    { "index": 59, "value": "#5A6A7A", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Condensed", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Condensed", "weight": "SemiBold", "size": "16px", "style": "normal" },
    { "index": 3, "family": "Sans", "weight": "Regular", "size": "13px", "style": "normal" },
    { "index": 4, "family": "Sans", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 5, "family": "Sans", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 6, "family": "Sans", "weight": "SemiBold", "size": "11px", "style": "normal" },
    { "index": 7, "family": "Sans", "weight": "SemiBold", "size": "28px", "style": "normal" },
    { "index": 8, "family": "Sans", "weight": "Light", "size": "11px", "style": "normal" }
  ],
  "cards": [
    {
      "index": 1,
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "titleFont": { "type": "FONT_REFERENCE", "index": 2 },
      "chartFont": { "type": "FONT_REFERENCE", "index": 5 },
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "borderRadius": 10,
      "borderWidth": 0,
      "dropShadow": true,
      "dropShadowColor": { "type": "COLOR_REFERENCE", "index": 40 },
      "padding": 20,
      "elementSpacing": 12,
      "accentColor": { "type": "COLOR_REFERENCE", "index": 29 }
    }
  ],
  "buttons": [
    {
      "index": 1,
      "fontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "navigation": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 4 },
      "titleFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "linkFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "activeLinkFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "activeColor": { "type": "COLOR_REFERENCE", "index": 31 },
      "titleFont": { "type": "FONT_REFERENCE", "index": 1 },
      "linkFont": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "headers": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 6 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "font": { "type": "FONT_REFERENCE", "index": 2 }
    }
  ],
  "tables": [
    {
      "index": 1,
      "headerBackgroundColor": { "type": "COLOR_REFERENCE", "index": 10 },
      "headerFontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "rowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "alternateRowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 11 },
      "rowHoverBackgroundColor": { "type": "COLOR_REFERENCE", "index": 12 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 47 },
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "tabs": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 8 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "activeBackgroundColor": { "type": "COLOR_REFERENCE", "index": 9 },
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "forms": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 7 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
      "focusBorderColor": { "type": "COLOR_REFERENCE", "index": 29 },
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm **dark nav** uses **`c2`** for link/title colors. Active tabs use **`c2`** on **`c9`** (steel blue) for readable contrast. **`c60`** is not imported.
