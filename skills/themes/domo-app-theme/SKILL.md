---

## name: domo-app-theme
description: Clean, professional dashboard theme for Domo custom apps. CSS custom properties, layout patterns, typography, and design polish that feel native to the Domo platform. Includes OKLCH color palette, layered shadows, concentric border radius, tabular numbers, and micro-interaction patterns.

# Domo Custom App Theme

A clean, professional dashboard theme used across Domo custom apps. Designed to feel native to the Domo platform while being modern and readable. Corporate but not sterile — hierarchy comes from font weight and subtle shadows rather than color. Feels Domo-native / Salesforce-adjacent.

Author: David Johnson

## Themed Design System (DESIGN.md)

This skill operates across **three styling layers** that must stay coherent:

1. **Design Intent** — mood, palette, typography, component recipes (the "what it should feel like")
2. **App Studio Theme JSON** — native Domo schema with `c1`–`c60` color slots, `f1`–`f8` fonts, `ca1`–`ca8` card styles
3. **Pro-Code CSS** — custom properties, inline styles, Recharts/Chart.js colors

Each curated theme has a dedicated **DESIGN.md** file in [themes/](themes/) that serves as the single source of truth for all three layers. A DESIGN.md contains:

- **Visual Theme and Atmosphere** — mood, density, philosophy (prevents generic output)
- **Color System with Slot Mapping Table** — every color has a semantic role, hex, OKLCH, theme slot (`c` number), and CSS variable in one row. This is the Rosetta Stone between native JSON and pro-code CSS.
- **Typography with Font Slot Mapping** — type scale mapped to `f1`–`f8` theme slots
- **Card and Component Styles** — cards, buttons, inputs, nav, tables with `ca`/`b` slot references
- **Chart Palette** — series colors with `colorRange` index mapping
- **Do's and Don'ts** — theme-specific guardrails (e.g., c60 dark mode fix)
- **Agent Quick Reference** — copy-paste CSS block, COLORS object, example prompts
- **Importable Theme JSON** — complete JSON that can be imported directly into App Studio

### Available Themes

| Theme | File | Mode | Accent | Best for |
|-------|------|------|--------|----------|
| **Core Themes** | | | | |
| Charcoal Ember Dark | [charcoal-ember-dark.DESIGN.md](themes/charcoal-ember-dark.DESIGN.md) | Dark | Warm orange | Benchmarks, performance, technical |
| Emerald Dark | [emerald-dark.DESIGN.md](themes/emerald-dark.DESIGN.md) | Dark | Bright emerald | SaaS, analytics, dev tools |
| Neon Magenta Dark | [neon-magenta-dark.DESIGN.md](themes/neon-magenta-dark.DESIGN.md) | Dark | Hot pink / magenta | CRM, engagement, consumer |
| Corporate Light | [corporate-light.DESIGN.md](themes/corporate-light.DESIGN.md) | Light | Cool blue-gray | Executive, corporate, general |
| **Punk Subgenre Themes** | | | | |
| Cyberpunk | [cyberpunk.DESIGN.md](themes/cyberpunk.DESIGN.md) | Dark | Neon cyan | Tech monitoring, cybersecurity, real-time |
| Steampunk | [steampunk.DESIGN.md](themes/steampunk.DESIGN.md) | Dark | Polished brass | Manufacturing, logistics, heritage |
| Solarpunk | [solarpunk.DESIGN.md](themes/solarpunk.DESIGN.md) | Light | Leaf green | Sustainability, ESG, wellness |
| Dieselpunk | [dieselpunk.DESIGN.md](themes/dieselpunk.DESIGN.md) | Dark | Rust orange | Military, industrial, supply chain |
| Biopunk | [biopunk.DESIGN.md](themes/biopunk.DESIGN.md) | Dark | Bioluminescent green | Biotech, pharma, genomics, lab |
| Dreadpunk | [dreadpunk.DESIGN.md](themes/dreadpunk.DESIGN.md) | Dark | Deep crimson | Risk, security, audit, compliance |
| Dungeonpunk | [dungeonpunk.DESIGN.md](themes/dungeonpunk.DESIGN.md) | Dark | Arcane amber | Gaming, fantasy, creative, inventory |
| Atompunk | [atompunk.DESIGN.md](themes/atompunk.DESIGN.md) | Light | Atomic orange | Energy, aerospace, innovation, R&D |

