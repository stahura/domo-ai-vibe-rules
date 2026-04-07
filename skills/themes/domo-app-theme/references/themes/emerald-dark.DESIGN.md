# Emerald Dark — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Green / emerald · **Mood**: Precision, technical, growth

---

## 1. Visual Theme and Atmosphere

**Personality**: Command center for growth. The UI reads like a calm operations deck: cool gray-greens recede, and emerald marks what matters right now.

**Density**: Medium-high. Cards pack tightly with 16px gaps; generous internal padding (20px) gives each card breathing room. The deep green-gray base makes tight spacing feel controlled, not cramped.

**Philosophy**: Restraint. Green is clinical and precise — reserved for primary data series, active controls, and the single most important signal on each surface. Chrome, labels, and scaffolding stay in desaturated gray-greens. If more than roughly 30% of visible pixels read as saturated emerald, the design has failed.

**Atmosphere cues**:
- Surfaces feel like polished obsidian with a faint green mineral vein — depth without neon
- Transitions are fast (150ms) and crisp, not elastic
- Shadows use pure black at moderate opacity; colored shadows do not read on dark bases
- Primary text is soft warm-off-white (`#EFF5F2`), never pure white (`#FFFFFF`) — pure white flares and feels unfinished on dark green-gray

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#1A2420` | `oklch(0.14 0.012 155)`     | `c1`       | `--bg`              |
| Card Surface        | `#243530` | `oklch(0.20 0.016 155)`     | `c2`       | `--surface`         |
| Surface Hover       | `#2C3F38` | `oklch(0.24 0.018 155)`     | `c3`       | `--surface-hover`   |
| Primary Text        | `#EFF5F2` | `oklch(0.95 0.005 155)`     | `c58`      | `--text-primary`    |
| Secondary Text      | `#8FAA9C` | `oklch(0.70 0.015 155)`     | `c59`      | `--text-secondary`  |
| Border              | `#3A4D44` | `oklch(0.30 0.012 155)`     | `c46`      | `--border`          |
| Border Light        | `#2F3F37` | `oklch(0.25 0.010 155)`     | `c47`      | `--border-light`    |
| Accent              | `#2DD47A` | `oklch(0.72 0.18 155)`      | `c29`      | `--accent`          |
| Accent Muted        | `#2DD47A26` | `oklch(0.72 0.18 155 / 0.15)` | —        | `--accent-muted`    |
| Accent Hover        | `#3DD383` | `oklch(0.77 0.17 155)`      | `c30`      | `--accent-hover`    |
| Nav Background      | `#1E2B26` | `oklch(0.17 0.014 155)`     | `c4`       | `--nav-bg`          |
| Nav Active          | `#2C3F38` | `oklch(0.24 0.018 155)`     | `c5`       | `--nav-active`      |
| Header Background   | `#1A2420` | `oklch(0.14 0.012 155)`     | `c6`       | `--header-bg`       |
| Input Background    | `#243530` | `oklch(0.20 0.016 155)`     | `c7`       | `--input-bg`        |
| Input Border        | `#3A4D44` | `oklch(0.30 0.012 155)`     | `c48`      | `--input-border`    |
| Tab Default BG      | `#243530` | `oklch(0.20 0.016 155)`     | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#2DD47A` | `oklch(0.72 0.18 155)`      | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#1E2B26` | `oklch(0.17 0.014 155)`     | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#1F2A26` | `oklch(0.17 0.013 155)`     | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#2C3F38` | `oklch(0.24 0.018 155)`     | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#050807` | `oklch(0.08 0.006 155)`     | `c40`      | —                   |
| Grayscale 2         | `#0E1713` | `oklch(0.12 0.009 155)`     | `c41`      | —                   |
| Grayscale 3         | `#1A2420` | `oklch(0.14 0.012 155)`     | `c42`      | —                   |
| Grayscale 4         | `#243530` | `oklch(0.20 0.016 155)`     | `c43`      | —                   |
| Grayscale 5         | `#3A4D44` | `oklch(0.30 0.012 155)`     | `c44`      | —                   |
| Grayscale 6         | `#4F6259` | `oklch(0.40 0.012 155)`     | `c45`      | —                   |
| Grayscale 7         | `#6E8379` | `oklch(0.52 0.012 155)`     | `c49`      | —                   |
| Grayscale 8         | `#8A9E94` | `oklch(0.65 0.014 155)`     | `c50`      | —                   |
| Grayscale 9         | `#A3B5AB` | `oklch(0.73 0.012 155)`     | `c51`      | —                   |
| Grayscale 10        | `#C5D5CC` | `oklch(0.84 0.008 155)`     | `c52`      | —                   |
| Grayscale 11        | `#DCE9E2` | `oklch(0.89 0.006 155)`     | `c53`      | —                   |
| Grayscale 12        | `#F2F8F5` | `oklch(0.96 0.004 155)`     | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#59C886` | `#102719`  | `#59C886` | `--on-track`     |
| At Risk  | `#F4A34B` | `#2F1D0B`  | `#F4A34B` | `--at-risk`      |
| Behind   | `#D48AAD` | `#25151D`  | `#D48AAD` | `--behind`       |
| Complete | `#2BB3B9` | `#002022`  | `#2BB3B9` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.22–0.25) with bright text (the primary color itself). Never use light-tinted badge backgrounds on dark surfaces.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.20),
  0px 1px 3px -1px oklch(0 0 0 / 0.30),
  0px 2px 6px 0px oklch(0 0 0 / 0.20);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.30),
  0px 2px 6px -1px oklch(0 0 0 / 0.40),
  0px 4px 12px 0px oklch(0 0 0 / 0.25);
