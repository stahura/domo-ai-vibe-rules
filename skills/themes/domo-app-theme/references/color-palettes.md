# Curated Color Palettes

50 palettes designed for dashboards, data visualization, and professional applications. Every value is OKLCH-native for perceptual uniformity — colors within a palette share consistent visual weight.

## How to use

1. Pick a palette by harmony type and mood.
2. Copy the `--c1` through `--c6` variables into your `:root` or component scope.
3. Rename to match your app's semantics (`--series-a`, `--kpi-primary`, etc.).
4. For fewer than 6 series, use `--c1` through `--c3` or `--c4` — the first colors in each palette carry the most visual range.

```css
:root {
  --c1: oklch(0.62 0.11 195);
  --c2: oklch(0.62 0.11 210);
  /* ... */
}
.bar-series-1 { fill: var(--c1); }
.bar-series-2 { fill: var(--c2); }
```

## Design principles behind these palettes

**Consistent lightness**: All colors in a categorical palette share the same L value (±0.02). No color shouts louder than another on the chart.

**Moderate chroma**: C values stay between 0.08–0.13. This is the "quiet, modern" range — distinguishable without being garish. High-chroma saturated colors (C > 0.15) are reserved for single-accent or alert use only.

**sRGB safe**: All values stay within sRGB gamut. No clipping on standard monitors.

**6 colors per palette**: Covers the most common chart series counts (3–6). If you need 7+, extend by shifting L ±0.08 on existing hues.

## Surface tinting

To create a cohesive background that subtly echoes your chosen palette, take the dominant hue and set:

```css
--bg-tint: oklch(0.975 0.006 H);  /* barely-there tint */
--bg-card: oklch(0.995 0.002 H);  /* near-white surface */
```

Replace `H` with the primary hue angle from your palette (e.g., 230 for a blue palette).

## Dark Mode Palettes

Three production-ready dark themes with full structural variables and chart series colors. Each theme includes page background, card surfaces, text colors, borders, and 6 chart series colors — all OKLCH-native.

**General dark mode principles** (apply to any palette):
- Chart series: raise L to 0.70–0.78 so colors pop on dark backgrounds. Reduce C by ~0.02 to avoid oversaturation.
- Surfaces: `oklch(0.18–0.22 0.01–0.03 H)` for cards, `oklch(0.12–0.16 0.008–0.02 H)` for page background.
- Text: primary at L 0.93–0.97, secondary at L 0.65–0.75. Keep slight hue tint matching the theme.
- Borders: L 0.25–0.35 with low chroma, or `rgba(255,255,255, 0.08–0.12)`.
- Shadows: use `rgba(0,0,0, 0.3–0.5)` — dark-on-dark shadow needs higher opacity than light mode.
- Keep the same hue angles as the light palette — only L and C change.

### D1. Emerald Dark

**Green accent on near-black** · SaaS dashboards, analytics, dev tools, sustainability

Inspired by dark-mode dashboard UIs with emerald accent — sidebar nav, bright green KPI highlights, teal-green bar charts on charcoal.

**Structural variables:**

```css
:root {
  /* Surfaces */
  --bg:            oklch(0.14 0.012 155);   /* #1A2420 — page background */
  --surface:       oklch(0.20 0.016 155);   /* #243530 — card background */
  --surface-hover: oklch(0.24 0.018 155);   /* #2C3F38 — row/item hover */

  /* Text */
  --text-primary:   oklch(0.95 0.005 155);  /* #EFF5F2 */
  --text-secondary: oklch(0.70 0.015 155);  /* #8FAA9C */

  /* Borders */
  --border:       oklch(0.30 0.012 155);    /* #3A4D44 */
  --border-light: oklch(0.25 0.010 155);    /* #2F3F37 */

  /* Accent */
  --accent:       oklch(0.72 0.18 155);     /* #2DD47A — bright emerald */
  --accent-muted: oklch(0.72 0.18 155 / 0.15); /* accent at 15% for backgrounds */

  /* Shadows */
  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.20),
    0px 1px 3px -1px oklch(0 0 0 / 0.30),
    0px 2px 6px 0px oklch(0 0 0 / 0.20);
}
```

