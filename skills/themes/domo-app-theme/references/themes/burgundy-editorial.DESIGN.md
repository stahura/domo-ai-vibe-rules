# Burgundy Editorial — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Wine burgundy / antique gold · **Mood**: Magazine editorial, cellar warmth, luxury print on cream stock

---

## 1. Visual Theme and Atmosphere

**Personality**: The page reads like uncoated cream paper (`#FFF8F5`); cards are pure white insert panels. A **wine-stained navigation rail** (`#3A0E1E`) anchors the layout like a folio spine, while burgundy (`#722F37`) and antique gold (`#B48C5A`) carry brand and data emphasis. Typography is **all-serif**—this is not a generic SaaS dashboard; it is an editorial spread with numbers.

**Density**: Medium. Serif body at 13px needs **line-height ~1.55** and comfortable padding (20px cards). Avoid cramming more than three KPIs across on narrow breakpoints without shrinking below 11px UI type.

**Philosophy**: **Dark nav on a light page** is intentional contrast—like a book’s spine against pages. Active navigation should read as **underlined** (or underline-adjacent) in implementation: use **`c29`** or a **2px gold rule** (`c31`) in pro-code when App Studio’s native indicator is a bar. Keep large fields neutral; let charts and CTAs carry the wine/gold story.

**Atmosphere cues**:
- Warm cream canvas—never cool blue-gray page fills
- Wine nav uses **`#FFFFFF` (`c2`)** for link and title text to preserve contrast; **never `c58` on `c4`**
- Body copy is **warm espresso** (`#2E1A14`); secondary is **taupe** (`#7A6458`)
- Borders feel like **deckled paper**—soft brown-gray, not neon dividers

---

## 2. Color System

### 2.1 Semantic Palette

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|----------------|
| Page background (reference) | `#FFF8F5` | `oklch(0.984 0.009 44.9)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c2` | `--surface` |
| Surface hover | `#F8F0EC` | `oklch(0.960 0.010 48.6)` | `c3` | `--surface-hover` |
| Navigation background | `#3A0E1E` | `oklch(0.245 0.071 1.5)` | `c4` | `--nav-bg` |
| Navigation active | `#5A1E32` | `oklch(0.334 0.090 2.7)` | `c5` | `--nav-active` |
| Header background | `#FFF8F5` | `oklch(0.984 0.009 44.9)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c7` | `--input-bg` |
| Tab default background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c8` | `--tab-bg` |
| Tab active background | `#722F37` | `oklch(0.401 0.095 15.1)` | `c9` | `--tab-active-bg` |
| Table header background | `#F5EBE6` | `oklch(0.947 0.013 48.6)` | `c10` | `--table-header-bg` |
| Table row stripe | `#FDF6F3` | `oklch(0.978 0.009 44.9)` | `c11` | `--table-stripe` |
| Table row hover | `#F8F0EC` | `oklch(0.960 0.010 48.6)` | `c12` | `--table-row-hover` |
| Accent primary | `#722F37` | `oklch(0.401 0.095 15.1)` | `c29` | `--accent` |
| Accent pressed | `#5C242C` | `oklch(0.344 0.082 13.7)` | `c30` | `--accent-pressed` |
| Secondary (antique gold) | `#B48C5A` | `oklch(0.667 0.083 71.8)` | `c31` | `--accent-gold` |
| Navigation hover | `#4A1628` | `oklch(0.290 0.081 2.2)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#1A0C08` | `oklch(0.174 0.026 37.2)` | `c40` | `--gray-950` |
| Grayscale 2 | `#241612` | `oklch(0.217 0.024 36.6)` | `c41` | `--gray-900` |
| Grayscale 3 | `#2E1C18` | `oklch(0.248 0.030 33.0)` | `c42` | `--gray-850` |
| Grayscale 4 | `#3A241E` | `oklch(0.286 0.036 35.9)` | `c43` | `--gray-800` |
| Grayscale 5 | `#4A3228` | `oklch(0.342 0.039 43.5)` | `c44` | `--gray-750` |
| Grayscale 6 | `#5A4034` | `oklch(0.397 0.042 45.8)` | `c45` | `--gray-700` |
| Border | `#D4C4B8` | `oklch(0.830 0.025 59.3)` | `c46` | `--border` |
| Border light | `#E8DCD4` | `oklch(0.902 0.017 56.2)` | `c47` | `--border-light` |
| Input border | `#D4C4B8` | `oklch(0.830 0.025 59.3)` | `c48` | `--input-border` |
| Grayscale 7 | `#8A7568` | `oklch(0.578 0.033 53.6)` | `c49` | `--gray-600` |
| Grayscale 8 | `#9A8678` | `oklch(0.634 0.032 57.1)` | `c50` | `--gray-500` |
| Grayscale 9 | `#B0A090` | `oklch(0.715 0.029 67.3)` | `c51` | `--gray-400` |
| Grayscale 10 | `#C8B8A8` | `oklch(0.792 0.029 67.4)` | `c52` | `--gray-300` |
| Grayscale 11 | `#DCCCBF` | `oklch(0.855 0.025 61.6)` | `c53` | `--gray-200` |
| Grayscale 12 | `#EDE0D6` | `oklch(0.914 0.020 60.2)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#FFF8F5` | `oklch(0.984 0.009 44.9)` | `c56` | `--bg` |
| Primary text (FONT) | `#2E1A14` | `oklch(0.243 0.034 37.4)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#7A6458` | `oklch(0.521 0.034 50.2)` | `c59` | `--text-secondary` |

