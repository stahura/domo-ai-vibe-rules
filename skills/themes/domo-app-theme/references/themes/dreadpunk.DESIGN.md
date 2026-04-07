# Dreadpunk — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Deep crimson / blood · **Mood**: Victorian gothic horror, pre-20th-century dread, candlelit studies, ink-stained manuscripts

---

## 1. Visual Theme and Atmosphere

**Personality**: Candlelit study of a Victorian occultist. The UI reads like a ledger bound in worn leather — heavy, intimate, and uneasy. Data is not “friendly”; it is *witnessed*.

**Density**: Medium-high. Cards sit in a 16px grid with 20px interior padding so dense risk and audit content stays legible without feeling clinical.

**Philosophy**: Crimson is *ink* — reserved for danger, risk, critical thresholds, and the few signals that must scream. Structural surfaces stay nearly achromatic (chroma < 0.10) so the accent reads as blood on parchment, not as a brand sticker. If crimson floods the canvas, the dread collapses into noise.

**Atmosphere cues**:
- Everything feels ancient, heavy, and ominous — weathered, not glossy
- Red highlights danger, risk, and critical data; gold reads as tarnished reward or “stable but solemn”
- The desaturated palette makes the crimson accent feel like blood on parchment
- No bright colors — everything is muted, aged, weathered
- Shadows are deep and omnipresent (pure black, 0.30–0.45 opacity layers), creating a sense of enclosure
- Primary text is bone white (`#E0D8D0`), aged and warm — never pure `#FFFFFF`

**Best for**: Risk analytics, security monitoring, audit dashboards, compliance, insurance, incident tracking.

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#0E0808` | `oklch(0.08 0.02 15)`       | `c1`       | `--bg`              |
| Card Surface        | `#1A1010` | `oklch(0.12 0.015 15)`      | `c2`       | `--surface`         |
| Surface Hover       | `#241818` | `oklch(0.16 0.02 15)`       | `c3`       | `--surface-hover`   |
| Primary Text        | `#E0D8D0` | `oklch(0.88 0.012 55)`      | `c58`      | `--text-primary`    |
| Secondary Text      | `#807870` | `oklch(0.55 0.01 55)`       | `c59`      | `--text-secondary`  |
| Border              | `#2A1C1C` | `oklch(0.18 0.02 15)`       | `c46`      | `--border`          |
| Border Light        | `#221414` | `oklch(0.14 0.02 15)`       | `c47`      | `--border-light`    |
| Accent              | `#8B2020` | `oklch(0.42 0.14 20)`       | `c29`      | `--accent`          |
| Accent Muted        | `rgba(139,32,32,0.18)` | `oklch(0.42 0.14 20 / 0.18)` | —    | `--accent-muted`    |
| Accent Hover        | `#A02828` | `oklch(0.47 0.13 20)`       | `c30`      | `--accent-hover`    |
| Nav Background      | `#100A0A` | `oklch(0.09 0.015 15)`      | `c4`       | `--nav-bg`          |
| Nav Active          | `#241818` | `oklch(0.16 0.02 15)`       | `c5`       | `--nav-active`      |
| Header Background   | `#0E0808` | `oklch(0.08 0.02 15)`       | `c6`       | `--header-bg`       |
| Input Background    | `#1A1010` | `oklch(0.12 0.015 15)`      | `c7`       | `--input-bg`        |
| Input Border        | `#2A1C1C` | `oklch(0.18 0.02 15)`       | `c48`      | `--input-border`    |
| Tab Default BG      | `#1A1010` | `oklch(0.12 0.015 15)`      | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#8B2020` | `oklch(0.42 0.14 20)`       | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#100A0A` | `oklch(0.09 0.015 15)`      | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#151010` | `oklch(0.11 0.015 15)`      | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#241818` | `oklch(0.16 0.02 15)`       | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#050303` | `oklch(0.05 0.01 15)`       | `c40`      | —                   |
| Grayscale 2         | `#0A0606` | `oklch(0.07 0.012 15)`      | `c41`      | —                   |
| Grayscale 3         | `#0E0808` | `oklch(0.08 0.02 15)`       | `c42`      | —                   |
| Grayscale 4         | `#151010` | `oklch(0.11 0.015 15)`      | `c43`      | —                   |
| Grayscale 5         | `#1A1010` | `oklch(0.12 0.015 15)`      | `c44`      | —                   |
| Grayscale 6         | `#322424` | `oklch(0.22 0.02 15)`       | `c45`      | —                   |
| Grayscale 7         | `#504840` | `oklch(0.38 0.015 50)`      | `c49`      | —                   |
| Grayscale 8         | `#807870` | `oklch(0.55 0.01 55)`       | `c50`      | —                   |
| Grayscale 9         | `#A09890` | `oklch(0.68 0.012 55)`      | `c51`      | —                   |
| Grayscale 10        | `#E0D8D0` | `oklch(0.88 0.012 55)`      | `c52`      | —                   |
| Grayscale 11        | `#E8E2DC` | `oklch(0.91 0.008 55)`      | `c53`      | —                   |
| Grayscale 12        | `#F2ECE8` | `oklch(0.94 0.006 55)`      | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#A08840` | `#16140E`  | `#A08840` | `--on-track`     |
| At Risk  | `#8B2020` | `#1A0C0C`  | `#8B2020` | `--at-risk`      |
| Behind   | `#5C3A6A` | `#140E16`  | `#5C3A6A` | `--behind`       |
| Complete | `#B0A890` | `#151512`  | `#B0A890` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.12–0.14) with saturated text in the status hue. Never use light-tinted badge backgrounds on these surfaces.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.35),
  0px 1px 3px -1px oklch(0 0 0 / 0.40),
  0px 2px 6px 0px oklch(0 0 0 / 0.30);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.40),
  0px 2px 6px -1px oklch(0 0 0 / 0.45),
  0px 4px 12px 0px oklch(0 0 0 / 0.35);