**Chart series:**

```css
--c1: oklch(0.72 0.16 155);  /* bright emerald — primary */
--c2: oklch(0.76 0.12 145);  /* soft green */
--c3: oklch(0.74 0.11 180);  /* teal */
--c4: oklch(0.78 0.10 135);  /* warm lime-green */
--c5: oklch(0.80 0.08 165);  /* pale mint */
--c6: oklch(0.73 0.10 195);  /* cyan-green */
```

**Status colors (dark mode):**

```css
--on-track:      oklch(0.75 0.14 155);     /* bright green */
--on-track-bg:   oklch(0.25 0.04 155);     /* dark green tint */
--at-risk:       oklch(0.78 0.14 65);      /* bright amber */
--at-risk-bg:    oklch(0.25 0.04 65);      /* dark amber tint */
--behind:        oklch(0.72 0.10 350);     /* soft pink */
--behind-bg:     oklch(0.22 0.03 350);     /* dark pink tint */
```

---

### D2. Neon Magenta Dark

**Hot pink / magenta accent on deep purple-black** · Customer intelligence, CRM, engagement, consumer analytics

Inspired by high-energy dark dashboards with magenta KPI cards, pink bar charts, purple gradients, and sparkline accents.

**Structural variables:**

```css
:root {
  /* Surfaces */
  --bg:            oklch(0.12 0.025 310);   /* #160E22 — deep purple-black */
  --surface:       oklch(0.18 0.035 310);   /* #261A38 — card background */
  --surface-hover: oklch(0.22 0.040 310);   /* #322344 — hover */

  /* Text */
  --text-primary:   oklch(0.95 0.008 340);  /* #F8F0F5 — warm white */
  --text-secondary: oklch(0.68 0.025 320);  /* #9A85A8 — muted lavender */

  /* Borders */
  --border:       oklch(0.28 0.035 310);    /* #3C2850 */
  --border-light: oklch(0.23 0.030 310);    /* #2F2042 */

  /* Accent */
  --accent:       oklch(0.70 0.20 350);     /* #FF3E8A — hot pink */
  --accent-muted: oklch(0.70 0.20 350 / 0.15);

  /* Shadows */
  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.25),
    0px 1px 3px -1px oklch(0 0 0 / 0.35),
    0px 2px 6px 0px oklch(0 0 0 / 0.25);
}
```

**Chart series:**

```css
--c1: oklch(0.70 0.18 350);  /* hot pink — primary */
--c2: oklch(0.65 0.16 330);  /* magenta */
--c3: oklch(0.73 0.14 10);   /* warm rose */
--c4: oklch(0.60 0.14 295);  /* purple */
--c5: oklch(0.78 0.10 350);  /* light pink */
--c6: oklch(0.68 0.12 15);   /* salmon */
```

**Status colors (dark mode):**

```css
--on-track:      oklch(0.75 0.14 155);
--on-track-bg:   oklch(0.20 0.04 155);
--at-risk:       oklch(0.78 0.14 65);
--at-risk-bg:    oklch(0.20 0.04 65);
--behind:        oklch(0.70 0.16 350);
--behind-bg:     oklch(0.20 0.05 350);
```

---

### D3. Charcoal Ember Dark

**Orange accent on neutral charcoal-black** · Benchmarks, leaderboards, performance, dev tools, technical dashboards

Inspired by minimal dark UIs with warm orange data bars on pure charcoal — clean card edges, white text, and gray secondary bars.

**Structural variables:**

```css
:root {
  /* Surfaces */
  --bg:            oklch(0.15 0.005 60);    /* #1E1C1A — near-black warm charcoal */
  --surface:       oklch(0.22 0.006 60);    /* #302C28 — card background */
  --surface-hover: oklch(0.26 0.008 60);    /* #3A3632 — hover */

  /* Text */
  --text-primary:   oklch(0.95 0.003 60);   /* #F5F3F0 — warm white */
  --text-secondary: oklch(0.65 0.008 60);   /* #9A9590 — warm gray */

  /* Borders */
  --border:       oklch(0.30 0.006 60);     /* #464240 */
  --border-light: oklch(0.26 0.005 60);     /* #3A3836 */

  /* Accent */
  --accent:       oklch(0.72 0.16 55);      /* #E87A20 — bright orange */
  --accent-muted: oklch(0.72 0.16 55 / 0.15);

  /* Shadows */
  --shadow:
    0px 0px 0px 1px oklch(0 0 0 / 0.25),
    0px 1px 3px -1px oklch(0 0 0 / 0.35),
    0px 2px 6px 0px oklch(0 0 0 / 0.20);
}
```

