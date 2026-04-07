# CH Charcoal Dark — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Lavender + steel / teal + warm orange highlights · **Mood**: Boutique hotel lounge, editorial data, confident warmth

---

## 1. Visual Theme and Atmosphere

**Personality**: Charcoal Light’s warm neutrals, inverted. The canvas is roasted coffee brown-black; navigation borrows a muted lavender-gray bar that feels designed, not “default dark mode.” Accents are intentionally plural—lavender for structure, steel and teal for analytical calm, orange for human warmth in alerts and highlights.

**Density**: Medium. Give KPI and narrative cards more air than raw grid charts; the **white KPI inversion** (`ca5` on `#FFFFFF`) is a deliberate spotlight—surround it with charcoal silence.

**Philosophy**: Typography carries identity: **Monospace** for the nav title (`f1`) whispers “systems + craft,” **Condensed** labels (`f4`) tighten dashboards without shrinking data ink, and **Sans** handles body and charts. Color never shouts; even orange is burnt caramel, not traffic-cone neon.

**Atmosphere cues**:
- **Lifted warm shadows** from `#E8E2DE` (primary text) at restrained opacity—cards feel paper-lifted, not glassmorphic
- **Lavender nav** (`#5D5A6A`) separates wayfinding from content without copying the page black
- **Signature KPI inversion**: `ca5` cards sit on **pure white** (`#FFFFFF`) for maximum drama on `#1A1512`
- Buttons in App Studio should follow **UNDERLINE** treatment with **LEFT** alignment where the editor allows—pair with monospace titles for an editorial systems aesthetic

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page background (reference) | `#1A1512` | `oklch(0.165 0.008 355.4)` | `c1` | `--bg-ref` |
| Card surface | `#2A2420` | `oklch(0.218 0.009 355.8)` | `c2` | `--surface` |
| Hover surface | `#3A322D` | `oklch(0.266 0.011 355.6)` | `c3` | `--surface-hover` |
| Navigation background | `#5D5A6A` | `oklch(0.389 0.017 184.4)` | `c4` | `--nav-bg` |
| Navigation active | `#3A3448` | `oklch(0.277 0.022 185.4)` | `c5` | `--nav-active` |
| Header background | `#1A1512` | `oklch(0.165 0.008 355.4)` | `c6` | `--header-bg` |
| Input background | `#2A2420` | `oklch(0.218 0.009 355.8)` | `c7` | `--input-bg` |
| Tab surface | `#2A2420` | `oklch(0.218 0.009 355.8)` | `c8` | `--tab-bg` |
| Tab active fill | `#9A96AE` | `oklch(0.559 0.024 184.2)` | `c9` | `--tab-active-bg` |
| Table header background | `#2A2420` | `oklch(0.218 0.009 355.8)` | `c10` | `--table-header-bg` |
| Table row stripe | `#322B26` | `oklch(0.242 0.011 356.1)` | `c11` | `--table-stripe` |
| Table row hover | `#3A322D` | `oklch(0.266 0.011 355.6)` | `c12` | `--table-row-hover` |
| Accent primary (lavender) | `#9A96AE` | `oklch(0.559 0.024 184.2)` | `c29` | `--accent` |
| Accent pressed | `#7F7B92` | `oklch(0.486 0.023 184.2)` | `c30` | `--accent-pressed` |
| Navigation / control hover | `#4A445A` | `oklch(0.322 0.019 184.0)` | `c31` | `--nav-hover` |
| Steel accent | `#8DB5BF` | `oklch(0.610 0.029 172.1)` | `c32` | `--accent-steel` |
| Teal accent | `#7AACA8` | `oklch(0.578 0.019 162.5)` | `c33` | `--accent-teal` |
| Orange accent | `#F4A870` | `oklch(0.656 0.092 355.9)` | `c34` | `--accent-orange` |
| KPI spotlight (white) | `#FFFFFF` | `oklch(0.819 0.000 0.0)` | `c55` | `--kpi-spotlight` |
| Grayscale 1 | `#0E0B09` | `oklch(0.125 0.005 355.9)` | `c40` | `--gray-950` |
| Grayscale 2 | `#181412` | `oklch(0.160 0.006 354.7)` | `c41` | `--gray-900` |
| Grayscale 3 | `#221D1A` | `oklch(0.193 0.008 355.4)` | `c42` | `--gray-850` |
| Grayscale 4 | `#2A2420` | `oklch(0.218 0.009 355.8)` | `c43` | `--gray-800` |
| Grayscale 5 | `#322B26` | `oklch(0.242 0.011 356.1)` | `c44` | `--gray-750` |
| Grayscale 6 | `#3F3732` | `oklch(0.282 0.011 355.6)` | `c45` | `--gray-700` |
| Border | `#4A4240` | `oklch(0.317 0.007 352.0)` | `c46` | `--border` |
| Border light | `#3A322D` | `oklch(0.266 0.011 355.6)` | `c47` | `--border-light` |
| Grayscale 7 | `#6B6360` | `oklch(0.415 0.008 353.5)` | `c48` | `--gray-600` |
| Grayscale 8 | `#867E7A` | `oklch(0.491 0.009 354.7)` | `c49` | `--gray-500` |
| Grayscale 9 | `#A09994` | `oklch(0.564 0.009 356.2)` | `c50` | `--gray-400` |
| Grayscale 10 | `#B8B1AD` | `oklch(0.627 0.008 355.3)` | `c51` | `--gray-300` |
| Grayscale 11 | `#CAC4C0` | `oklch(0.675 0.007 355.9)` | `c52` | `--gray-200` |
| Grayscale 12 | `#D9D4D0` | `oklch(0.715 0.006 356.6)` | `c53` | `--gray-150` |
| Grayscale 13 | `#E8E2DE` | `oklch(0.751 0.007 355.9)` | `c54` | `--gray-100` |
| Page background (App Studio) | `#1A1512` | `oklch(0.165 0.008 355.4)` | `c56` | `--bg` |
| Primary text (FONT) | `#E8E2DE` | `oklch(0.751 0.007 355.9)` | `c58` | `--text-primary` |
| Secondary text (FONT) | `#A89E98` | `oklch(0.579 0.011 355.4)` | `c59` | `--text-secondary` |
| Automatic (never set manually) | — | — | `c60` | — |

