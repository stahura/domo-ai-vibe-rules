# Atompunk — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Atomic orange · **Mood**: Retro-futuristic, optimistic, mid-century modern

---

## 1. Visual Theme and Atmosphere

**Personality**: Mission control at Cape Canaveral, 1962. Warm cream surfaces evoke mid-century modern interiors and briefing-room enamel. The orange accent pops like a launch button — reserved for primary actions, active navigation, and the metrics that matter. Navy text carries the gravity of atomic-age authority and engineering precision. The overall feel is optimistic, bold, and confident: the future is bright.

**Density**: Medium-high. Cards sit on a warm ground with 16px grid gaps; 20px internal padding keeps each card readable as its own instrument panel. Light, warm backgrounds tolerate tight layouts without feeling sterile.

**Philosophy**: Optimistic punk, not dystopia. Color celebrates progress — chart series stay saturated and legible; the shell stays clean (white cards, cream page, warm neutrals). Orange is the hero accent; use it where a user commits or where data demands attention. If the UI feels moody, cool-gray, or washed out, the theme has drifted off-genre.

**Atmosphere cues**:
- Warm cream surfaces (`#F0EAE0`) evoke mid-century modern interiors — never cool blue-gray page fills
- The orange accent reads as a **launch control** affordance — primary actions and key KPIs
- Navy primary text (`#1A2848`) signals authority and precision against white and cream
- Transitions stay brisk (150ms) and confident — mechanical, not bouncy
- **Rounded corners (`10px`)** echo 1950s dashboards and console bezels
- Shadows use a **navy tint at low opacity** so elevation stays on-brand

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH (approx.)             | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#F0EAE0` | `oklch(0.93 0.012 85)`      | `c1`       | `--bg`              |
| Card Surface        | `#FFFFFF` | `oklch(1 0 0)`              | `c2`       | `--surface`         |
| Surface Hover       | `#E8E2D8` | `oklch(0.90 0.012 85)`      | `c3`       | `--surface-hover`   |
| Primary Text        | `#1A2848` | `oklch(0.22 0.06 265)`      | `c58`      | `--text-primary`    |
| Secondary Text      | `#506070` | `oklch(0.45 0.03 235)`      | `c59`      | `--text-secondary`  |
| Border              | `#B8B0A4` | `oklch(0.76 0.018 85)`      | `c46`      | `--border`          |
| Border Light        | `#D8D0C8` | `oklch(0.86 0.012 85)`      | `c47`      | `--border-light`    |
| Accent              | `#FF6B35` | `oklch(0.68 0.19 45)`       | `c29`      | `--accent`          |
| Accent Muted        | `rgba(255,107,53,0.12)` | `oklch(0.68 0.19 45 / 0.12)` | —    | `--accent-muted`    |
| Accent Hover        | `#FF7E50` | `oklch(0.72 0.17 48)`       | `c30`      | `--accent-hover`    |
| Nav Background      | `#FFFFFF` | `oklch(1 0 0)`              | `c4`       | `--nav-bg`          |
| Nav Active          | `#E8E2D8` | `oklch(0.90 0.012 85)`      | `c5`       | `--nav-active`      |
| Header Background   | `#F0EAE0` | `oklch(0.93 0.012 85)`      | `c6`       | `--header-bg`       |
| Input Background    | `#FFFFFF` | `oklch(1 0 0)`              | `c7`       | `--input-bg`        |
| Input Border        | `#B8B0A4` | `oklch(0.76 0.018 85)`      | `c48`      | `--input-border`    |
| Tab Default BG      | `#FFFFFF` | `oklch(1 0 0)`              | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#FF6B35` | `oklch(0.68 0.19 45)`       | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#E8E2D8` | `oklch(0.90 0.012 85)`      | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#F5F2EC` | `oklch(0.95 0.008 85)`      | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#E8E2D8` | `oklch(0.90 0.012 85)`      | `c12`      | `--table-row-hover` |
| Grayscale 1 (near black) | `#0A1020` | `oklch(0.12 0.05 265)` | `c40`      | —                   |
| Grayscale 2         | `#121C38` | `oklch(0.18 0.055 265)`     | `c41`      | —                   |
| Grayscale 3         | `#1A2848` | `oklch(0.22 0.06 265)`      | `c42`      | —                   |
| Grayscale 4         | `#283A58` | `oklch(0.30 0.055 265)`     | `c43`      | —                   |
| Grayscale 5         | `#405070` | `oklch(0.40 0.045 265)`     | `c44`      | —                   |
| Grayscale 6         | `#506070` | `oklch(0.45 0.03 235)`      | `c45`      | —                   |
| Grayscale 7         | `#687888` | `oklch(0.55 0.025 240)`     | `c49`      | —                   |
| Grayscale 8         | `#8898A0` | `oklch(0.65 0.02 230)`      | `c50`      | —                   |
| Grayscale 9         | `#A8B0B0` | `oklch(0.74 0.015 220)`     | `c51`      | —                   |
| Grayscale 10        | `#C8C8C4` | `oklch(0.82 0.008 90)`      | `c52`      | —                   |
| Grayscale 11        | `#E0DCD4` | `oklch(0.90 0.012 85)`      | `c53`      | —                   |
| Grayscale 12 (near white) | `#F7F4EE` | `oklch(0.97 0.006 85)` | `c54`      | —                   |

