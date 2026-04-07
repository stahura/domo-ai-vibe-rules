# Chart Palette Overlays for Corporate Light

The [Corporate Light](corporate-light.DESIGN.md) DESIGN.md provides the structural base (backgrounds, text, borders, shadows, typography, components). To change only the chart/data visualization colors, swap the `--c1` through `--c6` variables and the `COLORS.series` array using the overlays below.

All 50 palettes from [color-palettes.md](../color-palettes.md) are listed here with copy-paste-ready CSS and JS overrides.

## How to Apply

1. Start from the Corporate Light DESIGN.md
2. Replace the `:root` chart series block (`--c1` through `--c6`) with the palette below
3. Replace `COLORS.series` in the JS COLORS object
4. Update the theme JSON `chartColorPalette.colorRanges[0]` through `[5]` with the hex values

---

## Analogous Palettes

### 1. Pacific Drift
**Teal to Blue** | Corporate analytics, SaaS dashboards
```css
--c1: oklch(0.63 0.11 195); --c2: oklch(0.63 0.11 210);
--c3: oklch(0.63 0.11 225); --c4: oklch(0.63 0.11 238);
--c5: oklch(0.63 0.09 183); --c6: oklch(0.63 0.09 250);
```
```js
series: ['#3A98AB', '#3A92BC', '#458BC6', '#5283CF', '#449696', '#7D81C7']
```

### 2. Forest Floor
**Green to Teal** | Environmental, sustainability, agriculture
```css
--c1: oklch(0.60 0.10 140); --c2: oklch(0.60 0.10 150);
--c3: oklch(0.60 0.10 160); --c4: oklch(0.60 0.10 170);
--c5: oklch(0.60 0.08 130); --c6: oklch(0.60 0.08 180);
```
```js
series: ['#4A8A5E', '#3A8B6E', '#2D8C7E', '#268D8D', '#5B8952', '#1C8E9E']
```

### 3. Desert Bloom
**Coral to Amber** | Marketing, engagement, conversion funnels
```css
--c1: oklch(0.65 0.11 25); --c2: oklch(0.65 0.11 35);
--c3: oklch(0.65 0.11 45); --c4: oklch(0.65 0.11 55);
--c5: oklch(0.65 0.09 15); --c6: oklch(0.65 0.09 65);
```
```js
series: ['#C07050', '#B87A48', '#AE8442', '#A48E40', '#C0685A', '#9C9640']
```

### 4. Twilight Fade
**Violet to Magenta** | Creative industries, innovation metrics
```css
--c1: oklch(0.60 0.11 270); --c2: oklch(0.60 0.11 285);
--c3: oklch(0.60 0.11 300); --c4: oklch(0.60 0.11 315);
--c5: oklch(0.60 0.09 258); --c6: oklch(0.60 0.09 328);
```
```js
series: ['#7A6CB0', '#8768B8', '#9464B8', '#A060B0', '#6E70A8', '#A85CA0']
```

### 5. Golden Hour
**Amber to Yellow** | Finance, performance, revenue
```css
--c1: oklch(0.68 0.11 60); --c2: oklch(0.68 0.11 70);
--c3: oklch(0.68 0.11 80); --c4: oklch(0.68 0.11 90);
--c5: oklch(0.68 0.09 50); --c6: oklch(0.68 0.09 100);
```
```js
series: ['#B49030', '#AAA028', '#9CAA28', '#8EB430', '#BA8238', '#80B838']
```

### 6. Spring Meadow
**Yellow-green to Green** | Growth metrics, agriculture, health
```css
--c1: oklch(0.63 0.10 105); --c2: oklch(0.63 0.10 115);
--c3: oklch(0.63 0.10 125); --c4: oklch(0.63 0.10 135);
--c5: oklch(0.63 0.08 95); --c6: oklch(0.63 0.08 145);
```
```js
series: ['#6E9838', '#5C9C42', '#4A9C52', '#3C9A62', '#809434', '#2E9878']
```

### 7. Coral Reef
**Rose to Warm red** | Lifestyle, health, customer sentiment
```css
--c1: oklch(0.64 0.11 5); --c2: oklch(0.64 0.11 15);
--c3: oklch(0.64 0.11 25); --c4: oklch(0.64 0.11 35);
--c5: oklch(0.64 0.09 355); --c6: oklch(0.64 0.09 45);
```
```js
series: ['#C06068', '#BC6858', '#B47050', '#AA7848', '#B85A72', '#A08248']
```