### 2.2 Status Colors

| Status | Primary | Background | Notes | OKLCH (primary) | CSS Variable |
|--------|---------|------------|-------|-----------------|--------------|
| On track | `#A0D771` | `#1E2418` | Lime from shared palette | `oklch(0.672 0.068 9.7)` | `--status-on-track` |
| At risk | `#F4A870` | `#2A1E16` | Warm orange family | `oklch(0.656 0.092 355.9)` | `--status-at-risk` |
| Behind / alert | `#E45F5F` | `#2A1616` | Shared alert red | `oklch(0.544 0.087 348.8)` | `--status-alert` |
| Complete / info | `#7AACA8` | `#152220` | Teal accent | `oklch(0.578 0.019 162.5)` | `--status-complete` |

### 2.3 Shadows

Lifted depth: warm veil from primary text, plus a deeper neutral drop for separation from charcoal canvas.

```css
--shadow:
  0px 0px 0px 1px oklch(0.751 0.007 355.9 / 0.20),
  0px 2px 6px -1px oklch(0.751 0.007 355.9 / 0.16),
  0px 10px 28px 0px oklch(0 0 0 / 0.38);
--shadow-hover:
  0px 0px 0px 1px oklch(0.751 0.007 355.9 / 0.26),
  0px 4px 10px -1px oklch(0.751 0.007 355.9 / 0.20),
  0px 14px 36px 0px oklch(0 0 0 / 0.45);
```

---

## 3. Typography

### 3.1 Font System

**Sans** (body, charts, KPIs):

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

**Monospace** (page / nav title slot `f1` only):

```css
font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace;
```

**Condensed** (labels `f4`—Domo “Condensed” preset maps to narrow sans in App Studio):

```css
font-family: "Arial Narrow", "Helvetica Condensed", Arial, sans-serif;
```

Pro-code should pick **one** stack per slot above; never mix Monospace body with Sans nav title.

