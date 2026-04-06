# Dieselpunk — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Rust orange · **Mood**: WWI–WWII industrial war tech, noir, propaganda poster aesthetic — diesel smoke and iron. Film noir meets military command.

---

## 1. Visual Theme and Atmosphere

**Personality**: War room command center circa 1942. Heavy, utilitarian, no decoration — every element serves a function. Surfaces feel like riveted iron panels. The palette is intentionally muted and desaturated; nothing shiny or polished. Typography feels industrial — weight does the work, no flourishes. All colors read as if filtered through diesel exhaust: slightly darkened, slightly warm.

**Density**: Medium-high. Cards pack tightly with 16px gaps; internal padding (20px) keeps each card legible. Dark gunmetal surfaces let tight grids feel orderly, not cramped.

**Philosophy**: Restraint. Rust orange is earned — primary series, active states, and the single most important call-to-action per view. Supporting hues (olive, khaki, propaganda red) appear in data and status, never as decorative chrome. If anything reads as neon or high-chroma, the design has failed.

**Atmosphere cues**:
- Surfaces read as dark iron and weathered steel — cool-neutral with a sooty warmth
- Motion is short (150ms), linear or ease-out — mechanical, not playful
- Shadows are heavier (black at ~0.35–0.45 opacity) for an oppressive, weighty stack
- Text is worn paper cream (`#D8D0C0`), never pure white — pure white breaks the noir, propaganda-poster discipline

**Best for**: Military and defense analytics, industrial operations, supply chain logistics, heavy manufacturing, infrastructure monitoring.

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                         | Theme Slot | CSS Variable        |
|---------------------|-----------|-------------------------------|------------|---------------------|
| Page Background     | `#111214` | `oklch(0.08 0.012 265)`       | `c1`       | `--bg`              |
| Card Surface        | `#1C1E22` | `oklch(0.14 0.015 265)`       | `c2`       | `--surface`         |
| Surface Hover       | `#262A2E` | `oklch(0.20 0.018 250)`       | `c3`       | `--surface-hover`   |
| Primary Text        | `#D8D0C0` | `oklch(0.86 0.018 85)`        | `c58`      | `--text-primary`    |
| Secondary Text      | `#787878` | `oklch(0.55 0.008 70)`        | `c59`      | `--text-secondary`  |
| Border              | `#2E3034` | `oklch(0.22 0.012 265)`       | `c46`      | `--border`          |
| Border Light        | `#242628` | `oklch(0.18 0.010 265)`       | `c47`      | `--border-light`    |
| Accent              | `#C87030` | `oklch(0.58 0.12 48)`         | `c29`      | `--accent`          |
| Accent Muted        | `rgba(200,112,48,0.15)` | `oklch(0.58 0.12 48 / 0.15)` | —        | `--accent-muted`    |
| Accent Hover        | `#D88040` | `oklch(0.64 0.11 52)`         | `c30`      | `--accent-hover`    |
| Nav Background      | `#0E1012` | `oklch(0.07 0.010 265)`       | `c4`       | `--nav-bg`          |
| Nav Active          | `#262A2E` | `oklch(0.20 0.018 250)`       | `c5`       | `--nav-active`      |
| Header Background   | `#111214` | `oklch(0.08 0.012 265)`       | `c6`       | `--header-bg`       |
| Input Background    | `#1C1E22` | `oklch(0.14 0.015 265)`       | `c7`       | `--input-bg`        |
| Input Border        | `#2E3034` | `oklch(0.22 0.012 265)`       | `c48`      | `--input-border`    |
| Tab Default BG      | `#1C1E22` | `oklch(0.14 0.015 265)`       | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#C87030` | `oklch(0.58 0.12 48)`         | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#0E1012` | `oklch(0.07 0.010 265)`       | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#181A1E` | `oklch(0.12 0.014 265)`       | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#262A2E` | `oklch(0.20 0.018 250)`       | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#000000` | `oklch(0 0 0)`                | `c40`      | —                   |
| Grayscale 2         | `#08090A` | `oklch(0.05 0.008 265)`       | `c41`      | —                   |
| Grayscale 3         | `#111214` | `oklch(0.08 0.012 265)`       | `c42`      | —                   |
| Grayscale 4         | `#181A1E` | `oklch(0.12 0.014 265)`       | `c43`      | —                   |
| Grayscale 5         | `#2E3034` | `oklch(0.22 0.012 265)`       | `c44`      | —                   |
| Grayscale 6         | `#505458` | `oklch(0.35 0.012 250)`       | `c45`      | —                   |
| Grayscale 7         | `#606468` | `oklch(0.45 0.010 250)`       | `c49`      | —                   |
| Grayscale 8         | `#787878` | `oklch(0.55 0.008 70)`        | `c50`      | —                   |
| Grayscale 9         | `#9A968E` | `oklch(0.65 0.015 85)`        | `c51`      | —                   |
| Grayscale 10        | `#B8B0A4` | `oklch(0.74 0.018 85)`        | `c52`      | —                   |
| Grayscale 11        | `#D8D0C0` | `oklch(0.86 0.018 85)`        | `c53`      | —                   |
| Grayscale 12        | `#E8E4DC` | `oklch(0.91 0.012 85)`        | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background (dark tint) | Text      | CSS Variable     |
|----------|-----------|-------------------------|-----------|------------------|
| On Track | `#7A8830` | `#1A2214`                 | `#7A8830` | `--on-track`     |
| At Risk  | `#C87030` | `#2A1C14`                 | `#C87030` | `--at-risk`      |
| Behind   | `#B03030` | `#221616`                 | `#B03030` | `--behind`       |
| Complete | `#6B7A88` | `#14181C`                 | `#8A9AA8` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.10–0.14) with readable text in the status hue — never light pastel fills on dark iron surfaces.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.35),
  0px 1px 3px -1px oklch(0 0 0 / 0.42),
  0px 2px 6px 0px oklch(0 0 0 / 0.30);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.40),
  0px 2px 6px -1px oklch(0 0 0 / 0.45),
  0px 4px 12px 0px oklch(0 0 0 / 0.35);
