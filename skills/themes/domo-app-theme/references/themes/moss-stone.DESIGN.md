# Moss & Stone — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Olive / warm brown · **Mood**: Earthy organic calm, agriculture and field operations, stone-warm canvas

---

## 1. Visual Theme and Atmosphere

**Personality**: The page is **warm field stone** (`#F2EDE4`); cards are **clean white** inserts. A **deep moss navigation** (`#3A4A32`) grounds the app like a barn door on limestone. **Olive** (`#697A55`) leads accents and primary series; **warm brown** (`#8B7355`) provides soil-toned secondary emphasis. Typography is **all slab**—sturdy, agricultural, and legible in sunlight-glare scenarios (metaphorically: high ambient light UI).

**Density**: Medium. Slab letterforms need a touch more air than ultra-compact Sans—keep **20px** card padding and **12px** element gaps for standard analytics tiles.

**Philosophy**: **Earth before neon**: if a color would not appear on a topo map, trail signage, or grain sack, question its use. Charts carry **green/brown/tan** families; chrome stays stone and moss. White cards on stone canvas sell the “outdoor operations” story without literal photography.

**Atmosphere cues**:
- Hover on white returns to **`#EBE5DA`**, not cool gray
- Moss nav requires **`c2` white** type—**never `c58` on `c4`**
- Text is **warm dark loam** (`#2A2820`); secondary is **driftwood** (`#6A6458`)
- Shadows are **warm**, sampled from **`c58`** at low alpha—like paper on stone, not glass

---

## 2. Color System

### 2.1 Semantic Palette

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|----------------|
| Page background (reference) | `#F2EDE4` | `oklch(0.948 0.013 82.4)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c2` | `--surface` |
| Surface hover | `#EBE5DA` | `oklch(0.924 0.016 82.8)` | `c3` | `--surface-hover` |
| Navigation background | `#3A4A32` | `oklch(0.388 0.044 135.5)` | `c4` | `--nav-bg` |
| Navigation active | `#4E5E44` | `oklch(0.461 0.045 133.7)` | `c5` | `--nav-active` |
| Header background | `#F2EDE4` | `oklch(0.948 0.013 82.4)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c7` | `--input-bg` |
| Tab default background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c8` | `--tab-bg` |
| Tab active background | `#697A55` | `oklch(0.555 0.058 128.2)` | `c9` | `--tab-active-bg` |
| Table header background | `#E8E4DC` | `oklch(0.920 0.012 84.6)` | `c10` | `--table-header-bg` |
| Table row stripe | `#F5F2EB` | `oklch(0.962 0.010 87.5)` | `c11` | `--table-stripe` |
| Table row hover | `#EBE5DA` | `oklch(0.924 0.016 82.8)` | `c12` | `--table-row-hover` |
| Accent primary | `#697A55` | `oklch(0.555 0.058 128.2)` | `c29` | `--accent` |
| Accent pressed | `#586A46` | `oklch(0.499 0.059 129.9)` | `c30` | `--accent-pressed` |
| Secondary (warm brown) | `#8B7355` | `oklch(0.571 0.053 72.7)` | `c31` | `--accent-earth` |
| Navigation hover | `#445438` | `oklch(0.424 0.049 132.4)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#141610` | `oklch(0.196 0.012 122.5)` | `c40` | `--gray-950` |
| Grayscale 2 | `#1C1E18` | `oklch(0.231 0.012 122.3)` | `c41` | `--gray-900` |
| Grayscale 3 | `#242620` | `oklch(0.264 0.011 122.2)` | `c42` | `--gray-850` |
| Grayscale 4 | `#2C2E28` | `oklch(0.297 0.011 122.1)` | `c43` | `--gray-800` |
| Grayscale 5 | `#34362E` | `oklch(0.328 0.014 118.6)` | `c44` | `--gray-750` |
| Grayscale 6 | `#3C3E34` | `oklch(0.359 0.017 116.4)` | `c45` | `--gray-700` |
| Border | `#C4BAA8` | `oklch(0.792 0.027 82.4)` | `c46` | `--border` |
| Border light | `#D8D0C2` | `oklch(0.860 0.021 81.8)` | `c47` | `--border-light` |
| Input border | `#C4BAA8` | `oklch(0.792 0.027 82.4)` | `c48` | `--input-border` |
| Grayscale 7 | `#7A7468` | `oklch(0.561 0.019 84.6)` | `c49` | `--gray-600` |
| Grayscale 8 | `#8A8478` | `oklch(0.615 0.019 84.6)` | `c50` | `--gray-500` |
| Grayscale 9 | `#9A9488` | `oklch(0.668 0.019 84.6)` | `c51` | `--gray-400` |
| Grayscale 10 | `#B4AEA0` | `oklch(0.752 0.021 87.5)` | `c52` | `--gray-300` |
| Grayscale 11 | `#C8C2B4` | `oklch(0.815 0.020 87.5)` | `c53` | `--gray-200` |
| Grayscale 12 | `#DCD6C8` | `oklch(0.877 0.020 87.5)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#F2EDE4` | `oklch(0.948 0.013 82.4)` | `c56` | `--bg` |
| Primary text (FONT) | `#2A2820` | `oklch(0.276 0.014 95.6)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#6A6458` | `oklch(0.505 0.020 84.6)` | `c59` | `--text-secondary` |

