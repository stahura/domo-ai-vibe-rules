# Cyberpunk — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Neon cyan · **Mood**: Blade Runner meets Tron — neon on absolute black, digital rain, holographic overlays, terminal aesthetics

**Best for**: Tech monitoring, cybersecurity, network analytics, DevOps, real-time systems, SOC-style operations views.

---

## 1. Visual Theme and Atmosphere

**Personality**: Hacker's command terminal meets executive dashboard. The chrome stays invisible; the story is told by luminous data on deep, cool void.

**Density**: Medium-high. Cards sit on a near-black canvas with 16px grid gaps; internal padding stays at 20px so dense telemetry still reads as deliberate panels, not clutter.

**Philosophy**: Neon is scarce and intentional. Cyan and sister neons appear only for data ink, focus rings, active controls, and single hero metrics — never as page-fill or large field backgrounds. If more than ~20% of visible pixels read as neon, the design has failed.

**Atmosphere cues**:
- Surfaces read like **LCD panels on black glass** — cool blue-gray lifts, not warm paper
- **Grid lines** use `--border` at ~**0.3 opacity** for a subtle matrix trace without visual noise
- **Tooltips** carry a **soft glow** (`box-shadow` with accent at low opacity) so they feel like HUD readouts, not flat boxes
- **Chart plot areas** feel **holographic** — series and grids float on darkness; backgrounds stay empty
- Motion stays crisp (150–200ms), linear or ease-out — no playful bounce; this is infrastructure UI
- **Primary text is cyan-white (`#C8E0F0`)**, never pure white — pure `#FFFFFF` flares on OLED-style blacks

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH (approx.)              | Theme Slot | CSS Variable        |
|---------------------|-----------|------------------------------|------------|---------------------|
| Page Background     | `#0A0E14` | `oklch(0.10 0.02 250)`       | `c1`       | `--bg`              |
| Card Surface        | `#141A24` | `oklch(0.14 0.025 250)`      | `c2`       | `--surface`         |
| Surface Hover       | `#1C2430` | `oklch(0.18 0.03 250)`       | `c3`       | `--surface-hover`   |
| Primary Text        | `#C8E0F0` | `oklch(0.88 0.04 230)`       | `c58`      | `--text-primary`    |
| Secondary Text      | `#607080` | `oklch(0.52 0.04 240)`       | `c59`      | `--text-secondary`  |
| Border              | `#1E2838` | `oklch(0.22 0.03 250)`       | `c46`      | `--border`          |
| Border Light        | `#182030` | `oklch(0.18 0.025 255)`      | `c47`      | `--border-light`    |
| Accent              | `#00E5FF` | `oklch(0.86 0.14 215)`       | `c29`      | `--accent`          |
| Accent Muted        | `rgba(0,229,255,0.12)` | `oklch(0.86 0.14 215 / 0.12)` | —   | `--accent-muted`    |
| Accent Hover        | `#40F0FF` | `oklch(0.90 0.12 210)`       | `c30`      | `--accent-hover`    |
| Nav Background      | `#0E1218` | `oklch(0.11 0.02 255)`       | `c4`       | `--nav-bg`          |
| Nav Active          | `#1C2430` | `oklch(0.18 0.03 250)`       | `c5`       | `--nav-active`      |
| Header Background   | `#0A0E14` | `oklch(0.10 0.02 250)`       | `c6`       | `--header-bg`       |
| Input Background    | `#141A24` | `oklch(0.14 0.025 250)`      | `c7`       | `--input-bg`        |
| Input Border        | `#1E2838` | `oklch(0.22 0.03 250)`       | `c48`      | `--input-border`    |
| Tab Default BG      | `#141A24` | `oklch(0.14 0.025 250)`      | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#00E5FF` | `oklch(0.86 0.14 215)`       | `c29`      | `--tab-active-bg`   |
| Table Header BG     | `#0E1218` | `oklch(0.11 0.02 255)`       | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#10151C` | `oklch(0.12 0.02 252)`       | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#1C2430` | `oklch(0.18 0.03 250)`       | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#000000` | `oklch(0 0 0)`               | `c40`      | —                   |
| Grayscale 2         | `#05070A` | `oklch(0.06 0.015 260)`      | `c41`      | —                   |
| Grayscale 3         | `#0A0E14` | `oklch(0.10 0.02 250)`       | `c42`      | —                   |
| Grayscale 4         | `#141A24` | `oklch(0.14 0.025 250)`      | `c43`      | —                   |
| Grayscale 5         | `#1E2838` | `oklch(0.22 0.03 250)`       | `c44`      | —                   |
| Grayscale 6         | `#2A3444` | `oklch(0.28 0.03 248)`       | `c45`      | —                   |
| Grayscale 7         | `#4A5568` | `oklch(0.42 0.03 245)`       | `c49`      | —                   |
| Grayscale 8         | `#607080` | `oklch(0.52 0.04 240)`       | `c50`      | —                   |
| Grayscale 9         | `#8A9EB0` | `oklch(0.68 0.03 235)`       | `c51`      | —                   |
| Grayscale 10        | `#B0C8D8` | `oklch(0.80 0.03 230)`       | `c52`      | —                   |
| Grayscale 11        | `#C8E0F0` | `oklch(0.88 0.04 230)`       | `c53`      | —                   |
| Grayscale 12        | `#E0EEF8` | `oklch(0.94 0.02 230)`       | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#39FF14` | `#0E1A12`  | `#39FF14` | `--on-track`     |
| At Risk  | `#FFB020` | `#1A140A`  | `#FFB020` | `--at-risk`      |
| Behind   | `#FF2D8A` | `#1A0E16`  | `#FF2D8A` | `--behind`       |
| Complete | `#40F0FF` | `#0E1820`  | `#40F0FF` | `--complete`     |