```

Shadow color is **pure black** between **0.30 and 0.45** opacity (plus a subtle 1px outline ring). On near-black surfaces, colored shadows vanish — only opacity defines depth.

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** family for all font slots. No Serif or Monospace in this theme.

### 3.2 Type Scale with Slot Mapping

| Role                     | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra                                  |
|--------------------------|------|--------|--------------------|-----------------|----------------------------------------|
| Page title               | 22px | SemiBold | 600              | `f1`            | `text-wrap: balance`                   |
| Card / section titles    | 16px | SemiBold | 600              | `f2`            | `text-wrap: balance`                   |
| Body text / descriptions | 13px | Regular  | 400              | `f3`            | line-height 1.5, `text-wrap: pretty`   |
| Labels / captions        | 11px | Regular  | 400              | `f4`            | uppercase, `letter-spacing: 0.04em`    |
| Chart axis text          | 11px | Regular  | 400              | `f5`            | `fill` color, not CSS `color`          |
| Badges / status text     | 11px | SemiBold | 600              | `f6`            | only small text that gets weight       |
| KPI numbers              | 28px | SemiBold | 600              | `f7`            | `font-variant-numeric: tabular-nums`   |
| KPI labels               | 11px | Light    | 300              | `f8`            | uppercase, `letter-spacing: 0.04em`    |

### 3.3 Weight Rules

- **SemiBold (600)**: Headings, KPI values, active button labels, badges
- **Regular (400)**: Body text, chart axes, table cells, descriptions
- **Light (300)**: KPI labels, timeframe captions — recedes behind the data
- **Never use Bold (700) or Black (900)** — they break the candlelit restraint

### 3.4 Text Color Rules

Primary text is `#E0D8D0` (bone, aged), not `#FFFFFF`. Pure white glares against blood-adjacent surfaces and reads modern, not manuscript. Secondary text at `#807870` is ash on parchment — a clear hierarchy without introducing blue or green.

Chart axis labels, tooltips, and legend text use `--text-secondary` (`#807870`). Data values and titles use `--text-primary` unless intentionally status-colored.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#1A1010`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#E0D8D0`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `8px`                          | `ca1.borderRadius` = `8`      |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#8B2020`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible card border — separation comes from shadow and the single step from page (`--bg`) to surface (`--surface`). **8px** radius is slightly softened but still architecturally heavy.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#1A1010`  | `#2A1C1C` | `#807870` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#241818`  | `#8B2020` | `#E0D8D0` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#8B2020`  | `#8B2020` | `#0E0808` | `--accent` / `--accent` / `--bg` |
| Disabled | `#100A0A`  | `#221414` | `#504840` | — |

