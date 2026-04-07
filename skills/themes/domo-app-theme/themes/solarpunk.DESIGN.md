# Solarpunk — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Leaf green · **Mood**: Optimistic green tech, communal futures, sustainable growth, botanical intelligence

---

## 1. Visual Theme and Atmosphere

**Personality**: Greenhouse laboratory meets community garden. The shell is sun-warmed linen and clean white; growth reads in leaf green, not in neon alarms. Data feels cultivated, not manufactured.

**Density**: Medium-high. Cards sit on a 16px grid with 20px internal padding so each metric has room to breathe. Light cream ground keeps tight layouts from feeling clinical.

**Philosophy**: Organic restraint. Green is for **growth**, **active states**, and the **primary data series**—never for painting entire nav slabs or heavy chrome. If the UI feels like a synthetic dashboard skin, dial saturation down and let cream, sage, and earth tones carry structure. Chart colors stay botanical: leaf, sun, soil, sky, clay, moss—never electric cyan or magenta.

**Atmosphere cues**:
- Surfaces are **warm cream** (`#F5F0E4`) and **card white** (`#FFFFFF`)—never cold blue-gray page fills
- Corners at **10px** evoke seed pods and leaves; avoid sharp 2px radii on hero surfaces
- Transitions stay quick (**150ms**) and ease-out—responsive, not bouncy
- Depth comes from **olive-tinted shadows** at low opacity, not harsh black slabs
- Body text is **deep olive** (`#2C3828`), never pure black (`#000000`) or pure white (`#FFFFFF`) on light surfaces
- Status badges use **light botanical tints** (sage growth, straw amber, terra rose)—readable, warm, and forward-looking

**Best for**: Sustainability, ESG, renewable energy, agriculture, environmental monitoring, wellness, community analytics.

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#F5F0E4` | `oklch(0.96 0.018 95)`      | `c1`       | `--bg`              |
| Card Surface        | `#FFFFFF` | `oklch(1 0 0)`              | `c2`       | `--surface`         |
| Surface Hover       | `#E8EDE0` | `oklch(0.93 0.012 145)`     | `c3`       | `--surface-hover`   |
| Primary Text        | `#2C3828` | `oklch(0.28 0.022 145)`     | `c58`      | `--text-primary`    |
| Secondary Text      | `#5C6E58` | `oklch(0.48 0.028 145)`     | `c59`      | `--text-secondary`  |
| Border              | `#B0BCA8` | `oklch(0.78 0.022 145)`     | `c46`      | `--border`          |
| Border Light        | `#D4DCC8` | `oklch(0.88 0.018 140)`     | `c47`      | `--border-light`    |
| Accent              | `#38A060` | `oklch(0.62 0.12 150)`      | `c29`      | `--accent`          |
| Accent Muted        | `#38A0601F` | `oklch(0.62 0.12 150 / 0.12)` | —        | `--accent-muted`    |
| Accent Hover        | `#48B070` | `oklch(0.68 0.11 150)`      | `c30`      | `--accent-hover`    |
| Nav Background      | `#FFFFFF` | `oklch(1 0 0)`              | `c4`       | `--nav-bg`          |
| Nav Active          | `#F3F6EE` | `oklch(0.97 0.008 145)`     | `c5`       | `--nav-active`      |
| Header Background   | `#F5F0E4` | `oklch(0.96 0.018 95)`      | `c6`       | `--header-bg`       |
| Input Background    | `#FFFFFF` | `oklch(1 0 0)`              | `c7`       | `--input-bg`        |
| Input Border        | `#B0BCA8` | `oklch(0.78 0.022 145)`     | `c48`      | `--input-border`    |
| Tab Default BG      | `#FFFFFF` | `oklch(1 0 0)`              | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#38A060` | `oklch(0.62 0.12 150)`      | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#E8EDE0` | `oklch(0.93 0.012 145)`     | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#FAFAF6` | `oklch(0.99 0.004 95)`      | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#EEF3E8` | `oklch(0.95 0.015 145)`     | `c12`      | `--table-row-hover` |
| Grayscale 1 (near black) | `#141A16` | `oklch(0.14 0.015 145)` | `c40`      | —                   |
| Grayscale 2         | `#1C241F` | `oklch(0.18 0.018 145)`     | `c41`      | —                   |
| Grayscale 3         | `#242E28` | `oklch(0.22 0.020 145)`     | `c42`      | —                   |
| Grayscale 4         | `#303A34` | `oklch(0.28 0.022 145)`     | `c43`      | —                   |
| Grayscale 5         | `#3D4A42` | `oklch(0.35 0.025 145)`     | `c44`      | —                   |
| Grayscale 6         | `#4F5E54` | `oklch(0.45 0.028 145)`     | `c45`      | —                   |
| Grayscale 7         | `#6B7A66` | `oklch(0.55 0.025 145)`     | `c49`      | —                   |
| Grayscale 8         | `#889882` | `oklch(0.65 0.035 145)`     | `c50`      | —                   |
| Grayscale 9         | `#A8B4A0` | `oklch(0.75 0.025 145)`     | `c51`      | —                   |
| Grayscale 10        | `#C8D0C0` | `oklch(0.85 0.018 145)`     | `c52`      | —                   |
| Grayscale 11        | `#E0E8DA` | `oklch(0.92 0.015 145)`     | `c53`      | —                   |
| Grayscale 12 (near white) | `#F7F9F4` | `oklch(0.98 0.006 145)` | `c54`      | —                   |

