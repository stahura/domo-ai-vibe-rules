# Neon Magenta Dark — Domo App Studio Design System

> **Mode**: Dark · **Accent family**: Hot pink / magenta · **Mood**: Bold, energetic, high-impact

---

## 1. Visual Theme and Atmosphere

**Personality**: Electric nightclub meets executive dashboard. The UI sits on velvet purple-black while KPIs and primary series punch forward in hot magenta. Data reads like neon on obsidian — premium, urgent, and unmistakably modern.

**Density**: Medium-high. Cards use 16px grid gaps with 20px internal padding. Deep surfaces let tight layouts breathe; magenta is reserved so the eye always finds the signal.

**Philosophy**: Magenta is earned — use it for primary KPIs, the lead series, active controls, and the single most important metric per view. Supporting UI stays in lavender-muted neutrals. If more than ~25% of visible area reads as pink or magenta, the design has failed.

**Atmosphere cues**:
- Surfaces feel like polished obsidian with a violet undertone — never flat gray, never icy blue
- Motion is fast (150ms) and decisive; avoid playful bounce
- Shadows are pure black at meaningful opacity (dark mode needs stronger separation than light themes)
- Primary text is warm off-white (`#F8F0F5`), not pure `#FFFFFF` — pure white flares on saturated dark purple bases
- **Best for**: Customer intelligence, CRM, engagement funnels, consumer analytics, lifecycle metrics

---

## 2. Color System

### 2.1 Semantic Palette with Slot Mapping

Every color exists in three representations. The **Semantic Role** column is the single source of truth; the other columns are derived from it.

| Semantic Role       | Hex       | OKLCH                         | Theme Slot | CSS Variable        |
|---------------------|-----------|-------------------------------|------------|---------------------|
| Page Background     | `#160E22` | `oklch(0.12 0.025 310)`       | `c1`       | `--bg`              |
| Card Surface        | `#261A38` | `oklch(0.18 0.035 310)`       | `c2`       | `--surface`         |
| Surface Hover       | `#322344` | `oklch(0.22 0.040 310)`       | `c3`       | `--surface-hover`   |
| Primary Text        | `#F8F0F5` | `oklch(0.95 0.008 340)`       | `c58`      | `--text-primary`    |
| Secondary Text      | `#9A85A8` | `oklch(0.68 0.025 320)`       | `c59`      | `--text-secondary`  |
| Border              | `#3C2850` | `oklch(0.28 0.035 310)`       | `c46`      | `--border`          |
| Border Light        | `#2F2042` | `oklch(0.23 0.030 310)`       | `c47`      | `--border-light`    |
| Accent              | `#FF3E8A` | `oklch(0.70 0.20 350)`        | `c29`      | `--accent`          |
| Accent Muted        | `#FF3E8A26` | `oklch(0.70 0.20 350 / 0.15)` | —        | `--accent-muted`    |
| Accent Hover        | `#FF78BE` | `oklch(0.75 0.18 350)`        | `c30`      | `--accent-hover`    |
| Nav Background      | `#1E1530` | `oklch(0.145 0.032 308)`      | `c4`       | `--nav-bg`          |
| Nav Active          | `#322344` | `oklch(0.22 0.040 310)`       | `c5`       | `--nav-active`      |
| Header Background   | `#160E22` | `oklch(0.12 0.025 310)`       | `c6`       | `--header-bg`       |
| Input Background    | `#261A38` | `oklch(0.18 0.035 310)`       | `c7`       | `--input-bg`        |
| Input Border        | `#3C2850` | `oklch(0.28 0.035 310)`       | `c48`      | `--input-border`    |
| Tab Default BG      | `#261A38` | `oklch(0.18 0.035 310)`       | `c8`       | `--tab-bg`          |
| Tab Active BG       | `#FF3E8A` | `oklch(0.70 0.20 350)`        | `c9`       | `--tab-active-bg`   |
| Table Header BG     | `#1E1530` | `oklch(0.145 0.032 308)`      | `c10`      | `--table-header-bg` |
| Table Row Stripe    | `#1A1024` | `oklch(0.15 0.028 310)`       | `c11`      | `--table-stripe`    |
| Table Row Hover     | `#322344` | `oklch(0.22 0.040 310)`       | `c12`      | `--table-row-hover` |
| Grayscale 1 (black) | `#040208` | `oklch(0.07 0.018 310)`       | `c40`      | —                   |
| Grayscale 2         | `#0A0612` | `oklch(0.10 0.022 310)`       | `c41`      | —                   |
| Grayscale 3         | `#160E22` | `oklch(0.12 0.025 310)`       | `c42`      | —                   |
| Grayscale 4         | `#1A1024` | `oklch(0.15 0.028 310)`       | `c43`      | —                   |
| Grayscale 5         | `#261A38` | `oklch(0.18 0.035 310)`       | `c44`      | —                   |
| Grayscale 6         | `#3C2850` | `oklch(0.28 0.035 310)`       | `c45`      | —                   |
| Grayscale 7         | `#5A4A6E` | `oklch(0.42 0.038 305)`       | `c49`      | —                   |
| Grayscale 8         | `#9A85A8` | `oklch(0.68 0.025 320)`       | `c50`      | —                   |
| Grayscale 9         | `#B8A5C4` | `oklch(0.76 0.040 310)`       | `c51`      | —                   |
| Grayscale 10        | `#DCCFE0` | `oklch(0.86 0.020 320)`       | `c52`      | —                   |
| Grayscale 11        | `#ECE4EE` | `oklch(0.91 0.015 320)`       | `c53`      | —                   |
| Grayscale 12        | `#F8F4FA` | `oklch(0.96 0.012 320)`       | `c54`      | —                   |

