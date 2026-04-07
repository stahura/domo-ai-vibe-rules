# Terracotta Sand — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Terracotta / dusty peach · **Mood**: Sun-baked clay, editorial warmth, Mediterranean calm

---

## 1. Visual Theme and Atmosphere

**Personality**: A light analytics skin that refuses sterile gray. The page is **warm sand** (`#F5EDE3`); cards are clean **white**; navigation is **deep clay** so the app has a grounded footer-like authority at the rail. Terracotta (`#C45A3C`) signals action and primary data without screaming “error red.”

**Density**: Medium. White cards on sand already create separation—use **standard** shadows (Section 2.3) instead of heavy borders. Reserve border strokes for tables and inputs.

**Philosophy**: **Serif typography everywhere** (`f1`–`f8` all Georgia / Times family) gives dashboards a magazine-meets-operations feel. Pair with generous line-height on body copy so serif text stays readable at 13px. Color discipline: earth tones in chrome; greens and teals in charts for categorical separation.

**Atmosphere cues**:
- Background grain should feel like **limestone dust**, not yellowed paper—keep sand desaturated
- Hover on white cards returns to **sand hover** (`#EDE5DB`), not cool gray
- Dark nav (`#5C2E1A`) uses **white link text** (`#FFFFFF` via `c2`) for WCAG contrast; page body text stays **dark warm brown** (`c58`)
- Chart series lean **terracotta → peach → sage → teal** so nature and craft stay on-brand

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#F5EDE3` | `oklch(0.779 0.013 358.2)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c2` | `--surface` |
| Hover surface | `#EDE5DB` | `oklch(0.759 0.013 358.2)` | `c3` | `--surface-hover` |
| Navigation background | `#5C2E1A` | `oklch(0.297 0.053 353.8)` | `c4` | `--nav-bg` |
| Navigation active | `#7A4028` | `oklch(0.364 0.063 353.7)` | `c5` | `--nav-active` |
| Header background | `#F0E8DE` | `oklch(0.766 0.013 358.2)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c7` | `--input-bg` |
| Tab surface | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab active fill | `#C45A3C` | `oklch(0.494 0.095 352.5)` | `c9` | `--tab-active-bg` |
| Table header background | `#EDE5DB` | `oklch(0.759 0.013 358.2)` | `c10` | `--table-header-bg` |
| Table row stripe | `#F8F4EF` | `oklch(0.792 0.008 358.1)` | `c11` | `--table-stripe` |
| Table row hover | `#EDE5DB` | `oklch(0.759 0.013 358.2)` | `c12` | `--table-row-hover` |
| Accent primary | `#C45A3C` | `oklch(0.494 0.095 352.5)` | `c29` | `--accent` |
| Accent pressed | `#A84830` | `oklch(0.436 0.086 352.2)` | `c30` | `--accent-pressed` |
| Secondary (dusty peach) | `#D4956A` | `oklch(0.597 0.076 355.7)` | `c31` | `--accent-secondary` |
| Navigation hover | `#6A3620` | `oklch(0.328 0.058 353.7)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#1A1410` | `oklch(0.162 0.010 355.8)` | `c40` | `--gray-950` |
| Grayscale 2 | `#241E18` | `oklch(0.197 0.012 357.4)` | `c41` | `--gray-900` |
| Grayscale 3 | `#2E2820` | `oklch(0.231 0.014 358.4)` | `c42` | `--gray-850` |
| Grayscale 4 | `#3A3228` | `oklch(0.265 0.017 358.2)` | `c43` | `--gray-800` |
| Grayscale 5 | `#4A4036` | `oklch(0.311 0.018 357.4)` | `c44` | `--gray-750` |
| Grayscale 6 | `#5C5044` | `oklch(0.361 0.021 357.4)` | `c45` | `--gray-700` |
| Border | `#C4B8AA` | `oklch(0.647 0.020 358.0)` | `c46` | `--border` |
| Border light | `#DDD4C8` | `oklch(0.717 0.016 358.5)` | `c47` | `--border-light` |
| Grayscale 7 | `#9A8B7E` | `oklch(0.531 0.022 356.9)` | `c48` | `--gray-600` |
| Grayscale 8 | `#B0A396` | `oklch(0.593 0.020 357.4)` | `c49` | `--gray-500` |
| Grayscale 9 | `#C9BDB2` | `oklch(0.661 0.017 357.1)` | `c50` | `--gray-400` |
| Grayscale 10 | `#D9CFC4` | `oklch(0.705 0.016 357.8)` | `c51` | `--gray-300` |
| Grayscale 11 | `#E5DCD2` | `oklch(0.737 0.014 357.8)` | `c52` | `--gray-200` |
| Grayscale 12 | `#EEE6DD` | `oklch(0.761 0.013 357.9)` | `c53` | `--gray-150` |
| Grayscale 13 | `#F8F2EC` | `oklch(0.790 0.009 357.5)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#F5EDE3` | `oklch(0.779 0.013 358.2)` | `c56` | `--bg` |
| Primary text (FONT) | `#3A2E24` | `oklch(0.256 0.020 356.6)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#7A6E62` | `oklch(0.448 0.020 357.4)` | `c59` | `--text-secondary` |
| Automatic (never set manually) | — | — | `c60` | — |