**Light mode font slots**: `c58` = primary copy (deep olive). `c59` = muted forest. **Always use `c58` / `c59` explicitly** for navigation, headers, cards, and forms—even in light mode—so agents and imports stay consistent with dark-theme docs and avoid `c60` drift.

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#60C080` | `#E0F0E8`  | `#2C7040` | `--on-track`     |
| At Risk  | `#D8A020` | `#FFF0D0`  | `#8A6810` | `--at-risk`      |
| Behind   | `#C06040` | `#F8E0D8`  | `#8A3020` | `--behind`       |
| Complete | `#4890B8` | `#E4F0F6`  | `#2C6088` | `--complete`     |

Light mode status badges use **light botanical backgrounds** (straw, sage, terra, sky mist) with **darker matching text**—never neon fills on white cards.

### 2.3 Shadows

Shadow stacks use **`#2C3828` (deep olive) at low opacity** so halos feel organic on `#F5F0E4`, not sterile gray or pure black.

```css
--shadow:
  0px 0px 0px 1px oklch(0.28 0.022 145 / 0.06),
  0px 1px 2px -1px oklch(0.28 0.022 145 / 0.08),
  0px 2px 4px 0px oklch(0.28 0.022 145 / 0.05);
--shadow-hover:
  0px 0px 0px 1px oklch(0.28 0.022 145 / 0.08),
  0px 2px 4px -1px oklch(0.28 0.022 145 / 0.10),
  0px 4px 12px 0px oklch(0.28 0.022 145 / 0.07);
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
- **Never use Bold (700) or Black (900)** — they fight the soft, botanical shell

### 3.4 Text Color Rules

Primary text is **`#2C3828` (deep olive)**, not `#000000` and not `#FFFFFF` on light surfaces. Secondary text at **`#5C6E58` (muted forest)** builds hierarchy without turning chrome gray-cold.

Chart axis labels, tooltips, and legend text use **`--text-secondary`** (`#5C6E58`). Values that must read as primary content use **`--text-primary`**.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#FFFFFF`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#2C3828`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#38A060`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

Depth comes from **shadow** on white over cream—no heavy card outline. Optional KPI treatment: **4px left border** in accent or status color; keep the rest borderless and rounded.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#FFFFFF`  | `#B0BCA8` | `#5C6E58` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#E8EDE0`  | `#38A060` | `#2C3828` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#38A060`  | `#38A060` | `#FFFFFF` | `--accent` / `--accent` / `--surface` |
| Disabled | `#FAFAF6`  | `#D4DCC8` | `#A8B4A0` | — |

Ghost/outline default; **6px** radius; transition `scale, background-color, border-color, box-shadow` at **150ms** ease-out; press **`scale(0.96)`**. Prefer **rounded, organic** hit targets—no razor-thin sharp rectangles.

### 4.3 Inputs and Selects

