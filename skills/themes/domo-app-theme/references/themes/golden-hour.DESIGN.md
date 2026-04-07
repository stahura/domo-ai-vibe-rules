# Golden Hour — Domo App Studio Design System

> **Mode**: Light · **Accent family**: Golden amber / dusky purple · **Mood**: Warm editorial, regal complementary contrast

---

## 1. Visual Theme and Atmosphere

**Personality**: Warm cream canvas (`#FFF9F0`), white cards, **dusky purple** nav (`#3A2E4A`) and **golden amber** accent (`#E8A849`). Purple dusk (`#6B5B7B`) belongs in data and secondary UI—not full-page fills.

**Density**: Medium density: airy content, 20px card padding. Purple nav anchors the shell; keep the canvas warm and photographic.

**Philosophy**: Complementary contrast: purple structure, gold interaction. Avoid extra jewel tones in chrome.

**Atmosphere cues**:
- Cream field reduces glare.
- Nav links in JSON use **`c2` white** on `c4`.
- Gold for tabs, focus, primary CTA.
- Warm type `#2A2420` / `#7A6E60`.

---

## 2. Color System

### 2.1 Semantic Palette

Every color exists in three representations. **Semantic Role** is the source of truth; **Theme Slot** must match the JSON in §8.

| Semantic Role | Hex | OKLCH | Theme Slot | CSS Variable |
|---------------|-----|-------|------------|--------------|
| Page Background (reference) | `#FFF9F0` | `oklch(0.984 0.014 78.3)` | `c1` | `--bg-ref` |
| Page Background (App Studio) | `#FFF9F0` | `oklch(0.984 0.014 78.3)` | `c56` | `--bg` |
| Card Surface | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c2` | `--surface` |
| Surface Hover | `#F8F0E4` | `oklch(0.958 0.018 78.2)` | `c3` | `--surface-hover` |
| Navigation Background | `#3A2E4A` | `oklch(0.327 0.051 303.4)` | `c4` | `--nav-bg` |
| Navigation Active | `#4E4060` | `oklch(0.400 0.055 304.0)` | `c5` | `--nav-active` |
| Nav Item Hover (pro-code) | `#443858` | `oklch(0.368 0.056 300.9)` | `—` | `--nav-hover` |
| Header Background | `#FFF9F0` | `oklch(0.984 0.014 78.3)` | `c6` | `--header-bg` |
| Input Background | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c7` | `--input-bg` |
| Tab Default Background | `#FFFFFF` | `oklch(1.000 0.000 0.0)` | `c8` | `--tab-bg` |
| Tab Active Background | `#E8A849` | `oklch(0.775 0.133 74.1)` | `c9` | `--tab-active-bg` |
| Table Header Background | `#F8F0E4` | `oklch(0.958 0.018 78.2)` | `c10` | `--table-header-bg` |
| Table Row Stripe | `#FFF9F0` | `oklch(0.984 0.014 78.3)` | `c11` | `--table-stripe` |
| Table Row Hover | `#F8F0E4` | `oklch(0.958 0.018 78.2)` | `c12` | `--table-row-hover` |
| Accent Primary | `#E8A849` | `oklch(0.775 0.133 74.1)` | `c29` | `--accent` |
| Accent Pressed | `#D49838` | `oklch(0.721 0.130 75.2)` | `c30` | `--accent-pressed` |
| Secondary (purple dusk) | `#6B5B7B` | `oklch(0.499 0.053 307.3)` | `—` | `--accent-secondary` |
| Primary Text (FONT) | `#2A2420` | `oklch(0.266 0.012 55.8)` | `c58` | `--text-primary` |
| Secondary Text (FONT) | `#7A6E60` | `oklch(0.545 0.026 71.5)` | `c59` | `--text-secondary` |
| Border | `#D4C8B8` | `oklch(0.838 0.026 75.2)` | `c46` | `--border` |
| Border Light | `#E4DAD0` | `oklch(0.894 0.017 67.6)` | `c47` | `--border-light` |
| Input Border | `#D4C8B8` | `oklch(0.838 0.026 75.2)` | `c48` | `--input-border` |
| Grayscale 1 | `#120F0C` | `oklch(0.171 0.008 67.3)` | `c40` | `--warm-gray-0` |
| Grayscale 2 | `#181410` | `oklch(0.195 0.010 67.2)` | `c41` | `--warm-gray-1` |
| Grayscale 3 | `#1E1A16` | `oklch(0.221 0.010 67.3)` | `c42` | `--warm-gray-2` |
| Grayscale 4 | `#26211C` | `oklch(0.252 0.012 67.2)` | `c43` | `--warm-gray-3` |
| Grayscale 5 | `#302A24` | `oklch(0.290 0.014 67.2)` | `c44` | `--warm-gray-4` |
| Grayscale 6 | `#3C352E` | `oklch(0.334 0.016 67.3)` | `c45` | `--warm-gray-5` |
| Grayscale 7 | `#6A6058` | `oklch(0.496 0.018 61.1)` | `c49` | `--warm-gray-mid-7` |
| Grayscale 8 | `#7A7068` | `oklch(0.552 0.017 61.1)` | `c50` | `--warm-gray-mid-8` |
| Grayscale 9 | `#8C8278` | `oklch(0.613 0.019 67.5)` | `c51` | `--warm-gray-mid-9` |
| Grayscale 10 | `#9E948A` | `oklch(0.672 0.019 67.5)` | `c52` | `--warm-gray-mid-10` |
| Grayscale 11 | `#B5ABA0` | `oklch(0.746 0.019 70.2)` | `c53` | `--warm-gray-mid-11` |
| Grayscale 12 | `#CEC4B8` | `oklch(0.825 0.020 72.5)` | `c54` | `--warm-gray-mid-12` |