### 2.2 Status Colors

| Status | Primary | Background | Text on light UI | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------------------|-----------------|--------------|
| On track | `#8B9A6B` | `#EEF2E6` | `#4A5A38` | `oklch(0.598 0.045 118.0)` | `--status-on-track` |
| At risk | `#D4956A` | `#FBEFE5` | `#8B4D28` | `oklch(0.597 0.076 355.7)` | `--status-at-risk` |
| Behind / alert | `#C45A3C` | `#FCEAE5` | `#7A3018` | `oklch(0.494 0.095 352.5)` | `--status-alert` |
| Complete / info | `#6B8A8A` | `#E8F0F0` | `#2F4A4A` | `oklch(0.548 0.030 182.0)` | `--status-complete` |

### 2.3 Shadows

Warm-tinted from primary text (`#3A2E24`) at gentle opacity—standard depth (not “lifted charcoal”).

```css
--shadow:
  0px 0px 0px 1px oklch(0.256 0.020 356.6 / 0.07),
  0px 1px 3px -1px oklch(0.256 0.020 356.6 / 0.06),
  0px 4px 14px 0px oklch(0.256 0.020 356.6 / 0.05);
--shadow-hover:
  0px 0px 0px 1px oklch(0.256 0.020 356.6 / 0.10),
  0px 3px 8px -1px oklch(0.256 0.020 356.6 / 0.08),
  0px 8px 22px 0px oklch(0.256 0.020 356.6 / 0.06);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: Georgia, "Times New Roman", "Palatino Linotype", serif;
```

App Studio: **Serif** family on **every** font slot (`f1`–`f8`). Pro-code must not substitute Sans for chart axes if native cards remain Serif—mixed families across canvas read as a bug, not “contrast.”

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance`; +0.01em letter-spacing optional |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Slightly tighter leading than body |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height **1.55** for serif legibility |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.06em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill`; keep numerals tabular where possible |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; color `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges—Serif SemiBold reads elegant, not sporty
- **Regular (400)**: All body, labels, and chart axes
- **Light (300)**: KPI labels only
- Avoid dropping below 11px for Serif UI text except where Domo enforces micro copy

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | 20px | Accent `c29`; charts use `f5` |
| `ca2` | Controls | `c2` | `c58` | 8px | Standard | 16px | Resting hover uses page `c3` behind chips |
| `ca3` | Narrative / image | `c2` or transparent | `c58` | 10px | Soft | 16px | Editorial blocks, OKRs |
| `ca4` | Compact | `c2` | `c58` | 6px | None | 12px | Dense pickers |
| `ca5` | KPI | `c2` | `c58` | 12px | Standard | 16px | Optional `c31` left rule |
| `ca6` | Secondary metric | `c3` | `c58` | 8px | None | 12px | Muted tile on sand |
| `ca7` | Callout | `c31` @ 18% opacity wash | `c58` | 10px | Standard | 16px | Peach tint, not solid flood |
| `ca8` | Banner | `c56` | `c58` | 0 | None | 12px | Full-bleed sand strip |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#5C2E1A` clay | `c4` |
| Active background | `#7A4028` | `c5` |
| Hover background | `#6A3620` mid clay | `c32` |
| Title font color | `#FFFFFF` | `c2` (shared white swatch) |
| Link font color | `#FFFFFF` | `c2` |
| Active link font color | `#FFFFFF` | `c2` |
| Active indicator | `#D4956A` dusty peach | `c31` |
| Title font | 22px SemiBold **Serif** | `f1` |
| Link font | 13px Regular **Serif** | `f3` |
| Divider | `1px solid` `#6A3620` | implement as pro-code if needed |
| Shadow | false (nav is flat clay) | — |

