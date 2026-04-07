---
name: app-studio
description: Build and manage Domo App Studio apps via REST API. Covers app creation, view/page management, canvas layouts, card placement, and multi-page dashboard configuration.
---

# Domo App Studio — Layouts, Pages & Card Management

> **CUSTOM PALETTE REQUIRED**: Never use Domo's native/default color palette. Always select a curated palette from `domo-app-theme/color-palettes.md` (50 OKLCH palettes across 9 harmony types). Pick a palette suited to the use case or ask the user. Use OKLCH values in pro-code CSS; convert to hex for native card `series_N_color` overrides. All App Studio theme colors, pro-code chart colors, banner colors, and card styling must use the chosen palette. See "Custom Color Palette" section under Theme Management.

> **CLI vs API**: The Java CLI has no App Studio commands. All App Studio operations (creating apps, managing views, configuring layouts) require the REST API via curl. This is one area where you must go directly to the API.

> **Authentication**: Use `X-Domo-Authentication: {SID}` for all App Studio API calls. Obtain a SID via `get_sid(instance)` from `upload_bridge.py` (if available in workspace) or via the ryuu token exchange flow (`domo login` → refresh token → SID). Developer tokens (`X-DOMO-Developer-Token`) work for some endpoints but fail on others — SID is universally reliable.

> **Status**: Reverse-engineered from live testing, March 2026
> **Verified against**: `aeroateam-partner.domo.com` (app `453445400`), `csibas.domo.com` (apps `1400847176`, `2061524048`)

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


| Field      | Value                  |
| ---------- | ---------------------- |
| **Method** | `POST`                 |
| **Path**   | `/content/v1/dataapps` |


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

**Verified**: Created 2 apps on `csibas.domo.com`. Both returned 200 with a single default view.

---

## API Endpoints

### 1. Get App Structure

Returns all views, navigation, theme, and app-level settings.


| Field      | Value                             |
| ---------- | --------------------------------- |
| **Method** | `GET`                             |
| **Path**   | `/content/v1/dataapps/:dataAppId` |


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


| Field      | Value                                                     |
| ---------- | --------------------------------------------------------- |
| **Method** | `PUT`                                                     |
| **Path**   | `/content/v1/dataapps/:dataAppId?includeHiddenViews=true` |


**Body**: The full app object as returned by GET. You MUST send the complete object — partial updates cause `400 Bad Request`. Read-only fields (`userAccess`, `isOwner`, `isFavorite`, `canEdit`) can be included (they are ignored) or omitted.

**Key fields that can be changed via PUT**:

| Field | Values | Notes |
|-------|--------|-------|
| `navOrientation` | `TOP`, `LEFT`, `BOTTOM` | Controls nav bar position |
| `showDomoNavigation` | `true`, `false` | **Must be `false` when `navOrientation` is `LEFT`** — the API rejects LEFT + showDomoNavigation=true |
| `showNavigation` | `true`, `false` | Whether nav is visible at all |
| `showTitle` | `true`, `false` | Show app title in nav bar. **Set to `false` for LEFT nav** — the title wastes vertical space and the page names in the left nav already identify the app. |
| `showLogo` | `true`, `false` | Show Domo logo. **Set to `false` for LEFT nav** — keeps the nav clean. |
| `title` | string | App title |
| `description` | string | App description |
| `iconDataFileId` | integer \| null | Custom app icon (tile/launcher). Set via Data File upload (see below). |
| `navIconDataFileId` | integer \| null | Custom icon shown in the left-nav sidebar. Usually set to the same value as `iconDataFileId`. |

The PUT does NOT add or modify views/navigations — use the dedicated endpoints below for those.

### 2a-bis. Custom App Icon

Every App Studio app **must** have a custom icon. Never leave the default placeholder.

**Step 1 — Generate a 256×256 PNG icon** using Pillow (or accept a user-provided image). The icon should visually represent the app's domain using the app's custom brand color palette.

```python
from PIL import Image, ImageDraw
import math, io

def generate_app_icon(brand_hex='#3B82C8', dark_hex='#23272E', size=256):
    """Generate a modern app icon with brand-colored gear and mini bar chart."""
    brand = tuple(int(brand_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
    dark  = tuple(int(dark_hex.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))

    img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    cx, cy = size // 2, size // 2

    # Background circle
    draw.ellipse([8, 8, size - 8, size - 8], fill=dark)

    # Gear teeth
    r_outer, teeth = 90, 8
    for i in range(teeth):
        a = i * (2 * math.pi / teeth)
        a1, a2 = a - 0.15, a + 0.15
        pts = [(cx + r * math.cos(ang), cy + r * math.sin(ang))
               for ang in (a1, a2) for r in (r_outer, r_outer + 18)]
        draw.polygon([pts[0], pts[1], pts[3], pts[2]], fill=brand)

    draw.ellipse([cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer], fill=brand)
    draw.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=dark)
    draw.ellipse([cx - 15, cy - 15, cx + 15, cy + 15], fill=brand)

    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()
```

**Step 2 — Upload to Domo Data File Service**

```
POST /api/data/v1/data-files?name={app-slug}-icon.png&description={App+Title+Icon}&public=true
Content-Type: image/png          ← MUST be image/png, not application/octet-stream
Body: raw PNG bytes
→ Response: {"dataFileId": 12345}
```

**Step 3 — Set on the app** via the standard app PUT (include in the full GET→modify→PUT flow):

```python
app = GET /api/content/v1/dataapps/{appId}
app['iconDataFileId']    = data_file_id
app['navIconDataFileId'] = data_file_id   # same file for both
PUT /api/content/v1/dataapps/{appId}  body=app
```

**Gotchas:**
- `Content-Type` must be `image/png` (not `application/octet-stream`) or the upload returns `415`.
- The PUT must send the **full app object** — partial payloads cause `400 Bad Request`.
- Icon should be 256×256 PNG with transparency for best rendering across Domo surfaces.

### 2b. Create a New View (Page)

Creates a new page/view within an existing App Studio app.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/content/v1/dataapps/:dataAppId/views` |

**Body** — send the `view` sub-object directly (not wrapped):

```json
{
  "owners": [{"id": 723132419, "type": "USER", "displayName": null}],
  "type": "dataappview",
  "title": "Production",
  "pageName": "Production",
  "locked": false,
  "mobileEnabled": true,
  "sharedViewPage": true,
  "virtualPage": false
}
```

**Response** includes both the `view` (with assigned `pageId`) and `layout` (with assigned `layoutId`) objects. The new view automatically gets a navigation entry with icon `pages`.

**Important**: The `owners` array must include at least the current user. The `type` must be `dataappview`. The `title` and `pageName` should match.

### 3. Read and Update Navigation

The navigation is stored in the `navigations` array on the app object, but it is **NOT updated via the app PUT** — changes to `navigations` in the app PUT body are silently ignored.

**READ navigation:**

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/content/v1/dataapps/:dataAppId/navigation` |

Returns the full navigation array including system items (HOME, AI_ASSISTANT, CONTROLS, DISTRIBUTE, MORE).

**UPDATE navigation (reorder, rename, set icons):**


| Field      | Value                                                |
| ---------- | ---------------------------------------------------- |
| **Method** | `PUT`                                                |
| **Path**   | `/content/v1/dataapps/:dataAppId/navigation/reorder` |


**Body**: The full navigation array as returned by GET, with modifications. You can change `title`, `icon`, `navOrder`, and `visible` fields.

```json
[
  {"dataAppId": 453445400, "entity": "HOME", "entityId": "home", "title": "Home", "navOrder": 1, "visible": true, "icon": {"value": "home", "size": "DEFAULT"}, "iconPosition": "LEFT"},
  {"dataAppId": 453445400, "entity": "VIEW", "entityId": "993651024", "title": "Vendor Performance", "navOrder": 2, "visible": true, "icon": {"value": "dashboard", "size": "DEFAULT"}, "iconPosition": "LEFT"},
  ...
]
```

Entity types: `HOME`, `VIEW`, `AI_ASSISTANT`, `CONTROLS`, `DISTRIBUTE`, `MORE`

**CRITICAL**: The `navigations` array is separate from the `views` array. Renaming a view title via the app PUT does NOT rename the nav label. You must use the `/navigation/reorder` endpoint to update nav labels and icons. Always GET the full navigation first, modify only the fields you need, and PUT the complete array back — missing system items causes `400`.

---

## Page Layout API

### 4. Get Page Layout

Returns the full layout definition for a view, including all content items and their positions.


| Field      | Value                               |
| ---------- | ----------------------------------- |
| **Method** | `GET`                               |
| **Path**   | `/content/v4/pages/:pageId/layouts` |


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


| Field      | Value                                           |
| ---------- | ----------------------------------------------- |
| **Method** | `PUT`                                           |
| **Path**   | `/content/v4/pages/layouts/:layoutId/writelock` |
| **Body**   | `{}`                                            |


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