**Slot mapping**: `c1` = page background reference; `c2` = card surface; `c3` = hover; `c4` = navigation background; `c5` = navigation active; `c6` = header background; `c7` = input background; `c8`–`c12` = tabs and table surfaces; `c29` / `c30` = accent / accent pressed; `c40`–`c54` = grayscale ramp (with `c46`–`c48` as border, border-light, input border); `c56` = page background (App Studio); `c58` / `c59` = primary / secondary text (FONT). On **dark** themes, `c58` is light (`#E0…` range) and `c59` dimmer. On **light** themes, `c58` is dark and `c59` medium. Prefer explicit `c58`/`c59` over `c60` for navigation.

### 2.2 Status Colors

| Status | Primary | Background | Text | OKLCH (primary) | CSS Variable |
|--------|---------|------------|------|-----------------|--------------|
| On Track | `#4A8A6A` | `#E8F5EE` | `#2A5A40` | `oklch(0.581 0.083 160.5)` | `--status-on-track` |
| At Risk | `#D49440` | `#FFF4E8` | `#8A5010` | `oklch(0.714 0.125 70.5)` | `--status-at-risk` |
| Behind | `#8A6AAA` | `#F0EAF8` | `#5A4080` | `oklch(0.581 0.102 306.5)` | `--status-behind` |
| Complete | `#E8A849` | `#FFF8EC` | `#8A6010` | `oklch(0.775 0.133 74.1)` | `--status-complete` |

### 2.3 Shadows

```css
--shadow:
  0px 0px 0px 1px oklch(0.266 0.012 55.8 / 0.06),
  0px 1px 3px -1px oklch(0.266 0.012 55.8 / 0.06),
  0px 4px 14px 0px oklch(0.266 0.012 55.8 / 0.05);
--shadow-hover:
  0px 0px 0px 1px oklch(0.266 0.012 55.8 / 0.09),
  0px 3px 8px -1px oklch(0.266 0.012 55.8 / 0.07),
  0px 10px 24px 0px oklch(0.266 0.012 55.8 / 0.06);
```

---

## 3. Typography

### 3.1 Font System

```css
font-family: Georgia, "Times New Roman", Times, serif;
```

App Studio: **Serif** on **all** slots `f1`–`f8`.

### 3.2 Type Scale

