# Arctic Frost — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Ice blue / cool slate · **Mood**: Clinical calm, ultra high-key minimalism, medical-grade clarity

---

## 1. Visual Theme and Atmosphere

**Personality**: The shell whispers instead of shouts. Surfaces are nearly white with a faint cool cast; the only chromatic punctuation is a powdery ice-blue accent and a slate-blue secondary for data series. The experience should feel like a spotless lab or a premium health dashboard—precise, legible, and emotionally cool.

**Density**: Medium-high. Cards sit on a whisper-gray canvas with tight but breathable 16px gutters. Internal card padding stays at 20px so dense grids of KPIs and tables remain scannable without turning into a spreadsheet slab.

**Philosophy**: **Light navigation is non-negotiable**—the left rail is pale frost, not inverted charcoal. Depth comes from **very subtle shadows** tinted from primary text at low alpha, never from heavy outlines. Saturated color belongs in **charts and status**, not in chrome. If the nav reads as a dark band, the theme has been mis-applied.

**Atmosphere cues**:
- Canvas `#FAFBFC` and cards `#FFFFFF` stay in a **two-step high-key** relationship—avoid mid-gray page fills
- Hover states lift one step to `#F5F7F9`; nav items use `#DCE3EB` on hover between default frost and active pill
- Shadows are **cool-neutral**, sampled from `#2C3340` at ~4–8% opacity—never pure black stacks
- Body copy is **dark slate** (`#2C3340`), never pure black; secondary copy is desaturated blue-gray (`#7A8494`)

---

## 2. Color System

### 2.1 Semantic Palette

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|----------------|
| Page background (reference) | `#FAFBFC` | `oklch(0.988 0.002 247.8)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c2` | `--surface` |
| Surface hover | `#F5F7F9` | `oklch(0.975 0.003 247.9)` | `c3` | `--surface-hover` |
| Navigation background | `#E8EDF2` | `oklch(0.944 0.009 247.9)` | `c4` | `--nav-bg` |
| Navigation active | `#D0D8E2` | `oklch(0.879 0.016 253.9)` | `c5` | `--nav-active` |
| Header background | `#FAFBFC` | `oklch(0.988 0.002 247.8)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c7` | `--input-bg` |
| Tab default background | `#FFFFFF` | `oklch(1.000 0.000 89.9)` | `c8` | `--tab-bg` |
| Tab active background | `#A8C5E2` | `oklch(0.812 0.052 248.5)` | `c9` | `--tab-active-bg` |
| Table header background | `#F0F4F8` | `oklch(0.965 0.007 247.9)` | `c10` | `--table-header-bg` |
| Table row stripe | `#EEF2F6` | `oklch(0.959 0.007 247.9)` | `c11` | `--table-stripe` |
| Table row hover | `#E8EDF2` | `oklch(0.944 0.009 247.9)` | `c12` | `--table-row-hover` |
| Accent primary | `#A8C5E2` | `oklch(0.812 0.052 248.5)` | `c29` | `--accent` |
| Accent pressed | `#8BAFC8` | `oklch(0.736 0.053 238.8)` | `c30` | `--accent-pressed` |
| Secondary (slate blue) | `#6B8DAE` | `oklch(0.630 0.063 248.1)` | `c31` | `--accent-secondary` |
| Navigation hover | `#DCE3EB` | `oklch(0.913 0.013 251.6)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#101418` | `oklch(0.189 0.010 248.4)` | `c40` | `--gray-950` |
| Grayscale 2 | `#181C22` | `oklch(0.225 0.013 258.4)` | `c41` | `--gray-900` |
| Grayscale 3 | `#202830` | `oklch(0.273 0.019 248.5)` | `c42` | `--gray-850` |
| Grayscale 4 | `#2A323C` | `oklch(0.314 0.021 254.1)` | `c43` | `--gray-800` |
| Grayscale 5 | `#3A4450` | `oklch(0.382 0.024 253.1)` | `c44` | `--gray-750` |
| Grayscale 6 | `#4A5664` | `oklch(0.448 0.028 252.4)` | `c45` | `--gray-700` |
| Border | `#C8D0DA` | `oklch(0.854 0.016 253.9)` | `c46` | `--border` |
| Border light | `#E0E6EE` | `oklch(0.923 0.013 255.5)` | `c47` | `--border-light` |
| Input border | `#C8D0DA` | `oklch(0.854 0.016 253.9)` | `c48` | `--input-border` |
| Grayscale 7 | `#8E96A4` | `oklch(0.671 0.023 261.7)` | `c49` | `--gray-600` |
| Grayscale 8 | `#A0A8B4` | `oklch(0.729 0.020 258.4)` | `c50` | `--gray-500` |
| Grayscale 9 | `#B8C0CC` | `oklch(0.805 0.019 258.4)` | `c51` | `--gray-400` |
| Grayscale 10 | `#D0D6DE` | `oklch(0.874 0.013 255.5)` | `c52` | `--gray-300` |
| Grayscale 11 | `#E4E8EE` | `oklch(0.930 0.009 258.3)` | `c53` | `--gray-200` |
| Grayscale 12 | `#F2F4F7` | `oklch(0.966 0.005 258.3)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#FAFBFC` | `oklch(0.988 0.002 247.8)` | `c56` | `--bg` |
| Primary text (FONT) | `#2C3340` | `oklch(0.320 0.025 262.7)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#7A8494` | `oklch(0.611 0.027 259.8)` | `c59` | `--text-secondary` |