Ghost/outline by default. **Border radius: 8px**. Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property    | Value                     |
|-------------|---------------------------|
| Background  | `#1A1010` (`--surface`)   |
| Border      | `#2A1C1C` (`--border`)    |
| Text        | `#E0D8D0` (`--text-primary`) |
| Placeholder | `#504840`                 |
| Focus border| `#8B2020` (`--accent`)    |
| Radius      | `8px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint (L ~0.12–0.14) with hue from the status color
- Text: the status primary color (legible on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#100A0A`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#E0D8D0`             | `navigation.linkFontColor` → `c58`  |
| Active link text  | `#E0D8D0`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#8B2020`             | `navigation.activeColor` → `c29`    |
| Title text        | `#E0D8D0`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#241818`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58`**, never **`c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, which hides nav labels on these surfaces.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#0E0808`             | `headers.backgroundColor` → `c1` |
| Font color  | `#E0D8D0`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#100A0A`             | `tables.headerBG` → `c4`   |
| Header text     | `#807870`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#1A1010`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#151010`             | `tables.stripeBG` → `c43`  |
| Row hover       | `#241818`             | `tables.hoverBG` → `c3`    |
| Row text        | `#E0D8D0`             | `tables.fontColor` → `c58` |
| Border          | `#221414`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#2A1C1C` (`--border`), 8px height, 4px radius
- Fill: status-colored or `--accent` for indeterminate risk; transition `width` 300ms ease
- Track sits one readable step above the card surface, never lighter than bone text

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#1A1010` (`--surface`)     |
| Radius       | `8px`                       |
| Label        | 12px, uppercase, `#807870`  |
| Value        | 28px, SemiBold, status-colored or `#E0D8D0` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#1A1010`  | `#2A1C1C` | `#807870` |
| Hover   | `#241818`  | `#2A1C1C` | `#E0D8D0` |
| Active  | `#8B2020`  | `#8B2020` | `#0E0808` |

Active tab uses full accent fill with near-page text (`--bg`) for contrast — high drama, use sparingly on a page.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#8B2020` | `oklch(0.42 0.14 20)`       | `[0][0]`         | `--c1`       |
| 2      | `#A08840` | `oklch(0.62 0.10 85)`       | `[1][0]`         | `--c2`       |
| 3      | `#707070` | `oklch(0.52 0.01 0)`        | `[2][0]`         | `--c3`       |
| 4      | `#5C3A6A` | `oklch(0.38 0.08 300)`      | `[3][0]`         | `--c4`       |
| 5      | `#B0A890` | `oklch(0.72 0.03 85)`       | `[4][0]`         | `--c5`       |
| 6      | `#383038` | `oklch(0.28 0.02 320)`      | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#A08840` | `oklch(0.62 0.10 85)`   | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#8B2020` | `oklch(0.42 0.14 20)`   | `nameColorMap.NegativeColor`    |
| Total / Net       | `#807870` | `oklch(0.55 0.01 55)`   | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#B0A890` | `oklch(0.72 0.03 85)`   | —                               |
| Forecast          | `#8B2020` | `oklch(0.42 0.14 20)`   | — (dashed stroke)               |
| Confidence Band   | `rgba(139,32,32,0.18)` | `oklch(0.42 0.14 20 / 0.18)` | — (area fill)            |
| Today Indicator   | `#5C3A6A` | `oklch(0.38 0.08 300)`  | —                               |

*Note*: Semantic “green/red” keys map to **tarnished gold** and **blood crimson** — no structural blue or green, consistent with Victorian horror and executive risk readouts.

### 5.3 Chart Styling Rules

