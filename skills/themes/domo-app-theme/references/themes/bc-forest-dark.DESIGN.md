# BC Forest Dark — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Luminous mint / forest green · **Mood**: Organic, nocturnal, calm precision

---

## 1. Visual Theme and Atmosphere

**Personality**: The light BC Forest palette turned down for night work. Deep black-greens hold the canvas; mint and sage accents glow like bioluminescence on bark. Navigation stays authoritative; data and accents feel fresh without neon harshness.

**Density**: Medium-high. Prefer tight card grids with 16px gutters and 20px interior padding on analytic cards so dense charts remain legible on `#152A1E` surfaces.

**Philosophy**: Green stays in the family—every neutral carries a hint of chlorophyll. Saturated mint (`#7BC79F`) marks primary actions, links, and the first chart series; warmer chart hues (amber, coral red) provide contrast against cool forest neutrals. Never flood the UI with accent green; let darkness and grayscale carry structure.

**Atmosphere cues**:
- Page ground reads as **forest black** (`#0B150F`), not flat gray
- Cards lift one step to **dark forest** (`#152A1E`) with **green-tinted shadows** derived from pale mint-white at low alpha
- Navigation is the **deepest well** (`#071009`) with **bright forest** active states (`#1E6B45`)
- Primary copy is **pale mint-white** (`#E8F0EC`); secondary is **sage** (`#9AB3A4`)—never pure white for body text

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#0B150F` | `oklch(0.150 0.003 42.1)` | `c1` | `--bg-ref` |
| Card surface | `#152A1E` | `oklch(0.215 0.006 42.8)` | `c2` | `--surface` |
| Hover surface | `#1E3828` | `oklch(0.257 0.008 36.6)` | `c3` | `--surface-hover` |
| Navigation background | `#071009` | `oklch(0.132 0.005 26.0)` | `c4` | `--nav-bg` |
| Navigation active | `#1E6B45` | `oklch(0.385 0.015 41.7)` | `c5` | `--nav-active` |
| Header background | `#071009` | `oklch(0.132 0.005 26.0)` | `c6` | `--header-bg` |
| Input background | `#152A1E` | `oklch(0.215 0.006 42.8)` | `c7` | `--input-bg` |
| Tab / panel surface | `#152A1E` | `oklch(0.215 0.006 42.8)` | `c8` | `--tab-bg` |
| Tab active fill | `#7BC79F` | `oklch(0.628 0.013 53.2)` | `c9` | `--tab-active-bg` |
| Table header background | `#071009` | `oklch(0.132 0.005 26.0)` | `c10` | `--table-header-bg` |
| Table row stripe | `#101C16` | `oklch(0.178 0.005 38.0)` | `c11` | `--table-stripe` |
| Table row hover | `#1E3828` | `oklch(0.257 0.008 36.6)` | `c12` | `--table-row-hover` |
| Accent primary | `#7BC79F` | `oklch(0.628 0.013 53.2)` | `c29` | `--accent` |
| Accent pressed | `#5AAE80` | `oklch(0.560 0.017 43.3)` | `c30` | `--accent-pressed` |
| Navigation / control hover | `#146240` | `oklch(0.360 0.013 49.3)` | `c31` | `--nav-hover` |
| Grayscale 1 | `#060D08` | `oklch(0.122 0.003 32.7)` | `c40` | `--gray-950` |
| Grayscale 2 | `#0A140E` | `oklch(0.146 0.004 41.7)` | `c41` | `--gray-900` |
| Grayscale 3 | `#0D1A12` | `oklch(0.166 0.004 38.2)` | `c42` | `--gray-850` |
| Grayscale 4 | `#102016` | `oklch(0.184 0.005 36.2)` | `c43` | `--gray-800` |
| Grayscale 5 | `#35483D` | `oklch(0.312 0.004 48.9)` | `c44` | `--gray-700` |
| Grayscale 6 | `#506158` | `oklch(0.389 0.003 65.9)` | `c45` | `--gray-600` |
| Border | `#2A4A36` | `oklch(0.309 0.009 35.7)` | `c46` | `--border` |
| Border light | `#1E3828` | `oklch(0.257 0.008 36.6)` | `c47` | `--border-light` |
| Grayscale 7 | `#6E7D75` | `oklch(0.470 0.003 67.6)` | `c48` | `--gray-500` |
| Grayscale 8 | `#89978F` | `oklch(0.542 0.003 57.5)` | `c49` | `--gray-400` |
| Grayscale 9 | `#A4B1AA` | `oklch(0.612 0.002 68.4)` | `c50` | `--gray-300` |
| Grayscale 10 | `#BAC4BF` | `oklch(0.664 0.001 84.0)` | `c51` | `--gray-200` |
| Grayscale 11 | `#CAD4CF` | `oklch(0.705 0.001 84.2)` | `c52` | `--gray-150` |
| Grayscale 12 | `#D9E2DE` | `oklch(0.741 0.001 106.8)` | `c53` | `--gray-100` |
| Grayscale 13 (near white) | `#E8F0EC` | `oklch(0.776 0.001 85.1)` | `c54` | `--gray-50` |
| Page background (App Studio) | `#0B150F` | `oklch(0.150 0.003 42.1)` | `c56` | `--bg` |
| Primary text (FONT) | `#E8F0EC` | `oklch(0.776 0.001 85.1)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#9AB3A4` | `oklch(0.608 0.005 48.6)` | `c59` | `--text-secondary` |
| Automatic (never set manually) | — | — | `c60` | — |