### 3.2 Type Scale with Slot Mapping

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page / nav title | 22px | SemiBold | 600 | `f1` | **Monospace**; `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | **Sans** |
| Body text / descriptions | 13px | Regular | 400 | `f3` | **Sans**; line-height 1.5 |
| Labels / captions | 11px | Regular | 400 | `f4` | **Condensed**; uppercase; `letter-spacing: 0.05em` |
| Chart axis text | 11px | Regular | 400 | `f5` | **Sans**; SVG `fill` |
| Badges / status | 11px | SemiBold | 600 | `f6` | **Sans** |
| KPI numbers | 28px | SemiBold | 600 | `f7` | **Sans**; `tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | **Sans**; uppercase |

### 3.3 Weight Rules

- **SemiBold (600)**: `f1` title, `f2` headings, `f6` badges, `f7` KPI values
- **Regular (400)**: `f3` body, `f4` labels (Condensed), `f5` chart axes
- **Light (300)**: `f8` only
- Keep **Monospace** usage isolated to `f1` so it reads as “masthead,” not “spreadsheet everywhere”

---

## 4. Card Styles

| Card slot | Role | Background | Font color | Radius | Shadow | Padding | Notes |
|-----------|------|------------|------------|--------|--------|---------|-------|
| `ca1` | Primary analytic | `c2` | `c58` | 10px | Lifted | 20px | Accent `c29`; chart fonts `f5` |
| `ca2` | Controls / filters | `c2` | `c58` | 8px | Lifted | 16px | Border `c47`; inputs `c7` |
| `ca3` | Media / embed | transparent | `c58` | 8px | None | 8px | Let canvas show |
| `ca4` | Dense tables-in-card | `c2` | `c58` | 6px | None | 12px | Pair with table tokens |
| `ca5` | **KPI spotlight** | **`c55` `#FFFFFF`** | **`c58`** | 12px | **Strong lift** | 16px | **Dark text on white**; `f7`/`f8`; optional `c34` rule |
| `ca6` | Secondary metric | `c3` | `c59` | 8px | Soft | 12px | Muted supporting tiles |
| `ca7` | Accent callout | `c5` | `c58` | 8px | Lifted | 16px | Lavender active tone sparingly |
| `ca8` | Banner | transparent | `c58` | 0 | None | 12px | Imagery / gradient from pro-code |

---

## 5. Navigation

| Property | Value | Slot / reference |
|----------|-------|------------------|
| Background | `#5D5A6A` muted lavender | `c4` |
| Active background | `#3A3448` deep lavender | `c5` |
| Hover background | `#4A445A` mid lavender | `c31` |
| Link font color (default) | `#A89E98` warm gray | `c59` |
| Active / title font color | `#E8E2DE` cream-white | `c58` |
| Active indicator | `#9A96AE` | `c29` |
| Title font | 22px SemiBold **Monospace** | `f1` |
| Link font | 13px Regular Sans | `f3` |
| Button style | **UNDERLINE** | — |
| Button alignment | **LEFT** | — |
| Shadow | true (lifted stack) | — |

If App Studio does not expose underline/left in JSON, apply equivalent styles in pro-code link components while keeping native nav colors aligned to **`c4`–`c5`–`c31`**.

---

## 6. Chart Color Palette

| Series | Hex | OKLCH | Role |
|--------|-----|-------|------|
| 1 | `#9A96AE` | `oklch(0.559 0.024 184.2)` | Lavender anchor |
| 2 | `#7AACA8` | `oklch(0.578 0.019 162.5)` | Teal / cool secondary |
| 3 | `#8DB5BF` | `oklch(0.610 0.029 172.1)` | Steel highlight |
| 4 | `#F4A870` | `oklch(0.656 0.092 355.9)` | Warm orange contrast |
| 5 | `#A0D771` | `oklch(0.672 0.068 9.7)` | Lime / growth |
| 6 | `#E45F5F` | `oklch(0.544 0.087 348.8)` | Alert / negative |

Pro-code: `['#9A96AE', '#7AACA8', '#8DB5BF', '#F4A870', '#A0D771', '#E45F5F']`

### Chart chrome

