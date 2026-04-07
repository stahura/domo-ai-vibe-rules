# Dungeonpunk — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Arcane amber / gold · **Mood**: Gritty magical technology, arcane runes, underground forges, enchanted minerals

---

## 1. Visual Theme and Atmosphere

**Personality**: Underground forge meets arcane library. Stone-textured surfaces catch warm amber light from enchanted sources — data reads like runes and ingots, not dashboard widgets.

**Density**: Medium-high. Cards sit in a 16px grid with 20px internal padding so dense RPG-style metrics still feel carved, not cramped. Dark stone makes tight layouts feel cavernous rather than cluttered.

**Philosophy**: Weight and texture over flat modernism. The gold accent is magical energy — reserved for primary data, active controls, and the one hero insight per view. If gold dominates the canvas, the spell is broken; structure stays in warm neutrals and mineral tones.

**Atmosphere cues**:
- Surfaces read as hewn slate and worn stone — warm undertone (sandstone family), never sterile blue-gray
- Chart colors suggest minerals and gemstones embedded in rock (gold, teal, amethyst, forge ember, mineral blue, weathered stone)
- Shadows are pure black at 0.25–0.40 opacity — depth and ritual weight, not airy elevation
- Text is pale sandstone (`#D8D0C0`), never pure white — pure `#FFFFFF` feels like glare in a torchlit vault

**Best for**: Gaming analytics, fantasy and entertainment, creative industries, inventory management, RPG-style progress tracking — anywhere the story is “earned progress in a dangerous world.”

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#161614` | `oklch(0.12 0.006 85)`      | `c1`       | `--bg`              |
| Card Surface        | `#222220` | `oklch(0.17 0.005 85)`      | `c2`       | `--surface`         |
| Surface Hover       | `#2C2C28` | `oklch(0.21 0.006 85)`      | `c3`       | `--surface-hover`   |
| Primary Text        | `#D8D0C0` | `oklch(0.86 0.012 85)`      | `c58`      | `--text-primary`    |
| Secondary Text      | `#8A8478` | `oklch(0.58 0.018 85)`      | `c59`      | `--text-secondary`  |
| Border              | `#323028` | `oklch(0.28 0.012 85)`      | `c46`      | `--border`          |
| Border Light        | `#2A2A26` | `oklch(0.24 0.008 85)`     | `c47`      | `--border-light`    |
| Accent              | `#D4A030` | `oklch(0.72 0.13 85)`       | `c29`      | `--accent`          |
| Accent Muted        | `rgba(212,160,48,0.15)` | `oklch(0.72 0.13 85 / 0.15)` | —    | `--accent-muted`    |
| Accent Hover        | `#E0B040` | `oklch(0.76 0.12 85)`       | `c30`      | `--accent-hover`    |
| Nav Background      | `#1A1A18` | `oklch(0.13 0.005 85)`      | `c4`       | `--nav-bg`          |
| Nav Active          | `#2C2C28` | `oklch(0.21 0.006 85)`      | `c5`       | `--nav-active`      |
| Header Background   | `#161614` | `oklch(0.12 0.006 85)`      | `c6`       | `--header-bg`       |
| Input Background    | `#222220` | `oklch(0.17 0.005 85)`      | `c7`       | `--input-bg`        |
| Input Border        | `#323028` | `oklch(0.28 0.012 85)`      | `c48`      | `--input-border`    |
| Tab Default BG      | `#222220` | `oklch(0.17 0.005 85)`      | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#D4A030` | `oklch(0.72 0.13 85)`       | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#1A1A18` | `oklch(0.13 0.005 85)`      | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#1C1C1A` | `oklch(0.14 0.005 85)`      | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#2C2C28` | `oklch(0.21 0.006 85)`      | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#060605` | `oklch(0.05 0.002 85)`      | `c40`      | —                   |
| Grayscale 2         | `#0E0E0C` | `oklch(0.09 0.004 85)`      | `c41`      | —                   |
| Grayscale 3         | `#161614` | `oklch(0.12 0.006 85)`      | `c42`      | —                   |
| Grayscale 4         | `#1C1C1A` | `oklch(0.14 0.005 85)`      | `c43`      | —                   |
| Grayscale 5         | `#222220` | `oklch(0.17 0.005 85)`      | `c44`      | —                   |
| Grayscale 6         | `#323028` | `oklch(0.28 0.012 85)`      | `c45`      | —                   |
| Grayscale 7         | `#605C54` | `oklch(0.48 0.014 85)`      | `c49`      | —                   |
| Grayscale 8         | `#787468` | `oklch(0.56 0.014 85)`      | `c50`      | —                   |
| Grayscale 9         | `#948C80` | `oklch(0.64 0.016 85)`      | `c51`      | —                   |
| Grayscale 10        | `#B0A898` | `oklch(0.74 0.014 85)`      | `c52`      | —                   |
| Grayscale 11        | `#C8C0B0` | `oklch(0.82 0.012 85)`      | `c53`      | —                   |
| Grayscale 12        | `#E0D8C8` | `oklch(0.90 0.010 85)`      | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#408888` | `#152624`  | `#408888` | `--on-track`     |
| At Risk  | `#C86030` | `#261A14`  | `#C86030` | `--at-risk`      |
| Behind   | `#6A4898` | `#1C1624`  | `#6A4898` | `--behind`       |
| Complete | `#5078A0` | `#141C28`  | `#5078A0` | `--complete`     |

