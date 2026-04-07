# Slate Granite — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Achromatic charcoal with mint teal signal · **Mood**: Technical clarity, infrastructure calm, understated precision

---

## 1. Visual Theme and Atmosphere

**Personality**: A **true neutral** light shell for engineering and general-purpose analytics. Surfaces are **white** on **`#F5F5F5`** canvas; graphite navigation grounds the UI. The signature move is **chromatic discipline**: everything structural is **achromatic** except **one mint teal** (`#5BBFB5`) that signals “selected / live / important” without rainbow chrome.

**Density**: Medium-high. Neutral rails tolerate information-dense layouts; keep **16px** gutters, **20px** card padding, and **tabular numerals** on KPIs so columns align cleanly in incident and capacity dashboards.

**Philosophy**: **Sans only** (`f1`–`f8`). Hierarchy comes from **weight and spacing**, not serif contrast. **`c29` / `c30`** read as **charcoal UI ink**—not a saturated brand hue—while **`c31`** teal is the **only** accent chroma in the shell. If a second hue appears in navigation, the theme has drifted.

**Atmosphere cues**:
- **Zero color temperature** in grayscale ramp—no sneaky blue-gray “because it’s tech”
- Hover on white is **`#EBEBEB`**, a neutral lift—not tinted mint
- **Graphite nav** uses **white** (`c2`) type; never **`c58`** on **`c4`**
- Shadows are **neutral gray** stacks derived from **`c58`**, not ink black
- Teal appears as **indicators, focus rings, active tabs, and chart series lead**—not as full-page gradients
- Photography and icons should be **desaturated** or monochrome so **`c31`** remains the dominant chroma signal

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#F5F5F5` | `oklch(0.970 0.000 89.9)` | `c1` | `--bg-ref` |
| Card surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c2` | `--surface` |
| Surface hover | `#EBEBEB` | `oklch(0.940 0.000 89.9)` | `c3` | `--surface-hover` |
| Navigation background | `#2C2F31` | `oklch(0.303 0.006 236.7)` | `c4` | `--nav-bg` |
| Navigation active | `#3E4244` | `oklch(0.376 0.006 229.0)` | `c5` | `--nav-active` |
| Navigation hover | `#353839` | `oklch(0.338 0.004 219.6)` | `c32` | `--nav-hover` |
| Header background | `#EBEBEB` | `oklch(0.940 0.000 89.9)` | `c6` | `--header-bg` |
| Input background | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c7` | `--input-bg` |
| Tab default surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab active fill | `#5BBFB5` | `oklch(0.742 0.095 186.6)` | `c9` | `--tab-active-bg` |
| Table header background | `#E8E8E8` | `oklch(0.931 0.000 89.9)` | `c10` | `--table-header-bg` |
| Table row stripe | `#FAFAFA` | `oklch(0.985 0.000 89.9)` | `c11` | `--table-stripe` |
| Table row hover | `#EBEBEB` | `oklch(0.940 0.000 89.9)` | `c12` | `--table-row-hover` |
| Accent (charcoal UI) | `#3C3F41` | `oklch(0.366 0.005 236.6)` | `c29` | `--accent` |
| Accent pressed | `#2C2F31` | `oklch(0.303 0.006 236.7)` | `c30` | `--accent-pressed` |
| Secondary (mint teal) | `#5BBFB5` | `oklch(0.742 0.095 186.6)` | `c31` | `--accent-signal` |
| Border | `#C0C0C0` | `oklch(0.808 0.000 89.9)` | `c46` | `--border` |
| Border light | `#D8D8D8` | `oklch(0.882 0.000 89.9)` | `c47` | `--border-light` |
| Input border | `#C0C0C0` | `oklch(0.808 0.000 89.9)` | `c46` | `--input-border` |
| Grayscale 1 (near black) | `#0A0A0A` | `oklch(0.145 0.000 89.9)` | `c40` | `--gray-950` |
| Grayscale 2 | `#191919` | `oklch(0.213 0.000 89.9)` | `c41` | `--gray-900` |
| Grayscale 3 | `#292929` | `oklch(0.281 0.000 89.9)` | `c42` | `--gray-850` |
| Grayscale 4 | `#3B3B3B` | `oklch(0.352 0.000 89.9)` | `c43` | `--gray-800` |
| Grayscale 5 | `#4D4D4D` | `oklch(0.420 0.000 89.9)` | `c44` | `--gray-750` |
| Grayscale 6 | `#606060` | `oklch(0.489 0.000 89.9)` | `c45` | `--gray-700` |
| Grayscale 7 | `#747474` | `oklch(0.559 0.000 89.9)` | `c48` | `--gray-600` |
| Grayscale 8 | `#888888` | `oklch(0.627 0.000 89.9)` | `c49` | `--gray-500` |
| Grayscale 9 | `#9D9D9D` | `oklch(0.696 0.000 89.9)` | `c50` | `--gray-400` |
| Grayscale 10 | `#B2B2B2` | `oklch(0.764 0.000 89.9)` | `c51` | `--gray-300` |
| Grayscale 11 | `#C8C8C8` | `oklch(0.833 0.000 89.9)` | `c52` | `--gray-200` |
| Grayscale 12 | `#DEDEDE` | `oklch(0.901 0.000 89.9)` | `c53` | `--gray-150` |
| Grayscale 13 (near white) | `#F5F5F5` | `oklch(0.970 0.000 89.9)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#F5F5F5` | `oklch(0.970 0.000 89.9)` | `c56` | `--bg` |
| Primary text (FONT) | `#2A2A2A` | `oklch(0.285 0.000 89.9)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#6A6A6A` | `oklch(0.524 0.000 89.9)` | `c59` | `--text-secondary` |
| Automatic (App Studio) | — | — | `c60` | `AUTOMATIC_COLOR` |