### 2.2 Status Colors

| Status   | Primary   | Background | Text      | CSS Variable     |
|----------|-----------|------------|-----------|------------------|
| On Track | `#71B798` | `#0D1F16`  | `#71B798` | `--on-track`     |
| At Risk  | `#E8A84C` | `#221206`  | `#E8A84C` | `--at-risk`      |
| Behind   | `#FF3E8A` | `#260B19`  | `#FF3E8A` | `--behind`       |
| Complete | `#C9A3D4` | `#1E1024`  | `#C9A3D4` | `--complete`     |

On-track primary is aligned to semantic positive green (`#71B798`). At-risk uses the OKLCH-spec amber family (`oklch(0.78 0.14 65)` → `#E8A84C`). **Behind** intentionally matches the accent (hot pink): in this theme, “behind” *is* the brand alarm color. Dark mode status badges use dark-tinted backgrounds (L ~0.18–0.22) with bright text. Never use light-tinted badge backgrounds on dark surfaces.

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0 0 0 / 0.25),
  0px 1px 3px -1px oklch(0 0 0 / 0.35),
  0px 2px 6px 0px oklch(0 0 0 / 0.25);
--shadow-hover:
  0px 0px 0px 1px oklch(0 0 0 / 0.30),
  0px 2px 6px -1px oklch(0 0 0 / 0.40),
  0px 4px 12px 0px oklch(0 0 0 / 0.28);
```

Shadow color is pure black at higher opacity than light themes. On dark violet surfaces, colored shadows vanish — only opacity and lift read as depth.

---

## 3. Typography

### 3.1 Font System

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
```

App Studio native theme: **Sans** family for all font slots. No Serif or Monospace in this theme.

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
- **Never use Bold (700) or Black (900)** — they overpower the high-contrast neon aesthetic

### 3.4 Text Color Rules

Primary text is `#F8F0F5` (warm near-white with a hint of rose), not `#FFFFFF`. Pure white competes with magenta highlights and feels harsh on saturated dark purple. Secondary text at `#9A85A8` (muted lavender) preserves hierarchy without drifting into cold gray.

Chart axis labels, tooltips, and legend text use `--text-secondary` (`#9A85A8`). Data values and KPI numerals use `--text-primary` unless intentionally status-colored.

---

## 4. Card and Component Styles

### 4.1 Cards

| Property        | Value                          | Theme Mapping                  |
|-----------------|--------------------------------|--------------------------------|
| Background      | `#261A38`                      | `ca1.backgroundColor` → `c2`  |
| Font color      | `#F8F0F5`                      | `ca1.fontColor` → `c58`       |
| Border radius   | `10px`                         | `ca1.borderRadius` = `10`     |
| Border width    | `0px`                          | `ca1.borderWidth` = `0`       |
| Drop shadow     | `true`                         | `ca1.dropShadow` = `true`     |
| Padding         | `20px`                         | `ca1.padding` = `20`          |
| Element spacing | `12px`                         | `ca1.elementSpacing` = `12`   |
| Accent color    | `#FF3E8A`                      | `ca1.accentColor` → `c29`     |
| Title font      | Sans, SemiBold, 16px           | `ca1.titleFont` → `f2`        |
| Chart font      | Sans, Regular, 11px            | `ca1.chartFont` → `f5`        |