Light mode: **`c58`** is dark slate for body and titles; **`c59`** is cooler, dimmer blue-gray for captions, axis labels, and de-emphasized nav links on the **light** rail.

### 2.2 Status Colors

| Status | Primary | Primary OKLCH | Background | Background OKLCH | Text | Text OKLCH | CSS Variable |
|--------|---------|---------------|------------|------------------|------|------------|----------------|
| On track | `#5A9A8E` | `oklch(0.640 0.069 180.6)` | `#E4F2EF` | `oklch(0.950 0.015 181.8)` | `#2F5E54` | `oklch(0.445 0.054 178.1)` | `--status-on-track` |
| At risk | `#D9A020` | `oklch(0.741 0.145 81.4)` | `#FDF6E4` | `oklch(0.974 0.025 89.2)` | `#8A6508` | `oklch(0.531 0.107 82.7)` | `--status-at-risk` |
| Behind | `#5A7A9A` | `oklch(0.568 0.062 249.0)` | `#E8EEF4` | `oklch(0.946 0.010 247.9)` | `#2E4058` | `oklch(0.367 0.048 255.8)` | `--status-behind` |
| Complete | `#6B8DAE` | `oklch(0.630 0.063 248.1)` | `#E8F0F8` | `oklch(0.951 0.014 248.0)` | `#3A5580` | `oklch(0.448 0.078 259.4)` | `--status-complete` |

### 2.3 Shadows

Cool-tinted from **`#2C3340`** at low opacity—barely perceptible lift suitable for clinical UI.

```css
--shadow:
  0px 0px 0px 1px oklch(0.320 0.025 262.7 / 0.05),
  0px 1px 2px -1px oklch(0.320 0.025 262.7 / 0.05),
  0px 2px 6px 0px oklch(0.320 0.025 262.7 / 0.035);
--shadow-hover:
  0px 0px 0px 1px oklch(0.320 0.025 262.7 / 0.07),
  0px 2px 4px -1px oklch(0.320 0.025 262.7 / 0.06),
  0px 6px 16px 0px oklch(0.320 0.025 262.7 / 0.045);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio: **Sans** on **all** font slots (`f1`–`f8`). Keep chart axes and badges in the same family so the canvas reads as one instrument panel.

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | `text-wrap: balance` |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.5; `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill`; align with `c59` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `letter-spacing: 0.04em`; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Page titles, card titles, KPI values, badges, active control labels
- **Regular (400)**: Body, table cells, chart axes, form values
- **Light (300)**: KPI labels and micro time-range captions only
- Avoid **700/900**—they break the frosted, clinical quiet

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Border | Padding | Notes |
|-----------|------|------------|------------|--------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard (`--shadow`) | none | 20px | Accent `c29`; chart font `f5` |
| `ca2` | Filters / controls | `c2` | `c58` | 10px | Standard | none | 16px | Hover chips borrow `c3` |
| `ca3` | Narrative / policy | `c2` | `c58` | 10px | Soft | none | 20px | Long-form serif not used—stay Sans |
| `ca4` | Compact | `c2` | `c58` | 8px | Minimal | none | 12px | Dense pickers |
| `ca5` | KPI hero | `c2` | `c58` | 12px | Standard | optional 4px left status | 16px | Value `f7`, label `f8` |
| `ca6` | Muted tile | `c3` | `c58` | 8px | none | none | 12px | Sits on canvas like a frost patch |
| `ca7` | Callout | `c9` @ 22% wash on `c2` | `c58` | 10px | Standard | none | 16px | Ice-blue hint, not solid flood |
| `ca8` | Full-bleed strip | `c56` | `c58` | 0 | none | none | 12px | Page-level banner |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#E8EDF2` pale frost | `c4` |
| Active item background | `#D0D8E2` | `c5` |
| Hover background | `#DCE3EB` | `c32` |
| Title font color | `#2C3340` | `c58` |
| Default link color | `#7A8494` | `c59` |
| Active link color | `#2C3340` | `c58` |
| Active indicator / bar | `#A8C5E2` | `c29` |
| Title font | 22px SemiBold Sans | `f1` |
| Link font | 13px Regular Sans | `f3` |
| Signature | **Light rail**—never substitute a dark nav | — |

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#6B8DAE` | `oklch(0.630 0.063 248.1)` | Slate blue anchor |
| 2 | `#A8C5E2` | `oklch(0.812 0.052 248.5)` | Ice blue fill |
| 3 | `#8BAFC8` | `oklch(0.736 0.053 238.8)` | Pressed / secondary ice |
| 4 | `#B8C8D8` | `oklch(0.826 0.029 248.2)` | Muted steel |
| 5 | `#5A7A9A` | `oklch(0.568 0.062 249.0)` | Deep harbor |
| 6 | `#9AAFBF` | `oklch(0.743 0.033 240.8)` | Fog blue |