**Slot notes**: `c29` is **charcoal**—use for **primary filled controls** with **`c2`** labels, not for paragraph text color. **`c31`** is the **only** saturated accent in chrome. **`c60`** is never assigned manually.

### 2.2 Status Colors

| Status | Primary | Background | Text | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------|-----------------|--------------|
| On track | `#5BBFB5` | `#E8F8F6` | `#2A6A62` | `oklch(0.742 0.095 186.6)` | `--status-on-track` |
| At risk | `#6A6A6A` | `#F0F0F0` | `#2A2A2A` | `oklch(0.524 0.000 89.9)` | `--status-at-risk` |
| Behind / alert | `#3C3F41` | `#ECECEC` | `#0A0A0A` | `oklch(0.366 0.005 236.6)` | `--status-alert` |
| Complete / info | `#3DA89E` | `#E6F6F4` | `#1F4A44` | `oklch(0.668 0.098 186.4)` | `--status-complete` |

### 2.3 Shadows

Pure neutral depth from **`c58`** at **low** opacity—no hue shift in the halo.

```css
--shadow:
  0px 0px 0px 1px oklch(0.285 0.000 89.9 / 0.060),
  0px 1px 3px -1px oklch(0.285 0.000 89.9 / 0.050),
  0px 4px 14px 0px oklch(0.285 0.000 89.9 / 0.040);
--shadow-hover:
  0px 0px 0px 1px oklch(0.285 0.000 89.9 / 0.090),
  0px 3px 8px -1px oklch(0.285 0.000 89.9 / 0.070),
  0px 8px 22px 0px oklch(0.285 0.000 89.9 / 0.055);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio JSON maps **all slots `f1`–`f8` → Sans**. This theme intentionally avoids display serifs so engineering dashboards stay utilitarian.

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance`; keep titles short |
| Card / section titles | 16px | SemiBold | 600 | `f2` | Tight leading; prefer single line |
| Body / descriptions | 13px | Regular | 400 | `f3` | line-height **1.5**; `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill`; align numerics to tabular where supported |
| Badges / status | 11px | SemiBold | 600 | `f6` | uppercase; pair with Section 2.2 fills |
| KPI numbers | 28px | SemiBold | 600 | `f7` | **`font-variant-numeric: tabular-nums` (required)** |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; color `c59` |

### 3.3 Weight Rules