**Chart series:**

```css
--c1: oklch(0.72 0.15 55);   /* bright orange — primary */
--c2: oklch(0.76 0.12 70);   /* warm amber */
--c3: oklch(0.55 0.010 60);  /* neutral gray (secondary bars) */
--c4: oklch(0.64 0.14 45);   /* burnt orange */
--c5: oklch(0.80 0.10 80);   /* light gold */
--c6: oklch(0.48 0.015 55);  /* dark warm gray */
```

**Status colors (dark mode):**

```css
--on-track:      oklch(0.75 0.12 155);
--on-track-bg:   oklch(0.22 0.03 155);
--at-risk:       oklch(0.72 0.15 55);
--at-risk-bg:    oklch(0.22 0.03 55);
--behind:        oklch(0.70 0.12 25);
--behind-bg:     oklch(0.22 0.03 25);
```

---

### Using dark palettes in pro-code apps

In `app.js`, define a `COLORS` object from the dark theme variables and set `background: transparent` on the app container (the App Studio card frame provides the dark surface). For standalone apps, use `--bg` on `html,body`.

**Adapting any light palette for dark backgrounds**: Take an existing palette (1–50), raise each color's L by +0.10 to +0.15, and reduce C by 0.02. Example with Pacific Drift (#1):

```css
/* Light (original) */         /* Dark (adapted) */
--c1: oklch(0.63 0.11 195);   --c1: oklch(0.75 0.09 195);
--c2: oklch(0.63 0.11 210);   --c2: oklch(0.75 0.09 210);
--c3: oklch(0.63 0.11 225);   --c3: oklch(0.75 0.09 225);
--c4: oklch(0.63 0.11 238);   --c4: oklch(0.75 0.09 238);
--c5: oklch(0.63 0.09 183);   --c5: oklch(0.75 0.07 183);
--c6: oklch(0.63 0.09 250);   --c6: oklch(0.75 0.07 250);
```

## Choosing a harmony type

| Harmony | Best for | Character |
|---------|----------|-----------|
| Analogous | Single-topic dashboards, trend lines, heatmaps | Calm, cohesive, low contrast between series |
| Monochromatic | Sequential data, single-metric depth, intensity scales | Focused, clean, one-dimensional |
| Triad | Multi-category comparisons, balanced dashboards | Balanced, dynamic, each series distinct |
| Complementary | Before/after, two-variable comparison, binary states | High contrast, tension, dramatic |
| Split Complementary | Primary metric + two supporting dimensions | Contrast with nuance, versatile |
| Square | 4-category comparisons, quadrant charts | Even coverage, democratic |
| Compound | Primary story + supporting context | Rich but controlled, editorial |
| Shades | Heatmaps, choropleth, progress, intensity | Progressive, quantitative |
| Signature | Specific dashboard archetypes, brand-adjacent | Curated, opinionated, ready-to-ship |

---

## Analogous Palettes

Neighboring hues (~30–50° spread). Calm and cohesive — ideal when the data tells one story.

### 1. Pacific Drift

**Teal → Blue** · Corporate analytics, SaaS dashboards

```css
--c1: oklch(0.63 0.11 195);
--c2: oklch(0.63 0.11 210);
--c3: oklch(0.63 0.11 225);
--c4: oklch(0.63 0.11 238);
--c5: oklch(0.63 0.09 183);
--c6: oklch(0.63 0.09 250);
```

### 2. Forest Floor

**Green → Teal** · Environmental, sustainability, agriculture