### 2.2 Status Colors

| Status | Primary | Background | Muted text / stroke | OKLCH (primary) | CSS Variable |
|--------|---------|------------|---------------------|-----------------|--------------|
| On track | `#59C886` | `#0F2418` | `#59C886` | `oklch(0.614 0.026 33.6)` | `--status-on-track` |
| At risk | `#FBAD56` | `#2A1F0F` | `#FBAD56` | `oklch(0.669 0.114 357.3)` | `--status-at-risk` |
| Behind / alert | `#E45F5F` | `#2A1414` | `#E45F5F` | `oklch(0.544 0.087 348.8)` | `--status-alert` |
| Complete / info | `#7BC79F` | `#12261C` | `#7BC79F` | `oklch(0.628 0.013 53.2)` | `--status-complete` |

### 2.3 Shadows

Tinted from primary text (`#E8F0EC`) and a whisper of mint accent so elevation reads “organic,” not neutral gray.

```css
--shadow:
  0px 0px 0px 1px oklch(0.776 0.001 85.1 / 0.14),
  0px 1px 2px -1px oklch(0.776 0.001 85.1 / 0.10),
  0px 2px 6px 0px oklch(0.628 0.013 53.2 / 0.07);
--shadow-hover:
  0px 0px 0px 1px oklch(0.776 0.001 85.1 / 0.18),
  0px 2px 6px -1px oklch(0.776 0.001 85.1 / 0.12),
  0px 6px 16px 0px oklch(0.628 0.013 53.2 / 0.10);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** for every font slot (`f1`–`f8`).

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | `text-wrap: balance` |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.5, `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase, `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill`, not CSS `color` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase, tight tracking |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase, `letter-spacing: 0.04em` |

### 3.3 Weight Rules

- **SemiBold (600)**: Page title, card titles, KPI values, badges, active control labels
- **Regular (400)**: Body, chart axes, table cells, form values
- **Light (300)**: KPI and timeframe labels only—must recede behind numbers
- Avoid **Bold (700+)** except where Domo components force it; hierarchy comes from size and mint accent, not heavy weight

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Border | Notes |
|-----------|------|------------|------------|--------|--------|---------|--------|-------|
| `ca1` | Primary analytic / chart | `c2` | `c58` | 10px | On (`c40` tint) | 20px | 0 | Accent `c29` for chart highlights |
| `ca2` | Filters / controls | `c2` | `c58` | 8px | On | 16px | `1px solid` `c47` | Inputs use `c7` |
| `ca3` | Media / embed | transparent | `c58` | 8px | Off | 8px | none | Let parent page show through |
| `ca4` | Compact list | `c2` | `c58` | 8px | Off | 12px | `c47` | Dense lists, settings panels |
| `ca5` | KPI / summary | `c2` | `c58` | 12px | On | 16px | 0 | Value `f7`, label `f8`; optional `c29` left rule |
| `ca6` | Secondary metric | `c2` | `c59` | 8px | Off | 12px | `c47` | Supporting stats |
| `ca7` | Callout | `c3` | `c58` | 10px | On | 16px | `c46` | Hover-state surface as emphasis |
| `ca8` | Banner / hero strip | transparent | `c58` | 0 | Off | 12px | none | Gradient or imagery from pro-code |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#071009` forest black | `c4` |
| Active background | `#1E6B45` bright forest | `c5` |
| Hover background | `#146240` | `c31` |
| Link font color (default) | `#9AB3A4` sage | `c59` |
| Active / title font color | `#E8F0EC` pale mint-white | `c58` |
| Active indicator / keyline | `#7BC79F` mint | `c29` |
| Title font | 22px SemiBold Sans | `f1` |
| Link font | 13px Regular Sans | `f3` |
| Button style | PILL (match BC Forest Light) | — |
| Shadow | true (subtle, same family as cards) | — |
| Divider | `1px solid` `c47` | — |

