# Steampunk — Domo App Studio Design System

> **Mode**: Dark (rich warm dark) · **Accent family**: Polished brass / copper · **Mood**: Victorian engineering meets brass machinery — gears, rivets, aged leather, copper pipes, sepia-toned instruments

**Best for**: Manufacturing, logistics, mechanical engineering, operations, heritage brands, historical data.

---

## 1. Visual Theme and Atmosphere

**Personality**: Victorian engineering control room. Surfaces read as aged leather and mahogany panels; brass reads as functional hardware — gauge bezels, pressure indicators, instrument trim — not ornamental glitter.

**Density**: Medium-high. Cards sit on a deep walnut ground with 16px grid gaps; internal card padding stays at 20px so dense operational dashboards still feel legible. Warm browns keep tight layouts from feeling cramped.

**Philosophy**: Brass is earned. Use `#C8A040` for primary series, active nav indicators, key CTAs, and the single most important KPI accent per view. Copper and bronze in the chart palette carry secondary stories. If brass dominates more than ~30% of visible area, the UI stops feeling like machinery and starts looking like costume.

**Atmosphere cues**:
- Depth over flat planes — subtle elevation (shadow + surface steps), not glassmorphism or neon flats
- Transitions run **180ms** (vs a typical 150ms) — slightly slower, deliberate, mechanical
- Shadows are pure black at **0.25–0.40** opacity in a three-layer stack (Section 2.3)
- Primary text is parchment `#E8DCC8` — **never** pure white (`#FFFFFF`); cream reads correct on warm dark wood tones

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                         | Theme Slot | CSS Variable        |
|---------------------|-----------|-------------------------------|------------|---------------------|
| Page Background     | `#141008` | `oklch(0.12 0.022 72)`        | `c1`       | `--bg`              |
| Card Surface        | `#221A10` | `oklch(0.18 0.028 68)`        | `c2`       | `--surface`         |
| Surface Hover       | `#2C2218` | `oklch(0.22 0.024 65)`        | `c3`       | `--surface-hover`   |
| Primary Text        | `#E8DCC8` | `oklch(0.90 0.024 88)`        | `c58`      | `--text-primary`    |
| Secondary Text      | `#8A7A60` | `oklch(0.58 0.045 72)`        | `c59`      | `--text-secondary`  |
| Border              | `#3A2E20` | `oklch(0.30 0.035 62)`        | `c46`      | `--border`          |
| Border Light        | `#2E2418` | `oklch(0.24 0.028 62)`        | `c47`      | `--border-light`    |
| Accent              | `#C8A040` | `oklch(0.72 0.13 78)`         | `c29`      | `--accent`          |
| Accent Muted        | `#C8A04026` | `oklch(0.72 0.13 78 / 0.15)` | —          | `--accent-muted`    |
| Accent Hover        | `#D8B050` | `oklch(0.78 0.12 82)`         | `c30`      | `--accent-hover`    |
| Nav Background      | `#181008` | `oklch(0.13 0.020 70)`        | `c4`       | `--nav-bg`          |
| Nav Active          | `#2C2218` | `oklch(0.22 0.024 65)`        | `c5`       | `--nav-active`      |
| Header Background   | `#141008` | `oklch(0.12 0.022 72)`        | `c6`       | `--header-bg`       |
| Input Background    | `#221A10` | `oklch(0.18 0.028 68)`        | `c7`       | `--input-bg`        |
| Input Border        | `#3A2E20` | `oklch(0.30 0.035 62)`        | `c48`      | `--input-border`    |
| Tab Default BG      | `#221A10` | `oklch(0.18 0.028 68)`        | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#C8A040` | `oklch(0.72 0.13 78)`         | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#181008` | `oklch(0.13 0.020 70)`        | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#1C160E` | `oklch(0.15 0.018 68)`        | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#2C2218` | `oklch(0.22 0.024 65)`        | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#050403` | `oklch(0.06 0.008 65)`        | `c40`      | —                   |
| Grayscale 2         | `#0E0A06` | `oklch(0.10 0.015 68)`        | `c41`      | —                   |
| Grayscale 3         | `#141008` | `oklch(0.12 0.022 72)`        | `c42`      | —                   |
| Grayscale 4         | `#221A10` | `oklch(0.18 0.028 68)`        | `c43`      | —                   |
| Grayscale 5         | `#3A2E20` | `oklch(0.30 0.035 62)`        | `c44`      | —                   |
| Grayscale 6         | `#524838` | `oklch(0.40 0.035 65)`        | `c45`      | —                   |
| Grayscale 7         | `#6A5E4C` | `oklch(0.50 0.038 68)`        | `c49`      | —                   |
| Grayscale 8         | `#8A7A60` | `oklch(0.58 0.045 72)`        | `c50`      | —                   |
| Grayscale 9         | `#B0A088` | `oklch(0.72 0.035 75)`        | `c51`      | —                   |
| Grayscale 10        | `#E8DCC8` | `oklch(0.90 0.024 88)`        | `c52`      | —                   |
| Grayscale 11        | `#F0E8D8` | `oklch(0.93 0.020 88)`        | `c53`      | —                   |
| Grayscale 12        | `#F8F2E8` | `oklch(0.96 0.016 88)`        | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#60A878` | `#1A2820`  | `#60A878` | `--on-track`     |
| At Risk  | `#D88030` | `#2A1E12`  | `#D88030` | `--at-risk`      |
| Behind   | `#C05040` | `#261818`  | `#C05040` | `--behind`       |
| Complete | `#A08050` | `#221A14`  | `#A08050` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.18) with bright text (the status primary). Never use light-tinted badge backgrounds on dark leather surfaces.

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