```css
--c1: oklch(0.60 0.10 140);
--c2: oklch(0.60 0.10 150);
--c3: oklch(0.60 0.10 160);
--c4: oklch(0.60 0.10 170);
--c5: oklch(0.60 0.08 130);
--c6: oklch(0.60 0.08 180);
```

### 3. Desert Bloom

**Coral → Amber** · Marketing, engagement, conversion funnels

```css
--c1: oklch(0.65 0.11 25);
--c2: oklch(0.65 0.11 35);
--c3: oklch(0.65 0.11 45);
--c4: oklch(0.65 0.11 55);
--c5: oklch(0.65 0.09 15);
--c6: oklch(0.65 0.09 65);
```

### 4. Twilight Fade

**Violet → Magenta** · Creative industries, innovation metrics

```css
--c1: oklch(0.60 0.11 270);
--c2: oklch(0.60 0.11 285);
--c3: oklch(0.60 0.11 300);
--c4: oklch(0.60 0.11 315);
--c5: oklch(0.60 0.09 258);
--c6: oklch(0.60 0.09 328);
```

### 5. Golden Hour

**Amber → Yellow** · Finance, performance, revenue

```css
--c1: oklch(0.68 0.11 60);
--c2: oklch(0.68 0.11 70);
--c3: oklch(0.68 0.11 80);
--c4: oklch(0.68 0.11 90);
--c5: oklch(0.68 0.09 50);
--c6: oklch(0.68 0.09 100);
```

### 6. Spring Meadow

**Yellow-green → Green** · Growth metrics, agriculture, health

```css
--c1: oklch(0.63 0.10 105);
--c2: oklch(0.63 0.10 115);
--c3: oklch(0.63 0.10 125);
--c4: oklch(0.63 0.10 135);
--c5: oklch(0.63 0.08 95);
--c6: oklch(0.63 0.08 145);
```

### 7. Coral Reef

**Rose → Warm red** · Lifestyle, health, customer sentiment

```css
--c1: oklch(0.64 0.11 5);
--c2: oklch(0.64 0.11 15);
--c3: oklch(0.64 0.11 25);
--c4: oklch(0.64 0.11 35);
--c5: oklch(0.64 0.09 355);
--c6: oklch(0.64 0.09 45);
```

### 8. Arctic Aurora

**Cyan → Indigo** · Scientific, research, data-heavy analysis

```css
--c1: oklch(0.56 0.13 210);
--c2: oklch(0.56 0.13 225);
--c3: oklch(0.56 0.13 240);
--c4: oklch(0.56 0.13 255);
--c5: oklch(0.56 0.11 198);
--c6: oklch(0.56 0.11 268);
```

---

## Monochromatic Palettes

Single hue, varying lightness and chroma. Focused and clean — best for sequential depth within one metric.

### 9. Deep Ocean

**Blue** · Classic corporate, trustworthy

```css
--c1: oklch(0.45 0.14 235);
--c2: oklch(0.52 0.12 235);
--c3: oklch(0.59 0.11 235);
--c4: oklch(0.66 0.09 235);
--c5: oklch(0.73 0.07 235);
--c6: oklch(0.80 0.05 235);
```

### 10. Slate Garden

**Green** · Sustainability, wellness

```css
--c1: oklch(0.42 0.12 155);
--c2: oklch(0.50 0.11 155);
--c3: oklch(0.58 0.10 155);
--c4: oklch(0.66 0.08 155);
--c5: oklch(0.74 0.06 155);
--c6: oklch(0.82 0.04 155);
```

### 11. Amethyst

**Purple** · Luxury, premium, creative

```css
--c1: oklch(0.40 0.13 295);
--c2: oklch(0.48 0.12 295);
--c3: oklch(0.56 0.10 295);
--c4: oklch(0.64 0.08 295);
--c5: oklch(0.72 0.06 295);
--c6: oklch(0.80 0.04 295);
```

### 12. Terracotta

**Warm brown-orange** · Earthy, retail, heritage brands

```css
--c1: oklch(0.42 0.10 50);
--c2: oklch(0.50 0.10 50);
--c3: oklch(0.58 0.09 50);
--c4: oklch(0.66 0.08 50);
--c5: oklch(0.74 0.06 50);
--c6: oklch(0.82 0.04 50);
```