**c60 rule**: Never assign `c60` (AUTOMATIC_COLOR) to navigation or card font colors on dark chrome—it resolves to dark text and disappears.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Use |
|--------|-----|-------|-----|
| 1 | `#7BC79F` | `oklch(0.628 0.013 53.2)` | Primary series, mint anchor |
| 2 | `#A8F4CA` | `oklch(0.741 0.013 50.8)` | Secondary mint / forecast |
| 3 | `#A0D771` | `oklch(0.672 0.068 9.7)` | Lime / positive divergence |
| 4 | `#FBAD56` | `oklch(0.669 0.114 357.3)` | Warm contrast / threshold |
| 5 | `#E45F5F` | `oklch(0.544 0.087 348.8)` | Negative / alert |
| 6 | `#4D9A75` | `oklch(0.512 0.012 58.0)` | Tertiary green, depth |

Pro-code series array: `['#7BC79F', '#A8F4CA', '#A0D771', '#FBAD56', '#E45F5F', '#4D9A75']`

### Chart chrome (grid, axes, legend)

- **Gridlines**: `c47` at 50% opacity; **axis lines**: `c46` at 70% opacity.
- **Tick / legend labels**: `c59` at 11px Regular (`f5`); **tick values** beside dense axes may bump to `c58` if contrast fails WCAG on your display.
- **Tooltip**: Background `c2`, text `c58`, subtle `var(--shadow)`; pointer border `c46`.
- **Null / comparison series**: Desaturate toward `c49` or use dashed strokes in `c29` rather than inventing a seventh saturated hue.

---

## 7. Agent Prompt Guide

### Do's

- Map page canvas to **`c56` / `c1`** (`#0B150F`) and cards to **`c2`** (`#152A1E`) in both App Studio JSON and pro-code CSS
- Use **`c58` / `c59`** for all explicit text hierarchy; verify nav links after import
- Reserve **`c29` / `#7BC79F`** for primary actions, active tabs, and first-class data series
- Apply green-tinted **`--shadow`** stack; avoid pure black-only shadows—they read muddy on forest blacks
- Keep chart gridlines in **`c47`** at ~50% opacity; axis labels in **`c59`**
- Use **`f7` / `f8`** pairing for every KPI: heavy number, whisper label

### Don'ts