Light mode: **`c58`** is warm dark body copy; **`c59`** is medium taupe for captions—on **cream/white** only. On **wine nav**, use **`c2`** for text.

### 2.2 Status Colors

| Status | Primary | Primary OKLCH | Background | Background OKLCH | Text | Text OKLCH | CSS Variable |
|--------|---------|---------------|------------|------------------|------|------------|----------------|
| On track | `#6B8E6B` | `oklch(0.610 0.065 144.7)` | `#EEF4EE` | `oklch(0.961 0.010 145.5)` | `#2D4A2D` | `oklch(0.377 0.060 144.3)` | `--status-on-track` |
| At risk | `#C98A40` | `oklch(0.683 0.118 67.7)` | `#FBF4E8` | `oklch(0.967 0.017 76.1)` | `#6B4818` | `oklch(0.431 0.079 71.1)` | `--status-at-risk` |
| Behind | `#A05050` | `oklch(0.529 0.106 21.3)` | `#F8EBE8` | `oklch(0.949 0.015 33.1)` | `#5A2828` | `oklch(0.346 0.074 21.6)` | `--status-behind` |
| Complete | `#722F37` | `oklch(0.401 0.095 15.1)` | `#F5E8EA` | `oklch(0.942 0.014 6.7)` | `#722F37` | `oklch(0.401 0.095 15.1)` | `--status-complete` |

### 2.3 Shadows

Warm charcoal from **`#2E1A14`** at restrained opacity—paper lift, not glass morphism.

```css
--shadow:
  0px 0px 0px 1px oklch(0.243 0.034 37.4 / 0.06),
  0px 1px 3px -1px oklch(0.243 0.034 37.4 / 0.06),
  0px 4px 14px 0px oklch(0.243 0.034 37.4 / 0.05);
--shadow-hover:
  0px 0px 0px 1px oklch(0.243 0.034 37.4 / 0.09),
  0px 3px 8px -1px oklch(0.243 0.034 37.4 / 0.07),
  0px 8px 22px 0px oklch(0.243 0.034 37.4 / 0.06);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: Georgia, "Times New Roman", "Palatino Linotype", serif;
```

App Studio: **Serif** on **every** font slot (`f1`–`f8`). Mixing Sans on charts while cards remain Serif reads as a production error.

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance`; +0.01em tracking optional |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Slightly tight leading |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height **1.55** for serif legibility |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.06em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill: c59` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges—Serif SemiBold feels editorial, not athletic
- **Regular (400)**: Body, axes, table cells
- **Light (300)**: KPI labels only
- Avoid weights **700+**—they fracture the magazine calm

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Border | Padding | Notes |
|-----------|------|------------|------------|--------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | none | 20px | Accent `c29`; chart `f5` Serif |
| `ca2` | Controls | `c2` | `c58` | 10px | Standard | none | 16px | Hover chips → `c3` |
| `ca3` | Editorial narrative | `c2` | `c58` | 10px | Soft | none | 20px | Long-form pull quotes |
| `ca4` | Compact | `c2` | `c58` | 8px | Minimal | none | 12px | Filters |
| `ca5` | KPI | `c2` | `c58` | 12px | Standard | optional gold `c31` rule | 16px | Value may inherit status hue |
| `ca6` | Muted | `c3` | `c58` | 8px | none | none | 12px | Secondary metrics on cream |
| `ca7` | Callout | `c31` @ 15% on `c2` | `c58` | 10px | Standard | none | 16px | Gold wash, not solid |
| `ca8` | Masthead strip | `c56` | `c58` | 0 | none | none | 12px | Section banners |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#3A0E1E` wine | `c4` |
| Active background | `#5A1E32` | `c5` |
| Hover background | `#4A1628` | `c32` |
| Title font color | `#FFFFFF` | `c2` (white on dark chrome) |
| Link font color | `#FFFFFF` | `c2` |
| Active link color | `#FFFFFF` | `c2` |
| Active indicator | `#B48C5A` gold rule / underline | `c31` |
| Underline treatment | **2px solid `c31`** under active label | pro-code / custom CSS |
| Title font | 22px SemiBold **Serif** | `f1` |
| Link font | 13px Regular **Serif** | `f3` |
| Signature | **Wine rail + white type + gold underline**—editorial spine |

