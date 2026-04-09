# Domo App Studio — Layouts, Pages & Card Management

> **CLI vs API**: The Java CLI has no App Studio commands. All App Studio operations (creating apps, managing views, configuring layouts) require the REST API via curl. This is one area where you must go directly to the API.

> **Status**: Reverse-engineered from live testing, March 2026

---

## Overview

Domo App Studio (formerly "Data Apps") provides a multi-page dashboard builder with a canvas-based layout system. Each app contains multiple **views** (pages), and each view has a **layout** that controls where cards are positioned.

Key concepts:
- **App** (`dataAppId`) — the top-level container (e.g., `453445400`)
- **View** (`viewId`) — a page within the app. The `viewId` doubles as a `pageId` for card operations
- **Layout** (`layoutId`) — the canvas definition for a view. Each view has its own layout with a separate numeric ID
- **Content** — items on the canvas (cards, headers, spacers, separators)
- **Canvas vs Appendix** — content can be on the visible canvas (`virtualAppendix: false`) or in the appendix (`virtualAppendix: true`)

---

## Creating an App Studio App

### 13. Create App

Creates a new App Studio app with a single default landing view.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/content/v1/dataapps` |

**Body**:

```json
{
  "title": "My Dashboard App",
  "description": "Description of the app"
}
```

**Response** (key fields):

```json
{
  "dataAppId": 1400847176,
  "title": "My Dashboard App",
  "landingViewId": 1219076757,
  "views": [
    {
      "viewId": 1219076757,
      "title": null,
      "parentViewId": 0,
      "visible": true,
      "layout": null,
      "children": []
    }
  ]
}
```

The app is created with one default view. The `landingViewId` is the `viewId` of the auto-created page, which doubles as the `pageId` for card and layout operations.

---

## API Endpoints

### 1. Get App Structure

Returns all views, navigation, theme, and app-level settings.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/content/v1/dataapps/:dataAppId` |

**Optional query params**: `?includeHiddenViews=true`

**Response** (key fields):

```json
{
  "dataAppId": 453445400,
  "title": "AeroWISE",
  "landingViewId": 1400409776,
  "views": [
    {
      "viewId": 993651024,
      "title": "Vendor Performance",
      "parentViewId": 0,
      "viewOrder": 4,
      "visible": true,
      "view": null,
      "layout": null,
      "children": []
    }
  ],
  "navigations": [...],
  "theme": {...}
}
```

Note: The `layout` field in views is always `null` here — layouts are fetched separately.

### 2. Update App Configuration

Updates app-level settings (views, nav, theme). Does NOT update layouts.

| Field | Value |
|-------|-------|
| **Method** | `PUT` |
| **Path** | `/content/v1/dataapps/:dataAppId?includeHiddenViews=true` |

### 3. Reorder Navigation

Reorders the nav tabs/items in the app sidebar.

| Field | Value |
|-------|-------|
| **Method** | `PUT` |
| **Path** | `/content/v1/dataapps/:dataAppId/navigation/reorder` |

**Body**: Array of navigation items with `navOrder`:

```json
[
  {"dataAppId": 453445400, "entity": "HOME", "entityId": "home", "title": "Home", "navOrder": 1, "visible": true, "icon": {"value": "home", "size": "DEFAULT"}, "iconPosition": "LEFT"},
  {"dataAppId": 453445400, "entity": "VIEW", "entityId": "993651024", "title": "Vendor Performance", "navOrder": 2, "visible": true, "icon": {"value": "pages", "size": "DEFAULT"}, "iconPosition": "LEFT"},
  ...
]
```

Entity types: `HOME`, `VIEW`, `AI_ASSISTANT`, `CONTROLS`, `DISTRIBUTE`, `MORE`

---

## Page Layout API

### 4. Get Page Layout

