# Charcoal Ember Dark — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Warm orange · **Mood**: Confident, technical, authoritative

---

## 1. Visual Theme and Atmosphere

**Personality**: Executive control room. The UI recedes into charcoal shadow while data ignites in ember-orange. Nothing competes with the numbers.

**Density**: Medium-high. Cards pack tightly with 16px gaps; generous internal padding (20px) gives each card breathing room. The dark surface makes tight spacing feel open.

**Philosophy**: Restraint. Orange is earned — used only for primary data series, active states, and the single most important metric on each page. Everything else lives in warm grays. If more than 30% of visible pixels are orange, the design has failed.

**Atmosphere cues**:
- Surfaces feel like brushed carbon — warm undertone, never blue-cold
- Transitions are fast (150ms) and mechanical, not bouncy
- Shadows are deep and high-contrast (dark mode demands more opacity)
- Text is warm white (#D0CBC5), never pure white (#FFFFFF) — pure white vibrates on dark backgrounds

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#1E1C1A` | `oklch(0.15 0.005 60)`      | `c1`       | `--bg`              |
| Card Surface        | `#302C28` | `oklch(0.22 0.006 60)`      | `c2`       | `--surface`         |
| Surface Hover       | `#3A3632` | `oklch(0.26 0.008 60)`      | `c3`       | `--surface-hover`   |
| Primary Text        | `#D0CBC5` | `oklch(0.84 0.01 70)`       | `c58`      | `--text-primary`    |
| Secondary Text      | `#9A9590` | `oklch(0.65 0.008 60)`      | `c59`      | `--text-secondary`  |
| Border              | `#464240` | `oklch(0.30 0.006 60)`      | `c46`      | `--border`          |
| Border Light        | `#3A3836` | `oklch(0.26 0.005 60)`      | `c47`      | `--border-light`    |
| Accent              | `#E87A20` | `oklch(0.72 0.16 55)`       | `c29`      | `--accent`          |
| Accent Muted        | `#E87A2026` | `oklch(0.72 0.16 55 / 0.15)` | —        | `--accent-muted`    |
| Accent Hover        | `#F09040` | `oklch(0.77 0.14 60)`       | `c30`      | `--accent-hover`    |
| Nav Background      | `#252220` | `oklch(0.18 0.005 60)`      | `c4`       | `--nav-bg`          |
| Nav Active          | `#3A3632` | `oklch(0.26 0.008 60)`      | `c5`       | `--nav-active`      |
| Header Background   | `#1E1C1A` | `oklch(0.15 0.005 60)`      | `c6`       | `--header-bg`       |
| Input Background    | `#302C28` | `oklch(0.22 0.006 60)`      | `c7`       | `--input-bg`        |
| Input Border        | `#464240` | `oklch(0.30 0.006 60)`      | `c48`      | `--input-border`    |
| Tab Default BG      | `#302C28` | `oklch(0.22 0.006 60)`      | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#E87A20` | `oklch(0.72 0.16 55)`       | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#252220` | `oklch(0.18 0.005 60)`      | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#2A2724` | `oklch(0.20 0.005 60)`      | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#3A3632` | `oklch(0.26 0.008 60)`      | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#0A0908` | `oklch(0.07 0.003 60)`      | `c40`      | —                   |
| Grayscale 2         | `#141210` | `oklch(0.12 0.004 60)`      | `c41`      | —                   |
| Grayscale 3         | `#1E1C1A` | `oklch(0.15 0.005 60)`      | `c42`      | —                   |
| Grayscale 4         | `#302C28` | `oklch(0.22 0.006 60)`      | `c43`      | —                   |
| Grayscale 5         | `#464240` | `oklch(0.30 0.006 60)`      | `c44`      | —                   |
| Grayscale 6         | `#5C5856` | `oklch(0.40 0.006 60)`      | `c45`      | —                   |
| Grayscale 7         | `#7A7674` | `oklch(0.52 0.005 60)`      | `c49`      | —                   |
| Grayscale 8         | `#9A9590` | `oklch(0.65 0.008 60)`      | `c50`      | —                   |
| Grayscale 9         | `#B0ACA8` | `oklch(0.73 0.006 60)`      | `c51`      | —                   |
| Grayscale 10        | `#D0CBC5` | `oklch(0.84 0.01 70)`       | `c52`      | —                   |
| Grayscale 11        | `#E0DCD8` | `oklch(0.89 0.006 60)`      | `c53`      | —                   |
| Grayscale 12        | `#F0EDEA` | `oklch(0.95 0.004 60)`      | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#71B798` | `#1E2E24`  | `#71B798` | `--on-track`     |
| At Risk  | `#E87A20` | `#2E2218`  | `#E87A20` | `--at-risk`      |
| Behind   | `#D06050` | `#2E1C1A`  | `#D06050` | `--behind`       |
| Complete | `#7AA0C0` | `#1A2430`  | `#7AA0C0` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.18) with bright text (the primary color itself). Never use light-tinted badge backgrounds on dark surfaces.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.25),
  0px 1px 3px -1px oklch(0 0 0 / 0.35),
  0px 2px 6px 0px oklch(0 0 0 / 0.20);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.30),
  0px 2px 6px -1px oklch(0 0 0 / 0.40),
  0px 4px 12px 0px oklch(0 0 0 / 0.25);