| Property     | Value                     |
|-------------|---------------------------|
| Background  | `#FFFFFF` (`--surface`)   |
| Border      | `#B0BCA8` (`--border`)    |
| Text        | `#2C3828` (`--text-primary`) |
| Placeholder | `#889882` (`c50`)         |
| Focus border| `#38A060` (`--accent`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: light tint from Section 2.2 (sage, straw, terra, sky mist)
- Text: darker matching tone from the same row—not the neon primary on white alone
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius **`4px`** (soft, not square)

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#FFFFFF`             | `navigation.backgroundColor` → `c4` |
| Right border      | `1px solid #D4DCC8`   | Pro-code / page wrapper CSS (`--border-light`) — App Studio may require a layout wrapper for the visible rule |
| Link text         | `#5C6E58`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#2C3828`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#38A060`             | `navigation.activeColor` → `c29` (**leaf green left accent bar** — not a dark fill) |
| Title text        | `#2C3828`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#E8EDE0`             | — (`--surface-hover`)               |

**Critical**: All `*FontColor` navigation properties reference **`c58` / `c59`**, never **`c60`**, for consistency with theme documentation and cross-mode parity.

**Active item pattern**: Emphasize the **`activeColor`** bar in **`#38A060`**. Do **not** use a dark charcoal or near-black active row fill—this is a **light**, optimistic theme.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#F5F0E4`             | `headers.backgroundColor` → `c1` |
| Font color  | `#2C3828`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#E8EDE0`             | `tables.headerBG` → `c10`   |
| Header text     | `#5C6E58`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#FFFFFF`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#FAFAF6`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#EEF3E8`             | `tables.hoverBG` → `c12`    |
| Row text        | `#2C3828`             | `tables.fontColor` → `c58` |
| Border          | `#D4DCC8`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#D4DCC8` (`--border-light`), 8px height, **4px** radius
- Fill: status-colored or `--accent`; `width` transition **300ms** ease

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#FFFFFF` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 11px (or 12px if native), uppercase, `#5C6E58` |
| Value        | 28px, SemiBold, status-colored or `#2C3828` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#FFFFFF`  | `#B0BCA8` | `#5C6E58` |
| Hover   | `#E8EDE0`  | `#B0BCA8` | `#2C3828` |
| Active  | `#38A060`  | `#38A060` | `#2C3828` |

Active tab uses **leaf green** fill with **deep olive** labels so the control stays earthy, not fluorescent. If contrast testing fails on small labels, switch active tab text to `#FFFFFF` for that instance only.

---

## 5. Chart Palette

Default **data** palette: **botanical six**—leaf, solar gold, earth, sky, terracotta, moss. Keeps analytics warm, legible, and on-theme for ESG and outdoors contexts.

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#38A060` | `oklch(0.62 0.12 150)`      | `[0][0]`         | `--c1`       |
| 2      | `#C8A030` | `oklch(0.72 0.12 85)`       | `[1][0]`         | `--c2`       |
| 3      | `#8A6E40` | `oklch(0.52 0.08 75)`       | `[2][0]`         | `--c3`       |
| 4      | `#4890B8` | `oklch(0.62 0.10 230)`      | `[3][0]`         | `--c4`       |
| 5      | `#B87050` | `oklch(0.58 0.10 35)`       | `[4][0]`         | `--c5`       |
| 6      | `#3C6848` | `oklch(0.42 0.06 150)`      | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#60C080` | `oklch(0.72 0.14 155)`  | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#C06040` | `oklch(0.55 0.14 25)`   | `nameColorMap.NegativeColor`    |
| Total / Net       | `#5C6E58` | `oklch(0.48 0.028 145)` | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#2C3828` | `oklch(0.28 0.022 145)` | —                               |
| Forecast          | `#38A060` | `oklch(0.62 0.12 150)`  | — (dashed stroke)               |
| Confidence Band   | `#38A06033` | `oklch(0.62 0.12 150 / 0.20)` | — (area fill)            |
| Today Indicator   | `#C06040` | `oklch(0.55 0.14 25)`   | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#D4DCC8` (`--border-light`), 1px, opacity **0.5**
- Axis lines: `#B0BCA8` (`--border`), 1px
- Axis tick text: `#5C6E58` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#FFFFFF` with `var(--shadow)`, **6px** radius, `#2C3828` text, `#5C6E58` secondary
- Legend text: `#5C6E58`, 11px, Regular
- Active/hover series: opacity **1.0**; inactive series: opacity **0.3**
- Avoid **neon** or **synthetic** series colors; stay in the botanical lane

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#F5F0E4` (--bg)   | none                 | Page background                  |
| Raised   | `#FFFFFF` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#FFFFFF`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0.28 0.022 145 / 0.25)` | none         | Modal scrim (olive-tinted)       |

Light mode hierarchy = **white planes on warm cream**, reinforced by **olive-tinted shadows**—not saturated green fills in chrome.

### 6.2 Border Usage

- Prefer **shadow** over heavy card outlines; thin rings keep white cards crisp on cream
- Use `1px solid var(--border-light)` for dividers, table rules, and **nav right edge**
- Use `1px solid var(--border)` for inputs and persistent control outlines (accessibility)
- Avoid **2px+** structural borders except **status** or **left accent** bars (KPI, active nav)
- Favor **rounded** corners and gentle spacing—avoid sharp, angular “control room” framing

---

## 7. Do's and Don'ts

### Do

- Use **warm cream** (`#F5F0E4`) for the **page background** instead of cold blue-gray
- Keep **charts earthy and organic**—botanical series, muted grids, no neon accents
- Use **`c58` / `c59`** for all typography color references in App Studio theme JSON (**even in light mode**); avoid relying on **`c60`**
- Use **deep olive** (`#2C3828`) for primary text—not pure white text on light surfaces, not pure black
- Use **`--accent-muted`** (`rgba(56,160,96,0.12)` / `#38A0601F`) for fills, highlights, and confidence bands
- Tint **shadows** with **deep olive** at low opacity—not harsh pure-black stacks on linen
- Give the **active nav** item a **leaf green** (`#38A060`) **left accent** via `activeColor`—not a dark filled rail
- Set `background: transparent` on pro-code app containers when the host card supplies the surface
- Apply `font-variant-numeric: tabular-nums` to dynamic numbers

### Don't

- Use **pure white** (`#FFFFFF`) for **body text** on light cards—use deep olive
- Use **pure black** (`#000000`) for text—it reads harsh next to cream and sage
- Use **sharp, angular** layout language everywhere—this theme should feel **natural** and **welcoming**
- Use **neon** chart colors or **synthetic** rainbow defaults
- **Invert** this palette to fake dark mode—**use a dedicated dark DESIGN.md** and full theme swap instead
- Use **`transition: all`** — specify exact properties
- Use font-weight **700** or **900** for dashboard UI type
- Rely on **`c60`** (AUTOMATIC_COLOR) for nav or header fonts when documenting agent-importable themes

---

## 8. Light Mode Adaptation Notes

This document defines the **canonical Solarpunk light** shell—optimistic, sun-lit, botanical.

1. **This is a LIGHT theme.** Surfaces are **cream and white**; text is **deep olive** and **muted forest**; shadows are **olive-tinted** at low opacity.

2. **If reversing to dark mode: do NOT invert.** Do not flip only lightness channels or invert hex pairs. Dark mode needs its own surface/text/border system, badge logic, and shadow stack (see [charcoal-ember-dark.DESIGN.md](charcoal-ember-dark.DESIGN.md)). **Use a separate dark DESIGN.md and theme JSON.**

3. **App Studio**: Import the JSON in Section 10. Verify **`c58`** on titles, active nav labels, headers, cards, and forms—not **`c60`**.

4. **Pro-code CSS**: Replace the entire `:root` token block with Section 9.1; sync `COLORS.series` to Section 9.3. Use `background: transparent` on the app root when embedded in themed cards.

5. **Charts on dark surfaces**: If charts move to dark backgrounds later, bump series lightness per `domo-app-theme` / `color-palettes.md` dark-adaptation guidance—do not reuse this light JSON unchanged.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.96 0.018 95);
  --surface:        oklch(1 0 0);
  --surface-hover:  oklch(0.93 0.012 145);
  --text-primary:   oklch(0.28 0.022 145);
  --text-secondary: oklch(0.48 0.028 145);
  --border:         oklch(0.78 0.022 145);
  --border-light:   oklch(0.88 0.018 140);
  --accent:         oklch(0.62 0.12 150);
  --accent-hover:   oklch(0.68 0.11 150);
  --accent-muted:   oklch(0.62 0.12 150 / 0.12);

  --on-track:       oklch(0.72 0.14 155);
  --on-track-bg:    oklch(0.94 0.03 155);
  --on-track-text:  oklch(0.45 0.12 155);
  --at-risk:        oklch(0.78 0.14 85);
  --at-risk-bg:     oklch(0.97 0.04 90);
  --at-risk-text:   oklch(0.48 0.10 80);
  --behind:         oklch(0.55 0.14 25);
  --behind-bg:      oklch(0.95 0.04 25);
  --behind-text:    oklch(0.42 0.12 25);
  --complete:       oklch(0.62 0.10 230);
  --complete-bg:    oklch(0.94 0.02 230);
  --complete-text:  oklch(0.42 0.10 230);

  --shadow:
    0px 0px 0px 1px oklch(0.28 0.022 145 / 0.06),
    0px 1px 2px -1px oklch(0.28 0.022 145 / 0.08),
    0px 2px 4px 0px oklch(0.28 0.022 145 / 0.05);
  --shadow-hover:
    0px 0px 0px 1px oklch(0.28 0.022 145 / 0.08),
    0px 2px 4px -1px oklch(0.28 0.022 145 / 0.10),
    0px 4px 12px 0px oklch(0.28 0.022 145 / 0.07);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  /* Botanical chart series */
  --c1: oklch(0.62 0.12 150);
  --c2: oklch(0.72 0.12 85);
  --c3: oklch(0.52 0.08 75);
  --c4: oklch(0.62 0.10 230);
  --c5: oklch(0.58 0.10 35);
  --c6: oklch(0.42 0.06 150);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #F5F0E4    Card bg      → c2   #FFFFFF