```

Shadow color is **pure black** at **0.30–0.45** opacity — heavier than typical dark UI defaults to reinforce mass, depth, and command-center gravity. No colored shadows.

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** family for all font slots. Industrial discipline: no serif or monospace in the base theme (add monospace in pro-code only if raw logistics codes demand it).

### 3.2 Type Scale with Slot Mapping

| Role                     | Size | Weight   | CSS `font-weight` | Theme Font Slot | Extra                                  |
|--------------------------|------|----------|-------------------|-----------------|----------------------------------------|
| Page title               | 22px | SemiBold | 600               | `f1`            | `text-wrap: balance`                   |
| Card / section titles    | 16px | SemiBold | 600               | `f2`            | `text-wrap: balance`                   |
| Body text / descriptions | 13px | Regular  | 400               | `f3`            | line-height 1.5, `text-wrap: pretty`   |
| Labels / captions        | 11px | Regular  | 400               | `f4`            | uppercase, `letter-spacing: 0.04em`    |
| Chart axis text          | 11px | Regular  | 400               | `f5`            | `fill` color, not CSS `color`          |
| Badges / status text     | 11px | SemiBold | 600               | `f6`            | only small text that gets weight       |
| KPI numbers              | 28px | SemiBold | 600               | `f7`            | `font-variant-numeric: tabular-nums`   |
| KPI labels               | 11px | Light    | 300               | `f8`            | uppercase, `letter-spacing: 0.04em`    |

### 3.3 Weight Rules

- **SemiBold (600)**: Headings, KPI values, active button labels, badges — the “stamped plate” hierarchy
- **Regular (400)**: Body, chart axes, table cells — operational clarity
- **Light (300)**: KPI labels and timeframe captions — recede behind the metric
- **Never Bold (700) or Black (900)** — they read as propaganda shout, not industrial order

### 3.4 Text Color Rules

Primary text is `#D8D0C0` (worn paper cream), not `#FFFFFF`. Secondary text at `#787878` (tarnished silver) defines hierarchy without introducing blue-gray polish. Chart axes, tooltips, and legends use `--text-secondary`; only values and primary labels use `--text-primary`.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#1C1E22`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#D8D0C0`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `6px`                          | `ca1.borderRadius` = `6`      |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#C87030`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible card border — separation comes from shadow and the step from gunmetal page (`--bg`) to dark iron surface (`--surface`). **6px radius** keeps corners angular enough for an industrial panel; do not exceed **6px** on structural containers.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#1C1E22`  | `#2E3034` | `#787878` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#262A2E`  | `#C87030` | `#D8D0C0` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#C87030`  | `#C87030` | `#111214` | `--accent` / `--accent` / `--bg` |
| Disabled | `#0E1012`  | `#242628` | `#505458` | — |