| Role | Size | Weight | CSS `font-weight` | Theme Font Slot | Extra |
|------|------|--------|-------------------|-----------------|-------|
| Page title | 22px | SemiBold | 600 | `f1` | `text-wrap: balance` |
| Card / section titles | 16px | SemiBold | 600 | `f2` | `text-wrap: balance` |
| Body text / descriptions | 13px | Regular | 400 | `f3` | line-height 1.5; `text-wrap: pretty` |
| Labels / captions | 11px | Regular | 400 | `f4` | uppercase; `letter-spacing: 0.04em` |
| Chart axis text | 11px | Regular | 400 | `f5` | SVG `fill`, not CSS `color` |
| Badges / status text | 11px | SemiBold | 600 | `f6` | uppercase; `letter-spacing: 0.04em` |
| KPI numbers | 28px | SemiBold | 600 | `f7` | `font-variant-numeric: tabular-nums` |
| KPI labels | 11px | Light | 300 | `f8` | uppercase; `letter-spacing: 0.04em`; `c59` |

### 3.3 Weight Rules

- **600** titles, KPIs, badges.
- **400** body and axes.
- **300** KPI labels.
- Italics only for quotes—not tables.

---

## 4. Card Styles

| Property | Value | Theme mapping / notes |
|----------|-------|----------------------|
| Background | `c2` white | `ca1.backgroundColor` |
| Font color | `c58` | `ca1.fontColor` |
| Radius / shadow | `10` / `true` | Editorial softness |
| Accent | `c29` gold | `ca1.accentColor` |

---

## 5. Navigation

| Property | Value | Theme mapping / notes |
|----------|-------|----------------------|
| Background | `c4` purple | `navigation.backgroundColor` |
| Link / title colors | `c2` white | JSON on dark nav |
| Active link | `c29` | `activeLinkFontColor` |
| Indicator | `c29` | `navigation.activeColor` |

---

## 6. Chart Color Palette

| Index | Hex | OKLCH | Role | Pro-code |
|-------|-----|-------|------|----------|
| 1 | `#E8A849` | `oklch(0.775 0.133 74.1)` | Series 1 | `series[0]` |
| 2 | `#6B5B7B` | `oklch(0.499 0.053 307.3)` | Series 2 | `series[1]` |
| 3 | `#D49838` | `oklch(0.721 0.130 75.2)` | Series 3 | `series[2]` |
| 4 | `#8A7A9A` | `oklch(0.605 0.051 307.5)` | Series 4 | `series[3]` |
| 5 | `#C08A30` | `oklch(0.671 0.122 76.1)` | Series 5 | `series[4]` |
| 6 | `#9E8E5A` | `oklch(0.649 0.073 92.9)` | Series 6 | `series[5]` |

Complementary pairs for portrait-style dashboards.

---

## 7. Agent Prompt Guide

### 7.1 Do's

- Keep purple in **nav + data**, not page fills.
- Use **`c2`** for nav typography in JSON.
- Gold owns **primary** emphasis.

### 7.2 Don'ts

- Dark **`c58`** text on purple nav without checking contrast.
- Pure **black** body copy.

### 7.3 Slot Mapping Cheat Sheet

```
Canvas → c56 cream
Cards → c2 white
Nav → c4 + white links (`c2`)
Accent → c29/c30
```

### 7.4 Pro-Code COLORS Object

```javascript
const COLORS = {"primary":"#E8A849","secondary":"#6B5B7B","surface":"#FFFFFF","bg":"#FFF9F0","text":"#2A2420","textMuted":"#7A6E60","series":["#E8A849","#6B5B7B","#D49838","#8A7A9A","#C08A30","#9E8E5A"]};
```

### 7.5 Example Agent Prompts

- **Editorial hero**: Cream bleed, white card, gold rule.
- **Nav contrast**: Verify `c2` links on `c4` in Theme Editor.

### 7.6 Theme QA

- Tab active: gold fill + dark `c58` text.
- Nav preview mandatory.



### 7.7 Agent workflow: rebuild order

1. Import the **Theme JSON** (§8) before placing cards so slot references resolve in previews.
2. Configure **navigation** and **tabs** first—if contrast fails here, fix `c4`/`c58`/`c59`/`c2` before building charts.
3. Drop **KPI** and **table** cards next; they stress `f7`/`f8` and zebra rows (`c11`/`c12`).
4. Add **charts** last; map series to §6 in order so saved color assignments stay stable across exports.