### 13. Rose Quartz

**Pink-rose** · Lifestyle, beauty, consumer

```css
--c1: oklch(0.45 0.12 350);
--c2: oklch(0.52 0.11 350);
--c3: oklch(0.59 0.10 350);
--c4: oklch(0.66 0.08 350);
--c5: oklch(0.73 0.06 350);
--c6: oklch(0.80 0.04 350);
```

### 14. Graphite

**Neutral cool gray** · Minimal, monochrome-first, content-forward

```css
--c1: oklch(0.35 0.015 260);
--c2: oklch(0.45 0.015 260);
--c3: oklch(0.55 0.012 260);
--c4: oklch(0.65 0.012 260);
--c5: oklch(0.75 0.010 260);
--c6: oklch(0.85 0.008 260);
```

---

## Triad Palettes

Three hues ~120° apart. Balanced and dynamic — each series is clearly distinct without competing.

### 15. Primary Refined

**Red · Green · Blue** (classic reinvented) · General-purpose multi-category

```css
--c1: oklch(0.60 0.10 25);
--c2: oklch(0.60 0.10 145);
--c3: oklch(0.60 0.10 260);
--c4: oklch(0.72 0.06 25);
--c5: oklch(0.72 0.06 145);
--c6: oklch(0.72 0.06 260);
```

### 16. Tropical Balance

**Teal · Magenta · Amber** · Energetic dashboards, social analytics

```css
--c1: oklch(0.62 0.11 190);
--c2: oklch(0.62 0.11 310);
--c3: oklch(0.62 0.11 70);
--c4: oklch(0.74 0.07 190);
--c5: oklch(0.74 0.07 310);
--c6: oklch(0.74 0.07 70);
```

### 17. Nordic Triad

**Sage · Plum · Sand** · Sophisticated, editorial, executive reports

```css
--c1: oklch(0.58 0.09 155);
--c2: oklch(0.58 0.09 275);
--c3: oklch(0.58 0.09 35);
--c4: oklch(0.70 0.06 155);
--c5: oklch(0.70 0.06 275);
--c6: oklch(0.70 0.06 35);
```

### 18. Mineral

**Stone · Teal · Violet** · Quiet, neutral-forward, utilities

```css
--c1: oklch(0.60 0.08 50);
--c2: oklch(0.60 0.08 170);
--c3: oklch(0.60 0.08 290);
--c4: oklch(0.72 0.05 50);
--c5: oklch(0.72 0.05 170);
--c6: oklch(0.72 0.05 290);
```

### 19. Coastal Triad

**Ocean · Coral · Lime** · Travel, hospitality, outdoor

```css
--c1: oklch(0.62 0.11 225);
--c2: oklch(0.62 0.11 345);
--c3: oklch(0.62 0.11 105);
--c4: oklch(0.74 0.07 225);
--c5: oklch(0.74 0.07 345);
--c6: oklch(0.74 0.07 105);
```

### 20. Neon Dusk

**Magenta · Lime · Cyan** · Tech-forward, dev tools, modern SaaS

```css
--c1: oklch(0.63 0.10 325);
--c2: oklch(0.63 0.10 85);
--c3: oklch(0.63 0.10 205);
--c4: oklch(0.75 0.06 325);
--c5: oklch(0.75 0.06 85);
--c6: oklch(0.75 0.06 205);
```

---

## Complementary Palettes

Opposite hues (~180° apart). High contrast between two poles — ideal for binary comparisons, before/after, or two-variable stories.

### 21. Ocean & Ember

**Blue ↔ Orange** · Revenue vs cost, plan vs actual

```css
--c1: oklch(0.55 0.12 230);
--c2: oklch(0.62 0.10 230);
--c3: oklch(0.72 0.07 230);
--c4: oklch(0.57 0.12 50);
--c5: oklch(0.65 0.10 50);
--c6: oklch(0.75 0.07 50);
```

### 22. Forest & Berry

**Green ↔ Magenta** · Growth vs decline, organic vs paid