Dark mode status badges use **dark-tinted backgrounds** (L ~0.10–0.12) with **neon text** matching the status primary. Never use light pastel badge fills on these surfaces — they read as broken glass, not HUD chrome.

### 2.3 Shadows

Pure **black** only, at **0.30–0.45** opacity across three layers — dark void eats colored shadows.

```css
--shadow:
  0px 0px 0px 1px rgba(0, 0, 0, 0.30),
  0px 1px 3px -1px rgba(0, 0, 0, 0.40),
  0px 2px 6px 0px rgba(0, 0, 0, 0.35);
--shadow-hover:
  0px 0px 0px 1px rgba(0, 0, 0, 0.38),
  0px 2px 6px -1px rgba(0, 0, 0, 0.45),
  0px 4px 12px 0px rgba(0, 0, 0, 0.30);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** family for **all** font slots. **No Serif** (breaks the digital readout aesthetic) and **no Monospace** in the native theme slots — use monospace only inside pro-code custom components where a terminal glyph is explicitly desired.

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

- **SemiBold (600)**: Headings, KPI values, active button labels, status chips
- **Regular (400)**: Body, axes, tables, descriptions
- **Light (300)**: KPI labels and timeframe captions — recede behind the signal
- **Never Bold (700) or Black (900)** — they shatter the thin neon line language

### 3.4 Text Color Rules

Primary copy uses **`#C8E0F0`** (cyan-white), not `#FFFFFF`. Secondary at **`#607080`** (steel blue) defines scaffolding, metadata, and axes. Chart legends and tooltips default to secondary for labels; **values** may pick up series neon or primary text for emphasis.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#141A24`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#C8E0F0`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#00E5FF`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

Depth comes from **black shadows** and the **single step** from page (`#0A0E14`) to panel (`#141A24`). Optional pro-code: **1px** inner highlight at `rgba(0,229,255,0.06)` on hero cards only — never full neon fills.

### 4.2 Buttons

| State    | Background | Border    | Text      | Notes |
|----------|------------|-----------|-----------|-------|
| Default  | `#141A24`  | `#1E2838` | `#607080` | Ghost / outline |
| Hover    | `#1C2430`  | `#00E5FF` | `#C8E0F0` | Subtle glow: `0 0 12px rgba(0,229,255,0.3)` |
| Active   | `#00E5FF`  | `#00E5FF` | `#0A0E14` | Dark text on neon |
| Disabled | `#0E1218`  | `#182030` | `#2A3444` | Muted steel |

Border radius **6px**. Transition: `transform, background-color, border-color, box-shadow` **150ms** `ease-out`. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property     | Value                     |
|--------------|---------------------------|
| Background   | `#141A24` (`--surface`)   |
| Border       | `#1E2838` (`--border`)    |
| Text         | `#C8E0F0` (`--text-primary`) |
| Placeholder  | `#2A3444` (mid gray, `c45`) |
| Focus border | `#00E5FF` (`--accent`)    |
| Radius       | `6px`                     |
| Font         | 13px, weight 600          |

Focus ring may use **outer glow** `0 0 0 1px #00E5FF, 0 0 12px rgba(0,229,255,0.25)` for accessibility without filling the field neon.