- Grids: `c47` @ 45% opacity; axes: `c46` @ 65%
- Legends / ticks: `c59` (`f5` Sans—**not** Condensed)
- Tooltips: `c2` surface, `c58` text; use Sans for consistency

---

## 7. Agent Prompt Guide

### Do's

- Use **`c55`** only for deliberate spotlight surfaces (`ca5` KPI), never as a global page fill
- Keep **`f1` Monospace** exclusively for the nav / page title slot in JSON and pro-code
- Use **`f4` Condensed** for form labels, filter chips, and table captions
- Thread **lavender (`c29`)** through tabs, focus rings, and primary series before introducing orange
- Apply **lifted shadows** (Section 2.3)—this theme fails if cards flatten to single-layer drops

### Don'ts

- Never assign **`c60`** to font colors on dark surfaces
- Do not set KPI text to cream (`c58`) on charcoal (`c2`) when the spec calls for **`ca5` white**—that breaks the signature inversion
- Do not replace Condensed **`f4`** with Monospace for labels (too “terminal”)
- Avoid pure black shadows; keep the warm `c58` tint in the outer ring

### Slot Mapping Cheat Sheet

```
Page bg      → c1 / c56  #1A1512     Card surface → c2   #2A2420
Hover        → c3        #3A322D     Nav bg       → c4   #5D5A6A
Nav active   → c5        #3A3448     Nav hover    → c31  #4A445A
Accent       → c29       #9A96AE     Accent ↓     → c30  #7F7B92
Steel / Teal / Orange → c32 #8DB5BF, c33 #7AACA8, c34 #F4A870
KPI white    → c55       #FFFFFF     Border       → c46  #4A4240
Border light → c47       #3A322D     Primary text → c58  #E8E2DE
Secondary    → c59       #A89E98     Grayscale    → c40–c54 (brown ramp); c46–c47 borders
Never        → c60 for fonts
```

### Pro-Code COLORS Object

```javascript
const COLORS = {
  primary: '#9A96AE',
  primaryPressed: '#7F7B92',
  steel: '#8DB5BF',
  teal: '#7AACA8',
  orange: '#F4A870',
  surface: '#2A2420',
  bg: '#1A1512',
  text: '#E8E2DE',
  textMuted: '#A89E98',
  border: '#4A4240',
  borderLight: '#3A322D',
  kpiSpotlight: '#FFFFFF',
  navBg: '#5D5A6A',
  navActive: '#3A3448',
  navHover: '#4A445A',
  positive: '#A0D771',
  negative: '#E45F5F',
  series: ['#9A96AE', '#7AACA8', '#8DB5BF', '#F4A870', '#A0D771', '#E45F5F']
};
```

### Example Agent Prompts

- **“Hero KPI strip (CH Charcoal Dark)”**: Use native or pro-code **`ca5`** with **`c55`** background, **`c58`** text, **`f7`/`f8`**, `var(--shadow-hover)`. Surround with **`c2`** analytic cards for rhythm.
- **“Left nav title”**: Apply **`f1`** Monospace SemiBold 22px, **`c58`** color, on **`c4`** background; links **`c59`**, active **`c58`**, hover bg **`c31`**.
- **“Underline text button row”**: App Studio **UNDERLINE** + **LEFT** alignment; pro-code: `text-decoration-thickness: 2px`, `text-underline-offset: 4px`, underline color **`c29`**; default text **`c59`**, hover **`c58`**.
- **“Mixed-accent chart”**: Map series 1–3 to lavender/teal/steel; reserve **`c34`** orange for the single series that must pop (e.g., revenue vs. cost stack).

### Pro-Code `:root` Reference

```css
:root {
  --bg: #1A1512;
  --surface: #2A2420;
  --surface-hover: #3A322D;
  --nav-bg: #5D5A6A;
  --nav-active: #3A3448;
  --nav-hover: #4A445A;
  --accent: #9A96AE;
  --accent-pressed: #7F7B92;
  --accent-steel: #8DB5BF;
  --accent-teal: #7AACA8;
  --accent-orange: #F4A870;
  --border: #4A4240;
  --border-light: #3A322D;
  --text-primary: #E8E2DE;
  --text-secondary: #A89E98;
  --kpi-spotlight: #FFFFFF;
}
```

