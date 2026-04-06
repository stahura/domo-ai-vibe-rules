---
name: app-studio-pro-code
description: Build and embed pro-code JavaScript custom apps inside Domo App Studio pages. Bridges the custom app build pipeline (initial-build, domo-app-theme) with App Studio card placement (app-studio). Covers decision routing between native cards and pro-code apps, build orchestration with design skills, canvas integration, page-level filter propagation (domo.onFiltersUpdated), App Studio variable integration (domo.onVariablesUpdated, domo.requestVariablesUpdate), and the pending/commit pattern for variable state management. Use when a visualization or interaction exceeds native card capabilities, when the user mentions pro-code editor, or when embedding custom apps in App Studio.
---

# Pro-Code Custom Apps in App Studio

> **CUSTOM PALETTE REQUIRED**: Never use Domo's native/default color palette. Always use the project's curated palette selected from `domo-app-theme/color-palettes.md`. Use OKLCH values directly in pro-code CSS; convert to hex for native card overrides. All chart series, text, grid, and status colors must use the chosen palette.

App Studio's Pro Code Editor allows embedding full JavaScript custom apps as cards on the App Studio canvas. This skill bridges two existing workflows: building custom apps (`initial-build`) and placing cards on App Studio pages (`app-studio`).

## When to Use

Use this skill when a user's requirement exceeds what native Domo cards can deliver. If a native card can handle it, use `app-studio` alone.

## Decision Routing: Native Card vs Pro-Code

Evaluate each component in the user's requirements against this table. A single pro-code signal means that component should be a custom app.

| Requirement | Native Card | Pro-Code |
|-------------|:-----------:|:--------:|
| Standard chart (bar, line, pie, donut, funnel) | X | |
| KPI / single value with comparison | X | |
| Simple data table with sorting | X | |
| Dropdown / date picker filters | X | |
| Custom visualization (Gantt, heatmap, org chart, calendar, network graph) | | X |
| Multi-step forms or wizard flows | | X |
| Real-time animation or transitions | | X |
| Complex conditional formatting beyond card rules | | X |
| Cross-card interactivity (selection in one drives another) | | X |
| AppDB document CRUD with custom UI | | X |
| AI-powered features (chat, generation, text-to-SQL) | | X |
| Custom styling beyond the ca1–ca8 style presets | | X |
| Embedded third-party library (D3, Mapbox, AG Grid) | | X |

| Header/banner image with gradient, text, branding | | X |
| Multi-series time chart with Plan/Actual/Forecast + confidence band | | X |

A single App Studio page can mix native cards and pro-code cards. Decide per-component, not per-page.

**Creating card instances**: `domo publish` creates a *design* in the Asset Library. Card instances are created programmatically via a two-step API — see the "Creating Custom App Card Instances" section in `app-studio` for the full flow (`POST /domoapps/apps/v2/contexts` → `POST /domoapps/apps/v2`). Each card instance gets its own context with independent dataset mappings.

## Build Workflow

### Step 1 — Plan the page

Produce a placement plan that lists every component on the target page:

```
Page: "Vendor Performance"
  1. Region filter         → native dropdown card
  2. Date range filter     → native date picker card
  3. Revenue KPI           → native KPI card
  4. Cost KPI              → native KPI card
  5. Margin KPI            → native KPI card
  6. Revenue trend chart   → native line chart card
  7. Gantt timeline        → PRO-CODE (custom Gantt, no native equivalent)
  8. Vendor scorecard      → PRO-CODE (interactive table with inline editing via AppDB)
```

### Step 2 — Build native cards

Use `app-studio` to create and place native cards (items 1–6 above). Follow the design-aware layout rules in `app-studio` for spacing, row harmony, and density.

### Step 3 — Build pro-code apps

For each pro-code component, run through the `initial-build` playbook with the following skill stack pre-loaded:

**Always load:**
- Custom palette from `domo-app-theme/color-palettes.md` — select a curated OKLCH palette suited to the use case
- `make-interfaces-feel-better` design principles — see [design-skills.md](design-skills.md)

**Load when applicable:**
- `writing-better` — when the app has significant user-facing text (labels, tooltips, error messages, empty states, help text).

The `initial-build` phases apply in full: manifest, app shell, data access, storage, toolkit, feature skills, performance review, build, publish.

### Step 4 — Create card instances and place on the App Studio page

After `domo publish` succeeds, create card instances from the design using the two-step API.

**CRITICAL**: The context/card creation endpoints use the **root domain** (`https://{instance}.domo.com/domoapps/...`), NOT the `/api/` prefix. Using `/api/domoapps/...` returns `404 "No static resource"`.

```python
DOMO = f"https://{instance}.domo.com"  # NOT {BASE} which has /api/

# Step 4a: Create a context for the custom app
ctx_body = {
    "designId": design_id,  # from manifest.json id field
    "mapping": [
        {"alias": alias, "dataSetId": ds_guid, "fields": [], "dql": None}
    ],
    "collections": [],
    "accountMapping": [], "actionMapping": [],
    "workflowMapping": [], "packageMapping": [],
    "isDisabled": False
}
resp = requests.post(f"{DOMO}/domoapps/apps/v2/contexts", headers=HEADERS, json=ctx_body)
context_id = resp.json()[0]["id"]

# Step 4b: Create the card on the target page
import urllib.parse
title = urllib.parse.quote("My Custom Chart")
resp = requests.post(
    f"{DOMO}/domoapps/apps/v2?fullpage=false&pageId={page_id}&cardTitle={title}",
    headers=HEADERS, json={"contextId": context_id, "id": context_id})

# Step 4c: Find the numeric card ID on the page
cards = requests.get(f"{BASE}/content/v1/pages/{page_id}/cards", headers=HEADERS).json()
card_id = next(c["id"] for c in cards if c["title"] == "My Custom Chart")
```

For apps with no datasets (banners), use `"mapping": []`. Create separate card instances per page for page-specific banners.

The card is automatically added to the page. Move it from the appendix to the canvas by updating the layout template (same process as native cards — see `app-studio`).

### Step 5 — Configure layout for pro-code cards

Pro-code cards typically need more canvas space than native cards. Recommended sizes:

| Pro-code app type | Width | Height | Notes |
|-------------------|-------|--------|-------|
| Full-width interactive (Gantt, timeline, map) | 60 | 30–40 | Takes full row |
| Half-width visualization (custom chart, scorecard) | 30 | 22–30 | Pairs with another card |
| Compact widget (status indicator, mini-form) | 20 | 15–20 | Three across |
| Tall interactive (chat, multi-step form) | 20–30 | 35–45 | Needs vertical space |

Set content entry properties for pro-code cards:

```json
{
  "hideTitle": true,
  "hideDescription": true,
  "hideFooter": true,
  "hideBorder": false,
  "hideMargins": false,
  "fitToFrame": true,
  "acceptFilters": true,
  "acceptDateFilter": true,
  "acceptSegments": true
}
```

`hideTitle: true` and `hideFooter: true` are typical for pro-code cards because the custom app renders its own header and footer. `fitToFrame: true` scales the app to fill its grid cell.

## App Studio Integration: Filters & Variables

Pro-code cards embedded in App Studio receive two types of external input: **page-level filters** (from native filter cards) and **variables** (from App Studio variable controls). Both require explicit listeners registered at the top level. For detailed patterns and production examples, see [app-studio-integration.md](app-studio-integration.md).

### Page-Level Filters

Register `domo.onFiltersUpdated` (past tense) at the top level — outside any component lifecycle or `useEffect`. It fires whenever a user changes a native filter card on the same App Studio page.

```javascript
domo.onFiltersUpdated((filters) => {
  if (!Array.isArray(filters) || filters.length === 0) return;

  filters.forEach((filter) => {
    const { column, operand, values, dataType } = filter;
    // Map column to internal state, then refetch data
  });

  fetchData();
});
```

**Filter object shape** — each element in the array:

| Field | Type | Description |
|-------|------|-------------|
| `column` | string | Dataset column name (e.g., `"YEAR_OF_EVENT"`) |
| `operand` | string | **Not `operator`**. One of: `BETWEEN`, `IN`, `GREATER_THAN_EQUAL`, `LESS_THAN_EQUAL`, `EQUALS` |
| `values` | array | Filter values. For `BETWEEN`: 2 elements `[min, max]`. For `IN`: array of selected values. For scalar operands: 1 element. |
| `dataType` | string | Column data type (e.g., `"LONG"`, `"STRING"`, `"DATE"`) |

**Operand handling patterns:**

| Operand | Values | How to map |
|---------|--------|------------|
| `BETWEEN` | `[min, max]` | Range filter: `{ min: Number(values[0]), max: Number(values[1]) }` |
| `IN` | `["val1", "val2"]` | Categorical: store as array. Empty array = "ALL" (no filter). |
| `GREATER_THAN_EQUAL` | `[threshold]` | Update `.min` of a range |
| `LESS_THAN_EQUAL` | `[threshold]` | Update `.max` of a range |

**Column name resilience**: Domo column names may arrive in different formats (e.g., `YEAR_OF_EVENT`, `YEAROFEVENT`, `Year of Event`). Normalize with `column?.toUpperCase()` and handle common variants in a switch/case.

For this to work:
- The content entry must have `acceptFilters: true`
- The custom app must use the same dataset that the filters target
- The dataset must be mapped in both the App Studio page's card configuration and the custom app's `manifest.json`
- After processing filters, trigger a data refetch immediately — page filters apply on change, not on an explicit "apply" action

### App Studio Variables

#### Creating Variables via API

Before a pro-code app can consume variables, the variables must exist. Create them via the function template API with `variable: true`:

```python
resp = requests.post(
    f"{BASE}/query/v1/functions/template?strict=false",
    headers={"X-Domo-Authentication": SID, "Content-Type": "application/json"},
    json={
        "name": "Selected Metric",
        "locked": False,
        "global": True,
        "expression": "'Revenue'",     # Default value as SQL literal
        "links": [],
        "aggregated": False,
        "analytic": False,
        "nonAggregatedColumns": [],
        "dataType": "STRING",           # STRING, DECIMAL, LONG, DATE
        "cacheWindow": "non_dynamic",
        "columnPositions": [],
        "functions": [],
        "functionTemplateDependencies": [],
        "archived": False,
        "hidden": False,
        "variable": True,               # CRITICAL — makes this a Variable
    },
    timeout=15,
)
data = resp.json()
function_id = data["id"]     # e.g., 115511 — use this numeric ID in pro-code
```

The returned `id` is the numeric `functionId` that the pro-code app uses in `domo.onVariablesUpdated` and `domo.requestVariablesUpdate`. Store these IDs — they are the bridge between the API-created variable and the pro-code app.

**Variable Controls must be added manually in the App Studio editor** — there is no API for this. After creating variables, tell the user to bind them in the editor: open the app → Controls icon in left toolbar → drag a control onto the canvas → select the variable to bind. See `app-studio` skill for complete UI instructions.

#### Consuming Variables in Pro-Code

Register `domo.onVariablesUpdated` (past tense) at the top level. It fires whenever any App Studio variable control changes value. Variables are identified by **numeric string IDs** (e.g., `"858"`, `"860"`).

```javascript
domo.onVariablesUpdated((variables) => {
  if (!variables || typeof variables !== "object") return;

  const typeVar = variables["860"];
  if (typeVar?.parsedExpression?.value) {
    const label = typeVar.parsedExpression.value;
    const mapped = LABEL_TO_VALUE_MAP[label];
    if (mapped) state.pendingValues.someField = { label, value: mapped };
  }

  updateUI();
});
```

**Variable object shape** — `variables` is a keyed object where each key is a variable's numeric function ID:

```javascript
{
  "858": { "parsedExpression": { "exprType": "LITERAL", "value": "Year Sold" } },
  "860": { "parsedExpression": { "exprType": "LITERAL", "value": "Cumulative" } }
}
```

**Pending/commit pattern**: Variables fire on every keystroke or selection. Use a two-phase approach:

1. `onVariablesUpdated` stores values in `pendingValues` (staging area)
2. User clicks an Apply button to commit pending values to active state
3. Apply triggers the data refetch

This prevents rapid-fire refetches while the user is adjusting multiple variable controls.

**Label-to-value mapping**: Variable values arrive as display labels (e.g., `"Days"`, `"Cumulative"`). The custom app must map these to internal enum values using a lookup table:

```javascript
const RETENTION_TYPE_MAP = {
  "Cumulative": "CUMULATIVE",
  "Marginal": "ADJUSTED_MARGINAL_RETENTION",
  "Lifetime": "LIFETIME",
};
```

### Writing Variables Back

A pro-code app can update App Studio variables using `domo.requestVariablesUpdate`. This enables two-way communication — e.g., when selecting an event type, automatically update a dependent event subtype variable.

```javascript
domo.requestVariablesUpdate(
  [{ functionId: 873, value: "Initial Service" }],
  (ackResponse) => { /* acknowledged */ },
  (replyResponse) => { /* completed */ }
);
```

**Loop prevention**: Updating a variable triggers `onVariablesUpdated` again. Guard with a flag:

```javascript
state.isUpdatingVariable = true;
domo.requestVariablesUpdate(updates, onAck, (reply) => {
  state.isUpdatingVariable = false;
});

// In the onVariablesUpdated handler:
if (state.isUpdatingVariable) return;
```

### Integration Summary

| Mechanism | API | Fires when | Refetch strategy |
|-----------|-----|------------|------------------|
| Page filters | `domo.onFiltersUpdated` | Native filter card changes | Immediate — refetch on every filter change |
| Variables | `domo.onVariablesUpdated` | Variable control changes | Staged — pending values committed on Apply |
| Variable write-back | `domo.requestVariablesUpdate` | App needs to update a variable | Guard with `isUpdatingVariable` flag |

## Theme Alignment

A pro-code card renders in an iframe with its own CSS — it does not inherit the App Studio app's theme. To maintain visual consistency:

1. **NEVER use Domo's native color palette.** Always use the curated palette selected from `domo-app-theme/color-palettes.md`. Use OKLCH values directly in CSS custom properties, or convert to hex for inline JS color references. All chart series, text, grid lines, and status colors must match the App Studio theme's custom palette. Example palette mapping for pro-code:
   - Series 1 (primary): brand-500 from the custom palette
   - Series 2: secondary ORDER_SOURCE (c22) from the custom palette
   - Series 3: tertiary ORDER_SOURCE (c29) from the custom palette
   - Series 4: quaternary ORDER_SOURCE (c36) from the custom palette
   - Grid lines: neutral-200
   - Text primary: neutral-950
   - Text secondary: neutral-500
   - Success: success-600 | Error: error-600
2. Match the page background: Set the custom app's body background to `transparent` so it blends with the surrounding canvas.
3. Match card styling: Pro-code containers should have `background: transparent`, no `box-shadow`, no `border-radius`. The App Studio card frame provides all chrome.
4. **No drop shadow on pro-code containers.** The card style (ca1 with 1px border, no shadow) handles card edges. Adding a shadow inside the iframe creates a double-border effect.

### Color Palette Workflow for Pro-Code Apps

When building pro-code apps, you MUST use the same curated palette that was applied to the App Studio theme. The palette source is the project's `DESIGN.md` (from `domo-app-theme/themes/`). Pro-code apps should use the OKLCH values via CSS custom properties, or convert to hex for inline JS references. Define a `COLORS` object at the top of each pro-code `app.js` with the project palette values.