Shadow color is **pure black** at 0.20–0.40 opacity. On warm dark wood and leather tones, colored shadows read muddy; black opacity defines depth.

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** family for all font slots. Steampunk is conveyed through **color, texture (shadow), and brass accent discipline** — not display serifs in native slots.

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

- **SemiBold (600)**: Headings, KPI values, active button labels, badges
- **Regular (400)**: Body text, chart axes, table cells, descriptions
- **Light (300)**: KPI labels, timeframe captions — recedes behind the data
- **Never use Bold (700) or Black (900)** — they break the workshop / instrument-board balance

### 3.4 Text Color Rules

Primary text is `#E8DCC8` (parchment), not `#FFFFFF`. Pure white flares against mahogany and reads cheap next to brass. Secondary `#8A7A60` is weathered brass — use for axes, legends, helper copy, and de-emphasized table headers.

Chart axis labels, tooltips, and legend text use `--text-secondary` (`#8A7A60`). Data marks and values use `--text-primary` or series colors.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#221A10`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#E8DCC8`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `8px`                          | `ca1.borderRadius` = `8`      |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#C8A040`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible card border — separation comes from shadow and the step from page (`#141008`) to leather surface (`#221A10`). **At most two sharp (0-radius) corners in a single layout** — prefer **8px** radius everywhere else for a softer, worn, handled object feel (intentionally different from a default 10px system).

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#221A10`  | `#3A2E20` | `#8A7A60` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#2C2218`  | `#C8A040` | `#E8DCC8` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#C8A040`  | `#C8A040` | `#141008` | `--accent` / `--accent` / `--bg` |
| Disabled | `#181008`  | `#2E2418` | `#524838` | — |

