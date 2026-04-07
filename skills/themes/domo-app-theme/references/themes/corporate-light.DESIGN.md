# Corporate Light — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Cool blue-gray · **Mood**: Professional, trustworthy, clean

---

## 1. Visual Theme and Atmosphere

**Personality**: Corporate boardroom, not startup. The chrome is calm and authoritative; hierarchy comes from type weight, spacing, and soft elevation—not from a loud brand color. Surfaces read as crisp white on a pale blue-gray canvas.

**Density**: Medium-high. Cards pack tightly with 16px gaps; internal padding stays at 20px so each card reads as its own document. Light backgrounds tolerate tight grids without feeling cramped.

**Philosophy**: Restraint. There is no bold primary “brand fill” in the UI shell—only a cool blue-gray accent (`#99CCEE`) for hover rings, active tabs, and subtle emphasis. Saturated color belongs in **data** (chart series, status, KPI semantics), not in navigation chrome or card frames. If structural UI starts competing with chart colors, the design has failed.

**Atmosphere cues**:
- Surfaces are **white on pale blue-gray** (`#FFFFFF` on `#F1F6FA`)—never pure gray slabs
- Transitions stay fast (150ms) and linear-ease; motion feels efficient, not playful
- Depth comes from **layered shadows** tinted from `--text-primary` at low opacity—not heavy outlines
- Body text is **soft charcoal** (`#3F454D`), never pure black (`#000000`)—pure black feels harsh on white and cheap next to Domo-native patterns

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                       | Theme Slot | CSS Variable        |
|---------------------|-----------|-----------------------------|------------|---------------------|
| Page Background     | `#F1F6FA` | `oklch(0.962 0.011 240)`    | `c1`       | `--bg`              |
| Card Surface        | `#FFFFFF` | `oklch(1 0 0)`              | `c2`       | `--surface`         |
| Surface Hover       | `#F8FAFC` | `oklch(0.979 0.004 240)`    | `c3`       | `--surface-hover`   |
| Primary Text        | `#3F454D` | `oklch(0.374 0.014 256)`    | `c58`      | `--text-primary`    |
| Secondary Text      | `#68737F` | `oklch(0.510 0.016 249)`    | `c59`      | `--text-secondary`  |
| Border              | `#B7C1CB` | `oklch(0.800 0.015 240)`    | `c46`      | `--border`          |
| Border Light        | `#DCE4EA` | `oklch(0.908 0.009 240)`    | `c47`      | `--border-light`    |
| Accent              | `#99CCEE` | `oklch(0.816 0.065 230)`    | `c29`      | `--accent` (same as SKILL `--accent-hover`) |
| Accent Muted        | `#99CCEE26` | `oklch(0.816 0.065 230 / 0.15)` | —      | `--accent-muted`    |
| Accent Pressed      | `#7AB3D8` | `oklch(0.72 0.08 230)`      | `c30`      | `--accent-pressed`  |
| Nav Background      | `#EDF3F8` | `oklch(0.965 0.012 240)`    | `c4`       | `--nav-bg`          |
| Nav Active          | `#DCE4EA` | `oklch(0.908 0.009 240)`    | `c5`       | `--nav-active`      |
| Header Background   | `#F1F6FA` | `oklch(0.962 0.011 240)`    | `c6`       | `--header-bg`       |
| Input Background    | `#FFFFFF` | `oklch(1 0 0)`              | `c7`       | `--input-bg`        |
| Input Border        | `#B7C1CB` | `oklch(0.800 0.015 240)`    | `c48`      | `--input-border`    |
| Tab Default BG      | `#FFFFFF` | `oklch(1 0 0)`              | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#99CCEE` | `oklch(0.816 0.065 230)`    | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#EFF4F9` | `oklch(0.965 0.010 240)`    | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#F8FAFC` | `oklch(0.979 0.004 240)`    | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#F1F6FA` | `oklch(0.962 0.011 240)`    | `c12`      | `--table-row-hover` |
| Grayscale 1 (near black) | `#0E1318` | `oklch(0.12 0.02 250)` | `c40`      | —                   |
| Grayscale 2         | `#161C22` | `oklch(0.16 0.018 250)`     | `c41`      | —                   |
| Grayscale 3         | `#1F262D` | `oklch(0.20 0.016 250)`     | `c42`      | —                   |
| Grayscale 4         | `#2A323A` | `oklch(0.26 0.014 256)`     | `c43`      | —                   |
| Grayscale 5         | `#3F454D` | `oklch(0.374 0.014 256)`    | `c44`      | —                   |
| Grayscale 6         | `#55606A` | `oklch(0.45 0.014 250)`     | `c45`      | —                   |
| Grayscale 7         | `#68737F` | `oklch(0.510 0.016 249)`    | `c49`      | —                   |
| Grayscale 8         | `#88929C` | `oklch(0.60 0.012 250)`     | `c50`      | —                   |
| Grayscale 9         | `#A8B2BC` | `oklch(0.72 0.010 250)`     | `c51`      | —                   |
| Grayscale 10        | `#C5CDD5` | `oklch(0.82 0.008 250)`     | `c52`      | —                   |
| Grayscale 11        | `#E2E9EF` | `oklch(0.92 0.006 240)`     | `c53`      | —                   |
| Grayscale 12 (near white) | `#F7FAFC` | `oklch(0.98 0.004 240)` | `c54`      | —                   |

