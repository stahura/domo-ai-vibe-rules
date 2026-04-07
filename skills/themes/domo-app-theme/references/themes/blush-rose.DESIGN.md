# Blush Rose — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Dusty rose & warm gold · **Mood**: Soft luxury, spa calm, editorial beauty

---

## 1. Visual Theme and Atmosphere

**Personality**: A light shell tuned for **beauty, wellness, and luxury retail**—never sterile clinical white. The canvas is a whisper of rose (`#F8F2F0`); cards stay crisp **white**; a **wine** navigation rail grounds the product like velvet ribbon. Dusty rose (`#C4848A`) and warm gold (`#D4A85C`) carry brand warmth; sage and periwinkle in charts keep categories legible without neon noise.

**Density**: Medium. Rose-tinted negative space already separates regions—prefer **shadow** over heavy card outlines. Default **20px** card padding and **12px** element spacing keep dense KPI grids breathable.

**Philosophy**: **Serif authority on titles, Sans everywhere else.** `f1` and `f2` use **Serif** for magazine-like hierarchy; operational UI (`f3`–`f8`) stays **Sans** so tables, filters, and chart chrome stay crisp at small sizes. Structural chrome stays **earth-wine**; saturated hue belongs in **data** and **accent controls**.

**Atmosphere cues**:
- Page grain reads like **powder and silk**—keep the rose tint low-chroma
- Hover on white returns to **`#F0E8E6`**, never cool neutral gray
- **Dark wine nav** uses **white** (`c2`) for link and title typography—never **`c58`** on **`c4`**
- Shadows are **rose-brown tinted** from **`c58`**, not stacked pure black
- Gold (`c31`) is for **accents and indicators**, not full-width header floods—reserve large fields for white (`c2`) or blush tints (`c6`, `c56`)
- When mixing **photography** with cards, align image midtones toward **`c56`** so white cards still feel brightest in the stack

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#F8F2F0` | `oklch(0.965 0.007 39.5)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c2` | `--surface` |
| Surface hover | `#F0E8E6` | `oklch(0.937 0.009 34.3)` | `c3` | `--surface-hover` |
| Navigation background | `#4A2832` | `oklch(0.324 0.053 1.5)` | `c4` | `--nav-bg` |
| Navigation active | `#5E3440` | `oklch(0.381 0.062 2.1)` | `c5` | `--nav-active` |
| Navigation hover | `#543030` | `oklch(0.354 0.053 20.0)` | `c32` | `--nav-hover` |
| Header background | `#F0E6E8` | `oklch(0.933 0.011 3.5)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c7` | `--input-bg` |
| Tab default surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab active fill | `#C4848A` | `oklch(0.680 0.079 13.2)` | `c9` | `--tab-active-bg` |
| Table header background | `#EEE6E4` | `oklch(0.931 0.009 34.3)` | `c10` | `--table-header-bg` |
| Table row stripe | `#FDFBFA` | `oklch(0.989 0.003 48.7)` | `c11` | `--table-stripe` |
| Table row hover | `#F5EEEC` | `oklch(0.954 0.008 36.6)` | `c12` | `--table-row-hover` |
| Accent | `#C4848A` | `oklch(0.680 0.079 13.2)` | `c29` | `--accent` |
| Accent pressed | `#A86E74` | `oklch(0.601 0.074 12.8)` | `c30` | `--accent-pressed` |
| Secondary (warm gold) | `#D4A85C` | `oklch(0.756 0.108 79.6)` | `c31` | `--accent-secondary` |
| Border | `#D4C4C0` | `oklch(0.832 0.019 34.3)` | `c46` | `--border` |
| Border light | `#E4D8D4` | `oklch(0.891 0.014 39.4)` | `c47` | `--border-light` |
| Input border | `#D4C4C0` | `oklch(0.832 0.019 34.3)` | `c46` | `--input-border` |
| Grayscale 1 (near black) | `#1A1214` | `oklch(0.193 0.014 1.8)` | `c40` | `--gray-950` |
| Grayscale 2 | `#292123` | `oklch(0.258 0.013 1.2)` | `c41` | `--gray-900` |
| Grayscale 3 | `#393132` | `oklch(0.322 0.012 9.2)` | `c42` | `--gray-850` |
| Grayscale 4 | `#4A4142` | `oklch(0.385 0.012 10.1)` | `c43` | `--gray-800` |
| Grayscale 5 | `#5C5353` | `oklch(0.451 0.012 17.6)` | `c44` | `--gray-750` |
| Grayscale 6 | `#6E6565` | `oklch(0.515 0.011 17.5)` | `c45` | `--gray-700` |
| Grayscale 7 | `#807877` | `oklch(0.580 0.010 26.1)` | `c48` | `--gray-600` |
| Grayscale 8 | `#938B8A` | `oklch(0.643 0.010 26.1)` | `c49` | `--gray-500` |
| Grayscale 9 | `#A79F9E` | `oklch(0.709 0.009 26.1)` | `c50` | `--gray-400` |
| Grayscale 10 | `#BAB3B2` | `oklch(0.772 0.008 27.2)` | `c51` | `--gray-300` |
| Grayscale 11 | `#CFC8C6` | `oklch(0.838 0.008 36.5)` | `c52` | `--gray-200` |
| Grayscale 12 | `#E3DDDB` | `oklch(0.902 0.007 39.5)` | `c53` | `--gray-150` |
| Grayscale 13 (near white) | `#F8F2F0` | `oklch(0.965 0.007 39.5)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#F8F2F0` | `oklch(0.965 0.007 39.5)` | `c56` | `--bg` |
| Primary text (FONT) | `#3A2A28` | `oklch(0.303 0.024 26.7)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#7A6A66` | `oklch(0.538 0.021 34.3)` | `c59` | `--text-secondary` |
| Automatic (App Studio) | — | — | `c60` | `AUTOMATIC_COLOR` |