For the 50 light chart palettes (which share the Corporate Light structural base but vary chart series colors), see [palette-overlays.md](themes/palette-overlays.md).

### When to Use a DESIGN.md

- **Building a new App Studio app**: Start from a DESIGN.md. Use its Slot Mapping Table to configure the native theme AND its CSS block for pro-code components.
- **Applying a dark theme**: Use the DESIGN.md instead of the generic dark mode guidance below. The DESIGN.md includes the exact `c58`/`c60` fix, component colors, and importable JSON.
- **Debugging visual inconsistency**: Check the Slot Mapping Table — if a semantic role maps to different values in the theme JSON vs. pro-code CSS, they're out of sync.

### Relationship to This Skill

The content below defines the **default light theme** — structural colors, typography rules, component recipes, spacing, shadows, transitions, and design principles. These are theme-agnostic patterns that apply regardless of which DESIGN.md is active. The DESIGN.md files override the color system and component color values but inherit the layout, spacing, typography philosophy, shadow structure, transition timing, and micro-interaction patterns documented here.

## CSS Custom Properties

```css
:root {
  /* Typography — system sans stack for modern, minimal feel */
  --font-stack: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;

  /* Core Colors (OKLCH primary, hex fallback in comments) */
  --text-primary: oklch(0.374 0.014 256);    /* #3F454D */
  --text-secondary: oklch(0.510 0.016 249);  /* #68737F */
  --bg: oklch(0.962 0.011 240);              /* #F1F6FA */
  --surface: oklch(1 0 0);                   /* #FFFFFF */
  --border: oklch(0.800 0.015 240);          /* #B7C1CB */
  --border-light: oklch(0.908 0.009 240);    /* #DCE4EA */
  --hover-bg: oklch(0.908 0.009 240);        /* #DCE4EA */
  --subtle-hover: oklch(0.979 0.004 240);    /* #F8FAFC */
  --accent-hover: oklch(0.816 0.065 230);    /* #99CCEE */

  /* Status Colors */
  --on-track: oklch(0.835 0.065 155);        /* #ADD4C1 */
  --on-track-bg: oklch(0.943 0.025 155);     /* #e8f3ec */
  --on-track-text: oklch(0.520 0.060 155);   /* #4a7a5a */
  --at-risk: oklch(0.740 0.155 60);          /* #FF9922 */
  --at-risk-bg: oklch(0.960 0.035 75);       /* #fff0dd */
  --at-risk-text: oklch(0.580 0.110 60);     /* #c47a10 */
  --behind: oklch(0.545 0.100 290);          /* #776CB0 */
  --behind-bg: oklch(0.930 0.025 290);       /* #eae7f3 */
  --behind-text: oklch(0.440 0.080 290);     /* #5a5094 */
  --complete: oklch(0.816 0.065 230);        /* #99CCEE */
  --complete-bg: oklch(0.940 0.025 230);     /* #e0f0fa */
  --complete-text: oklch(0.660 0.060 230);   /* #5a9abe */

  /* Summary Card Values */
  --on-track-value: oklch(0.620 0.070 155);  /* #6a9f7a */
  --at-risk-value: oklch(0.740 0.155 60);    /* #FF9922 */
  --behind-value: oklch(0.545 0.100 290);    /* #776CB0 */
  --complete-value: oklch(0.816 0.065 230);  /* #99CCEE */
  --total-value: oklch(0.374 0.014 256);     /* #3F454D */

  /* Accent / Highlight */
  --alert: oklch(0.590 0.160 20);            /* #e45f5f */
  --avatar-bg: oklch(0.374 0.014 256);       /* #3F454D */
  --avatar-text: oklch(1 0 0);               /* #FFFFFF */

  /* Shadows — three-layer depth for natural lift */
  --shadow:
    0px 0px 0px 1px oklch(0.374 0.014 256 / 0.06),
    0px 1px 2px -1px oklch(0.374 0.014 256 / 0.06),
    0px 2px 4px 0px oklch(0.374 0.014 256 / 0.04);
  --shadow-hover:
    0px 0px 0px 1px oklch(0.374 0.014 256 / 0.08),
    0px 2px 4px -1px oklch(0.374 0.014 256 / 0.08),
    0px 4px 12px 0px oklch(0.374 0.014 256 / 0.06);

  /* Border Radius — concentric: outer = inner + padding */
  --radius-card: 10px;   /* outer: card surface */
  --radius-btn: 6px;     /* inner: with 4px card padding clearance */
  --radius-badge: 4px;
  --radius-bar: 4px;

  /* Spacing */
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;
}
```