**Pro-code series array**: `['#6B8DAE', '#A8C5E2', '#8BAFC8', '#B8C8D8', '#5A7A9A', '#9AAFBF']`

**Chart chrome**: Grid `c47` at ~0.5 opacity; axis lines `c46`; ticks and legend `c59` via `f5`; tooltips `c2` surface with `--shadow`.

### 6.1 Semantic chart anchors

| Role | Hex | OKLCH | Mapping |
|------|-----|-------|---------|
| Positive / up | `#5A9A8E` | `oklch(0.640 0.069 180.6)` | Waterfall / variance “good” |
| Negative / down | `#C45A5A` | `oklch(0.599 0.136 22.0)` | Loss / unfavorable |
| Total / neutral | `#6B8DAE` | `oklch(0.630 0.063 248.1)` | Subtotal bars |
| Forecast | `#A8C5E2` | `oklch(0.812 0.052 248.5)` | Dashed projection |
| Today marker | `#D9A020` | `oklch(0.741 0.145 81.4)` | Vertical reference |
| Confidence band | `#A8C5E233` | `oklch(0.812 0.052 248.5 / 0.20)` | Area fill |

### 6.2 Interaction rules

- Inactive series opacity **0.35**; hovered series **1.0**
- Do not use chart colors for **nav** or **page chrome**—keep opposition between data ink and UI shell
- On export to PDF, preserve light backgrounds; do not force dark mode chart styles

---

## 7. Agent Prompt Guide

### Do's

- Keep **`c56`** and **`c1`** identical to **`#FAFBFC`** so page chrome and App Studio background stay aligned
- Use **`c4`–`c5`–`c32`** for the **light** navigation stack—verify visually that the rail is not inverted
- Bind cards to **`c2`** white and body text to **`c58`**; use **`c59`** for secondary copy and chart axes
- Tint every shadow stack from **`oklch(0.320 0.025 262.7 / …)`** (text-primary), not `#000`
- Reserve **`c31`** and the Section 6 palette for **data ink**; keep structural chrome in frosted neutrals

### Don'ts

- Do not apply **dark nav** treatments—this theme’s signature is a **light frost rail**
- Do not use **pure black** text or **pure black** shadows on the near-white canvas
- Do not saturate large fields with **`c29`**; use it for tabs, focus rings, and slender indicators
- Avoid **`c60`** for documented font color—prefer **`c58` / `c59`** for agent portability

### Slot Mapping Cheat Sheet

```
c1 / c56   → #FAFBFC   page background (reference + App Studio)
c2         → #FFFFFF   card / input fill
c3         → #F5F7F9   hover surfaces
c4         → #E8EDF2   nav background (LIGHT)
c5         → #D0D8E2   nav active
c6         → #FAFBFC   headers
c7         → #FFFFFF   inputs
c8–c12     → tabs + table chrome (frost tints)
c29 / c30  → #A8C5E2 / #8BAFC8   accent / pressed
c31        → #6B8DAE   secondary / series
c32        → #DCE3EB   nav hover
c40–c45    → blue-gray shadow + deep ramp
c46–c48    → borders + input border
c49–c54    → light blue-gray ramp
c58 / c59  → #2C3340 / #7A8494   FONT primary / secondary (light UI)
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#A8C5E2',
  primaryPressed: '#8BAFC8',
  secondary: '#6B8DAE',
  surface: '#FFFFFF',
  bg: '#FAFBFC',
  text: '#2C3340',
  textMuted: '#7A8494',
  border: '#C8D0DA',
  borderLight: '#E0E6EE',
  navBg: '#E8EDF2',
  navActive: '#D0D8E2',
  navHover: '#DCE3EB',
  series: ['#6B8DAE', '#A8C5E2', '#8BAFC8', '#B8C8D8', '#5A7A9A', '#9AAFBF']
};
```