### 7.8 Pro-code CSS variable mirror

Mirror semantic names in `:root` for custom apps (`--surface` → `c2`, `--text-primary` → `c58`). Never fork hex between theme JSON and CSS without updating both. For App Studio embeds, set the app root to `background: transparent` when the host card supplies `c2`.

### 7.9 Data density guardrails

- Prefer **small multiples** over one overcrowded chart when series count exceeds five.
- If more than six filters apply, show a compact summary row in `f4`/`c59`.
- Use **`tabular-nums`** on every dynamic number, including tooltips.

### 7.10 Accessibility checks

- **`:focus-visible`** rings: derive from `c29`, or `c58` on filled accent buttons, ≥2px.
- Never encode **status by hue alone**—pair with text (“At risk”, “Behind”).
- Honor **`prefers-reduced-motion`**: disable staggered entrances and parallax in embeds.

### 7.11 Print and export

- **Dark** themes: enable background graphics when printing/PDF-exporting, or cards may look detached.
- **Light** themes without card borders: confirm KPI legibility when flattened to grayscale.

### 7.12 Versioning

- Track changes in git with DESIGN.md; Domo JSON has no semver field.
- White-label clones: adjust **`c29`/`c30` first**, then re-check `c58`/`c59` on `c2` and `c4`.

### 7.13 Chart grid and axes

- Default **gridlines** to `c47` at 0.45 opacity on dark cards and 0.55 on light cards unless engineering asks for sharper baselines.
- **Axis baselines** use 1px `c46`; optional **zero line** at 1.5px `c58` for signed metrics.
- **Tick labels** use `f5` at `c59`; never use `c58` for dense tick strips on dark fills without contrast check.
- **Tooltip** surfaces match `c2` with `c58` primary and `c59` secondary metadata.

### 7.14 Tables and dense data

- **Header row** maps to `c10` with `c59` labels unless the header sits on a dark chrome strip—then invert using `c58`.
- **Zebra** `c11` vs base `c2` should stay within one luminance step on light themes and two steps on dark themes.
- **Row hover** `c12` must not equal the selection color; add a 1px `c46` left indicator for the active row if needed.

### 7.15 Buttons and forms

- **Default buttons** use `c2` fill, `c46` stroke, `c59` label on light themes; on dark themes, mirror with `c2`/`c46`/`c59` against `c2` surfaces.
- **Primary** actions may use `c29` fill with **dark text** (`c40` on Terminal Sage tabs, `c58` on Golden Hour gold fill, `c2` on Blueprint).
- **Focus** rings: `c29` for neutral fields; `c58` when the control is already on an accent fill.

### 7.16 Navigation patterns

- **Dark nav bars** (`c4`): use **`c2` white** in JSON for link text when `c58` would be too dim or wrong hue (Golden Hour, Blueprint, Data Ink).
- **Dark themes** with muted links: `c59` inactive and `c58` active (Ocean Kelp, Terminal Sage) when contrast holds.
- **Active indicator** color is almost always `c29`; never point it at `c60`.

### 7.17 KPI cards

- **Value** uses `f7` + `tabular-nums`; color may inherit `c58` or a **status** color—never a non-semantic rainbow.
- **Label** uses `f8` + `c59` (or Light weight rules in §3.3).
- Optional **4px left border** in status hue is preferred over filling the entire KPI card.

### 7.18 Tabs and segmented control

- **Inactive** tab: `c8` background, `c59` text, `c46` border (when borders are enabled).
- **Active** tab: `c29` fill; pair **font** with `tab activeFontColor` from JSON (`c58`, `c2`, or `c40` per theme).
- Avoid more than **two** tab rows; use nested pages instead.

### 7.19 Theming pro-code chart libraries

- **Recharts / ECharts / Vega**: map `COLORS.series` in order; do not shuffle without updating saved screenshots in docs.
- **Grid**: pass `stroke={c47}` with opacity prop, not hard-coded `#ccc`.
- **Legend**: `f5` size, `c59` fill.