```css
--c1: oklch(0.53 0.11 155);
--c2: oklch(0.62 0.09 155);
--c3: oklch(0.72 0.06 155);
--c4: oklch(0.53 0.11 335);
--c5: oklch(0.62 0.09 335);
--c6: oklch(0.72 0.06 335);
```

### 23. Midnight & Gold

**Indigo ↔ Gold** · Budget analysis, premium vs standard

```css
--c1: oklch(0.50 0.13 265);
--c2: oklch(0.60 0.11 265);
--c3: oklch(0.70 0.08 265);
--c4: oklch(0.58 0.12 85);
--c5: oklch(0.68 0.10 85);
--c6: oklch(0.78 0.06 85);
```

### 24. Sage & Rose

**Muted green ↔ Muted pink** · Gender splits, soft binary, editorial

```css
--c1: oklch(0.55 0.08 145);
--c2: oklch(0.65 0.06 145);
--c3: oklch(0.75 0.04 145);
--c4: oklch(0.55 0.08 5);
--c5: oklch(0.65 0.06 5);
--c6: oklch(0.75 0.04 5);
```

### 25. Ice & Fire

**Cyan ↔ Red-orange** · Temperature, sentiment, deviation

```css
--c1: oklch(0.55 0.11 210);
--c2: oklch(0.62 0.09 210);
--c3: oklch(0.72 0.06 210);
--c4: oklch(0.58 0.11 30);
--c5: oklch(0.65 0.09 30);
--c6: oklch(0.75 0.06 30);
```

---

## Split Complementary Palettes

Base hue + two hues adjacent to its complement. Contrast with nuance — more versatile than straight complementary.

### 26. Teal Prism

**Teal + Rose + Amber** · Multi-KPI dashboards, balanced reporting

```css
--c1: oklch(0.58 0.11 190);
--c2: oklch(0.68 0.08 190);
--c3: oklch(0.60 0.10 350);
--c4: oklch(0.72 0.07 350);
--c5: oklch(0.63 0.10 50);
--c6: oklch(0.75 0.07 50);
```

### 27. Blue Sunrise

**Blue + Red-orange + Amber** · Performance vs target, time-series overlay

```css
--c1: oklch(0.55 0.12 240);
--c2: oklch(0.65 0.09 240);
--c3: oklch(0.60 0.11 30);
--c4: oklch(0.72 0.07 30);
--c5: oklch(0.65 0.11 80);
--c6: oklch(0.77 0.07 80);
```

### 28. Violet Garden

**Purple + Lime-gold + Green** · Creative performance, content analytics

```css
--c1: oklch(0.55 0.11 290);
--c2: oklch(0.67 0.08 290);
--c3: oklch(0.63 0.10 80);
--c4: oklch(0.75 0.06 80);
--c5: oklch(0.58 0.10 140);
--c6: oklch(0.70 0.06 140);
```

### 29. Crimson Harbor

**Red + Teal + Cyan-blue** · Alert-aware dashboards, ops monitoring

```css
--c1: oklch(0.58 0.11 25);
--c2: oklch(0.70 0.07 25);
--c3: oklch(0.58 0.10 175);
--c4: oklch(0.70 0.07 175);
--c5: oklch(0.56 0.10 215);
--c6: oklch(0.68 0.07 215);
```

### 30. Emerald Dusk

**Emerald + Magenta + Rose** · Sustainability with highlights, ESG

```css
--c1: oklch(0.55 0.10 160);
--c2: oklch(0.67 0.07 160);
--c3: oklch(0.57 0.10 310);
--c4: oklch(0.69 0.07 310);
--c5: oklch(0.60 0.09 350);
--c6: oklch(0.72 0.06 350);
```

---

## Square Palettes

Four hues ~90° apart. Even coverage across the color wheel — democratic, no single hue dominates.

### 31. Cardinal Points

**Red-orange · Green · Blue · Purple** · Balanced 4-category comparison

```css
--c1: oklch(0.60 0.10 30);
--c2: oklch(0.60 0.10 120);
--c3: oklch(0.60 0.10 210);
--c4: oklch(0.60 0.10 300);
--c5: oklch(0.72 0.06 30);
--c6: oklch(0.72 0.06 210);
```