No visible card border — depth comes from shadow. Card surface (`--surface`) steps up from the page (`--bg`) for clear layering on the purple-black field.

### 4.2 Buttons

| State    | Background | Border    | Text      | CSS Variable           |
|----------|------------|-----------|-----------|------------------------|
| Default  | `#261A38`  | `#3C2850` | `#9A85A8` | `--surface` / `--border` / `--text-secondary` |
| Hover    | `#322344`  | `#FF3E8A` | `#F8F0F5` | `--surface-hover` / `--accent` / `--text-primary` |
| Active   | `#FF3E8A`  | `#FF3E8A` | `#160E22` | `--accent` / `--accent` / `--bg` |
| Disabled | `#1E1530`  | `#2F2042` | `#5A4A6E` | — |

Ghost / outline default; accent fill on active. Border radius: 6px. Transition: `scale, background-color, border-color, box-shadow` at 150ms ease-out. Press: `scale(0.96)`.

### 4.3 Inputs and Selects

| Property     | Value                        |
|--------------|------------------------------|
| Background   | `#261A38` (`--surface`)      |
| Border       | `#3C2850` (`--border`)       |
| Text         | `#F8F0F5` (`--text-primary`) |
| Placeholder  | `#5A4A6E`                    |
| Focus border | `#FF3E8A` (`--accent`)       |
| Radius       | `6px`                        |
| Font         | 13px, weight 600             |

### 4.4 Status Badges

- Background: dark tint at L ~0.18–0.22 with hue matched to the status color
- Text: the status primary color (bright on dark)
- Font: 11px, SemiBold (600), uppercase, `letter-spacing: 0.5px`
- Padding: `3px 8px`, radius `4px`

### 4.5 Navigation (Left Nav / Sidebar)

| Property          | Value                 | Theme Mapping                       |
|-------------------|-----------------------|-------------------------------------|
| Background        | `#1E1530`             | `navigation.backgroundColor` → `c4` |
| Link text         | `#F8F0F5`             | `navigation.linkFontColor` → `c58`  |
| Active link text  | `#F8F0F5`             | `navigation.activeLinkFontColor` → `c58` |
| Active indicator  | `#FF3E8A`             | `navigation.activeColor` → `c29`    |
| Title text        | `#F8F0F5`             | `navigation.titleFontColor` → `c58` |
| Hover background  | `#322344`             | —                                    |

**Critical**: All `*FontColor` navigation properties must reference `c58`, never `c60`. The `c60` AUTOMATIC_COLOR slot defaults to dark text regardless of background, which makes nav labels invisible on purple-black.

### 4.6 Headers and Section Titles

| Property    | Value                 | Theme Mapping                   |
|-------------|-----------------------|---------------------------------|
| Background  | `#160E22`             | `headers.backgroundColor` → `c1` |
| Font color  | `#F8F0F5`             | `headers.fontColor` → `c58`     |
| Border      | none                  | —                                |

### 4.7 Tables

| Property        | Value                 | Theme Mapping               |
|-----------------|-----------------------|-----------------------------|
| Header BG       | `#1E1530`             | `tables.headerBG` → `c4`   |
| Header text     | `#9A85A8`             | `tables.headerFontColor` → `c59` |
| Row BG          | `#261A38`             | `tables.rowBG` → `c2`      |
| Row stripe      | `#1A1024`             | `tables.stripeBG` → `c11`  |
| Row hover       | `#322344`             | `tables.hoverBG` → `c3`    |
| Row text        | `#F8F0F5`             | `tables.fontColor` → `c58` |
| Border          | `#2F2042`             | `tables.borderColor` → `c47` |

### 4.8 Progress Bars

- Track: `#3C2850` (`--border`), 8px height, 4px radius
- Fill: status-colored; `width` transition 300ms ease
- On dark backgrounds, the track sits one readable step above the surface without glowing

### 4.9 Summary / KPI Cards

| Property     | Value                         |
|--------------|-------------------------------|
| Background   | `#261A38` (`--surface`)       |
| Radius       | `10px`                        |
| Label        | 11px, uppercase, `#9A85A8`    |
| Value        | 28px, SemiBold, status or `#F8F0F5` |
| Shadow       | `var(--shadow)`               |

### 4.10 Tabs