**Light mode font slots**: `c58` = primary copy (`#1A2848`). `c59` = de-emphasized copy (`#506070`). **Always prefer explicit `c58` / `c59` over `c60` (AUTOMATIC_COLOR)** so navigation, cards, and headers stay consistent across theme swaps and match dark-theme documentation discipline.

**Navigation chrome**: Active items are indicated by **`navigation.activeColor` → `c29` (atomic orange)** — implement as App Studio’s **left accent bar** in atomic orange on the white nav (`c4`).

### 2.2 Status Colors

Light mode status badges use **light-tinted backgrounds** with **darker matching text** — readable on white cards, on-brand for atomic-age instrumentation.

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#20A0A0` | `#D8F0F0`  | `#106060` | `--on-track`     |
| At Risk  | `#FF6B35` | `#FFE8D8`  | `#A04018` | `--at-risk`      |
| Behind   | `#D04040` | `#F8D8D8`  | `#802020` | `--behind`       |
| Complete | `#D8A820` | `#FCF6E0`  | `#705810` | `--complete`     |

### 2.3 Shadows

Navy-tinted shadows at **low opacity** — anchored to `--text-primary` hue so halos feel atomic-age, not generic gray.

```css
--shadow:
  0px 0px 0px 1px oklch(0.22 0.06 265 / 0.08),
  0px 1px 2px -1px oklch(0.22 0.06 265 / 0.08),
  0px 2px 4px 0px oklch(0.22 0.06 265 / 0.06);
--shadow-hover:
  0px 0px 0px 1px oklch(0.22 0.06 265 / 0.10),
  0px 2px 4px -1px oklch(0.22 0.06 265 / 0.10),
  0px 4px 12px 0px oklch(0.22 0.06 265 / 0.08);
```

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
- **Never use Bold (700) or Black (900)** — they overpower the mid-century clarity

### 3.4 Text Color Rules

Primary text is **`#1A2848` (deep navy)**, not pure black — pure black feels harsh on warm cream and white. Secondary text at **`#506070`** (muted teal-gray) builds hierarchy without going drab. Chart axis labels, tooltips, and legend text use **`--text-secondary`**. KPI values and primary narrative use **`--text-primary`**.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#FFFFFF`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#1A2848`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#FF6B35`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

Depth comes from **navy-tinted shadow** on **white** over **cream** page — optional **4px left border** in accent or status color for hero KPIs.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#FFFFFF`  | `#B8B0A4` | `#506070` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#E8E2D8`  | `#FF6B35` | `#1A2848` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#FF6B35`  | `#FF6B35` | `#FFFFFF` | `--accent` / `--accent` / `--surface` |
| Disabled | `#F5F2EC`  | `#D8D0C8` | `#8898A0` | — |

Outline default; **6px** radius; transition `scale, background-color, border-color, box-shadow` at **150ms** ease-out; press **`scale(0.96)`**.

### 4.3 Inputs and Selects