### 32. Seasonal

**Spring green · Summer gold · Autumn red · Winter blue** · Quarterly, YoY, seasonal

```css
--c1: oklch(0.60 0.10 145);
--c2: oklch(0.63 0.10 75);
--c3: oklch(0.60 0.10 25);
--c4: oklch(0.58 0.11 240);
--c5: oklch(0.72 0.06 145);
--c6: oklch(0.75 0.06 75);
```

### 33. Element

**Earth · Water · Fire · Air** · Multi-segment, regional, categorical

```css
--c1: oklch(0.58 0.09 50);
--c2: oklch(0.58 0.11 225);
--c3: oklch(0.58 0.11 20);
--c4: oklch(0.60 0.09 185);
--c5: oklch(0.72 0.05 50);
--c6: oklch(0.70 0.06 225);
```

### 34. Metro

**Blue · Green · Amber · Magenta** · Urban data, transport, infrastructure

```css
--c1: oklch(0.58 0.11 240);
--c2: oklch(0.60 0.10 150);
--c3: oklch(0.65 0.11 65);
--c4: oklch(0.58 0.10 320);
--c5: oklch(0.70 0.07 240);
--c6: oklch(0.72 0.06 150);
```

---

## Compound Palettes

Complementary pair + analogous neighbors of the base. Rich but controlled — supports a primary story with nuanced context.

### 35. Coastal Compound

**Blue base + Orange accent + Teal/Indigo neighbors** · Business intelligence, ops

```css
--c1: oklch(0.60 0.11 220);
--c2: oklch(0.60 0.09 195);
--c3: oklch(0.60 0.09 245);
--c4: oklch(0.62 0.11 40);
--c5: oklch(0.72 0.07 220);
--c6: oklch(0.74 0.06 40);
```

### 36. Botanical

**Green base + Pink accent + Teal/Lime neighbors** · Healthcare, wellness, CPG

```css
--c1: oklch(0.58 0.10 150);
--c2: oklch(0.58 0.08 125);
--c3: oklch(0.58 0.08 175);
--c4: oklch(0.60 0.10 340);
--c5: oklch(0.70 0.06 150);
--c6: oklch(0.72 0.06 340);
```

### 37. Royal Compound

**Purple base + Gold accent + Blue/Magenta neighbors** · Luxury, finance, advisory

```css
--c1: oklch(0.55 0.11 285);
--c2: oklch(0.57 0.09 260);
--c3: oklch(0.57 0.09 310);
--c4: oklch(0.65 0.11 85);
--c5: oklch(0.68 0.07 285);
--c6: oklch(0.77 0.06 85);
```

### 38. Sunset Compound

**Orange base + Blue accent + Red/Gold neighbors** · Media, retail, consumer

```css
--c1: oklch(0.63 0.11 35);
--c2: oklch(0.63 0.09 15);
--c3: oklch(0.65 0.09 55);
--c4: oklch(0.58 0.11 215);
--c5: oklch(0.75 0.06 35);
--c6: oklch(0.70 0.07 215);
```

### 39. Jade Compound

**Teal base + Rose accent + Green/Cyan neighbors** · Real estate, operations

```css
--c1: oklch(0.58 0.10 175);
--c2: oklch(0.58 0.08 155);
--c3: oklch(0.58 0.08 195);
--c4: oklch(0.60 0.10 355);
--c5: oklch(0.70 0.06 175);
--c6: oklch(0.72 0.06 355);
```

---

## Shades Palettes (Sequential)

Single hue, progressive lightness — dark to light. Perfect for heatmaps, choropleth maps, intensity scales, and progress indicators.

### 40. Blue Depth

**Deep navy → Light sky** · Density, volume, concentration

```css
--c1: oklch(0.35 0.14 235);
--c2: oklch(0.44 0.12 235);
--c3: oklch(0.53 0.10 235);
--c4: oklch(0.62 0.08 235);
--c5: oklch(0.71 0.06 235);
--c6: oklch(0.80 0.04 235);
```

### 41. Green Gradient

**Deep forest → Pale mint** · Utilization, saturation, health scores