```

Shadow color is pure black at higher opacity than a typical light theme. On dark surfaces, colored shadows disappear — only opacity creates separation.

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

Primary text is `#EFF5F2` (soft warm off-white), not `#FFFFFF`. Pure white causes glare on dark green-gray backgrounds and reads as unfinished. Secondary text at `#8FAA9C` establishes hierarchy without competing with emerald accents.

Chart axis labels, tooltips, and legend text all use `--text-secondary` (`#8FAA9C`). Only the data values themselves use `--text-primary`.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#243530`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#EFF5F2`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#2DD47A`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible border — depth comes from shadow alone. The card surface (`--surface`) is one step lighter than the page (`--bg`), creating natural layering.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#243530`  | `#3A4D44` | `#8FAA9C` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#2C3F38`  | `#2DD47A` | `#EFF5F2` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#2DD47A`  | `#2DD47A` | `#1A2420` | `--accent` / `--accent` / `--bg` |
| Disabled | `#1E2B26`  | `#2F3F37` | `#4F6259` | — |

Ghost/outline style by default. Border radius: 6px. Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property    | Value                     |
|-------------|---------------------------|
| Background  | `#243530` (`--surface`)   |
| Border      | `#3A4D44` (`--border`)    |
| Text        | `#EFF5F2` (`--text-primary`) |
| Placeholder | `#4F6259`                 |
| Focus border| `#2DD47A` (`--accent`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint at L ~0.22–0.25 with hue from the status color
- Text: the status primary color itself (bright on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#1E2B26`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#8FAA9C`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#EFF5F2`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#2DD47A`             | `navigation.activeColor` → `c29`    |
| Title text        | `#EFF5F2`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#2C3F38`             | —                                    |

**Critical**: Navigation font colors must use `c58` / `c59` — never `c60`. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, causing invisible nav text on dark surfaces. Use `c59` for default links and `c58` for active links (and titles).

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#1A2420`             | `headers.backgroundColor` → `c1` |
| Font color  | `#EFF5F2`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#1E2B26`             | `tables.headerBG` → `c4`   |
| Header text     | `#8FAA9C`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#243530`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#1F2A26`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#2C3F38`             | `tables.hoverBG` → `c3`    |
| Row text        | `#EFF5F2`             | `tables.fontColor` → `c58` |
| Border          | `#2F3F37`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#3A4D44` (`--border`), 8px height, 4px radius
- Fill: status-colored, `width` transition 300ms ease
- On dark backgrounds, the track is one shade lighter than the surface (not lighter than the border)

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#243530` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 12px, uppercase, `#8FAA9C`  |
| Value        | 28px, SemiBold, status-colored or `#EFF5F2` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#243530`  | `#3A4D44` | `#8FAA9C` |
| Hover   | `#2C3F38`  | `#3A4D44` | `#EFF5F2` |
| Active  | `#2DD47A`  | `#2DD47A` | `#1A2420` |

Active tab uses full accent fill with dark text — the only place accent fills a large area.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#35C177` | `oklch(0.72 0.16 155)`      | `[0][0]`         | `--c1`       |
| 2      | `#7FC581` | `oklch(0.76 0.12 145)`      | `[1][0]`         | `--c2`       |
| 3      | `#4BC1AD` | `oklch(0.74 0.11 180)`      | `[2][0]`         | `--c3`       |
| 4      | `#9CC685` | `oklch(0.78 0.10 135)`      | `[3][0]`         | `--c4`       |
| 5      | `#8CCFB1` | `oklch(0.80 0.08 165)`      | `[4][0]`         | `--c5`       |
| 6      | `#4CBBBB` | `oklch(0.73 0.10 195)`      | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#59C886` | `oklch(0.75 0.14 155)`  | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#D48AAD` | `oklch(0.72 0.10 350)`  | `nameColorMap.NegativeColor`    |
| Total / Net       | `#8FAA9C` | `oklch(0.70 0.015 155)` | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#EFF5F2` | `oklch(0.95 0.005 155)` | —                               |
| Forecast          | `#2DD47A` | `oklch(0.72 0.18 155)`  | — (dashed stroke)               |
| Confidence Band   | `#2DD47A26` | `oklch(0.72 0.18 155 / 0.15)` | — (area fill)            |
| Today Indicator   | `#F4A34B` | `oklch(0.78 0.14 65)`   | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#2F3F37` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#3A4D44` (`--border`), 1px
- Axis tick text: `#8FAA9C` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#1E2B26` with `--shadow`, 6px radius, `#EFF5F2` text
- Legend text: `#8FAA9C`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#1A2420` (--bg)   | none                 | Page background                  |
| Raised   | `#243530` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#2C3F38`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.50)` | none             | Modal backdrop                   |

Dark mode depth relies on surface lightness steps rather than shadow alone. Each tier is roughly ~0.04–0.06 **L** higher than the previous in OKLCH terms. Shadows reinforce but do not create the hierarchy.

### 6.2 Border Usage

- Prefer shadow over border for card edges — shadows adapt to any background
- Use `1px solid var(--border-light)` only for explicit dividers (horizontal rules, table row separators)
- Use `1px solid var(--border)` for input outlines (accessibility requirement)
- Never use borders thicker than `2px` except for status indicators (left accent borders on cards)

---

## 7. Do's and Don'ts

### Do

- Use `c58` for primary text and `c59` for secondary text (e.g. table headers, tab labels, default nav links) in the App Studio theme JSON — never `c60`
- Keep saturated emerald usage under ~30% of visible area per page (accents, primary series, active controls)
- Use `--text-primary` (`#EFF5F2` soft warm off-white) instead of `#FFFFFF` for body and titles
- Set `background: transparent` on pro-code app containers embedded in App Studio cards
- Use three-layer shadows with pure black at moderate opacity (0.20–0.40)
- Test every native element (hero cards, filters, nav) for text visibility after theme application
- Apply `font-variant-numeric: tabular-nums` to all dynamic numbers
- Keep chrome and scaffolding in cool gray-greens; let emerald signal “this is the live signal”

### Don't

- Use `c60` (AUTOMATIC_COLOR) for any font color — it defaults to dark text on dark backgrounds
- Use pure white (`#FFFFFF`) for text — it flares and reads unfinished on dark green-gray surfaces
- Use light-tinted status badge backgrounds (L > 0.80) — they look washed out on dark cards
- Apply a light theme’s border colors — they disappear or clip contrast on dark surfaces
- Use `transition: all` — specify exact properties
- Use font-weight 700 or 900 — too heavy for the minimal aesthetic
- Place colored shadows — they disappear on dark surfaces; use pure black only
- Spray emerald across icons, borders, and backgrounds “for brand” — reserve it for primary data and active states

---

## 8. Dark Mode Adaptation Notes

This is already a dark theme. When an agent encounters a request to apply this theme:

1. **App Studio Native Theme**: Apply colors from the Slot Mapping Table (Section 2.1) to the corresponding `c1`–`c60` positions. Replace every `c60` reference in `cards[].fontColor`, `navigation[]*FontColor`, `headers[].fontColor`, and `components[]*FontColor` with `c58` or `c59` as appropriate (primary vs secondary). Never leave `c60` in place.

2. **Pro-Code CSS**: Copy the full `--bg` through chart `--c6` block from Section 9.1 into the app's `:root`. Set the `COLORS` object in `app.js` from these values. Use `background: transparent` on the app container.

3. **Chart Colors**: Map `--c1` through `--c6` into the Recharts/Chart.js color array. Apply semantic chart colors (Section 5.2) for goal lines, forecast, confidence bands, and waterfall segments.

4. **If reversing to light mode**: Do NOT simply invert L values. Use the light theme’s `domo-app-theme` structural colors and a light palette from `color-palettes.md`. Dark-to-light is a full theme swap, not an inversion.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.14 0.012 155);
  --surface:        oklch(0.20 0.016 155);
  --surface-hover:  oklch(0.24 0.018 155);
  --text-primary:   oklch(0.95 0.005 155);
  --text-secondary: oklch(0.70 0.015 155);
  --border:         oklch(0.30 0.012 155);
  --border-light:   oklch(0.25 0.010 155);
  --accent:         oklch(0.72 0.18 155);
  --accent-muted:   oklch(0.72 0.18 155 / 0.15);
  --accent-hover:   oklch(0.77 0.17 155);

  --on-track:       oklch(0.75 0.14 155);
  --on-track-bg:    oklch(0.25 0.04 155);
  --at-risk:        oklch(0.78 0.14 65);
  --at-risk-bg:     oklch(0.25 0.04 65);
  --behind:         oklch(0.72 0.10 350);
  --behind-bg:      oklch(0.22 0.03 350);
  --complete:       oklch(0.70 0.11 200);
  --complete-bg:    oklch(0.22 0.04 200);

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.20),
    0px 1px 3px -1px oklch(0 0 0 / 0.30),
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

  --c1: oklch(0.72 0.16 155);
  --c2: oklch(0.76 0.12 145);
  --c3: oklch(0.74 0.11 180);
  --c4: oklch(0.78 0.10 135);
  --c5: oklch(0.80 0.08 165);
  --c6: oklch(0.73 0.10 195);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #1A2420    Card bg      → c2   #243530