### 8. Arctic Aurora
**Cyan to Indigo** | Scientific, research, data-heavy analysis
```css
--c1: oklch(0.56 0.13 210); --c2: oklch(0.56 0.13 225);
--c3: oklch(0.56 0.13 240); --c4: oklch(0.56 0.13 255);
--c5: oklch(0.56 0.11 198); --c6: oklch(0.56 0.11 268);
```
```js
series: ['#2080A0', '#2878B0', '#3070B8', '#4068C0', '#188898', '#5060C0']
```

---

## Monochromatic Palettes

### 9. Deep Ocean
**Blue** | Classic corporate, trustworthy
```css
--c1: oklch(0.45 0.14 235); --c2: oklch(0.52 0.12 235);
--c3: oklch(0.59 0.11 235); --c4: oklch(0.66 0.09 235);
--c5: oklch(0.73 0.07 235); --c6: oklch(0.80 0.05 235);
```
```js
series: ['#1A4C8A', '#2E60A0', '#4474B0', '#5C8ABC', '#78A0C8', '#96B6D4']
```

### 10. Slate Garden
**Green** | Sustainability, wellness
```css
--c1: oklch(0.42 0.12 155); --c2: oklch(0.50 0.11 155);
--c3: oklch(0.58 0.10 155); --c4: oklch(0.66 0.08 155);
--c5: oklch(0.74 0.06 155); --c6: oklch(0.82 0.04 155);
```
```js
series: ['#1E5040', '#2C6450', '#3C7860', '#508C72', '#6CA088', '#8CB4A0']
```

### 11. Amethyst
**Purple** | Luxury, premium, creative
```css
--c1: oklch(0.40 0.13 295); --c2: oklch(0.48 0.12 295);
--c3: oklch(0.56 0.10 295); --c4: oklch(0.64 0.08 295);
--c5: oklch(0.72 0.06 295); --c6: oklch(0.80 0.04 295);
```
```js
series: ['#3C2880', '#503C94', '#6650A4', '#7E68B0', '#9480BC', '#AC98C8']
```

### 12. Terracotta
**Warm brown-orange** | Earthy, retail, heritage brands
```css
--c1: oklch(0.42 0.10 50); --c2: oklch(0.50 0.10 50);
--c3: oklch(0.58 0.09 50); --c4: oklch(0.66 0.08 50);
--c5: oklch(0.74 0.06 50); --c6: oklch(0.82 0.04 50);
```
```js
series: ['#4A3220', '#604630', '#785C42', '#907456', '#A88E70', '#C0A88C']
```

### 13. Rose Quartz
**Pink-rose** | Lifestyle, beauty, consumer
```css
--c1: oklch(0.45 0.12 350); --c2: oklch(0.52 0.11 350);
--c3: oklch(0.59 0.10 350); --c4: oklch(0.66 0.08 350);
--c5: oklch(0.73 0.06 350); --c6: oklch(0.80 0.04 350);
```
```js
series: ['#6A2848', '#803C58', '#965068', '#AA6880', '#BC8098', '#D098B0']
```

### 14. Graphite
**Neutral cool gray** | Minimal, monochrome-first, content-forward
```css
--c1: oklch(0.35 0.015 260); --c2: oklch(0.45 0.015 260);
--c3: oklch(0.55 0.012 260); --c4: oklch(0.65 0.012 260);
--c5: oklch(0.75 0.010 260); --c6: oklch(0.85 0.008 260);
```
```js
series: ['#3A3E44', '#525862', '#6C747E', '#88929C', '#A4AEB8', '#C0C8D0']
```

---

## Triad Palettes

### 15. Primary Refined
**Red, Green, Blue** | General-purpose multi-category
```css
--c1: oklch(0.60 0.10 25); --c2: oklch(0.60 0.10 145);
--c3: oklch(0.60 0.10 260); --c4: oklch(0.72 0.06 25);
--c5: oklch(0.72 0.06 145); --c6: oklch(0.72 0.06 260);
```
```js
series: ['#A86050', '#3C8A5C', '#5870B0', '#C09888', '#7CB898', '#98A8CC']
```

### 16. Tropical Balance
**Teal, Magenta, Amber** | Energetic dashboards, social analytics
```css
--c1: oklch(0.62 0.11 190); --c2: oklch(0.62 0.11 310);
--c3: oklch(0.62 0.11 70); --c4: oklch(0.74 0.07 190);
--c5: oklch(0.74 0.07 310); --c6: oklch(0.74 0.07 70);
```
```js
series: ['#2A8C90', '#9458A0', '#A08830', '#60B0B0', '#B890C0', '#C0B070']
```