Ghost/outline by default. Border radius: **6px** (controls stay slightly tighter than cards). Transition: `scale, background-color, border-color, box-shadow` at **180ms** ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property     | Value                     |
|--------------|---------------------------|
| Background   | `#221A10` (`--surface`)   |
| Border       | `#3A2E20` (`--border`)    |
| Text         | `#E8DCC8` (`--text-primary`) |
| Placeholder  | `#524838` (`--grayscale-6`) |
| Focus border | `#C8A040` (`--accent`)    |
| Radius       | `6px`                     |
| Font         | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint at L ~0.18 with hue from the status color (Section 2.2)
- Text: status primary color (bright on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius **`8px`** (match card softness) or `4px` only if the page already uses two sharp corners elsewhere — stay within the two-sharp-corner budget

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#181008`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#8A7A60`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#E8DCC8`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#C8A040`             | `navigation.activeColor` → `c29`    |
| Title text        | `#E8DCC8`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#2C2218`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58`** (or `c59` for default links as specified), **never `c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text and will disappear on dark nav.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#141008`             | `headers.backgroundColor` → `c1` |
| Font color  | `#E8DCC8`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#181008`             | `tables.headerBG` → `c4`   |
| Header text     | `#8A7A60`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#221A10`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#1C160E`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#2C2218`             | `tables.hoverBG` → `c3`    |
| Row text        | `#E8DCC8`             | `tables.fontColor` → `c58` |
| Border          | `#2E2418`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#3A2E20` (`--border`), 8px height, **8px** radius (or 4px if paired with sharp-corner exceptions)
- Fill: status-colored; `width` transition **300ms** ease
- Track reads as a machined groove — slightly darker than hover, not lighter than the card face

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#221A10` (`--surface`)     |
| Radius       | `8px`                       |
| Label        | 11px, uppercase, `#8A7A60`  |
| Value        | 28px, SemiBold, status-colored or `#E8DCC8` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#221A10`  | `#3A2E20` | `#8A7A60` |
| Hover   | `#2C2218`  | `#3A2E20` | `#E8DCC8` |
| Active  | `#C8A040`  | `#C8A040` | `#141008` |

Active tab is full brass fill with dark mahogany text — high-contrast and readable; reserve large accent fills for tabs and primary CTAs only.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                    | colorRange Index | CSS Variable |
|--------|-----------|--------------------------|------------------|--------------|
| 1      | `#C8A040` | `oklch(0.72 0.13 78)`    | `[0][0]`         | `--c1`       |
| 2      | `#B87040` | `oklch(0.62 0.12 55)`    | `[1][0]`         | `--c2`       |
| 3      | `#A08050` | `oklch(0.58 0.08 72)`    | `[2][0]`         | `--c3`       |
| 4      | `#7A7878` | `oklch(0.55 0.005 70)`   | `[3][0]`         | `--c4`       |
| 5      | `#D8C060` | `oklch(0.82 0.11 85)`    | `[4][0]`         | `--c5`       |
| 6      | `#5A5458` | `oklch(0.45 0.012 300)`  | `[5][0]`         | `--c6`       |

Brass is primary; copper and bronze carry secondary metrics; steam gray and iron cool the mix **within the metallic range** — not blue.

### 5.2 Semantic Chart Colors

| Role              | Hex         | OKLCH                     | Theme JSON Key                  |
|-------------------|-------------|---------------------------|---------------------------------|
| Positive / Up     | `#60A878`   | `oklch(0.68 0.11 150)`    | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#C05040`   | `oklch(0.55 0.14 25)`     | `nameColorMap.NegativeColor`    |
| Total / Net       | `#8A7A60`   | `oklch(0.58 0.045 72)`    | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#E8DCC8`   | `oklch(0.90 0.024 88)`    | —                               |
| Forecast          | `#C8A040`   | `oklch(0.72 0.13 78)`     | — (dashed stroke)               |
| Confidence Band   | `#C8A04026` | `oklch(0.72 0.13 78 / 0.15)` | — (area fill)                |
| Today Indicator   | `#D88030`   | `oklch(0.68 0.14 55)`     | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#2E2418` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#3A2E20` (`--border`), 1px
- Axis tick text: `#8A7A60` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#181008` with `--shadow`, **8px** radius, `#E8DCC8` text
- Legend text: `#8A7A60`, 11px, Regular
- Active/hover series: opacity 1.0; inactive: opacity 0.3

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface              | Shadow                | Use                              |
|----------|----------------------|------------------------|----------------------------------|
| Ground   | `#141008` (--bg)     | none                   | Page background                  |
| Raised   | `#221A10` (--surface) | `var(--shadow)`       | Cards, panels, containers        |
| Floating | `#2C2218`            | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.50)` | none                   | Modal backdrop                   |

Hierarchy is established by **warm brown lightness steps** (~0.06 L between tiers) and reinforced by black-opacity shadows — not by colored or neon glows.

### 6.2 Border Usage

- Prefer shadow over visible card edges; leather panels read as stacked slabs
- `1px solid var(--border-light)` for dividers and subtle table separators
- `1px solid var(--border)` for inputs and focus rings
- Avoid borders thicker than `2px` except intentional rivet / status accent bars (e.g. 4px left border in brass or status hue)

---

## 7. Do's and Don'ts

### Do

- Use **warm tones exclusively** for structural UI — mahogany, leather, oxidized copper borders, brass accent. No cool blues or greens in backgrounds, nav, headers, card chrome, or dividers.
- Use **`c58`** for all light-on-dark font color references in App Studio theme JSON — **never `c60`** (AUTOMATIC_COLOR reads as dark text on dark surfaces).
- Use **`#C8A040` brass** for data highlights, active nav indicators, focus rings, and primary series.
- Embrace **subtle depth** — layered shadows, surface steps, restrained borders — steampunk is workshop machinery, not flat Material cards.
- Use **three-layer shadows** with **pure black** at **0.25–0.40** cumulative opacity.
- Prefer **`8px` radius** on cards and major containers for a softer, worn object feel; keep **no more than two sharp corners** per view.
- Run motion at **~180ms** for hovers and state changes where the platform allows — deliberate, mechanical.
- Apply `font-variant-numeric: tabular-nums` to dynamic numbers.

