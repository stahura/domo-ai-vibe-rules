# Electric Teal — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Electric teal / coral contrast · **Mood**: Dev-tool precision, terminal calm, flat planes with grid discipline

---

## 1. Visual Theme and Atmosphere

**Personality**: The shell feels like a focused IDE: a **dark teal-gray void** (`#0D1F1E`) hosts slightly lifted panels (`#152A28`). **Electric teal** (`#00D4AA`) is the primary signal—hyper-legible on dark—and **coral** (`#FF6B6B`) provides warm error/alert opposition. Nothing relies on soft puff shadows; **structure is drawn with lines**.

**Density**: Medium-high. Monospace numerals align in tight columns; use **12–16px** internal spacing so glyphs do not collide. Prefer **tabular figures** everywhere counts appear.

**Philosophy**: **Flat cards**—**zero border-radius**, **no drop shadows**, **1px borders** in `c46` create a **grid of panes** like panes in a tiling window manager. Depth is implied by **contrast and hue**, not elevation. This theme is for builders who distrust “marketing gradients.”

**Atmosphere cues**:
- Page, header, and nav share the **near-black teal** family—continuous terminal canvas
- Hover states step to **`#1E3835`**—a readable delta without glow
- Text is **pale teal-white** (`#E0F0EE`); secondary is **muted sea-glass** (`#8AABA8`)
- Coral is for **danger, diff-down, alert**—never for primary chrome fills

---

## 2. Color System

### 2.1 Semantic Palette

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|----------------|
| Page background (reference) | `#0D1F1E` | `oklch(0.223 0.024 191.0)` | `c1` | `--bg-ref` |
| Card surface | `#152A28` | `oklch(0.267 0.027 187.9)` | `c2` | `--surface` |
| Surface hover | `#1E3835` | `oklch(0.319 0.033 186.3)` | `c3` | `--surface-hover` |
| Navigation background | `#0A1A19` | `oklch(0.203 0.022 190.4)` | `c4` | `--nav-bg` |
| Navigation active | `#1A3230` | `oklch(0.297 0.030 188.8)` | `c5` | `--nav-active` |
| Header background | `#0D1F1E` | `oklch(0.223 0.024 191.0)` | `c6` | `--header-bg` |
| Input background | `#152A28` | `oklch(0.267 0.027 187.9)` | `c7` | `--input-bg` |
| Tab default background | `#152A28` | `oklch(0.267 0.027 187.9)` | `c8` | `--tab-bg` |
| Tab active background | `#00D4AA` | `oklch(0.775 0.151 171.7)` | `c9` | `--tab-active-bg` |
| Table header background | `#182E2C` | `oklch(0.282 0.028 188.3)` | `c10` | `--table-header-bg` |
| Table row stripe | `#132624` | `oklch(0.252 0.025 187.1)` | `c11` | `--table-stripe` |
| Table row hover | `#1E3835` | `oklch(0.319 0.033 186.3)` | `c12` | `--table-row-hover` |
| Accent primary | `#00D4AA` | `oklch(0.775 0.151 171.7)` | `c29` | `--accent` |
| Accent pressed | `#00B894` | `oklch(0.697 0.135 172.1)` | `c30` | `--accent-pressed` |
| Secondary (coral) | `#FF6B6B` | `oklch(0.712 0.181 22.8)` | `c31` | `--accent-coral` |
| Navigation hover | `#142825` | `oklch(0.259 0.027 183.6)` | `c32` | `--nav-hover` |
| Grayscale 1 | `#030807` | `oklch(0.126 0.012 183.1)` | `c40` | `--gray-950` |
| Grayscale 2 | `#081210` | `oklch(0.171 0.016 180.6)` | `c41` | `--gray-900` |
| Grayscale 3 | `#0C1816` | `oklch(0.197 0.018 182.8)` | `c42` | `--gray-850` |
| Grayscale 4 | `#101E1C` | `oklch(0.221 0.020 184.6)` | `c43` | `--gray-800` |
| Grayscale 5 | `#142420` | `oklch(0.245 0.023 176.8)` | `c44` | `--gray-750` |
| Grayscale 6 | `#182A28` | `oklch(0.269 0.024 187.0)` | `c45` | `--gray-700` |
| Border | `#2A4A46` | `oklch(0.383 0.039 185.6)` | `c46` | `--border` |
| Border light | `#1E3835` | `oklch(0.319 0.033 186.3)` | `c47` | `--border-light` |
| Input border | `#2A4A46` | `oklch(0.383 0.039 185.6)` | `c48` | `--input-border` |
| Grayscale 7 | `#4A6A66` | `oklch(0.498 0.038 186.4)` | `c49` | `--gray-600` |
| Grayscale 8 | `#6A8A86` | `oklch(0.608 0.037 186.8)` | `c50` | `--gray-500` |
| Grayscale 9 | `#8AAAA6` | `oklch(0.713 0.036 187.1)` | `c51` | `--gray-400` |
| Grayscale 10 | `#A4C4C0` | `oklch(0.796 0.035 187.2)` | `c52` | `--gray-300` |
| Grayscale 11 | `#BCD8D4` | `oklch(0.860 0.030 186.2)` | `c53` | `--gray-200` |
| Grayscale 12 | `#D4ECE8` | `oklch(0.924 0.026 184.7)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#0D1F1E` | `oklch(0.223 0.024 191.0)` | `c56` | `--bg` |
| Primary text (FONT) | `#E0F0EE` | `oklch(0.943 0.017 187.9)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#8AABA8` | `oklch(0.716 0.036 189.6)` | `c59` | `--text-secondary` |