Dark mode status badges use dark-tinted backgrounds (L ~0.12–0.16) with hue borrowed from the status primary; text uses the bright status color. Never use light-tinted badge backgrounds on dark stone.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.25),
  0px 1px 3px -1px oklch(0 0 0 / 0.35),
  0px 2px 6px 0px oklch(0 0 0 / 0.25);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.30),
  0px 2px 6px -1px oklch(0 0 0 / 0.40),
  0px 4px 12px 0px oklch(0 0 0 / 0.30);
```

Shadow color is **pure black** at 0.25–0.40 opacity. On dark stone, colored shadows vanish — only opacity defines depth.

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
| Labels / captions        | 11px | Regular  | 400              | `f4`            | uppercase, `letter-spacing: 0.04em`  |
| Chart axis text          | 11px | Regular  | 400              | `f5`            | `fill` color, not CSS `color`          |
| Badges / status text     | 11px | SemiBold | 600              | `f6`            | only small text that gets weight       |
| KPI numbers              | 28px | SemiBold | 600              | `f7`            | `font-variant-numeric: tabular-nums`   |
| KPI labels               | 11px | Light    | 300              | `f8`            | uppercase, `letter-spacing: 0.04em`    |

### 3.3 Weight Rules

- **SemiBold (600)**: Headings, KPI values, active button labels, badges
- **Regular (400)**: Body text, chart axes, table cells, descriptions
- **Light (300)**: KPI labels, timeframe captions — recedes behind the numbers
- **Never use Bold (700) or Black (900)** — they break the carved-stone restraint

### 3.4 Text Color Rules

Primary text is `#D8D0C0` (pale sandstone), not `#FFFFFF`. Secondary text at `#8A8478` reads as weathered stone — two clear tiers without neon contrast.

Chart axis labels, tooltips, and legend text use `--text-secondary` (`#8A8478`). Data values and series labels use `--text-primary` where they must read as “ink in the ledger.”

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#222220`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#D8D0C0`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `8px`                          | `ca1.borderRadius` = `8`      |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#D4A030`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible card border — separation comes from shadow and the step from page (`#161614`) to slate (`#222220`). **8px radius** reads as cut stone blocks, not pills or perfect circles.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#222220`  | `#323028` | `#8A8478` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#2C2C28`  | `#D4A030` | `#D8D0C0` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#D4A030`  | `#D4A030` | `#161614` | `--accent` / `--accent` / `--bg` |
| Disabled | `#1A1A18`  | `#2A2A26` | `#484640` | — |