**CRITICAL — Theme Color Inheritance**: Pro-code components render in iframes and do NOT inherit the App Studio theme colors. Every color used in pro-code CSS and JS must be **explicitly derived from the same DESIGN.md** that was used for the App Studio theme. This includes:
- Banner gradient backgrounds, accent overlays, brand text color, top border
- Chart primary color (P), grid lines, axis text, tooltip backgrounds
- Multi-series chart line/bar colors (C1, C2, C3...)
- All text colors (titles, subtitles, labels, legends)

If the theme palette changes (e.g., from green to copper), **every pro-code component must be updated and republished** with the new colors. There is no automatic inheritance. Forgetting this creates jarring mismatches between native Domo cards (which follow the theme) and pro-code cards (which use hardcoded values).

## Time Axis Tick Density

When building time-series charts with daily data spanning months/years, raw daily ticks overlap and become unreadable. Use an "every N days" interval strategy:

```javascript
const calcTickInterval = (dataLength) => {
  if (dataLength <= 30) return 0;          // show every tick
  if (dataLength <= 90) return 6;          // ~weekly
  if (dataLength <= 180) return 13;        // ~biweekly
  return Math.ceil(dataLength / 18) - 1;   // ~18 visible ticks
};

// In XAxis:
// interval={aggregation === 'day' ? calcTickInterval(data.length) : 'preserveStartEnd'}
```

Target approximately 15–20 visible tick labels on any viewport width. For angled labels (when data is dense), use `angle: -35` and `textAnchor: 'end'`.

## Pro-Code Card Shadow & Border Handling

Pro-code cards embedded in App Studio should NOT render their own `box-shadow` or `border-radius` on the outermost container. The App Studio card frame (via `style.sourceId` in the content entry) handles the card chrome. Set the custom app's container to `background: transparent; border-radius: 0; padding: 20px 24px 16px;` and let the card style provide the chrome.

**Zero border-radius is mandatory** — all card styles use `borderRadius: 0`, so the pro-code container MUST also use `border-radius: 0`. No rounded corners anywhere.

## Responsive Behavior

App Studio renders pro-code cards at two breakpoints via the `standard` and `compact` templates. The custom app's own responsive CSS operates independently inside its iframe.

For the compact (mobile) template:
- Set pro-code cards to width 12 (full mobile width)
- Height should be taller than the desktop version (content stacks vertically)
- The custom app's internal responsive breakpoints should handle the narrower viewport

## Design Skills Integration

For detailed guidance on applying design polish to pro-code apps, see [design-skills.md](design-skills.md).

## Complete Workflow Example

Building an App Studio page with 4 native KPI cards and 1 pro-code Gantt chart:

```python
import requests

BASE = "https://instance.domo.com/api"
HEADERS = {"X-DOMO-Developer-Token": TOKEN, "Content-Type": "application/json"}

# 1. Create the App Studio app
app = requests.post(f"{BASE}/content/v1/dataapps",
    headers=HEADERS, json={"title": "Project Tracker"}).json()
page_id = app["landingViewId"]

# 2. Create 4 native KPI cards on the page
kpi_ids = []
for card_def in kpi_definitions:
    resp = requests.put(f"{BASE}/content/v3/cards/kpi?pageId={page_id}",
        headers=HEADERS, json=card_def)
    kpi_ids.append(resp.json()["id"])

# 3. Build and publish the Gantt custom app (via initial-build skill)
# ... scaffold, code, npm run build, cd dist, domo publish ...
gantt_design_id = "abc12345-..."  # from manifest.json id field

# 4. Create a card instance from the published design
# NOTE: Use root domain (DOMO), NOT {BASE} which has /api/ prefix
DOMO = f"https://{instance}.domo.com"
import urllib.parse
ctx = requests.post(f"{DOMO}/domoapps/apps/v2/contexts", headers=HEADERS, json={
    "designId": gantt_design_id,
    "mapping": [{"alias": "tasks", "dataSetId": dataset_id, "fields": [], "dql": None}],
    "collections": [], "accountMapping": [], "actionMapping": [],
    "workflowMapping": [], "packageMapping": [], "isDisabled": False
}).json()[0]
context_id = ctx["id"]
requests.post(
    f"{DOMO}/domoapps/apps/v2?fullpage=false&pageId={page_id}&cardTitle={urllib.parse.quote('Project Gantt')}",
    headers=HEADERS, json={"contextId": context_id, "id": context_id})
gantt_card_id = next(c["id"] for c in requests.get(
    f"{BASE}/content/v1/pages/{page_id}/cards", headers=HEADERS).json()
    if "Gantt" in c.get("title", ""))

# 5. Get and update the layout
layout = requests.get(f"{BASE}/content/v4/pages/{page_id}/layouts",
    headers=HEADERS).json()
layout_id = layout["layoutId"]

# Acquire write lock
requests.put(f"{BASE}/content/v4/pages/layouts/{layout_id}/writelock",
    headers=HEADERS, json={})

# Build template: KPIs on row 1, Gantt below
# (Read actual contentKeys from layout["content"] first)
std_template = [
    {"type": "SPACER", "contentKey": 0, "x": 0, "y": 0,
     "width": 60, "height": 3, "virtualAppendix": False,
     "virtual": False, "children": None},
    # ... KPI cards at y=3, width 15 each, height 10 ...
    # ... SPACER at y=13, height 3 ...
    # ... Gantt card at y=16, width 60, height 35 ...
]

# Set Gantt card content properties
for c in layout["content"]:
    if c.get("cardId") == gantt_card_id:
        c["hideTitle"] = True
        c["hideFooter"] = True
        c["fitToFrame"] = True

layout["standard"]["template"] = std_template
# ... build compact template similarly ...

requests.put(f"{BASE}/content/v4/pages/layouts/{layout_id}",
    headers=HEADERS, json=layout)
requests.delete(f"{BASE}/content/v4/pages/layouts/{layout_id}/writelock",
    headers=HEADERS)
```

## Verified Behavior

Based on production pro-code apps running in App Studio:

1. **Filter propagation works**: `domo.onFiltersUpdated` fires in pro-code cards when native filter cards on the same page change. The content entry needs `acceptFilters: true`. Filter objects use `operand` (not `operator`).
2. **Variable propagation works**: `domo.onVariablesUpdated` fires when App Studio variable controls change. Variables are identified by numeric function IDs. `domo.requestVariablesUpdate` allows writing variables back.
3. **Theme isolation confirmed**: Pro-code cards render in an isolated iframe. No CSS inherits from App Studio. The custom app must provide all its own styling.
4. **`domo.get` respects page filters implicitly**: When using `domo.get("/data/v1/alias")`, the platform automatically applies active page filters to the data request. However, this only works for Data API v1 queries — Code Engine calls, SQL queries, and other data access methods require explicit filter handling via `onFiltersUpdated`.

## Pro-Code Pattern: CSS Gradient Banner

A lightweight custom app that renders a branded page header. No JS framework or dataset needed.

**Files**: `index.html`, `app.css`, `manifest.json`

```html
<!-- index.html -->
<div class="banner">
  <div class="banner-geo"></div>
  <div class="banner-content">
    <span class="banner-brand">COMPANY NAME</span>
    <h1 class="banner-title" id="bannerTitle">PAGE TITLE</h1>
    <p class="banner-sub" id="bannerSub">Contextual subheader describing this page's focus</p>
  </div>
</div>
```

```css
/* app.css — dark gradient with subtle background pattern (see Banner Background Patterns section) */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
.banner {
  width: 100%; height: 100%;
  background:
    radial-gradient(circle, rgba(91, 153, 213, 0.07) 1px, transparent 1px),  /* dot grid pattern */
    linear-gradient(135deg, #23272E 0%, #3A4352 100%);
  background-size: 20px 20px, 100% 100%;
  display: flex; align-items: center;
}
.banner-content { padding: 0 40px; }
.banner-brand { font-size: 11px; font-weight: 600; letter-spacing: 0.14em; color: #5B99D5; display: block; margin-bottom: 6px; } /* brand-400 */
.banner-title { font-size: 26px; font-weight: 600; color: #FFFFFF; letter-spacing: 0.02em; margin-bottom: 4px; }
.banner-sub { font-size: 13px; font-weight: 400; color: #B1BAC8; max-width: 600px; line-height: 1.4; } /* neutral-300 */
```