- **SemiBold (600)**: Titles, KPI values, badges, primary buttons
- **Regular (400)**: Body, labels, chart axes, table cells, nav links
- **Light (300)**: KPI labels only—must recede behind the metric
- Avoid **Bold (700+)** except rare data-outlier callouts inside charts (not chrome)
- **Tabular numerals**: Mandatory on **`f7`** and financial tables; optional on **`f5`** when axes show currency
- **No serif**: Do not swap `f1`/`f2` to Serif in pro-code—breaks the neutral contract

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Standard | 20px | Chart `f5`; accent ring uses **`c31`** only |
| `ca2` | Filters / controls | `c2` | `c58` | 8px | Standard | 16px | Focus rings **`c31`** 2px |
| `ca3` | Runbook / SOP | `c2` | `c58` | 10px | Soft | 16px | Long-form technical prose |
| `ca4` | Compact | `c2` | `c58` | 6px | None | 12px | Dense pickers |
| `ca5` | KPI hero | `c2` | `c58` | 12px | Standard | 16px | Optional **4px left** in **`c31`** |
| `ca6` | Muted metric | `c3` | `c58` | 8px | None | 12px | Secondary tile on `#F5F5F5` canvas |
| `ca7` | Signal highlight | `c31` @ **10%** on `c2` | `c58` | 10px | Standard | 16px | Teal veil—**only** chromatic wash |
| `ca8` | Full-bleed strip | `c56` | `c58` | 0 | None | 12px | Incidents, maintenance banners |
| `ca9` | Diff / pair | `c2` | `c58` | 10px | Standard | 16px | Before|After with `c47` divider |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#2C2F31` graphite | `c4` |
| Active background | `#3E4244` | `c5` |
| Hover background | `#353839` | `c32` |
| Title font color | `#FFFFFF` | `c2` |
| Link font color | `#FFFFFF` | `c2` |
| Active link font color | `#FFFFFF` | `c2` |
| Active indicator | `#5BBFB5` mint teal | `c31` |
| Title font | 22px SemiBold **Sans** | `f1` |
| Link font | 13px Regular **Sans** | `f3` |
| Divider | `1px solid` `#353839` | `c32` at ~**0.65** opacity over `c4` |
| Drop shadow | false | — |

**Critical**: Do not place **`c58`** on **`c4`**. Teal is for **indicators**, not entire nav backgrounds.

**Implementation notes for agents**:

- **SVG icons** in nav should default to **`c2`**; active state may use **`c31`** stroke on **`c5`** pill.
- **Badge counts** on nav items: `f6` on **`c31`** at **18%** opacity plate, text **`c58`** for small pills on white—**not** on `c4`.
- **Keyboard focus** on dark chrome: **`c31`** 2px outline, **2px** offset.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#5BBFB5` | `oklch(0.742 0.095 186.6)` | Mint teal / primary signal |
| 2 | `#3C3F41` | `oklch(0.366 0.005 236.6)` | Charcoal anchor |
| 3 | `#8AD4CC` | `oklch(0.819 0.075 187.2)` | Light teal |
| 4 | `#6A6A6A` | `oklch(0.524 0.000 89.9)` | Neutral mid |
| 5 | `#3DA89E` | `oklch(0.668 0.098 186.4)` | Deep mint |
| 6 | `#2C2F31` | `oklch(0.303 0.006 236.7)` | Graphite low |

**Chart chrome**: Grid `c47` @ **0.5** opacity; axis `c46`; ticks **`f5`** + `c59`; tooltips **`c2`**, `var(--shadow)`.

**Variance semantics**: Use **teal** for “healthy / within SLO” and **charcoal/graphite** for “baseline / remainder”; avoid introducing reds unless status semantics demand it (then use a single alert hue sparingly).

---

## 7. Agent Prompt Guide

### Do's

- Keep **`c1`** / **`c56`** on **`#F5F5F5`**; cards on **`c2`**
- Treat **`c31`** as the **only** chromatic accent in chrome; charts may use the full series set
- Use **`c29` / `c30`** for **dark filled buttons** with **`c2`** labels
- On **graphite nav**, bind type to **`c2`**
- Use **`font-variant-numeric: tabular-nums`** on **`f7`** and numeric tables
- Keep borders strictly **`c46` / `c47`**—no blue-gray imports from other themes

### Don'ts