**Slot notes**: `c56` mirrors the page background used by App Studio canvas. `c58` / `c59` are **FONT** tags for copy on **light** surfaces. On **dark wine** chrome (`c4`–`c5`), bind nav typography to **`c2`**, not `c60` or `c58`. **`c60`** is reserved—**never** set manually in theme JSON or agent specs.

### 2.2 Status Colors

| Status | Primary | Background | Text | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------|-----------------|--------------|
| On track | `#8B9A7A` | `#EEF2E8` | `#4A5C3E` | `oklch(0.665 0.049 128.1)` | `--status-on-track` |
| At risk | `#D4A85C` | `#FBF4E8` | `#8A6230` | `oklch(0.756 0.108 79.6)` | `--status-at-risk` |
| Behind / alert | `#A86E74` | `#F8ECEE` | `#6E3840` | `oklch(0.601 0.074 12.8)` | `--status-alert` |
| Complete / info | `#7A8AAA` | `#E9EDF5` | `#3D4D66` | `oklch(0.632 0.052 264.1)` | `--status-complete` |

### 2.3 Shadows

Rose-brown tint from **`c58`** (`#3A2A28`) at restrained opacity—luxury depth without muddy halos.

```css
--shadow:
  0px 0px 0px 1px oklch(0.303 0.024 26.7 / 0.065),
  0px 1px 3px -1px oklch(0.303 0.024 26.7 / 0.055),
  0px 4px 14px 0px oklch(0.303 0.024 26.7 / 0.045);
--shadow-hover:
  0px 0px 0px 1px oklch(0.303 0.024 26.7 / 0.095),
  0px 3px 8px -1px oklch(0.303 0.024 26.7 / 0.075),
  0px 8px 22px 0px oklch(0.303 0.024 26.7 / 0.055);
```

---

## 3. Typography

### 3.1 Font System

```css
/* f1–f2 titles */
font-family: Georgia, "Iowan Old Style", "Palatino Linotype", "Times New Roman", serif;
/* f3–f8 body & chrome */
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio JSON maps **`f1` / `f2` → Serif**; **`f3`–`f8` → Sans**. Pro-code apps should mirror the split so native cards and embedded HTML feel unified.

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | Serif; `text-wrap: balance`; optional +0.01em tracking |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Serif; slightly tighter leading than body |
| Body / descriptions | 13px | Regular | 400 | `f3` | Sans; line-height **1.5**; `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | Sans; uppercase; `letter-spacing: 0.05em` |
| Chart axis text | 11px | Regular | 400 | `f5` | Sans; SVG `fill`; align numerics to tabular where supported |
| Badges / status | 11px | SemiBold | 600 | `f6` | Sans; uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | Sans; `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | Sans; uppercase; color `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Page and card titles (Serif), KPI values, badges, emphasized controls
- **Regular (400)**: Body, labels, chart axes, table cells, default navigation links (Sans)
- **Light (300)**: KPI labels and timeframe captions—must recede behind the number
- Avoid **Bold (700+)** in dashboard chrome; it fights the soft-luxury voice
- **Tracking**: Keep default system tracking for Sans; allow **+0.01em** on Serif titles only when the string is short (under ~40 characters)
- **Numerals**: Prefer **lining figures** from the Sans stack; never mix old-style figures in KPI tiles

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | 20px | Title `f2` Serif; chart `f5`; accent `c29` |
| `ca2` | Filters / controls | `c2` | `c58` | 8px | Standard | 16px | Chips hover on `c3` wash |
| `ca3` | Narrative / brand | `c2` | `c58` | 10px | Soft | 16px | OKRs, editorial callouts |
| `ca4` | Compact | `c2` | `c58` | 6px | None | 12px | Dense pickers, mobile |
| `ca5` | KPI hero | `c2` | `c58` | 12px | Standard | 16px | Optional **4px left** rule in `c31` gold or `c29` rose |
| `ca6` | Muted metric | `c3` | `c58` | 8px | None | 12px | Secondary tile on blush canvas |
| `ca7` | Promo / highlight | `c31` @ **14%** opacity on `c2` | `c58` | 10px | Standard | 16px | Gold veil, not solid flood |
| `ca8` | Full-bleed strip | `c56` | `c58` | 0 | None | 12px | Page-level banners |
| `ca9` | Comparison / pair | `c2` | `c58` | 10px | Standard | 16px | Side-by-side A|B with shared `c47` divider |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#4A2832` wine | `c4` |
| Active background | `#5E3440` | `c5` |
| Hover background | `#543030` | `c32` |
| Title font color | `#FFFFFF` | `c2` (on dark chrome) |
| Link font color | `#FFFFFF` | `c2` |
| Active link font color | `#FFFFFF` | `c2` |
| Active indicator | `#D4A85C` warm gold | `c31` |
| Title font | 22px SemiBold **Serif** | `f1` |
| Link font | 13px Regular **Sans** | `f3` |
| Divider | `1px solid` `#543030` | `c32` at reduced opacity if layered |
| Drop shadow | false (flat velvet rail) | — |