Outline / stone-slab default. Border radius: `6px` (controls stay slightly tighter than cards). Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property     | Value                     |
|--------------|---------------------------|
| Background   | `#222220` (`--surface`)   |
| Border       | `#323028` (`--border`)    |
| Text         | `#D8D0C0` (`--text-primary`) |
| Placeholder  | `#484640`                 |
| Focus border | `#D4A030` (`--accent`)    |
| Radius       | `6px`                     |
| Font         | 13px, weight 600          |

### 4.4 Status Badges

- Background: dark tint (Section 2.2) with status hue
- Text: status primary color
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px` (small chips; cards keep **8px**)

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#1A1A18`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#D8D0C0`             | `navigation.linkFontColor` → `c58`  |
| Active link text  | `#D8D0C0`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#D4A030`             | `navigation.activeColor` → `c29`    |
| Title text        | `#D8D0C0`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#2C2C28`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58`**, never **`c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text and will hide nav labels on dark stone.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#161614`             | `headers.backgroundColor` → `c1` |
| Font color  | `#D8D0C0`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#1A1A18`             | `tables.headerBG` → `c4`   |
| Header text     | `#8A8478`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#222220`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#1C1C1A`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#2C2C28`             | `tables.hoverBG` → `c3`    |
| Row text        | `#D8D0C0`             | `tables.fontColor` → `c58` |
| Border          | `#2A2A26`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#323028` (`--border`), 8px height, **6px** radius (blocky, not round)
- Fill: status-colored or accent; `width` transition 300ms ease

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#222220` (`--surface`)     |
| Radius       | `8px`                       |
| Label        | 11px Light uppercase, `#8A8478` |
| Value        | 28px SemiBold, accent or status or `#D8D0C0` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#222220`  | `#323028` | `#8A8478` |
| Hover   | `#2C2C28`  | `#323028` | `#D8D0C0` |
| Active  | `#D4A030`  | `#D4A030` | `#161614` |

Active tab uses full arcane gold fill with dark text — high ritual emphasis; use sparingly on a page.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#D4A030` | `oklch(0.72 0.13 85)`       | `[0][0]`         | `--c1`       |
| 2      | `#408888` | `oklch(0.52 0.08 195)`      | `[1][0]`         | `--c2`       |
| 3      | `#6A4898` | `oklch(0.45 0.14 305)`      | `[2][0]`         | `--c3`       |
| 4      | `#C86030` | `oklch(0.58 0.15 45)`       | `[3][0]`         | `--c4`       |
| 5      | `#5078A0` | `oklch(0.52 0.08 250)`      | `[4][0]`         | `--c5`       |
| 6      | `#787468` | `oklch(0.56 0.014 85)`      | `[5][0]`         | `--c6`       |

Series read as **arcane gold**, **enchanted teal**, **runestone purple**, **forge fire**, **mineral blue**, **weathered stone** — gemstone and ore, not neon UI defaults.

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#408888` | `oklch(0.52 0.08 195)`  | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#C86030` | `oklch(0.58 0.15 45)`   | `nameColorMap.NegativeColor`    |
| Total / Net       | `#8A8478` | `oklch(0.58 0.018 85)`  | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#D8D0C0` | `oklch(0.86 0.012 85)`  | —                               |
| Forecast          | `#D4A030` | `oklch(0.72 0.13 85)`   | — (dashed stroke)               |
| Confidence Band   | `#D4A03026` | `oklch(0.72 0.13 85 / 0.15)` | — (area fill)            |
| Today Indicator   | `#C86030` | `oklch(0.58 0.15 45)`   | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#2A2A26` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#323028` (`--border`), 1px
- Axis tick text: `#8A8478` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#1A1A18` with `--shadow`, 6px radius, `#D8D0C0` text
- Legend text: `#8A8478`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3
- Avoid electric cyan, lime, or magenta — keep the palette forged and mineral

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#161614` (--bg)   | none                 | Page background                  |
| Raised   | `#222220` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#2C2C28`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0 0 0 / 0.55)` | none             | Modal backdrop                   |