```json
// manifest.json — no datasets
{"name": "Banner", "version": "1.0.0", "size": {"width": 10, "height": 1}, "mapping": []}
```

**Placement**: width 60, **height 14**, y=0. Content entry: `hideTitle`, `hideFooter`, `hideBorder`, `hideMargins`, `hideWrench` all `true`, `fitToFrame: true`, style `ca8`. The taller height (14 vs 7) accommodates the subheader text and creates a more intentional visual anchor.

**Per-page titles**: Create a **separate banner design per page** (e.g., `mfg-banner-overview/`, `mfg-banner-production/`), each with hardcoded title and subtitle in its `index.html`. Do NOT share a single design across pages — iframe cards cannot receive URL params from the App Studio host. Publish each design separately, then create one card instance per design on the correct page via the context API.

**Color palette alignment**: Use the curated palette from `domo-app-theme/color-palettes.md` in ALL pro-code components. NEVER use Domo native/default colors. Chart series colors should match the App Studio theme's ORDER_SOURCE values (c8, c22, c29, c36).

### Banner Background Patterns

Banners should include a **subtle background pattern** layered over the base gradient. This adds visual depth and a premium, editorial feel without distracting from the text content. Patterns are pure CSS (no external images), use the accent color at very low opacity, and are palette-aware.

**Always add a pattern.** Select one per app (all pages use the same pattern for consistency) based on the data domain. Apply the pattern by replacing the flat `linear-gradient` in `.banner` with a layered `background` property.

| Pattern | Best for | Visual character |
|---------|----------|-----------------|
| **Dot Grid** | Corporate, analytics, SaaS | Clean, data-forward, structured |
| **Diagonal Lines** | Manufacturing, engineering, energy | Motion, precision, industrial |
| **Radial Glow** | Executive, overview, hero pages | Spotlight, focus, premium |
| **Topographic** | Supply chain, logistics, geography | Technical, depth, complexity |
| **Crosshatch** | Financial, compliance, healthcare | Woven, texture, institutional |

#### Dot Grid

Small repeating dots in the accent color. Subtle, structured, works universally.

```css
.banner {
  background:
    radial-gradient(circle, var(--accent-dot) 1px, transparent 1px),
    linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%);
  background-size: 20px 20px, 100% 100%;
}
```

Light mode example: `--accent-dot: rgba(58, 105, 131, 0.07)`
Dark mode example: `--accent-dot: rgba(232, 122, 32, 0.08)`

#### Diagonal Lines

Thin angled lines suggesting motion and precision.

```css
.banner {
  background:
    repeating-linear-gradient(
      -45deg,
      transparent,
      transparent 40px,
      var(--line-color) 40px,
      var(--line-color) 41px
    ),
    linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%);
}
```

Light mode: `--line-color: rgba(58, 105, 131, 0.04)`
Dark mode: `--line-color: rgba(232, 122, 32, 0.05)`

#### Radial Glow

A soft spotlight behind the text area. Creates a focal point and premium depth.

```css
.banner {
  background:
    radial-gradient(ellipse at 30% 50%, var(--glow-color) 0%, transparent 60%),
    linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%);
}
```

Light mode: `--glow-color: rgba(58, 105, 131, 0.08)`
Dark mode: `--glow-color: rgba(232, 122, 32, 0.12)`

#### Topographic

Concentric rings evoking contour maps. Technical and layered.

```css
.banner {
  background:
    radial-gradient(ellipse at 75% 40%, transparent 30%, var(--topo-line) 30.5%, transparent 31%),
    radial-gradient(ellipse at 75% 40%, transparent 45%, var(--topo-line) 45.5%, transparent 46%),
    radial-gradient(ellipse at 75% 40%, transparent 60%, var(--topo-line) 60.5%, transparent 61%),
    radial-gradient(ellipse at 75% 40%, transparent 75%, var(--topo-line) 75.5%, transparent 76%),
    linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%);
}
```

Light mode: `--topo-line: rgba(58, 105, 131, 0.05)`
Dark mode: `--topo-line: rgba(232, 122, 32, 0.06)`

#### Crosshatch

A fine woven grid pattern. Institutional and textured.

```css
.banner {
  background:
    linear-gradient(0deg, var(--hatch-color) 1px, transparent 1px),
    linear-gradient(90deg, var(--hatch-color) 1px, transparent 1px),
    linear-gradient(135deg, var(--bg-start) 0%, var(--bg-end) 100%);
  background-size: 24px 24px, 24px 24px, 100% 100%;
}
```

Light mode: `--hatch-color: rgba(58, 105, 131, 0.03)`
Dark mode: `--hatch-color: rgba(232, 122, 32, 0.04)`

#### Implementation notes

- **Opacity range**: Keep pattern elements between 0.03–0.12 opacity. Anything higher competes with text.
- **CSS custom properties**: The examples use `var(--...)` placeholders. In the actual banner `app.css`, replace with literal color values from the project's palette (e.g., `rgba(232, 122, 32, 0.08)` for Charcoal Ember accent).
- **Consistency**: Use the same pattern on all page banners within an app. Varying patterns per page feels chaotic.
- **Text readability**: The banner text area (left 40% of the banner) should have the strongest gradient coverage. Place radial/focal patterns toward the right side of the banner where there's no text.
- **Performance**: Pure CSS gradients have zero loading cost. Never use `<canvas>`, JavaScript particle systems, or external image files for banner patterns.

**Dark mode pro-code apps**: When using a dark mode palette (D1 Emerald, D2 Neon Magenta, D3 Charcoal Ember from `color-palettes.md`), pro-code CSS must explicitly set light text colors, dark container backgrounds, and dark-adapted grid/axis colors. Pro-code apps handle dark mode correctly by design (explicit CSS) — the critical failure point is the **App Studio native theme**. After applying dark background colors to the theme, you MUST replace all `c60` font color references with `c58` across cards, navigation, headers, and components. Without this, native elements (hero cards, filter dropdowns, nav text, section headers) render with invisible dark-on-dark text. See `app-studio` skill's "Dark Mode Theme" section for the mandatory fix.

## Pro-Code Chart Patterns (ONLY when explicitly requested)

**Pro-code charts are OPTIONAL. Only build them when the user explicitly asks for pro-code, custom charts, Recharts, D3, or custom visualizations.** Default builds should use native Domo charts.

When pro-code IS requested, use these **proven, production-tested patterns**. All reference apps below have been deployed and verified working in Domo App Studio iframes.

### Default Library Selection

When a pro-code chart is needed, **always default to one of these two stacks** — do not introduce other charting libraries unless the user explicitly requests them:

| Stack | When to use | Reference project |
|-------|------------|-------------------|
| **React + Recharts** (Pattern 1) | Default for most charts. Use when the chart needs React state, composition, or complex interactivity. | `forecast line recharts/` |
| **Chart.js vanilla** (Pattern 3) | Use for simpler charts, when React adds unnecessary weight, or when the app already uses vanilla JS (e.g. Code Engine / AI integration). | `temp-apt-vanilla/customer-retention-aptive/src/vanilla/` |

If the user does not specify a preference, **default to Pattern 1 (React + Recharts)**.

### Proven Reference Pattern 1: React + Recharts + Import Maps (DEFAULT)

This pattern is used by multiple production apps. Key architecture:
- `index.html` loads `ryuu.js` explicitly via `<script src="https://unpkg.com/ryuu.js"></script>`
- Import maps load React 18.2.0 and Recharts 2.12.7 from `esm.sh` (no npm build step)
- `app.js` is an ES module using `React.createElement()` (no JSX transpilation needed)
- Data fetching via `domo.get('/data/v1/{alias}')` with `try/catch`
- Filter listener: use `domo.onFiltersUpdate` (preferred, matches `ryuu.js` API). Always wrap in `try { ... } catch (_) {}` to handle initialization edge cases. The variant `domo.onFiltersUpdated` also works on some `ryuu.js` versions but `onFiltersUpdate` is more reliable