### Parity Checklist

1. JSON **`fonts[0]`** is **Monospace**; **`fonts[3]`** is **Condensed**.
2. JSON **`cards`** includes **`index: 5`** referencing **`c55`** for KPI inversion.
3. All font color references resolve to **`58`/`59`**, never **`60`**.
4. Shadow CSS uses warm tint from **`c58`**, not cold neutral gray.

---

## 8. App Studio Theme JSON (Importable)

```json
{
  "name": "CH Charcoal Dark",
  "colors": [
    { "index": 1, "value": "#1A1512", "tag": "PRIMARY" },
    { "index": 2, "value": "#2A2420", "tag": "PRIMARY" },
    { "index": 3, "value": "#3A322D", "tag": "PRIMARY" },
    { "index": 4, "value": "#5D5A6A", "tag": "PRIMARY" },
    { "index": 5, "value": "#3A3448", "tag": "PRIMARY" },
    { "index": 6, "value": "#1A1512", "tag": "PRIMARY" },
    { "index": 7, "value": "#2A2420", "tag": "PRIMARY" },
    { "index": 8, "value": "#2A2420", "tag": "PRIMARY" },
    { "index": 9, "value": "#9A96AE", "tag": "SECONDARY" },
    { "index": 10, "value": "#2A2420", "tag": "PRIMARY" },
    { "index": 11, "value": "#322B26", "tag": "PRIMARY" },
    { "index": 12, "value": "#3A322D", "tag": "PRIMARY" },
    { "index": 29, "value": "#9A96AE", "tag": "SECONDARY" },
    { "index": 30, "value": "#7F7B92", "tag": "SECONDARY" },
    { "index": 31, "value": "#4A445A", "tag": "SECONDARY" },
    { "index": 32, "value": "#8DB5BF", "tag": "SECONDARY" },
    { "index": 33, "value": "#7AACA8", "tag": "SECONDARY" },
    { "index": 34, "value": "#F4A870", "tag": "SECONDARY" },
    { "index": 40, "value": "#0E0B09", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#181412", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#221D1A", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#2A2420", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#322B26", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#3F3732", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#4A4240", "tag": "CUSTOM" },
    { "index": 47, "value": "#3A322D", "tag": "CUSTOM" },
    { "index": 48, "value": "#6B6360", "tag": "GRAYSCALE" },
    { "index": 49, "value": "#867E7A", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#A09994", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B8B1AD", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#CAC4C0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#D9D4D0", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E8E2DE", "tag": "GRAYSCALE" },
    { "index": 55, "value": "#FFFFFF", "tag": "CUSTOM" },
    { "index": 56, "value": "#1A1512", "tag": "PRIMARY" },
    { "index": 58, "value": "#E8E2DE", "tag": "FONT" },
    { "index": 59, "value": "#A89E98", "tag": "FONT" }
  ],
  "fonts": [
    { "index": 1, "family": "Monospace", "weight": "SemiBold", "size": "22px", "style": "normal" },
    { "index": 2, "family": "Sans", "weight": "SemiBold", "size": "16px", "style": "normal" },
    { "index": 3, "family": "Sans", "weight": "Regular", "size": "13px", "style": "normal" },
    { "index": 4, "family": "Condensed", "weight": "Regular", "size": "11px", "style": "normal" },
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
    },
    {
      "index": 5,
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "titleFont": { "type": "FONT_REFERENCE", "index": 2 },
      "chartFont": { "type": "FONT_REFERENCE", "index": 5 },
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 55 },
      "borderRadius": 12,
      "borderWidth": 0,
      "dropShadow": true,
      "dropShadowColor": { "type": "COLOR_REFERENCE", "index": 40 },
      "padding": 16,
      "elementSpacing": 12,
      "accentColor": { "type": "COLOR_REFERENCE", "index": 34 }
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

> **Import note**: Confirm **`cards`** contains both **`index: 1`** and **`index: 5`** (KPI white). Set native button style to **UNDERLINE** / **LEFT** in the Theme Editor UI if those fields are not exported in JSON. Never use **`c60`** for font colors.