Light mode: **`c58`** is warm near-black for titles and body; **`c59`** is medium stone-brown for captions. On **moss nav**, bind text to **`c2`**.

### 2.2 Status Colors

| Status | Primary | Primary OKLCH | Background | Background OKLCH | Text | Text OKLCH | CSS Variable |
|--------|---------|---------------|------------|------------------|------|------------|----------------|
| On track | `#5A7A48` | `oklch(0.542 0.083 134.9)` | `#EEF2EA` | `oklch(0.956 0.011 128.6)` | `#2D4024` | `oklch(0.347 0.053 136.1)` | `--status-on-track` |
| At risk | `#B8893A` | `oklch(0.661 0.111 77.5)` | `#FBF4E8` | `oklch(0.969 0.018 81.3)` | `#5C4818` | `oklch(0.413 0.070 85.9)` | `--status-at-risk` |
| Behind | `#A06050` | `oklch(0.557 0.088 34.8)` | `#F8EBE8` | `oklch(0.949 0.015 33.1)` | `#4A2820` | `oklch(0.319 0.053 34.1)` | `--status-behind` |
| Complete | `#697A55` | `oklch(0.555 0.058 128.2)` | `#EEF1EA` | `oklch(0.954 0.010 125.7)` | `#3A4A30` | `oklch(0.387 0.047 133.9)` | `--status-complete` |

### 2.3 Shadows

Warm lift from **`#2A2820`** at gentle opacity—stone slab, not fluorescent office.

```css
--shadow:
  0px 0px 0px 1px oklch(0.276 0.014 95.6 / 0.06),
  0px 1px 3px -1px oklch(0.276 0.014 95.6 / 0.06),
  0px 4px 14px 0px oklch(0.276 0.014 95.6 / 0.05);
--shadow-hover:
  0px 0px 0px 1px oklch(0.276 0.014 95.6 / 0.09),
  0px 3px 8px -1px oklch(0.276 0.014 95.6 / 0.07),
  0px 8px 22px 0px oklch(0.276 0.014 95.6 / 0.06);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: "Roboto Slab", Rockwell, "Courier New", serif;
```