> Native App Studio may render `activeColor` as a **vertical bar**. For true **underline** navigation, override link styles in pro-code: `text-decoration-thickness: 2px; text-underline-offset: 4px; text-decoration-color: var(--accent-gold)`.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#722F37` | `oklch(0.401 0.095 15.1)` | Burgundy lead |
| 2 | `#B48C5A` | `oklch(0.667 0.083 71.8)` | Antique gold |
| 3 | `#9A5060` | `oklch(0.525 0.100 7.3)` | Rosé midtone |
| 4 | `#8A7050` | `oklch(0.562 0.056 72.1)` | Barrel brown |
| 5 | `#A04048` | `oklch(0.504 0.128 17.9)` | Deep scarlet |
| 6 | `#C4A070` | `oklch(0.727 0.077 74.1)` | Parchment gold |

**Pro-code series array**: `['#722F37', '#B48C5A', '#9A5060', '#8A7050', '#A04048', '#C4A070']`

**Chart chrome**: Grid `c47` @ 0.5 opacity; axis `c46`; ticks `c59`; tooltips `c2` + `--shadow`.

### 6.1 Semantic chart anchors

| Role | Hex | OKLCH | Notes |
|------|-----|-------|---------|
| Positive | `#6B8E6B` | `oklch(0.610 0.065 144.7)` | Favorable variance |
| Negative | `#A05050` | `oklch(0.529 0.106 21.3)` | Unfavorable |
| Total | `#7A6458` | `oklch(0.521 0.034 50.2)` | Neutral reference |
| Highlight | `#B48C5A` | `oklch(0.667 0.083 71.8)` | Callout series |

### 6.2 Interaction rules

- Keep chart backgrounds **`c2`** inside cards; page remains **`c56`**
- Do not use **cool blues** for grid lines—stay in **`c46` / `c47`**
- Serif legends at **`f5`**; maintain **`c59`** for axis numerals

---

## 7. Agent Prompt Guide

### Do's

- Bind **nav typography** to **`c2`** on **`c4`**—this is a hard contrast rule
- Keep **`c56`** cream aligned with **`c1`** for page continuity
- Run **Serif** across **all eight** JSON font slots before writing custom CSS
- Use **`c31`** for **underline** and secondary “premium” emphasis alongside **`c29`**
- Apply **line-height 1.55** on 13px body in pro-code containers

### Don'ts

- Do not place **`c58`** text directly on **`c4`** wine without failing WCAG
- Do not substitute **system Sans** “for chart performance” on a Serif system
- Avoid **`c60`** for font color documentation
- Do not default to **gray** borders from unrelated themes—use **`c46` / `c47`**

### Slot Mapping Cheat Sheet

```
c1 / c56   → #FFF8F5   cream page
c2         → #FFFFFF   cards + nav text on wine
c3         → #F8F0EC   hover
c4         → #3A0E1E   wine nav
c5         → #5A1E32   nav active
c6         → #FFF8F5   headers
c7         → #FFFFFF   inputs
c8–c12     → tabs + tables (cream tints)
c29 / c30  → #722F37 / #5C242C   burgundy / pressed
c31        → #B48C5A   gold underline + secondary
c32        → #4A1628   nav hover
c40–c45    → warm dark ramp
c46–c48    → #D4C4B8 / #E8DCD4 / #D4C4B8   borders + input border
c49–c54    → warm light ramp
c58 / c59  → #2E1A14 / #7A6458   FONT on light surfaces
Nav text   → c2 on c4 only
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#722F37',
  primaryPressed: '#5C242C',
  secondary: '#B48C5A',
  surface: '#FFFFFF',
  bg: '#FFF8F5',
  text: '#2E1A14',
  textMuted: '#7A6458',
  border: '#D4C4B8',
  borderLight: '#E8DCD4',
  navBg: '#3A0E1E',
  navActive: '#5A1E32',
  navHover: '#4A1628',
  onDarkChrome: '#FFFFFF',
  series: ['#722F37', '#B48C5A', '#9A5060', '#8A7050', '#A04048', '#C4A070']
};
```

