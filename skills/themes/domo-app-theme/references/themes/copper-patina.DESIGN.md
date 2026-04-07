# Copper Patina — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Verdigris teal + oxidized copper · **Mood**: Museum catalog, crafted metal, calm precision

---

## 1. Visual Theme and Atmosphere

**Personality**: Two metals in dialogue: **verdigris teal** (`#4D8A7F`) carries trust and freshness, while **copper** (`#B87333`) adds warmth and urgency without defaulting to traffic red. The page reads as **cream vellum** (`#FAF7F2`); cards are **white labs**; navigation is **dark teal patina** so the app feels anchored and collectible.

**Density**: Medium-high acceptable—white cards on cream separate cleanly with **standard warm shadows** (Section 2.3). Prefer shadow over borders on analytic cards; keep **1px** rules for tables and inputs.

**Philosophy**: **Sans** throughout for a modern craft / premium commerce vibe. Neutrals are slightly warm (`#2E2A24` text) so the theme never slides into sterile blue-gray UI. Charts alternate teal family hues with copper and sand for categorical clarity.

**Atmosphere cues**:
- **Cream canvas** + **white surface** = archival paper stack
- **Dark teal nav** recalls oxidized bronze bezels—pair with **white** nav type (`c2`)
- Accent buttons and links: **verdigris** first; **copper** for secondary emphasis and “earned attention” series
- Hover on white cards: **cream hover** (`#F2EDE6`), not flat gray

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#FAF7F2` | `oklch(0.801 0.006 359.2)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c2` | `--surface` |
| Hover surface | `#F2EDE6` | `oklch(0.777 0.009 358.6)` | `c3` | `--surface-hover` |
| Navigation background | `#2C4A42` | `oklch(0.312 0.007 142.3)` | `c4` | `--nav-bg` |
| Navigation active | `#3A5E54` | `oklch(0.368 0.008 140.4)` | `c5` | `--nav-active` |
| Header background | `#F2EDE6` | `oklch(0.777 0.009 358.6)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c7` | `--input-bg` |
| Tab surface | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab active fill | `#4D8A7F` | `oklch(0.480 0.017 153.6)` | `c9` | `--tab-active-bg` |
| Table header background | `#F2EDE6` | `oklch(0.777 0.009 358.6)` | `c10` | `--table-header-bg` |
| Table row stripe | `#FAF7F2` | `oklch(0.801 0.006 359.2)` | `c11` | `--table-stripe` |
| Table row hover | `#F2EDE6` | `oklch(0.777 0.009 358.6)` | `c12` | `--table-row-hover` |
| Accent primary (verdigris) | `#4D8A7F` | `oklch(0.480 0.017 153.6)` | `c29` | `--accent` |
| Accent pressed | `#3D7A6F` | `oklch(0.436 0.016 152.8)` | `c30` | `--accent-pressed` |
| Secondary (copper) | `#B87333` | `oklch(0.513 0.095 356.5)` | `c31` | `--accent-copper` |
| Navigation hover | `#345248` | `oklch(0.336 0.006 127.6)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#141210` | `oklch(0.151 0.004 357.4)` | `c40` | `--gray-950` |
| Grayscale 2 | `#201E1C` | `oklch(0.194 0.004 357.4)` | `c41` | `--gray-900` |
| Grayscale 3 | `#2C2A26` | `oklch(0.234 0.006 359.7)` | `c42` | `--gray-850` |
| Grayscale 4 | `#3A3632` | `oklch(0.275 0.007 357.4)` | `c43` | `--gray-800` |
| Grayscale 5 | `#4A4540` | `oklch(0.323 0.009 357.4)` | `c44` | `--gray-750` |
| Grayscale 6 | `#5C5650` | `oklch(0.375 0.010 357.4)` | `c45` | `--gray-700` |
| Border | `#C4BEB4` | `oklch(0.659 0.013 359.2)` | `c46` | `--border` |
| Border light | `#DDD8D0` | `oklch(0.725 0.010 359.0)` | `c47` | `--border-light` |
| Grayscale 7 | `#8A8580` | `oklch(0.508 0.008 357.5)` | `c48` | `--gray-600` |
| Grayscale 8 | `#A39E98` | `oklch(0.575 0.009 358.1)` | `c49` | `--gray-500` |
| Grayscale 9 | `#BCB7B0` | `oklch(0.641 0.010 358.6)` | `c50` | `--gray-400` |
| Grayscale 10 | `#D0CCC5` | `oklch(0.694 0.009 359.3)` | `c51` | `--gray-300` |
| Grayscale 11 | `#E0DCD6` | `oklch(0.734 0.008 358.8)` | `c52` | `--gray-200` |
| Grayscale 12 | `#ECE9E4` | `oklch(0.766 0.006 359.2)` | `c53` | `--gray-150` |
| Grayscale 13 | `#F7F4F0` | `oklch(0.793 0.005 358.5)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#FAF7F2` | `oklch(0.801 0.006 359.2)` | `c56` | `--bg` |
| Primary text (FONT) | `#2E2A24` | `oklch(0.236 0.010 358.8)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#706A60` | `oklch(0.432 0.014 359.1)` | `c59` | `--text-secondary` |
| Automatic (never set manually) | — | — | `c60` | — |