App Studio: **Slab** on **all** slots (`f1`–`f8`) per platform mapping. Slab delivers the **ag / sustainability / outdoor ops** voice—stable, honest, and highly legible.

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Slightly open leading |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height **1.52** |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.05em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill: c59` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges
- **Regular (400)**: Body, axes, tables
- **Light (300)**: KPI labels only
- Slab at **700+** looks industrial-fast—stay at **600** max for UI chrome

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Border | Padding | Notes |
|-----------|------|------------|------------|--------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | none | 20px | Accent `c29`; charts `f5` Slab |
| `ca2` | Controls | `c2` | `c58` | 10px | Standard | none | 16px | Chips hover `c3` |
| `ca3` | Field narrative | `c2` | `c58` | 10px | Soft | none | 20px | Sustainability copy blocks |
| `ca4` | Compact | `c2` | `c58` | 8px | Minimal | none | 12px | Dense filters |
| `ca5` | KPI | `c2` | `c58` | 12px | Standard | optional `c31` rule | 16px | Yield / acre metrics |
| `ca6` | Muted | `c3` | `c58` | 8px | none | none | 12px | Secondary metrics on stone |
| `ca7` | Callout | `c29` @ 12% on `c2` | `c58` | 10px | Standard | none | 16px | Olive wash |
| `ca8` | Banner | `c56` | `c58` | 0 | none | none | 12px | Full-bleed stone strip |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#3A4A32` deep moss | `c4` |
| Active | `#4E5E44` | `c5` |
| Hover | `#445438` | `c32` |
| Title font color | `#FFFFFF` | `c2` |
| Link font color | `#FFFFFF` | `c2` |
| Active link color | `#FFFFFF` | `c2` |
| Active indicator | `#697A55` | `c29` |
| Secondary hint (optional) | `#8B7355` | `c31` |
| Title font | 22px SemiBold **Slab** | `f1` |
| Link font | 13px Regular **Slab** | `f3` |
| Signature | **Moss rail + white type**—barn / trailhead authority |

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#697A55` | `oklch(0.555 0.058 128.2)` | Olive primary |
| 2 | `#8B7355` | `oklch(0.571 0.053 72.7)` | Warm brown |
| 3 | `#A09470` | `oklch(0.668 0.052 91.8)` | Khaki field |
| 4 | `#88A076` | `oklch(0.676 0.066 132.2)` | Spring green |
| 5 | `#6A5A44` | `oklch(0.477 0.039 75.4)` | Dark loam |
| 6 | `#7A9A68` | `oklch(0.649 0.080 134.7)` | Fern |

**Pro-code series array**: `['#697A55', '#8B7355', '#A09470', '#88A076', '#6A5A44', '#7A9A68']`

**Chart chrome**: Grid `c47` @ 0.5 opacity; axis `c46`; ticks `c59`; tooltips `c2` + `--shadow`.

### 6.1 Semantic chart anchors

| Role | Hex | OKLCH | Notes |
|------|-----|-------|---------|
| Positive | `#5A7A48` | `oklch(0.542 0.083 134.9)` | Favorable yield |
| Negative | `#A06050` | `oklch(0.557 0.088 34.8)` | Shortfall |
| Total | `#6A6458` | `oklch(0.505 0.020 84.6)` | Neutral baseline |
| Highlight | `#8B7355` | `oklch(0.571 0.053 72.7)` | Soil / cost overlay |

### 6.2 Interaction rules

- Avoid **neon** greens; stay in **muted organic** chroma
- Inactive series **0.35** opacity; hovered **1.0**
- Legends use **`f5`** at **`c59`**

---

## 7. Agent Prompt Guide

### Do's

- Align **`c56`** stone with **`c1`** for seamless page chrome
- Use **`c2` white** on **`c4` moss** for all navigation typography
- Keep **Slab** across **every** JSON font slot
- Pair **`c29` olive** with **`c31` earth brown** for dual-series field stories
- Use **warm shadows** from Section 2.3—never cool blue-gray stacks

### Don'ts

- Do not place **`c58`** directly on **`c4`** without failing contrast
- Do not import **corporate blue** chart palettes into this vertical skin
- Avoid **`c60`** for font documentation
- Do not strip **moss nav** to gray “for neutrality”—green chroma is intentional

### Slot Mapping Cheat Sheet

```
c1 / c56   → #F2EDE4   warm stone page
c2         → #FFFFFF   cards + nav text on moss
c3         → #EBE5DA   hover
c4         → #3A4A32   moss nav
c5         → #4E5E44   nav active
c6         → #F2EDE4   headers
c7         → #FFFFFF   inputs
c8–c12     → tabs + tables (stone tints)
c29 / c30  → #697A55 / #586A46   olive / pressed
c31        → #8B7355   earth brown
c32        → #445438   nav hover
c40–c45    → warm olive-gray ramp
c46–c48    → #C4BAA8 / #D8D0C2 / #C4BAA8   borders + input border
c49–c54    → light stone ramp
c58 / c59  → #2A2820 / #6A6458   FONT on light UI
Nav text   → c2 on c4 only
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#697A55',
  primaryPressed: '#586A46',
  secondary: '#8B7355',
  surface: '#FFFFFF',
  bg: '#F2EDE4',
  text: '#2A2820',
  textMuted: '#6A6458',
  border: '#C4BAA8',
  borderLight: '#D8D0C2',
  navBg: '#3A4A32',
  navActive: '#4E5E44',
  navHover: '#445438',
  onDarkChrome: '#FFFFFF',
  series: ['#697A55', '#8B7355', '#A09470', '#88A076', '#6A5A44', '#7A9A68']
};
```

