# CH Charcoal Light — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Warm charcoal with lavender-steel-teal · **Mood**: Editorial, sophisticated, technical
> **Origin**: Extracted from production theme "Custom-Theme--CH-UX---Charcoal"

---

## 1. Visual Theme and Atmosphere

**Personality**: Technical editorial meets warm sophistication. Brown-tinted charcoal grays (#1A1512 → #E4DCD8) give warmth that pure neutrals lack, while the tri-accent system — lavender gray (#777484), steel blue (#81A0AA), teal (#6A9490) — adds visual interest without loudness. The Monospace nav title and Condensed description font give the app a typographic, magazine-like quality.

**Density**: Medium-high. Fixed-width 8-column grid. Charts use minimal padding (1px) for data density; content cards use standard 16px padding.

**Philosophy**: Warm restraint. The warm brown-tinted grays are the foundation — they feel more human than cool grays. Three cool accents (lavender, steel, teal) provide variety without chaos. Card chrome uses LIFTED shadows for subtle depth. The font mix (Monospace titles, Condensed descriptions, Sans body) creates a layered typographic hierarchy that feels intentional and editorial.

**Atmosphere cues**:
- Page canvas is **white** (#FFFFFF) with **warm neutral** card surfaces (#E8E8EA, #E4DCD8)
- Navigation is **lavender gray** (#777484) with UNDERLINE button style and LEFT alignment
- KPI cards (ca5) use **pure black** (#000000) backgrounds for dramatic contrast
- Cards use **LIFTED** shadows throughout — subtle depth without heaviness
- The **Monospace** nav title font gives a technical/code-inspired edge
- Warm orange (#F49B5C, #FFA05A) provides accent contrast via custom colors and chart series

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

| Semantic Role          | Hex       | Theme Slot | CSS Variable         |
|------------------------|-----------|------------|----------------------|
| Page Background        | `#FFFFFF` | `c56`      | `--bg`               |
| Card Surface (charts)  | `#E8E8EA` | `c27`      | `--surface`          |
| Card Surface (alt)     | `#E4DCD8` | `c7`       | `--surface-warm`     |
| Primary Text (dark)    | `#000000` | `c58`      | `--text-primary`     |
| Light Text             | `#FFFFFF` | `c59`      | `--text-light`       |
| Warm Gray Darkest      | `#1A1512` | `c1`       | `--gray-900`         |
| Warm Gray Dark         | `#36312E` | `c2`       | `--gray-800`         |
| Warm Gray Mid          | `#564F4C` | `c3`       | `--gray-700`         |
| Warm Gray              | `#77706D` | `c4`       | `--gray-600`         |
| Warm Gray Light        | `#9A928F` | `c5`       | `--gray-500`         |
| Warm Gray Lighter      | `#BEB7B3` | `c6`       | `--gray-400`         |
| Charcoal Primary       | `#2E2825` | `c8`       | `--charcoal`         |
| Charcoal Mid           | `#4D4643` | `c9`       | `--charcoal-mid`     |
| Charcoal Light         | `#615B57` | `c10`      | `--charcoal-light`   |
| Lavender Gray          | `#777484` | `c22`      | `--lavender`         |
| Steel Blue             | `#81A0AA` | `c29`      | `--steel`            |
| Teal                   | `#6A9490` | `c36`      | `--teal`             |
| Nav Background         | `#777484` | `c22`      | `--nav-bg`           |
| Nav Active             | `#4D4643` | `c9`       | `--nav-active`       |
| Nav Hover              | `#2E2825` | `c8`       | `--nav-hover`        |
| Custom Steel Blue      | `#81A0AA` | `c61`      | `--custom-steel`     |
| Custom Salmon/Orange   | `#F49B5C` | `c62`      | `--custom-orange`    |

### 2.2 Chart Series (Key Colors)

| Series | Hex       | Name           | colorRange ref |
|--------|-----------|----------------|----------------|
| 1      | `#777484` | Lavender gray  | Color 1 key    |
| 2      | `#6A9490` | Teal           | Color 2 key    |
| 3      | `#81A0AA` | Steel blue     | Color 3 key    |
| 4      | `#FFA05A` | Amber/orange   | Color 4 key    |
| 5      | `#A0D771` | Lime           | Color 5 key    |
| 6      | `#FBAD56` | Gold           | Color 6 key    |
| 7      | `#C92E25` | Red            | Color 7 key    |

Pro-code chart series: `['#777484', '#6A9490', '#81A0AA', '#FFA05A', '#A0D771', '#FBAD56']`

---

## 3. Typography

### 3.1 Font System

**Mixed font families** — this theme's typographic variety is a defining feature:

| Domo Family  | Pro-Code CSS `font-family`                                     | Used For           |
|--------------|----------------------------------------------------------------|--------------------|
| **Monospace**| `"SF Mono", "Fira Code", "Cascadia Code", monospace`           | Nav title (f1)     |
| **Condensed**| `"Roboto Condensed", "Arial Narrow", sans-serif`               | Descriptions (f6)  |
| **Sans**     | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif` | Everything else |

### 3.2 Type Scale with Slot Mapping

| Role                  | Size | Weight   | Family     | Theme Slot |
|-----------------------|------|----------|------------|------------|
| Nav Title             | 24px | Regular  | Monospace  | `f1`       |
| Section Heading       | 32px | Bold     | Sans       | `f2`       |
| Summary Number        | 24px | SemiBold | Sans       | `f3`       |
| Card Title            | 14px | SemiBold | Sans       | `f4`       |
| Subheading            | 20px | Bold     | Sans       | `f5`       |
| Description / Caption | 12px | Light    | Condensed  | `f6`       |
| Body / Chart Text     | 12px | Regular  | Sans       | `f7`       |
| Nav Link / Button     | 14px | SemiBold | Sans       | `f8`       |
| Pill Label            | 12px | SemiBold | Sans       | `f9`       |

---

## 4. Card Styles

| Style | Role          | Background       | Border Radius | Shadow  | Padding  |
|-------|---------------|------------------|---------------|---------|----------|
| `ca1` | Charts        | `c27` (#E8E8EA)  | 4px           | LIFTED  | 1px      |
| `ca2` | Controls      | `c28` (#FFFFFF)  | 4px           | LIFTED  | 16px     |
| `ca3` | Images/Docs   | transparent      | 4px           | LIFTED  | 4px      |
| `ca5` | KPI / Summary | `c21` (#000000)  | 4px           | NONE    | 16px     |
| `ca8` | Banners       | transparent      | 4px           | NONE    | 16px     |

**Notable**: ca5 (KPI cards) use **pure black** background — a bold design choice that makes summary numbers pop dramatically against the light canvas.

---

## 5. Navigation

| Property        | Value                          |
|-----------------|--------------------------------|
| Background      | `c22` (#777484 — lavender gray)|
| Active BG       | `c9` (#4D4643)                 |
| Hover BG        | `c8` (#2E2825)                 |
| Link Font Color | `c60` (auto)                   |
| Title Font      | `f1` (Monospace 24px Regular)  |
| Button Style    | UNDERLINE                      |
| Button Align    | LEFT                           |
| Shadow          | true                           |

---

## 6. Components & Pills

This theme includes a **full component system** (co1–co8) with detailed hover/active states, and **3 pill styles** (p1–p3) — more comprehensive than most themes. Key component features:

- **co1**: Bordered items (2px c12), dark hover fills, no shadow
- **co3**: LIFTED + FLOATING shadows for dramatic depth on hover/active
- **Pills**: p1 uses charcoal bg (c8), p2 uses white bg with gray border, p3 uses charcoal @ 50% opacity

---

## 7. Agent Prompt Guide

### 7.1 Do's
- Use the Monospace font for the nav title — it's the theme's signature typographic element
- Use Condensed for descriptions and captions — it creates a magazine-like density
- Leverage the tri-accent system: lavender (#777484) for structure, steel (#81A0AA) for data, teal (#6A9490) for secondary data
- Use the black KPI cards (ca5) for hero metrics — they create dramatic contrast

### 7.2 Don'ts
- Don't flatten all fonts to Sans — the Monospace/Condensed mix is intentional
- Don't skip the LIFTED shadows — they're core to the theme's depth language
- Don't use pure black (#000000) for body text — use charcoal (#2E2825) or warm grays
- Don't pair the amber/orange (#FFA05A) with the lavender (#777484) as adjacent chart series — they clash at similar luminance

### 7.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#777484',
  secondary: '#81A0AA',
  tertiary:  '#6A9490',
  surface:   '#E8E8EA',
  bg:        '#FFFFFF',
  text:      '#2E2825',
  textMuted: '#77706D',
  border:    '#BEB7B3',
  positive:  '#A0D771',
  negative:  '#C92E25',
  orange:    '#F49B5C',
  series: ['#777484', '#6A9490', '#81A0AA', '#FFA05A', '#A0D771', '#FBAD56']
};
```

---

## 8. App Studio Theme JSON (Importable)

The source theme JSON file is `Custom-Theme--CH-UX---Charcoal.json`. Apply via the App Studio PUT endpoint using the full JSON payload. Key slot summary:

```
Page bg      → c56  #FFFFFF    Card bg (chart) → c27  #E8E8EA
Nav bg       → c22  #777484    Nav active      → c9   #4D4643
Primary text → c58  #000000    Light text      → c59  #FFFFFF
Charcoal     → c8   #2E2825    Steel blue      → c29  #81A0AA
Teal         → c36  #6A9490    Lavender        → c22  #777484
Custom steel → c61  #81A0AA    Custom orange   → c62  #F49B5C
KPI cards    → ca5  bg=c21 (#000000) — dramatic black
```
