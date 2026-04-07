# Biopunk — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Toxic bioluminescent green · **Mood**: Gene-splicing labs, biotech capitalism, bioluminescent organisms, organic circuitry — *Ex Machina* meets *Annihilation*

---

## 1. Visual Theme and Atmosphere

**Personality**: Gene-splicing laboratory at midnight. The UI sits on near-black benches with a persistent green undertone; cards read like petri dishes and instrument panels under low light. Nothing whispers “nature documentary” — it whispers *proprietary assay*.

**Density**: Medium-high. Cards pack tightly with 16px gaps; internal padding at 20px keeps dense lab metrics legible. Dark bio-green surfaces let tight grids feel contained rather than cramped.

**Philosophy**: Extreme restraint on the accent. `#39FF14` reads as radioactive; it is reserved for primary series, the single strongest KPI emphasis per view, focus rings, and active controls. If more than ~15% of visible area reads as neon green, the lab stops feeling cold and elite — it becomes a novelty theme. Earn the glow.

**Atmosphere cues**:
- Surfaces feel like petri dishes on dark lab benches — matte, slightly humid, never warm taupe
- The green undertone in every structural surface (hue ~155) creates an under-the-microscope, clinical calm
- Data points and highlights glow like bioluminescent organisms against the void
- Transitions stay crisp (150ms), not elastic — equipment responds; it doesn’t bounce
- Shadows stay pure black at 0.25–0.40 opacity — colored shadows die on these depths
- Body text is pale bioluminescent white-green (`#D0E8D0`), never the accent green — neon green body copy fails contrast and reads as alarm, not content

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                         | Theme Slot | CSS Variable        |
|---------------------|-----------|-------------------------------|------------|---------------------|
| Page Background     | `#0A100A` | `oklch(0.06 0.018 155)`       | `c1`       | `--bg`              |
| Card Surface        | `#142018` | `oklch(0.14 0.028 155)`       | `c2`       | `--surface`         |
| Surface Hover       | `#1C2820` | `oklch(0.18 0.032 155)`       | `c3`       | `--surface-hover`   |
| Primary Text        | `#D0E8D0` | `oklch(0.90 0.035 145)`       | `c58`      | `--text-primary`    |
| Secondary Text      | `#6A8068` | `oklch(0.52 0.045 145)`       | `c59`      | `--text-secondary`  |
| Border              | `#223028` | `oklch(0.22 0.028 155)`       | `c46`      | `--border`          |
| Border Light        | `#1A2820` | `oklch(0.17 0.028 155)`       | `c47`      | `--border-light`    |
| Accent              | `#39FF14` | `oklch(0.88 0.35 145)`        | `c29`      | `--accent`          |
| Accent Muted        | `rgba(57,255,20,0.12)` | `oklch(0.88 0.35 145 / 0.12)` | —    | `--accent-muted`    |
| Accent Hover        | `#50FF30` | `oklch(0.90 0.32 145)`        | `c30`      | `--accent-hover`    |
| Nav Background      | `#0C1410` | `oklch(0.08 0.022 155)`       | `c4`       | `--nav-bg`          |
| Nav Active          | `#1C2820` | `oklch(0.18 0.032 155)`       | `c5`       | `--nav-active`      |
| Header Background   | `#0A100A` | `oklch(0.06 0.018 155)`       | `c6`       | `--header-bg`       |
| Input Background    | `#142018` | `oklch(0.14 0.028 155)`       | `c7`       | `--input-bg`        |
| Input Border        | `#223028` | `oklch(0.22 0.028 155)`       | `c48`      | `--input-border`    |
| Tab Default BG      | `#142018` | `oklch(0.14 0.028 155)`       | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#39FF14` | `oklch(0.88 0.35 145)`        | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#0C1410` | `oklch(0.08 0.022 155)`       | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#101810` | `oklch(0.10 0.020 155)`       | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#1C2820` | `oklch(0.18 0.032 155)`       | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#000000` | `oklch(0 0 0)`                | `c40`      | —                   |
| Grayscale 2         | `#060806` | `oklch(0.05 0.012 155)`       | `c41`      | —                   |
| Grayscale 3         | `#0A100A` | `oklch(0.06 0.018 155)`       | `c42`      | —                   |
| Grayscale 4         | `#101810` | `oklch(0.10 0.020 155)`       | `c43`      | —                   |
| Grayscale 5         | `#223028` | `oklch(0.22 0.028 155)`       | `c44`      | —                   |
| Grayscale 6         | `#2E3C34` | `oklch(0.28 0.030 155)`       | `c45`      | —                   |
| Grayscale 7         | `#485848` | `oklch(0.40 0.035 145)`       | `c49`      | —                   |
| Grayscale 8         | `#6A8068` | `oklch(0.52 0.045 145)`       | `c50`      | —                   |
| Grayscale 9         | `#98B098` | `oklch(0.68 0.040 145)`       | `c51`      | —                   |
| Grayscale 10        | `#D0E8D0` | `oklch(0.90 0.035 145)`       | `c52`      | —                   |
| Grayscale 11        | `#E0F2E0` | `oklch(0.93 0.025 145)`       | `c53`      | —                   |
| Grayscale 12        | `#F0FAF0` | `oklch(0.97 0.015 145)`       | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#50D848` | `#0E1A12`  | `#50D848` | `--on-track`     |
| At Risk  | `#D4A020` | `#1A160E`  | `#D4A020` | `--at-risk`      |
| Behind   | `#C04050` | `#1A1014`  | `#C04050` | `--behind`       |
| Complete | `#20C8E0` | `#0E1820`  | `#20C8E0` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.10–0.12) with saturated text in the status hue. Never use light-tinted badge backgrounds on dark surfaces — they read as errors in a clinical UI.

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