```css
--c1: oklch(0.35 0.11 160);
--c2: oklch(0.44 0.10 160);
--c3: oklch(0.53 0.09 160);
--c4: oklch(0.62 0.07 160);
--c5: oklch(0.71 0.05 160);
--c6: oklch(0.80 0.03 160);
```

### 42. Warm Gradient

**Deep umber → Light sand** · Revenue tiers, engagement levels

```css
--c1: oklch(0.38 0.10 55);
--c2: oklch(0.47 0.09 55);
--c3: oklch(0.56 0.08 55);
--c4: oklch(0.65 0.07 55);
--c5: oklch(0.74 0.05 55);
--c6: oklch(0.83 0.03 55);
```

### 43. Cool Gray Steps

**Charcoal → Mist** · Neutral intensity, population density, weight

```css
--c1: oklch(0.30 0.012 260);
--c2: oklch(0.40 0.012 260);
--c3: oklch(0.50 0.010 260);
--c4: oklch(0.60 0.010 260);
--c5: oklch(0.70 0.008 260);
--c6: oklch(0.80 0.006 260);
```

### 44. Purple Descent

**Dark plum → Pale lavender** · Risk tiers, priority levels, scoring

```css
--c1: oklch(0.35 0.13 300);
--c2: oklch(0.44 0.11 300);
--c3: oklch(0.53 0.09 300);
--c4: oklch(0.62 0.07 300);
--c5: oklch(0.71 0.05 300);
--c6: oklch(0.80 0.03 300);
```

---

## Signature Palettes

Hand-tuned multi-harmony palettes for specific dashboard archetypes. Ready to ship — no assembly required.

### 45. Fintech Clarity

**Clean, trustworthy, institutional** · Payment dashboards, banking, fintech

```css
--c1: oklch(0.55 0.12 230);
--c2: oklch(0.60 0.10 195);
--c3: oklch(0.63 0.09 155);
--c4: oklch(0.62 0.09 25);
--c5: oklch(0.68 0.10 80);
--c6: oklch(0.70 0.06 260);
```

### 46. Product Precision

**Muted, focused, tool-like** · Project management, dev dashboards, product analytics

```css
--c1: oklch(0.55 0.11 275);
--c2: oklch(0.60 0.09 230);
--c3: oklch(0.62 0.08 195);
--c4: oklch(0.58 0.07 155);
--c5: oklch(0.63 0.09 310);
--c6: oklch(0.68 0.06 60);
```

### 47. Warm Canvas

**Inviting, approachable, editorial** · Content platforms, CMS, knowledge bases

```css
--c1: oklch(0.60 0.08 55);
--c2: oklch(0.62 0.07 35);
--c3: oklch(0.58 0.09 15);
--c4: oklch(0.65 0.06 80);
--c5: oklch(0.57 0.07 160);
--c6: oklch(0.60 0.06 220);
```

### 48. Monochrome Edge

**Near-monochrome + single blue accent** · Minimal, data-dense, developer tools

```css
--c1: oklch(0.35 0.015 250);
--c2: oklch(0.45 0.012 250);
--c3: oklch(0.55 0.010 250);
--c4: oklch(0.65 0.010 250);
--c5: oklch(0.75 0.008 250);
--c6: oklch(0.58 0.12 230);
```

### 49. Vitality

**Energetic, balanced, multi-dimensional** · Health, wellness, fitness, HR

```css
--c1: oklch(0.60 0.12 190);
--c2: oklch(0.62 0.11 145);
--c3: oklch(0.63 0.11 50);
--c4: oklch(0.60 0.11 25);
--c5: oklch(0.58 0.11 285);
--c6: oklch(0.62 0.10 230);
```

### 50. Executive Ink

**Dark, sophisticated, boardroom** · C-suite reports, investor decks, board packs

```css
--c1: oklch(0.45 0.06 235);
--c2: oklch(0.50 0.05 200);
--c3: oklch(0.48 0.05 260);
--c4: oklch(0.53 0.04 180);
--c5: oklch(0.52 0.07 85);
--c6: oklch(0.47 0.05 310);
```