Hover bg     → c3   #E8EDE0    Nav bg       → c4   #FFFFFF
Primary text → c58  #2C3828    Secondary    → c59  #5C6E58
Accent       → c29  #38A060    Accent hover → c30  #48B070
Border       → c46  #B0BCA8    Border light → c47  #D4DCC8
Nav accent bar → c29 (leaf green left indicator; not dark fill)
Font colors  → ALWAYS c58 / c59; NEVER c60 (for agent parity)
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#38A060',
  secondary: '#5C6E58',
  tertiary:  '#B0BCA8',
  surface:   '#FFFFFF',
  bg:        '#F5F0E4',
  text:      '#2C3828',
  textMuted: '#5C6E58',
  border:    '#B0BCA8',
  positive:  '#60C080',
  negative:  '#C06040',
  series: ['#38A060', '#C8A030', '#8A6E40', '#4890B8', '#B87050', '#3C6848']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: White (`--surface`) on `--bg`, `var(--shadow)` only. Values 28px SemiBold `tabular-nums`; labels 11px Light uppercase in `--text-secondary`. Optional 4px left border in `--accent` or a status color from Section 2.2.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow from the `app-studio-pro-code` skill. Text `--text-primary`; gradients from `--bg` / `--surface`; glow from `--accent-muted`.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fills. `CartesianGrid` stroke `#D4DCC8` at 0.5 opacity. `XAxis` / `YAxis` tick fill `#5C6E58`. Tooltip white surface, `var(--shadow)`, `#2C3828` body / `#5C6E58` meta.