### Example Agent Prompts

- **“Cream editorial dashboard”**: Page `c56`, cards `c2`, shadows from Section 2.3—no harsh outlines.
- **“Wine nav with gold underline”**: Background `c4`, text `c2`, active `c5`, `border-bottom: 2px solid #B48C5A` on active link.
- **“Serif KPI tile”**: `f7` + `f8` both **Serif**; value `c58`, label `c59`; optional `c31` left rule.
- **“Burgundy CTA”**: Fill `c29`, pressed `c30`, label `c2`; focus ring `c30`.
- **“Magazine table”**: Header `c10`, stripe `c11`, hover `c12`, borders `c47`.

### Pro-Code `:root` token block

```css
:root {
  --bg: oklch(0.984 0.009 44.9);
  --surface: oklch(1 0 0);
  --surface-hover: oklch(0.960 0.010 48.6);
  --text-primary: oklch(0.243 0.034 37.4);
  --text-secondary: oklch(0.521 0.034 50.2);
  --border: oklch(0.830 0.025 59.3);
  --border-light: oklch(0.902 0.017 56.2);
  --accent: oklch(0.401 0.095 15.1);
  --accent-pressed: oklch(0.344 0.082 13.7);
  --accent-gold: oklch(0.667 0.083 71.8);
  --nav-bg: oklch(0.245 0.071 1.5);
  --font-stack: Georgia, "Times New Roman", "Palatino Linotype", serif;
}
```

### Import parity checklist

1. **All `fonts` entries**: `"family": "Serif"`.
2. **Navigation** link/title colors → **`c2`**, not **`c58`**.
3. **`c56`** present and equals **`#FFF8F5`**.
4. **Tabs**: active background **`c9`** with **`c2`** text.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Burgundy Editorial",
  "colors": [
    { "index": 1, "value": "#FFF8F5", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#F8F0EC", "tag": "PRIMARY" },
    { "index": 4, "value": "#3A0E1E", "tag": "PRIMARY" },
    { "index": 5, "value": "#5A1E32", "tag": "PRIMARY" },
    { "index": 6, "value": "#FFF8F5", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#722F37", "tag": "SECONDARY" },
    { "index": 10, "value": "#F5EBE6", "tag": "PRIMARY" },
    { "index": 11, "value": "#FDF6F3", "tag": "PRIMARY" },
    { "index": 12, "value": "#F8F0EC", "tag": "PRIMARY" },
    { "index": 29, "value": "#722F37", "tag": "SECONDARY" },
    { "index": 30, "value": "#5C242C", "tag": "SECONDARY" },
    { "index": 31, "value": "#B48C5A", "tag": "SECONDARY" },
    { "index": 32, "value": "#4A1628", "tag": "SECONDARY" },
    { "index": 40, "value": "#1A0C08", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#241612", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#2E1C18", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#3A241E", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#4A3228", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#5A4034", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#D4C4B8", "tag": "CUSTOM" },
    { "index": 47, "value": "#E8DCD4", "tag": "CUSTOM" },
    { "index": 48, "value": "#D4C4B8", "tag": "CUSTOM" },
    { "index": 49, "value": "#8A7568", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#9A8678", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B0A090", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C8B8A8", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#DCCCBF", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#EDE0D6", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#FFF8F5", "tag": "PRIMARY" },
    { "index": 58, "value": "#2E1A14", "tag": "FONT" },
    { "index": 59, "value": "#7A6458", "tag": "FONT" }
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
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 1 },
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
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "activeBackgroundColor": { "type": "COLOR_REFERENCE", "index": 29 },
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "forms": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "borderColor": { "type": "COLOR_REFERENCE", "index": 48 },
      "focusBorderColor": { "type": "COLOR_REFERENCE", "index": 29 },
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm **Serif** on all font slots and **white (`c2`)** navigation labels on **wine (`c4`)**. Add **underline** styling in pro-code if the native active indicator is not underline-shaped.