### 2.2 Status Colors

| Status | Primary | Background | Text on light UI | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------------------|-----------------|--------------|
| On track | `#4D8A7F` | `#E8F2F0` | `#2A5C54` | `oklch(0.480 0.017 153.6)` | `--status-on-track` |
| At risk | `#D4956A` | `#FBF0E8` | `#8B4D28` | `oklch(0.597 0.076 355.7)` | `--status-at-risk` |
| Behind / alert | `#C45A3C` | `#FCEAE5` | `#7A3018` | `oklch(0.494 0.095 352.5)` | `--status-alert` |
| Complete / info | `#6AA898` | `#E8F3F0` | `#2F5E52` | `oklch(0.559 0.013 143.9)` | `--status-complete` |

### 2.3 Shadows

Standard depth, warm-tinted from `#2E2A24` (primary text). No exaggerated vertical lift—this theme is gallery-quiet.

```css
--shadow:
  0px 0px 0px 1px oklch(0.236 0.010 358.8 / 0.06),
  0px 1px 3px -1px oklch(0.236 0.010 358.8 / 0.05),
  0px 4px 14px 0px oklch(0.236 0.010 358.8 / 0.045);
--shadow-hover:
  0px 0px 0px 1px oklch(0.236 0.010 358.8 / 0.09),
  0px 3px 8px -1px oklch(0.236 0.010 358.8 / 0.07),
  0px 8px 22px 0px oklch(0.236 0.010 358.8 / 0.055);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio: **Sans** on all slots `f1`–`f8`.

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | — |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.5 |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Headings, KPI values, badges
- **Regular (400)**: Body, labels, charts, tables
- **Light (300)**: KPI labels only
- Keep weights in the 300–600 band for a calm premium feel

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | 20px | Accent `c29`; chart `f5` |
| `ca2` | Controls | `c2` | `c58` | 8px | Standard | 16px | Inputs `c7`, focus `c29` |
| `ca3` | Media | `c2` | `c58` | 10px | Soft | 12px | Copper accent allowable in chrome |
| `ca4` | Compact | `c2` | `c58` | 6px | None | 12px | Settings drawers |
| `ca5` | KPI | `c2` | `c58` | 12px | Standard | 16px | Optional `c31` copper hairline |
| `ca6` | Secondary metric | `c3` | `c58` | 8px | None | 12px | On-canvas quiet tiles |
| `ca7` | Dual-accent callout | `c3` | `c58` | 10px | Standard | 16px | Left border `c29`, icon `c31` |
| `ca8` | Banner | `c56` | `c58` | 0 | None | 12px | Cream full-bleed |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#2C4A42` dark teal | `c4` |
| Active background | `#3A5E54` | `c5` |
| Hover background | `#345248` | `c32` |
| Title font color | `#FFFFFF` | `c2` |
| Link font color | `#FFFFFF` | `c2` |
| Active link font color | `#FFFFFF` | `c2` |
| Active indicator | `#4D8A7F` verdigris | `c29` |
| Title font | 22px SemiBold Sans | `f1` |
| Link font | 13px Regular Sans | `f3` |
| Shadow | false | — |

Use **`c2` white** on **`c4` nav**—do not use **`c58`** brown-gray on dark teal. **`c60`** is forbidden for font colors.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#4D8A7F` | `oklch(0.480 0.017 153.6)` | Verdigris primary |
| 2 | `#B87333` | `oklch(0.513 0.095 356.5)` | Oxidized copper |
| 3 | `#6AA898` | `oklch(0.559 0.013 143.9)` | Lighter patina teal |
| 4 | `#D4956A` | `oklch(0.597 0.076 355.7)` | Warm sand accent |
| 5 | `#8B7355` | `oklch(0.470 0.044 358.1)` | Bronzed neutral |
| 6 | `#3D7A6F` | `oklch(0.436 0.016 152.8)` | Deep teal / pressed |

Pro-code: `['#4D8A7F', '#B87333', '#6AA898', '#D4956A', '#8B7355', '#3D7A6F']`

### Chart chrome

- Grid: `c47` @ 0.5 opacity; axis lines: `c46` @ 0.65
- Ticks / legend: `c59`, `f5`
- Tooltip: `c2` bg, `c58` text, border `c46`, shadow per Section 2.3

---

## 7. Agent Prompt Guide

### Do's

- Pair **`c29` teal** with **`c31` copper** deliberately—teal leads, copper highlights exceptions
- Mirror **cream / white / cream-hover** layering across layout and cards
- Keep **navigation** in **dark teal** with **white** type; content area uses **`c58` / `c59`**
- Use **standard** shadow tokens; this theme should feel precise, not theatrical
- Reference **`c56`** for page background in App Studio and pro-code wrappers

### Don'ts