```

Shadow color is pure black at higher opacity than the light theme (0.20–0.40 vs 0.04–0.08). On dark surfaces, colored shadows disappear — only opacity creates separation.

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
- **Never use Bold (700) or Black (900)** — they overpower the minimal aesthetic

### 3.4 Text Color Rules

Primary text is `#D0CBC5` (warm off-white), not `#FFFFFF`. Pure white causes eye strain on dark backgrounds and creates a cheap/unrefined feel. Secondary text at `#9A9590` creates a two-tier hierarchy without clashing with the warm charcoal surface.

Chart axis labels, tooltips, and legend text all use `--text-secondary` (`#9A9590`). Only the data values themselves use `--text-primary`.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#302C28`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#D0CBC5`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#E87A20`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible border — depth comes from shadow alone. The card surface (`--surface`) is one step lighter than the page (`--bg`), creating natural layering.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#302C28`  | `#464240` | `#9A9590` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#3A3632`  | `#E87A20` | `#D0CBC5` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#E87A20`  | `#E87A20` | `#1E1C1A` | `--accent` / `--accent` / `--bg` |
| Disabled | `#252220`  | `#3A3836` | `#5C5856` | — |

Ghost/outline style by default. Border radius: 6px. Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property    | Value                     |
|-------------|---------------------------|
| Background  | `#302C28` (`--surface`)   |
| Border      | `#464240` (`--border`)    |
| Text        | `#D0CBC5` (`--text-primary`) |
| Placeholder | `#5C5856`                 |
| Focus border| `#E87A20` (`--accent`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint at L ~0.18 with hue from the status color
- Text: the status primary color itself (bright on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#252220`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#9A9590`             | `navigation.linkFontColor` → `c58`  |
| Active link text  | `#D0CBC5`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#E87A20`             | `navigation.activeColor` → `c29`    |
| Title text        | `#D0CBC5`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#3A3632`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference `c58`, never `c60`. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, causing invisible nav text on dark surfaces.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#1E1C1A`             | `headers.backgroundColor` → `c1` |
| Font color  | `#D0CBC5`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#252220`             | `tables.headerBG` → `c4`   |
| Header text     | `#9A9590`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#302C28`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#2A2724`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#3A3632`             | `tables.hoverBG` → `c3`    |
| Row text        | `#D0CBC5`             | `tables.fontColor` → `c58` |
| Border          | `#3A3836`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#464240` (`--border`), 8px height, 4px radius
- Fill: status-colored, `width` transition 300ms ease
- On dark backgrounds, the track is one shade lighter than the surface (not lighter than the border)

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#302C28` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 12px, uppercase, `#9A9590`  |
| Value        | 28px, SemiBold, status-colored or `#D0CBC5` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#302C28`  | `#464240` | `#9A9590` |
| Hover   | `#3A3632`  | `#464240` | `#D0CBC5` |
| Active  | `#E87A20`  | `#E87A20` | `#1E1C1A` |

Active tab uses full accent fill with dark text — the only place accent fills a large area.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#E87A20` | `oklch(0.72 0.15 55)`       | `[0][0]`         | `--c1`       |
| 2      | `#D4A040` | `oklch(0.76 0.12 70)`       | `[1][0]`         | `--c2`       |
| 3      | `#7A7674` | `oklch(0.55 0.010 60)`      | `[2][0]`         | `--c3`       |
| 4      | `#C06828` | `oklch(0.64 0.14 45)`       | `[3][0]`         | `--c4`       |
| 5      | `#E0C060` | `oklch(0.80 0.10 80)`       | `[4][0]`         | `--c5`       |
| 6      | `#5C5856` | `oklch(0.48 0.015 55)`      | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#71B798` | `oklch(0.75 0.12 155)`  | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#D06050` | `oklch(0.58 0.14 25)`   | `nameColorMap.NegativeColor`    |
| Total / Net       | `#9A9590` | `oklch(0.65 0.008 60)`  | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#D0CBC5` | `oklch(0.84 0.01 70)`   | —                               |
| Forecast          | `#E87A20` | `oklch(0.72 0.16 55)`   | — (dashed stroke)               |
| Confidence Band   | `#E87A2033` | `oklch(0.72 0.16 55 / 0.20)` | — (area fill)            |
| Today Indicator   | `#D06050` | `oklch(0.58 0.14 25)`   | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#3A3836` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#464240` (`--border`), 1px
- Axis tick text: `#9A9590` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#252220` with `--shadow`, 6px radius, `#D0CBC5` text
- Legend text: `#9A9590`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#1E1C1A` (--bg)   | none                 | Page background                  |
| Raised   | `#302C28` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#3A3632`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.50)` | none             | Modal backdrop                   |

Dark mode depth relies on surface lightness steps rather than shadow alone. Each tier is ~0.06 L higher than the previous. Shadows reinforce but do not create the hierarchy.

### 6.2 Border Usage

- Prefer shadow over border for card edges — shadows adapt to any background
- Use `1px solid var(--border-light)` only for explicit dividers (horizontal rules, table row separators)
- Use `1px solid var(--border)` for input outlines (accessibility requirement)
- Never use borders thicker than `2px` except for status indicators (left accent borders on cards)

---

## 7. Do's and Don'ts

### Do

- Use `c58` for all font color references in the App Studio theme JSON — never `c60`
- Keep accent (orange) usage under 30% of visible area per page
- Use `--text-primary` (`#D0CBC5` warm off-white) instead of `#FFFFFF`
- Set `background: transparent` on pro-code app containers embedded in App Studio cards
- Use three-layer shadows with pure black at higher opacity (0.20–0.40)
- Test every native element (hero cards, filters, nav) for text visibility after theme application
- Apply `font-variant-numeric: tabular-nums` to all dynamic numbers

### Don't

- Use `c60` (AUTOMATIC_COLOR) for any font color — it defaults to dark text on dark backgrounds
- Use pure white (`#FFFFFF`) for text — it vibrates and feels cheap on dark surfaces
- Use light-tinted status badge backgrounds (L > 0.80) — they look washed out on dark cards
- Apply the light theme's border colors — they're too light and disappear on dark surfaces
- Use `transition: all` — specify exact properties
- Use font-weight 700 or 900 — too heavy for the minimal aesthetic
- Place colored shadows — they disappear on dark surfaces; use pure black only
- Use warm hue offsets (H 50–80) for cool-data series — the warm charcoal base already adds warmth; let data series hues stay honest

---

## 8. Dark Mode Adaptation Notes

This is already a dark theme. When an agent encounters a request to apply this theme:

1. **App Studio Native Theme**: Apply colors from the Slot Mapping Table (Section 2.1) to the corresponding `c1`–`c60` positions. Replace every `c60` reference in `cards[].fontColor`, `navigation[]*FontColor`, `headers[].fontColor`, and `components[]*FontColor` with `c58`.

2. **Pro-Code CSS**: Copy the full `--bg` through `--accent-muted` block from Section 2.1 into the app's `:root`. Set the `COLORS` object in `app.js` from these values. Use `background: transparent` on the app container.

3. **Chart Colors**: Map `--c1` through `--c6` into the Recharts/Chart.js color array. Apply semantic chart colors (Section 5.2) for goal lines, forecast, confidence bands, and waterfall segments.

4. **If reversing to light mode**: Do NOT simply invert L values. Use the light theme's `domo-app-theme` structural colors and a light palette from `color-palettes.md`. Dark-to-light is a full theme swap, not an inversion.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.15 0.005 60);
  --surface:        oklch(0.22 0.006 60);
  --surface-hover:  oklch(0.26 0.008 60);
  --text-primary:   oklch(0.84 0.01 70);
  --text-secondary: oklch(0.65 0.008 60);
  --border:         oklch(0.30 0.006 60);
  --border-light:   oklch(0.26 0.005 60);
  --accent:         oklch(0.72 0.16 55);
  --accent-muted:   oklch(0.72 0.16 55 / 0.15);
  --accent-hover:   oklch(0.77 0.14 60);

  --on-track:       oklch(0.75 0.12 155);
  --on-track-bg:    oklch(0.18 0.03 155);
  --at-risk:        oklch(0.72 0.16 55);
  --at-risk-bg:     oklch(0.18 0.03 55);
  --behind:         oklch(0.58 0.14 25);
  --behind-bg:      oklch(0.18 0.03 25);

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.25),
    0px 1px 3px -1px oklch(0 0 0 / 0.35),
    0px 2px 6px 0px oklch(0 0 0 / 0.20);
  --shadow-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.30),
    0px 2px 6px -1px oklch(0 0 0 / 0.40),
    0px 4px 12px 0px oklch(0 0 0 / 0.25);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --c1: oklch(0.72 0.15 55);
  --c2: oklch(0.76 0.12 70);
  --c3: oklch(0.55 0.010 60);
  --c4: oklch(0.64 0.14 45);
  --c5: oklch(0.80 0.10 80);
  --c6: oklch(0.48 0.015 55);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #1E1C1A    Card bg      → c2   #302C28