**Light mode font slots**: `c58` = FONT, dark text (`#3F454D`). `c59` = FONT, secondary text (`#68737F`). `c60` (AUTOMATIC_COLOR) defaults to dark text on light backgrounds and is **safe** in light mode—but **prefer `c58` / `c59` explicitly** for parity with dark-theme documents and to avoid silent breakage if a surface flips to dark later.

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#ADD4C1` | `#E8F3EC`  | `#4A7A5A` | `--on-track`     |
| At Risk  | `#FF9922` | `#FFF0DD`  | `#C47A10` | `--at-risk`      |
| Behind   | `#776CB0` | `#EAE7F3`  | `#5A5094` | `--behind`       |
| Complete | `#99CCEE` | `#E0F0FA`  | `#5A9ABE` | `--complete`     |

Light mode status badges use **light-tinted backgrounds** (high L, low chroma) with **darker matching text**—never neon fills on white cards.

### 2.3 Shadows

Shadow color is **`--text-primary` at low opacity** so the halo stays cool-neutral and coherent on `#F1F6FA`.

```css
--shadow:
  0px 0px 0px 1px oklch(0.374 0.014 256 / 0.06),
  0px 1px 2px -1px oklch(0.374 0.014 256 / 0.06),
  0px 2px 4px 0px oklch(0.374 0.014 256 / 0.04);
--shadow-hover:
  0px 0px 0px 1px oklch(0.374 0.014 256 / 0.08),
  0px 2px 4px -1px oklch(0.374 0.014 256 / 0.08),
  0px 4px 12px 0px oklch(0.374 0.014 256 / 0.06);
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
- **Never use Bold (700) or Black (900)** — they overpower the minimal aesthetic

### 3.4 Text Color Rules

Primary text is `#3F454D` (soft charcoal), not `#000000`. Secondary text at `#68737F` builds a two-tier hierarchy without introducing hue noise. Chart axis labels, tooltips, and legend text use `--text-secondary` (`#68737F`). Only values that must read as “primary content” use `--text-primary`.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#FFFFFF`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#3F454D`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#99CCEE`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

Prefer **shadow** over a visible card border. Optional KPI treatment: **4px left border** in a status or series color—keep the rest borderless.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#FFFFFF`  | `#B7C1CB` | `#68737F` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#DCE4EA`  | `#99CCEE` | `#3F454D` | `--border-light` / `--accent-hover` / `--text-primary` |
| Active   | `#3F454D`  | `#3F454D` | `#FFFFFF` | `--text-primary` / `--text-primary` / `--surface` |
| Disabled | `#F8FAFC`  | `#DCE4EA` | `#A8B2BC` | — |

Ghost/outline default; **6px** radius; transition `scale, background-color, border-color, box-shadow` at **150ms** ease-out; press **`scale(0.96)`**.

### 4.3 Inputs and Selects

| Property     | Value                     |
|-------------|---------------------------|
| Background  | `#FFFFFF` (`--surface`)   |
| Border      | `#B7C1CB` (`--border`)    |
| Text        | `#3F454D` (`--text-primary`) |
| Placeholder | `#88929C` (`c50`)         |
| Focus border| `#99CCEE` (`--accent-hover`)    |
| Radius      | `6px`                     |
| Font        | 13px, weight 600          |

### 4.4 Status Badges