| Property     | Value                     |
|-------------|---------------------------|
| Background  | `#FFFFFF` (`--surface`)   |
| Border      | `#B8B0A4` (`--border`)    |
| Text        | `#1A2848` (`--text-primary`) |
| Placeholder | `#8898A0` (`c50`)         |
| Focus border| `#FF6B35` (`--accent`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: light tint from Section 2.2 (on-track / at-risk / behind / complete)
- Text: darker matching tone from the same row
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#FFFFFF`             | `navigation.backgroundColor` → `c4` |
| Right border      | `1px solid #D8D0C8`   | Pro-code / layout CSS (`--border-light`) |
| Link text         | `#506070`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#1A2848`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#FF6B35`             | `navigation.activeColor` → `c29` (left accent bar) |
| Title text        | `#1A2848`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#E8E2D8`             | —                                    |

**Critical**: Use **`c58` / `c59` explicitly** for all navigation font colors — **never `c60`**. For parity with dark-theme docs and to prevent invisible text if a surface ever flips.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#F0EAE0`             | `headers.backgroundColor` → `c1` |
| Font color  | `#1A2848`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#E8E2D8`             | `tables.headerBG` → `c10`   |
| Header text     | `#506070`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#FFFFFF`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#F5F2EC`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#E8E2D8`             | `tables.hoverBG` → `c12`   |
| Row text        | `#1A2848`             | `tables.fontColor` → `c58` |
| Border          | `#D8D0C8`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#D8D0C8` (`--border-light`), 8px height, 4px radius
- Fill: status-colored or `--accent`; `width` transition **300ms** ease

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#FFFFFF` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 11px, uppercase, `#506070`  |
| Value        | 28px, SemiBold, accent or status or `#1A2848` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#FFFFFF`  | `#B8B0A4` | `#506070` |
| Hover   | `#E8E2D8`  | `#B8B0A4` | `#1A2848` |
| Active  | `#FF6B35`  | `#FF6B35` | `#FFFFFF` |

Active tab uses **full atomic-orange fill** with **white** label — the “launch” treatment for segmented controls.

---

## 5. Chart Palette

Default **data** palette: **Atomic Age Six** — saturated, legible hues for energy, aerospace, engineering, and innovation dashboards. **Do not** desaturate series for a “muted corporate” look; atompunk data should **pop** on white cards.

### 5.1 Series Colors with Mapping

| Series | Name           | Hex       | OKLCH (approx.)        | colorRange Index | CSS Variable |
|--------|----------------|-----------|------------------------|------------------|--------------|
| 1      | Atomic orange  | `#FF6B35` | `oklch(0.68 0.19 45)`  | `[0][0]`         | `--c1`       |
| 2      | Reactor teal   | `#20A0A0` | `oklch(0.62 0.10 195)` | `[1][0]`         | `--c2`       |
| 3      | Rocket red     | `#D04040` | `oklch(0.52 0.17 25)`  | `[2][0]`         | `--c3`       |
| 4      | Nuclear gold   | `#D8A820` | `oklch(0.76 0.14 90)`  | `[3][0]`         | `--c4`       |
| 5      | Space navy     | `#304880` | `oklch(0.38 0.09 265)` | `[4][0]`         | `--c5`       |
| 6      | Plutonium green| `#408050` | `oklch(0.52 0.10 145)` | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH (approx.)          | Theme JSON Key                  |
|-------------------|-----------|--------------------------|---------------------------------|
| Positive / Up     | `#20A0A0` | `oklch(0.62 0.10 195)`   | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#D04040` | `oklch(0.52 0.17 25)`    | `nameColorMap.NegativeColor`    |
| Total / Net       | `#506070` | `oklch(0.45 0.03 235)`   | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#1A2848` | `oklch(0.22 0.06 265)`   | —                               |
| Forecast          | `#FF7E50` | `oklch(0.72 0.17 48)`    | — (dashed stroke)               |
| Confidence Band   | `rgba(255,107,53,0.12)` | `oklch(0.68 0.19 45 / 0.12)` | — (area fill)     |
| Today Indicator   | `#D04040` | `oklch(0.52 0.17 25)`    | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#D8D0C8` (`--border-light`), 1px, opacity **0.5**
- Axis lines: `#B8B0A4` (`--border`), 1px
- Axis tick text: `#506070` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#FFFFFF` with `var(--shadow)`, 6px radius, `#1A2848` text, `#506070` secondary
- Legend text: `#506070`, 11px, Regular
- Active/hover series: opacity **1.0**; inactive series: opacity **0.3**

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#F0EAE0` (--bg)   | none                 | Page background                  |
| Raised   | `#FFFFFF` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#FFFFFF`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0.22 0.06 265 / 0.25)` | none         | Modal scrim (navy tint)          |

Light mode hierarchy favors **white instruments** on a **warm cream** field, with **navy-tinted** shadows — not flat gray slabs.

### 6.2 Border Usage

- Prefer **shadow** over heavy card outlines; subtle **1px** rings can reinforce white-on-cream separation
- Use **`1px solid var(--border-light)`** for dividers and table row separators
- Use **`1px solid var(--border)`** for inputs and persistent control outlines
- **Nav**: **`#FFFFFF`** surface with **`1px` right border** in `--border-light` — separates launch deck from mission content
- Avoid **2px+** structural borders except **status** or **left accent** bars (e.g. active nav, KPI emphasis)

---

## 7. Do's and Don'ts

### Do

- Use **warm cream (`#F0EAE0`)** for page background — **not** cool blue-gray
- Keep the **orange accent bold and confident** — this is optimistic **atompunk**, not pastel minimalism
- Use **`c58` / `c59`** for all documented font color slots — **the `c58` fix for consistency**; avoid `c60` in agent-authored theme JSON
- Use **navy (`#1A2848`)** for primary text authority on light surfaces
- Let **chart series stay saturated** — atompunk analytics should read like **instrument panels**, not washed reports
- Set `background: transparent` on pro-code app containers when the host card supplies the surface
- Use **navy-tinted shadows** at low opacity (Section 2.3)
- Apply **`font-variant-numeric: tabular-nums`** to dynamic numbers
- Give **active nav** a **left accent bar** in **atomic orange** (`c29`)

### Don't

- Use **dark / brooding** base colors — atompunk is about the **promise** of the future
- Use **muted or desaturated** chart colors as the default palette
- Use **`c60` (AUTOMATIC_COLOR)** for navigation or card typography when specifying importable themes — prefer explicit slots
- Use **`transition: all`** — specify exact properties
- Use font-weight **700** or **900** for dashboard UI type
- Fake **dark mode** by inverting this palette — **use a separate dark `DESIGN.md`**
- Rely on **pure black** (`#000000`) for text or shadow cores — anchor to **navy** instead

---

## 8. Light Mode Adaptation Notes

**This document defines a canonical LIGHT theme only.** Atompunk’s optimism, cream ground, and white nav are intentional; a brooding or charcoal-dark treatment belongs in a **different `DESIGN.md`** (with its own surfaces, badge logic, shadow stack, and JSON).

When an agent needs a dark variant:

1. **Do not** invert hex values or only flip lightness. Build a dedicated dark atompunk (or sibling) theme with appropriate contrast, table stripes, and status badges.

2. **App Studio**: Import the **dark** theme’s JSON when switching modes; re-apply **`c58` / `c59`** rules documented in that file (dark themes often map all nav font colors to a single light text slot).

3. **Pro-code**: Replace the entire `:root` token block and `COLORS` object with the target `DESIGN.md`; bump series **lightness/chroma** if charts sit on deep surfaces.

4. **Charts**: If the chart canvas drops below ~L 0.2, lighten series colors per `domo-app-theme` / `color-palettes.md` dark-adaptation guidance.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.93 0.012 85);
  --surface:        oklch(1 0 0);
  --surface-hover:  oklch(0.90 0.012 85);
  --text-primary:   oklch(0.22 0.06 265);
  --text-secondary: oklch(0.45 0.03 235);
  --border:         oklch(0.76 0.018 85);
  --border-light:   oklch(0.86 0.012 85);
  --accent:         oklch(0.68 0.19 45);
  --accent-muted:   oklch(0.68 0.19 45 / 0.12);
  --accent-hover:   oklch(0.72 0.17 48);

  --on-track:       oklch(0.62 0.10 195);
  --on-track-bg:    oklch(0.93 0.04 195);
  --on-track-text:  oklch(0.38 0.08 195);
  --at-risk:        oklch(0.68 0.19 45);
  --at-risk-bg:     oklch(0.95 0.04 45);
  --at-risk-text:   oklch(0.48 0.14 35);
  --behind:         oklch(0.52 0.17 25);
  --behind-bg:      oklch(0.94 0.03 25);
  --behind-text:    oklch(0.38 0.12 25);
  --complete:       oklch(0.76 0.14 90);
  --complete-bg:    oklch(0.97 0.03 95);
  --complete-text:  oklch(0.48 0.10 85);

  --shadow:
    0px 0px 0px 1px oklch(0.22 0.06 265 / 0.08),
    0px 1px 2px -1px oklch(0.22 0.06 265 / 0.08),
    0px 2px 4px 0px oklch(0.22 0.06 265 / 0.06);
  --shadow-hover:
    0px 0px 0px 1px oklch(0.22 0.06 265 / 0.10),
    0px 2px 4px -1px oklch(0.22 0.06 265 / 0.10),
    0px 4px 12px 0px oklch(0.22 0.06 265 / 0.08);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --c1: oklch(0.68 0.19 45);
  --c2: oklch(0.62 0.10 195);
  --c3: oklch(0.52 0.17 25);
  --c4: oklch(0.76 0.14 90);
  --c5: oklch(0.38 0.09 265);
  --c6: oklch(0.52 0.10 145);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #F0EAE0    Card bg      → c2   #FFFFFF