Hover bg     → c3   #3A3632    Nav bg       → c4   #252220
Primary text → c58  #D0CBC5    Secondary    → c59  #9A9590
Accent       → c29  #E87A20    Border       → c46  #464240
Font colors  → ALWAYS c58, NEVER c60
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#E87A20',
  secondary: '#D4A040',
  tertiary:  '#7A7674',
  surface:   '#302C28',
  bg:        '#1E1C1A',
  text:      '#D0CBC5',
  textMuted: '#9A9590',
  border:    '#464240',
  positive:  '#71B798',
  negative:  '#D06050',
  series: ['#E87A20', '#D4A040', '#7A7674', '#C06828', '#E0C060', '#5C5856']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: Use `--surface` background, `--text-primary` for the value (28px SemiBold tabular-nums), `--text-secondary` for the label (11px Light uppercase). Status-colored left border (4px). No visible card border — shadow only.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow pattern from the `app-studio-pro-code` skill's Banner Background Patterns section. Set text to `--text-primary`, gradient start from `--surface`, accent glow from `--accent-muted`.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fill array. `CartesianGrid` stroke `#3A3836` opacity 0.5. `XAxis`/`YAxis` tick fill `#9A9590`. Tooltip with `#252220` bg and `#D0CBC5` text. `ResponsiveContainer` at 100% width.