Dark mode: **`c58`** is pale teal-white; **`c59`** is dimmer sea-glass for axes, captions, and de-emphasized UI.

### 2.2 Status Colors

| Status | Primary | Primary OKLCH | Background | Background OKLCH | Text | Text OKLCH | CSS Variable |
|--------|---------|---------------|------------|------------------|------|------------|----------------|
| On track | `#00D4AA` | `oklch(0.775 0.151 171.7)` | `#0A2A24` | `oklch(0.259 0.039 178.5)` | `#00D4AA` | `oklch(0.775 0.151 171.7)` | `--status-on-track` |
| At risk / alert | `#FF6B6B` | `oklch(0.712 0.181 22.8)` | `#3A2020` | `oklch(0.278 0.041 20.0)` | `#FFB0B0` | `oklch(0.833 0.093 19.2)` | `--status-at-risk` |
| Behind / warn | `#FFB347` | `oklch(0.821 0.149 72.1)` | `#3A3018` | `oklch(0.314 0.041 87.4)` | `#FFD494` | `oklch(0.893 0.094 77.0)` | `--status-behind` |
| Complete / info | `#4DE8C8` | `oklch(0.842 0.137 176.1)` | `#0F2A26` | `oklch(0.262 0.034 182.7)` | `#4DE8C8` | `oklch(0.842 0.137 176.1)` | `--status-complete` |

### 2.3 Shadows

**Flat system**—default cards and panels use **borders**, not elevation. Optional: a **1px ring** only for focus-visible outlines.

```css
--shadow: none;
--shadow-hover: none;
--focus-ring: 0 0 0 2px oklch(0.775 0.151 171.7 / 0.45);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: "SF Mono", "Fira Code", "Cascadia Code", ui-monospace, monospace;
```

App Studio: **Monospace** on **all** slots (`f1`–`f8`). This is a **full-stack mono** dashboard—do not hybridize with Sans for “readability.”

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Tight leading |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.45 |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.08em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill: c59` |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase |
| KPI numbers | 28px | SemiBold | 600 | `f7` | **tabular-nums** mandatory |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges
- **Regular (400)**: Body, axes, data cells
- **Light (300)**: KPI labels only
- Mono benefits from **fewer weights**—do not add extraneous Bold 700

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Border | Padding | Notes |
|-----------|------|------------|------------|--------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | **0px** | **none** | **1px `c46`** | 20px | **Flat pane**; accent `c29` for spark |
| `ca2` | Controls | `c2` | `c58` | **0px** | **none** | **1px `c46`** | 16px | Grid-aligned filters |
| `ca3` | Log / trace | `c2` | `c58` | **0px** | **none** | **1px `c46`** | 12px | Dense mono logs |
| `ca4` | Compact | `c2` | `c58` | **0px** | **none** | **1px `c46`** | 12px | Pickers |
| `ca5` | KPI | `c2` | `c58` | **0px** | **none** | **1px `c46`** | 16px | Optional coral `c31` left rule for alert |
| `ca6` | Muted | `c3` | `c58` | **0px** | **none** | **1px `c47`** | 12px | Secondary metrics |
| `ca7` | Callout | `c2` | `c58` | **0px** | **none** | **2px `c29`** | 16px | Teal double-line emphasis |
| `ca8` | Banner | `c56` | `c58` | **0** | **none** | **bottom 1px `c46`** | 12px | Full-bleed strip |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#0A1A19` | `c4` |
| Active | `#1A3230` | `c5` |
| Hover | `#142825` | `c32` |
| Title font color | `#E0F0EE` | `c58` |
| Link font color | `#8AABA8` | `c59` |
| Active link color | `#E0F0EE` | `c58` |
| Active indicator | `#00D4AA` | `c29` |
| Title font | 22px SemiBold **Monospace** | `f1` |
| Link font | 13px Regular **Monospace** | `f3` |
| Signature | **Near-black teal rail** + **electric teal** focus—IDE, not consumer app |

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#00D4AA` | `oklch(0.775 0.151 171.7)` | Electric teal |
| 2 | `#FF6B6B` | `oklch(0.712 0.181 22.8)` | Coral contrast |
| 3 | `#4DE8C8` | `oklch(0.842 0.137 176.1)` | Mint highlight |
| 4 | `#FF8E8E` | `oklch(0.769 0.137 20.7)` | Soft coral |
| 5 | `#00B894` | `oklch(0.697 0.135 172.1)` | Pressed teal |
| 6 | `#E05555` | `oklch(0.634 0.174 23.5)` | Deep alert |