- Do not set **`c60`** manually in JSON or tokens
- Do not add **second saturated accent** (purple, orange) to navigation chrome
- Do not tint the **grayscale ramp** cool or warm—achromatic only
- Do not use **`c58`** text on **`c31`** fills without verifying contrast (prefer **`c2`** on solid teal)

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #F5F5F5     Card surface → c2   #FFFFFF
Hover        → c3        #EBEBEB     Nav bg       → c4   #2C2F31
Nav active   → c5        #3E4244     Nav hover    → c32  #353839
Header       → c6        #EBEBEB     Input fill   → c7   #FFFFFF
Accent (UI)  → c29       #3C3F41     Accent ↓     → c30  #2C2F31
Signal teal  → c31       #5BBFB5     Border       → c46  #C0C0C0
Border light → c47       #D8D8D8     Primary text → c58  #2A2A2A (FONT)
Secondary    → c59       #6A6A6A (FONT)   Nav text (dark chrome) → c2
Grayscale ramp → c40–c45, c48–c54 (13 steps); c46–c47 reserved for borders
Never manual → c60       AUTOMATIC_COLOR
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#3C3F41',
  primaryPressed: '#2C2F31',
  signal: '#5BBFB5',
  surface: '#FFFFFF',
  bg: '#F5F5F5',
  text: '#2A2A2A',
  textMuted: '#6A6A6A',
  border: '#C0C0C0',
  borderLight: '#D8D8D8',
  navBg: '#2C2F31',
  navActive: '#3E4244',
  navHover: '#353839',
  onLightChrome: '#2A2A2A',
  onDarkChrome: '#FFFFFF',
  series: ['#5BBFB5', '#3C3F41', '#8AD4CC', '#6A6A6A', '#3DA89E', '#2C2F31']
};
```

### Example Agent Prompts

- **“Neutral shell + teal signal”**: Page `c56`, cards `c2`, single teal accent `c31` for active tab + focus rings.
- **“SRE KPI row”**: Four `ca5` tiles, values `f7` with **tabular-nums**, labels `f8` in `c59`, optional 4px `c31` left rule.
- **“Graphite sidebar”**: Nav `c4`, type `c2`, active `c5`, teal rail `c31`.
- **“Charcoal primary button”**: Fill `c29`, hover `c30`, label `c2`, focus `c31`.
- **“Incident timeline chart”**: Series[0] teal `c31`, Series[1] charcoal `c29`, grid `c47` @ 0.5 alpha.
- **“Comparison table (A|B)”**: Use `ca9`, zebra `c11`, hover `c12`, monospace not required—stay Sans.

### Pro-code and App Studio sync

- Import JSON, then confirm **tabs**: active fill is **`c9`** (**`c31`** teal) with **`c2`** text.
- Pro-code containers inside App Studio cards should inherit shadows from the host card unless explicitly floating.
- If you must add **dark mode** later, rebuild ramps in a separate DESIGN.md—**do not** hue-shift this neutral system.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "Slate Granite",
  "colors": [
    { "index": 1, "value": "#F5F5F5", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#EBEBEB", "tag": "PRIMARY" },
    { "index": 4, "value": "#2C2F31", "tag": "PRIMARY" },
    { "index": 5, "value": "#3E4244", "tag": "PRIMARY" },
    { "index": 6, "value": "#EBEBEB", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#5BBFB5", "tag": "SECONDARY" },
    { "index": 10, "value": "#E8E8E8", "tag": "PRIMARY" },
    { "index": 11, "value": "#FAFAFA", "tag": "PRIMARY" },
    { "index": 12, "value": "#EBEBEB", "tag": "PRIMARY" },
    { "index": 29, "value": "#3C3F41", "tag": "SECONDARY" },
    { "index": 30, "value": "#2C2F31", "tag": "SECONDARY" },
    { "index": 31, "value": "#5BBFB5", "tag": "SECONDARY" },
    { "index": 32, "value": "#353839", "tag": "SECONDARY" },
    { "index": 40, "value": "#0A0A0A", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#191919", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#292929", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#3B3B3B", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#4D4D4D", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#606060", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#C0C0C0", "tag": "CUSTOM" },
    { "index": 47, "value": "#D8D8D8", "tag": "CUSTOM" },
    { "index": 48, "value": "#747474", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#888888", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#9D9D9D", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B2B2B2", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C8C8C8", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#DEDEDE", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F5F5F5", "tag": "GRAYSCALE" },
    { "index": 56, "value": "#F5F5F5", "tag": "PRIMARY" },
    { "index": 58, "value": "#2A2A2A", "tag": "FONT" },
    { "index": 59, "value": "#6A6A6A", "tag": "FONT" }
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
      "accentColor": { "type": "COLOR_REFERENCE", "index": 31 }
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
      "focusBorderColor": { "type": "COLOR_REFERENCE", "index": 31 },
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm **graphite nav** uses **`c2`** type. Active tabs use **`c2`** on teal **`c9`**. **`c60`** is not imported.