Ghost/outline by default. Border radius: **6px** (same cap as cards for consistency). Transition: `transform, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.98)` — subtle, mechanical.

### 4.3 Inputs and Selects

| Property     | Value                     |
|--------------|---------------------------|
| Background   | `#1C1E22` (`--surface`)   |
| Border       | `#2E3034` (`--border`)    |
| Text         | `#D8D0C0` (`--text-primary`) |
| Placeholder  | `#505458` (`--placeholder`, `c45`) |
| Focus border | `#C87030` (`--accent`)    |
| Radius       | `6px`                     |
| Font         | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint (L ~0.12) with hue borrowed from the status color
- Text: status primary color
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius **4px** (keep badges compact; cards stay at 6px max)

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#0E1012`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#787878`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#D8D0C0`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#C87030`             | `navigation.activeColor` → `c29`    |
| Title text        | `#D8D0C0`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#262A2E`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58` or `c59`** as appropriate — **never `c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text and will disappear on gunmetal nav.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#111214`             | `headers.backgroundColor` → `c1` |
| Font color  | `#D8D0C0`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#0E1012`             | `tables.headerBG` → `c4`   |
| Header text     | `#787878`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#1C1E22`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#181A1E`             | `tables.stripeBG` → `c43`  |
| Row hover       | `#262A2E`             | `tables.hoverBG` → `c3`    |
| Row text        | `#D8D0C0`             | `tables.fontColor` → `c58` |
| Border          | `#242628`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#2E3034` (`--border`), 8px height, **4px** radius
- Fill: status-colored or rust accent; `width` transition 300ms ease
- Track reads as machined channel — not lighter than the card face

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#1C1E22` (`--surface`)     |
| Radius       | `6px`                       |
| Label        | 11px, uppercase, `#787878`  |
| Value        | 28px, SemiBold, status-colored or `#D8D0C0` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#1C1E22`  | `#2E3034` | `#787878` |
| Hover   | `#262A2E`  | `#2E3034` | `#D8D0C0` |
| Active  | `#C87030`  | `#C87030` | `#111214` |

Active tab uses full rust fill with **gunmetal** text (`#111214`, theme `c1`) for contrast — the largest allowed accent field outside charts.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                    | colorRange Index | CSS Variable   |
|--------|-----------|--------------------------|------------------|----------------|
| 1      | `#C87030` | `oklch(0.58 0.12 48)`    | `[0][0]`         | `--chart-1`    |
| 2      | `#7A7820` | `oklch(0.48 0.08 100)`   | `[1][0]`         | `--chart-2`    |
| 3      | `#808080` | `oklch(0.55 0 0)`        | `[2][0]`         | `--chart-3`    |
| 4      | `#B03030` | `oklch(0.45 0.14 25)`    | `[3][0]`         | `--chart-4`    |
| 5      | `#A8A060` | `oklch(0.68 0.08 95)`    | `[4][0]`         | `--chart-5`    |
| 6      | `#505458` | `oklch(0.35 0.012 250)`  | `[5][0]`         | `--chart-6`    |

Series 1 is the **primary** rust accent; keep other series at moderate chroma so the chart stays industrial, not poster-dayglo.

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                     | Theme JSON Key                  |
|-------------------|-----------|---------------------------|---------------------------------|
| Positive / Up     | `#7A8830` | `oklch(0.52 0.10 120)`    | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#B03030` | `oklch(0.45 0.14 25)`     | `nameColorMap.NegativeColor`    |
| Total / Net       | `#808080` | `oklch(0.55 0 0)`         | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#D8D0C0` | `oklch(0.86 0.018 85)`    | —                               |
| Forecast          | `#C87030` | `oklch(0.58 0.12 48)`     | — (dashed stroke)               |
| Confidence Band   | `rgba(200,112,48,0.15)` | `oklch(0.58 0.12 48 / 0.15)` | — (area fill)            |
| Today Indicator   | `#B03030` | `oklch(0.45 0.14 25)`     | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#242628` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#2E3034` (`--border`), 1px
- Axis tick text: `#787878` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#0E1012` with `var(--shadow)`, **6px** radius, `#D8D0C0` text
- Legend text: `#787878`, 11px, Regular
- Active series: opacity 1.0; inactive: 0.3
- **Do not** push saturation to “dashboard neon” — if a series reads as candy-colored, reduce chroma or darken the hex

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow                 | Use                              |
|----------|--------------------|-------------------------|----------------------------------|
| Ground   | `#111214` (--bg)   | none                    | Page background                  |
| Raised   | `#1C1E22` (--surface) | `var(--shadow)`      | Cards, panels, containers        |
| Floating | `#262A2E`          | `var(--shadow-hover)`   | Dropdowns, tooltips, popovers    |
| Overlay  | `oklch(0 0 0 / 0.55)` | none                 | Modal backdrop                   |