**Critical**: Do not place **`c58`** on **`c4`**—contrast fails. App Studio may not expose every hover slot; document **`c32`** for custom CSS where needed.

**Implementation notes for agents**:

- If the host page places a **logo** atop the nav, keep the logo container background **`transparent`** so `c4` reads continuously.
- **Collapsed nav** icon buttons should use **`c2`** icons on `c4`; pressed state may move toward **`c5`** with the same icon color.
- Long link labels should **truncate with ellipsis** before wrapping to a second line—Condensed is not used in this theme, so horizontal space is precious.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#C4848A` | `oklch(0.680 0.079 13.2)` | Dusty rose / brand lead |
| 2 | `#D4A85C` | `oklch(0.756 0.108 79.6)` | Warm gold |
| 3 | `#8B9A7A` | `oklch(0.665 0.049 128.1)` | Sage green |
| 4 | `#7A8AAA` | `oklch(0.632 0.052 264.1)` | Dusty periwinkle |
| 5 | `#A86E74` | `oklch(0.601 0.074 12.8)` | Deep rose |
| 6 | `#E8B864` | `oklch(0.809 0.116 79.9)` | Bright gold highlight |

**Chart chrome**: Grid `c47` @ **0.5** opacity; axis lines `c46`; ticks and legend **`f5`** with `c59`; tooltips **`c2`** surface, `var(--shadow)`, `c58` primary / `c59` meta.

**Waterfall / variance semantics**: Positive deltas may reuse series sage (`#8B9A7A`); negative deltas deep rose (`#A86E74`); totals read in **`c58`**. Forecast overlays use **`c29`** at ~**65%** opacity with dashed stroke; do not introduce a seventh neon hue for “projected.”

---

## 7. Agent Prompt Guide

### Do's

- Keep **`c1`** and **`c56`** aligned to **`#F8F2F0`**; cards on **`c2`** white
- Run **Serif on `f1`–`f2`** and **Sans on `f3`–`f8`** in theme JSON before writing custom CSS
- Use **`c29` / `c30`** for rose-filled controls; use **`c31`** gold for secondary emphasis and nav indicators
- On **dark nav**, bind link and title colors to **`c2`**, never **`c58`**
- Tint shadows from **`c58`** alpha stacks, not `#000000` at high opacity
- Apply **`font-variant-numeric: tabular-nums`** to dynamic KPIs and small multiples

### Don'ts