**"Add a forecast line with confidence band"**: `ComposedChart` with `Line` for historical (solid `--c1`), `Line` for forecast (dashed `--c1` strokeDasharray="6 4"), `Area` for confidence band (`--accent-muted` fill, no stroke). `ReferenceLine` at today's date with `--behind` stroke (dashed). Toggle the band via a `.confidence-toggle` button.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements all colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Charcoal Ember Dark",
  "colors": [
    { "index": 1, "value": "#1E1C1A", "tag": "PRIMARY" },
    { "index": 2, "value": "#302C28", "tag": "PRIMARY" },
    { "index": 3, "value": "#3A3632", "tag": "PRIMARY" },
    { "index": 4, "value": "#252220", "tag": "PRIMARY" },
    { "index": 5, "value": "#3A3632", "tag": "PRIMARY" },
    { "index": 6, "value": "#1E1C1A", "tag": "PRIMARY" },
    { "index": 7, "value": "#302C28", "tag": "PRIMARY" },
    { "index": 29, "value": "#E87A20", "tag": "SECONDARY" },
    { "index": 30, "value": "#F09040", "tag": "SECONDARY" },
    { "index": 40, "value": "#0A0908", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#141210", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#1E1C1A", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#302C28", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#464240", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#5C5856", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#464240", "tag": "CUSTOM" },
    { "index": 47, "value": "#3A3836", "tag": "CUSTOM" },
    { "index": 48, "value": "#464240", "tag": "CUSTOM" },
    { "index": 49, "value": "#7A7674", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#9A9590", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B0ACA8", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#D0CBC5", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E0DCD8", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F0EDEA", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#D0CBC5", "tag": "FONT" },
    { "index": 59, "value": "#9A9590", "tag": "FONT" }
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
      "borderRadius": 6,
      "font": { "type": "FONT_REFERENCE", "index": 3 }
    }
  ]
}
```

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Then verify all navigation and header font colors show `c58` (not `c60`).