Depth is a stack of **matte iron** steps plus **heavy black shadows** (0.35–0.45). Lightness steps are deliberate but subtle — the noir mood comes from weight, not glare.

### 6.2 Border Usage

- Prefer shadow over visible card rim; iron panels are separated by shadow and tone
- `1px solid var(--border-light)` for dividers and table separators
- `1px solid var(--border)` for inputs and focus rings
- Avoid radii **above 6px** on cards, inputs, and tabs — industrial means nearly square
- Status can use a **4px** left accent stripe on KPI cards (rivet-line emphasis)

---

## 7. Do's and Don'ts

### Do

- **Keep everything desaturated** — high chroma breaks the industrial / diesel-soot aesthetic
- Use **`c58`** for primary light text in theme JSON — **never `c60`**
- Use **`c59`** for secondary / de-emphasized native text where the JSON allows a second font color
- Use **`--text-primary` (`#D8D0C0`)** instead of `#FFFFFF`
- Use **slightly heavier shadows** — pure black at **~0.35–0.45** opacity for mass and command-center gravity
- Cap **border-radius at 6px** for cards, inputs, and tabs (badges may use 4px)
- Set `background: transparent` on pro-code app containers inside App Studio cards
- Test nav, headers, filters, and hero cards after import for contrast on `#0E1012` / `#111214`
- Apply `font-variant-numeric: tabular-nums` to operational numbers and KPIs

### Don't

- Use **`c60` (AUTOMATIC_COLOR)** for any font color on dark iron
- Use **pure white** (`#FFFFFF`) for body or chart label text
- Use **rounded corners larger than 6px** on structural surfaces — too soft for riveted iron
- Use **bright, neon, or candy** accent colors — they shatter the noir / propaganda discipline
- Use **light-tinted** status fills (high L) on dark cards
- Use **colored shadows** — they vanish on dark UI and read as toy UI
- Use **`transition: all`** — list properties explicitly
- Use **font-weight 700 / 900** except in rare one-off pro-code exceptions

---

## 8. Dark Mode Adaptation Notes

This theme is **native dark**. When applying it:

1. **App Studio theme JSON**: Map Section 2.1 slots to `c1`–`c60` positions as in Section 10. Replace any **`c60`** font color with **`c58`** (or **`c59`** for deliberate secondary copy) in cards, navigation, headers, forms, and components.

2. **Pro-code CSS**: Copy the `:root` block from Section 9.1. Mirror values in `COLORS` (Section 9.3). Keep the app shell `background: transparent` so card shadows and App Studio layout read correctly.

3. **Charts**: Use `--chart-1` … `--chart-6` for category series; use Section 5.2 for waterfalls, forecast lines, confidence bands, and reference lines.