| State   | Background | Border    | Text      |
|---------|------------|-----------|-----------|
| Default | `#261A38`  | `#3C2850` | `#9A85A8` |
| Hover   | `#322344`  | `#3C2850` | `#F8F0F5` |
| Active  | `#FF3E8A`  | `#FF3E8A` | `#160E22` |

Active tab uses full accent fill with dark text (`--bg`) for maximum contrast — one of the few large accent fields allowed.

---

## 5. Chart Palette

### 5.1 Series Colors with Mapping

| Series | Hex       | OKLCH                       | colorRange Index | CSS Variable |
|--------|-----------|-----------------------------|------------------|--------------|
| 1      | `#ED68AE` | `oklch(0.70 0.18 350)`      | `[0][0]`         | `--c1`       |
| 2      | `#C467BD` | `oklch(0.65 0.16 330)`      | `[1][0]`         | `--c2`       |
| 3      | `#F18093` | `oklch(0.73 0.14 10)`       | `[2][0]`         | `--c3`       |
| 4      | `#876CCA` | `oklch(0.60 0.14 295)`      | `[3][0]`         | `--c4`       |
| 5      | `#E89DC0` | `oklch(0.78 0.10 350)`      | `[4][0]`         | `--c5`       |
| 6      | `#D87880` | `oklch(0.68 0.12 15)`       | `[5][0]`         | `--c6`       |

Series 1 is the hero magenta/pink line or bar set; remaining series rotate through magenta, warm rose, purple, light pink, and salmon so multi-series charts stay on-brand without introducing cool blue.

### 5.2 Semantic Chart Colors

| Role              | Hex         | OKLCH                         | Theme JSON Key                  |
|-------------------|-------------|-------------------------------|---------------------------------|
| Positive / Up     | `#71B798`   | `oklch(0.724 0.085 164)`      | `nameColorMap.WaterfallGreen`   |
| Negative / Down   | `#FF3E8A`   | `oklch(0.70 0.20 350)`        | `nameColorMap.NegativeColor`    |
| Total / Net       | `#9A85A8`   | `oklch(0.68 0.025 320)`       | `nameColorMap.WaterfallTotal`   |
| Goal / Target     | `#F8F0F5`   | `oklch(0.95 0.008 340)`       | —                               |
| Forecast          | `#FF3E8A`   | `oklch(0.70 0.20 350)`        | — (dashed stroke)               |
| Confidence Band   | `#FF3E8A26` | `oklch(0.70 0.20 350 / 0.15)` | — (area fill)                   |
| Today Indicator   | `#FF3E8A`   | `oklch(0.70 0.20 350)`        | —                               |

Negative/down intentionally uses the **accent** (hot pink): semantic “bad” aligns with the brand alarm color. Positive remains anchored in green (`#71B798`) for universal readability.

### 5.3 Chart Styling Rules

- Grid lines: `#2F2042` (`--border-light`), 1px, opacity 0.5
- Axis lines: `#3C2850` (`--border`), 1px
- Axis tick text: `#9A85A8` (`--text-secondary`), 11px, Regular (400)
- Tooltip background: `#1E1530` with `--shadow`, 6px radius, `#F8F0F5` text
- Legend text: `#9A85A8`, 11px, Regular
- Active/hover series: opacity 1.0; inactive series: opacity 0.3
- **Do not** default to blue reference lines or node highlights — they fight the violet field; use `--text-primary`, green, or accent instead

---

## 6. Depth and Elevation

### 6.1 Elevation Tiers

| Tier      | Surface                         | Shadow                 | Use                              |
|-----------|---------------------------------|-------------------------|----------------------------------|
| Ground    | `#160E22` (--bg)                | none                    | Page background                  |
| Raised    | `#261A38` (--surface)           | `var(--shadow)`         | Cards, panels, main containers   |
| Floating  | `#322344` (--surface-hover)     | `var(--shadow-hover)`   | Dropdowns, tooltips, popovers    |
| Overlay   | `oklch(0 0 0 / 0.55)`           | none                    | Modal backdrop                   |

Dark-mode depth uses lightness steps on the purple axis (~0.06–0.10 L between tiers) plus black shadows. Neon accent is not an elevation tool — reserve it for data and interaction.

### 6.2 Border Usage

- Prefer shadow over visible card rims; shadows stay legible on `#160E22`
- Use `1px solid var(--border-light)` for dividers and subtle table separators
- Use `1px solid var(--border)` for inputs (focus + accessibility)
- Avoid borders thicker than `2px` except status callouts (e.g. 4px left accent on KPI cards)