**Nav hover hex** `#6A3620`: App Studio may not expose hover color per slot; store in agent notes and custom CSS. Do not use **`c60`** for nav fonts—white is explicit **`c2`** here.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#C45A3C` | `oklch(0.494 0.095 352.5)` | Terracotta / primary |
| 2 | `#D4956A` | `oklch(0.597 0.076 355.7)` | Dusty peach |
| 3 | `#8B9A6B` | `oklch(0.598 0.045 118.0)` | Sage green |
| 4 | `#6B8A8A` | `oklch(0.548 0.030 182.0)` | Muted teal |
| 5 | `#9A7A5A` | `oklch(0.508 0.045 55.0)` | Umber / wood |
| 6 | `#A84830` | `oklch(0.436 0.086 352.2)` | Deep terracotta |

Pro-code: `['#C45A3C', '#D4956A', '#8B9A6B', '#6B8A8A', '#9A7A5A', '#A84830']`

### Chart chrome

- Grid: `c47` @ 0.55 opacity; axis: `c46` @ 0.65
- Ticks / legend: `c59` in `f5`
- Zero line / reference: `c58` at 35% opacity

---

## 7. Agent Prompt Guide

### Do's

- Keep **page** on **`c56`** sand and **cards** on **`c2`** white—this two-step base is the theme’s signature
- Run **Serif** on **all eight** font slots in JSON before writing any custom CSS
- Use **`c29` / `c30`** for primary buttons, links, and positive emphasis—not random reds
- On **dark nav**, bind link and title colors to **`c2` white**, not **`c58`** brown
- Warm shadows only—sample from **`c58`** alpha, never pure black 0.4+ on sand

### Don'ts