### 4.4 Status Badges

- Background: dark tint from Section 2.2
- Text: status primary (neon)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`
- Optional: `box-shadow: 0 0 8px` with status color at **0.25** opacity for "live" indicators

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#0E1218`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#C8E0F0`             | `navigation.linkFontColor` → `c58`  |
| Active link text  | `#C8E0F0`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#00E5FF`             | `navigation.activeColor` → `c29`    |
| Title text        | `#C8E0F0`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#1C2430`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference **`c58`**, never **`c60`**. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, which **erases** nav labels on dark chrome.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#0A0E14`             | `headers.backgroundColor` → `c1` |
| Font color  | `#C8E0F0`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#0E1218`             | `tables.headerBG` → `c4`   |
| Header text     | `#607080`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#141A24`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#10151C`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#1C2430`             | `tables.hoverBG` → `c3`    |
| Row text        | `#C8E0F0`             | `tables.fontColor` → `c58` |
| Border          | `#182030`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#1E2838` (`--border`), **8px** height, **4px** radius
- Fill: status neon or `--accent`; transition **width 300ms** `ease`
- Optional: soft outer glow on fill using the same color at **0.35** opacity

### 4.9 Summary / KPI Cards

| Property     | Value                       |
|--------------|-----------------------------|
| Background   | `#141A24` (`--surface`)     |
| Radius       | `10px`                      |
| Label        | 11px, uppercase, `#607080`  |
| Value        | 28px, SemiBold, accent or status neon |
| Shadow       | `var(--shadow)`             |

Cap **one** neon hue per KPI row besides the shared cyan accent chrome.

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#141A24`  | `#1E2838` | `#607080` |
| Hover   | `#1C2430`  | `#1E2838` | `#C8E0F0` |
| Active  | `#00E5FF`  | `#00E5FF` | `#0A0E14` |

Active tab is one of the few large accent fills; keep tab strips **narrow** so neon area stays a minority of the viewport.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH (approx.)         | colorRange Index | CSS Variable |
|--------|-----------|-------------------------|------------------|--------------|
| 1      | `#00E5FF` | `oklch(0.86 0.14 215)`  | `[0][0]`         | `--series-1` |
| 2      | `#FF2D8A` | `oklch(0.65 0.24 350)`  | `[1][0]`         | `--series-2` |
| 3      | `#8B5CF6` | `oklch(0.58 0.22 290)`  | `[2][0]`         | `--series-3` |
| 4      | `#39FF14` | `oklch(0.88 0.35 145)`  | `[3][0]`         | `--series-4` |
| 5      | `#FFB020` | `oklch(0.78 0.16 75)`   | `[4][0]`         | `--series-5` |
| 6      | `#4A6070` | `oklch(0.45 0.04 245)`  | `[5][0]`         | `--series-6` |

**Rule**: Prefer **series 1 (cyan)** plus **one** contrasting neon (magenta, purple, acid green, or amber) per card; use **`#4A6070`** for tertiary comparison series so the HUD does not become carnival lighting.

### 5.2 Semantic Chart Colors

| Role              | Hex       | OKLCH (approx.)        | Theme JSON Key                |
|-------------------|-----------|------------------------|-------------------------------|
| Positive / Up     | `#39FF14` | `oklch(0.88 0.35 145)` | `nameColorMap.WaterfallGreen` |
| Negative / Down   | `#FF2D8A` | `oklch(0.65 0.24 350)` | `nameColorMap.NegativeColor`  |
| Total / Net       | `#607080` | `oklch(0.52 0.04 240)` | `nameColorMap.WaterfallTotal` |
| Goal / Target     | `#C8E0F0` | `oklch(0.88 0.04 230)` | —                             |
| Forecast          | `#00E5FF` | `oklch(0.86 0.14 215)` | — (dashed stroke)             |
| Confidence Band   | `rgba(0,229,255,0.12)` | `oklch(0.86 0.14 215 / 0.12)` | — (area fill)      |
| Today Indicator   | `#FF2D8A` | `oklch(0.65 0.24 350)` | —                             |

### 5.3 Chart Styling Rules