Hover bg     → c3   #E8E2D8    Nav bg       → c4   #FFFFFF
Primary text → c58  #1A2848    Secondary    → c59  #506070
Accent       → c29  #FF6B35    Accent hover → c30  #FF7E50
Border       → c46  #B8B0A4    Border light → c47  #D8D0C8
Font colors  → c58 / c59; NEVER c60 for importable JSON
Active nav   → activeColor c29 (left bar, atomic orange)
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#FF6B35',
  secondary: '#20A0A0',
  tertiary:  '#304880',
  surface:   '#FFFFFF',
  bg:        '#F0EAE0',
  text:      '#1A2848',
  textMuted: '#506070',
  border:    '#B8B0A4',
  positive:  '#20A0A0',
  negative:  '#D04040',
  series: ['#FF6B35', '#20A0A0', '#D04040', '#D8A820', '#304880', '#408050']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: White (`--surface`) on `--bg`, `var(--shadow)` only. Values 28px SemiBold `tabular-nums` in `--text-primary` or `--accent`; labels 11px Light uppercase in `--text-secondary`. Optional 4px left border in `--accent` or status color.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow from the `app-studio-pro-code` skill. Text `--text-primary`; gradients from `--surface` / `--bg`; glow from `--accent-muted`.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fills. `CartesianGrid` stroke `#D8D0C8` at 0.5 opacity. `XAxis` / `YAxis` tick fill `#506070`. Tooltip white surface, `var(--shadow)`, `#1A2848` body / `#506070` meta.