Hover bg     → c3   #2C3F38    Nav bg       → c4   #1E2B26
Primary text → c58  #EFF5F2    Secondary    → c59  #8FAA9C
Accent       → c29  #2DD47A    Accent hover → c30  #3DD383
Border       → c46  #3A4D44    Nav links    → c59; active → c58
Font colors  → c58 / c59 as hierarchy dictates; NEVER c60
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#2DD47A',
  primaryHover: '#3DD383',
  secondary: '#7FC581',
  tertiary:  '#4BC1AD',
  surface:   '#243530',
  bg:        '#1A2420',
  text:      '#EFF5F2',
  textMuted: '#8FAA9C',
  border:    '#3A4D44',
  positive:  '#59C886',
  negative:  '#D48AAD',
  series: ['#35C177', '#7FC581', '#4BC1AD', '#9CC685', '#8CCFB1', '#4CBBBB']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: Use `--surface` background, `--text-primary` for the value (28px SemiBold tabular-nums), `--text-secondary` for the label (11px Light uppercase). Status-colored left border (4px). No visible card border — shadow only.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow pattern from the `app-studio-pro-code` skill's Banner Background Patterns section. Set text to `--text-primary`, gradient start from `--surface`, accent glow from `--accent-muted`.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fill array. `CartesianGrid` stroke `#2F3F37` opacity 0.5. `XAxis`/`YAxis` tick fill `#8FAA9C`. Tooltip with `#1E2B26` bg and `#EFF5F2` text. `ResponsiveContainer` at 100% width.