Returns the full layout definition for a view, including all content items and their positions.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/content/v4/pages/:pageId/layouts` |

**Response**:

```json
{
  "layoutId": 2063828519,
  "pageUrn": "993651024",
  "printFriendly": true,
  "isDynamic": true,
  "content": [...],
  "standard": {
    "aspectRatio": 1.67,
    "width": 60,
    "frameMargin": 4,
    "framePadding": 8,
    "type": "STANDARD",
    "template": [...]
  },
  "compact": {
    "aspectRatio": 1,
    "width": 12,
    "frameMargin": 4,
    "framePadding": 8,
    "type": "COMPACT",
    "template": [...]
  },
  "hasPageBreaks": false,
  "style": null
}
```

### 5. Acquire Write Lock (REQUIRED before editing)

You **must** acquire a write lock before updating a layout. Without it, you get `403 WL003: Cannot edit without valid writelock`.

| Field | Value |
|-------|-------|
| **Method** | `PUT` |
| **Path** | `/content/v4/pages/layouts/:layoutId/writelock` |
| **Body** | `{}` |

**Response**:

```json
{
  "layoutId": 895068205,
  "userId": 1176270794,
  "lockTimestamp": 1772753728868,
  "lockHeartbeat": 1772753728868
}
```

### 6. Update Page Layout

Updates the layout (card positions, styles, canvas vs appendix). Must hold write lock.

| Field | Value |
|-------|-------|
| **Method** | `PUT` |
| **Path** | `/content/v4/pages/layouts/:layoutId` |
| **Content-Type** | `application/json;charset=utf-8` |

**Body**: The full layout object (same structure as GET response). See "Layout Structure" below.

### 7. Release Write Lock

Always release the lock when done editing.

| Field | Value |
|-------|-------|
| **Method** | `DELETE` |
| **Path** | `/content/v4/pages/layouts/:layoutId/writelock` |

---

## Adding Cards to App Studio Pages

### 8. Add Card to a Page

Adds an existing card to an App Studio view. The card goes to the **appendix** by default.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/content/v1/pages/:pageId/cards/:cardId` |
| **Body** | `{}` |

This is the same as standard Domo page card assignment. The `pageId` is the `viewId` from the app structure.

### 9. List Cards on a Page

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/content/v1/pages/:pageId/cards` |

Returns an array of card objects with `id` and `title`.

### 10. Create a Card Directly on a Page

Creates a new KPI card and adds it to the page in one step.

| Field | Value |
|-------|-------|
| **Method** | `PUT` |
| **Path** | `/content/v3/cards/kpi?pageId=:pageId` |

See `domo-card-crud.md` for the full card body schema.

### 11. Remove a Card from a Page

Removes a card from an App Studio page without deleting the card itself. The card remains in Domo and on any other pages it's assigned to.

| Field | Value |
|-------|-------|
| **Method** | `DELETE` |
| **Path** | `/content/v1/pages/:pageId/cards/:cardId` |

No request body needed. Returns empty response on success.

**Verified**: Used to remove 34 cards from 7 App Studio pages in a single session. All 34 removals succeeded per page.

### 12. Add Cards to the Domo Overview Page

The Domo overview/home page uses the special page ID `-100000`. Cards can be added to it using the same endpoint as any other page.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/content/v1/pages/-100000/cards/:cardId` |
| **Body** | `{}` |

**Verified**: Added 34 cards to page `-100000` in a single batch. All succeeded.

This is useful when you want cards visible on the main Domo overview but NOT inside the App Studio app views.

---

## Layout Structure

### Content Array

The `content` array defines what items exist on the page. Each item has a `contentKey` that links to the `template` arrays.

**Card content item**:

```json
{
  "id": 614,
  "contentKey": 2,
  "compactInteractionDefault": true,
  "hideTitle": false,
  "hideDescription": true,
  "hideSummary": false,
  "summaryNumberOnly": false,
  "hideTimeframe": false,
  "hideFooter": true,
  "hideWrench": false,
  "hideMargins": false,
  "hasSummary": false,
  "fitToFrame": false,
  "hideBorder": false,
  "acceptFilters": true,
  "acceptDateFilter": true,
  "acceptSegments": true,
  "cardId": 2011347189,
  "cardUrn": "2011347189",
  "style": {
    "sourceId": "ca8",
    "textColor": null
  },
  "type": "CARD"
}
```

**Header content item**:

```json
{
  "contentKey": 1,
  "text": "Section Title",
  "type": "HEADER"
}
```

### Content Item Properties