Dark stone depth comes from **surface lightness steps** plus black shadows. Each tier steps up in L; shadows reinforce carved relief, not glassmorphism.

### 6.2 Border Usage

- Prefer shadow over visible card edges on the vault floor
- Use `1px solid var(--border-light)` for dividers and table row separators
- Use `1px solid var(--border)` for inputs (focus moves to accent)
- Avoid thick chrome borders; reserve strong edges for **status** or **rune-like** left accents on hero cards (4px accent bar)

---

## 7. Do's and Don'ts

### Do

- Use **warm neutral tones** for every structural surface (stone family, not cool gray)
- Make the **gold accent feel earned** — primary metrics, active states, one focal chart series per view
- Use **`c58` for all theme font color references** — **NEVER `c60`**
- Use **`8px` border-radius on cards and KPI surfaces** — stone blocks, not circles or pills
- Use **pure black shadows** at **0.25–0.40** opacity for hover and default elevation
- Set `background: transparent` on pro-code app containers inside App Studio cards
- Apply `font-variant-numeric: tabular-nums` to all dynamic numbers and level-style KPIs
- Test nav, headers, filters, and forms after import — confirm every label uses `c58`

### Don't

- Use **`c60`** (AUTOMATIC_COLOR) for any font color on dark backgrounds
- Default to a **modern / flat / clinical** look — texture, weight, and warmth define Dungeonpunk
- Use **neon or electric** colors — nothing should feel like RGB gamer trim; keep it hand-forged
- Flood the UI with **accent gold** — it is magical fuel, not wallpaper
- Use **pure white** (`#FFFFFF`) for body text
- Use **light-tinted** status badge fills on dark cards
- Use **`transition: all`** — list explicit properties
- Use **font-weight 700+** for this aesthetic

---

## 8. Dark Mode Adaptation Notes

This theme is **native dark**. When applying it:

1. **App Studio native theme**: Map Section 2.1 slots to `c1`–`c59` as in Section 10 JSON. Replace any `c60` in `cards`, `navigation`, `headers`, `components`, or `forms` with **`c58`**.

2. **Pro-code CSS**: Copy the `:root` custom properties from Section 9.1. Mirror values in a `COLORS` object for charts. Keep the app shell `background: transparent` when embedded.

3. **Charts**: Use Section 5.1 series order for Recharts / Chart.js. Map semantic colors (5.2) for waterfalls, forecast overlays, and reference lines.

4. **Light mode**: Do not invert L channels. A light Dungeonpunk would need a separate palette (bleached limestone + soot ink) — treat as a full theme swap.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.12 0.006 85);
  --surface:        oklch(0.17 0.005 85);
  --surface-hover:  oklch(0.21 0.006 85);
  --text-primary:   oklch(0.86 0.012 85);
  --text-secondary: oklch(0.58 0.018 85);
  --border:         oklch(0.28 0.012 85);
  --border-light:   oklch(0.24 0.008 85);
  --accent:         oklch(0.72 0.13 85);
  --accent-muted:   oklch(0.72 0.13 85 / 0.15);
  --accent-hover:   oklch(0.76 0.12 85);

  --on-track:       oklch(0.52 0.08 195);
  --on-track-bg:    oklch(0.16 0.03 195);
  --at-risk:        oklch(0.58 0.15 45);
  --at-risk-bg:     oklch(0.16 0.04 45);
  --behind:         oklch(0.45 0.14 305);
  --behind-bg:      oklch(0.14 0.04 305);
  --complete:       oklch(0.52 0.08 250);
  --complete-bg:    oklch(0.14 0.04 250);

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.25),
    0px 1px 3px -1px oklch(0 0 0 / 0.35),
    0px 2px 6px 0px oklch(0 0 0 / 0.25);
  --shadow-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.30),
    0px 2px 6px -1px oklch(0 0 0 / 0.40),
    0px 4px 12px 0px oklch(0 0 0 / 0.30);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 8px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --chart-1: oklch(0.72 0.13 85);
  --chart-2: oklch(0.52 0.08 195);
  --chart-3: oklch(0.45 0.14 305);
  --chart-4: oklch(0.58 0.15 45);
  --chart-5: oklch(0.52 0.08 250);
  --chart-6: oklch(0.56 0.014 85);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #161614    Card bg      → c2   #222220