### 17. Nordic Triad
**Sage, Plum, Sand** | Sophisticated, editorial, executive reports
```css
--c1: oklch(0.58 0.09 155); --c2: oklch(0.58 0.09 275);
--c3: oklch(0.58 0.09 35); --c4: oklch(0.70 0.06 155);
--c5: oklch(0.70 0.06 275); --c6: oklch(0.70 0.06 35);
```
```js
series: ['#3A7860', '#6860A0', '#986850', '#6CA088', '#908CC0', '#C09888']
```

### 18. Mineral
**Stone, Teal, Violet** | Quiet, neutral-forward, utilities
```css
--c1: oklch(0.60 0.08 50); --c2: oklch(0.60 0.08 170);
--c3: oklch(0.60 0.08 290); --c4: oklch(0.72 0.05 50);
--c5: oklch(0.72 0.05 170); --c6: oklch(0.72 0.05 290);
```
```js
series: ['#907050', '#3C8C80', '#7868A0', '#B8A890', '#78B0A8', '#A898C0']
```

### 19. Coastal Triad
**Ocean, Coral, Lime** | Travel, hospitality, outdoor
```css
--c1: oklch(0.62 0.11 225); --c2: oklch(0.62 0.11 345);
--c3: oklch(0.62 0.11 105); --c4: oklch(0.74 0.07 225);
--c5: oklch(0.74 0.07 345); --c6: oklch(0.74 0.07 105);
```
```js
series: ['#3880B0', '#B05070', '#6C9840', '#78A8CC', '#CC88A0', '#98BC78']
```

### 20. Neon Dusk
**Magenta, Lime, Cyan** | Tech-forward, dev tools, modern SaaS
```css
--c1: oklch(0.63 0.10 325); --c2: oklch(0.63 0.10 85);
--c3: oklch(0.63 0.10 205); --c4: oklch(0.75 0.06 325);
--c5: oklch(0.75 0.06 85); --c6: oklch(0.75 0.06 205);
```
```js
series: ['#A05890', '#909830', '#3088A0', '#C890B8', '#B0B870', '#70B0C0']
```

---

## Complementary Palettes

### 21. Ocean & Ember
**Blue vs Orange** | Revenue vs cost, plan vs actual
```css
--c1: oklch(0.55 0.12 230); --c2: oklch(0.62 0.10 230);
--c3: oklch(0.72 0.07 230); --c4: oklch(0.57 0.12 50);
--c5: oklch(0.65 0.10 50); --c6: oklch(0.75 0.07 50);
```
```js
series: ['#2868A0', '#3C80B0', '#6CA0C8', '#906840', '#A88050', '#C0A078']
```

### 22. Forest & Berry
**Green vs Magenta** | Growth vs decline, organic vs paid
```css
--c1: oklch(0.53 0.11 155); --c2: oklch(0.62 0.09 155);
--c3: oklch(0.72 0.06 155); --c4: oklch(0.53 0.11 335);
--c5: oklch(0.62 0.09 335); --c6: oklch(0.72 0.06 335);
```
```js
series: ['#2A6048', '#3C7860', '#6CA088', '#803858', '#984C70', '#BC8098']
```

### 23. Midnight & Gold
**Indigo vs Gold** | Budget analysis, premium vs standard
```css
--c1: oklch(0.50 0.13 265); --c2: oklch(0.60 0.11 265);
--c3: oklch(0.70 0.08 265); --c4: oklch(0.58 0.12 85);
--c5: oklch(0.68 0.10 85); --c6: oklch(0.78 0.06 85);
```
```js
series: ['#3C48A0', '#5060B0', '#7888C0', '#908820', '#A8A038', '#C0B870']
```

### 24. Sage & Rose
**Muted green vs Muted pink** | Gender splits, soft binary, editorial
```css
--c1: oklch(0.55 0.08 145); --c2: oklch(0.65 0.06 145);
--c3: oklch(0.75 0.04 145); --c4: oklch(0.55 0.08 5);
--c5: oklch(0.65 0.06 5); --c6: oklch(0.75 0.04 5);
```
```js
series: ['#487058', '#6C9078', '#94B0A0', '#905868', '#A87888', '#C098A8']
```