4. **Light mode**: Dieselpunk is not a light theme. A light variant would need a new structural ramp (paper field, ink text), not a naive inversion of L values.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             #111214;
  --surface:        #1C1E22;
  --surface-hover:  #262A2E;
  --text-primary:   #D8D0C0;
  --text-secondary: #787878;
  --placeholder:    #505458;
  --border:         #2E3034;
  --border-light:   #242628;
  --accent:         #C87030;
  --accent-muted:   rgba(200, 112, 48, 0.15);
  --accent-hover:   #D88040;

  --nav-bg:         #0E1012;
  --header-bg:      #111214;

  --on-track:       #7A8830;
  --on-track-bg:    #1A2214;
  --at-risk:        #C87030;
  --at-risk-bg:     #2A1C14;
  --behind:         #B03030;
  --behind-bg:      #221616;
  --complete:       #8A9AA8;
  --complete-bg:    #14181C;

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.35),
    0px 1px 3px -1px oklch(0 0 0 / 0.42),
    0px 2px 6px 0px oklch(0 0 0 / 0.30);
  --shadow-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.40),
    0px 2px 6px -1px oklch(0 0 0 / 0.45),
    0px 4px 12px 0px oklch(0 0 0 / 0.35);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 6px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --chart-1: #C87030;
  --chart-2: #7A7820;
  --chart-3: #808080;
  --chart-4: #B03030;
  --chart-5: #A8A060;
  --chart-6: #505458;
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #111214    Card bg      → c2   #1C1E22
Hover bg     → c3   #262A2E    Nav bg       → c4   #0E1012
Primary text → c58  #D8D0C0    Secondary    → c59  #787878
Accent       → c29  #C87030    Accent hover → c30  #D88040
Border       → c46  #2E3034    Border light → c47  #242628
Font colors  → ALWAYS c58 / c59 as needed — NEVER c60
Card radius  → 6px (max for industrial surfaces)
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#C87030',
  secondary: '#7A7820',
  tertiary:  '#808080',
  surface:   '#1C1E22',
  bg:        '#111214',
  text:      '#D8D0C0',
  textMuted: '#787878',
  border:    '#2E3034',
  positive:  '#7A8830',
  negative:  '#B03030',
  series: ['#C87030', '#7A7820', '#808080', '#B03030', '#A8A060', '#505458']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: Surface `#1C1E22`, value `#D8D0C0` (28px SemiBold tabular-nums), label `#787878` (11px Light uppercase). Optional 4px left border in `--at-risk` or `--on-track`. Shadow only — no heavy borders.

**"Build a bar chart card"**: Series fills `COLORS.series`. Grid `#242628` at 0.5 opacity. Axis ticks `#787878`. Tooltip `#0E1012` background, `#D8D0C0` text, 6px radius, `var(--shadow)`.

**"Add a forecast line with confidence band"**: Solid history `--chart-1`; dashed forecast `--chart-1`; band fill `rgba(200,112,48,0.15)`. Reference “today” with `--behind` if it signals danger, or `--chart-4` for consistency with propaganda red.

**"Status strip for supply readiness"**: Badges use Section 2.2 backgrounds with olive / rust / red text. No neon greens; on-track stays olive `#7A8830`.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements colors, fonts, card styles ( **6px** radius), navigation, tables, tabs, and forms for the Dieselpunk system.

```json
{
  "name": "Dieselpunk",
  "colors": [
    { "index": 1, "value": "#111214", "tag": "PRIMARY" },
    { "index": 2, "value": "#1C1E22", "tag": "PRIMARY" },
    { "index": 3, "value": "#262A2E", "tag": "PRIMARY" },
    { "index": 4, "value": "#0E1012", "tag": "PRIMARY" },
    { "index": 5, "value": "#262A2E", "tag": "PRIMARY" },
    { "index": 6, "value": "#111214", "tag": "PRIMARY" },
    { "index": 7, "value": "#1C1E22", "tag": "PRIMARY" },
    { "index": 29, "value": "#C87030", "tag": "SECONDARY" },
    { "index": 30, "value": "#D88040", "tag": "SECONDARY" },
    { "index": 40, "value": "#000000", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#08090A", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#111214", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#181A1E", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#2E3034", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#505458", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#2E3034", "tag": "CUSTOM" },
    { "index": 47, "value": "#242628", "tag": "CUSTOM" },
    { "index": 48, "value": "#2E3034", "tag": "CUSTOM" },
    { "index": 49, "value": "#606468", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#787878", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#9A968E", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#B8B0A4", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#D8D0C0", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E8E4DC", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#D8D0C0", "tag": "FONT" },
    { "index": 59, "value": "#787878", "tag": "FONT" }
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
      "borderRadius": 6,
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
      "fontColor": { "type": "COLOR_REFERENCE", "index": 58 },
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
      "headerBackgroundColor": { "type": "COLOR_REFERENCE", "index": 4 },
      "headerFontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "rowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "alternateRowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 43 },
      "rowHoverBackgroundColor": { "type": "COLOR_REFERENCE", "index": 3 },
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
      "borderColor": { "type": "COLOR_REFERENCE", "index": 46 },
      "focusBorderColor": { "type": "COLOR_REFERENCE", "index": 29 },
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm navigation uses **`c58` / `c59`** for font colors — **never `c60`**. Confirm cards use **border radius 6** and drop shadow color **`c40`** (`#000000`).