| Field            | Value                                 |
| ---------------- | ------------------------------------- |
| **Method**       | `PUT`                                 |
| **Path**         | `/content/v4/pages/layouts/:layoutId` |
| **Content-Type** | `application/json;charset=utf-8`      |


**Body**: The full layout object (same structure as GET response). See "Layout Structure" below.

### 7. Release Write Lock

Always release the lock when done editing.


| Field      | Value                                           |
| ---------- | ----------------------------------------------- |
| **Method** | `DELETE`                                        |
| **Path**   | `/content/v4/pages/layouts/:layoutId/writelock` |


---

## Adding Cards to App Studio Pages

### 8. Add Card to a Page

Adds an existing card to an App Studio view. The card goes to the **appendix** by default.


| Field      | Value                                     |
| ---------- | ----------------------------------------- |
| **Method** | `POST`                                    |
| **Path**   | `/content/v1/pages/:pageId/cards/:cardId` |
| **Body**   | `{}`                                      |


This is the same as standard Domo page card assignment. The `pageId` is the `viewId` from the app structure.

### 9. List Cards on a Page


| Field      | Value                             |
| ---------- | --------------------------------- |
| **Method** | `GET`                             |
| **Path**   | `/content/v1/pages/:pageId/cards` |


Returns an array of card objects with `id` and `title`.

### 10. Create a Card Directly on a Page

Creates a new KPI card and adds it to the page in one step.


| Field      | Value                                  |
| ---------- | -------------------------------------- |
| **Method** | `PUT`                                  |
| **Path**   | `/content/v3/cards/kpi?pageId=:pageId` |


See `domo-card-crud.md` for the full card body schema.

### 11. Remove a Card from a Page

Removes a card from an App Studio page without deleting the card itself. The card remains in Domo and on any other pages it's assigned to.


| Field      | Value                                     |
| ---------- | ----------------------------------------- |
| **Method** | `DELETE`                                  |
| **Path**   | `/content/v1/pages/:pageId/cards/:cardId` |


No request body needed. Returns empty response on success.

**Verified**: Used to remove 34 cards from 7 App Studio pages in a single session. All 34 removals succeeded per page.

### 12. Add Cards to the Domo Overview Page

The Domo overview/home page uses the special page ID `-100000`. Cards can be added to it using the same endpoint as any other page.


| Field      | Value                                     |
| ---------- | ----------------------------------------- |
| **Method** | `POST`                                    |
| **Path**   | `/content/v1/pages/-100000/cards/:cardId` |
| **Body**   | `{}`                                      |


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


| Property             | Description                                              |
| -------------------- | -------------------------------------------------------- |
| `contentKey`         | Unique key within this layout, links to template entries |
| `type`               | `CARD`, `HEADER`, `SPACER`, `SEPARATOR`                  |
| `cardId` / `cardUrn` | The Domo card ID (for `CARD` type only)                  |
| `style`              | Card styling — see "Card Styles" below                   |
| `hideTitle`          | Hide the card title                                      |
| `hideDescription`    | Hide the card description                                |
| `hideFooter`         | Hide the card footer                                     |
| `hideSummary`        | Hide the summary number                                  |
| `hideBorder`         | Hide the card border                                     |
| `hideMargins`        | Hide margins around the card                             |
| `fitToFrame`         | Scale card to fit its frame                              |
| `acceptFilters`      | Whether this card accepts page-level filters             |
| `acceptDateFilter`   | Whether this card accepts date filters                   |
| `acceptSegments`     | Whether this card accepts segments                       |


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


| Property          | Canvas  | Appendix |
| ----------------- | ------- | -------- |
| `virtual`         | `false` | `true`   |
| `virtualAppendix` | `false` | `true`   |


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


| Type         | Purpose                               | Has contentKey in content array? |
| ------------ | ------------------------------------- | -------------------------------- |
| `CARD`       | A Domo card                           | Yes                              |
| `HEADER`     | Section title text                    | Yes (with `text` field)          |
| `SPACER`     | Empty vertical space                  | No (template only)               |
| `SEPARATOR`  | Horizontal divider line               | No (template only)               |
| `PAGE_BREAK` | Page break marker (appendix artifact) | No (template only)               |


---

## Card Styles

Cards on App Studio pages can have visual styles applied. The style is set in the `content` array entry.

```json
"style": {
  "sourceId": "ca1",
  "textColor": null
}
```

### Style IDs

Styles range from `ca1` to `ca8`:

| sourceId | Style | Recommended use |
|----------|-------|----------------|
| `ca1` | Default surface | **Primary default** — translucent white bg, floating shadow |
| `ca2` | Alternate surface | Same as ca1, alternate slot for variation |
| `ca3` | Light translucent | Lighter opacity — filter/control cards |
| `ca4`–`ca6` | Accent styles | Colored/themed cards |
| `ca7` | Near-opaque surface | Subtle shadow, higher opacity for emphasis |
| `ca8` | Transparent/borderless | Banners, images, notebooks (no chrome) |

Style is applied per-card per-page. The same card can have different styles on different pages. Omitting the `style` property uses the default/no style.

To apply a style, add the `style` object to the content entry and PUT the layout.

### Default Card Style

Cards should use **zero border-radius, zero border weight, zero padding, no drop shadow** per the mandatory reference configuration. See "Card Styles (ca1–ca8)" under Theme Management for the full spec.

```python
# ca1/ca2 — clean surface, zero chrome
card['backgroundColor'] = {'value': 'c56', 'type': 'COLOR_REFERENCE'}  # white
card['borderWidth'] = 0
card['borderRadius'] = 0
card['dropShadow'] = 'NONE'
card['padding'] = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}

# ca8 — fully transparent (banners, images)
card['backgroundColor'] = {'value': 'c56', 'opacity': '00', 'type': 'COLOR_REFERENCE'}
card['borderWidth'] = 0
card['borderRadius'] = 0
card['dropShadow'] = 'NONE'
```

### Page Background: Ultra-Light Gray

Set the page background to an ultra-light neutral gray (`#F5F6F8` or similar). This provides subtle contrast with translucent card surfaces and is standard in modern dashboard design.

```python
# Use c55 for page background
theme['pages'][0]['background'] = {'value': 'c55', 'type': 'COLOR_REFERENCE'}
# Ensure c55 is ultra-light gray
for c in theme['colors']:
    if c['id'] == 'c55':
        c['value'] = {'value': '#F5F6F8', 'type': 'RGB_HEX'}
```

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

This workflow creates a multi-section App Studio app from scratch — no UI interaction needed. Verified on `csibas.domo.com` with 23 cards across 2 sections.

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

### Step 1b: Discover Dataset Schemas

Before creating any cards, query each dataset's schema to get exact column names and types:

```python
resp = requests.get(f"{BASE}/query/v1/datasources/{dataset_guid}/schema/indexed", headers=HEADERS)
schema = resp.json()
columns = schema["tables"][0]["columns"]  # [{"name": "OrderDate", "type": "DATE"}, ...]
```

Store column names per dataset — you'll need them for card `columns` arrays (VALUE, ITEM, SERIES mappings).

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


| Card Type              | Width | Height | Layout Pattern |
| ---------------------- | ----- | ------ | -------------- |
| KPI / single value     | 15    | 10     | 4 across       |
| KPI / single value     | 20    | 10     | 3 across       |
| Chart (bar, line, pie) | 20    | 22     | 3 across       |
| Chart (bar, line, pie) | 30    | 22     | 2 across       |
| Table (detail)         | 60    | 25     | Full width     |
| Table (summary)        | 30-40 | 25     | 1-2 across     |
| Header                 | 60    | 4      | Full width     |
| Separator              | 60    | 2      | Full width     |


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

## Creating Custom App Card Instances (Pro-Code)

Custom app card instances (from published designs) are created via a two-step API: create a context, then create the card from that context.

**CRITICAL PATH NOTE**: The context and card creation endpoints use the **root domain** path (`https://{instance}.domo.com/domoapps/apps/v2/...`), NOT the `/api/` prefix. Using `{BASE}/domoapps/apps/v2/contexts` (where BASE includes `/api/`) returns `404 "No static resource"`. The correct base for these calls is `https://{instance}.domo.com`.

### Step 1: Create a Context

A context defines the dataset mappings, collections, and resource bindings for a card instance.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `https://{instance}.domo.com/domoapps/apps/v2/contexts` |
| **Auth** | `X-DOMO-Developer-Token` or `X-Domo-Authentication` (SID) |

```python
DOMO = f"https://{instance}.domo.com"
ctx_body = {
    "designId": design_id,
    "mapping": [{"alias": alias, "dataSetId": ds_guid, "fields": [], "dql": None}],
    "collections": [], "accountMapping": [], "actionMapping": [],
    "workflowMapping": [], "packageMapping": [],
    "isDisabled": False
}
resp = requests.post(f"{DOMO}/domoapps/apps/v2/contexts", headers=H, json=ctx_body)
context_id = resp.json()[0]["id"]
```