**"Add a forecast line with confidence band"**: `ComposedChart` with solid historical `--c1`, dashed forecast `--accent-hover`, `Area` confidence using `--accent-muted`. `ReferenceLine` “today” with `--c3` dashed stroke.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements all colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Atompunk",
  "colors": [
    { "index": 1, "value": "#F0EAE0", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#E8E2D8", "tag": "PRIMARY" },
    { "index": 4, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 5, "value": "#E8E2D8", "tag": "PRIMARY" },
    { "index": 6, "value": "#F0EAE0", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#FF6B35", "tag": "SECONDARY" },
    { "index": 10, "value": "#E8E2D8", "tag": "PRIMARY" },
    { "index": 11, "value": "#F5F2EC", "tag": "PRIMARY" },
    { "index": 12, "value": "#E8E2D8", "tag": "PRIMARY" },
    { "index": 29, "value": "#FF6B35", "tag": "SECONDARY" },
    { "index": 30, "value": "#FF7E50", "tag": "SECONDARY" },
    { "index": 40, "value": "#0A1020", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#121C38", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#1A2848", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#283A58", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#405070", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#506070", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#B8B0A4", "tag": "CUSTOM" },
    { "index": 47, "value": "#D8D0C8", "tag": "CUSTOM" },
    { "index": 48, "value": "#B8B0A4", "tag": "CUSTOM" },
    { "index": 49, "value": "#687888", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#8898A0", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#A8B0B0", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C8C8C4", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E0DCD4", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F7F4EE", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#1A2848", "tag": "FONT" },
    { "index": 59, "value": "#506070", "tag": "FONT" }
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
      "backgroundColor": { "type": "COLOR_REFERENCE", "index": 2 },
      "fontColor": { "type": "COLOR_REFERENCE", "index": 59 },
      "activeBackgroundColor": { "type": "COLOR_REFERENCE", "index": 29 },
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 2 },
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm **navigation** uses **`c59`** for default links, **`c58`** for titles and active link text, and **`c29`** for the **active indicator** (left accent bar in atomic orange). Confirm **tabs** use **`c2` (`#FFFFFF`)** for active label on **`c29`** fill. Verify cards, headers, and tables use **`c58`** — **not `c60`**. Add a **1px right border** on the nav in app layout CSS (`--border-light`) so the white nav separates from the cream canvas.