**Pro-code series array**: `['#00D4AA', '#FF6B6B', '#4DE8C8', '#FF8E8E', '#00B894', '#E05555']`

**Chart chrome**: Grid **`c46`** at **full opacity** (grid-line aesthetic); axis **`c46`**; ticks **`c59`**; tooltips **`c2`** border **`c46`**, **no shadow**.

### 6.1 Semantic chart anchors

| Role | Hex | OKLCH | Notes |
|------|-----|-------|---------|
| Positive | `#00D4AA` | `oklch(0.775 0.151 171.7)` | Uptrend |
| Negative | `#FF6B6B` | `oklch(0.712 0.181 22.8)` | Downtrend / error |
| Neutral | `#8AABA8` | `oklch(0.716 0.036 189.6)` | Baseline |
| Forecast | `#4DE8C8` | `oklch(0.842 0.137 176.1)` | Dashed projection |

### 6.2 Interaction rules

- Inactive series **0.3** opacity; active **1.0**
- Prefer **1px** Cartesian grid strokes—this theme celebrates lines
- Avoid **rounded chart containers**—match **0px** card radius in pro-code wrappers

---

## 7. Agent Prompt Guide

### Do's

- Set **`borderRadius: 0`**, **`dropShadow: false`**, **`borderWidth: 1`** on default cards in JSON
- Use **`c46`** for **grid lines** and **card outlines** consistently
- Keep **Monospace** on **all eight** font slots
- Use **`c1` / `c56`** for continuous **canvas** behind flat panes
- Put **alerts** on **`c31`** coral, not on **`c29`** unless intentionally unified

### Don'ts

- Do not add **soft shadows** “for polish”—that violates the flat signature
- Do not round cards to **8–12px** without explicit user override
- Avoid **Sans** or **Serif** intrusions into the mono stack
- Do not use **`c60`** in documented font mappings

### Slot Mapping Cheat Sheet

```
c1 / c56   → #0D1F1E   canvas
c2         → #152A28   card / input fill
c3         → #1E3835   hover
c4         → #0A1A19   nav
c5         → #1A3230   nav active
c6         → #0D1F1E   headers
c7         → #152A28   inputs
c8–c12     → tabs + tables (teal steps)
c29 / c30  → #00D4AA / #00B894   teal / pressed
c31        → #FF6B6B   coral secondary
c32        → #142825   nav hover
c40–c45    → near-black teal ramp
c46–c48    → #2A4A46 / #1E3835 / #2A4A46   borders + input border
c49–c54    → light teal ramp (overlays)
c58 / c59  → #E0F0EE / #8AABA8   FONT on dark UI
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#00D4AA',
  primaryPressed: '#00B894',
  secondary: '#FF6B6B',
  surface: '#152A28',
  bg: '#0D1F1E',
  text: '#E0F0EE',
  textMuted: '#8AABA8',
  border: '#2A4A46',
  borderLight: '#1E3835',
  navBg: '#0A1A19',
  navActive: '#1A3230',
  navHover: '#142825',
  series: ['#00D4AA', '#FF6B6B', '#4DE8C8', '#FF8E8E', '#00B894', '#E05555']
};
```

### Example Agent Prompts

- **“Flat IDE dashboard”**: Page `c56`, cards `c2`, `border: 1px solid #2A4A46`, `border-radius: 0`, `box-shadow: none`.
- **“Mono KPI row”**: `f7`/`f8` **Monospace**; values `c58`; negative delta glyph `c31`.
- **“Teal primary button”**: Fill `c29`, pressed `c30`, label `c1` (dark on bright fill); `outline: var(--focus-ring)`.
- **“Diff chart teal vs coral”**: Bars `c29` up / `c31` down; grid `c46` 1px.
- **“Table with grid lines”**: Row borders `c46`, header `c10`, hover `c12`.