## Reset & Baseline

```css
* { box-sizing: border-box; margin: 0; padding: 0; }

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

## Typography

### Philosophy: Weight Does the Work

Modern, minimal typography relies on **weight contrast** — not size explosion — for hierarchy. The scale uses only 5 sizes (11, 12, 13, 16, 22). Headings feel authoritative through SemiBold (600), while body text stays light and airy at Regular (400). Light (300) is used for secondary/caption text to create breathing room between the data and its labels.

Never use Bold (700) or Black (900) for UI text — they overpower the minimal feel. Reserve SemiBold for headings, KPI values, and active button labels only. Everything else stays Regular or Light.

### Type Scale


| Role                         | Size | Weight | Extra                                                      |
| ---------------------------- | ---- | ------ | ---------------------------------------------------------- |
| Page title                   | 22px | 600    | `text-wrap: balance`                                       |
| Card / section titles        | 16px | 600    | `text-wrap: balance`                                       |
| Body text / descriptions     | 13px | 400    | line-height 1.5, `text-wrap: pretty`                       |
| Labels / captions            | 11px | 400    | uppercase, letter-spacing 0.04em                           |
| Chart axis text              | 11px | 400    | `fill` color, not CSS `color`                              |
| Badges / status text         | 11px | 600    | only place small text gets weight                          |
| KPI / summary numbers        | 28px | 600    | `font-variant-numeric: tabular-nums`                       |
| KPI labels                   | 11px | 300    | uppercase, letter-spacing 0.04em — fades behind the number |
| Micro text (avatar initials) | 9px  | 600    | letter-spacing 0.5px                                       |
| Dynamic numbers              | any  | —      | `font-variant-numeric: tabular-nums`                       |


### Font Stack

The font family is a design decision set in the project's `DESIGN.md`. Domo App Studio supports three font families:

| Domo family | Pro-code CSS `font-family` | Feel |
|-------------|----------------------------|------|
| **Sans** (default) | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` | Clean, modern, tech-forward (GitHub, Stripe, Linear) |
| **Serif** | `Georgia, "Times New Roman", "Palatino Linotype", serif` | Editorial, warm, premium (NYT, Medium) |
| **Slab** | `"Roboto Slab", "Rockwell", "Courier New", serif` | Bold, structured, industrial |

**CRITICAL**: The App Studio theme `fonts[].family` and all pro-code CSS `font-family` must use the **same** family. Mixing Sans native cards with Serif pro-code components (or vice versa) breaks visual cohesion. When a `DESIGN.md` specifies a font family, apply it everywhere.

### App Studio Native Font Settings

Configure the App Studio theme editor font slots. Replace `{family}` with the chosen family from the table above:

| Slot                 | Style preset | Font family | Weight   | Size |
| -------------------- | ------------ | ----------- | -------- | ---- |
| Card Title           | Heading 4    | {family}    | SemiBold | 16px |
| Card Description     | Body         | {family}    | Regular  | 13px |
| Timeframe            | Paragraph    | {family}    | Light    | 11px |
| Chart text           | Body         | {family}    | Regular  | 11px |
| Summary number       | Heading 5    | {family}    | SemiBold | 28px |
| Summary number label | Paragraph    | {family}    | Light    | 11px |


This creates a consistent look between native cards and pro-code cards on the same page. The key choices:

- **Card Title at SemiBold** — authoritative without being heavy
- **Timeframe at Light** — barely-there, unobtrusive, lets the data breathe
- **Summary number label at Light** — the label recedes so the number dominates
- **Chart text at Regular 11px** — clean axis labels that don't compete with data

### Weight Map (Domo App Studio ↔ CSS)