### 25. Ice & Fire
**Cyan vs Red-orange** | Temperature, sentiment, deviation
```css
--c1: oklch(0.55 0.11 210); --c2: oklch(0.62 0.09 210);
--c3: oklch(0.72 0.06 210); --c4: oklch(0.58 0.11 30);
--c5: oklch(0.65 0.09 30); --c6: oklch(0.75 0.06 30);
```
```js
series: ['#207890', '#3890A0', '#6CB0C0', '#A06848', '#B07858', '#C8A080']
```

---

## Split Complementary Palettes

### 26. Teal Prism
**Teal + Rose + Amber** | Multi-KPI dashboards, balanced reporting
```css
--c1: oklch(0.58 0.11 190); --c2: oklch(0.68 0.08 190);
--c3: oklch(0.60 0.10 350); --c4: oklch(0.72 0.07 350);
--c5: oklch(0.63 0.10 50); --c6: oklch(0.75 0.07 50);
```
```js
series: ['#2A7C88', '#50A0A8', '#A85868', '#C88898', '#987048', '#C0A078']
```

### 27. Blue Sunrise
**Blue + Red-orange + Amber** | Performance vs target, time-series overlay
```css
--c1: oklch(0.55 0.12 240); --c2: oklch(0.65 0.09 240);
--c3: oklch(0.60 0.11 30); --c4: oklch(0.72 0.07 30);
--c5: oklch(0.65 0.11 80); --c6: oklch(0.77 0.07 80);
```
```js
series: ['#2060A8', '#4C88C0', '#A86848', '#C09878', '#909430', '#B8B870']
```

### 28. Violet Garden
**Purple + Lime-gold + Green** | Creative performance, content analytics
```css
--c1: oklch(0.55 0.11 290); --c2: oklch(0.67 0.08 290);
--c3: oklch(0.63 0.10 80); --c4: oklch(0.75 0.06 80);
--c5: oklch(0.58 0.10 140); --c6: oklch(0.70 0.06 140);
```
```js
series: ['#6050A8', '#8878C0', '#989430', '#B8B870', '#488C50', '#78B080']
```

### 29. Crimson Harbor
**Red + Teal + Cyan-blue** | Alert-aware dashboards, ops monitoring
```css
--c1: oklch(0.58 0.11 25); --c2: oklch(0.70 0.07 25);
--c3: oklch(0.58 0.10 175); --c4: oklch(0.70 0.07 175);
--c5: oklch(0.56 0.10 215); --c6: oklch(0.68 0.07 215);
```
```js
series: ['#A06050', '#C09888', '#2C8888', '#60B0B0', '#2078A0', '#4898B8']
```

### 30. Emerald Dusk
**Emerald + Magenta + Rose** | Sustainability with highlights, ESG
```css
--c1: oklch(0.55 0.10 160); --c2: oklch(0.67 0.07 160);
--c3: oklch(0.57 0.10 310); --c4: oklch(0.69 0.07 310);
--c5: oklch(0.60 0.09 350); --c6: oklch(0.72 0.06 350);
```
```js
series: ['#2C7060', '#5C9888', '#7C50A0', '#A080B8', '#A05870', '#C08098']
```

---

## Square Palettes

### 31. Cardinal Points
**Red-orange, Green, Blue, Purple** | Balanced 4-category comparison
```css
--c1: oklch(0.60 0.10 30); --c2: oklch(0.60 0.10 120);
--c3: oklch(0.60 0.10 210); --c4: oklch(0.60 0.10 300);
--c5: oklch(0.72 0.06 30); --c6: oklch(0.72 0.06 210);
```
```js
series: ['#A86850', '#5C9438', '#2080A0', '#8860B0', '#C09888', '#60B0C0']
```

### 32. Seasonal
**Spring, Summer, Autumn, Winter** | Quarterly, YoY, seasonal
```css
--c1: oklch(0.60 0.10 145); --c2: oklch(0.63 0.10 75);
--c3: oklch(0.60 0.10 25); --c4: oklch(0.58 0.11 240);
--c5: oklch(0.72 0.06 145); --c6: oklch(0.75 0.06 75);
```
```js
series: ['#3C8A5C', '#A09830', '#A86050', '#2868A0', '#7CB898', '#C0B870']
```

### 33. Element
**Earth, Water, Fire, Air** | Multi-segment, regional, categorical
```css
--c1: oklch(0.58 0.09 50); --c2: oklch(0.58 0.11 225);
--c3: oklch(0.58 0.11 20); --c4: oklch(0.60 0.09 185);
--c5: oklch(0.72 0.05 50); --c6: oklch(0.70 0.06 225);
```
```js
series: ['#886840', '#2868A0', '#A05850', '#388888', '#B8A890', '#4890B8']
```