Response: `[context, []]` — the context object contains the generated `id`.

For apps with no datasets (e.g., banners), use `"mapping": []`.

### Step 2: Create the Card from the Context

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **URL** | `https://{instance}.domo.com/domoapps/apps/v2?fullpage=false&pageId={pageId}&cardTitle={urlEncodedTitle}` |

```python
import urllib.parse
title = urllib.parse.quote("My Chart Card")
resp = requests.post(
    f"{DOMO}/domoapps/apps/v2?fullpage=false&pageId={page_id}&cardTitle={title}",
    headers=H, json={"contextId": context_id, "id": context_id})
```

**Critical**: The `id` field must be the **context ID** from Step 1, NOT the design ID. Using the design ID causes 500 errors when datasets differ from the original.

| Param | Description |
|-------|-------------|
| `fullpage` | `false` for standard card, `true` for full-page app |
| `pageId` | Target page ID, or `-100000` for asset library only |
| `cardTitle` | URL-encoded title for the card |

The card is created on the target page. Check the page's card list to get the numeric card ID for layout operations.

### Updating a Context (Rewire Dataset)

`PUT https://{instance}.domo.com/domoapps/apps/v2/contexts/{contextId}` — send the full context object with updated `mapping`.

**Verified**: Used to create banner cards (no datasets) and chart cards (with dataset mapping) across multiple App Studio pages.

### Design Caching Gotcha

If a pro-code card renders a blank `#app` div (HTML loads correctly, `ryuu.js` loads, but ESM imports never fire), the design's files may be cached/corrupted from a prior publish. **Fix**: Create a NEW design (`domo publish` from a directory without an existing `id` in manifest.json) instead of republishing the old design ID. The new design ID will get fresh CDN cache entries.

---

## Page Layout Patterns

### Hero Card Pattern

Every page should follow this vertical structure from top to bottom:

```
y=0:   BANNER (pro-code, per-page design) — full width (60), height 14, style ca8
y=14:  FILTER CARDS — 2-3 dropdown selectors, width 20 each, height 6 (low-profile)
y=20:  HERO METRICS ROW — 3-4 native badge_pop_multi_value cards in ONE ROW (width 20 for 3, or 15 for 4), height 12, style ca1
y=34:  HEADER — section title (e.g., "Production Output"), height 4
y=38:  PRIMARY VIZ — full width (60), height 30, style ca1
y=68:  HEADER — section title (e.g., "Quality & Waste"), height 4
y=72:  DETAIL CARDS — 2-3 native charts per row (width 20 or 30), height 22
y=94+: Additional HEADER + DETAIL SECTIONS as needed
```

The **hero metrics** are **native `badge_pop_multi_value` (Period over Period Multi-Value) cards** — NEVER pro-code. They automatically provide: big number, percent change vs prior period, direction indicator, and additional text. Create via `PUT /content/v3/cards/kpi?pageId=:pageId` with `chartType: "badge_pop_multi_value"`. See `card-creation/SKILL.md` for the full body schema.

The **primary visualization** spans the full horizontal width of the page. **The Overview page** typically uses a time-series line/area chart showing trends. **Sub-pages MUST vary chart types** — use bar charts, stacked bars, horizontal bars, scatter plots, heatmaps, or other types suited to the page's data story. Never use the same chart type on every page. See the chart type selection table below.

#### Primary Viz Chart Type by Page

| Page position | Recommended chart types | Why |
|---------------|------------------------|-----|
| **Overview** | Time-series line/area | Shows trends, forecasts, high-level trajectory |
| **Sub-page 1** (e.g., Production, Revenue) | Vertical bar, grouped bar, stacked bar | Compares categories, shows composition |
| **Sub-page 2** (e.g., Quality, Engagement) | Horizontal bar, lollipop, beeswarm | Rankings, distributions, part-to-whole |
| **Sub-page 3** (e.g., Supply Chain, Support) | Scatter, bubble, treemap, heatmap | Correlations, density, multi-dimensional |

The agent MUST select a **different primary chart type for each sub-page**. Repeating line charts across all pages makes dashboards feel monotonous and wastes the opportunity to match visualization type to data shape. When using pro-code charts, the `app-studio-pro-code` skill provides templates for line, bar, stacked bar, horizontal bar, and scatter patterns.

### Hero Metric Card Design (NATIVE — Never Pro-Code)

**CRITICAL: Never use pro-code apps for hero/summary metric cards.** Always use native `badge_pop_multi_value` cards. They are purpose-built for this use case and provide automatic period-over-period comparison.

Create each hero card with `PUT /content/v3/cards/kpi?pageId=:pageId`:

**CRITICAL: PoP cards require THREE things to show comparison data:**
1. **Date column in `main.columns`** with `mapping: "ITEM"` and `aggregation: "MAX"` (populates the "Time period" drop zone)
2. **`dateRangeFilter`** on the `main` subscription (sets "Date range: This Month" + "Compare to: 1 month ago")
3. **`time_period` subscription** with the same date column

Without all three, the PoP comparison shows "0" instead of actual prior period values.

```python
DATE_RANGE_FILTER = {
    "column": {"column": "OrderDate", "exprType": "COLUMN"},
    "dateTimeRange": {
        "dateTimeRangeType": "INTERVAL_OFFSET",
        "interval": "YEAR",
        "offset": 0,
        "count": 0
    },
    "periods": {
        "type": "COMBINED",
        "combined": [{"interval": "YEAR", "type": "OVER", "count": 1}],
        "count": 0
    }
}
# IMPORTANT: Always use YEAR interval, not MONTH. MONTH causes blank heroes
# when current month has insufficient data (common with synthetic datasets).
# YEAR provides reliable year-over-year comparison that always has data.

card_body = {
    "definition": {
        "subscriptions": {
            "big_number": {
                "name": "big_number",
                "columns": [
                    {"column": "UnitsProduced", "aggregation": "SUM", "alias": "Total Production",
                     "format": {"type": "abbreviated", "format": "#A"}}
                ],
                "filters": []
            },
            "main": {
                "name": "main",
                "columns": [
                    {"column": "OrderDate", "aggregation": "MAX", "mapping": "ITEM"},
                    {"column": "UnitsProduced", "mapping": "VALUE", "aggregation": "SUM", "alias": "Total Production"}
                ],
                "filters": [], "orderBy": [], "groupBy": [],
                "dateRangeFilter": DATE_RANGE_FILTER,
                "fiscal": False, "projection": False, "distinct": False
            },
            "time_period": {
                "name": "time_period",
                "columns": [{"column": "OrderDate", "aggregation": "MAX"}],
                "filters": [], "orderBy": [], "groupBy": [],
                "fiscal": False, "projection": False, "distinct": False
            }
        },
        "formulas": {"dsUpdated": [], "dsDeleted": [], "card": []},
        "annotations": {"new": [], "modified": [], "deleted": []},
        "conditionalFormats": {"card": [], "datasource": []},
        "controls": [],
        "segments": {"active": [], "create": [], "update": [], "delete": []},
        "charts": {
            "main": {
                "component": "main",
                "chartType": "badge_pop_multi_value",
                "overrides": {
                    "gauge_layout": "Center Vertical",
                    "comp_val_displayed": "Percent Change",
                    "addl_text": "Prior Year",
                    "title_text": "Total Production"
                },
                "goal": None
            }
        },
        "dynamicTitle": {"text": [{"text": "Total Production", "type": "TEXT"}]},
        "dynamicDescription": {"text": [], "displayOnCardDetails": True},
        "chartVersion": "12",
        "inputTable": False, "noDateRange": False,
        "title": "Total Production", "description": ""
    },
    "dataProvider": {"dataSourceId": "DATASET_UUID"},
    "variables": True, "columns": False
}
```

Key overrides for `badge_pop_multi_value`:
| Override | Values | Purpose |
|----------|--------|---------|
| `gauge_layout` | `Center Vertical` | Layout of metric elements |
| `comp_val_displayed` | `Percent Change` | Show % change vs prior period |
| `addl_text` | `Prior Year` (ALWAYS use "Prior Year" — MONTH causes blank heroes) | Contextual subtitle |
| `title_text` | e.g. `Total Production` | **Required.** Chart-level title displayed inside the card. Must always be set. |
| `gauge_sizing` | `Default` | Auto-size values |

Create **3-4** hero metric cards per page in a **SINGLE ROW** (never 2 rows). Each card uses the appropriate column, aggregation, and title for that page's domain. Choose the 3-4 most important KPIs. If you have more metrics, put them in the detail section below the primary viz.