| Property | Description |
|----------|-------------|
| `contentKey` | Unique key within this layout, links to template entries |
| `type` | `CARD`, `HEADER`, `SPACER`, `SEPARATOR` |
| `cardId` / `cardUrn` | The Domo card ID (for `CARD` type only) |
| `style` | Card styling — see "Card Styles" below |
| `hideTitle` | Hide the card title |
| `hideDescription` | Hide the card description |
| `hideFooter` | Hide the card footer |
| `hideSummary` | Hide the summary number |
| `hideBorder` | Hide the card border |
| `hideMargins` | Hide margins around the card |
| `fitToFrame` | Scale card to fit its frame |
| `acceptFilters` | Whether this card accepts page-level filters |
| `acceptDateFilter` | Whether this card accepts date filters |
| `acceptSegments` | Whether this card accepts segments |

### Template Arrays (Standard & Compact)

The `standard.template` and `compact.template` arrays define the **grid positions** of each content item. Standard is for desktop, compact is for mobile.

**Canvas item** (visible on the page):

```json
{
  "type": "CARD",
  "contentKey": 7,
  "x": 0,
  "y": 3,
  "width": 10,
  "height": 10,
  "virtualAppendix": false,
  "virtual": false,
  "children": null
}
```

**Appendix item** (hidden in the appendix section):

```json
{
  "type": "CARD",
  "contentKey": 3,
  "x": 0,
  "y": 38,
  "width": 15,
  "height": 30,
  "virtualAppendix": true,
  "virtual": true,
  "children": null
}
```

### Canvas vs Appendix

| Property | Canvas | Appendix |
|----------|--------|----------|
| `virtual` | `false` | `true` |
| `virtualAppendix` | `false` | `true` |

To move a card from the appendix to the canvas, set both to `false` and position it in the grid.

### Grid System

**Standard layout** (desktop):
- Grid width: `60` units
- Typical card widths: `10` (6 across), `15` (4 across), `20` (3 across), `30` (2 across), `60` (full width)
- Typical card height: `10` units for KPI/filter cards, `22` for charts, `25` for tables, `30` for large charts
- Header height: `4` units
- Spacer height: `3` units
- Separator height: `2` units

**Compact layout** (mobile):
- Grid width: `12` units
- Typical card width: `12` (full width, stacked vertically)
- Typical card height: `6` for KPI cards, `8` for charts, `10` for tables
- Header height: `3` units

### Content Type Elements

| Type | Purpose | Has contentKey in content array? |
|------|---------|----------------------------------|
| `CARD` | A Domo card | Yes |
| `HEADER` | Section title text | Yes (with `text` field) |
| `SPACER` | Empty vertical space | No (template only) |
| `SEPARATOR` | Horizontal divider line | No (template only) |
| `PAGE_BREAK` | Page break marker (appendix artifact) | No (template only) |

---

## Card Styles

Cards on App Studio pages can have visual styles applied. The style is set in the `content` array entry.

```json
"style": {
  "sourceId": "ca8",
  "textColor": null
}
```

### Style IDs

Styles range from `ca1` to `ca8`:

| sourceId | Style |
|----------|-------|
| `ca1` | Style 1 |
| `ca2` | Style 2 |
| `ca3` | Style 3 |
| `ca4` | Style 4 |
| `ca5` | Style 5 |
| `ca6` | Style 6 |
| `ca7` | Style 7 |
| `ca8` | Style 8 (confirmed working) |

Style is applied per-card per-page. The same card can have different styles on different pages. Omitting the `style` property uses the default/no style.

To apply a style, add the `style` object to the content entry and PUT the layout.

---

## Complete Workflow: Add Filter Cards to All Pages

This workflow adds 6 dropdown filter cards to all views in an App Studio app, positioned identically on each page.

### Step 1: Create the cards on one page

```bash
curl -X PUT "https://instance.domo.com/api/content/v3/cards/kpi?pageId=993651024" \
  -H "Content-Type: application/json" \
  -H "X-DOMO-Developer-Token: $TOKEN" \
  -d '{ ... card body ... }'
```

### Step 2: Configure the layout on the first page via the UI

Use the App Studio editor to position the cards, set styles, etc. This becomes the reference layout.

### Step 3: Add the same cards to other pages (goes to appendix)

```bash
curl -X POST "https://instance.domo.com/api/content/v1/pages/{pageId}/cards/{cardId}" \
  -H "X-DOMO-Developer-Token: $TOKEN" \
  -d '{}'
```

### Step 4: Move cards from appendix to canvas on each page

For each target page:

```python
# 1. GET the layout
layout = GET /content/v4/pages/{pageId}/layouts

# 2. Acquire write lock
PUT /content/v4/pages/layouts/{layoutId}/writelock  body: {}

# 3. Modify the layout:
#    - Add content entries for each card (with style)
#    - Add template entries with virtualAppendix=false, virtual=false
#    - Position cards in the grid (x, y, width, height)

# 4. PUT the updated layout
PUT /content/v4/pages/layouts/{layoutId}  body: { modified layout }

# 5. Release write lock
DELETE /content/v4/pages/layouts/{layoutId}/writelock
```

### Example: 6 filter cards in a row

Content entries:
```json
{
  "contentKey": 7,
  "hideFooter": true,
  "hideDescription": true,
  "acceptFilters": true,
  "cardId": 1219580811,
  "cardUrn": "1219580811",
  "style": {"sourceId": "ca8", "textColor": null},
  "type": "CARD"
}
```

Standard template (6 cards, 10 units wide each):
```json
{"type": "SPACER", "contentKey": 0, "x": 0, "y": 0, "width": 60, "height": 3, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 2, "x": 0,  "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 3, "x": 10, "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 4, "x": 20, "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 5, "x": 30, "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 6, "x": 40, "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "CARD", "contentKey": 7, "x": 50, "y": 3, "width": 10, "height": 10, "virtualAppendix": false, "virtual": false},
{"type": "SEPARATOR", "contentKey": 8, "x": 0, "y": 13, "width": 60, "height": 2, "virtualAppendix": false, "virtual": false}
```

---

## Complete Workflow: Build a Full Dashboard App Programmatically

This workflow creates a multi-section App Studio app from scratch — no UI interaction needed.

### Step 1: Create the App

```python
resp = requests.post(f"{BASE}/content/v1/dataapps", headers=HEADERS, json={
    "title": "Sales Metrics Dashboard",
    "description": "Sales performance metrics"
})
app = resp.json()
app_id = app["dataAppId"]       # e.g., 1400847176
page_id = app["landingViewId"]  # e.g., 1219076757 — this IS the pageId
```

### Step 2: Create Cards on the Page

Use `PUT /content/v3/cards/kpi?pageId={page_id}` to create each card. Cards are automatically added to the page and placed in the **appendix**. See `domo-card-crud.md` for the full card body schema.

```python
# Create as many cards as needed — they all go to the appendix
for card_def in card_definitions:
    resp = requests.put(f"{BASE}/content/v3/cards/kpi?pageId={page_id}",
        headers=HEADERS, json=card_def)
    card_id = resp.json()["id"]
```

### Step 3: Get the Layout and Inspect Content Keys

```python
resp = requests.get(f"{BASE}/content/v4/pages/{page_id}/layouts", headers=HEADERS)
layout = resp.json()
layout_id = layout["layoutId"]

# Print all content items to see their contentKeys
for c in layout["content"]:
    print(f"key={c['contentKey']} type={c['type']} card={c.get('cardId','')}")
```

**Important**: Domo auto-assigns `contentKey` values when cards are added to the appendix. Keys may not be sequential — gaps occur (e.g., 1,2,3,4,5,6,7,8,9,11,12 — skipping 10). Always read the actual layout to get the real keys.

### Step 4: Build the Template and Update Layout