---

## 7. Do's and Don'ts

### Do

- Use `c58` (`#F8F0F5`) for all theme JSON font color references — **never** `c60`
- Use `c59` (`#9A85A8`) for secondary copy where the UI supports a distinct secondary font color (e.g. table headers)
- Keep pink / magenta / hot accent below ~25% of visible area per screen
- Use `--text-primary` instead of `#FFFFFF` for body and KPI values
- Set `background: transparent` on pro-code app containers embedded in App Studio cards
- Use three-layer black shadows at opacity 0.25–0.40
- Test nav, filters, and hero cards after theme import — purple-black exposes any wrong automatic text colors immediately
- Use `font-variant-numeric: tabular-nums` on metrics and tables

### Don't

- Use `c60` (AUTOMATIC_COLOR) for any font color on this dark theme
- Use pure white (`#FFFFFF`) for large text blocks
- Use light pastel badge fills (high L) on dark cards — they read as dirty smudges
- Use **blue** accents, links, or chart defaults — they clash with violet surfaces and break the neon story
- Apply light-theme border hex values — they disappear or halo incorrectly on dark purple
- Use `transition: all` — list explicit properties
- Use font-weight 700 / 900 except in rare marketing overlays
- Use colored drop shadows — they do not read on obsidian-like bases; black only
- Flood pages with accent pink “just for energy” — restraint makes magenta feel expensive

---

## 8. Dark Mode Adaptation Notes

This **is** a dark theme. When an agent applies it:

1. **App Studio native theme**: Map Section 2.1 slots to `c1`–`c60` positions. Replace every `c60` reference in `cards[].fontColor`, `navigation.*FontColor`, `headers[].fontColor`, and `components.*FontColor` with `c58`.

2. **Pro-code CSS**: Copy the Section 9.1 `:root` block. Set the `COLORS` object from those hex values. Keep the app shell `background: transparent`.

3. **Charts**: Pipe `--c1`–`c6` into the chart library color array. Use Section 5.2 for waterfalls, deltas, forecast lines, and bands — negative/down = accent pink; positive/up = `#71B798`.

4. **Light mode**: Do not invert L channels. Swap to a dedicated light palette and theme JSON if a light variant is required.

---

## 9. Agent Quick Reference

### 9.1 CSS Custom Properties Block (copy-paste ready)

```css
:root {
  --bg:             oklch(0.12 0.025 310);
  --surface:        oklch(0.18 0.035 310);
  --surface-hover:  oklch(0.22 0.040 310);
  --text-primary:   oklch(0.95 0.008 340);
  --text-secondary: oklch(0.68 0.025 320);
  --border:         oklch(0.28 0.035 310);
  --border-light:   oklch(0.23 0.030 310);
  --accent:         oklch(0.70 0.20 350);
  --accent-muted:   oklch(0.70 0.20 350 / 0.15);
  --accent-hover:   oklch(0.75 0.18 350);

  --on-track:       oklch(0.724 0.085 164);
  --on-track-bg:    oklch(0.20 0.04 155);
  --at-risk:        oklch(0.78 0.14 65);
  --at-risk-bg:     oklch(0.20 0.04 65);
  --behind:         oklch(0.70 0.16 350);
  --behind-bg:      oklch(0.20 0.05 350);

  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.25),
    0px 1px 3px -1px oklch(0 0 0 / 0.35),
    0px 2px 6px 0px oklch(0 0 0 / 0.25);
  --shadow-hover:
    0px 0px 0px 1px oklch(0 0 0 / 0.30),
    0px 2px 6px -1px oklch(0 0 0 / 0.40),
    0px 4px 12px 0px oklch(0 0 0 / 0.28);

  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;

  --c1: oklch(0.70 0.18 350);
  --c2: oklch(0.65 0.16 330);
  --c3: oklch(0.73 0.14 10);
  --c4: oklch(0.60 0.14 295);
  --c5: oklch(0.78 0.10 350);
  --c6: oklch(0.68 0.12 15);
}
```

### 9.2 Slot Mapping Cheat Sheet

```
Page bg      → c1   #160E22    Card bg      → c2   #261A38
Hover bg     → c3   #322344    Nav bg       → c4   #1E1530
Primary text → c58  #F8F0F5    Secondary    → c59  #9A85A8
Accent       → c29  #FF3E8A    Border       → c46  #3C2850
Font colors  → ALWAYS c58, NEVER c60
```