- Do not set font colors to **`c60`** anywhere in JSON or CSS wrappers
- Do not use pure **`#FFFFFF`** body text—use **`#E8F0EC`** (`c58`) for primary copy
- Do not place saturated mint fills behind mint data ink—maintain contrast against **`c2`**
- Do not borrow grayscale from an untinted corporate theme; neutrals must stay green-tinted (`c40`–`c54`)

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #0B150F     Card surface → c2   #152A1E
Hover        → c3        #1E3828     Nav bg       → c4   #071009
Nav active   → c5        #1E6B45     Nav hover    → c31  #146240
Header / input → c6 / c7 (deepest / card)
Accent       → c29       #7BC79F     Accent ↓     → c30  #5AAE80
Border       → c46       #2A4A36     Border light → c47  #1E3828
Primary text → c58       #E8F0EC     Secondary    → c59  #9AB3A4
Grayscale    → c40–c54 (green-tinted ramp); c46–c47 are structural borders
Never        → c60 AUTOMATIC_COLOR for fonts
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#7BC79F',
  primaryPressed: '#5AAE80',
  secondary: '#9AB3A4',
  surface: '#152A1E',
  bg: '#0B150F',
  text: '#E8F0EC',
  textMuted: '#9AB3A4',
  border: '#2A4A36',
  borderLight: '#1E3828',
  navBg: '#071009',
  navActive: '#1E6B45',
  navHover: '#146240',
  positive: '#59C886',
  negative: '#E45F5F',
  warning: '#FBAD56',
  series: ['#7BC79F', '#A8F4CA', '#A0D771', '#FBAD56', '#E45F5F', '#4D9A75']
};
```

### Example Agent Prompts

- **“Build a KPI row for BC Forest Dark”**: Cards on `c2`, shadow from section 2.3, values `f7` + `c58`, labels `f8` + `c59`, optional 4px left border `c29`. No `c60` font references.
- **“Match App Studio chart colors in Recharts”**: Use `COLORS.series` order; `CartesianGrid` stroke `c47` at 0.5 opacity; `XAxis`/`YAxis` tick fill `c59`; tooltip surface `c2`, text `c58`, border `c46`.
- **“Add a forest-themed CTA button”**: Default ghost on `c2` with border `c46` and text `c59`; hover `c3` and border `c29` with text `c58`; active fill `c29` with text `c1` (dark on mint).
- **“Audit theme import”**: Search JSON for `"index": 60` on font colors; replace with `58` or `59`. Confirm `c56` matches canvas and navigation uses `c59` default links.

### Pro-Code `:root` Reference (align with JSON slots)

```css
:root {
  --bg: #0B150F;
  --surface: #152A1E;
  --surface-hover: #1E3828;
  --nav-bg: #071009;
  --nav-active: #1E6B45;
  --nav-hover: #146240;
  --accent: #7BC79F;
  --accent-pressed: #5AAE80;
  --border: #2A4A36;
  --border-light: #1E3828;
  --text-primary: #E8F0EC;
  --text-secondary: #9AB3A4;
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
}
```

### Native vs Pro-Code Parity Checklist

1. Page background in App Studio layout matches **`c56`** and pro-code outer wrapper is transparent when embedded.
2. Any custom card chrome uses **`c2`** / **`c58`** before introducing new hex values.
3. Filter controls share **`c7`** input fill and **`c46`** focus ring via **`c29`**.
4. Chart tooltips mirror card surface (**`c2`**) so they feel attached to the forest deck, not floating white boxes.

---

## 8. App Studio Theme JSON (Importable)

Paste into App Studio → Theme Editor → Import. After import, spot-check left nav links, tab labels, and table headers for contrast.

```json
{
  "name": "BC Forest Dark",
  "colors": [
    { "index": 1, "value": "#0B150F", "tag": "PRIMARY" },
    { "index": 2, "value": "#152A1E", "tag": "PRIMARY" },
    { "index": 3, "value": "#1E3828", "tag": "PRIMARY" },
    { "index": 4, "value": "#071009", "tag": "PRIMARY" },
    { "index": 5, "value": "#1E6B45", "tag": "PRIMARY" },
    { "index": 6, "value": "#071009", "tag": "PRIMARY" },
    { "index": 7, "value": "#152A1E", "tag": "PRIMARY" },
    { "index": 8, "value": "#152A1E", "tag": "PRIMARY" },
    { "index": 9, "value": "#7BC79F", "tag": "SECONDARY" },
    { "index": 10, "value": "#071009", "tag": "PRIMARY" },
    { "index": 11, "value": "#101C16", "tag": "PRIMARY" },
    { "index": 12, "value": "#1E3828", "tag": "PRIMARY" },
    { "index": 29, "value": "#7BC79F", "tag": "SECONDARY" },
    { "index": 30, "value": "#5AAE80", "tag": "SECONDARY" },
    { "index": 31, "value": "#146240", "tag": "SECONDARY" },
    { "index": 40, "value": "#060D08", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0A140E", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#0D1A12", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#102016", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#35483D", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#506158", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#2A4A36", "tag": "CUSTOM" },
    { "index": 47, "value": "#1E3828", "tag": "CUSTOM" },
    { "index": 48, "value": "#6E7D75", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#89978F", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#A4B1AA", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#BAC4BF", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#CAD4CF", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#D9E2DE", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E8F0EC", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#0B150F", "tag": "PRIMARY" },
    { "index": 58, "value": "#E8F0EC", "tag": "FONT" },
    { "index": 59, "value": "#9AB3A4", "tag": "FONT" }
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
      "titleFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "linkFontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "activeLinkFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
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
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 1 },
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

> **Import note**: Native navigation hover may still approximate `c31`; if the editor does not expose hover slots, reinforce hover states in pro-code sidebars. **`c60`** must never appear on font color references.