### 7.20 Escalation: when slots are insufficient

- Add **pro-code CSS variables** for one-off marketing campaigns; do **not** repurpose `c49`–`c54` for brand colors without updating this DESIGN.md and the JSON together.
- If a customer demands a **second accent**, document it as `--accent-warm` in pro-code only; keep App Studio JSON on the canonical `c29`/`c30` pair.

### 7.21 Cross-filtering and linked interactions

- When a chart selection drives another dataset, show **pending** state with `c3` wash and `c29` 1px outline—never disable the whole page gray overlay unless it is a modal.

### 7.22 Time series conventions

- **Trailing window** charts default to **solid** stroke; **forecast** segments use dashed `c29` at 70% opacity with historical in `series[0]`.
- **Today** reference lines use `c46` 1px dashed unless status red is required for deadline context.

### 7.23 Geo and maps

- **Choropleth** scales should reuse **§6** series colors before introducing a diverging ramp; if diverging is required, anchor ends to `c58` and `c29`, not new hues.

### 7.24 Alerts and subscriptions UI

- **Bell** icons and subscription toggles use `c59` idle and `c29` active; badge counts use `f6` on `c2` or `c29` pill depending on background.

### 7.25 Sandbox and QA datasets

- When demo data uses neon placeholders, **swap** those card-level palettes back to §6 before executive review—neon is for dev-only fixtures.

### 7.26 Handoff package contents

- Check in: this DESIGN.md, exported JSON (§8), and a **screenshot** of Theme Editor preview (nav + tab + card + chart).

### 7.27 Font slot quick matrix

| Slot | Size | Weight | Role |
|------|------|--------|------|
| `f1` | 22px | SemiBold | Page title |
| `f2` | 16px | SemiBold | Card title |
| `f3` | 13px | Regular | Body |
| `f4` | 11px | Regular | Labels |
| `f5` | 11px | Regular | Chart axes |
| `f6` | 11px | SemiBold | Badges |
| `f7` | 28px | SemiBold | KPI value |
| `f8` | 11px | Light | KPI label |

### 7.28 Structural color indices

| Slots | Role |
|-------|------|
| `c1`, `c56` | Page background |
| `c2`–`c3` | Card + hover |
| `c4`–`c5` | Nav + nav active |
| `c6`–`c7` | Header + input |
| `c8`–`c12` | Tabs + tables |
| `c29`–`c30` | Accent + pressed |
| `c40`–`c54` | Grayscale ramp + borders at `c46`–`c48` |
| `c58`–`c59` | Text (FONT) |

### 7.29 Pre-ship checklist

- [ ] Theme JSON imports without validation errors.
- [ ] Nav + tab previews pass contrast on real `c4` / `c29`.
- [ ] Card `ca1` uses documented radius/shadow/border.
- [ ] `COLORS.series` matches §6 order.
- [ ] No `c60` on nav font colors.

### 7.30 Common agent mistakes

- Mixing **light-theme** `c58` on **dark** `c4` without retesting.
- Using **accent** as full-page background.
- Enabling **shadows** on Terminal Sage or **Data Ink** flat themes.
- **Skipping** `tabular-nums` on KPI components.

### 7.31 Glossary

- **Chrome**: nav, tabs, headers—not chart ink.
- **Series**: encoded chart colors from §6.
- **Slot**: App Studio color index (`c1`…`c59`).
- **FONT tag**: Domo marks `c58`/`c59` for typography defaults.

### 7.32 Storytelling with annotations

- Use **1px** `c29` callout lines from chart to label; labels sit in `f4` with `c59` unless emphasis requires `c58`.
- Limit **on-chart text** to three annotations per view; push detail to tooltips.

### 7.33 Tooltip content order

1. **Measure name** (`f6`, `c58`)
2. **Value** (`f3`, `c58`, `tabular-nums`)
3. **Dimension context** (`f4`, `c59`)
4. **Delta** optional (`f4`, status color)

### 7.34 Mobile and narrow layouts