- **Grid lines**: `stroke: #1E2838` (`--border`), **1px**, **`opacity: 0.3`** — matrix trace, not graph paper
- **Axis lines**: `#1E2838`, **1px**, opacity **0.5**
- **Axis tick text**: `#607080` (`--text-secondary`), **11px**, Regular (400)
- **Tooltip**: background `#0E1218`, text `#C8E0F0`, radius **6px**, **`box-shadow: 0 0 16px rgba(0,229,255,0.15), var(--shadow)`**
- **Legend**: `#607080`, **11px**; active series at full opacity, inactive **0.35**
- **Plot area**: transparent or **radial** `rgba(0,229,255,0.03)` at center only — never solid neon fills

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier     | Surface            | Shadow              | Use                              |
|----------|--------------------|---------------------|----------------------------------|
| Ground   | `#0A0E14` (--bg)   | none                | Page background                  |
| Raised   | `#141A24` (--surface) | `var(--shadow)`  | Cards, panels                    |
| Floating | `#1C2430`          | `var(--shadow-hover)` | Dropdowns, tooltips, popovers |
| Overlay  | `rgba(0,0,0,0.55)` | none                | Modal scrim                      |

Hierarchy is **lightness steps on cool blue-gray** plus **black shadow**. Neon never defines a tier — it only annotates.

### 6.2 Border Usage

- Prefer **shadow** for card edges; optional **hairline** `1px solid rgba(30,40,56,0.5)` if cards must read on noisy imagery
- Dividers: `1px solid` `--border-light` (`#182030`)
- Inputs: `1px solid` `--border` (`#1E2838`); focus transitions to accent
- Status callouts: **3–4px** left border in status neon, no full fill

---

## 7. Do's and Don'ts

### Do

- Use **`c58` for all font color references** in App Studio theme JSON — **never `c60`**
- Keep **neon to ≤ ~20%** of visible pixels per viewport — data and focus only
- Add **subtle glow** to accent affordances: `box-shadow: 0 0 12px rgba(0,229,255,0.3)` (buttons, active nav rail, primary KPI)
- Use **`#C8E0F0`** for primary text instead of pure white
- Set **`background: transparent`** on pro-code app root containers inside App Studio cards
- Use **three-layer shadows** with **pure black** at **0.30–0.45** opacity
- Run a **full native pass** (nav, filters, hero, tables) after theme import
- Apply **`font-variant-numeric: tabular-nums`** to live metrics and tables
- Keep **≤ 2 distinct neon hues** on a single card (e.g., cyan + one other series)

### Don't

- Use **`c60` (AUTOMATIC_COLOR)** for any font color on dark surfaces
- Use **neon for backgrounds** or large fields — causes **eye strain** and kills contrast hierarchy
- Use **serif fonts** in the App Studio theme slots — they **break the digital** readout look
- Mix **more than two neon colors** in one card's primary data layer
- Use **pure white (`#FFFFFF`)** body text
- Use **light pastel** status badge fills
- Use **`transition: all`** — list explicit properties
- Use **font-weight 700+** on UI chrome
- Use **colored drop shadows** for elevation — stick to **black**

---

## 8. Dark Mode Adaptation Notes

This theme **is** dark-first. When an agent applies it:

1. **App Studio native theme**: Map Section **2.1** slots to `c1`–`c59` as in Section **10**. Replace every **`c60`** reference in cards, navigation, headers, and components with **`c58`**.

2. **Pro-code CSS**: Copy the `:root` block from Section **9.1**. Mirror values in a `COLORS` object (Section **9.3**). Root wrapper: `background: transparent`.

3. **Charts**: Feed **`--series-1`…`--series-6`** into your chart library. Use Section **5.2** for waterfalls, forecast overlays, and reference lines. Keep **grid opacity at ~0.3** for the matrix feel.