| App Studio weight | CSS `font-weight` | When to use                                      |
| ----------------- | ----------------- | ------------------------------------------------ |
| Extra Light       | 200               | Never in standard UI — too faint for readability |
| Light             | 300               | KPI labels, timeframe text, secondary captions   |
| Regular           | 400               | Body text, descriptions, chart axis, table cells |
| SemiBold          | 600               | Headings, KPI values, active buttons, badges     |
| Bold              | 700               | Avoid — breaks the minimal feel                  |
| Black             | 900               | Never — too heavy for any dashboard context      |


### Rules

- Apply `text-wrap: balance` to headings (6 lines or fewer). Apply `text-wrap: pretty` to body paragraphs to prevent orphans.
- Apply `font-variant-numeric: tabular-nums` to any number that updates dynamically — counters, KPI values, prices, timers, table columns. Prevents layout shift as digits change.
- Use `letter-spacing: 0.04em` on uppercase labels (11px). At larger sizes, reduce to `0.02em` or remove entirely.
- Line height: 1.5 for body text, 1.2 for headings, 1 for KPI numbers.

## Color Palette

For curated chart and data visualization palettes (50 palettes across 9 harmony types), see [color-palettes.md](color-palettes.md). The palettes below define the theme's structural colors — backgrounds, surfaces, text, and status indicators.

### Core Colors


| Role             | Hex       | Usage                                              |
| ---------------- | --------- | -------------------------------------------------- |
| Text primary     | `#3F454D` | Headings, card titles, meta labels, active buttons |
| Text secondary   | `#68737F` | Descriptions, captions, filter labels              |
| Background       | `#F1F6FA` | Page background                                    |
| Surface          | `#FFFFFF` | Cards, containers, inputs                          |
| Border           | `#B7C1CB` | Input borders, button borders                      |
| Border light     | `#DCE4EA` | Dividers, progress bar tracks, row borders         |
| Hover background | `#DCE4EA` | Button/row hover                                   |
| Subtle hover bg  | `#F8FAFC` | Table/list row hover                               |
| Accent hover     | `#99CCEE` | Border highlight on hover (inputs, buttons)        |


### Status Colors


| Status   | Primary   | Background | Text      | Usage                 |
| -------- | --------- | ---------- | --------- | --------------------- |
| On Track | `#ADD4C1` | `#e8f3ec`  | `#4a7a5a` | Bars, borders, badges |
| At Risk  | `#FF9922` | `#fff0dd`  | `#c47a10` | Bars, borders, badges |
| Behind   | `#776CB0` | `#eae7f3`  | `#5a5094` | Bars, borders, badges |
| Complete | `#99CCEE` | `#e0f0fa`  | `#5a9abe` | Bars, borders, badges |


### Summary Card Values


| Category | Color     |
| -------- | --------- |
| On Track | `#6a9f7a` |
| At Risk  | `#FF9922` |
| Behind   | `#776CB0` |
| Complete | `#99CCEE` |
| Total    | `#3F454D` |


### Accent / Highlight


| Role        | Hex       | Usage                          |
| ----------- | --------- | ------------------------------ |
| Alert/today | `#e45f5f` | Today marker line, alert color |
| Avatar bg   | `#3F454D` | Initials fallback avatar       |
| Avatar text | `#FFFFFF` | Initials text                  |


## Spacing & Layout

- **Page padding**: 24px
- **Max width**: 1400px, centered
- **Grid gap**: 16px
- **Card grid**: `repeat(auto-fill, minmax(320px, 1fr))`
- **Section gap**: 16px–24px vertical between sections
- **Card padding**: 20px
- **Input/button padding**: 6px 12px (inputs), 6px 14px (filter buttons), 8px 20px (tab buttons)

## Shadows

Three-layer shadows for natural depth. Layer 1 acts as a 1px border ring, layer 2 adds subtle lift, layer 3 provides ambient depth. Shadow color derives from `--text-primary` at low opacity so it stays cohesive on any background.

For **buttons, cards, and containers** that need depth, prefer `box-shadow` over solid borders. Shadows adapt to any background via transparency; solid borders don't. Keep solid borders for layout dividers (`border-b`, `border-t`) and form input outlines (for accessibility).

```css
.card {
  box-shadow: var(--shadow);
  transition-property: box-shadow;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}
.card:hover {
  box-shadow: var(--shadow-hover);
}
```