- Collapse nav to **icon rail** using same `c4`; do not lighten `c4` solely for mobile—adjust padding instead.
- KPI tiles **stack** single-column; maintain `f7`/`f8` pairing.

### 7.35 Embedded iframe apps

- Match **parent** theme tokens via query or postMessage contract; never hard-code a second palette inside the iframe.

### 7.36 Final sign-off prompts

- *“Generate a KPI strip”* → reference §4, §3.2 `f7`/`f8`, and `c2`/`c56` layering.
- *“Recolor this chart”* → edit §6 order and `COLORS.series` together.
- *“Darken the nav”* → adjust `c4`/`c5` only after checking link tokens (`c2` vs `c58`/`c59`).
- *“Match brand PDF”* → export Theme JSON + §2.1 hex/OKLCH table as the single source of truth for designers.
- *“Audit accessibility”* → run §7.10 checks on nav, tabs, KPIs, and chart tooltips in one pass.
- *“Snapshot for compliance”* → attach §8 JSON + Theme Editor PNG to the change ticket.

### 7.37 Cross-theme diff discipline

- Keep **§2.1 row order** identical across sibling themes when possible so designers can diff hex changes line-by-line in version control.

### 7.38 Support bundle

- File bugs with **§8 JSON**, a **Theme Editor screenshot**, and the **first card ID** that shows the defect—this triages import vs runtime issues quickly.

### 7.39 Regression triggers

- Any change to **`c4`** or **`c29`** requires full nav + tab + active-state screenshot refresh in the PR.
- Any change to **`f7`/`f8`** requires KPI screenshot comparison on both dense and sparse layouts.

### 7.40 Copy deck alignment

- Marketing copy pasted into cards should still obey **`f3`** line length guidance (~72 characters) even when Domo allows wider text boxes.



---

## 8. App Studio Theme JSON (Importable)

