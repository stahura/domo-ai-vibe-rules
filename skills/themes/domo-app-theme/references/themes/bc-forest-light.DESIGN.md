# BC Forest Light — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Deep forest green · **Mood**: Organic, premium, editorial
> **Origin**: Extracted from production theme "Custom Theme - BC UX - Custom2"

---

## 1. Visual Theme and Atmosphere

**Personality**: Sustainability-forward brand meets editorial polish. The deep forest green navigation (#0B150F → #146240) anchors the app with authority while the white canvas and mint accents (#AFEFD3) keep things fresh and readable. Data tells the story; the chrome recedes.

**Density**: Medium-high. Fixed-width 8-column grid. Cards use minimal internal padding (1px on charts, 4–16px on content) for maximum data density.

**Philosophy**: Nature-derived restraint. Forest greens and sage tones carry the brand identity exclusively through navigation and accent elements. Charts get the full multi-hue palette (sage, lime, amber, red) — structural UI stays green-tinted neutral. Card surfaces are mint (#AFEFD3) or white, never competing with data ink.

**Atmosphere cues**:
- Surfaces are **white on white** (`#FFFFFF` canvas) — the green lives in nav and accents only
- Navigation is **dark forest** (#0B150F) with white text and green active/hover states
- Cards use **mint backgrounds** (ca1 = #AFEFD3) or **transparent** (ca8 banners)
- KPI cards (ca5) get generous border-radius (12px) for a soft, modern feel
- No drop shadows on most card styles — clean edges, PILL nav buttons

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role          | Hex       | Theme Slot | CSS Variable         |
|------------------------|-----------|------------|----------------------|
| Page Background        | `#FFFFFF` | `c56`      | `--bg`               |
| Card Surface (charts)  | `#AFEFD3` | `c7`       | `--surface`          |
| Surface Hover          | `#EBEBEB` | `c55`      | `--surface-hover`    |
| Primary Text (dark)    | `#000000` | `c58`      | `--text-primary`     |
| Light Text             | `#FFFFFF` | `c59`      | `--text-light`       |
| Tinted Gray Darkest    | `#121714` | `c1`       | `--gray-900`         |
| Tinted Gray Dark       | `#2E3430` | `c2`       | `--gray-800`         |
| Tinted Gray Mid        | `#4C524F` | `c3`       | `--gray-700`         |
| Tinted Gray            | `#6D736F` | `c4`       | `--gray-600`         |
| Tinted Gray Light      | `#8F9692` | `c5`       | `--gray-500`         |
| Tinted Gray Lighter    | `#B3BAB6` | `c6`       | `--gray-400`         |
| Accent Primary         | `#146240` | `c8`       | `--accent`           |
| Accent Active          | `#368460` | `c9`       | `--accent-active`    |
| Accent Mid             | `#4D9A75` | `c10`      | `--accent-mid`       |
| Accent Light           | `#7BC79F` | `c12`      | `--accent-light`     |
| Accent Lightest        | `#A8F4CA` | `c14`      | `--accent-lightest`  |
| Secondary (near-black) | `#0B150F` | `c22`      | `--secondary`        |
| Tertiary (sage)        | `#71B798` | `c29`      | `--tertiary`         |
| Quaternary (dark grn)  | `#08271A` | `c36`      | `--quaternary`       |
| Nav Background         | `#0B150F` | `c22`      | `--nav-bg`           |
| Nav Active             | `#368460` | `c9`       | `--nav-active`       |
| Nav Hover              | `#146240` | `c8`       | `--nav-hover`        |
| Custom 1               | `#337E5D` | `c61`      | `--custom-1`         |
| Custom 2               | `#F7F7F7` | `c62`      | `--custom-2`         |
| Custom 3               | `#81A0AA` | `c63`      | `--custom-3`         |

### 2.2 Chart Series (Key Colors)

| Series | Hex       | Name           | colorRange ref |
|--------|-----------|----------------|----------------|
| 1      | `#0B150F` | Near-black     | Color 1 key    |
| 2      | `#08271A` | Dark forest    | Color 2 key    |
| 3      | `#71B798` | Sage green     | Color 3 key    |
| 4      | `#337E5D` | Forest green   | Color 4 key    |
| 5      | `#A0D771` | Lime           | Color 5 key    |
| 6      | `#FBAD56` | Amber          | Color 6 key    |
| 7      | `#C92E25` | Red            | Color 7 key    |

Pro-code chart series: `['#71B798', '#337E5D', '#A0D771', '#FBAD56', '#C92E25', '#0B150F']`

---

## 3. Typography

### 3.1 Font System

All **Sans** family. System sans-serif stack for pro-code:
```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

### 3.2 Type Scale with Slot Mapping

| Role                  | Size | Weight   | Theme Slot |
|-----------------------|------|----------|------------|
| Display / Hero        | 48px | SemiBold | `f1`       |
| Section Heading       | 32px | Bold     | `f2`       |
| Summary Number        | 24px | SemiBold | `f3`       |
| Card Title / Nav Link | 16px | SemiBold | `f4` / `f8`|
| Subheading            | 20px | Bold     | `f5`       |
| Description           | 14px | Light    | `f6`       |
| Body / Chart Text     | 12px | Regular  | `f7`       |

---

## 4. Card Styles

| Style | Role          | Background    | Border Radius | Shadow | Padding    |
|-------|---------------|---------------|---------------|--------|------------|
| `ca1` | Charts        | `c7` (mint)   | 4px           | NONE   | 1px all    |
| `ca2` | Controls      | `c55` @ 20%   | 4px           | NONE   | 16px       |
| `ca3` | Images/Docs   | transparent   | 4px           | NONE   | 4px        |
| `ca5` | KPI / Summary | `c56` (white) | 12px          | NONE   | 4px        |
| `ca8` | Banners       | transparent   | 4px           | NONE   | 8px        |

---

## 5. Navigation

| Property        | Value                       |
|-----------------|-----------------------------|
| Background      | `c22` (#0B150F — near-black) |
| Active BG       | `c9` (#368460)              |
| Hover BG        | `c8` (#146240)              |
| Link Font Color | `c56` (#FFFFFF — white)     |
| Title Font      | `f1` (48px SemiBold)        |
| Button Style    | PILL                        |
| Shadow          | true                        |

---

## 6. Agent Prompt Guide

### 6.1 Do's
- Use mint (`#AFEFD3`) for chart card backgrounds — it's the signature look
- Keep page canvas white; the green lives in nav and accents
- Use forest green (#146240) as the primary accent for pro-code elements
- Chart series should span sage → forest → lime → amber → red for good differentiation

### 6.2 Don'ts
- Don't use the dark nav color (#0B150F) as card text — it's too close to pure black
- Don't put green accents on green card backgrounds — use white or neutral instead
- Don't omit the chart's amber (#FBAD56) and red (#C92E25) — they provide essential warm contrast

### 6.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#146240',
  secondary: '#71B798',
  tertiary:  '#337E5D',
  surface:   '#AFEFD3',
  bg:        '#FFFFFF',
  text:      '#000000',
  textMuted: '#6D736F',
  border:    '#B3BAB6',
  positive:  '#A0D771',
  negative:  '#C92E25',
  series: ['#71B798', '#337E5D', '#A0D771', '#FBAD56', '#C92E25', '#0B150F']
};
```

---

## 7. App Studio Theme JSON (Importable)

The source theme JSON file is `Custom-Theme---BC-UX---Custom2.json`. Apply via the App Studio PUT endpoint using the full JSON payload. Key slot summary:

```
Page bg      → c56  #FFFFFF    Card bg (chart) → c7   #AFEFD3
Nav bg       → c22  #0B150F    Nav active      → c9   #368460
Primary text → c58  #000000    Light text      → c59  #FFFFFF
Accent       → c8   #146240    Tertiary        → c29  #71B798
Custom       → c61  #337E5D    Custom          → c63  #81A0AA
```