- Background: light tint from the status row (Section 2.2)
- Text: darker matching tone (not the neon primary on white)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#EDF3F8`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#68737F`             | `navigation.linkFontColor` → `c59`  |
| Active link text  | `#3F454D`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#99CCEE`             | `navigation.activeColor` → `c29` (`--accent-hover`) |
| Title text        | `#3F454D`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#DCE4EA`             | —                                    |

**Consistency**: Prefer explicit `c58` / `c59` for nav typography. `c60` works on light surfaces but hides intent when themes are reused across modes.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#F1F6FA`             | `headers.backgroundColor` → `c1` |
| Font color  | `#3F454D`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#EFF4F9`             | `tables.headerBG` → `c10`   |
| Header text     | `#68737F`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#FFFFFF`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#F8FAFC`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#F1F6FA`             | `tables.hoverBG` → `c12`    |
| Row text        | `#3F454D`             | `tables.fontColor` → `c58` |
| Border          | `#DCE4EA`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#DCE4EA` (`--border-light`), 8px height, 4px radius
- Fill: status-colored; `width` transition **300ms** ease

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#FFFFFF` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 11px (or 12px if native), uppercase, `#68737F` |
| Value        | 28px, SemiBold, status-colored or `#3F454D` |
| Shadow       | `var(--shadow)`             |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#FFFFFF`  | `#B7C1CB` | `#68737F` |
| Hover   | `#F8FAFC`  | `#B7C1CB` | `#3F454D` |
| Active  | `#99CCEE`  | `#99CCEE` | `#3F454D` |

Active tab uses the **soft accent fill** with **charcoal text**—large accent fields stay low-chroma by design.

---

## 5. Chart Palette

Default **data** palette: **Pacific Drift** (palette `#1` in [color-palettes.md](../color-palettes.md))—analogous teal → blue, built for corporate analytics.

### 5.1 Series Colors with Mapping

Hex values below are **sRGB approximations** of the OKLCH coordinates; prefer **OKLCH in CSS** when authoring.

| Series | Hex (approx.) | OKLCH                       | colorRange Index | CSS Variable |
|--------|---------------|-----------------------------|------------------|--------------|
| 1      | `#3A98AB`     | `oklch(0.63 0.11 195)`      | `[0][0]`         | `--c1`       |
| 2      | `#3A92BC`     | `oklch(0.63 0.11 210)`      | `[1][0]`         | `--c2`       |
| 3      | `#458BC6`     | `oklch(0.63 0.11 225)`      | `[2][0]`         | `--c3`       |
| 4      | `#5283CF`     | `oklch(0.63 0.11 238)`      | `[3][0]`         | `--c4`       |
| 5      | `#449696`     | `oklch(0.63 0.09 183)`      | `[4][0]`         | `--c5`       |
| 6      | `#7D81C7`     | `oklch(0.63 0.09 250)`      | `[5][0]`         | `--c6`       |

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH                   | Theme JSON Key                  |
|-------------------|-----------|-------------------------|---------------------------------|
| Positive / Up     | `#ADD4C1` | `oklch(0.835 0.065 155)` | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#E45F5F` | `oklch(0.590 0.160 20)`  | `nameColorMap.NegativeColor`    |
| Total / Net       | `#68737F` | `oklch(0.510 0.016 249)` | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#3F454D` | `oklch(0.374 0.014 256)` | —                               |
| Forecast          | `#99CCEE` | `oklch(0.816 0.065 230)` | — (dashed; `--accent-hover`)    |
| Confidence Band   | `#99CCEE33` | `oklch(0.816 0.065 230 / 0.20)` | — (area fill)            |
| Today Indicator   | `#E45F5F` | `oklch(0.590 0.160 20)`  | —                               |

### 5.3 Chart Styling Rules

- Grid lines: `#DCE4EA` (`--border-light`), 1px, opacity **0.5**
- Axis lines: `#B7C1CB` (`--border`), 1px
- Axis tick text: `#68737F` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#FFFFFF` with `var(--shadow)`, 6px radius, `#3F454D` text, `#68737F` secondary
- Legend text: `#68737F`, 11px, Regular
- Active/hover series: opacity **1.0**; inactive series: opacity **0.3**

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|----------------------|----------------------------------|
| Ground   | `#F1F6FA` (--bg)   | none                 | Page background                  |
| Raised   | `#FFFFFF` (--surface) | `var(--shadow)`   | Cards, panels, containers        |
| Floating | `#FFFFFF`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers   |
| Overlay  | `oklch(0.374 0.014 256 / 0.25)` | none         | Modal scrim (text-primary tint)  |