```json
{"name":"Golden Hour","colors":[{"index":1,"value":"#FFF9F0","tag":"PRIMARY"},{"index":2,"value":"#FFFFFF","tag":"PRIMARY"},{"index":3,"value":"#F8F0E4","tag":"PRIMARY"},{"index":4,"value":"#3A2E4A","tag":"PRIMARY"},{"index":5,"value":"#4E4060","tag":"PRIMARY"},{"index":6,"value":"#FFF9F0","tag":"PRIMARY"},{"index":7,"value":"#FFFFFF","tag":"PRIMARY"},{"index":8,"value":"#FFFFFF","tag":"PRIMARY"},{"index":9,"value":"#E8A849","tag":"PRIMARY"},{"index":10,"value":"#F8F0E4","tag":"PRIMARY"},{"index":11,"value":"#FFF9F0","tag":"PRIMARY"},{"index":12,"value":"#F8F0E4","tag":"PRIMARY"},{"index":29,"value":"#E8A849","tag":"SECONDARY"},{"index":30,"value":"#D49838","tag":"SECONDARY"},{"index":40,"value":"#120F0C","tag":"GRAYSCALE"},{"index":41,"value":"#181410","tag":"GRAYSCALE"},{"index":42,"value":"#1E1A16","tag":"GRAYSCALE"},{"index":43,"value":"#26211C","tag":"GRAYSCALE"},{"index":44,"value":"#302A24","tag":"GRAYSCALE"},{"index":45,"value":"#3C352E","tag":"GRAYSCALE"},{"index":46,"value":"#D4C8B8","tag":"CUSTOM"},{"index":47,"value":"#E4DAD0","tag":"CUSTOM"},{"index":48,"value":"#D4C8B8","tag":"CUSTOM"},{"index":49,"value":"#6A6058","tag":"GRAYSCALE"},{"index":50,"value":"#7A7068","tag":"GRAYSCALE"},{"index":51,"value":"#8C8278","tag":"GRAYSCALE"},{"index":52,"value":"#9E948A","tag":"GRAYSCALE"},{"index":53,"value":"#B5ABA0","tag":"GRAYSCALE"},{"index":54,"value":"#CEC4B8","tag":"GRAYSCALE"},{"index":56,"value":"#FFF9F0","tag":"PRIMARY"},{"index":58,"value":"#2A2420","tag":"FONT"},{"index":59,"value":"#7A6E60","tag":"FONT"}],"fonts":[{"index":1,"family":"Serif","weight":"SemiBold","size":"22px","style":"normal"},{"index":2,"family":"Serif","weight":"SemiBold","size":"16px","style":"normal"},{"index":3,"family":"Serif","weight":"Regular","size":"13px","style":"normal"},{"index":4,"family":"Serif","weight":"Regular","size":"11px","style":"normal"},{"index":5,"family":"Serif","weight":"Regular","size":"11px","style":"normal"},{"index":6,"family":"Serif","weight":"SemiBold","size":"11px","style":"normal"},{"index":7,"family":"Serif","weight":"SemiBold","size":"28px","style":"normal"},{"index":8,"family":"Serif","weight":"Light","size":"11px","style":"normal"}],"cards":[{"index":1,"fontColor":{"type":"COLOR_REFERENCE","index":58},"titleFont":{"type":"FONT_REFERENCE","index":2},"chartFont":{"type":"FONT_REFERENCE","index":5},"backgroundColor":{"type":"COLOR_REFERENCE","index":2},"borderRadius":10,"borderWidth":0,"dropShadow":true,"dropShadowColor":{"type":"COLOR_REFERENCE","index":40},"padding":20,"elementSpacing":12,"accentColor":{"type":"COLOR_REFERENCE","index":29}}],"buttons":[{"index":1,"fontColor":{"type":"COLOR_REFERENCE","index":59},"backgroundColor":{"type":"COLOR_REFERENCE","index":2},"borderColor":{"type":"COLOR_REFERENCE","index":46},"borderRadius":10,"font":{"type":"FONT_REFERENCE","index":3}}],"navigation":[{"index":1,"backgroundColor":{"type":"COLOR_REFERENCE","index":4},"titleFontColor":{"type":"COLOR_REFERENCE","index":2},"linkFontColor":{"type":"COLOR_REFERENCE","index":2},"activeLinkFontColor":{"type":"COLOR_REFERENCE","index":29},"activeColor":{"type":"COLOR_REFERENCE","index":29},"titleFont":{"type":"FONT_REFERENCE","index":1},"linkFont":{"type":"FONT_REFERENCE","index":3}}],"headers":[{"index":1,"backgroundColor":{"type":"COLOR_REFERENCE","index":1},"fontColor":{"type":"COLOR_REFERENCE","index":58},"font":{"type":"FONT_REFERENCE","index":2}}],"tables":[{"index":1,"headerBackgroundColor":{"type":"COLOR_REFERENCE","index":10},"headerFontColor":{"type":"COLOR_REFERENCE","index":59},"rowBackgroundColor":{"type":"COLOR_REFERENCE","index":2},"alternateRowBackgroundColor":{"type":"COLOR_REFERENCE","index":11},"rowHoverBackgroundColor":{"type":"COLOR_REFERENCE","index":12},"fontColor":{"type":"COLOR_REFERENCE","index":58},"borderColor":{"type":"COLOR_REFERENCE","index":47},"font":{"type":"FONT_REFERENCE","index":3}}],"tabs":[{"index":1,"backgroundColor":{"type":"COLOR_REFERENCE","index":8},"fontColor":{"type":"COLOR_REFERENCE","index":59},"activeBackgroundColor":{"type":"COLOR_REFERENCE","index":29},"activeFontColor":{"type":"COLOR_REFERENCE","index":58},"borderColor":{"type":"COLOR_REFERENCE","index":46},"font":{"type":"FONT_REFERENCE","index":3}}],"forms":[{"index":1,"backgroundColor":{"type":"COLOR_REFERENCE","index":7},"fontColor":{"type":"COLOR_REFERENCE","index":58},"borderColor":{"type":"COLOR_REFERENCE","index":48},"focusBorderColor":{"type":"COLOR_REFERENCE","index":29},"borderRadius":10,"font":{"type":"FONT_REFERENCE","index":3}}]}
```

> **Import**: App Studio → Theme Editor → Import Theme JSON. Confirm navigation and tab active text contrast after import.