### Pro-Code `:root` token block

```css
:root {
  --bg: oklch(0.223 0.024 191);
  --surface: oklch(0.267 0.027 187.9);
  --surface-hover: oklch(0.319 0.033 186.3);
  --text-primary: oklch(0.943 0.017 187.9);
  --text-secondary: oklch(0.716 0.036 189.6);
  --border: oklch(0.383 0.039 185.6);
  --border-light: oklch(0.319 0.033 186.3);
  --accent: oklch(0.775 0.151 171.7);
  --accent-pressed: oklch(0.697 0.135 172.1);
  --coral: oklch(0.712 0.181 22.8);
  --radius-card: 0px;
  --shadow: none;
  --font-stack: "SF Mono", "Fira Code", "Cascadia Code", ui-monospace, monospace;
}
```

### Import parity checklist

1. **Cards**: `borderRadius` **0**, `dropShadow` **false**, `borderWidth` **1** (set card border color via theme overrides or pro-code if native JSON lacks stroke color).
2. **All fonts**: `"family": "Monospace"`.
3. **`c56`** equals **`c1`**.
4. **Tabs**: `activeFontColor` → **`c1`** on **`c9`** teal fill.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Electric Teal",
  "colors": [
    { "index": 1, "value": "#0D1F1E", "tag": "PRIMARY" },
    { "index": 2, "value": "#152A28", "tag": "PRIMARY" },
    { "index": 3, "value": "#1E3835", "tag": "PRIMARY" },
    { "index": 4, "value": "#0A1A19", "tag": "PRIMARY" },
    { "index": 5, "value": "#1A3230", "tag": "PRIMARY" },
    { "index": 6, "value": "#0D1F1E", "tag": "PRIMARY" },
    { "index": 7, "value": "#152A28", "tag": "PRIMARY" },
    { "index": 8, "value": "#152A28", "tag": "PRIMARY" },
    { "index": 9, "value": "#00D4AA", "tag": "SECONDARY" },
    { "index": 10, "value": "#182E2C", "tag": "PRIMARY" },
    { "index": 11, "value": "#132624", "tag": "PRIMARY" },
    { "index": 12, "value": "#1E3835", "tag": "PRIMARY" },
    { "index": 29, "value": "#00D4AA", "tag": "SECONDARY" },
    { "index": 30, "value": "#00B894", "tag": "SECONDARY" },
    { "index": 31, "value": "#FF6B6B", "tag": "SECONDARY" },
    { "index": 32, "value": "#142825", "tag": "SECONDARY" },
    { "index": 40, "value": "#030807", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#081210", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#0C1816", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#101E1C", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#142420", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#182A28", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#2A4A46", "tag": "CUSTOM" },
    { "index": 47, "value": "#1E3835", "tag": "CUSTOM" },
    { "index": 48, "value": "#2A4A46", "tag": "CUSTOM" },
    { "index": 49, "value": "#4A6A66", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#6A8A86", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#8AAAA6", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#A4C4C0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#BCD8D4", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#D4ECE8", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#0D1F1E", "tag": "PRIMARY" },
    { "index": 58, "value": "#E0F0EE", "tag": "FONT" },
    { "index": 59, "value": "#8AABA8", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Monospace", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Monospace", "weight": "SemiBold", "size": "16px", "style": "normal" },
    { "index": 3, "family": "Monospace", "weight": "Regular", "size": "13px", "style": "normal" },
    { "index": 4, "family": "Monospace", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 5, "family": "Monospace", "weight": "Regular", "size": "11px", "style": "normal" },
    { "index": 6, "family": "Monospace", "weight": "SemiBold", "size": "11px", "style": "normal" },
    { "index": 7, "family": "Monospace", "weight": "SemiBold", "size": "28px", "style": "normal" },
    { "index": 8, "family": "Monospace", "weight": "Light", "size": "11px", "style": "normal" }
  ],
  "cards": [
    {
      "index": 1,
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "titleFont": { "type": "FONT_REFERENCE", "index": 2 },
      "chartFont": { "type": "FONT_REFERENCE", "index": 5 },
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "borderRadius": 0,
      "borderWidth": 1,
      "dropShadow": false,
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
      "borderRadius": 0,
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
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
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
      "borderRadius": 0,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **Import**: App Studio → Theme Editor → Import Theme JSON. Visually confirm **square corners** and **no card shadows**. If native cards ignore `borderWidth` stroke color, enforce **`outline: 1px solid var(--border)`** in pro-code wrappers.