### Don't

- Use **`c60`** for any font color on dark surfaces.
- Use **pure white** (`#FFFFFF`) for body or chart label text.
- Use **cool structural accents** (teal panels, blue nav, green dividers) — reserve green for **on-track / positive data** only.
- Default to **modern ultra-flat** UI (no shadow, no surface step) — it fights the brief.
- Use **light-tinted** status badge fills on dark cards.
- Use `transition: all` — list explicit properties.
- Use font-weight **700 / 900** on native theme fonts.
- Place **colored drop shadows** — they disappear or muddy on warm dark brown; use black opacity only.

---

## 8. Dark Mode Adaptation Notes

This theme is **native dark** (rich warm dark). When an agent applies it:

1. **App Studio Native Theme**: Map Section 2.1 slots to `c1`–`c60` as in Section 10. Replace any **`c60`** font references with **`c58`** (or `c59` for deliberately muted link text in nav).

2. **Pro-Code CSS**: Copy the `:root` custom properties from Section 9.1. Set the `COLORS` object in `app.js` from the same hex values. Use `background: transparent` on the app root when embedded in App Studio cards.

3. **Charts**: Map series hexes from Section 5.1 into Recharts / Chart.js color arrays. Use Section 5.2 for waterfall, forecast dashes, and confidence bands (`--accent-muted`).

4. **Light mode**: Do not invert L channels. A light steampunk variant would need new page/surface/text slots (parchment page, ink text) — treat as a separate theme file.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.12 0.022 72);
  --surface:        oklch(0.18 0.028 68);
  --surface-hover:  oklch(0.22 0.024 65);
  --text-primary:   oklch(0.90 0.024 88);
  --text-secondary: oklch(0.58 0.045 72);
  --border:         oklch(0.30 0.035 62);
  --border-light:   oklch(0.24 0.028 62);
  --accent:         oklch(0.72 0.13 78);
  --accent-muted:   oklch(0.72 0.13 78 / 0.15);
  --accent-hover:   oklch(0.78 0.12 82);

  --on-track:       oklch(0.68 0.11 150);
  --on-track-bg:    oklch(0.18 0.03 150);
  --at-risk:        oklch(0.68 0.14 55);
  --at-risk-bg:     oklch(0.18 0.03 55);
  --behind:         oklch(0.55 0.14 25);
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
  --radius-card: 8px;
  --radius-btn: 6px;
  --radius-badge: 8px;
  --transition-ui: 180ms ease-out;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --c1: oklch(0.72 0.13 78);
  --c2: oklch(0.62 0.12 55);
  --c3: oklch(0.58 0.08 72);
  --c4: oklch(0.55 0.005 70);
  --c5: oklch(0.82 0.11 85);
  --c6: oklch(0.45 0.012 300);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #141008    Card bg      → c2   #221A10