Hover bg     → c3   #2C2C28    Nav bg       → c4   #1A1A18
Primary text → c58  #D8D0C0    Secondary    → c59  #8A8478
Accent       → c29  #D4A030    Accent hover → c30  #E0B040
Border       → c46  #323028    Border light → c47  #2A2A26
Font colors  → ALWAYS c58, NEVER c60
Card radius  → 8px (stone blocks)
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#D4A030',
  secondary: '#408888',
  tertiary:  '#6A4898',
  surface:   '#222220',
  bg:        '#161614',
  text:      '#D8D0C0',
  textMuted: '#8A8478',
  border:    '#323028',
  positive:  '#408888',
  negative:  '#C86030',
  behind:    '#6A4898',
  series: ['#D4A030', '#408888', '#6A4898', '#C86030', '#5078A0', '#787468']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: `--surface` cards, **8px** radius, `--shadow`, KPI value 28px SemiBold tabular-nums in `--text-primary` or `--accent` for the lead metric, label in `--text-secondary` Light uppercase. Optional 4px left border in `--accent` or status color.

**"Build a guild / party status board"**: Status pills with Section 2.2 backgrounds and primaries. Table from Section 4.7. Progress bars with forge/teal/purple fills for quest lanes.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series`. `CartesianGrid` stroke `#2A2A26` opacity 0.5. Axes tick fill `#8A8478`. Tooltip `#1A1A18` bg, `#D8D0C0` text.

**"Add inventory / loot breakdown"**: Donut or bar using c1–c6 as ore tiers; legend `--text-secondary`; center label `--text-primary` for total count.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the Dungeonpunk palette, **8px** card radius, fonts, navigation (**`c58` only** — no `c60`), tables, tabs, and forms.

```json
{
  "name": "Dungeonpunk",
  "colors": [
    { "index": 1, "value": "#161614", "tag": "PRIMARY" },
    { "index": 2, "value": "#222220", "tag": "PRIMARY" },
    { "index": 3, "value": "#2C2C28", "tag": "PRIMARY" },
    { "index": 4, "value": "#1A1A18", "tag": "PRIMARY" },
    { "index": 5, "value": "#2C2C28", "tag": "PRIMARY" },
    { "index": 6, "value": "#161614", "tag": "PRIMARY" },
    { "index": 7, "value": "#222220", "tag": "PRIMARY" },
    { "index": 29, "value": "#D4A030", "tag": "SECONDARY" },
    { "index": 30, "value": "#E0B040", "tag": "SECONDARY" },
    { "index": 40, "value": "#060605", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0E0E0C", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#161614", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#1C1C1A", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#222220", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#323028", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#323028", "tag": "CUSTOM" },
    { "index": 47, "value": "#2A2A26", "tag": "CUSTOM" },
    { "index": 48, "value": "#323028", "tag": "CUSTOM" },
    { "index": 49, "value": "#605C54", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#787468", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#948C80", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#B0A898", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#C8C0B0", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E0D8C8", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#D8D0C0", "tag": "FONT" },
    { "index": 59, "value": "#8A8478", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm navigation, headers, cards, tables, tabs, and forms use **`c58`** for text — **never `c60`**.
