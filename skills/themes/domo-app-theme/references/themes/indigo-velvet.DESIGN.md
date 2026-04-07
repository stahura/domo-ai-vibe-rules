# Indigo Velvet — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Lavender / royal purple with gold opposition · **Mood**: Luxurious VIP analytics, velvet depth, after-hours boardroom

---

## 1. Visual Theme and Atmosphere

**Personality**: The canvas is a deep indigo vault (`#1A1335`); cards lift as eggplant panels (`#221B3A`). Lavender (`#8B7FD4`) is the jewel tone—used for emphasis, active states, and primary series—while antique gold (`#D4A85C`) provides warm counterpoint in charts and secondary highlights. Nothing reads as “default gray dark mode”; every neutral carries a **purple undertone**.

**Density**: Medium. Give cards 20px padding and 12px internal element spacing so dense KPI grids still feel like premium tiles, not terminal output. Avoid stacking more than three typographic weights on one card.

**Philosophy**: **Purple + gold opposition** carries the brand story: cool sovereignty (purple) versus warm reward (gold). Keep chrome desaturated relative to **data**—let series colors and KPI semantics carry saturation. Shadows are **soft violet halos** from light text at low alpha, never harsh white glows.

**Atmosphere cues**:
- Page and header backgrounds align to **`#1A1335`** so full-bleed layouts feel continuous
- Hover lifts surfaces to **`#2C2448`**—a readable step without jumping to mid-gray
- Primary copy is **pale lavender-white** (`#E8E2F0`); secondary is **muted lilac** (`#A89CC0`)
- Gold appears as **accents**, not fills for entire nav bars—reserve it for indicators, second series, and VIP callouts

---

## 2. Color System

### 2.1 Semantic Palette

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|----------------|
| Page background (reference) | `#1A1335` | `oklch(0.217 0.064 289.4)` | `c1` | `--bg-ref` |
| Card surface | `#221B3A` | `oklch(0.248 0.058 292.0)` | `c2` | `--surface` |
| Surface hover | `#2C2448` | `oklch(0.288 0.065 292.1)` | `c3` | `--surface-hover` |
| Navigation background | `#160F2E` | `oklch(0.198 0.060 290.3)` | `c4` | `--nav-bg` |
| Navigation active | `#3A2D5E` | `oklch(0.337 0.084 293.6)` | `c5` | `--nav-active` |
| Header background | `#1A1335` | `oklch(0.217 0.064 289.4)` | `c6` | `--header-bg` |
| Input background | `#221B3A` | `oklch(0.248 0.058 292.0)` | `c7` | `--input-bg` |
| Tab default background | `#221B3A` | `oklch(0.248 0.058 292.0)` | `c8` | `--tab-bg` |
| Tab active background | `#8B7FD4` | `oklch(0.643 0.125 288.8)` | `c9` | `--tab-active-bg` |
| Table header background | `#2C2448` | `oklch(0.288 0.065 292.1)` | `c10` | `--table-header-bg` |
| Table row stripe | `#261F40` | `oklch(0.265 0.060 291.5)` | `c11` | `--table-stripe` |
| Table row hover | `#2C2448` | `oklch(0.288 0.065 292.1)` | `c12` | `--table-row-hover` |
| Accent primary | `#8B7FD4` | `oklch(0.643 0.125 288.8)` | `c29` | `--accent` |
| Accent pressed | `#7A6EC0` | `oklch(0.585 0.123 288.7)` | `c30` | `--accent-pressed` |
| Secondary (gold) | `#D4A85C` | `oklch(0.756 0.108 79.6)` | `c31` | `--accent-gold` |
| Navigation hover | `#2D2454` | `oklch(0.298 0.084 288.9)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#0A0614` | `oklch(0.138 0.032 296.6)` | `c40` | `--gray-950` |
| Grayscale 2 | `#120E22` | `oklch(0.181 0.040 291.0)` | `c41` | `--gray-900` |
| Grayscale 3 | `#1A1630` | `oklch(0.220 0.050 288.7)` | `c42` | `--gray-850` |
| Grayscale 4 | `#221E3E` | `oklch(0.257 0.059 287.2)` | `c43` | `--gray-800` |
| Grayscale 5 | `#2E284E` | `oklch(0.303 0.067 289.0)` | `c44` | `--gray-750` |
| Grayscale 6 | `#3A345E` | `oklch(0.352 0.072 288.7)` | `c45` | `--gray-700` |
| Border | `#3A3260` | `oklch(0.349 0.078 289.7)` | `c46` | `--border` |
| Border light | `#2C2448` | `oklch(0.288 0.065 292.1)` | `c47` | `--border-light` |
| Input border | `#3A3260` | `oklch(0.349 0.078 289.7)` | `c48` | `--input-border` |
| Grayscale 7 | `#4A446E` | `oklch(0.412 0.069 289.5)` | `c49` | `--gray-600` |
| Grayscale 8 | `#6A6288` | `oklch(0.518 0.060 293.9)` | `c50` | `--gray-500` |
| Grayscale 9 | `#8A82A2` | `oklch(0.625 0.048 296.4)` | `c51` | `--gray-400` |
| Grayscale 10 | `#A8A0BC` | `oklch(0.722 0.041 298.4)` | `c52` | `--gray-300` |
| Grayscale 11 | `#C8C0D6` | `oklch(0.821 0.032 302.2)` | `c53` | `--gray-200` |
| Grayscale 12 | `#E0D8F0` | `oklch(0.896 0.034 300.9)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#1A1335` | `oklch(0.217 0.064 289.4)` | `c56` | `--bg` |
| Primary text (FONT) | `#E8E2F0` | `oklch(0.922 0.020 305.3)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#A89CC0` | `oklch(0.715 0.053 300.3)` | `c59` | `--text-secondary` |