- Never use **`c60`** for typography
- Do not import cool **blue-gray** borders from unrelated themes—stick to **`c46` / `c47`**
- Avoid a third saturated accent beyond teal + copper unless it is a **status** color
- Do not set **teal text** (`c29`) on **teal backgrounds** without verifying contrast

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #FAF7F2     Card surface → c2   #FFFFFF
Hover        → c3        #F2EDE6     Nav bg       → c4   #2C4A42
Nav active   → c5        #3A5E54     Nav hover    → c32  #345248
Header       → c6        #F2EDE6     Input fill   → c7   #FFFFFF
Accent       → c29       #4D8A7F     Accent ↓     → c30  #3D7A6F
Copper       → c31       #B87333
Border       → c46       #C4BEB4     Border light → c47  #DDD8D0
Primary text → c58       #2E2A24     Secondary    → c59  #706A60
Nav text     → c2        #FFFFFF
Grayscale    → c40–c54 warm ramp; c46–c47 borders
Never        → c60 for fonts
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#4D8A7F',
  primaryPressed: '#3D7A6F',
  copper: '#B87333',
  surface: '#FFFFFF',
  bg: '#FAF7F2',
  text: '#2E2A24',
  textMuted: '#706A60',
  border: '#C4BEB4',
  borderLight: '#DDD8D0',
  navBg: '#2C4A42',
  navActive: '#3A5E54',
  navHover: '#345248',
  onDarkChrome: '#FFFFFF',
  series: ['#4D8A7F', '#B87333', '#6AA898', '#D4956A', '#8B7355', '#3D7A6F']
};
```

### Example Agent Prompts

- **“Patina KPI card”**: White `c2`, shadow standard, value `f7` `c58`, label `f8` `c59`, optional 3px bottom rule in `c31` copper.
- **“Teal primary button”**: Fill `c29`, hover `c30`, text `c2`, focus ring `c30` 2px.
- **“Copper alert badge”**: Background `#FDF4EC`, text `c31`, border `c31` @ 40% opacity, `f6`.
- **“Dual-accent line chart”**: Historical `c29`, comparison `c31`, forecast dashed `c30`, grid `c47`.

### Pro-Code `:root` Reference

```css
:root {
  --bg: #FAF7F2;
  --surface: #FFFFFF;
  --surface-hover: #F2EDE6;
  --nav-bg: #2C4A42;
  --nav-active: #3A5E54;
  --nav-hover: #345248;
  --accent: #4D8A7F;
  --accent-pressed: #3D7A6F;
  --copper: #B87333;
  --border: #C4BEB4;
  --border-light: #DDD8D0;
  --text-primary: #2E2A24;
  --text-secondary: #706A60;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
```

### Parity Checklist

1. **`c56`** equals canvas cream and appears in JSON.
2. Nav font colors reference **`c2`**, body references **`c58` / `c59`**.
3. Tabs active state: **`c9`** fill with **`c2`** text (white on teal).
4. Zero **`c60`** font slots after import.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Copper Patina",
  "colors": [
    { "index": 1, "value": "#FAF7F2", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#F2EDE6", "tag": "PRIMARY" },
    { "index": 4, "value": "#2C4A42", "tag": "PRIMARY" },
    { "index": 5, "value": "#3A5E54", "tag": "PRIMARY" },
    { "index": 6, "value": "#F2EDE6", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#4D8A7F", "tag": "SECONDARY" },
    { "index": 10, "value": "#F2EDE6", "tag": "PRIMARY" },
    { "index": 11, "value": "#FAF7F2", "tag": "PRIMARY" },
    { "index": 12, "value": "#F2EDE6", "tag": "PRIMARY" },
    { "index": 29, "value": "#4D8A7F", "tag": "SECONDARY" },
    { "index": 30, "value": "#3D7A6F", "tag": "SECONDARY" },
    { "index": 31, "value": "#B87333", "tag": "SECONDARY" },
    { "index": 32, "value": "#345248", "tag": "SECONDARY" },
    { "index": 40, "value": "#141210", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#201E1C", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#2C2A26", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#3A3632", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#4A4540", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#5C5650", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#C4BEB4", "tag": "CUSTOM" },
    { "index": 47, "value": "#DDD8D0", "tag": "CUSTOM" },
    { "index": 48, "value": "#8A8580", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#A39E98", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#BCB7B0", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#D0CCC5", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#E0DCD6", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#ECE9E4", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F7F4F0", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#FAF7F2", "tag": "PRIMARY" },
    { "index": 58, "value": "#2E2A24", "tag": "FONT" },
    { "index": 59, "value": "#706A60", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Sans", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Sans", "weight": "SemiBold", "size": "16px", "style": "normal" },
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
      "activeColor": { "type": "COLOR_REFERENCE", "index": 29 },
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

> **Import note**: Tab active pairs **`c9`** (`#4D8A7F`) with **`c2`** white type. Buttons default to muted **`c59`** on white—promote primary actions to filled **`c29`** in the editor or pro-code.