### 9.3 Pro-Code COLORS Object

```javascript
const COLORS = {
  primary:   '#FF3E8A',
  secondary: '#C467BD',
  tertiary:  '#876CCA',
  surface:   '#261A38',
  bg:        '#160E22',
  text:      '#F8F0F5',
  textMuted: '#9A85A8',
  border:    '#3C2850',
  positive:  '#71B798',
  negative:  '#FF3E8A',
  series: ['#ED68AE', '#C467BD', '#F18093', '#876CCA', '#E89DC0', '#D87880']
};
```

### 9.4 Example Agent Prompts

**"Build a hero metrics row"**: Use `--surface` background, `--text-primary` for values (28px SemiBold `tabular-nums`), `--text-secondary` for labels (11px Light uppercase). Optional 4px left border in `--accent` or status green. No card border — `var(--shadow)` only.

**"Build a banner with background pattern"**: Use Diagonal Lines + Radial Glow from the `app-studio-pro-code` skill. Foreground text `--text-primary`; base gradient from `--surface`; glow from `--accent-muted` (keep glow subtle — under 25% accent coverage).

**"Build a bar chart card"**: Recharts `BarChart` with `COLORS.series` fills. `CartesianGrid` stroke `#2F2042` at opacity 0.5. `XAxis` / `YAxis` tick fill `#9A85A8`. Tooltip surface `#1E1530`, text `#F8F0F5`, shadow from `--shadow`. Avoid default blue cartesian or cursor strokes.

**"Add a forecast line with confidence band"**: `ComposedChart` — solid historical `--c1`, dashed forecast `--accent`, `Area` fill `--accent-muted`. `ReferenceLine` “today” may use `--negative` (accent) or `--text-secondary` if you need a quieter marker. Provide a toggle for the band.

---

## 10. App Studio Theme JSON (Importable)

The complete theme JSON below can be imported directly into Domo App Studio. It implements the colors, fonts, card styles, navigation, and component settings defined in this document.

```json
{
  "name": "Neon Magenta Dark",
  "colors": [
    { "index": 1, "value": "#160E22", "tag": "PRIMARY" },
    { "index": 2, "value": "#261A38", "tag": "PRIMARY" },
    { "index": 3, "value": "#322344", "tag": "PRIMARY" },
    { "index": 4, "value": "#1E1530", "tag": "PRIMARY" },
    { "index": 5, "value": "#322344", "tag": "PRIMARY" },
    { "index": 6, "value": "#160E22", "tag": "PRIMARY" },
    { "index": 7, "value": "#261A38", "tag": "PRIMARY" },
    { "index": 29, "value": "#FF3E8A", "tag": "SECONDARY" },
    { "index": 30, "value": "#FF78BE", "tag": "SECONDARY" },
    { "index": 40, "value": "#040208", "tag": "GRAYSCALE" },
    { "index": 41, "value": "#0A0612", "tag": "GRAYSCALE" },
    { "index": 42, "value": "#160E22", "tag": "GRAYSCALE" },
    { "index": 43, "value": "#1A1024", "tag": "GRAYSCALE" },
    { "index": 44, "value": "#261A38", "tag": "GRAYSCALE" },
    { "index": 45, "value": "#3C2850", "tag": "GRAYSCALE" },
    { "index": 46, "value": "#3C2850", "tag": "CUSTOM" },
    { "index": 47, "value": "#2F2042", "tag": "CUSTOM" },
    { "index": 48, "value": "#3C2850", "tag": "CUSTOM" },
    { "index": 49, "value": "#5A4A6E", "tag": "GRAYSCALE" },
    { "index": 50, "value": "#9A85A8", "tag": "GRAYSCALE" },
    { "index": 51, "value": "#B8A5C4", "tag": "GRAYSCALE" },
    { "index": 52, "value": "#DCCFE0", "tag": "GRAYSCALE" },
    { "index": 53, "value": "#ECE4EE", "tag": "GRAYSCALE" },
    { "index": 54, "value": "#F8F4FA", "tag": "GRAYSCALE" },
    { "index": 58, "value": "#F8F0F5", "tag": "FONT" },
    { "index": 59, "value": "#9A85A8", "tag": "FONT" }
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

> **To import**: In App Studio → Theme Editor → Import Theme JSON, paste this object. Confirm navigation and header font colors reference `c58` (not `c60`), and that alternate table rows (`c43`) read slightly darker than the primary row (`c2`) for subtle striping.