```python
# Acquire write lock
requests.put(f"{BASE}/content/v4/pages/layouts/{layout_id}/writelock", headers=HEADERS, json={})

# Build standard + compact templates
std_template = []
compact_template = []
y = 0  # Track vertical position for standard
cy = 0  # Track vertical position for compact

# Header row
std_template.append({"type": "HEADER", "contentKey": 1, "x": 0, "y": y, "width": 60, "height": 4,
    "virtualAppendix": False, "virtual": False, "children": None})
compact_template.append({"type": "HEADER", "contentKey": 1, "x": 0, "y": cy, "width": 12, "height": 3,
    "virtualAppendix": False, "virtual": False, "children": None})
y += 4; cy += 3

# KPI cards row (4 cards, 15 units each)
for i, key in enumerate([16, 2, 3, 27]):
    std_template.append({"type": "CARD", "contentKey": key, "x": i * 15, "y": y, "width": 15, "height": 10,
        "virtualAppendix": False, "virtual": False, "children": None})
    compact_template.append({"type": "CARD", "contentKey": key, "x": 0, "y": cy, "width": 12, "height": 6,
        "virtualAppendix": False, "virtual": False, "children": None})
    cy += 6
y += 10

# Chart row (2 charts, 30 units each)
for i, key in enumerate([12, 21]):
    std_template.append({"type": "CARD", "contentKey": key, "x": i * 30, "y": y, "width": 30, "height": 22,
        "virtualAppendix": False, "virtual": False, "children": None})
    compact_template.append({"type": "CARD", "contentKey": key, "x": 0, "y": cy, "width": 12, "height": 8,
        "virtualAppendix": False, "virtual": False, "children": None})
    cy += 8
y += 22

# CRITICAL: Include appendix artifacts (PAGE_BREAK, SEPARATOR) that Domo auto-generated
# These MUST be in the template or you get 400 errors
for artifact_key, artifact_type in appendix_artifacts:
    std_template.append({"type": artifact_type, "contentKey": artifact_key, "x": 0, "y": y, "width": 60,
        "height": 0 if artifact_type == "PAGE_BREAK" else 3,
        "virtualAppendix": True, "virtual": True, "children": None})
    compact_template.append({"type": artifact_type, "contentKey": artifact_key, "x": 0, "y": cy, "width": 12,
        "height": 0 if artifact_type == "PAGE_BREAK" else 1,
        "virtualAppendix": True, "virtual": True, "children": None})

# Update header text
for c in layout["content"]:
    if c["type"] == "HEADER" and c["contentKey"] == 1:
        c["text"] = "Sales Overview"

layout["standard"]["template"] = std_template
layout["compact"]["template"] = compact_template

# PUT the updated layout
requests.put(f"{BASE}/content/v4/pages/layouts/{layout_id}", headers=HEADERS, json=layout)

# Release write lock
requests.delete(f"{BASE}/content/v4/pages/layouts/{layout_id}/writelock", headers=HEADERS)
```

### Recommended Card Sizes

| Card Type | Width | Height | Layout Pattern |
|-----------|-------|--------|----------------|
| KPI / single value | 15 | 10 | 4 across |
| KPI / single value | 20 | 10 | 3 across |
| Chart (bar, line, pie) | 20 | 22 | 3 across |
| Chart (bar, line, pie) | 30 | 22 | 2 across |
| Table (detail) | 60 | 25 | Full width |
| Table (summary) | 30-40 | 25 | 1-2 across |
| Header | 60 | 4 | Full width |
| Separator | 60 | 2 | Full width |

### Multi-Section Layout Pattern

Use `HEADER` content items and `SEPARATOR` template items to create visual sections:

```
y=0:  HEADER "Sales Overview" (height 4)
y=4:  KPI | KPI | KPI | KPI (height 10, width 15 each)
y=14: Chart | Chart (height 22, width 30 each)
y=36: Chart | Chart | Chart (height 22, width 20 each)
y=58: SEPARATOR (height 2)
y=60: HEADER "Pipeline Metrics" (height 4)
y=64: KPI | KPI | Chart (height 10)
y=74: Chart | Chart (height 22, width 30 each)
y=96: Table (height 25, width 60)
```

---

## Gotchas and Known Issues