Dark mode: **`c58`** is light lavender-white (`#E0+` range); **`c59`** is dimmer lilac for captions, axes, and de-emphasized chrome.

### 2.2 Status Colors

| Status | Primary | Primary OKLCH | Background | Background OKLCH | Text | Text OKLCH | CSS Variable |
|--------|---------|---------------|------------|------------------|------|------------|----------------|
| On track | `#6FD4A8` | `oklch(0.797 0.115 163.5)` | `#1E3A2E` | `oklch(0.322 0.041 164.7)` | `#6FD4A8` | `oklch(0.797 0.115 163.5)` | `--status-on-track` |
| At risk | `#F0B84D` | `oklch(0.815 0.138 80.7)` | `#3A3020` | `oklch(0.315 0.030 79.0)` | `#F0B84D` | `oklch(0.815 0.138 80.7)` | `--status-at-risk` |
| Behind | `#E07A9A` | `oklch(0.702 0.131 1.0)` | `#3A2030` | `oklch(0.284 0.047 342.9)` | `#E8C8D4` | `oklch(0.863 0.039 353.3)` | `--status-behind` |
| Complete | `#8B7FD4` | `oklch(0.643 0.125 288.8)` | `#2A2440` | `oklch(0.281 0.051 292.7)` | `#D4C8F8` | `oklch(0.858 0.067 296.4)` | `--status-complete` |

### 2.3 Shadows

Lift uses **light text** tint at low alpha so edges glow like velvet pile, not neon rim-lights.

```css
--shadow:
  0px 0px 0px 1px oklch(0.922 0.020 305.3 / 0.10),
  0px 1px 3px -1px oklch(0.922 0.020 305.3 / 0.08),
  0px 4px 14px 0px oklch(0.138 0.032 296.6 / 0.45);
--shadow-hover:
  0px 0px 0px 1px oklch(0.922 0.020 305.3 / 0.14),
  0px 3px 8px -1px oklch(0.922 0.020 305.3 / 0.12),
  0px 10px 28px 0px oklch(0.138 0.032 296.6 / 0.55);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio: **Sans** on **all** slots (`f1`–`f8`). Keep the voice modern-luxury; do not mix Serif into a single analytics canvas.

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance`; slight letter-spacing optional |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Tight leading vs body |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.5 |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill: c59` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges, emphasized controls
- **Regular (400)**: Body, axes, table data
- **Light (300)**: KPI labels only—recedes behind numbers
- Avoid **700+** on dark velvet; it reads harsh against `#221B3A`

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Border | Padding | Notes |
|-----------|------|------------|------------|--------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | none | 20px | Accent `c29`; optional gold `c31` KPI rule |
| `ca2` | Controls | `c2` | `c58` | 10px | Standard | none | 16px | Chips hover `c3` |
| `ca3` | VIP summary | `c2` | `c58` | 12px | Hover lift | none | 20px | Gold sparklines encouraged |
| `ca4` | Compact | `c2` | `c58` | 8px | Minimal | none | 12px | Dense filters |
| `ca5` | KPI | `c2` | `c58` | 12px | Standard | none | 16px | Value may use `c31` or `c29` |
| `ca6` | Muted tile | `c3` | `c58` | 8px | none | none | 12px | Secondary metrics |
| `ca7` | Callout | `c29` @ 18% on `c2` | `c58` | 10px | Standard | none | 16px | Lavender wash |
| `ca8` | Banner | `c56` | `c58` | 0 | none | none | 12px | Full-bleed indigo |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#160F2E` deepest purple | `c4` |
| Active item | `#3A2D5E` | `c5` |
| Hover | `#2D2454` | `c32` |
| Title font color | `#E8E2F0` | `c58` |
| Default link color | `#A89CC0` | `c59` |
| Active link color | `#E8E2F0` | `c58` |
| Active indicator | `#8B7FD4` | `c29` |
| Secondary sparkle (optional) | `#D4A85C` | `c31` |
| Title font | 22px SemiBold Sans | `f1` |
| Link font | 13px Regular Sans | `f3` |
| Signature | **Deepest rail** + lavender active state—VIP lounge, not terminal |

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#8B7FD4` | `oklch(0.643 0.125 288.8)` | Lavender primary |
| 2 | `#D4A85C` | `oklch(0.756 0.108 79.6)` | Gold opposition |
| 3 | `#A896E0` | `oklch(0.717 0.107 294.7)` | Soft iris |
| 4 | `#C4956A` | `oklch(0.704 0.081 63.4)` | Warm bronze |
| 5 | `#6B5FA8` | `oklch(0.530 0.112 289.5)` | Royal shadow |
| 6 | `#E0C07A` | `oklch(0.820 0.096 85.8)` | Champagne highlight |