**"Add a forecast line with confidence band"**: `ComposedChart` with solid historical `--c1`, dashed forecast `--accent`, `Area` confidence using `--accent-muted`. `ReferenceLine` “today” with `--behind` dashed stroke.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Solarpunk",
  "colors": [
    { "index": 1, "value": "#F5F0E4", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#E8EDE0", "tag": "PRIMARY" },
    { "index": 4, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 5, "value": "#F3F6EE", "tag": "PRIMARY" },
    { "index": 6, "value": "#F5F0E4", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#38A060", "tag": "SECONDARY" },
    { "index": 10, "value": "#E8EDE0", "tag": "PRIMARY" },
    { "index": 11, "value": "#FAFAF6", "tag": "PRIMARY" },
    { "index": 12, "value": "#EEF3E8", "tag": "PRIMARY" },
    { "index": 29, "value": "#38A060", "tag": "SECONDARY" },
    { "index": 30, "value": "#48B070", "tag": "SECONDARY" },
    { "index": 40, "value": "#141A16", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#1C241F", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#242E28", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#303A34", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#3D4A42", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#4F5E54", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#B0BCA8", "tag": "CUSTOM" },
    { "index": 47, "value": "#D4DCC8", "tag": "CUSTOM" },
    { "index": 48, "value": "#B0BCA8", "tag": "CUSTOM" },
    { "index": 49, "value": "#6B7A66", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#889882", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#A8B4A0", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C8D0C0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E0E8DA", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F7F9F4", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#2C3828", "tag": "FONT" },
    { "index": 59, "value": "#5C6E58", "tag": "FONT" }
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
      "activeFontColor": { "type": "COLOR_REFERENCE", "index": 58 },
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm **navigation** uses **`c59`** for default links, **`c58`** for titles and active labels, and **`c29`** for the **active indicator** (leaf green bar). Add a **`1px` right border** on the nav column in pro-code or layout CSS using **`#D4DCC8`** if the host frame does not draw it automatically. Verify cards and headers use **`c58`** for body/titles—not **`c60`**.