### Example Agent Prompts

- **“Stone page + white yield cards”**: Layout `c56`, cards `c2`, `var(--shadow)` from Section 2.3.
- **“Moss navigation”**: `c4` background, `c2` labels, active `c5`, indicator `c29`.
- **“Slab KPI for acres”**: `f7`/`f8` **Slab**; values `c58`; positive delta optional `c29`.
- **“Brown vs olive combo chart”**: Series[0] `c29`, Series[1] `c31`; grid `c47`.
- **“Sustainability table”**: Header `c10`, stripes `c11`, hover `c12`.

### Pro-Code `:root` token block

```css
:root {
  --bg: oklch(0.948 0.013 82.4);
  --surface: oklch(1 0 0);
  --surface-hover: oklch(0.924 0.016 82.8);
  --text-primary: oklch(0.276 0.014 95.6);
  --text-secondary: oklch(0.505 0.020 84.6);
  --border: oklch(0.792 0.027 82.4);
  --border-light: oklch(0.860 0.021 81.8);
  --accent: oklch(0.555 0.058 128.2);
  --accent-pressed: oklch(0.499 0.059 129.9);
  --earth: oklch(0.571 0.053 72.7);
  --nav-bg: oklch(0.388 0.044 135.5);
  --font-stack: "Roboto Slab", Rockwell, "Courier New", serif;
}
```

### Import parity checklist

1. **Fonts**: `"family": "Slab"` on indices **1–8**.
2. **Navigation** text colors → **`c2`**.
3. **`c56`** equals **`#F2EDE4`**.
4. **Tabs**: active **`c9`** with **`c2`** text for contrast on olive fill.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Moss & Stone",
  "colors": [
    { "index": 1, "value": "#F2EDE4", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#EBE5DA", "tag": "PRIMARY" },
    { "index": 4, "value": "#3A4A32", "tag": "PRIMARY" },
    { "index": 5, "value": "#4E5E44", "tag": "PRIMARY" },
    { "index": 6, "value": "#F2EDE4", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#697A55", "tag": "SECONDARY" },
    { "index": 10, "value": "#E8E4DC", "tag": "PRIMARY" },
    { "index": 11, "value": "#F5F2EB", "tag": "PRIMARY" },
    { "index": 12, "value": "#EBE5DA", "tag": "PRIMARY" },
    { "index": 29, "value": "#697A55", "tag": "SECONDARY" },
    { "index": 30, "value": "#586A46", "tag": "SECONDARY" },
    { "index": 31, "value": "#8B7355", "tag": "SECONDARY" },
    { "index": 32, "value": "#445438", "tag": "SECONDARY" },
    { "index": 40, "value": "#141610", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#1C1E18", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#242620", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#2C2E28", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#34362E", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#3C3E34", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#C4BAA8", "tag": "CUSTOM" },
    { "index": 47, "value": "#D8D0C2", "tag": "CUSTOM" },
    { "index": 48, "value": "#C4BAA8", "tag": "CUSTOM" },
    { "index": 49, "value": "#7A7468", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#8A8478", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#9A9488", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#B4AEA0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#C8C2B4", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#DCD6C8", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#F2EDE4", "tag": "PRIMARY" },
    { "index": 58, "value": "#2A2820", "tag": "FONT" },
    { "index": 59, "value": "#6A6458", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Slab", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Slab", "weight": "SemiBold", "size": "16px", "style": "normal" },
    { "index": 3, "family": "Slab", "weight": "Regular", "size": "13px", "style": "normal" },
    { "index": 4, "family": "Slab", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 5, "family": "Slab", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 6, "family": "Slab", "weight": "SemiBold", "size": "11px", "style": "normal" },
    { "index": 7, "family": "Slab", "weight": "SemiBold", "size": "28px", "style": "normal" },
    { "index": 8, "family": "Slab", "weight": "Light", "size": "11px", "style": "normal" }
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

> **Import**: App Studio → Theme Editor → Import Theme JSON. Verify **Slab** typography and **moss** nav (`#3A4A32`) with **white** link text (`c2`).