Hover bg     → c3   #2C2218    Nav bg       → c4   #181008
Primary text → c58  #E8DCC8    Secondary    → c59  #8A7A60
Accent       → c29  #C8A040    Border       → c46  #3A2E20
Font colors  → ALWAYS c58 (or c59 for muted links), NEVER c60
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#C8A040',
  secondary: '#B87040',
  tertiary:  '#A08050',
  surface:   '#221A10',
  bg:        '#141008',
  text:      '#E8DCC8',
  textMuted: '#8A7A60',
  border:    '#3A2E20',
  positive:  '#60A878',
  negative:  '#C05040',
  series: ['#C8A040', '#B87040', '#A08050', '#7A7878', '#D8C060', '#5A5458']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: `--surface` background, `--text-primary` values (28px SemiBold tabular-nums), `--text-secondary` labels (11px Light uppercase). Optional 4px **brass** or status left rail. Shadow only — no card border.

**"Build a bar chart card"**: Series fills from `COLORS.series`. Grid stroke `#2E2418` at 0.5 opacity. Axis ticks `#8A7A60`. Tooltip `#181008` background, `#E8DCC8` text, 8px radius.

**"Add forecast + confidence band"**: Solid line `--c1` (`#C8A040`), forecast dashed same hue, area fill `rgba(200,160,64,0.15)`. Today marker `--at-risk` (`#D88030`) dashed if it must read as "attention" without implying failure.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the Steampunk palette, **8px** card radius, fonts, navigation ( **`c58` / `c59` only — never `c60`** ), headers, tables, tabs, and forms.

```json
{
  "name": "Steampunk",
  "colors": [
    { "index": 1, "value": "#141008", "tag": "PRIMARY" },
    { "index": 2, "value": "#221A10", "tag": "PRIMARY" },
    { "index": 3, "value": "#2C2218", "tag": "PRIMARY" },
    { "index": 4, "value": "#181008", "tag": "PRIMARY" },
    { "index": 5, "value": "#2C2218", "tag": "PRIMARY" },
    { "index": 6, "value": "#141008", "tag": "PRIMARY" },
    { "index": 7, "value": "#221A10", "tag": "PRIMARY" },
    { "index": 11, "value": "#1C160E", "tag": "PRIMARY" },
    { "index": 29, "value": "#C8A040", "tag": "SECONDARY" },
    { "index": 30, "value": "#D8B050", "tag": "SECONDARY" },
    { "index": 40, "value": "#050403", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0E0A06", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#141008", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#221A10", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#3A2E20", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#524838", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#3A2E20", "tag": "CUSTOM" },
    { "index": 47, "value": "#2E2418", "tag": "CUSTOM" },
    { "index": 48, "value": "#3A2E20", "tag": "CUSTOM" },
    { "index": 49, "value": "#6A5E4C", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#8A7A60", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B0A088", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#E8DCC8", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#F0E8D8", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F8F2E8", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#E8DCC8", "tag": "FONT" },
    { "index": 59, "value": "#8A7A60", "tag": "FONT" }
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
      "headerBackgroundColor": { "type": "COLOR_REFERENCE", "index": 4 },
      "headerFontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "rowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "alternateRowBackgroundColor": { "type": "COLOR_REFERENCE", "index": 11 },
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

> **To import**: App Studio → Theme Editor → Import Theme JSON → paste this object. Confirm navigation, headers, cards, tables, tabs, and forms use **`c58`/`c59`** for text — **never `c60`**.