- Grid lines: `#221414` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#2A1C1C` (`--border`), 1px
- Axis tick text: `#807870` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#100A0A` with `--shadow`, **8px** radius, `#E0D8D0` text
- Legend text: `#807870`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#0E0808` (--bg)   | none                 | Page background                  |
| Raised   | `#1A1010` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#241818`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.55)` | none             | Modal backdrop                   |

Hierarchy comes from small lightness steps on ruddy near-black bases, reinforced by **pure black** shadows at **0.30–0.45** opacity — never colored shadow.

### 6.2 Border Usage

- Prefer shadow over visible card edges
- Use `1px solid var(--border-light)` for dividers and subtle table separation
- Use `1px solid var(--border)` for input outlines (focus + accessibility)
- Avoid borders thicker than `2px` except deliberate status rails (e.g. 4px left accent on incident cards)

---

## 7. Do's and Don'ts

### Do

- Keep structural colors **deeply desaturated** — target **chroma < 0.10** for surfaces, borders, and neutral text tiers
- Use **crimson (`#8B2020`) only** for danger, risk, critical alerts, and primary emphasis — it carries inherent narrative weight
- Use **`c58`** for all explicit font color references in App Studio theme JSON — **never `c60`**
- Use **`8px` border-radius** on cards, buttons, inputs, and tabs — softer than a blade, still heavy
- Use `--text-primary` (`#E0D8D0` bone) instead of `#FFFFFF`
- Set `background: transparent` on pro-code app containers embedded in App Studio cards
- Stack **three-layer shadows** with **pure black** between **0.30 and 0.45** opacity
- Test hero cards, filters, and nav after theme apply — verify no “invisible” text from automatic dark defaults
- Apply `font-variant-numeric: tabular-nums` to live metrics and incident counts

### Don't

- Use **`c60`** (AUTOMATIC_COLOR) for any font color — it yields dark text on dark grounds
- Use **blue or green** in **structural** UI (nav, headers, forms, table chrome) — it breaks Victorian horror and reads as unrelated SaaS chrome
- Use **bright or cheerful** accents — they contradict dread, age, and enclosure
- Use **pure white** (`#FFFFFF`) for body text — it flattens the manuscript palette
- Use **light-tinted** status badge fills (high L) — they look like stickers on waxed wood
- Use **`transition: all`** — list exact properties
- Use font-weight **700** or **900**
- Use **colored** shadows — they disappear on these surfaces; **pure black only**

---

## 8. Dark Mode Adaptation Notes

This is a native **dark** theme. When applying it:

1. **App Studio Native Theme**: Map Section 2.1 slots to `c1`–`c60` as in the JSON below. Replace every `c60` reference in `cards[].fontColor`, `navigation.*FontColor`, `headers[].fontColor`, and `components.*FontColor` with **`c58`**.

2. **Pro-Code CSS**: Copy the `--bg` through chart `--c6` custom properties from Section 9.1 into `:root`. Mirror values in the `COLORS` object in `app.js`. Keep the app shell `background: transparent` when embedded in App Studio.

3. **Chart Colors**: Pipe `--c1`–`c6` into the series array. Use Section 5.2 for waterfalls, forecast overlays, and reference lines — **gold / crimson / bruise purple**, not corporate green-blue.

4. **If a stakeholder asks for “light mode”**: Do not invert L channels. Perform a full palette swap using a dedicated light design system. Dreadpunk is optically tuned for candlelit darkness.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.08 0.02 15);
  --surface:        oklch(0.12 0.015 15);
  --surface-hover:  oklch(0.16 0.02 15);
  --text-primary:   oklch(0.88 0.012 55);
  --text-secondary: oklch(0.55 0.01 55);
  --border:         oklch(0.18 0.02 15);
  --border-light:   oklch(0.14 0.02 15);
  --accent:         oklch(0.42 0.14 20);
  --accent-muted:   oklch(0.42 0.14 20 / 0.18);
  --accent-hover:   oklch(0.47 0.13 20);

  --on-track:       oklch(0.62 0.10 85);
  --on-track-bg:    oklch(0.14 0.02 85);
  --at-risk:        oklch(0.42 0.14 20);
  --at-risk-bg:     oklch(0.14 0.04 20);
  --behind:         oklch(0.38 0.08 300);
  --behind-bg:      oklch(0.14 0.03 300);
  --complete:       oklch(0.72 0.03 85);
  --complete-bg:    oklch(0.12 0.01 55);

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.35),
    0px 1px 3px -1px oklch(0 0 0 / 0.40),
    0px 2px 6px 0px oklch(0 0 0 / 0.30);
  --shadow-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.40),
    0px 2px 6px -1px oklch(0 0 0 / 0.45),
    0px 4px 12px 0px oklch(0 0 0 / 0.35);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 8px;
  --radius-btn: 8px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --c1: oklch(0.42 0.14 20);
  --c2: oklch(0.62 0.10 85);
  --c3: oklch(0.52 0.01 0);
  --c4: oklch(0.38 0.08 300);
  --c5: oklch(0.72 0.03 85);
  --c6: oklch(0.28 0.02 320);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #0E0808    Card bg      → c2   #1A1010