- Do not use **`c60`** anywhere you need predictable text color
- Do not place **`c58` text** directly on **`c29`** terracotta fills without checking contrast (prefer white on filled terracotta buttons)
- Do not swap Serif for system Sans “for performance” on a single card—it breaks the editorial system
- Avoid cool blue-gray borders borrowed from corporate themes; use **`c46` / `c47`**

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #F5EDE3     Card surface → c2   #FFFFFF
Hover        → c3        #EDE5DB     Nav bg       → c4   #5C2E1A
Nav active   → c5        #7A4028     Nav hover    → c32       #6A3620
Header tint  → c6        #F0E8DE     Input fill   → c7   #FFFFFF
Accent       → c29       #C45A3C     Accent ↓     → c30  #A84830
Secondary peach → c31    #D4956A     Nav hover    → c32  #6A3620
Border       → c46       #C4B8AA     Border light → c47  #DDD4C8
Primary text → c58       #3A2E24     Secondary    → c59  #7A6E62
Nav text     → c2        #FFFFFF (on dark chrome only)
Grayscale    → c40–c54 red-brown ramp; c46–c47 structural borders
Never        → c60 for fonts
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#C45A3C',
  primaryPressed: '#A84830',
  secondary: '#D4956A',
  surface: '#FFFFFF',
  bg: '#F5EDE3',
  text: '#3A2E24',
  textMuted: '#7A6E62',
  border: '#C4B8AA',
  borderLight: '#DDD4C8',
  navBg: '#5C2E1A',
  navActive: '#7A4028',
  navHover: '#6A3620',
  onLightChrome: '#3A2E24',
  onDarkChrome: '#FFFFFF',
  series: ['#C45A3C', '#D4956A', '#8B9A6B', '#6B8A8A', '#9A7A5A', '#A84830']
};
```

### Example Agent Prompts

- **“Sand page + white cards”**: Outer layout `c56`, card collection `c2`, `var(--shadow)` only—no 1px border unless table.
- **“Serif KPI tile”**: `f7` + `f8` both **Serif**; value `c58`, label `c59`; optional peach rule `c31`.
- **“Dark clay navigation”**: Background `c4`, text `c2`, active state `c5` with `c2` labels; never `c58` on `c4`.
- **“Terracotta CTA”**: Fill `c29`, hover `c30`, label `c2`; focus ring `c30` at 2px offset.

### Pro-Code `:root` Reference

```css
:root {
  --bg: #F5EDE3;
  --surface: #FFFFFF;
  --surface-hover: #EDE5DB;
  --nav-bg: #5C2E1A;
  --nav-active: #7A4028;
  --nav-hover: #6A3620;
  --accent: #C45A3C;
  --accent-pressed: #A84830;
  --accent-secondary: #D4956A;
  --border: #C4B8AA;
  --border-light: #DDD4C8;
  --text-primary: #3A2E24;
  --text-secondary: #7A6E62;
  --font-stack: Georgia, "Times New Roman", "Palatino Linotype", serif;
}
```

### Parity Checklist

1. Theme JSON **`fonts`** array: **Serif** on indices 1–8.
2. **`c56`** present and equals **`c1`** sand value.
3. Navigation font colors point to **`c2`**, not **`c58`**.
4. No **`c60`** font references post-import.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Terracotta Sand",
  "colors": [
    { "index": 1, "value": "#F5EDE3", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#EDE5DB", "tag": "PRIMARY" },
    { "index": 4, "value": "#5C2E1A", "tag": "PRIMARY" },
    { "index": 5, "value": "#7A4028", "tag": "PRIMARY" },
    { "index": 6, "value": "#F0E8DE", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#C45A3C", "tag": "SECONDARY" },
    { "index": 10, "value": "#EDE5DB", "tag": "PRIMARY" },
    { "index": 11, "value": "#F8F4EF", "tag": "PRIMARY" },
    { "index": 12, "value": "#EDE5DB", "tag": "PRIMARY" },
    { "index": 29, "value": "#C45A3C", "tag": "SECONDARY" },
    { "index": 30, "value": "#A84830", "tag": "SECONDARY" },
    { "index": 31, "value": "#D4956A", "tag": "SECONDARY" },
    { "index": 32, "value": "#6A3620", "tag": "SECONDARY" },
    { "index": 40, "value": "#1A1410", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#241E18", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#2E2820", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#3A3228", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#4A4036", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#5C5044", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#C4B8AA", "tag": "CUSTOM" },
    { "index": 47, "value": "#DDD4C8", "tag": "CUSTOM" },
    { "index": 48, "value": "#9A8B7E", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#B0A396", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#C9BDB2", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#D9CFC4", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#E5DCD2", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#EEE6DD", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F8F2EC", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#F5EDE3", "tag": "PRIMARY" },
    { "index": 58, "value": "#3A2E24", "tag": "FONT" },
    { "index": 59, "value": "#7A6E62", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Serif", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Serif", "weight": "SemiBold", "size": "16px", "style": "normal" },
    { "index": 3, "family": "Serif", "weight": "Regular", "size": "13px", "style": "normal" },
    { "index": 4, "family": "Serif", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 5, "family": "Serif", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 6, "family": "Serif", "weight": "SemiBold", "size": "11px", "style": "normal" },
    { "index": 7, "family": "Serif", "weight": "SemiBold", "size": "28px", "style": "normal" },
    { "index": 8, "family": "Serif", "weight": "Light", "size": "11px", "style": "normal" }
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

> **Import note**: After import, verify **dark nav** text uses **`c2`**. Tab active state uses **white (`c2`)** on **terracotta (`c9`)** for readable contrast.