**Pro-code series array**: `['#8B7FD4', '#D4A85C', '#A896E0', '#C4956A', '#6B5FA8', '#E0C07A']`

**Chart chrome**: Grid `c47` @ 0.45 opacity; axis `c46`; ticks `c59`; tooltip `c2` with `--shadow`; legend `c59`.

### 6.1 Semantic chart anchors

| Role | Hex | OKLCH | Notes |
|------|-----|-------|---------|
| Positive | `#6FD4A8` | `oklch(0.797 0.115 163.5)` | Uptrend / favorable |
| Negative | `#E07A9A` | `oklch(0.702 0.131 1.0)` | Downtrend |
| Total | `#A89CC0` | `oklch(0.715 0.053 300.3)` | Neutral stack |
| Forecast | `#8B7FD4` | `oklch(0.643 0.125 288.8)` | Dashed lavender |
| Gold highlight | `#D4A85C` | `oklch(0.756 0.108 79.6)` | Target / VIP |

### 6.2 Interaction rules

- Default inactive series at **0.35** opacity on dark cards
- Prefer **gold** for “reward” semantics only—do not paint entire chart frames gold
- Export: keep `#1A1335` page behind charts for consistent luxury framing

---

## 7. Agent Prompt Guide

### Do's

- Align **`c1`**, **`c6`**, and **`c56`** to **`#1A1335`** for continuous vault background
- Use **`c58` / `c59`** on all dark surfaces; never place **`c58`** on **`c29`** fills without contrast check
- Pair **`c29`** with **`c31`** in prompts when you need **primary + reward** duality
- Keep cards on **`c2`** with **`dropShadow: true`** for the velvet lift
- Use **`c1`** (canvas) as **active tab text** on **`c9`** lavender fills in JSON for legibility

### Don'ts

- Do not flatten everything to neutral gray—preserve **purple chroma** in borders and stripes
- Do not use **pure white** (`#FFFFFF`) as page background; it breaks the vault mood
- Avoid **`c60`** for documented typography—bind to **`c58` / `c59`**
- Do not remove **`c31`** from the palette—gold opposition is a signature

### Slot Mapping Cheat Sheet

```
c1 / c56   → #1A1335   page + header ground
c2         → #221B3A   cards / inputs
c3         → #2C2448   hover
c4         → #160F2E   nav (deepest)
c5         → #3A2D5E   nav active
c6         → #1A1335   headers
c7         → #221B3A   input fill
c8–c12     → tabs + tables (eggplant steps)
c29 / c30  → #8B7FD4 / #7A6EC0   accent / pressed
c31        → #D4A85C   gold secondary
c32        → #2D2454   nav hover
c40–c45    → dark purple ramp
c46–c48    → borders / input border
c49–c54    → light lilac ramp (for overlays / disabled)
c58 / c59  → #E8E2F0 / #A89CC0   FONT on dark UI
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#8B7FD4',
  primaryPressed: '#7A6EC0',
  secondary: '#D4A85C',
  surface: '#221B3A',
  bg: '#1A1335',
  text: '#E8E2F0',
  textMuted: '#A89CC0',
  border: '#3A3260',
  borderLight: '#2C2448',
  navBg: '#160F2E',
  navActive: '#3A2D5E',
  navHover: '#2D2454',
  series: ['#8B7FD4', '#D4A85C', '#A896E0', '#C4956A', '#6B5FA8', '#E0C07A']
};
```