Hover bg     → c3   #241818    Nav bg       → c4   #100A0A
Primary text → c58  #E0D8D0    Secondary    → c59  #807870
Accent       → c29  #8B2020    Border       → c46  #2A1C1C
Font colors  → ALWAYS c58, NEVER c60
Radius       → 8px cards / buttons / forms / tabs
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#8B2020',
  secondary: '#A08840',
  tertiary:  '#707070',
  surface:   '#1A1010',
  bg:        '#0E0808',
  text:      '#E0D8D0',
  textMuted: '#807870',
  border:    '#2A1C1C',
  positive:  '#A08840',
  negative:  '#8B2020',
  series: ['#8B2020', '#A08840', '#707070', '#5C3A6A', '#B0A890', '#383038']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: Surfaces on `--surface`, values at 28px SemiBold `tabular-nums` in `--text-primary` or status hues. Labels 11px Light uppercase `--text-secondary`. Optional 4px left rail in `--accent` only for critical KPIs. Shadow only — no card border.

**"Build a security incident timeline"**: Use series `--c1` (open), `--c4` (contained), `--c3` (informational). Today marker `--behind`. Tooltip `--nav-bg` with `--shadow` and bone text.

**"Build a compliance bar chart"**: Recharts `BarChart` with `COLORS.series`. `CartesianGrid` stroke `#221414` @ 0.5 opacity. Axes tick fill `#807870`. Tooltip `#100A0A` / `#E0D8D0`.

**"Add a forecast band"**: Historical solid `--c1`; forecast dashed `--c1`; band fill `var(--accent-muted)`. No teal confidence halos.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements all colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Dreadpunk",
  "colors": [
    { "index": 1, "value": "#0E0808", "tag": "PRIMARY" },
    { "index": 2, "value": "#1A1010", "tag": "PRIMARY" },
    { "index": 3, "value": "#241818", "tag": "PRIMARY" },
    { "index": 4, "value": "#100A0A", "tag": "PRIMARY" },
    { "index": 5, "value": "#241818", "tag": "PRIMARY" },
    { "index": 6, "value": "#0E0808", "tag": "PRIMARY" },
    { "index": 7, "value": "#1A1010", "tag": "PRIMARY" },
    { "index": 29, "value": "#8B2020", "tag": "SECONDARY" },
    { "index": 30, "value": "#A02828", "tag": "SECONDARY" },
    { "index": 40, "value": "#050303", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0A0606", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#0E0808", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#151010", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#1A1010", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#322424", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#2A1C1C", "tag": "CUSTOM" },
    { "index": 47, "value": "#221414", "tag": "CUSTOM" },
    { "index": 48, "value": "#2A1C1C", "tag": "CUSTOM" },
    { "index": 49, "value": "#504840", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#807870", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#A09890", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#E0D8D0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E8E2DC", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F2ECE8", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#E0D8D0", "tag": "FONT" },
    { "index": 59, "value": "#807870", "tag": "FONT" }
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
      "borderRadius": 8,
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
      "borderRadius": 8,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ],
  "navigation": [
    {
      "index": 1,
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 4 },
      "titleFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
      "linkFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
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
      "borderRadius": 8,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm every navigation and header font color resolves to **`c58`** (not **`c60`**).