## Components

### Buttons (Filter / Tab)


| State   | Background | Border    | Text      |
| ------- | ---------- | --------- | --------- |
| Default | `#FFFFFF`  | `#B7C1CB` | `#68737F` |
| Hover   | `#DCE4EA`  | `#99CCEE` | `#3F454D` |
| Active  | `#3F454D`  | `#3F454D` | `#FFFFFF` |


- Ghost/outline style throughout — no fills on default buttons
- Border radius: 6px
- Transition: `transition-property: scale, background-color, border-color, box-shadow; transition-duration: 150ms; transition-timing-function: ease-out;`
- Press feedback: `scale(0.96)` on `:active` — never below `0.95`

### Cards

- White background, 10px radius, subtle shadow
- 4px left border colored by status
- Hover lifts shadow
- Padding: 20px

### Status Badges

- 11px uppercase text, weight 600, letter-spacing 0.5px
- Padding: 3px 8px, 4px radius
- Tinted background with darker matching text (see status colors table)

### Progress Bars

- Track: `#DCE4EA`, 8px height, 4px radius
- Fill: status-colored, `width` transition 0.3s ease

### Owner Avatars

- **Default size**: 22px circle (cards), 18px circle (compact/gantt contexts)
- Image: `border-radius: 50%`, `object-fit: cover`
- Fallback: `#3F454D` circle with white initials (9px default, 8px compact)
- Always `flex-shrink: 0` to prevent squishing
- Paired with name in a flex row with 6px gap

### Select Inputs

- White bg, `#B7C1CB` border, 6px radius
- 13px text, weight 600, `#3F454D` text color
- Hover: `#99CCEE` border

### Summary Cards

- White bg, 10px radius, subtle shadow
- `flex: 1`, min-width 140px
- Label: 12px uppercase secondary text
- Value: 28px weight 700, color per status (see summary card values table)

### Gantt Chart

- Container: white bg, 10px radius, subtle shadow
- Row height: 40px min
- Row dividers: 1px solid `#F1F6FA`
- Row hover: `#F8FAFC`
- Header divider: 2px solid `#DCE4EA`
- Bars: 24px height, 4px radius, status-colored with darker fill layer for progress
- Today line: 2px `#e45f5f` dashed, with 10px label above

## Transitions

Never use `transition: all` or `transition-property: all`. Always specify exact properties — `all` forces the browser to watch every property and causes unexpected transitions on colors, padding, or shadows you didn't intend to animate.


| Element           | Transition                                                                              |
| ----------------- | --------------------------------------------------------------------------------------- |
| Buttons/controls  | `transition-property: scale, background-color, border-color, box-shadow` 150ms ease-out |
| Progress bars     | `transition-property: width` 300ms ease                                                 |
| Card hover shadow | `transition-property: box-shadow` 150ms ease-out                                        |
| Gantt bars        | `transition-property: opacity` 150ms ease (hover to 0.85)                               |


Use CSS transitions for interactive state changes (hover, toggle, open/close) — they can be interrupted mid-animation. Reserve CSS keyframe animations for one-shot sequences (loading spinners, enter animations).

## Micro-Interactions

### Scale on Press

```css
.button {
  transition-property: scale, background-color, border-color, box-shadow;
  transition-duration: 150ms;
  transition-timing-function: ease-out;
}
.button:active { scale: 0.96; }
```

Always use `0.96`. Never below `0.95` — anything smaller feels exaggerated. Add a `data-static` attribute to disable the effect on buttons where motion would distract (e.g., submit buttons in forms).

### Image Outlines

Add a subtle 1px inset outline to images for consistent depth:

```css
img {
  outline: 1px solid oklch(0.374 0.014 256 / 0.1);
  outline-offset: -1px;
}
```

`outline` doesn't affect layout (no added width/height) and `-1px` offset keeps it inset.

## Concentric Border Radius

When nesting rounded elements, the outer radius must equal the inner radius plus the gap between them: `outerRadius = innerRadius + padding`.

With this theme: card radius is 10px, card padding is 20px. Since padding (20px) exceeds the outer radius (10px), inner elements are treated as independent surfaces — use `--radius-btn` (6px) or `--radius-badge` (4px) independently. Concentric math matters most when padding is small (under 24px) and the nested elements are visually close to the outer boundary.