Shadow color is **pure black** at 0.25–0.40 opacity. On near-black bio-green surfaces, tinted shadows vanish — only opacity defines separation.

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
- **Never use Bold (700) or Black (900)** — they break the cold lab minimalism

### 3.4 Text Color Rules

Primary text is `#D0E8D0` (pale bioluminescent green-white), not `#FFFFFF` and **not** `#39FF14`. Pure white flares on these depths; neon green as body copy is unreadable and signals danger. Secondary text at `#6A8068` (muted lichen) defines hierarchy without warming the palette.

Chart axis labels, tooltips, and legend text use `--text-secondary` (`#6A8068`). Data marks, primary series, and emphasis numerals may use `--accent` only where small and surrounded by neutral context.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#142018`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#D0E8D0`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#39FF14`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible border — depth from shadow. Card surface is one measured step above page background; both share hue ~155 so the stack feels like one instrument rack.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#142018`  | `#223028` | `#6A8068` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#1C2820`  | `#39FF14` | `#D0E8D0` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#39FF14`  | `#39FF14` | `#0A100A` | `--accent` / `--accent` / `--bg` |
| Disabled | `#0C1410`  | `#1A2820` | `#2E3C34` | — |

Ghost/outline by default. Border radius: 6px. Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`. Keep filled accent buttons rare — prefer outline + glow on hover.

### 4.3 Inputs and Selects

| Property    | Value                     |
|-------------|---------------------------|
| Background  | `#142018` (`--surface`)   |
| Border      | `#223028` (`--border`)    |
| Text        | `#D0E8D0` (`--text-primary`) |
| Placeholder | `#2E3C34`                 |
| Focus border| `#39FF14` (`--accent`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint at L ~0.10–0.12 with hue from the status color
- Text: the status primary color (bright on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#0C1410`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#6A8068`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#D0E8D0`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#39FF14`             | `navigation.activeColor` → `c29`    |
| Title text        | `#D0E8D0`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#1C2820`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58` or `c59`** as appropriate — **never `c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, which erases nav labels on dark bio surfaces.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#0A100A`             | `headers.backgroundColor` → `c1` |
| Font color  | `#D0E8D0`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#0C1410`             | `tables.headerBG` → `c4`   |
| Header text     | `#6A8068`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#142018`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#101810`             | `tables.stripeBG` → `c43`  |
| Row hover       | `#1C2820`             | `tables.hoverBG` → `c3`    |
| Row text        | `#D0E8D0`             | `tables.fontColor` → `c58` |
| Border          | `#1A2820`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#223028` (`--border`), 8px height, 4px radius
- Fill: status-colored or `--accent` for neutral progress; transition `width` 300ms ease
- On dark backgrounds the track sits one step above surface chroma, not lighter than the accent

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#142018` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 12px, uppercase, `#6A8068`  |
| Value        | 28px, SemiBold, `#D0E8D0` or status / accent for one hero metric |
| Shadow       | `var(--shadow)`             |

Use accent for **at most one** primary KPI per row; the rest stay primary text or status colors.

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#142018`  | `#223028` | `#6A8068` |
| Hover   | `#1C2820`  | `#223028` | `#D0E8D0` |
| Active  | `#39FF14`  | `#39FF14` | `#0A100A` |

Active tab uses full accent fill with **near-black** text (`--bg`) — large neon fields need dark glyphs for legibility.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#39FF14` | `oklch(0.88 0.35 145)`      | `[0][0]`         | `--c1`       |
| 2      | `#9B59B6` | `oklch(0.55 0.22 300)`      | `[1][0]`         | `--c2`       |
| 3      | `#20C8E0` | `oklch(0.72 0.12 220)`      | `[2][0]`         | `--c3`       |
| 4      | `#D4A020` | `oklch(0.72 0.15 85)`       | `[3][0]`         | `--c4`       |
| 5      | `#C04050` | `oklch(0.55 0.18 15)`       | `[4][0]`         | `--c5`       |
| 6      | `#2C6040` | `oklch(0.38 0.08 155)`      | `[5][0]`         | `--c6`       |

Series 1 is the **bioluminescent** anchor; series 6 is **chlorophyll dark** — use for baselines, confidence, or secondary ecology metrics so the chart does not become all neon.

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                     | Theme JSON Key                  |
|-------------------|-----------|---------------------------|---------------------------------|
| Positive / Up     | `#50D848` | `oklch(0.78 0.20 145)`    | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#C04050` | `oklch(0.55 0.18 15)`     | `nameColorMap.NegativeColor`    |
| Total / Net       | `#6A8068` | `oklch(0.52 0.045 145)`   | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#D0E8D0` | `oklch(0.90 0.035 145)`   | —                               |
| Forecast          | `#39FF14` | `oklch(0.88 0.35 145)`    | — (dashed `--c1` stroke)        |
| Confidence Band   | `rgba(57,255,20,0.12)` | `oklch(0.88 0.35 145 / 0.12)` | — (area fill)            |
| Today Indicator   | `#D4A020` | `oklch(0.72 0.15 85)`     | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#1A2820` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#223028` (`--border`), 1px
- Axis tick text: `#6A8068` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#0C1410` with `--shadow`, 6px radius, `#D0E8D0` text
- Legend text: `#6A8068`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3
- Do not default every line to `#39FF14` — rotate the palette so toxicity stays intentional

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#0A100A` (--bg)   | none                 | Page background                  |
| Raised   | `#142018` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#1C2820`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.55)` | none             | Modal backdrop                   |

Dark mode depth uses **lightness steps** on the same green hue (~155). Shadows reinforce hierarchy but surfaces do the heavy lifting.

### 6.2 Border Usage

- Prefer shadow over border for card edges
- Use `1px solid var(--border-light)` for dividers and subtle table separators
- Use `1px solid var(--border)` for inputs (accessibility)
- Avoid warm structural borders — keep dividers in the cold green-gray family
- Status or assay emphasis: optional 4px left border in accent or status color on a single card per section

---

## 7. Do's and Don'ts

### Do

- Keep the **green undertone in ALL structural surfaces** (hue ~155, low chroma) — the lab is one environment, not gray cards on a green wallpaper
- Use **`c58`** for all primary UI text color references in App Studio theme JSON — **never `c60`**
- Use **`#39FF14` only for primary data series, focus rings, active tab/button fills, and one hero emphasis per view**
- Use **`#D0E8D0`** for body and titles; **`#6A8068`** for secondary labels, axes, and nav defaults
- Use **`c59` for `linkFontColor`** where you want inactive nav/filter links to recede (pair with **`c58`** for active states)
- Set `background: transparent` on pro-code app containers embedded in App Studio cards
- Use **three-layer shadows** with **pure black** at **0.25–0.40** opacity
- Test hero cards, filters, and nav after import — green-tinted surfaces expose bad automatic contrast choices instantly
- Apply `font-variant-numeric: tabular-nums` to all dynamic numbers
- Treat **chlorophyll dark (`#2C6040`)** and **muted accent fills** as relief valves so charts stay readable

### Don't

- Use **`c60`** (AUTOMATIC_COLOR) for any font color — it defaults to dark text on dark backgrounds
- Use **`#39FF14` for body text, paragraphs, or chart axis labels** — unreadable and emotionally wrong for dense copy
- Use **warm hues** (orange browns, warm grays) for **structural** chrome — the lab reads cold; warmth belongs in **data** (amber series, blood red), not in the bench
- Exceed **~15% accent coverage** per screen — the “toxic bioluminescent” read comes from **restraint**, not saturation
- Use **light-tinted** status badge backgrounds on dark cards
- Use **`transition: all`** — list explicit properties
- Use **font-weight 700+** for this aesthetic
- Use **colored drop shadows** — they disappear; use **black** only
- Default **every** KPI to accent green — you will lose hierarchy and the UI will shout

---

## 8. Dark Mode Adaptation Notes

This theme is **native dark**. When an agent applies it:

1. **App Studio Native Theme**: Map Section 2.1 slots to `c1`–`c60` as in the import JSON. Replace every `c60` reference in cards, navigation, headers, tables, tabs, and forms with **`c58`** (or **`c59`** where secondary copy is intended).

2. **Pro-Code CSS**: Copy the `:root` block from Section 9.1. Set `COLORS` / chart arrays from Section 9.3. Use `background: transparent` on the app root inside cards.

3. **Chart Colors**: Map `--c1` through `--c6` into Recharts/Chart.js. Use Section 5.2 for waterfall, forecast dashes, and confidence bands (`--accent-muted`).

4. **Light mode**: Do **not** invert luminance. A light Biopunk variant would need new structural neutrals and a darker accent glyph strategy — treat as a separate theme.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.06 0.018 155);
  --surface:        oklch(0.14 0.028 155);
  --surface-hover:  oklch(0.18 0.032 155);
  --text-primary:   oklch(0.90 0.035 145);
  --text-secondary: oklch(0.52 0.045 145);
  --border:         oklch(0.22 0.028 155);
  --border-light:   oklch(0.17 0.028 155);
  --accent:         oklch(0.88 0.35 145);
  --accent-muted:   oklch(0.88 0.35 145 / 0.12);
  --accent-hover:   oklch(0.90 0.32 145);

  --on-track:       oklch(0.78 0.20 145);
  --on-track-bg:    oklch(0.12 0.04 150);
  --at-risk:        oklch(0.72 0.15 85);
  --at-risk-bg:     oklch(0.12 0.04 85);
  --behind:         oklch(0.55 0.18 15);
  --behind-bg:      oklch(0.12 0.04 15);
  --complete:       oklch(0.72 0.12 220);
  --complete-bg:    oklch(0.12 0.04 220);

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

  --c1: oklch(0.88 0.35 145);
  --c2: oklch(0.55 0.22 300);
  --c3: oklch(0.72 0.12 220);
  --c4: oklch(0.72 0.15 85);
  --c5: oklch(0.55 0.18 15);
  --c6: oklch(0.38 0.08 155);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #0A100A    Card bg      → c2   #142018
Hover bg     → c3   #1C2820    Nav bg       → c4   #0C1410
Primary text → c58  #D0E8D0    Secondary    → c59  #6A8068
Accent       → c29  #39FF14    Border       → c46  #223028
Font colors  → ALWAYS c58 (or c59 for muted links) — NEVER c60
Accent cap   → < ~15% of visible area per view
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#39FF14',
  secondary: '#9B59B6',
  tertiary:  '#20C8E0',
  surface:   '#142018',
  bg:        '#0A100A',
  text:      '#D0E8D0',
  textMuted: '#6A8068',
  border:    '#223028',
  positive:  '#50D848',
  negative:  '#C04050',
  series: ['#39FF14', '#9B59B6', '#20C8E0', '#D4A020', '#C04050', '#2C6040']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: `--surface` cards, values at 28px SemiBold tabular-nums in `--text-primary`; use `--accent` for **one** hero only. Labels 11px Light uppercase `--text-secondary`. Optional 4px left border in status or accent. Shadow only — no card border.

**"Build a banner with background pattern"**: Subtle grid or organic noise in `--border-light` at very low opacity; accent glow from `--accent-muted` — never full-width `#39FF14`.

**"Build a bar chart card"**: Recharts with `COLORS.series`. `CartesianGrid` stroke `#1A2820` opacity 0.5. Axes tick fill `#6A8068`. Tooltip `#0C1410` bg, `#D0E8D0` text.

**"Add a forecast line with confidence band"**: Solid history `--c1`, dashed forecast `--c1`, band fill `rgba(57,255,20,0.12)`. Reference “today” with `--c4` (toxin amber) dashed if it must read as alert, not as primary series.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Biopunk",
  "colors": [
    { "index": 1, "value": "#0A100A", "tag": "PRIMARY" },
    { "index": 2, "value": "#142018", "tag": "PRIMARY" },
    { "index": 3, "value": "#1C2820", "tag": "PRIMARY" },
    { "index": 4, "value": "#0C1410", "tag": "PRIMARY" },
    { "index": 5, "value": "#1C2820", "tag": "PRIMARY" },
    { "index": 6, "value": "#0A100A", "tag": "PRIMARY" },
    { "index": 7, "value": "#142018", "tag": "PRIMARY" },
    { "index": 29, "value": "#39FF14", "tag": "SECONDARY" },
    { "index": 30, "value": "#50FF30", "tag": "SECONDARY" },
    { "index": 40, "value": "#000000", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#060806", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#0A100A", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#101810", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#223028", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#2E3C34", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#223028", "tag": "CUSTOM" },
    { "index": 47, "value": "#1A2820", "tag": "CUSTOM" },
    { "index": 48, "value": "#223028", "tag": "CUSTOM" },
    { "index": 49, "value": "#485848", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#6A8068", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#98B098", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#D0E8D0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E0F2E0", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F0FAF0", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#D0E8D0", "tag": "FONT" },
    { "index": 59, "value": "#6A8068", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm every `fontColor` uses **`c58`** or **`c59`** — **never `c60`**. Active tab text uses **`c1`** (`#0A100A`) for contrast on neon green.