### 34. Metro
**Blue, Green, Amber, Magenta** | Urban data, transport, infrastructure
```css
--c1: oklch(0.58 0.11 240); --c2: oklch(0.60 0.10 150);
--c3: oklch(0.65 0.11 65); --c4: oklch(0.58 0.10 320);
--c5: oklch(0.70 0.07 240); --c6: oklch(0.72 0.06 150);
```
```js
series: ['#2868A0', '#3C886C', '#A89030', '#9050A0', '#5090C0', '#6CB098']
```

---

## Compound Palettes

### 35. Coastal Compound
**Blue base + Orange accent** | Business intelligence, ops
```css
--c1: oklch(0.60 0.11 220); --c2: oklch(0.60 0.09 195);
--c3: oklch(0.60 0.09 245); --c4: oklch(0.62 0.11 40);
--c5: oklch(0.72 0.07 220); --c6: oklch(0.74 0.06 40);
```
```js
series: ['#3078A8', '#2C8898', '#4070B0', '#AC7848', '#6CA0C8', '#C0A078']
```

### 36. Botanical
**Green base + Pink accent** | Healthcare, wellness, CPG
```css
--c1: oklch(0.58 0.10 150); --c2: oklch(0.58 0.08 125);
--c3: oklch(0.58 0.08 175); --c4: oklch(0.60 0.10 340);
--c5: oklch(0.70 0.06 150); --c6: oklch(0.72 0.06 340);
```
```js
series: ['#3C8068', '#508C4C', '#308880', '#A05878', '#6CA890', '#B888A0']
```

### 37. Royal Compound
**Purple base + Gold accent** | Luxury, finance, advisory
```css
--c1: oklch(0.55 0.11 285); --c2: oklch(0.57 0.09 260);
--c3: oklch(0.57 0.09 310); --c4: oklch(0.65 0.11 85);
--c5: oklch(0.68 0.07 285); --c6: oklch(0.77 0.06 85);
```
```js
series: ['#5848A0', '#4860A8', '#804CA0', '#A09830', '#8880B8', '#C0B870']
```

### 38. Sunset Compound
**Orange base + Blue accent** | Media, retail, consumer
```css
--c1: oklch(0.63 0.11 35); --c2: oklch(0.63 0.09 15);
--c3: oklch(0.65 0.09 55); --c4: oklch(0.58 0.11 215);
--c5: oklch(0.75 0.06 35); --c6: oklch(0.70 0.07 215);
```
```js
series: ['#B07848', '#B06858', '#A88C40', '#2878A0', '#C8A888', '#4898B8']
```

### 39. Jade Compound
**Teal base + Rose accent** | Real estate, operations
```css
--c1: oklch(0.58 0.10 175); --c2: oklch(0.58 0.08 155);
--c3: oklch(0.58 0.08 195); --c4: oklch(0.60 0.10 355);
--c5: oklch(0.70 0.06 175); --c6: oklch(0.72 0.06 355);
```
```js
series: ['#2C8480', '#3C7C68', '#208888', '#A85868', '#60ACA8', '#C08898']
```

---

## Shades Palettes (Sequential)

### 40. Blue Depth
**Deep navy to Light sky** | Density, volume, concentration
```css
--c1: oklch(0.35 0.14 235); --c2: oklch(0.44 0.12 235);
--c3: oklch(0.53 0.10 235); --c4: oklch(0.62 0.08 235);
--c5: oklch(0.71 0.06 235); --c6: oklch(0.80 0.04 235);
```
```js
series: ['#0C3470', '#1C4888', '#30609C', '#4C78B0', '#6C94C4', '#90B0D4']
```

### 41. Green Gradient
**Deep forest to Pale mint** | Utilization, saturation, health scores
```css
--c1: oklch(0.35 0.11 160); --c2: oklch(0.44 0.10 160);
--c3: oklch(0.53 0.09 160); --c4: oklch(0.62 0.07 160);
--c5: oklch(0.71 0.05 160); --c6: oklch(0.80 0.03 160);
```
```js
series: ['#103828', '#1C4C38', '#306448', '#487C60', '#6C9880', '#90B4A0']
```