**"Add a forecast line with confidence band"**: `ComposedChart` with `Line` for historical (solid `--c1`), `Line` for forecast (dashed `--accent` strokeDasharray="6 4"), `Area` for confidence band (`--accent-muted` fill, no stroke). `ReferenceLine` at today's date with `--at-risk` stroke (dashed). Toggle the band via a `.confidence-toggle` button.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements all colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Emerald Dark",
  "colors": [
    { "index": 1, "value": "#1A2420", "tag": "PRIMARY" },
    { "index": 2, "value": "#243530", "tag": "PRIMARY" },
    { "index": 3, "value": "#2C3F38", "tag": "PRIMARY" },
    { "index": 4, "value": "#1E2B26", "tag": "PRIMARY" },
    { "index": 5, "value": "#2C3F38", "tag": "PRIMARY" },
    { "index": 6, "value": "#1A2420", "tag": "PRIMARY" },
    { "index": 7, "value": "#243530", "tag": "PRIMARY" },
    { "index": 29, "value": "#2DD47A", "tag": "SECONDARY" },
    { "index": 30, "value": "#3DD383", "tag": "SECONDARY" },
    { "index": 40, "value": "#050807", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0E1713", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#1A2420", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#243530", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#3A4D44", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#4F6259", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#3A4D44", "tag": "CUSTOM" },
    { "index": 47, "value": "#2F3F37", "tag": "CUSTOM" },
    { "index": 48, "value": "#3A4D44", "tag": "CUSTOM" },
    { "index": 49, "value": "#6E8379", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#8A9E94", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#A3B5AB", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C5D5CC", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#DCE9E2", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F2F8F5", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#EFF5F2", "tag": "FONT" },
    { "index": 59, "value": "#8FAA9C", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Then verify navigation uses `c59` for link text, `c58` for active links and titles, and headers/cards use `c58` — never `c60`.

> **Table stripes**: Native `alternateRowBackgroundColor` references `c43` (surface-level). For a subtler stripe, point this slot at `c11` in a forked JSON or override in pro-code tables using `#1F2A26`.