## Dark Mode

The light theme above is the default. For dark mode apps, **prefer a themed DESIGN.md file** from [themes/](themes/) — it provides the complete visual contract including slot mappings, importable JSON, and agent-ready prompts. Currently available: [Charcoal Ember Dark](themes/charcoal-ember-dark.DESIGN.md).

For palettes without a full DESIGN.md, use one of the three curated dark themes defined in [color-palettes.md](color-palettes.md) (D1 Emerald Dark, D2 Neon Magenta Dark, D3 Charcoal Ember Dark). Each includes structural variables (backgrounds, surfaces, text, borders, shadows) and chart series colors.

**Key adaptations when switching to dark mode:**


| Property        | Light mode                     | Dark mode                                     |
| --------------- | ------------------------------ | --------------------------------------------- |
| Page background | `oklch(0.96 0.01 H)`           | `oklch(0.12–0.16 0.005–0.025 H)`              |
| Card surface    | `oklch(1 0 0)` (white)         | `oklch(0.18–0.22 0.01–0.035 H)`               |
| Text primary    | `oklch(0.37 0.014 256)` (dark) | `oklch(0.93–0.97 0.003–0.008 H)` (near-white) |
| Text secondary  | `oklch(0.51 0.016 249)`        | `oklch(0.65–0.75 0.01–0.025 H)`               |
| Borders         | `oklch(0.80 0.015 H)`          | `oklch(0.25–0.35 0.01–0.035 H)`               |
| Shadows         | `oklch(text / 0.04–0.08)`      | `oklch(0 0 0 / 0.20–0.35)` (higher opacity)   |
| Chart series L  | 0.55–0.68                      | 0.70–0.80 (brighter on dark)                  |
| Chart series C  | 0.09–0.13                      | 0.07–0.11 (slightly reduced)                  |
| Status badge bg | light tint `oklch(0.93+ ...)`  | dark tint `oklch(0.20–0.25 ...)`              |


**Component adjustments:**

- Buttons: invert — default bg becomes surface color, text becomes near-white, hover lightens the surface
- Cards: no white background — use `--surface` from the dark palette. Shadow opacity increases
- Status badges: swap to dark-tinted backgrounds with brighter text (L 0.75+)
- Progress bar track: use `--border` instead of `--border-light`
- Avatars: use the theme's accent color instead of `--text-primary` for the circle fill

**Applying in pro-code apps:** Set the dark palette's `--bg` on `html, body` (or use `background: transparent` if the App Studio card frame provides the dark surface). Override `color` to `--text-primary` from the dark palette.

**CRITICAL — App Studio native elements on dark mode:**

When embedding dark mode apps in App Studio, Domo's native elements (hero cards, filter dropdowns, section headers, navigation text) use the theme's `c60` AUTOMATIC_COLOR for font color. `c60` does NOT reliably detect dark backgrounds — it defaults to dark text, making native text invisible on dark card/page surfaces.

**Mandatory fix:** After setting dark mode colors, replace ALL `c60` font color references in the App Studio theme with `c58` (the light text color). This affects `cards[].fontColor`, `navigation[].titleFontColor`, `navigation[].linkFontColor`, `headers[].fontColor`, and every `*FontColor` property in `components[]`. See `app-studio` skill's "Dark Mode Theme" section for the full code pattern.

Without this fix, the left nav, hero card labels, filter labels, and section headers will be invisible.

## Design Principles

- All colors are derived from a cool-gray palette anchored on `--text-primary` (oklch 0.374 0.014 256)
- OKLCH is used for all color values. Hex equivalents are documented as comments. OKLCH enables perceptually uniform palette extension — adjust L for contrast, keep C and H constant
- Status colors are intentionally muted/pastel for bars and borders, with saturated variants only in small text badges
- The theme avoids pure black (`oklch(0 0 0)`) and pure white borders — everything has a slight blue-gray tint
- No bold primary color — soft blue (`--accent-hover`) is used sparingly for accents
- Hierarchy comes from font weight and subtle shadows rather than color
- Shadows use three-layer compositing for natural depth instead of single-layer flat shadows
- Interactive elements have at least 40x40px hit area. Extend with a pseudo-element if the visible element is smaller