### Example Agent Prompts

- **“VIP revenue dashboard”**: Canvas `c56`, cards `c2`, lavender CTAs `c29`, gold sparkline `c31`.
- **“Dark nav with lilac active”**: Rail `c4`, active `c5`, indicator `c29`, links `c59` default and `c58` active.
- **“KPI deck with gold accents”**: Numbers `f7` in `c58`; optional gold `c31` for positive delta glyphs only.
- **“Lavender primary button”**: Fill `c29`, pressed `c30`, label `c1` (dark text on bright fill) or `c58` if contrast passes—verify in preview.
- **“Combo chart purple + gold”**: Line `c29`, bar `c31`, grid `c47` subdued.

### Pro-Code `:root` token block

```css
:root {
  --bg: oklch(0.217 0.064 289.4);
  --surface: oklch(0.248 0.058 292);
  --surface-hover: oklch(0.288 0.065 292.1);
  --text-primary: oklch(0.922 0.020 305.3);
  --text-secondary: oklch(0.715 0.053 300.3);
  --border: oklch(0.349 0.078 289.7);
  --border-light: oklch(0.288 0.065 292.1);
  --accent: oklch(0.643 0.125 288.8);
  --accent-pressed: oklch(0.585 0.123 288.7);
  --gold: oklch(0.756 0.108 79.6);
}
```

### Import parity checklist

1. **`c56`** matches **`c1`** (`#1A1335`).
2. **`c58` / `c59`** imported as **FONT** tags.
3. Tab **`activeFontColor`** references **`c1`** for text on **`c9`** lavender.
4. Cards keep **radius 10** and **shadow** for default analytics layout.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Indigo Velvet",
  "colors": [
    { "index": 1, "value": "#1A1335", "tag": "PRIMARY" },
    { "index": 2, "value": "#221B3A", "tag": "PRIMARY" },
    { "index": 3, "value": "#2C2448", "tag": "PRIMARY" },
    { "index": 4, "value": "#160F2E", "tag": "PRIMARY" },
    { "index": 5, "value": "#3A2D5E", "tag": "PRIMARY" },
    { "index": 6, "value": "#1A1335", "tag": "PRIMARY" },
    { "index": 7, "value": "#221B3A", "tag": "PRIMARY" },
    { "index": 8, "value": "#221B3A", "tag": "PRIMARY" },
    { "index": 9, "value": "#8B7FD4", "tag": "SECONDARY" },
    { "index": 10, "value": "#2C2448", "tag": "PRIMARY" },
    { "index": 11, "value": "#261F40", "tag": "PRIMARY" },
    { "index": 12, "value": "#2C2448", "tag": "PRIMARY" },
    { "index": 29, "value": "#8B7FD4", "tag": "SECONDARY" },
    { "index": 30, "value": "#7A6EC0", "tag": "SECONDARY" },
    { "index": 31, "value": "#D4A85C", "tag": "SECONDARY" },
    { "index": 32, "value": "#2D2454", "tag": "SECONDARY" },
    { "index": 40, "value": "#0A0614", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#120E22", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#1A1630", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#221E3E", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#2E284E", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#3A345E", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#3A3260", "tag": "CUSTOM" },
    { "index": 47, "value": "#2C2448", "tag": "CUSTOM" },
    { "index": 48, "value": "#3A3260", "tag": "CUSTOM" },
    { "index": 49, "value": "#4A446E", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#6A6288", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#8A82A2", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#A8A0BC", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#C8C0D6", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E0D8F0", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#1A1335", "tag": "PRIMARY" },
    { "index": 58, "value": "#E8E2F0", "tag": "FONT" },
    { "index": 59, "value": "#A89CC0", "tag": "FONT" }
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
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 1 },
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

> **Import**: App Studio → Theme Editor → Import Theme JSON. Preview nav at **`#160F2E`** and confirm lavender **`c29`** reads as the jewel accent, not default blue.