4. **Light mode**: Do **not** invert luminance mechanically. Cyberpunk light would be a **different** palette (higher base L, restrained neon). Treat as a separate theme if ever required.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             #0A0E14;
  --surface:        #141A24;
  --surface-hover:  #1C2430;
  --text-primary:   #C8E0F0;
  --text-secondary: #607080;
  --border:         #1E2838;
  --border-light:   #182030;
  --accent:         #00E5FF;
  --accent-muted:   rgba(0, 229, 255, 0.12);
  --accent-hover:   #40F0FF;

  --on-track:       #39FF14;
  --on-track-bg:    #0E1A12;
  --at-risk:        #FFB020;
  --at-risk-bg:     #1A140A;
  --behind:         #FF2D8A;
  --behind-bg:      #1A0E16;
  --complete:       #40F0FF;
  --complete-bg:    #0E1820;

  --shadow:
    0px 0px 0px 1px rgba(0, 0, 0, 0.30),
    0px 1px 3px -1px rgba(0, 0, 0, 0.40),
    0px 2px 6px 0px rgba(0, 0, 0, 0.35);
  --shadow-hover:
    0px 0px 0px 1px rgba(0, 0, 0, 0.38),
    0px 2px 6px -1px rgba(0, 0, 0, 0.45),
    0px 4px 12px 0px rgba(0, 0, 0, 0.30);

  --glow-accent:    0 0 12px rgba(0, 229, 255, 0.3);
  --glow-tooltip:   0 0 16px rgba(0, 229, 255, 0.15);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --series-1: #00E5FF;
  --series-2: #FF2D8A;
  --series-3: #8B5CF6;
  --series-4: #39FF14;
  --series-5: #FFB020;
  --series-6: #4A6070;
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #0A0E14    Card bg      → c2   #141A24
Hover bg     → c3   #1C2430    Nav bg       → c4   #0E1218
Primary text → c58  #C8E0F0    Secondary    → c59  #607080
Accent       → c29  #00E5FF    Accent hover → c30  #40F0FF
Border       → c46  #1E2838    Border light → c47  #182030
Font colors  → ALWAYS c58, NEVER c60
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#00E5FF',
  secondary: '#FF2D8A',
  tertiary:  '#8B5CF6',
  surface:   '#141A24',
  bg:        '#0A0E14',
  text:      '#C8E0F0',
  textMuted: '#607080',
  border:    '#1E2838',
  positive:  '#39FF14',
  negative:  '#FF2D8A',
  series: ['#00E5FF', '#FF2D8A', '#8B5CF6', '#39FF14', '#FFB020', '#4A6070']
};
```

### 9.4 Example Agent Prompts

**"Build a real-time monitoring dashboard"**: Page `--bg`, cards `--surface` with `var(--shadow)`. Primary KPIs in `--accent` with `var(--glow-accent)`. Secondary metrics in `--text-secondary`. Charts use `COLORS.series` with **CartesianGrid** stroke `#1E2838` and **opacity 0.3** for the matrix grid. Refresh intervals and timestamps in tabular nums.

**"Build a network status card with glowing indicators"**: Card `--surface`, row layout. Each node: status dot using `--on-track` / `--at-risk` / `--behind` with `box-shadow: 0 0 10px` matching the dot color at **0.4** opacity. Labels `--text-secondary`, hostnames `--text-primary`. Avoid a third neon on the same card.

**"Build a line chart for error rates"**: `Line` stroke `--series-1` or `--behind` depending on severity; `CartesianGrid` stroke `#1E2838` **strokeOpacity={0.3}**; axes tick fill `#607080`. Tooltip: `#0E1218` background, `#C8E0F0` text, `box-shadow: var(--glow-tooltip), var(--shadow)`. Plot area transparent — holographic readout on void.

**"Build a hero metrics row"**: `--surface`, values **28px** SemiBold tabular-nums (`--text-primary` or `--accent`), labels **11px** Light uppercase `--text-secondary`. Optional **4px** left border `--accent` on the hero card only. No neon fill behind the row.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Cyberpunk",
  "colors": [
    { "index": 1, "value": "#0A0E14", "tag": "PRIMARY" },
    { "index": 2, "value": "#141A24", "tag": "PRIMARY" },
    { "index": 3, "value": "#1C2430", "tag": "PRIMARY" },
    { "index": 4, "value": "#0E1218", "tag": "PRIMARY" },
    { "index": 5, "value": "#1C2430", "tag": "PRIMARY" },
    { "index": 6, "value": "#0A0E14", "tag": "PRIMARY" },
    { "index": 7, "value": "#141A24", "tag": "PRIMARY" },
    { "index": 29, "value": "#00E5FF", "tag": "SECONDARY" },
    { "index": 30, "value": "#40F0FF", "tag": "SECONDARY" },
    { "index": 40, "value": "#000000", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#05070A", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#0A0E14", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#10151C", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#1E2838", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#2A3444", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#1E2838", "tag": "CUSTOM" },
    { "index": 47, "value": "#182030", "tag": "CUSTOM" },
    { "index": 48, "value": "#1E2838", "tag": "CUSTOM" },
    { "index": 49, "value": "#4A5568", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#607080", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#8A9EB0", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#B0C8D8", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#C8E0F0", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#E0EEF8", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#C8E0F0", "tag": "FONT" },
    { "index": 59, "value": "#607080", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm **navigation**, **headers**, **cards**, **tables**, **tabs**, and **forms** use **`c58`** for all font colors (not **`c60`**). Validate **tab active** state: cyan fill with **dark** text via **`c1`** (`#0A0E14`).