Light mode hierarchy leans on **white planes** on a tinted ground, reinforced by **soft shadows**—not on saturated fills.

### 6.2 Border Usage

- Prefer **shadow** over heavy card outlines; 1px shadow rings read as crisp edges without visual noise
- Use `1px solid var(--border-light)` for dividers and table row separators
- Use `1px solid var(--border)` for inputs and persistent control outlines (accessibility)
- Avoid **2px+** structural borders except status accents (e.g., 4px left KPI border)

---

## 7. Do's and Don'ts

### Do

- Use **`c58`** for primary copy and **`c59`** for de-emphasized UI copy; prefer explicit slots over **`c60`** for cross-theme consistency
- Let **chart series** carry hue; keep chrome neutral (white, pale gray, soft blue-gray accent)
- Use **`#3F454D`** (or OKLCH equivalent) instead of pure black for body text
- Prefer **`box-shadow`** (`--shadow` / `--shadow-hover`) over thick borders for cards and floating surfaces
- Set `background: transparent` on pro-code app containers embedded in App Studio cards when the host card supplies the surface
- Apply `font-variant-numeric: tabular-nums` to all dynamic numbers
- Tint shadows with **`--text-primary` opacity**, not pure black stacks (unless debugging contrast in isolation)

### Don't

- Use **pure black** (`#000000`) for text or shadows in the product UI
- Use **heavy 2px+ borders** around every card—“spreadsheet grid” breaks the executive tone
- Put **bright saturated colors** on structural elements (nav bars, full-width headers, default buttons)
- Use **`transition: all`** — specify exact properties
- Use font-weight **700** or **900** for dashboard UI type
- Invert lightness-only to “fake” dark mode — **swap to a dark DESIGN.md** instead
- Rely on **`c60`** alone when documenting themes agents will port to dark surfaces later

---

## 8. Light Mode Adaptation Notes

This document defines the **canonical light** shell for executive and corporate analytics. When an agent is asked to “go dark” or match a night-mode executive view:

1. **Do not invert** light hex values or flip only L channels. Dark mode requires its own surface/text/border system, badge logic, and shadow stack (see [charcoal-ember-dark.DESIGN.md](charcoal-ember-dark.DESIGN.md) and the `domo-app-theme` skill dark-mode table).

2. **App Studio**: Import the dark theme’s JSON and apply its **`c58` / `c60` guidance**—dark themes replace `c60` with `c58` where documented; light themes may use `c60` safely but should still prefer explicit font slots.

3. **Pro-code CSS**: Replace the `:root` token block entirely with the target mode’s DESIGN.md block; update `COLORS.series` to a dark-adjusted palette when charts sit on `#1x` surfaces.

4. **Charts**: If the background drops below ~L 0.2, bump series lightness per `domo-app-theme` / `color-palettes.md` dark-adaptation recipe (+0.10–0.15 L, −0.02 C).

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.962 0.011 240);
  --surface:        oklch(1 0 0);
  --surface-hover:  oklch(0.979 0.004 240);
  --text-primary:   oklch(0.374 0.014 256);
  --text-secondary: oklch(0.510 0.016 249);
  --border:         oklch(0.800 0.015 240);
  --border-light:   oklch(0.908 0.009 240);
  --accent:         oklch(0.816 0.065 230);
  --accent-hover:   oklch(0.816 0.065 230);
  --accent-muted:   oklch(0.816 0.065 230 / 0.15);
  --accent-pressed: oklch(0.72 0.08 230);

  --on-track:       oklch(0.835 0.065 155);
  --on-track-bg:    oklch(0.943 0.025 155);
  --on-track-text:  oklch(0.520 0.060 155);
  --at-risk:        oklch(0.740 0.155 60);
  --at-risk-bg:     oklch(0.960 0.035 75);
  --at-risk-text:   oklch(0.580 0.110 60);
  --behind:         oklch(0.545 0.100 290);
  --behind-bg:      oklch(0.930 0.025 290);
  --behind-text:    oklch(0.440 0.080 290);
  --complete:       oklch(0.816 0.065 230);
  --complete-bg:    oklch(0.940 0.025 230);
  --complete-text:  oklch(0.660 0.060 230);

  --alert:          oklch(0.590 0.160 20);

  --shadow:
    0px 0px 0px 1px oklch(0.374 0.014 256 / 0.06),
    0px 1px 2px -1px oklch(0.374 0.014 256 / 0.06),
    0px 2px 4px 0px oklch(0.374 0.014 256 / 0.04);
  --shadow-hover:
    0px 0px 0px 1px oklch(0.374 0.014 256 / 0.08),
    0px 2px 4px -1px oklch(0.374 0.014 256 / 0.08),
    0px 4px 12px 0px oklch(0.374 0.014 256 / 0.06);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  /* Pacific Drift — default chart series */
  --c1: oklch(0.63 0.11 195);
  --c2: oklch(0.63 0.11 210);
  --c3: oklch(0.63 0.11 225);
  --c4: oklch(0.63 0.11 238);
  --c5: oklch(0.63 0.09 183);
  --c6: oklch(0.63 0.09 250);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #F1F6FA    Card bg      → c2   #FFFFFF