**Layout content entry for hero cards** — always hide title and summary (the card's built-in chart display handles all labeling; the App Studio title bar and summary number are redundant clutter):

```json
{
  "hideTitle": true, "hideSummary": true,
  "hideDescription": true, "hideFooter": true,
  "hideBorder": false, "acceptFilters": true, "acceptDateFilter": true,
  "style": {"sourceId": "ca1", "textColor": null}
}
```

**Hero card background — MUST be transparent/light.** Hero cards use style `ca1` which should have a transparent or page-matching background. **NEVER** apply dark background colors or colored card styles (ca3, ca4, etc.) to hero cards. If hero cards appear with dark backgrounds, the theme's `ca1` card definition is wrong — fix it by setting `ca1.backgroundColor` to transparent/white and ensuring `ca1.borderRadius` is 0 with no dark fills. The hero card value text relies on sufficient contrast against a light background.

**Hero card height** — use height **14** in the standard template (not 10). Height 10 is too short and makes the metric values hard to read. Compact (mobile) height: **8**.

**Hero card date range — ALWAYS use YEAR interval.** PoP cards configured with MONTH interval frequently show blank values because:
1. Current month may have no data yet (e.g., April 2nd has minimal April data)
2. Synthetic/demo datasets may not have data in the exact current month
3. MONTH comparisons are fragile and require precise date coverage

**ALWAYS use YEAR interval** — this compares the current year to the prior year, which reliably captures data across all datasets:
```python
"dateTimeRange": {
    "dateTimeRangeType": "INTERVAL_OFFSET",
    "interval": "YEAR",
    "offset": 0,
    "count": 0
},
"periods": {
    "type": "COMBINED",
    "combined": [{"interval": "YEAR", "type": "OVER", "count": 1}],
    "count": 0
}
```
Set `addl_text: "Prior Year"` in overrides. **NEVER use MONTH interval** — it is the #1 cause of blank hero cards.

**Updating existing hero cards:** Use `PUT /content/v3/cards/kpi/definition` (with body `{"dynamicText": true, "variables": true, "urn": "CARD_ID"}`) to READ the current card definition, modify `dateRangeFilter` and `overrides.addl_text`, then `PUT /content/v3/cards/kpi/CARD_ID` with the full body (including `dataProvider.dataSourceId`, `variables: true`, `columns: false`). Format `formulas` as `{"dsUpdated":[], "dsDeleted":[], "card":[]}`, `annotations` as `{"new":[], "modified":[], "deleted":[]}`, `conditionalFormats` as `{"card":[], "datasource":[]}`, `segments` as `{"active":[], "create":[], "update":[], "delete":[]}`.

### Banner Card Placement

Banners are pro-code custom apps (CSS gradient + branding text + **subheader context**) placed at y=0 spanning full width. Each banner should include:
- Brand line (e.g., "MODOCORP MANUFACTURING") in accent color
- Page title (e.g., "Overview") in white, 26px bold
- Subheader describing the page's focus (e.g., "Real-time production metrics, quality, and supply chain performance") in muted light color

Use **height 14** in standard layout (not 7 — taller banners accommodate the subheader and feel more intentional). Content entry settings:

```json
{
  "hideTitle": true, "hideDescription": true, "hideFooter": true,
  "hideBorder": true, "hideMargins": true, "fitToFrame": true,
  "hideWrench": true,
  "style": {"sourceId": "ca8", "textColor": null}
}
```

**Publish one banner design per page** — each with hardcoded title and subtitle. Do NOT share a single banner design across pages (iframe cards cannot receive URL params from the host page). Create 4 separate directories (e.g., `mfg-banner-overview/`, `mfg-banner-production/`) each with a page-specific `index.html` containing hardcoded text, and publish each as a separate design. Then create one card instance per design on the appropriate page via the context API.

### Full-Width Primary Visualization

The primary visualization should span width 60 with height 25-30. On the Overview page, this is typically a time-series line/area chart. On sub-pages, use varied chart types (bar, stacked bar, horizontal bar, scatter, heatmap) — see "Primary Viz Chart Type by Page" above. Content entry settings:

```json
{
  "hideTitle": true, "hideDescription": true, "hideFooter": true,
  "fitToFrame": true, "acceptFilters": true, "acceptDateFilter": true,
  "style": {"sourceId": "ca1", "textColor": null}
}
```

---

## Pro-Code Cards & App Studio Integration

App Studio pages can contain **pro-code custom apps** alongside native cards. A pro-code card is a full JavaScript custom app (built via `initial-build`) published as a Domo card and placed on the canvas.

**When to use pro-code**: Custom visualizations (Gantt, heatmap, org chart), multi-step forms, cross-card interactivity, AppDB CRUD with custom UI, AI features, or any requirement that exceeds native card capabilities. Use `app-studio-pro-code` for the full decision table and build workflow.

### Filter & Variable Integration

Pro-code cards can interact seamlessly with native App Studio page filters and variables:

- **Page filters**: Pro-code cards receive filter changes via `domo.onFiltersUpdated`. Set `acceptFilters: true` on the content entry. See `domo-js` for the filter object shape (`column`, `operand`, `values`, `dataType`).
- **App Studio variables**: Pro-code cards receive variable changes via `domo.onVariablesUpdated`. Variables are keyed by numeric function IDs with values at `parsedExpression.value`.
- **Variable write-back**: Pro-code cards can update variables via `domo.requestVariablesUpdate([{ functionId, value }], onAck, onReply)` — enables dependent dropdown cascades.

When placing a pro-code card, set these content entry properties:

```json
{
  "hideTitle": true, "hideDescription": true, "hideFooter": true,
  "fitToFrame": true, "acceptFilters": true, "acceptDateFilter": true
}
```

For the full build workflow, filter/variable patterns, and layout sizing guidance for pro-code cards, use `app-studio-pro-code`.

---

## Page-Level Filter Cards

Native filter cards (dropdown selectors, date selectors, etc.) provide page-level filtering for all cards on the page. When a user selects a value, Domo's interaction filter system automatically applies the filter to every card that has `acceptFilters: true` in its content entry.

### Creating Filter Cards

Create filter cards with `PUT /content/v3/cards/kpi?pageId=:pageId`, using the appropriate selector chart type.

**Dropdown selector** (filters by a categorical column):

```python
card_body = {
    "definition": {
        "subscriptions": {
            "big_number": {
                "name": "big_number",
                "columns": [{"column": "PlantName", "aggregation": "COUNT",
                             "alias": "PlantName",
                             "format": {"type": "abbreviated", "format": "#A"}}],
                "filters": [],
            },
            "main": {
                "name": "main",
                "columns": [{"column": "PlantName", "mapping": "ITEM"}],
                "filters": [], "orderBy": [],
                "groupBy": [{"column": "PlantName"}],
                "fiscal": False, "projection": False, "distinct": False,
            },
        },
        "formulas": {"dsUpdated": [], "dsDeleted": [], "card": []},
        "annotations": {"new": [], "modified": [], "deleted": []},
        "conditionalFormats": {"card": [], "datasource": []},
        "controls": [],
        "segments": {"active": [], "create": [], "update": [], "delete": []},
        "charts": {"main": {
            "component": "main",
            "chartType": "badge_dropdown_selector",
            "overrides": {
                "allow_multi_select": "true",
                "dropdown_label_text": "Plant",
                "dropdown_label_pos": "Top",
            },
            "goal": None,
        }},
        "dynamicTitle": {"text": [{"text": "Plant", "type": "TEXT"}]},
        "dynamicDescription": {"text": [], "displayOnCardDetails": True},
        "chartVersion": "12", "inputTable": False,
        "noDateRange": False, "title": "Plant", "description": "",
    },
    "dataProvider": {"dataSourceId": "DATASET_UUID"},
    "variables": True, "columns": False,
}
```

**Date selector** (filters by a date column):

```python
# Same structure but with badge_date_selector and no groupBy
"chartType": "badge_date_selector",
"overrides": {},
# main.columns: [{"column": "OrderDate", "mapping": "ITEM"}]
# main.groupBy: []  (empty for date selectors)
# big_number.columns: [{"column": "OrderDate", "aggregation": "MAX", ...}]
```

### Available Selector Chart Types

| Chart type | Purpose | Key override |
|-----------|---------|-------------|
| `badge_dropdown_selector` | Dropdown list filter | `allow_multi_select`, `dropdown_label_text` |
| `badge_date_selector` | Date range picker | — |
| `badge_checkbox_selector` | Checkbox filter (multi-select visible) | — |
| `badge_radio_selector` | Radio button filter (single-select visible) | — |
| `badge_range_selector` | Numeric range slider | — |
| `badge_slicer` | Slicer-style filter | — |

### Filter Card Content Entry (CRITICAL)

**Filter cards MUST be extremely low-profile.** They are controls, not content — they should blend into the page background, not compete visually with hero metrics or charts. NO colored backgrounds, NO bold headers, NO large fonts.

```json
{
  "hideTitle": true,
  "hideDescription": true,
  "hideSummary": true,
  "hideFooter": true,
  "hideTimeframe": true,
  "hideMargins": true,
  "fitToFrame": true,
  "hideBorder": true,
  "acceptFilters": true,
  "acceptDateFilter": true,
  "style": null
}
```

- **`hideSummary: true`** — hides the summary number (e.g., "5K PlantName") that appears above the dropdown. Without this, filter cards display a distracting count.
- **`hideMargins: true`** — removes internal padding for tighter fit.
- **`fitToFrame: true`** — scales the dropdown to fill the card frame.
- **`hideBorder: true`** — removes the card border for a seamless look.
- **`style: null`** — NO style applied. Do NOT use `ca3` or any colored style on filter cards. They should have a transparent/default background that blends with the page. Colored or opaque backgrounds (green, blue, etc.) make filters visually polarizing and distracting.
- **`hideTitle: true`** — hide the card-level title. The dropdown selector already renders its own field label (e.g., "Region", "Status"), so showing the card title creates redundant text. If the card title contains coded prefixes (e.g., "FS-Ov-Reg"), hiding it is essential.

### Filter Card Layout Sizing

Filter cards should be **compact** — they are controls, not content. Use minimal height.

| Template | Width | Height | Notes |
|----------|-------|--------|-------|
| Standard (desktop) | 20 (3 across) or 15 (4 across) | **6** | Minimal height for low-profile appearance |
| Compact (mobile) | 12 (full width, stacked) | **6–8** | Stacked vertically |

**Recommended page layout with filters (CANONICAL — matches pb-apps-initial-build Step 7):**

```
y=0:   Banner (h=14)
y=14:  Filter1 | Filter2 | Filter3 (h=6, w=20 each) — low-profile, transparent
y=20:  Hero metrics row (h=14) — 3-4 badge_pop_multi_value in ONE ROW
y=34:  Header (h=4) — section title
y=38:  Primary Viz (h=30)
y=68:  Header (h=4) — next section title
y=72:  Detail Charts (h=22)
```

### Cross-Dataset Filtering

Filter cards filter all cards on the page that share the same column name, **regardless of dataset**. A `PlantName` dropdown powered by the Work Orders dataset will also filter Quality Inspection cards if they have a `PlantName` column. This enables cross-dataset filtering on overview pages without additional configuration.

For date columns, this only works if the column names match across datasets. If datasets use different date column names (e.g., `OrderDate` vs `InspectionDate`), date selectors filter only cards from the matching dataset.

---

## App Studio Variables

Variables are global values in the Domo instance that function inside Beast Mode calculations. They enable what-if analysis, metric switching, and dynamic controls on dashboards and App Studio pages.

### Creating Variables Programmatically

Variables are created via the same function template API as Beast Modes, with `variable: true` and `global: true`.

**Endpoint**: `POST /query/v1/functions/template?strict=false`

```python
variable_payload = {
    "name": "Selected Plant",
    "locked": False,
    "global": True,
    "expression": "'All'",          # Default value as SQL literal
    "links": [],                     # Empty — variables are not tied to a dataset
    "aggregated": False,
    "analytic": False,
    "nonAggregatedColumns": [],
    "dataType": "STRING",            # STRING, DECIMAL, LONG, DATE
    "status": "VALID",
    "cacheWindow": "non_dynamic",
    "columnPositions": [],
    "functions": [],
    "functionTemplateDependencies": [],
    "archived": False,
    "hidden": False,
    "variable": True,                # CRITICAL — makes this a Variable, not a Beast Mode
}

resp = requests.post(
    f"{BASE}/query/v1/functions/template?strict=false",
    headers=HEADERS, json=variable_payload, timeout=15)

data = resp.json()
function_id = data["id"]        # e.g., 115511 — numeric ID for pro-code integration
legacy_id = data["legacyId"]    # e.g., "calculation_abc123..." — for Beast Mode references
```

**Variable data types:**

| dataType | expression example | Use case |
|----------|-------------------|----------|
| `STRING` | `"'All'"` | Dropdown selections, text filters |
| `DECIMAL` | `"95"` | Thresholds, percentages, what-if values |
| `LONG` | `"100"` | Integer counts, limits |
| `DATE` | `"'2026-01-01'"` | Date selections |

The `function_id` (numeric, e.g., `115511`) is used by pro-code apps:
- Read: `domo.onVariablesUpdated(vars => vars["115511"]?.parsedExpression?.value)`
- Write: `domo.requestVariablesUpdate([{ functionId: 115511, value: "Plant A" }])`

### Variable Controls — App Studio Editor (Manual Steps Required)

**Variable Controls cannot be added programmatically.** The layout API only supports `CARD`, `HEADER`, `SPACER`, `SEPARATOR`, and `PAGE_BREAK` content types. Variable Controls must be configured through the App Studio editor UI.

After creating variables via the API, instruct the user to complete these steps in the App Studio editor:

1. **Open the app** in App Studio editor (Apps Home → hover app → More → Edit)
2. **Navigate to the target page** using the page tabs at the bottom
3. **Open the left toolbar** and click the **Controls** icon (slider/knob icon)
4. **Drag a control type** onto the canvas:
   - **Dropdown** — for string variables with discrete choices
   - **Range Selector** — for numeric variables (thresholds, targets)
   - **Date Selector** — for date variables
   - **Radio Button / Checkbox** — for small option sets
5. **In the control configuration panel** (right side):
   - Select the **Variable** to bind (e.g., "Selected Plant")
   - Configure available values (from a dataset column or manual list)
   - Set the default value
6. **Position the control** on the canvas (recommended: in the filter row between heroes and charts)
7. **Save the app**

To persist variable values across pages, configure persistent filters:
1. Go to **App Configuration** → **Filter Options** tab
2. Check **"Persist Variable controls"**
3. Note: Variable controls only apply to pages that contain that control. Add the control to each page where persistence is needed.

### Variables vs Filter Cards

Both provide page-level interactivity, but they work differently:

| Feature | Filter Cards | Variables |
|---------|-------------|-----------|
| Creation | Fully programmatic (API) | Programmatic creation + manual UI binding |
| Mechanism | Interaction filter system | Beast Mode calculation system |
| Cross-card | Automatic (same column name) | Requires Beast Mode on each card |
| Pro-code API | `domo.onFiltersUpdated` | `domo.onVariablesUpdated` |
| Use case | Column-based filtering | What-if analysis, metric switching, calculated parameters |
| Persistence | Built-in page-level | Configurable via persistent filters |

**Recommendation**: Use **filter cards** for straightforward column filtering (Plant, Status, Date Range). Use **variables** for calculated parameters (threshold %, metric selector, aggregation granularity) and when pro-code apps need to read/write shared state.

---

## Design-Aware Layout

These rules make layouts feel intentional rather than mechanically packed. For detailed layout density presets and spacing examples, see [layout-design.md](layout-design.md).

### Breathing Room

Insert SPACERs to create visual separation between card groups. Without intentional whitespace, layouts feel cramped.

| Spacing purpose | Element | Height |
|----------------|---------|--------|
| Top of page (before first content) | SPACER | 3 |
| Between cards in the same section | (none — cards touch) | 0 |
| Between card rows within a section | (implicit from y positioning) | 0 |
| Between sections (before a HEADER) | SPACER | 5 |
| After a section header | (none — cards start at y + header height) | 0 |
| After filter row (before main content) | SEPARATOR | 2 |

### Row Harmony

Cards on the same grid row should use the same height. Mixed heights on a row (e.g., KPI at height 10 next to a chart at height 22) create a ragged bottom edge. When mixing card types on a row, either use the taller card's height for all items, or separate them into distinct rows.

### Visual Weight Distribution

Place cards in this order top-to-bottom: filters, then KPIs/summary numbers, then charts, then tables. This mirrors the natural reading pattern — controls first, summary second, detail last. Each tier represents increasing information density.

### Section Title Quality

HEADER content items should use concise, specific text. Avoid generic labels like "Overview" or "Metrics" — use labels that tell the reader what the data answers, e.g., "Revenue by Region", "Pipeline Health", "Monthly Trend".

### Layout Density Presets

Choose a density tier based on the audience and page purpose:

| Preset | Cards/page | Card widths | Spacer usage | Audience |
|--------|-----------|-------------|--------------|----------|
| **Executive** | 4–8 | 20–30 | Generous (height 5 spacers) | C-suite, board decks |
| **Operational** | 8–16 | 15–20 | Moderate (height 3 spacers) | Managers, daily use |
| **Detailed** | 16+ | 10–15 | Minimal (height 2 spacers) | Analysts, drill-down |

### Style ID Usage

Apply `style.sourceId` in the content array to differentiate card types visually. Use a consistent pattern across all pages:

- **Filter cards**: no style (default) — keeps them visually neutral
- **KPI / summary cards**: a contrasting style to draw attention
- **Chart / table cards**: a uniform style for the detail tier

Apply the same style mapping on every page in the app for visual consistency. The same card can have different styles on different pages, but keeping them consistent across pages reduces cognitive load.

---

## Theme Management

The `theme` object inside the app controls all visual styling — colors, fonts, card styles, navigation appearance, page background, and layout density. It is updated via the full-body `PUT /content/v1/dataapps/:dataAppId?includeHiddenViews=true` endpoint.

### Theme Structure

```json
{
  "theme": {
    "name": "My Theme",
    "colors": [...],
    "fonts": [...],
    "cards": [...],
    "tables": [...],
    "navigation": [...],
    "pages": [...],
    "buttons": [...],
    "tabs": [...],
    "forms": [...],
    "notebooks": [...],
    "components": [...],
    "pills": [...],
    "headers": [...],
    "app": { "backgroundColor": {...}, "resizeMode": "AUTO" }
  }
}
```

### Custom Color Palette (NEVER use Domo native colors)

**CRITICAL: Never use Domo's native/default color palette.** Always select a curated palette from `domo-app-theme/color-palettes.md`. This file contains 50 perceptually-uniform OKLCH palettes across 9 harmony types (Analogous, Monochromatic, Triad, Complementary, Split Complementary, Square, Compound, Shades, Signature). Pick the palette that best suits the use case and data domain, or ask the user for preference.

#### Palette Selection Workflow

1. Read `domo-app-theme/color-palettes.md` and review the harmony type table to identify the best fit for the dashboard's data story
2. Select a specific palette (e.g., "Pacific Drift" for corporate analytics, "Mineral" for manufacturing/industrial)
3. The palette provides 6 OKLCH series colors (`--c1` through `--c6`)
4. **For pro-code CSS**: use the OKLCH values directly
5. **For native card `series_N_color` overrides**: convert OKLCH to uppercase hex (use Python `coloraide` or a quick conversion script)
6. **For App Studio theme slots**: map the palette's 6 colors to the c8/c22/c29/c36 series positions as hex, and derive neutral/semantic scales from the `domo-app-theme` base CSS properties

#### Palette Structure for App Studio

App Studio's theme has 60 color slots (`c1`–`c60`) organized by tag group. Map your custom palette following this structure:

| Slot range | Tag | Purpose | Example mapping |
|-----------|-----|---------|-----------------|
| c1–c7 | TINTED_GRAY | Neutral grayscale dark→light | neutral-950, 900, 600, 300, 200, 100, white |
| c8–c14 | PRIMARY (ORDER_SOURCE at c8) | Brand series base→tints | brand-500, 400, 300, 200, 100, 50, 50 |
| c15–c21 | PRIMARY | Brand darker shades | brand-600→950 |
| c22–c28 | SECONDARY (ORDER_SOURCE at c22) | 2nd series base→tints | teal-600→50 |
| c29–c35 | TERTIARY (ORDER_SOURCE at c29) | 3rd series base→tints | amber-600→50 |
| c36–c42 | QUATERNARY (ORDER_SOURCE at c36) | 4th series base→tints | red-600→50 |
| c43–c57 | GRAYSCALE | Nav/sidebar/text/borders dark→light | neutral-950→white |
| c58–c59 | FONT | Dark/light font | neutral-950, white |
| c60 | AUTOMATIC_COLOR | Do NOT modify | Automatic dark/light switching |

**Colors**: Update via `color_entry['value'] = {'value': '#HEX', 'type': 'RGB_HEX'}`. All hex values **MUST be uppercase**. Skip `c60`.

#### Chart Color Palette (`chartColorPalette`)

The theme's `c8-c42` color slots control UI chrome (nav, pills, buttons, backgrounds) but **NOT chart series colors**. Chart series colors are controlled exclusively by the `chartColorPalette` theme field.

**`chartColorPalette`** accepts only `{"id": "<palette name>", "type": "DOMO"}` where the palette name references a Brand Kit chart color palette. The only built-in valid name is `"Domo Default Palette"`. Setting an unrecognized name results in `null` (charts fall back to theme color families c8/c15/c22/c29/c36 or hardcoded defaults).

**To apply custom chart colors to native App Studio cards:**

1. **Preferred: Create a Brand Kit palette** through the Domo Admin UI (Admin > Brand Kit > Chart Colors > New Palette). Use the same brand/teal/amber/red hex values from the custom palette. After creating and activating it, reference its name in the theme:
   ```python
   theme['chartColorPalette'] = {'id': '<Brand Kit Palette Name>', 'type': 'DOMO'}
   ```

2. **Fallback: Set chartColorPalette to null** by using an invalid name (`{'id': 'Custom', 'type': 'DOMO'}`). Charts may fall back to the theme's color families (c8, c15, c22, c29, c36).

**Important:** The `chartColorPalette` field does NOT accept `type: "CUSTOM"` with inline colors — the API returns `400 Bad Request`. There is no public API for programmatic Brand Kit palette creation; it must be done through the Admin UI.

3. **Most reliable: Set series colors per card via overrides.** Use `PUT /content/v3/cards/kpi/:cardId` to set `series_1_color` through `series_8_color` in the chart `overrides` object. This works for ALL chart types and guarantees the custom palette appears regardless of Brand Kit settings.

   ```python
   SERIES_COLORS = ['#3B82C8', '#0D9488', '#D97706', '#DC2626',
                    '#2661A3', '#059669', '#7C3AED', '#DB2777']
   
   # Read card → fix format mismatches → add overrides → update
   for i, color in enumerate(SERIES_COLORS, 1):
       overrides[f'series_{i}_color'] = color
   ```

   **Gotcha — Read/Write format mismatches:** The READ endpoint (`PUT /content/v3/cards/kpi/definition`) returns simplified formats that the WRITE endpoint rejects. You MUST fix these before updating:
   - `formulas`: read returns `[]` → write needs `{"dsUpdated": [], "dsDeleted": [], "card": []}`
   - `conditionalFormats`: read returns `[]` → write needs `{"card": [], "datasource": []}`
   - `annotations`: read returns `[]` → write needs `{"new": [], "modified": [], "deleted": []}`
   - `segments`: read has `{"active": [], "definitions": []}` → write needs `{"active": [], "create": [], "update": [], "delete": []}`
   - Must add missing fields: `title`, `description`, `noDateRange`
   - Must remove read-only fields: `modified`, `allowTableDrill`
   - Must provide `dataProvider.dataSourceId` (read returns it as `None` in subscriptions)

#### Decision Rules for Palette Selection

- Prefer restrained, modern palettes: calm neutrals + one strong accent
- Use the neutral scale for background, surface, border, muted text (NOT brand color)
- Choose brand hue that works across multiple shades
- Reject palettes that look good as swatches but fail in cards/buttons/headings
- For light mode: default to light backgrounds; chart series ORDER_SOURCE colors (c8, c22, c29, c36) must have sufficient contrast on white backgrounds
- For dark mode: use the dark mode palettes from `domo-app-theme/color-palettes.md` and follow the dark mode theme rules below

#### Dark Mode Theme (CRITICAL — `c60` Font Color Override)

When building an App Studio app with a **dark background** (dark page bg, dark card surfaces), Domo's `c60` AUTOMATIC_COLOR **does not reliably detect dark backgrounds** and defaults to dark text — making ALL native element text invisible. This is the #1 dark mode failure.

**Root cause**: `c60` is an `AUTOMATIC_COLOR` with `dark` → `c58` and `light` → `c59` variants. The Clarion theme treats itself as "light mode" regardless of actual background colors, so it always picks `c59` (dark text). On dark backgrounds, this produces invisible text on cards, navigation, headers, filters, and components.

**MANDATORY fix — replace ALL `c60` font color references with `c58`:**

```python
# c58 must be set to your light text color (e.g., #F5F3F0 for warm white)
LIGHT_TEXT_REF = {"value": "c58", "type": "COLOR_REFERENCE"}

# Card styles: fontColor
for card in theme.get('cards', []):
    if isinstance(card.get('fontColor'), dict) and card['fontColor'].get('value') == 'c60':
        card['fontColor'] = dict(LIGHT_TEXT_REF)

# Navigation: titleFontColor, linkFontColor
for nav in theme.get('navigation', []):
    for key in ['titleFontColor', 'linkFontColor']:
        if isinstance(nav.get(key), dict) and nav[key].get('value') == 'c60':
            nav[key] = dict(LIGHT_TEXT_REF)

# Headers: fontColor
for h in theme.get('headers', []):
    if isinstance(h.get('fontColor'), dict) and h['fontColor'].get('value') == 'c60':
        h['fontColor'] = dict(LIGHT_TEXT_REF)

# Components: ALL font color properties
for comp in theme.get('components', []):
    for key in ['titleFontColor', 'descriptionFontColor', 'title1FontColor',
                'title2FontColor', 'contentFontColor', 'labelDescriptionFontColor']:
        if isinstance(comp.get(key), dict) and comp[key].get('value') == 'c60':
            comp[key] = dict(LIGHT_TEXT_REF)

# Forms, tables, notebooks, pills, tabs — recursively replace c60
for section in ['forms', 'tables', 'notebooks', 'pills', 'tabs']:
    for item in theme.get(section, []):
        for key, val in item.items():
            if isinstance(val, dict) and val.get('type') == 'COLOR_REFERENCE' and val.get('value') == 'c60':
                item[key] = dict(LIGHT_TEXT_REF)
```

**Dark mode color slot mapping** (inverted from light mode):

| Slot | Light mode | Dark mode |
|------|-----------|-----------|
| c1–c7 | dark→light grays | light→dark (c1=page bg dark, c5=text light, c7=white) |
| c43–c54 | dark nav/sidebar grays | dark backgrounds matching page bg |
| c55 | page bg (ultra-light gray) | page bg (**dark**, e.g., #1E1C1A) |
| c56 | card surface (white) | card surface (**dark**, e.g., #302C28) |
| c58 | dark font | **light font** (e.g., #F5F3F0) — primary text on dark bg |
| c59 | light/white font | **dark font** (e.g., #1E1C1A) — inverse text |

**Dark mode sidebar colors** — match the banner gradient:
```python
for c in theme['colors']:
    if c['id'] == 'c43': c['value'] = {'value': '#1E1C1A', 'type': 'RGB_HEX'}  # nav bg
    if c['id'] == 'c44': c['value'] = {'value': '#302C28', 'type': 'RGB_HEX'}  # nav hover
    if c['id'] == 'c45': c['value'] = {'value': '#3A3632', 'type': 'RGB_HEX'}  # nav active
```

**Font**: Use `Sans` family throughout (not `Slab`). Map to domo-app-theme typography:

| Font ID | Role | Family | Weight | Size |
|---------|------|--------|--------|------|
| f1 | Page title | Sans | 700 | 22 |
| f2 | Header h1 | Sans | 700 | 22 |
| f3 | Section title | Sans | 600 | 16 |
| f4 | Card title | Sans | 600 | 16 |
| f5 | Body semibold | Sans | 600 | 13 |
| f6 | Body text | Sans | 400 | 13 |
| f7 | Captions | Sans | 400 | 12 |
| f8 | Button text | Sans | 600 | 13 |
| f9 | Small/badge | Sans | 600 | 11 |

### Border Radius — ZERO EVERYWHERE (MANDATORY)

**All border-radius values MUST be 0.** No rounded corners on any element — cards, containers, buttons, inputs, filters, tables, notebooks, components, tabs, forms, or pills. This is a strict global rule.

| Element | Radius | Notes |
|---------|--------|-------|
| Cards (`borderRadius`) | **0** | Zero rounding on all card styles |
| Tables (`borderRadius`) | **0** | Zero rounding |
| Notebooks (`borderRadius`) | **0** | Zero rounding |
| Components outer (`borderRadius`) | **0** | Zero rounding |
| Components inner (`itemBorderRadius`) | **0** | Zero rounding |
| Buttons (`borderRadius`) | **0** | Zero rounding |
| Tabs (`borderRadius`) | **0** | Zero rounding |
| Forms (`borderRadius`) | **0** | Zero rounding |
| Pills (`radius`) | **0** | Zero rounding |

```python
# Apply zero border-radius to ALL theme elements
for card in theme.get('cards', []):
    card['borderRadius'] = 0
    if 'itemBorderRadius' in card:
        card['itemBorderRadius'] = 0
for table in theme.get('tables', []):
    table['borderRadius'] = 0
for notebook in theme.get('notebooks', []):
    notebook['borderRadius'] = 0
for component in theme.get('components', []):
    component['borderRadius'] = 0
    if 'itemBorderRadius' in component:
        component['itemBorderRadius'] = 0
for button in theme.get('buttons', []):
    button['borderRadius'] = 0
for tab in theme.get('tabs', []):
    tab['borderRadius'] = 0
for form in theme.get('forms', []):
    form['borderRadius'] = 0
for pill in theme.get('pills', []):
    pill['borderRadius'] = 0
    if 'radius' in pill:
        pill['radius'] = 0
```

### Card Styles (ca1–ca8) — Reference Configuration (MANDATORY)

All card styles MUST follow this reference configuration. Zero border-radius, zero border weight, zero padding, no drop shadow, no content spacing:

```python
# ca1–ca7 — clean surface, zero chrome (default for all content cards)
for card in theme.get('cards', []):
    card['borderRadius'] = 0
    card['borderWidth'] = 0
    card['dropShadow'] = 'NONE'
    card['dropShadowColor'] = None
    card['padding'] = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
    card['contentSpacing'] = None       # "Card content spacing: Nil"
    card['headerBottomSpacing'] = 0     # "Space below header content: 0"
```

Keep ca8 as fully transparent/borderless for banners and pro-code frames:

```python
# ca8 — transparent frame (banners, pro-code containers)
card['backgroundColor'] = {'value': 'c56', 'opacity': '00', 'type': 'COLOR_REFERENCE'}
card['borderWidth'] = 0
card['borderRadius'] = 0
card['dropShadow'] = 'NONE'
card['padding'] = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
```

**Reference card settings (from App Studio design panel):**

| Setting | Value | API property |
|---------|-------|-------------|
| Rounded corners | **0 px** | `borderRadius: 0` |
| Border weight | **0 px** | `borderWidth: 0` |
| Drop shadow | **None** | `dropShadow: 'NONE'` |
| Controls color | **#2563BE** | Theme color `c8` → `#2563BE` |
| Card inner padding | **Custom, 0 px** | `padding: {left:0, right:0, top:0, bottom:0}` |
| Card content spacing | **Nil** | `contentSpacing: None` (null) |
| Space below header content | **0 px** | `headerBottomSpacing: 0` |

### Controls Color

Set the controls/accent color to `#2563BE`:
```python
for c in theme.get('colors', []):
    if c['id'] == 'c8':
        c['value'] = {'value': '#2563BE', 'type': 'RGB_HEX'}
```

### Card Padding Constraint

Card padding values have a **maximum of 16**. Setting `padding` values above 16 causes `400 Bad Request`. Use `{'left': 0, 'right': 0, 'top': 0, 'bottom': 0}` by default (zero padding is the standard).

### Fixed-Width Layout (MANDATORY)

**All App Studio apps MUST use fixed-width layout.** Auto-width is never acceptable. Set **both**:

1. **Theme-level**: `theme.pages[0].isDynamic = false` and `theme.pages[0].density = {'compact': 8, 'standard': 8}`
2. **Page-level**: Each page layout's `isDynamic` (via layout PUT) should also be `false`

```python
# Fixed-width — ALWAYS apply this
for page in theme.get('pages', []):
    page['isDynamic'] = False
    page['density'] = {'compact': 8, 'standard': 8}
```

The theme-level setting controls the default; page-level can override.

### Sidebar–Banner Color Tie

When using a dark gradient banner, tie the sidebar/navigation background to the same color palette. The nav theme uses color references `c43` (background), `c44` (hover), `c45` (active). Set these to match the banner's gradient endpoints:

```python
# Banner gradient: oklch(0.280 0.020 256) → oklch(0.374 0.014 256)
# ≈ #2A2E35 → #3F454D
for c in theme['colors']:
    if c['id'] == 'c43': c['value'] = {'value': '#2A2E35', 'type': 'RGB_HEX'}  # nav bg
    if c['id'] == 'c44': c['value'] = {'value': '#353A42', 'type': 'RGB_HEX'}  # nav hover
    if c['id'] == 'c45': c['value'] = {'value': '#3F454D', 'type': 'RGB_HEX'}  # nav active
```

This creates visual continuity between the sidebar and page banners. Always do this when building apps with dark banner headers.

### Navigation Icons

Icons are set via the `/navigation/reorder` endpoint. The body must be the **full navigation array** as returned by GET — partial payloads cause `400 Bad Request`.

**HOME icon**: Always set `icon.value = "home"` for the HOME navigation item.

**WARNING**: Google Material icon names (`monetization_on`, `trending_up`, `inventory_2`, `assignment_return`) do NOT render in Domo's left nav. Domo uses its own internal icon set. **ONLY use icons from the catalog below.** If an icon name is wrong, the nav item renders with no visible icon (blank space).

#### Recommended icons by page type

| Page type | Recommended icons (pick one) |
|-----------|------------------------------|
| Overview / Dashboard | `analytics`, `pop-chart`, `chart-bar-vertical`, `select-chart`, `badge-layout-8` |
| Production / Operations | `gauge`, `dataflow`, `cube-filled`, `completed-submissions` |
| Quality / Compliance | `certified`, `checkbox-marked-outline`, `check-in-icon`, `approval-center` |
| Supply Chain / Logistics | `globe`, `data-app`, `local_shipping`, `warehouse`, `shopping_cart` |
| Retail / Store | `store`, `cube-filled`, `numbers`, `toolbox` |
| Financial | `money-universal`, `money`, `benchmark`, `books`, `calculator` |
| People / HR / Patients | `people`, `person`, `person-card`, `person-plus`, `people-plus`, `heart` |
| Time / Scheduling | `clock`, `calendar-simple`, `calendar-time`, `alarm`, `interrupting-timer` |
| Documents / Reports | `document`, `document-outline`, `books`, `newspaper`, `clipboard-copy` |
| AI / ML / Intelligence | `ai-chat`, `magic`, `wand`, `lightbulb`, `lightning-bolt`, `sciency-data`, `analyzer` |
| Marketing / Campaigns | `area-chart`, `funnel`, `bell-outline`, `video`, `image` |
| Settings / Admin | `controls`, `pages-gear`, `code-tags`, `pencil-box`, `lock-closed` |
| Geography / Location | `globe`, `map-marker`, `building` |
| Forecasting / Goals | `forecast`, `goals`, `trophy`, `exclamation-triangle` |
| Education | `graduation-cap`, `domo-university` |
| Health / Safety | `heart`, `glasses`, `adc` |
| Inventory / Products | `cube-filled`, `domobox`, `table`, `tag-multiple`, `badge-layout-small` |

#### Complete Domo icon catalog (133 verified names)

Scanned from 100+ live App Studio apps. Every name below is confirmed to render correctly:

```
abc                    adc                    ai-chat                airplane
alarm                  align-center-icon      align-left-icon        analytics
analyzer               approval-center        approval-center-alt    appstore
area-chart             arrow-box              arrow-merge            arrow-right-circle
arrow-up-circle        avatar                 axis                   badge-layout-8
badge-layout-medium    badge-layout-mixed     badge-layout-small     bell-outline
benchmark              beta                   books                  building
calculator             calendar-simple        calendar-time          camera
card-notebook          card-poll              cell-phone             certified
certified-company      chart-bar-vertical     chart-line             chart-properties
check-in-icon          checkbox-marked-outline clipboard-copy        clock
code-tags              color                  completed-submissions  controls
cube-filled            dashboard              data-app               data-science
database               dataflow               document               document-outline
domo                   domo-university        domobox                dot-plot-chart
dots-vertical          drill                  exclamation-triangle   flag
forecast               format-list-checks     funnel                 funnel-strike
gauge                  glasses                globe                  goals
graduation-cap         handshake              heart                  home
image                  inbox-full             interrupting-timer     lightbulb
lightning-bolt         link                   local_shipping         lock-closed
magic                  map-marker             marker                 money
money-universal        newspaper              non-interrupting-timer numbers
pages                  pages-bars             pages-chart            pages-gear
paperclip              pencil                 pencil-box             people
people-plus            person                 person-card            person-plus
phone                  play-circle-outline    pop-chart              presentation
question-circle        ringing-bell           sandcastle             sciency-data
search                 seeding                select-chart           shopping_cart
smile                  store                  sync                   table
table-column           tag-multiple           tag-vertical           toolbox
trophy                 variable               video                  wand
warehouse              workflow               workspace              x-circle
your-submissions
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
| **LEFT nav requires `showDomoNavigation: false`** | Setting `navOrientation` to `LEFT` while `showDomoNavigation` is `true` causes `400 Bad Request`. All LEFT-nav apps in production have `showDomoNavigation: false`. Set both in the same PUT. |
| **View creation body format** | `POST /content/v1/dataapps/:id/views` requires the `view` sub-object directly as the body — NOT wrapped in `{"view": {...}}` or `{"title": "..."}`. The body must include `type: "dataappview"`, `title`, `pageName`, and an `owners` array. |
| **App PUT requires full body** | The `PUT /content/v1/dataapps/:id` endpoint rejects partial bodies with `400 Bad Request`. You must send the complete app object from GET. Read-only fields like `userAccess`, `isOwner`, `isFavorite`, `canEdit` are safely ignored by the server. |
| **New apps have `isDynamic: false`** | Newly created App Studio apps have `isDynamic: false` in their layout (unlike apps created via the UI which may have `isDynamic: true`). This does not affect layout operations. |
| **New apps have `enabled: true`** | Newly created apps include an `enabled` field in the layout response. Preserve this when PUTting updates. |
| **Style is per-content-entry** | Card styles (`"style": {"sourceId": "ca8"}`) are set in the `content` array, not in the template. The same card can have different styles on different pages. |
| **No card duplication** | Adding the same card to multiple pages doesn't duplicate it — it's the same card rendered on each page. Filter interactions are shared. |
| **GET uses `/layouts` (plural)** | The GET endpoint is `/content/v4/pages/{pageId}/layouts` (plural), but the PUT endpoint is `/content/v4/pages/layouts/{layoutId}` (singular with layout ID in path). |
| **DELETE removes card from page only** | `DELETE /content/v1/pages/{pageId}/cards/{cardId}` removes the card-page association, not the card itself. The card continues to exist in Domo and on other pages. |
| **Overview page is `-100000`** | The Domo overview/home page has the special page ID `-100000`. Adding cards to it works with the same `POST /content/v1/pages/-100000/cards/{cardId}` endpoint. |
| **Cards on overview != cards in App Studio** | Adding a card to page `-100000` puts it on the Domo overview page. It does NOT appear inside App Studio views. To have cards in App Studio, add them to the specific view `pageId`. These are independent assignments. |
| **Cards from different datasets on same page** | An App Studio page can contain cards powered by different datasets. There is no restriction. This was verified with a page containing 23 cards across 2 datasets. |
| **Hex values MUST be uppercase** | Color hex values in the theme (e.g., `#3F454D`) must use uppercase letters. Lowercase hex (e.g., `#3f454d`) causes `400 Bad Request` on PUT. |
| **Card padding max is 16** | Card `padding` values (left/right/top/bottom) cannot exceed 16. Values like 20 cause `400 Bad Request`. Use 16 for maximum padding. |
| **Nav reorder requires full array** | The `/navigation/reorder` endpoint requires the complete navigation array as returned by GET. Sending a subset or partial objects causes `400`. **CRITICAL: You MUST preserve all default system nav items** (HOME, AI_ASSISTANT, CONTROLS, DISTRIBUTE, MORE/Details) when reordering. First GET the app to read `navigations[]`, then modify only the `icon` and `navOrder` fields — never drop items. Missing system items makes the app uneditable from the UI. **If HOME is missing from the navigations array (some new apps don't include it by default), add it explicitly**: `{"entity": "HOME", "title": "Home", "icon": {"type": "NAME", "value": "home"}, "visible": true}`. Without HOME, users cannot navigate back to the Domo portal. |
| **Theme pages[0].isDynamic controls fixed width** | Setting `theme.pages[0].isDynamic = false` with `density: {'compact': 8, 'standard': 8}` creates a fixed-width layout. This is independent of per-page layout `isDynamic`. |
| **LEFT nav: hide title and logo** | For `navOrientation: 'LEFT'`, set `showTitle: false` and `showLogo: false`. The page names in the left nav already identify the app — the title wastes vertical space. |
| **Sidebar color must match banner** | When using a dark gradient banner, update `c43`/`c44`/`c45` to match the banner's gradient palette. Mismatched sidebar and banner colors break visual continuity. |
| **Pro-code cards: no own shadow** | Pro-code apps embedded in App Studio should set `background: transparent` and no `box-shadow`. The App Studio card style (ca1) provides the card chrome. Duplicate shadows create a double-border effect. |
| **Daily tick density** | Time-series pro-code charts with >30 data points must thin ticks using an interval formula. Target ~18 visible labels. See `app-studio-pro-code` for the `calcTickInterval` function. |
| **Banner height = 14** | Banners should use height 14 (not 7) in standard template to accommodate subheader text. Compact: height 8. |
| **Dark mode: c60 invisible text** | `c60` (AUTOMATIC_COLOR) does NOT reliably detect dark card/page backgrounds. On dark themes, it defaults to dark text — making ALL native text invisible. **MANDATORY**: Replace every `c60` font color reference across cards, navigation, headers, and components with `c58` (your light text color). See "Dark Mode Theme" section. This is the #1 dark mode failure. |
| **Dark mode: font property names** | Theme font properties use `family`, `weight`, `size`, `style` (not `fontFamily`/`fontWeight`/`fontSize`). Setting the wrong property names silently fails — fonts revert to theme defaults on next GET. |
| **Pro-code colors are NOT inherited** | Pro-code components render in iframes and use their own CSS — they do NOT inherit the App Studio theme colors. When the theme palette changes, every pro-code component (banners, charts) must be manually updated with the new hex values AND republished via `domo publish`. Forgetting this creates jarring green-charts-on-copper-theme mismatches. |
| **Font family must match across all surfaces** | The App Studio theme `fonts[].family` (Sans/Serif/Slab) must match all pro-code CSS `font-family` stacks. Mixing Serif native cards with Sans pro-code charts looks broken. When updating fonts, update BOTH the theme AND every pro-code `app.css`. |
| **Nav icons: use only catalog names** | Domo uses its own internal icon set (133 verified names). Google Material icon names like `inventory_2`, `assignment_return`, `trending_up` render as blank/invisible. See the "Complete Domo icon catalog" section above. Always pick from the verified catalog. |

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