| Issue | Detail |
|-------|--------|
| **Write lock required** | You must `PUT /content/v4/pages/layouts/{layoutId}/writelock` before updating a layout. Without it: `403 WL003: Cannot edit without valid writelock`. |
| **Always release the lock** | `DELETE /content/v4/pages/layouts/{layoutId}/writelock` after editing. If you don't, no one else can edit the page until the lock times out. |
| **Cards go to appendix by default** | When you add a card via `POST /content/v1/pages/{pageId}/cards/{cardId}` or `PUT /content/v3/cards/kpi?pageId=`, it goes to the appendix. You must update the layout to move it to the canvas. |
| **layoutId ≠ pageId** | Each page has its own `layoutId` (a different numeric ID). Get it from `GET /content/v4/pages/{pageId}/layouts`. |
| **viewId = pageId** | In App Studio, the `viewId` from the app structure IS the `pageId` for card and layout operations. |
| **Template must account for ALL content keys** | Every `contentKey` present in the `content` array MUST have a corresponding entry in BOTH `standard.template` AND `compact.template`. If any key is missing from either template, the PUT returns `400 Bad Request` with no detail. This is the #1 cause of layout update failures. |
| **Appendix artifacts MUST be preserved** | When Domo adds cards to the appendix, it auto-generates `PAGE_BREAK` and `SEPARATOR` entries in the template with `contentKey` values that do NOT exist in the `content` array. These template-only entries MUST be included in your updated template (keep them as `virtualAppendix: true, virtual: true`). Removing them causes `400 Bad Request`. Always diff `content` keys vs `template` keys before building your new layout. |
| **Content keys may have gaps** | Domo assigns `contentKey` values incrementally, but gaps occur (e.g., 1,2,3,4,5,6,7,8,9,11,12 — key 10 is skipped). Never assume sequential keys. Always read the layout to get actual keys. |
| **standard + compact both required** | The PUT body must include both `standard` (desktop) and `compact` (mobile) template arrays. Both must contain entries for all content keys. |
| **Content array is managed by Domo** | When creating cards on a page, Domo auto-populates the `content` array with full card properties (`hideTitle`, `hideFooter`, `acceptFilters`, etc.). You can modify these entries (e.g., change header `text`) but should not add or remove `CARD` entries manually — only move them between canvas and appendix via the template. |
| **New apps have `isDynamic: false`** | Newly created App Studio apps have `isDynamic: false` in their layout (unlike apps created via the UI which may have `isDynamic: true`). This does not affect layout operations. |
| **New apps have `enabled: true`** | Newly created apps include an `enabled` field in the layout response. Preserve this when PUTting updates. |
| **Style is per-content-entry** | Card styles (`"style": {"sourceId": "ca8"}`) are set in the `content` array, not in the template. The same card can have different styles on different pages. |
| **No card duplication** | Adding the same card to multiple pages doesn't duplicate it — it's the same card rendered on each page. Filter interactions are shared. |
| **GET uses `/layouts` (plural)** | The GET endpoint is `/content/v4/pages/{pageId}/layouts` (plural), but the PUT endpoint is `/content/v4/pages/layouts/{layoutId}` (singular with layout ID in path). |
| **DELETE removes card from page only** | `DELETE /content/v1/pages/{pageId}/cards/{cardId}` removes the card-page association, not the card itself. The card continues to exist in Domo and on other pages. |
| **Overview page is `-100000`** | The Domo overview/home page has the special page ID `-100000`. Adding cards to it works with the same `POST /content/v1/pages/-100000/cards/{cardId}` endpoint. |
| **Cards on overview != cards in App Studio** | Adding a card to page `-100000` puts it on the Domo overview page. It does NOT appear inside App Studio views. To have cards in App Studio, add them to the specific view `pageId`. These are independent assignments. |
| **Cards from different datasets on same page** | An App Studio page can contain cards powered by different datasets. There is no restriction. This was verified with a page containing 23 cards across 2 datasets. |

### Layout Update Debugging Checklist

If a layout PUT returns `400 Bad Request`, check these in order:

1. **Missing template entries**: Compare content keys (from `content` array) with template keys (from `standard.template`). Every content key must appear in both `standard` and `compact` templates.
2. **Missing appendix artifacts**: Check for `PAGE_BREAK` and `SEPARATOR` entries in the existing template that have `contentKey` values NOT in the `content` array. These must be preserved.
3. **Template key mismatch**: Ensure the same set of `contentKey` values appears in `standard.template` and `compact.template`.
4. **Children field**: Every template entry must include `"children": null` (or be omitted). Observed in all working layouts.
5. **Missing write lock**: Ensure you acquired the write lock before PUTting.

```python
# Debugging helper — run this before any layout PUT
content_keys = {c["contentKey"] for c in layout["content"]}
std_keys = {t["contentKey"] for t in layout["standard"]["template"]}
cmp_keys = {t["contentKey"] for t in layout["compact"]["template"]}

in_content_not_std = content_keys - std_keys
in_std_not_content = std_keys - content_keys  # May include PAGE_BREAK, SEPARATOR
in_std_not_cmp = std_keys - cmp_keys

if in_content_not_std:
    print(f"ERROR: content keys missing from standard template: {in_content_not_std}")
if in_std_not_cmp:
    print(f"ERROR: standard keys missing from compact template: {in_std_not_cmp}")
# in_std_not_content is OK — these are SEPARATOR/PAGE_BREAK appendix artifacts
```