Hover bg     → c3   #F8FAFC    Nav bg       → c4   #EDF3F8
Primary text → c58  #3F454D    Secondary    → c59  #68737F
Accent       → c29  #99CCEE    Border       → c46  #B7C1CB
Font colors  → c58 (primary) / c59 (muted); prefer explicit slots over c60 for docs parity
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#99CCEE',
  secondary: '#68737F',
  tertiary:  '#B7C1CB',
  surface:   '#FFFFFF',
  bg:        '#F1F6FA',
  text:      '#3F454D',
  textMuted: '#68737F',
  border:    '#B7C1CB',
  positive:  '#ADD4C1',
  negative:  '#E45F5F',
  series: ['#3A98AB', '#3A92BC', '#458BC6', '#5283CF', '#449696', '#7D81C7']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: White (`--surface`) cards on `--bg`, `var(--shadow)` only—no heavy borders. Values at 28px SemiBold with `tabular-nums`; labels 11px Light uppercase in `--text-secondary`. Optional 4px left border in a status color.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow from the `app-studio-pro-code` skill. Text `--text-primary`; gradients anchored to `--surface` / `--bg`; glow from `--accent-muted`.

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fills. `CartesianGrid` stroke `#DCE4EA` at 0.5 opacity. `XAxis` / `YAxis` tick fill `#68737F`. Tooltip white surface, `var(--shadow)`, `#3F454D` body / `#68737F` meta.

**"Add a forecast line with confidence band"**: `ComposedChart` with solid historical `--c1`, dashed forecast `--accent-hover`, `Area` confidence using `--accent-muted`. `ReferenceLine` “today” with `--alert` dashed stroke.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Corporate Light",
  "colors": [
    { "index": 1, "value": "#F1F6FA", "tag": "PRIMARY" },
    { "index": 2, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 3, "value": "#F8FAFC", "tag": "PRIMARY" },
    { "index": 4, "value": "#EDF3F8", "tag": "PRIMARY" },
    { "index": 5, "value": "#DCE4EA", "tag": "PRIMARY" },
    { "index": 6, "value": "#F1F6FA", "tag": "PRIMARY" },
    { "index": 7, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 8, "value": "#FFFFFF", "tag": "PRIMARY" },
    { "index": 9, "value": "#99CCEE", "tag": "SECONDARY" },
    { "index": 10, "value": "#EFF4F9", "tag": "PRIMARY" },
    { "index": 11, "value": "#F8FAFC", "tag": "PRIMARY" },
    { "index": 12, "value": "#F1F6FA", "tag": "PRIMARY" },
    { "index": 29, "value": "#99CCEE", "tag": "SECONDARY" },
    { "index": 30, "value": "#7AB3D8", "tag": "SECONDARY" },
    { "index": 40, "value": "#0E1318", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#161C22", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#1F262D", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#2A323A", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#3F454D", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#55606A", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#B7C1CB", "tag": "CUSTOM" },
    { "index": 47, "value": "#DCE4EA", "tag": "CUSTOM" },
    { "index": 48, "value": "#B7C1CB", "tag": "CUSTOM" },
    { "index": 49, "value": "#68737F", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#88929C", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#A8B2BC", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#C5CDD5", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#E2E9EF", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F7FAFC", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#3F454D", "tag": "FONT" },
    { "index": 59, "value": "#68737F", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm navigation uses **`c59`** for default links and **`c58`** for titles/active links; cards and headers use **`c58`** for body/titles.