**Working examples** (copy and adapt these — they are proven to work):
- `_archive_prior_build/mfg-production-chart/` — Multi-line with Actual/Plan/Forecast + confidence band, aggregation controls (Daily/Weekly/Monthly)
- `_archive_prior_build/mfg-quality-chart/` — Dual-line (defect rate + scrap rate) with area fill, weekly aggregation
- `forecast line recharts/` — Visits prediction chart with MAE confidence bands

### Proven Reference Pattern 2: D3 + Observable Plot (vanilla JS)

For more exotic visualizations (beeswarms, force layouts, custom SVG):
- Uses `d3.min.js` and `@observablehq/plot` from CDN
- Vanilla `<script>` tags (no ES modules/import maps)
- `domo.get()` via `@domoinc/query` helper
- Working example: `_archive_prior_build/ddx-snowflake_/` — D3 force beeswarm with detail panel

### Proven Reference Pattern 3: Chart.js (vanilla JS)

For simpler charts or when React isn't needed. This is the default vanilla (non-React) stack.

- Uses **Chart.js 4.4.1** from jsDelivr CDN
- Vanilla JavaScript, no framework
- `ryuu.js` loaded from unpkg (same as Pattern 1)
- Working example: `temp-apt-vanilla/customer-retention-aptive/src/vanilla/` — retention chart with Code Engine + AI integration

**CDN URLs** (pin these exact versions):

```html
<script src="https://unpkg.com/ryuu.js"></script>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.1/dist/chart.umd.min.js"></script>
```

Add additional CDN libraries only when the specific feature requires them (e.g. `marked` for AI markdown rendering, `pako` for decompression). The two scripts above are the vanilla baseline.

**Chart.js vanilla styling reference** (from customer-retention-aptive):

```javascript
// Chart.js configuration matching the reference app
const chart = new Chart(ctx, {
  type: 'line',
  data: { datasets: datasets },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    animation: false,
    interaction: { mode: 'nearest', intersect: false },
    scales: {
      x: {
        type: 'linear',
        title: { display: true, text: 'X Label', color: tickColor, font: { size: 12, weight: 500 } },
        grid: { color: gridColor, drawBorder: false },
        ticks: { color: tickColor, font: { size: 11 }, callback: v => v.toLocaleString() }
      },
      y: {
        min: 0, max: 100,
        title: { display: true, text: 'Percent (%)', color: tickColor, font: { size: 12, weight: 500 } },
        grid: { color: gridColor, drawBorder: false },
        ticks: { color: tickColor, font: { size: 11 }, callback: v => `${v}%` }
      }
    },
    plugins: {
      legend: {
        position: 'right',
        labels: { color: legendColor, font: { size: 11 }, usePointStyle: true, pointStyle: 'line' }
      },
      tooltip: { enabled: false, external: externalTooltipHandler }
    }
  }
});
```

**Per-dataset line config:**

```javascript
// Line style options — match reference app patterns
const getLineConfig = (color) => ({
  tension: 0.4,
  borderWidth: 2.5,
  borderColor: color,
  backgroundColor: color,
  pointRadius: 0,
  pointHoverRadius: 5,
  pointHoverBackgroundColor: color,
  pointHoverBorderColor: '#e8ebe8',  // or '#344D38' for dark theme
  pointHoverBorderWidth: 2,
});
```

**Font-family**: Must match the App Studio theme's font family setting from the project's `DESIGN.md`. Map as follows:

| Theme font family | Pro-code CSS `font-family` |
|-------------------|----------------------------|
| Sans              | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif` |
| Serif             | `Georgia, "Times New Roman", "Palatino Linotype", serif` |
| Slab              | `"Roboto Slab", "Rockwell", "Courier New", serif` |

**NEVER hardcode a font stack that doesn't match the App Studio theme.** If the theme uses Serif fonts, all pro-code components must also use Serif. Mismatched fonts between native cards and pro-code cards break visual cohesion.

**Container layout**: `.app-container` with `height: 100vh`, `.chart-container` with `flex: 1; min-height: 0; padding: 16px`. Canvas set to `width: 100% !important; height: 100% !important`.

**CRITICAL: Each sub-page MUST use a DIFFERENT chart type.** Never repeat line charts across all pages. The Overview page uses a time-series line/area chart. Sub-pages MUST vary: use bar, stacked bar, horizontal bar, scatter, beeswarm, heatmap, or treemap. Select chart type based on the page's data shape:

| Page data shape | Chart type | Recharts component |
|-----------------|-----------|-------------------|
| Trend over time | Line / Area | `ComposedChart` + `Line` / `Area` |
| Category comparison | Vertical bar | `BarChart` + `Bar` |
| Composition / breakdown | Stacked bar | `BarChart` + `Bar` (stacked) |
| Ranking / distribution | Horizontal bar | `BarChart` layout="vertical" + `Bar` |
| Correlation / density | Scatter | `ScatterChart` + `Scatter` |
| Part-to-whole | Donut / pie | `PieChart` + `Pie` |

This is a **static HTML app** (no build step). The `index.html` loads `ryuu.js` explicitly and uses browser-native import maps to load React and Recharts from esm.sh. Publish directly with `domo publish` from the app directory.

**Files**: `index.html`, `app.css`, `app.js`, `manifest.json`, `thumbnail.png`

```html
<!-- index.html — MUST load ryuu.js explicitly for domo.get() to work -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <link rel="stylesheet" href="app.css" />
</head>
<body>
  <div id="app"></div>
  <script src="https://unpkg.com/ryuu.js"></script>
  <script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@18.2.0",
      "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
      "recharts": "https://esm.sh/recharts@2.12.7?deps=react@18.2.0,react-dom@18.2.0"
    }
  }
  </script>
  <script type="module" src="app.js"></script>
</body>
</html>
```

```css
/* app.css — styling matched to forecast-line-recharts reference app */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden;
  background: #F8F8F9;
  color: #1F2937;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; }