### 42. Warm Gradient
**Deep umber to Light sand** | Revenue tiers, engagement levels
```css
--c1: oklch(0.38 0.10 55); --c2: oklch(0.47 0.09 55);
--c3: oklch(0.56 0.08 55); --c4: oklch(0.65 0.07 55);
--c5: oklch(0.74 0.05 55); --c6: oklch(0.83 0.03 55);
```
```js
series: ['#3C2818', '#543C28', '#705438', '#8C6E50', '#A88C70', '#C4A890']
```

### 43. Cool Gray Steps
**Charcoal to Mist** | Neutral intensity, population density
```css
--c1: oklch(0.30 0.012 260); --c2: oklch(0.40 0.012 260);
--c3: oklch(0.50 0.010 260); --c4: oklch(0.60 0.010 260);
--c5: oklch(0.70 0.008 260); --c6: oklch(0.80 0.006 260);
```
```js
series: ['#2E3238', '#444A52', '#5E666E', '#7A8490', '#98A0A8', '#B4BCC2']
```

### 44. Purple Descent
**Dark plum to Pale lavender** | Risk tiers, priority levels
```css
--c1: oklch(0.35 0.13 300); --c2: oklch(0.44 0.11 300);
--c3: oklch(0.53 0.09 300); --c4: oklch(0.62 0.07 300);
--c5: oklch(0.71 0.05 300); --c6: oklch(0.80 0.03 300);
```
```js
series: ['#2C1860', '#442C78', '#5E4490', '#785EA4', '#9478B8', '#B098CC']
```

---

## Signature Palettes

### 45. Fintech Clarity
**Clean, trustworthy, institutional** | Payment dashboards, banking
```css
--c1: oklch(0.55 0.12 230); --c2: oklch(0.60 0.10 195);
--c3: oklch(0.63 0.09 155); --c4: oklch(0.62 0.09 25);
--c5: oklch(0.68 0.10 80); --c6: oklch(0.70 0.06 260);
```
```js
series: ['#2868A0', '#2C8898', '#3C886C', '#A07050', '#A09830', '#7080B0']
```

### 46. Product Precision
**Muted, focused, tool-like** | Project management, dev dashboards
```css
--c1: oklch(0.55 0.11 275); --c2: oklch(0.60 0.09 230);
--c3: oklch(0.62 0.08 195); --c4: oklch(0.58 0.07 155);
--c5: oklch(0.63 0.09 310); --c6: oklch(0.68 0.06 60);
```
```js
series: ['#5050A0', '#3878A8', '#3C8C90', '#4C7C64', '#885CA0', '#A09060']
```

### 47. Warm Canvas
**Inviting, approachable, editorial** | Content platforms, CMS
```css
--c1: oklch(0.60 0.08 55); --c2: oklch(0.62 0.07 35);
--c3: oklch(0.58 0.09 15); --c4: oklch(0.65 0.06 80);
--c5: oklch(0.57 0.07 160); --c6: oklch(0.60 0.06 220);
```
```js
series: ['#907050', '#986858', '#985C5C', '#909444', '#487868', '#507890']
```

### 48. Monochrome Edge
**Near-monochrome + single blue accent** | Minimal, developer tools
```css
--c1: oklch(0.35 0.015 250); --c2: oklch(0.45 0.012 250);
--c3: oklch(0.55 0.010 250); --c4: oklch(0.65 0.010 250);
--c5: oklch(0.75 0.008 250); --c6: oklch(0.58 0.12 230);
```
```js
series: ['#383C44', '#4C5260', '#64707C', '#808C98', '#9CA8B4', '#3070A8']
```

### 49. Vitality
**Energetic, multi-dimensional** | Health, wellness, fitness, HR
```css
--c1: oklch(0.60 0.12 190); --c2: oklch(0.62 0.11 145);
--c3: oklch(0.63 0.11 50); --c4: oklch(0.60 0.11 25);
--c5: oklch(0.58 0.11 285); --c6: oklch(0.62 0.10 230);
```
```js
series: ['#2A8890', '#3C885C', '#A07840', '#A06050', '#6050A8', '#3080B0']
```

### 50. Executive Ink
**Dark, sophisticated, boardroom** | C-suite reports, investor decks
```css
--c1: oklch(0.45 0.06 235); --c2: oklch(0.50 0.05 200);
--c3: oklch(0.48 0.05 260); --c4: oklch(0.53 0.04 180);
--c5: oklch(0.52 0.07 85); --c6: oklch(0.47 0.05 310);
```
```js
series: ['#485870', '#4C6870', '#504C78', '#587878', '#6C6840', '#584870']
```