- Do not assign **`c60`** manually in JSON, CSS variables, or design tokens
- Do not import **cool corporate blue-gray** borders—use **`c46` / `c47`**
- Do not place **`c58`** text on **`c29`** fills without verifying contrast (prefer **`c2`** on solid rose buttons)
- Do not add a third display family to chart legends while cards remain Serif/Sans split

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #F8F2F0     Card surface → c2   #FFFFFF
Hover        → c3        #F0E8E6     Nav bg       → c4   #4A2832
Nav active   → c5        #5E3440     Nav hover    → c32  #543030
Header       → c6        #F0E6E8     Input fill   → c7   #FFFFFF
Accent       → c29       #C4848A     Accent ↓     → c30  #A86E74
Secondary    → c31       #D4A85C     Border       → c46  #D4C4C0
Border light → c47       #E4D8D4     Primary text → c58  #3A2A28 (FONT)
Secondary    → c59       #7A6A66 (FONT)   Nav text (dark chrome) → c2
Grayscale ramp → c40–c45, c48–c54 (13 steps); c46–c47 reserved for borders
Never manual → c60       AUTOMATIC_COLOR
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#C4848A',
  primaryPressed: '#A86E74',
  secondary: '#D4A85C',
  surface: '#FFFFFF',
  bg: '#F8F2F0',
  text: '#3A2A28',
  textMuted: '#7A6A66',
  border: '#D4C4C0',
  borderLight: '#E4D8D4',
  navBg: '#4A2832',
  navActive: '#5E3440',
  navHover: '#543030',
  onLightChrome: '#3A2A28',
  onDarkChrome: '#FFFFFF',
  series: ['#C4848A', '#D4A85C', '#8B9A7A', '#7A8AAA', '#A86E74', '#E8B864']
};
```

### Example Agent Prompts

- **“Blush canvas + white cards”**: Page `c56`, cards `c2`, `var(--shadow)` only—skip heavy borders except tables/forms.
- **“Serif page title + Sans body”**: H1 uses `f1` (Serif 22 SemiBold); paragraphs `f3` (Sans 13 Regular, line-height 1.5).
- **“Wine sidebar navigation”**: Background `c4`, text `c2`, active pill `c5` with `c2` labels, gold rail `c31`—never `c58` on `c4`.
- **“Dusty rose CTA”**: Fill `c29`, hover toward `c30`, label `c2`; focus ring `c30` with 2px offset.
- **“Gold secondary chip”**: Stroke `c46`, text `c58`, hover wash `c31` at ~12% opacity on `c2`.
- **“Spa KPI row (4 tiles)”**: Each tile `ca5` on `c2`, value `f7` tabular, label `f8` in `c59`, optional 4px left accent alternating `c29` and `c31`.
- **“Editorial hero banner”**: Full-bleed `ca8` on `c56`, headline `f1` Serif, subcopy `f3` Sans in `c59`, CTA outline using `c46` + text `c58`.
- **“Status table with badges”**: Rows `c2` / `c11` striping; badges `f6` on Section 2.2 tints; never raw `#FF0000` on white.

### Pro-code and App Studio sync

- After importing JSON, spot-check **navigation** and **tabs** in the Theme Editor preview: dark chrome must show **`c2`** type, not **`c58`**.
- In embedded pro-code cards, set `background: transparent` when the host App Studio card supplies **`c2`**, so shadows stay native.
- Keep CSS variables aligned with Section 2.1 names (`--surface`, `--accent`, etc.) so future dark-theme ports only swap the `:root` block.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Blush Rose",
  "colors": [
    { "index": 1, "value": "#F8F2F0", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#F0E8E6", "tag": "PRIMARY" },
    { "index": 4, "value": "#4A2832", "tag": "PRIMARY" },
    { "index": 5, "value": "#5E3440", "tag": "PRIMARY" },
    { "index": 6, "value": "#F0E6E8", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#C4848A", "tag": "SECONDARY" },
    { "index": 10, "value": "#EEE6E4", "tag": "PRIMARY" },
    { "index": 11, "value": "#FDFBFA", "tag": "PRIMARY" },
    { "index": 12, "value": "#F5EEEC", "tag": "PRIMARY" },
    { "index": 29, "value": "#C4848A", "tag": "SECONDARY" },
    { "index": 30, "value": "#A86E74", "tag": "SECONDARY" },
    { "index": 31, "value": "#D4A85C", "tag": "SECONDARY" },
    { "index": 32, "value": "#543030", "tag": "SECONDARY" },
    { "index": 40, "value": "#1A1214", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#292123", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#393132", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#4A4142", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#5C5353", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#6E6565", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#D4C4C0", "tag": "CUSTOM" },
    { "index": 47, "value": "#E4D8D4", "tag": "CUSTOM" },
    { "index": 48, "value": "#807877", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#938B8A", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#A79F9E", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#BAB3B2", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#CFC8C6", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E3DDDB", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F8F2F0", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#F8F2F0", "tag": "PRIMARY" },
    { "index": 58, "value": "#3A2A28", "tag": "FONT" },
    { "index": 59, "value": "#7A6A66", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Serif", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Serif", "weight": "SemiBold", "size": "16px", "style": "normal" },
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

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm **dark nav** uses **`c2`** for link/title colors. Active tabs use **`c2`** on **`c9`** (dusty rose) for readable contrast. **`c60`** is not imported—App Studio supplies automatic text color where applicable.