### Example Agent Prompts

- **“Frosted clinical dashboard”**: Page `c56`, cards `c2`, `var(--shadow)` only—no 1px card outlines unless tabular.
- **“KPI row with calm hierarchy”**: Values `f7` + `c58`, labels `f8` + `c59`, optional 4px left rule in a Section 2.2 status color.
- **“Light navigation rail”**: Background `c4`, hover `c32`, active pill `c5`, indicator `c29`; links `c59` default and `c58` active.
- **“Ice-blue primary CTA”**: Fill `c29`, pressed `c30`, label `c58` (dark text on soft fill); focus ring `c30` at 2px offset.
- **“Bar chart on white card”**: `COLORS.series` order as Section 6; grid `c47` @ 0.5 opacity; axes `c59`.
- **“Table with frost header”**: Header `c10`, stripes `c11`, hover `c12`, borders `c47`, text `c58` / header labels `c59`.
- **“Status badge row”**: Light tints from Section 2.2 backgrounds; text uses matching darker column; font `f6`.

### Pro-Code `:root` token block

```css
:root {
  --bg: oklch(0.988 0.002 247.8);
  --surface: oklch(1 0 0);
  --surface-hover: oklch(0.975 0.003 247.9);
  --text-primary: oklch(0.320 0.025 262.7);
  --text-secondary: oklch(0.611 0.027 259.8);
  --border: oklch(0.854 0.016 253.9);
  --border-light: oklch(0.923 0.013 255.5);
  --accent: oklch(0.812 0.052 248.5);
  --accent-pressed: oklch(0.736 0.053 238.8);
  --nav-bg: oklch(0.944 0.009 247.9);
  --nav-active: oklch(0.879 0.016 253.9);
  --nav-hover: oklch(0.913 0.013 251.6);
}
```

### Import parity checklist

1. **`c56`** equals **`c1`** (`#FAFBFC`).
2. Navigation **`c4`** is **`#E8EDF2`** (verify light rail in preview).
3. Cards use **`dropShadow: true`** and **`borderRadius: 10`** for default analytics tiles.
4. No manual **`c60`** font bindings in JSON after import.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Arctic Frost",
  "colors": [
    { "index": 1, "value": "#FAFBFC", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#F5F7F9", "tag": "PRIMARY" },
    { "index": 4, "value": "#E8EDF2", "tag": "PRIMARY" },
    { "index": 5, "value": "#D0D8E2", "tag": "PRIMARY" },
    { "index": 6, "value": "#FAFBFC", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#A8C5E2", "tag": "SECONDARY" },
    { "index": 10, "value": "#F0F4F8", "tag": "PRIMARY" },
    { "index": 11, "value": "#EEF2F6", "tag": "PRIMARY" },
    { "index": 12, "value": "#E8EDF2", "tag": "PRIMARY" },
    { "index": 29, "value": "#A8C5E2", "tag": "SECONDARY" },
    { "index": 30, "value": "#8BAFC8", "tag": "SECONDARY" },
    { "index": 31, "value": "#6B8DAE", "tag": "SECONDARY" },
    { "index": 32, "value": "#DCE3EB", "tag": "SECONDARY" },
    { "index": 40, "value": "#101418", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#181C22", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#202830", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#2A323C", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#3A4450", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#4A5664", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#C8D0DA", "tag": "CUSTOM" },
    { "index": 47, "value": "#E0E6EE", "tag": "CUSTOM" },
    { "index": 48, "value": "#C8D0DA", "tag": "CUSTOM" },
    { "index": 49, "value": "#8E96A4", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#A0A8B4", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B8C0CC", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#D0D6DE", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E4E8EE", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F2F4F7", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#FAFBFC", "tag": "PRIMARY" },
    { "index": 58, "value": "#2C3340", "tag": "FONT" },
    { "index": 59, "value": "#7A8494", "tag": "FONT" }
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
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
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

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm the navigation background is **`#E8EDF2`** (light frost), not a dark purple or charcoal override.