#app { width: 100%; height: 100%; display: flex; flex-direction: column; padding: 12px; }
.chart-container { display: flex; flex-direction: column; flex: 1; min-height: 0;
  background: #F1F1F3; padding: 16px; }
.chart-header { margin-bottom: 12px; display: flex; justify-content: space-between;
  align-items: flex-start; gap: 8px; flex-wrap: wrap; flex-shrink: 0; }
.chart-title-section h1 { font-size: 16px; font-weight: 600; color: #111827; margin-bottom: 2px; }
.chart-subtitle { font-size: 12px; color: #6B7280; }
.chart-wrapper { flex: 1; min-height: 0; background: #F1F1F3; padding: 8px; }

/* Dropdown — matches reference .aggregation-select exactly */
.aggregation-select {
  appearance: none; background: #FFFFFF;
  border: 1px solid #D1D5DB; border-radius: 3px;
  padding: 3px 18px 3px 6px; font-size: 10px;
  color: #374151; cursor: pointer; min-width: 50px;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='8' height='8' viewBox='0 0 12 12'%3E%3Cpath d='M3 5l3 3 3-3' fill='none' stroke='%236B7280' stroke-width='1.5' stroke-linecap='round'/%3E%3C/svg%3E");
  background-repeat: no-repeat; background-position: right 4px center;
}
.aggregation-select:hover { border-color: #9CA3AF; }
.aggregation-select:focus { outline: none; border-color: #3A6983;
  box-shadow: 0 0 0 2px rgba(58, 105, 131, 0.1); }

/* Confidence band toggle — matches reference .confidence-toggle */
.confidence-toggle {
  display: flex; align-items: center; gap: 3px;
  background: #FFFFFF; border: 1px solid #D1D5DB; border-radius: 3px;
  padding: 3px 6px; font-size: 10px; color: #6B7280;
  cursor: pointer; transition: all 0.15s ease;
}
.confidence-toggle:hover { border-color: #99A9BD; }
.confidence-toggle.active { background: #CAE1F0; border-color: #5E92CE; color: #3A6983; }
.toggle-icon { font-size: 8px; }

/* Tooltip — matches reference .custom-tooltip */
.custom-tooltip {
  background: #FFFFFF; border: 1px solid #E5E7EB; border-radius: 6px;
  padding: 12px 14px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1); font-size: 13px;
}
.tooltip-date { font-weight: 600; color: #111827; margin-bottom: 8px;
  padding-bottom: 8px; border-bottom: 1px solid #F3F4F6; }
.custom-tooltip p { margin: 4px 0; }

/* Legend footer — matches reference .chart-footer */
.chart-footer { display: flex; justify-content: center; gap: 16px; margin-top: 8px;
  padding-top: 8px; border-top: 1px solid #F3F4F6; flex-wrap: wrap; flex-shrink: 0; }
.legend-item { display: flex; align-items: center; gap: 6px; font-size: 11px; color: #4B5563; }
.legend-line { width: 24px; height: 2px; border-radius: 1px; }
.legend-line.dashed { background: repeating-linear-gradient(
  to right, currentColor 0, currentColor 4px, transparent 4px, transparent 7px); }

/* Loading state — matches reference .loading-container */
.loading-container { display: flex; flex-direction: column; align-items: center;
  justify-content: center; flex: 1; color: #6B7280; font-size: 12px; }
.loading-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 0;
  width: 24px; height: 24px; margin-bottom: 8px; }
.loading-cell { background: #5E92CE; border-radius: 1px;
  animation: gridPulse 1.2s ease-in-out infinite; }
@keyframes gridPulse {
  0%, 100% { opacity: 0.3; transform: scale(0.85); }
  50% { opacity: 1; transform: scale(1); }
}

/* Error state — matches reference */
.error-container { display: flex; flex-direction: column; align-items: center;
  justify-content: center; flex: 1; text-align: center; padding: 24px; }
.error-container h2 { color: #DC2626; font-size: 18px; margin-bottom: 8px; }
.error-container p { color: #6B7280; font-size: 14px; margin-bottom: 4px; }

/* Grid line override — reference uses lighter horizontal grid */
.recharts-cartesian-grid-horizontal line { stroke: #F3F4F6; }
.recharts-legend-wrapper { display: none !important; }

@media (max-width: 768px) {
  #app { padding: 16px; }
  .legend-item { font-size: 12px; }
}
```

```javascript
/* app.js — PRODUCTION-GRADE React + Recharts chart (ES module)
   Styling matched to forecast-line-recharts reference app.
   Copy and customize COLORS, ALIAS, column names, TITLE, Y_LABEL per page. */
import React, { useState, useEffect, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ComposedChart, Area, Line, Bar, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

// ── CUSTOMIZE THESE PER PAGE ──────────────────────────────────────────
const COLORS = {
  primary:   '#3A6983',  // main series — replace with palette brand hex
  secondary: '#5E92CE',  // second series (prediction / forecast)
  muted:     '#99A9BD',  // confidence band labels in tooltip
  bandTop:   '#B2D5F3',  // confidence gradient top (opacity 0.4)
  bandBot:   '#CAE1F0',  // confidence gradient bottom (opacity 0.15)
  grid:      '#E5E7EB',  // CartesianGrid stroke (CSS overrides to #F3F4F6)
  axisLine:  '#E5E7EB',  // X-axis line
  text:      '#111827',  // heading text
  textSec:   '#6B7280',  // subtitle, axis ticks, labels
  today:     '#9CA3AF',  // ReferenceLine stroke
  todayLabel:'#6B7280',  // ReferenceLine label fill
};
const ALIAS    = 'DATASET_ALIAS';
const DATE_COL = 'DATE_COL';
const VAL_COLS = ['VAL_COL_1'];
const TITLE    = 'Chart Title';
const Y_LABEL  = 'Units';
// Set true if the dataset has upper/lower confidence columns
const HAS_CONFIDENCE = false;
const CONF_UPPER = 'UPPER_COL';
const CONF_LOWER = 'LOWER_COL';
// ─────────────────────────────────────────────────────────────────────

// ── DATA PARSING ─────────────────────────────────────────────────────
const parseData = (raw) => {
  if (!raw?.length) return [];
  let headers, rows;
  if (Array.isArray(raw[0])) {
    headers = raw[0].map(h => String(h).toUpperCase().replace(/\./g, '_'));
    rows = raw.slice(1);
  } else {
    headers = Object.keys(raw[0]).map(h => h.toUpperCase().replace(/\./g, '_'));
    rows = raw.map(r => Object.keys(r).map(k => r[k]));
  }
  const find = (n) => headers.findIndex(h => h === n.toUpperCase() || h.includes(n.toUpperCase()));
  const di = find(DATE_COL);
  if (di === -1) { console.error('Date column not found. Headers:', headers); return []; }
  const valIndices = VAL_COLS.map(c => ({ key: c, idx: find(c) })).filter(v => v.idx !== -1);
  const upperIdx = HAS_CONFIDENCE ? find(CONF_UPPER) : -1;
  const lowerIdx = HAS_CONFIDENCE ? find(CONF_LOWER) : -1;

  return rows.map(r => {
    const obj = { date: new Date(r[di]) };
    valIndices.forEach(({ key, idx }) => { obj[key] = parseFloat(r[idx]) || null; });
    if (upperIdx !== -1 && lowerIdx !== -1) {
      const lo = parseFloat(r[lowerIdx]), hi = parseFloat(r[upperIdx]);
      if (!isNaN(lo) && !isNaN(hi)) obj.confidenceRange = [lo, hi];
    }
    return obj;
  }).filter(d => !isNaN(d.date.getTime()));
};

// ── AGGREGATION (Daily / Weekly / Monthly) ───────────────────────────
const aggregateData = (data, period) => {
  const grouped = {};
  data.forEach(item => {
    let key;
    const d = item.date;
    switch (period) {
      case 'week': {
        const s = new Date(d); s.setDate(d.getDate() - d.getDay());
        key = s.toISOString().split('T')[0]; break;
      }
      case 'month':
        key = `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-01`; break;
      default:
        key = d.toISOString().split('T')[0];
    }
    if (!grouped[key]) grouped[key] = { date: key, _counts: {} };
    const g = grouped[key];
    VAL_COLS.forEach(c => {
      if (item[c] != null) {
        g[c] = (g[c] || 0) + item[c];
        g._counts[c] = (g._counts[c] || 0) + 1;
      }
    });
    if (item.confidenceRange) g.confidenceRange = item.confidenceRange;
  });
  return Object.values(grouped)
    .map(g => { const { _counts, ...rest } = g; return rest; })
    .sort((a, b) => new Date(a.date) - new Date(b.date));
};

// ── FORMATTING ───────────────────────────────────────────────────────
const fmtNum = v => {
  if (v >= 1e6) return `${(v/1e6).toFixed(1)}M`;
  if (v >= 1e3) return `${(v/1e3).toFixed(0)}K`;
  return `${Math.round(v)}`;
};
const fmtDate = (s, period) => {
  const d = new Date(s);
  if (period === 'month') return d.toLocaleDateString('en-US',{ month:'short', year:'numeric' });
  return d.toLocaleDateString('en-US',{ month:'short', day:'numeric' });
};
const calcTickInterval = (len) => {
  if (len <= 30) return 0;
  if (len <= 90) return 6;
  if (len <= 180) return 13;
  return Math.ceil(len / 18) - 1;
};

// ── CUSTOM TOOLTIP (uses .custom-tooltip CSS class) ──────────────────
const ChartTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  const d = new Date(label);
  const fmt = d.toLocaleDateString('en-US',{ weekday:'short', month:'short', day:'numeric', year:'numeric' });
  const pt = payload[0]?.payload;
  return React.createElement('div', { className: 'custom-tooltip' },
    React.createElement('p', { className: 'tooltip-date' }, fmt),
    VAL_COLS.map((c, i) =>
      pt?.[c] != null && React.createElement('p', { key: c,
        style: { color: i === 0 ? COLORS.primary : COLORS.secondary, margin: 0 } },
        `${c}: ${fmtNum(pt[c])}`)
    ),
    HAS_CONFIDENCE && pt?.confidenceRange && [
      React.createElement('p', { key:'lo', style:{ color: COLORS.muted, margin: 0 } },
        `Lower: ${fmtNum(pt.confidenceRange[0])}`),
      React.createElement('p', { key:'hi', style:{ color: COLORS.muted, margin: 0 } },
        `Upper: ${fmtNum(pt.confidenceRange[1])}`)
    ]
  );
};

// ── LOADING CELL DELAYS (row-major 3×3 grid) ────────────────────────
const LOAD_DELAYS = ['0s','0.1s','0.2s','0.1s','0.2s','0.3s','0.2s','0.3s','0.4s'];

// ── MAIN CHART COMPONENT ─────────────────────────────────────────────
const Chart = () => {
  const [rawData, setRawData] = useState([]);
  const [aggregation, setAggregation] = useState('day');
  const [showBand, setShowBand] = useState(true);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const now = new Date();
  const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

  const fetchAndParse = async () => {
    try {
      setLoading(true);
      const data = await domo.get('/data/v1/' + ALIAS);
      setRawData(parseData(data));
      setError(null);
    } catch (e) { setError(e.message || String(e)); }
    finally { setLoading(false); }
  };

  useEffect(() => { fetchAndParse(); }, []);

  useEffect(() => {
    try {
      if (typeof domo !== 'undefined' && domo.onFiltersUpdate) {
        domo.onFiltersUpdate(() => fetchAndParse());
      }
    } catch (_) {}
  }, []);

  const chartData = useMemo(() => aggregateData(rawData, aggregation), [rawData, aggregation]);
  const todayInRange = chartData.length > 0 &&
    new Date(chartData[0].date) <= new Date(today) &&
    new Date(chartData[chartData.length - 1].date) >= new Date(today);

  if (loading) return React.createElement('div', { className: 'loading-container' },
    React.createElement('div', { className: 'loading-grid' },
      ...[0,1,2,3,4,5,6,7,8].map(i =>
        React.createElement('div', { key: i, className: 'loading-cell',
          style: { animationDelay: LOAD_DELAYS[i] } })
      )
    ),
    React.createElement('p', null, 'Loading…')
  );

  if (error) return React.createElement('div', { className: 'error-container' },
    React.createElement('h2', null, 'Error'),
    React.createElement('p', null, error)
  );

  const dateRange = chartData.length > 0
    ? `${new Date(chartData[0].date).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})} – ${new Date(chartData[chartData.length-1].date).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}`
    : '';

  const colorKeys = [COLORS.primary, COLORS.secondary];

  return React.createElement('div', { className: 'chart-container' },
    React.createElement('div', { className: 'chart-header' },
      React.createElement('div', { className: 'chart-title-section' },
        React.createElement('h1', null, TITLE),
        React.createElement('p', { className: 'chart-subtitle' },
          `${dateRange}, by ${aggregation === 'day' ? 'Day' : aggregation === 'week' ? 'Week' : 'Month'}`)
      ),
      React.createElement('div', { style: { display:'flex', alignItems:'center', gap: 6 } },
        HAS_CONFIDENCE && React.createElement('button', {
          className: `confidence-toggle${showBand ? ' active' : ''}`,
          onClick: () => setShowBand(b => !b)
        },
          React.createElement('span', { className: 'toggle-icon' }, '◉'),
          'Band'
        ),
        React.createElement('select', {
          className: 'aggregation-select',
          value: aggregation, onChange: e => setAggregation(e.target.value)
        },
          React.createElement('option', { value:'day' }, 'Daily'),
          React.createElement('option', { value:'week' }, 'Weekly'),
          React.createElement('option', { value:'month' }, 'Monthly')
        )
      )
    ),

    React.createElement('div', { className: 'chart-wrapper', key: `w-${aggregation}` },
      React.createElement(ResponsiveContainer, { width: '100%', height: '100%' },
        React.createElement(ComposedChart, { data: chartData, margin: { top:10, right:20, left:10, bottom:20 } },
          React.createElement('defs', null,
            React.createElement('linearGradient', { id: 'confidenceGradient', x1:'0', y1:'0', x2:'0', y2:'1' },
              React.createElement('stop', { offset:'0%', stopColor: COLORS.bandTop, stopOpacity: 0.4 }),
              React.createElement('stop', { offset:'100%', stopColor: COLORS.bandBot, stopOpacity: 0.15 })
            )
          ),
          React.createElement(CartesianGrid, { strokeDasharray:'3 3', stroke: COLORS.grid, vertical: false }),
          React.createElement(XAxis, {
            dataKey: 'date', tickFormatter: d => fmtDate(d, aggregation),
            stroke: COLORS.textSec, fontSize: 10, tickLine: false,
            axisLine: { stroke: COLORS.axisLine },
            height: aggregation === 'day' ? 40 : 30,
            interval: aggregation === 'day' ? calcTickInterval(chartData.length) : 'preserveStartEnd'
          }),
          React.createElement(YAxis, {
            tickFormatter: fmtNum, stroke: COLORS.textSec, fontSize: 12,
            tickLine: false, axisLine: false,
            label: { value: Y_LABEL, angle: -90, position: 'insideLeft',
              style: { textAnchor: 'middle', fill: COLORS.textSec, fontSize: 12 } }
          }),
          React.createElement(Tooltip, { content: React.createElement(ChartTooltip) }),
          todayInRange && React.createElement(ReferenceLine, {
            x: today, stroke: COLORS.today, strokeDasharray: '4 4',
            label: { value: 'Today', position: 'top', fill: COLORS.todayLabel, fontSize: 11 }
          }),
          HAS_CONFIDENCE && showBand && React.createElement(Area, {
            type: 'monotone', dataKey: 'confidenceRange',
            stroke: 'none', fill: 'url(#confidenceGradient)', fillOpacity: 1,
            name: 'Confidence Band', legendType: 'none'
          }),
          ...VAL_COLS.map((c, i) => React.createElement(Line, {
            key: c, type: 'monotone', dataKey: c,
            stroke: colorKeys[i % colorKeys.length], strokeWidth: 2,
            dot: false, activeDot: { r: 4, fill: colorKeys[i % colorKeys.length] },
            name: c, connectNulls: false,
            ...(i > 0 ? { strokeDasharray: '4 3' } : {})
          }))
        )
      )
    ),

    React.createElement('div', { className: 'chart-footer' },
      ...VAL_COLS.map((c, i) =>
        React.createElement('div', { key: c, className: 'legend-item' },
          React.createElement('span', { className: `legend-line${i > 0 ? ' dashed' : ''}`,
            style: { background: i > 0 ? undefined : colorKeys[i], color: colorKeys[i] } }),
          React.createElement('span', null, c)
        )
      ),
      HAS_CONFIDENCE && React.createElement('div', { className: 'legend-item' },
        React.createElement('span', { style: {
          display: 'inline-block', width: 16, height: 12, borderRadius: 2,
          background: `linear-gradient(180deg, rgba(178,213,243,0.4) 0%, rgba(202,225,240,0.15) 100%)`,
          border: '1px solid rgba(94,146,206,0.4)'
        } }),
        React.createElement('span', null, 'Confidence Band')
      )
    )
  );
};

createRoot(document.getElementById('app')).render(React.createElement(Chart));
```

**Placement**: width 60, height 30, `hideTitle: true`, `fitToFrame: true`, style ca1. Position below a HEADER content item.

**Per-page customization**: Create a separate app directory per page. Change `ALIAS`, `DATE_COL`, `VAL_COL`, `TITLE`, `SUBTITLE`, and `COLORS` in each `app.js`.

**Manifest**: Use empty `fields: []` to avoid column-name mismatches. Include a `thumbnail.png` (300×300 min) or Domo returns DA0087.

### Alternative Chart Type Templates (Sub-Pages)

The line/area template above is for Overview pages. Sub-pages MUST use different chart types. Below are the key Recharts `createElement` snippets for alternative types. All use the same `index.html`, `app.css`, data parsing, loading/error states, and tooltip patterns from the line chart template — only the chart render section changes.

**Vertical Bar Chart** (category comparison — e.g., production by plant, revenue by region):

```javascript
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';

// In render — replace ComposedChart+Line with:
React.createElement(ResponsiveContainer, { width: '100%', height: '100%' },
  React.createElement(BarChart, { data: chartData, margin: { top: 10, right: 20, left: 10, bottom: 20 } },
    React.createElement(CartesianGrid, { strokeDasharray: '3 3', stroke: COLORS.grid, vertical: false }),
    React.createElement(XAxis, {
      dataKey: 'category', stroke: COLORS.textSec, fontSize: 10,
      tickLine: false, axisLine: { stroke: COLORS.axisLine }
    }),
    React.createElement(YAxis, {
      tickFormatter: fmtNum, stroke: COLORS.textSec, fontSize: 12,
      tickLine: false, axisLine: false,
      label: { value: Y_LABEL, angle: -90, position: 'insideLeft',
        style: { textAnchor: 'middle', fill: COLORS.textSec, fontSize: 12 } }
    }),
    React.createElement(Tooltip, { content: React.createElement(ChartTooltip) }),
    React.createElement(Bar, { dataKey: 'value', fill: COLORS.primary, radius: [2, 2, 0, 0], maxBarSize: 40 })
  )
)
```

**Stacked Bar Chart** (composition — e.g., defects by type, cost breakdown):

```javascript
// Same imports as vertical bar. Data must have multiple value keys.
React.createElement(BarChart, { data: chartData, margin: { top: 10, right: 20, left: 10, bottom: 20 } },
  React.createElement(CartesianGrid, { strokeDasharray: '3 3', stroke: COLORS.grid, vertical: false }),
  React.createElement(XAxis, { dataKey: 'category', stroke: COLORS.textSec, fontSize: 10, tickLine: false }),
  React.createElement(YAxis, { tickFormatter: fmtNum, stroke: COLORS.textSec, fontSize: 12, tickLine: false, axisLine: false }),
  React.createElement(Tooltip, { content: React.createElement(ChartTooltip) }),
  // One Bar per series, all stackId="stack"
  React.createElement(Bar, { dataKey: 'series1', stackId: 'stack', fill: COLORS.primary, maxBarSize: 40 }),
  React.createElement(Bar, { dataKey: 'series2', stackId: 'stack', fill: COLORS.secondary, maxBarSize: 40 }),
  React.createElement(Bar, { dataKey: 'series3', stackId: 'stack', fill: COLORS.muted, radius: [2, 2, 0, 0], maxBarSize: 40 })
)
```

**Horizontal Bar Chart** (rankings — e.g., top suppliers, defect causes, plant performance):

```javascript
// BarChart with layout="vertical" flips axes
React.createElement(BarChart, {
  data: chartData, layout: 'vertical',
  margin: { top: 10, right: 20, left: 80, bottom: 10 }  // left margin for category labels
},
  React.createElement(CartesianGrid, { strokeDasharray: '3 3', stroke: COLORS.grid, horizontal: false }),
  React.createElement(XAxis, {
    type: 'number', tickFormatter: fmtNum, stroke: COLORS.textSec, fontSize: 10
  }),
  React.createElement(YAxis, {
    type: 'category', dataKey: 'category', stroke: COLORS.textSec, fontSize: 11,
    width: 70, tickLine: false
  }),
  React.createElement(Tooltip, { content: React.createElement(ChartTooltip) }),
  React.createElement(Bar, { dataKey: 'value', fill: COLORS.primary, radius: [0, 2, 2, 0], maxBarSize: 24 })
)
```

**Scatter Chart** (correlation — e.g., cycle time vs defect rate, cost vs lead time):

```javascript
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, ZAxis } from 'recharts';

React.createElement(ResponsiveContainer, { width: '100%', height: '100%' },
  React.createElement(ScatterChart, { margin: { top: 10, right: 20, left: 10, bottom: 20 } },
    React.createElement(CartesianGrid, { strokeDasharray: '3 3', stroke: COLORS.grid }),
    React.createElement(XAxis, {
      dataKey: 'x', name: 'X Metric', stroke: COLORS.textSec, fontSize: 10,
      label: { value: 'X Label', position: 'bottom', fill: COLORS.textSec, fontSize: 12 }
    }),
    React.createElement(YAxis, {
      dataKey: 'y', name: 'Y Metric', stroke: COLORS.textSec, fontSize: 12,
      label: { value: 'Y Label', angle: -90, position: 'insideLeft',
        style: { textAnchor: 'middle', fill: COLORS.textSec, fontSize: 12 } }
    }),
    React.createElement(ZAxis, { dataKey: 'z', range: [40, 400], name: 'Size' }),
    React.createElement(Tooltip, { content: React.createElement(ChartTooltip) }),
    React.createElement(Scatter, { data: chartData, fill: COLORS.primary, fillOpacity: 0.7 })
  )
)
```

**Data shape for each chart type**: The data parsing function must produce the correct shape:
- **Vertical/stacked bar**: `[{ category: 'Plant A', value: 1234 }, ...]` — group by dimension, aggregate metric
- **Horizontal bar**: Same as vertical bar, sorted by value descending
- **Scatter**: `[{ x: 45.2, y: 3.1, z: 100, label: 'Plant A' }, ...]` — two numeric axes + optional size

## Known Issues and Gotchas

### Design Cache Corruption

When `domo publish` updates an existing design (same `id` in manifest.json), the CDN may cache stale files. Symptoms: HTML loads correctly (`<div id="app">` exists), `ryuu.js` loads, but ESM module imports from `esm.sh` never fire — `#app` innerHTML is empty.

**Diagnosis**: Compare a working chart's iframe network requests (dozens of `esm.sh` 200s) vs the broken chart (zero `esm.sh` requests). Both have identical `index.html` with importmap, but ESM resolution silently fails on the broken design.

**Fix**: Remove the `id` field from `manifest.json` and run `domo publish` again. This creates a NEW design with a fresh CDN cache. Then create a new context and card instance from the new design ID. The old card can be deleted with `DELETE /content/v1/cards/{cardId}`.

### Context API Path

The `/domoapps/apps/v2/contexts` and `/domoapps/apps/v2` endpoints do NOT use the `/api/` prefix. They live at the root domain:
- `POST https://{instance}.domo.com/domoapps/apps/v2/contexts`
- `POST https://{instance}.domo.com/domoapps/apps/v2?fullpage=false&pageId=...`

Using `https://{instance}.domo.com/api/domoapps/...` returns `404 "No static resource"`.

### Page IDs Can Change

When an App Studio app is rebuilt or modified, page IDs (`viewId`s) may change. Always read the current app structure via `GET /content/v1/dataapps/{appId}?includeHiddenViews=true` and use `views[].viewId` to get current page IDs. Never cache page IDs across sessions.

## Open Questions

1. **Compact template interaction**: How do the compact template's dimensions interact with a custom app that has its own responsive breakpoints?
2. **Style ID on custom app cards**: Do `sourceId` styles (ca1–ca8) have any visual effect on custom app card containers, or only on native cards?
3. **`acceptDateFilter` vs `acceptFilters`**: Are date filters delivered via the same `onFiltersUpdated` callback, or through a separate mechanism?
