# Domo App Studio — Advanced (CLI Edition)

This is the full App Studio reference converted to use `community-domo-cli` commands instead of
raw `curl`/`requests` API calls. All operational examples use CLI. Reference material (layout
structure, card styles, theme management, design patterns, gotchas) is preserved in full.

For the lightweight operational-only version, see `basic-app-studio`.

> **CUSTOM PALETTE REQUIRED**: Never use Domo's native/default color palette. Always select a curated palette from `domo-app-theme/color-palettes.md` (50 OKLCH palettes across 9 harmony types). Pick a palette suited to the use case or ask the user. Use OKLCH values in pro-code CSS; convert to hex for native card `series_N_color` overrides. All App Studio theme colors, pro-code chart colors, banner colors, and card styling must use the chosen palette. See "Custom Color Palette" section under Theme Management.

> **Status**: Reverse-engineered from live testing, March 2026
> **Verified against**: `aeroateam-partner.domo.com` (app `453445400`), `csibas.domo.com` (apps `1400847176`, `2061524048`), `modocorp.domo.com`

---

## Authentication

Run once per instance. No manual token or header management needed after this.

```bash
domo login -i myinstance.domo.com
```

The CLI reads the saved session automatically on every command. Set a default instance so you
don't have to pass `--instance` every time:

```bash
community-domo-cli config set-profile --name default --instance myinstance --make-default
```

All examples below assume a default profile is set. If not, prepend
`--instance myinstance.domo.com` to every command.

---

## CLI Conventions

```bash
# Global flags come BEFORE the subcommand group
community-domo-cli --output json --instance myco app-studio get 12345

# Mutating commands require --yes (-y) to skip confirmation
community-domo-cli -y app-studio create --body-file app.json

# Dry-run shows the exact HTTP request without executing
community-domo-cli --dry-run app-studio layout-set $APP_ID $VIEW_ID --body-file layout.json

# Capture JSON output for scripting
APP_ID=$(community-domo-cli --output json app-studio create --body '{"title":"My App"}' -y \
  | python3 -c "import json,sys; print(json.load(sys.stdin)['dataAppId'])")
```

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

Creates a new App Studio app with a single default landing view.

```bash
community-domo-cli --output json -y app-studio create \
  --body '{"title": "My Dashboard App", "description": "Description of the app"}' \
  > app_response.json

APP_ID=$(python3 -c "import json; print(json.load(open('app_response.json'))['dataAppId'])")
PAGE_ID=$(python3 -c "import json; print(json.load(open('app_response.json'))['landingViewId'])")
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

## App Operations

### Get App Structure

Returns all views, navigation, theme, and app-level settings.

```bash
community-domo-cli --output json app-studio get $APP_ID > app.json
```

Views are embedded in the response under `views[]`. Each view has `viewId`, `title`,
`visible`, `viewOrder`. The `viewId` == `pageId` for all card and layout operations.

**Note**: `GET /content/v1/dataapps/:id/views` is a dead endpoint (405). Always use
`app-studio get` and read the `views[]` array from the response.

### Update App Configuration

The full GET → modify → PUT flow using the CLI:

```bash
# 1. GET current state
community-domo-cli --output json app-studio get $APP_ID > app.json

# 2. Modify in place (Python example — change nav orientation)
python3 -c "
import json
app = json.load(open('app.json'))
app['navOrientation'] = 'LEFT'
app['showDomoNavigation'] = False   # REQUIRED when navOrientation=LEFT
app['showTitle'] = False            # Recommended for LEFT nav
app['showLogo'] = False             # Recommended for LEFT nav
json.dump(app, open('app_updated.json', 'w'))
"

# 3. PUT updated app (CLI automatically sends ?includeHiddenViews=true)
community-domo-cli --output json -y app-studio update $APP_ID \
  --body-file app_updated.json > app_updated_response.json
```

**Key fields changeable via update**:


| Field                | Values                  | Notes                                                                                                                                                     |
| -------------------- | ----------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `navOrientation`     | `TOP`, `LEFT`, `BOTTOM` | Controls nav bar position                                                                                                                                 |
| `showDomoNavigation` | `true`, `false`         | **Must be `false` when `navOrientation` is `LEFT`** — the API rejects LEFT + showDomoNavigation=true                                                      |
| `showNavigation`     | `true`, `false`         | Whether nav is visible at all                                                                                                                             |
| `showTitle`          | `true`, `false`         | Show app title in nav bar. **Set to `false` for LEFT nav** — the title wastes vertical space and the page names in the left nav already identify the app. |
| `showLogo`           | `true`, `false`         | Show Domo logo. **Set to `false` for LEFT nav** — keeps the nav clean.                                                                                    |
| `title`              | string                  | App title                                                                                                                                                 |
| `description`        | string                  | App description                                                                                                                                           |
| `iconDataFileId`     | integer | null          | Custom app icon (tile/launcher). Set via Data File upload (see below).                                                                                    |
| `navIconDataFileId`  | integer | null          | Custom icon shown in the left-nav sidebar. Usually set to the same value as `iconDataFileId`.                                                             |


The PUT does NOT add or modify views/navigations — use the dedicated endpoints below for those.

### Custom App Icon

Every App Studio app **must** have a custom icon. Never leave the default placeholder.

**Step 1 — Generate a 256x256 PNG icon** using Pillow (or accept a user-provided image). The icon should visually represent the app's domain using the app's custom brand color palette.

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

**Step 2 — Upload via CLI**

```bash
community-domo-cli --output json -y files upload --file-path icon.png > icon_response.json
DATA_FILE_ID=$(python3 -c "import json; print(json.load(open('icon_response.json'))['dataFileId'])")
```

**Step 3 — Set on the app** (include in the GET->modify->PUT flow):

```python
app['iconDataFileId']    = data_file_id
app['navIconDataFileId'] = data_file_id  # same file for both
```

**Note**: The CLI uses `mimetypes.guess_type()` for content type. PNG files are correctly
detected as `image/png`. The CLI does not send `?name=&public=true` query params — the
`dataFileId` is still returned and works for icon assignment.

**Gotchas:**

- `Content-Type` must be `image/png` (not `application/octet-stream`) or the upload returns `415`.
- The PUT must send the **full app object** — partial payloads cause `400 Bad Request`.
- Icon should be 256x256 PNG with transparency for best rendering across Domo surfaces.

### Create a New View (Page)

```bash
# Write the view body to a file first
python3 -c "
import json
# Get current user ID from the app's owners list
app = json.load(open('app.json'))
owner_id = app['owners'][0]['id']
body = {
    'owners': [{'id': owner_id, 'type': 'USER', 'displayName': None}],
    'type': 'dataappview',
    'title': 'Production',
    'pageName': 'Production',
    'locked': False,
    'mobileEnabled': True,
    'sharedViewPage': True,
    'virtualPage': False
}
json.dump(body, open('new_view.json', 'w'))
"

community-domo-cli --output json -y app-studio create-view $APP_ID \
  --body-file new_view.json > view_response.json

VIEW_ID=$(python3 -c "import json; d=json.load(open('view_response.json')); print(d['view']['pageId'])")
LAYOUT_ID=$(python3 -c "import json; d=json.load(open('view_response.json')); print(d['layout']['layoutId'])")
```

**Response** includes both the `view` (with assigned `pageId`) and `layout` (with assigned `layoutId`) objects. The new view automatically gets a navigation entry with icon `pages`.

**Important**: The `owners` array must include at least the current user. The `type` must be `dataappview`. The `title` and `pageName` should match.

---

## Navigation

Navigation cannot be updated via `app-studio update` — changes to `navigations[]` in the PUT
body are silently ignored. Use the `pages` CLI commands below.

> **Endpoint note**: The CLI `pages` commands use global Domo page navigation endpoints, which
> differ from the App Studio-specific navigation endpoints. For App Studio apps, these commands
> work for reading nav state and reordering pages. Icon and label updates for App Studio nav
> items are not supported by the current CLI commands.

### Read Navigation

```bash
community-domo-cli --output json pages nav-get > nav.json
```

Returns all navigation entries across the instance. Filter to your app's views by matching
`entityId` values against your `views[]` from `app-studio get`.

Entity types: `HOME`, `VIEW`, `AI_ASSISTANT`, `CONTROLS`, `DISTRIBUTE`, `MORE`

**CRITICAL**: The `navigations` array is separate from the `views` array. Renaming a view title via the app PUT does NOT rename the nav label. Always GET the full navigation first, modify only the fields you need, and PUT the complete array back — missing system items causes `400`.

### Reorder Pages

```bash
# Build ordered comma-separated page ID string, then:
community-domo-cli --output json -y pages nav-reorder \
  --body '{"pageOrderMap": {"0": "VIEW_ID_1,VIEW_ID_2,VIEW_ID_3"}}'
```

The `pageOrderMap` key `"0"` is the root level. Value is a comma-separated string of page/view
IDs in the desired order. Send only the IDs you want reordered.

---

## Page Layout API

### Get Page Layout

Returns the full layout definition for a view, including all content items and their positions.

```bash
community-domo-cli --output json app-studio layout-get $APP_ID $VIEW_ID > layout.json

LAYOUT_ID=$(python3 -c "import json; print(json.load(open('layout.json'))['layoutId'])")
```

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

Response fields: `layoutId`, `pageUrn`, `content[]`, `standard.template[]`,
`compact.template[]`, `isDynamic`, `hasPageBreaks`, `printFriendly`, `enabled`.

### Update Page Layout

The CLI handles write lock acquisition and release automatically — no manual lock calls needed.

```bash
# Modify the layout object in Python, then:
community-domo-cli --output json -y app-studio layout-set $APP_ID $VIEW_ID \
  --body-file layout_modified.json
```

The CLI executes three steps internally:
1. `PUT /content/v4/pages/layouts/{layoutId}/writelock`
2. `PUT /content/v4/pages/layouts/{layoutId}` with the body
3. `DELETE /content/v4/pages/layouts/{layoutId}/writelock` (always runs, even on failure)

The body **must contain `layoutId`** — the CLI extracts it to build the lock/PUT/unlock URLs.
If `layoutId` is missing, the CLI raises: `Body must include layoutId. Run layout-get first.`

**Verify dry-run before executing**:

```bash
community-domo-cli --dry-run app-studio layout-set $APP_ID $VIEW_ID --body-file layout_modified.json
# Shows all 3 steps with full request bodies — inspect before committing
```

---

## Adding Cards to App Studio Pages

### Add an Existing Card to a Page

Cards added this way go to the **appendix**. Use `layout-set` to move them to the canvas.

```bash
community-domo-cli -y pages add-card $VIEW_ID $CARD_ID
# Returns empty body on success
```

### List Cards on a Page

```bash
community-domo-cli --output json pages list-cards $VIEW_ID > page_cards.json
```

Returns array of card objects with `id`, `title`, `type`, `urn`.

> **Endpoint note**: CLI uses `GET /content/v3/stacks/{pageId}/cards` (v3 stacks endpoint).
> Response shape may differ slightly from the v1 cards endpoint — same cards, different wrapper.

### Create a Card Directly on a Page

Creates a new KPI card and adds it to the page in one step.

```bash
community-domo-cli --output json -y cards create \
  --body-file card_definition.json \
  --page-id $VIEW_ID > card_response.json

CARD_ID=$(python3 -c "import json; print(json.load(open('card_response.json'))['id'])")
```

Cards created this way go to the **appendix** automatically. Use `layout-set` to place them on
the canvas. See `card-creation/SKILL.md` for the full card body schema.

**CRITICAL — chart type names**: All native chart types require the `badge_` prefix. Use
`badge_vert_bar` (not `bar`), `badge_horiz_bar` (not `horizontal_bar`), etc. Omitting the
prefix causes `400 Bad Request` with no detail. See `card-creation/SKILL.md` for the complete
chart type catalog (207 types).

**CRITICAL — `badge_line` is broken**: `badge_line` always returns HTTP 400 on creation. It is
the only known broken chart type. Use `badge_two_trendline` (full-featured, 203 overrides) or
`badge_spark_line` (compact, 40 overrides) instead. `badge_area` is also not a valid type — use
`badge_vert_area_overlay` for area charts.

#### Common Chart Types Quick Reference

| Use case | `badge_*` chart type | Notes |
|---|---|---|
| **Line / trend** | `badge_two_trendline` | NOT `badge_line` (broken). Full-featured line chart |
| **Compact sparkline** | `badge_spark_line` | Minimal line chart, 40 overrides |
| **Vertical bar** | `badge_vert_bar` | Standard bar chart |
| **Horizontal bar** | `badge_horiz_bar` | Rankings, comparisons |
| **Stacked bar** | `badge_vert_stackedbar` | Composition / part-to-whole |
| **Horizontal stacked** | `badge_horiz_stackedbar` | Horizontal composition |
| **Pie** | `badge_pie` | Simple part-to-whole |
| **Donut** | `badge_donut` | Pie with center hole |
| **Area** | `badge_vert_area_overlay` | NOT `badge_area` (invalid) |
| **Curved area** | `badge_vert_curved_area_overlay` | Smooth area chart |
| **Stacked area** | `badge_stackedtrend` | Stacked area / stream |
| **Combo (bar+line)** | `badge_vert_bar_line` | Dual-axis bar and line |
| **Scatter / bubble** | `badge_xybubble` | XY plot with optional size |
| **Treemap** | `badge_treemap` | Hierarchical area |
| **Funnel** | `badge_funnel` | Conversion funnels |
| **Heatmap** | `badge_heatmap` | Density / matrix |
| **Waterfall** | `badge_vert_waterfall` | Running totals |
| **Gauge** | `badge_gauge` | Radial gauge |
| **Filled gauge** | `badge_filledgauge` | Linear filled gauge |
| **KPI (PoP)** | `badge_pop_multi_value` | Period-over-period hero metric |
| **Dropdown filter** | `badge_dropdown_selector` | Page-level filter control |
| **Date filter** | `badge_date_selector` | Date range picker |

### Read a Card Definition

```bash
community-domo-cli --output json cards definition $CARD_ID > card_def.json
```

Returns `definition`, `dataSourceWrite`, `drillpath`, `embedded`, `id`, `urn`, `columns`.

**Read/write format mismatches** — when reading via `cards definition` then writing via
`cards update`, fix these fields before updating:

| Field | Read returns | Write requires |
|---|---|---|
| `formulas` | `[]` | `{"dsUpdated": [], "dsDeleted": [], "card": []}` |
| `conditionalFormats` | `[]` | `{"card": [], "datasource": []}` |
| `annotations` | `[]` | `{"new": [], "modified": [], "deleted": []}` |
| `segments` | `{"active": [], "definitions": []}` | `{"active": [], "create": [], "update": [], "delete": []}` |

Also: add `title`, `description`, `noDateRange` if missing; remove `modified`, `allowTableDrill`.

### Update a Card

```bash
community-domo-cli --output json -y cards update $CARD_ID \
  --body-file card_updated.json
```

### Add Card to the Domo Overview Page

The Domo overview/home page uses the special page ID `-100000`:

```bash
community-domo-cli -y pages add-card -- -100000 $CARD_ID
```

Note the `--` separator before the negative page ID to prevent it being parsed as a flag.

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


| sourceId    | Style                  | Recommended use                                             |
| ----------- | ---------------------- | ----------------------------------------------------------- |
| `ca1`       | Default surface        | **Primary default** — translucent white bg, floating shadow |
| `ca2`       | Alternate surface      | Same as ca1, alternate slot for variation                   |
| `ca3`       | Light translucent      | Lighter opacity — filter/control cards                      |
| `ca4`-`ca6` | Accent styles          | Colored/themed cards                                        |
| `ca7`       | Near-opaque surface    | Subtle shadow, higher opacity for emphasis                  |
| `ca8`       | Transparent/borderless | Banners, images, notebooks (no chrome)                      |


Style is applied per-card per-page. The same card can have different styles on different pages. Omitting the `style` property uses the default/no style.

To apply a style, add the `style` object to the content entry and update the layout via `layout-set`.

### Default Card Style

Cards should use **zero border-radius, zero border weight, zero padding, no drop shadow** per the mandatory reference configuration. See "Card Styles (ca1-ca8)" under Theme Management for the full spec.

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

This workflow adds dropdown filter cards to all views in an App Studio app, positioned identically on each page.

### Step 1: Create the cards on one page

```bash
community-domo-cli --output json -y cards create \
  --body-file filter_card.json --page-id $PAGE_ID > filter1.json
FILTER1=$(python3 -c "import json; print(json.load(open('filter1.json'))['id'])")
```

### Step 2: Add the same cards to other pages (goes to appendix)

```bash
for PAGE in $PAGE2 $PAGE3 $PAGE4; do
  community-domo-cli -y pages add-card $PAGE $FILTER1
done
```

### Step 3: Move cards from appendix to canvas on each page

```bash
for PAGE in $PAGE2 $PAGE3 $PAGE4; do
  # Get layout
  community-domo-cli --output json app-studio layout-get $APP_ID $PAGE > layout_p.json

  # Modify layout (set virtualAppendix=false, virtual=false, set x/y/width/height)
  python3 - <<'PYEOF'
import json
layout = json.load(open('layout_p.json'))
# ... position your filter cards ...
json.dump(layout, open('layout_p_updated.json', 'w'))
PYEOF

  # Apply — write lock handled by CLI
  community-domo-cli --output json -y app-studio layout-set $APP_ID $PAGE \
    --body-file layout_p_updated.json
done
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

```bash
community-domo-cli --output json -y app-studio create \
  --body '{"title": "Sales Metrics Dashboard", "description": "Sales performance metrics"}' \
  > app.json
APP_ID=$(python3 -c "import json; print(json.load(open('app.json'))['dataAppId'])")
PAGE_ID=$(python3 -c "import json; print(json.load(open('app.json'))['landingViewId'])")
echo "App: $APP_ID  Page: $PAGE_ID"
```

### Step 1b: Discover Dataset Schemas

Before creating any cards, query each dataset's schema to get exact column names and types:

```bash
community-domo-cli --output json datasets schema $DATASET_ID > schema.json

python3 -c "
import json
cols = json.load(open('schema.json'))['tables'][0]['columns']
for col in cols:
    print(f\"{col['name']:40s} {col['type']}\")
"
```

Store column names per dataset — you'll need them for card `columns` arrays (VALUE, ITEM, SERIES mappings).

### Step 2: Create Cards on the Page

```bash
# Create as many cards as needed — they all go to the appendix
community-domo-cli --output json -y cards create \
  --body-file card_kpi.json --page-id $PAGE_ID > card1.json
CARD1=$(python3 -c "import json; print(json.load(open('card1.json'))['id'])")
```

See `card-creation/SKILL.md` for the full card body schema. **All chart types require the `badge_` prefix** (e.g., `badge_vert_bar`, `badge_two_trendline`, `badge_pie`) — see the Quick Reference table above or that skill for the complete catalog. **Never use `badge_line`** (always 400) or `badge_area` (invalid).

**Important**: Domo auto-assigns `contentKey` values when cards are added to the appendix. Keys may not be sequential — gaps occur (e.g., 1,2,3,4,5,6,7,8,9,11,12 — skipping 10). Always read the actual layout to get the real keys.

### Step 3: Get the Layout and Inspect Content Keys

```bash
community-domo-cli --output json app-studio layout-get $APP_ID $PAGE_ID > layout.json

python3 -c "
import json
layout = json.load(open('layout.json'))
print('layoutId:', layout['layoutId'])
for c in layout['content']:
    print(f\"  key={c['contentKey']} type={c['type']} card={c.get('cardId','')}\")
"
```

### Step 4: Build the Template and Update Layout

```python
# layout.json was fetched via CLI in Step 3
import json

layout = json.load(open('layout.json'))
layout_id = layout['layoutId']

# Build standard + compact templates
std_template = []
compact_template = []
y = 0   # Track vertical position for standard
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

# CRITICAL: preserve appendix artifacts (PAGE_BREAK, SEPARATOR template-only entries)
content_keys = {c['contentKey'] for c in layout['content']}
for entry in layout['standard']['template']:
    if entry['contentKey'] not in content_keys:
        std_template.append({**entry, 'virtual': True, 'virtualAppendix': True})
for entry in layout['compact']['template']:
    if entry['contentKey'] not in content_keys:
        compact_template.append({**entry, 'virtual': True, 'virtualAppendix': True})

# Update header text
for c in layout['content']:
    if c['type'] == 'HEADER' and c['contentKey'] == 1:
        c['text'] = 'Sales Overview'

layout['standard']['template'] = std_template
layout['compact']['template'] = compact_template
json.dump(layout, open('layout_updated.json', 'w'))
```

```bash
# Apply layout — CLI handles write lock automatically
community-domo-cli --output json -y app-studio layout-set $APP_ID $PAGE_ID \
  --body-file layout_updated.json
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

Custom app card instances (from published designs) are created via a two-step CLI flow: create a context, then create the card from that context.

### Step 1: Create a Context

A context defines the dataset mappings, collections, and resource bindings for a card instance.

```bash
python3 -c "
import json
body = {
    'designId': '$DESIGN_ID',
    'mapping': [{'alias': 'sales', 'dataSetId': '$DATASET_ID', 'fields': [], 'dql': None}],
    'collections': [], 'accountMapping': [], 'actionMapping': [],
    'workflowMapping': [], 'packageMapping': [],
    'isDisabled': False
}
json.dump(body, open('context.json', 'w'))
"

community-domo-cli --output json -y domoapps context-create \
  --body-file context.json > context_response.json

CONTEXT_ID=$(python3 -c "import json; d=json.load(open('context_response.json')); print(d[0]['id'])")
```

Response: `[context, []]` — the context object contains the generated `id`.

For apps with no datasets (e.g., banners), use `"mapping": []`.

### Step 2: Create the Card from the Context

```bash
community-domo-cli --output json -y domoapps card-create \
  --page-id $VIEW_ID \
  --body "{\"contextId\": \"$CONTEXT_ID\", \"id\": \"$CONTEXT_ID\"}" \
  > domoapps_card_response.json
```

**Critical**: The `id` field must be the **context ID** from Step 1, NOT the design ID. Using the design ID causes 500 errors when datasets differ from the original.

| Param       | Description                                         |
| ----------- | --------------------------------------------------- |
| `fullpage`  | `false` for standard card, `true` for full-page app |
| `pageId`    | Target page ID, or `-100000` for asset library only |
| `cardTitle` | URL-encoded title for the card                      |

### Updating a Context (Rewire Dataset)

Use the CLI's context update command with the full context object and updated `mapping`.

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

The **hero metrics** are **native `badge_pop_multi_value` (Period over Period Multi-Value) cards** — NEVER pro-code. They automatically provide: big number, percent change vs prior period, direction indicator, and additional text. Create via `cards create --page-id` with `chartType: "badge_pop_multi_value"`. See `card-creation/SKILL.md` for the full body schema.

The **primary visualization** spans the full horizontal width of the page. **The Overview page** typically uses a time-series line/area chart showing trends. **Sub-pages MUST vary chart types** — use bar charts, stacked bars, horizontal bars, scatter plots, heatmaps, or other types suited to the page's data story. Never use the same chart type on every page. See the chart type selection table below.

#### Primary Viz Chart Type by Page


| Page position                                | Recommended chart types                | `badge_*` name                                                           | Why                                            |
| -------------------------------------------- | -------------------------------------- | ------------------------------------------------------------------------ | ---------------------------------------------- |
| **Overview**                                 | Time-series line/area                  | `badge_two_trendline`, `badge_vert_area_overlay`                         | Shows trends, forecasts, high-level trajectory |
| **Sub-page 1** (e.g., Production, Revenue)   | Vertical bar, grouped bar, stacked bar | `badge_vert_bar`, `badge_vert_bar_overlay`, `badge_vert_stackedbar`      | Compares categories, shows composition         |
| **Sub-page 2** (e.g., Quality, Engagement)   | Horizontal bar, lollipop, beeswarm     | `badge_horiz_bar`, `badge_horiz_bar_overlay`, `badge_horiz_stackedbar`   | Rankings, distributions, part-to-whole         |
| **Sub-page 3** (e.g., Supply Chain, Support) | Scatter, bubble, treemap, heatmap      | `badge_xybubble`, `badge_treemap`, `badge_heatmap`                       | Correlations, density, multi-dimensional       |


The agent MUST select a **different primary chart type for each sub-page**. Repeating line charts across all pages makes dashboards feel monotonous and wastes the opportunity to match visualization type to data shape. When using pro-code charts, the `app-studio-pro-code` skill provides templates for line, bar, stacked bar, horizontal bar, and scatter patterns.

### Hero Metric Card Design (NATIVE — Never Pro-Code)

**CRITICAL: Never use pro-code apps for hero/summary metric cards.** Always use native `badge_pop_multi_value` cards. They are purpose-built for this use case and provide automatic period-over-period comparison.

Create each hero card with `cards create --page-id`:

**CRITICAL: PoP cards require THREE things to show comparison data:**

1. **Date column in `main.columns`** with `mapping: "ITEM"` and `aggregation: "MAX"` (populates the "Time period" drop zone)
2. `**dateRangeFilter**` on the `main` subscription (sets "Date range: This Year" + "Compare to: 1 year ago")
3. `**time_period` subscription** with the same date column

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


| Override             | Values                                                             | Purpose                                                                        |
| -------------------- | ------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| `gauge_layout`       | `Center Vertical`                                                  | Layout of metric elements                                                      |
| `comp_val_displayed` | `Percent Change`                                                   | Show % change vs prior period                                                  |
| `addl_text`          | `Prior Year` (ALWAYS use "Prior Year" — MONTH causes blank heroes) | Contextual subtitle                                                            |
| `title_text`         | e.g. `Total Production`                                            | **Required.** Chart-level title displayed inside the card. Must always be set. |
| `gauge_sizing`       | `Default`                                                          | Auto-size values                                                               |


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

**Updating existing hero cards:**

```bash
# Read current definition
community-domo-cli --output json cards definition $CARD_ID > card_def.json

# Modify in Python (fix format mismatches, update dateRangeFilter, overrides, etc.)
# Then update:
community-domo-cli --output json -y cards update $CARD_ID --body-file card_updated.json
```

Format `formulas` as `{"dsUpdated":[], "dsDeleted":[], "card":[]}`, `annotations` as `{"new":[], "modified":[], "deleted":[]}`, `conditionalFormats` as `{"card":[], "datasource":[]}`, `segments` as `{"active":[], "create":[], "update":[], "delete":[]}`.

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

Create filter cards with `cards create --page-id`, using the appropriate selector chart type.

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


| Chart type                | Purpose                                     | Key override                                |
| ------------------------- | ------------------------------------------- | ------------------------------------------- |
| `badge_dropdown_selector` | Dropdown list filter                        | `allow_multi_select`, `dropdown_label_text` |
| `badge_date_selector`     | Date range picker                           | -                                           |
| `badge_checkbox_selector` | Checkbox filter (multi-select visible)      | -                                           |
| `badge_radio_selector`    | Radio button filter (single-select visible) | -                                           |
| `badge_range_selector`    | Numeric range slider                        | -                                           |
| `badge_slicer`            | Slicer-style filter                         | -                                           |


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

- `**hideSummary: true**` — hides the summary number (e.g., "5K PlantName") that appears above the dropdown. Without this, filter cards display a distracting count.
- `**hideMargins: true**` — removes internal padding for tighter fit.
- `**fitToFrame: true**` — scales the dropdown to fill the card frame.
- `**hideBorder: true**` — removes the card border for a seamless look.
- `**style: null**` — NO style applied. Do NOT use `ca3` or any colored style on filter cards. They should have a transparent/default background that blends with the page. Colored or opaque backgrounds (green, blue, etc.) make filters visually polarizing and distracting.
- `**hideTitle: true**` — hide the card-level title. The dropdown selector already renders its own field label (e.g., "Region", "Status"), so showing the card title creates redundant text. If the card title contains coded prefixes (e.g., "FS-Ov-Reg"), hiding it is essential.

### Filter Card Layout Sizing

Filter cards should be **compact** — they are controls, not content. Use minimal height.


| Template           | Width                          | Height  | Notes                                     |
| ------------------ | ------------------------------ | ------- | ----------------------------------------- |
| Standard (desktop) | 20 (3 across) or 15 (4 across) | **6**   | Minimal height for low-profile appearance |
| Compact (mobile)   | 12 (full width, stacked)       | **6-8** | Stacked vertically                        |


**Recommended page layout with filters (CANONICAL):**

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

```bash
python3 -c "
import json
body = {
    'name': 'Selected Plant',
    'locked': False,
    'global': True,
    'expression': \"'All'\",
    'links': [],
    'aggregated': False,
    'analytic': False,
    'nonAggregatedColumns': [],
    'dataType': 'STRING',
    'status': 'VALID',
    'cacheWindow': 'non_dynamic',
    'columnPositions': [],
    'functions': [],
    'functionTemplateDependencies': [],
    'archived': False,
    'hidden': False,
    'variable': True   # CRITICAL — makes this a Variable, not a Beast Mode
}
json.dump(body, open('variable.json', 'w'))
"

community-domo-cli --output json -y beast-modes create \
  --body-file variable.json > variable_response.json

FUNCTION_ID=$(python3 -c "import json; print(json.load(open('variable_response.json'))['id'])")
LEGACY_ID=$(python3 -c "import json; print(json.load(open('variable_response.json'))['legacyId'])")
```

**Variable data types:**


| dataType  | expression example | Use case                                |
| --------- | ------------------ | --------------------------------------- |
| `STRING`  | `"'All'"`          | Dropdown selections, text filters       |
| `DECIMAL` | `"95"`             | Thresholds, percentages, what-if values |
| `LONG`    | `"100"`            | Integer counts, limits                  |
| `DATE`    | `"'2026-01-01'"`   | Date selections                         |


The `function_id` (numeric, e.g., `115511`) is used by pro-code apps:

- Read: `domo.onVariablesUpdated(vars => vars["115511"]?.parsedExpression?.value)`
- Write: `domo.requestVariablesUpdate([{ functionId: 115511, value: "Plant A" }])`

### Variable Controls — App Studio Editor (Manual Steps Required)

**Variable Controls cannot be added programmatically.** The layout API only supports `CARD`, `HEADER`, `SPACER`, `SEPARATOR`, and `PAGE_BREAK` content types. Variable Controls must be configured through the App Studio editor UI.

After creating variables via the CLI, instruct the user to complete these steps in the App Studio editor:

1. **Open the app** in App Studio editor (Apps Home -> hover app -> More -> Edit)
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

1. Go to **App Configuration** -> **Filter Options** tab
2. Check **"Persist Variable controls"**
3. Note: Variable controls only apply to pages that contain that control. Add the control to each page where persistence is needed.

### Variables vs Filter Cards

Both provide page-level interactivity, but they work differently:


| Feature      | Filter Cards                 | Variables                                                 |
| ------------ | ---------------------------- | --------------------------------------------------------- |
| Creation     | Fully programmatic (CLI)     | Programmatic creation + manual UI binding                 |
| Mechanism    | Interaction filter system    | Beast Mode calculation system                             |
| Cross-card   | Automatic (same column name) | Requires Beast Mode on each card                          |
| Pro-code API | `domo.onFiltersUpdated`      | `domo.onVariablesUpdated`                                 |
| Use case     | Column-based filtering       | What-if analysis, metric switching, calculated parameters |
| Persistence  | Built-in page-level          | Configurable via persistent filters                       |


**Recommendation**: Use **filter cards** for straightforward column filtering (Plant, Status, Date Range). Use **variables** for calculated parameters (threshold %, metric selector, aggregation granularity) and when pro-code apps need to read/write shared state.

---

## Design-Aware Layout

These rules make layouts feel intentional rather than mechanically packed. For detailed layout density presets and spacing examples, see [layout-design.md](layout-design.md).

### Breathing Room

Insert SPACERs to create visual separation between card groups. Without intentional whitespace, layouts feel cramped.


| Spacing purpose                        | Element                                   | Height |
| -------------------------------------- | ----------------------------------------- | ------ |
| Top of page (before first content)     | SPACER                                    | 3      |
| Between cards in the same section      | (none — cards touch)                      | 0      |
| Between card rows within a section     | (implicit from y positioning)             | 0      |
| Between sections (before a HEADER)     | SPACER                                    | 5      |
| After a section header                 | (none — cards start at y + header height) | 0      |
| After filter row (before main content) | SEPARATOR                                 | 2      |


### Row Harmony

Cards on the same grid row should use the same height. Mixed heights on a row (e.g., KPI at height 10 next to a chart at height 22) create a ragged bottom edge. When mixing card types on a row, either use the taller card's height for all items, or separate them into distinct rows.

### Visual Weight Distribution

Place cards in this order top-to-bottom: filters, then KPIs/summary numbers, then charts, then tables. This mirrors the natural reading pattern — controls first, summary second, detail last. Each tier represents increasing information density.

### Section Title Quality

HEADER content items should use concise, specific text. Avoid generic labels like "Overview" or "Metrics" — use labels that tell the reader what the data answers, e.g., "Revenue by Region", "Pipeline Health", "Monthly Trend".

### Layout Density Presets

Choose a density tier based on the audience and page purpose:


| Preset          | Cards/page | Card widths | Spacer usage                | Audience             |
| --------------- | ---------- | ----------- | --------------------------- | -------------------- |
| **Executive**   | 4-8        | 20-30       | Generous (height 5 spacers) | C-suite, board decks |
| **Operational** | 8-16       | 15-20       | Moderate (height 3 spacers) | Managers, daily use  |
| **Detailed**    | 16+        | 10-15       | Minimal (height 2 spacers)  | Analysts, drill-down |


### Style ID Usage

Apply `style.sourceId` in the content array to differentiate card types visually. Use a consistent pattern across all pages:

- **Filter cards**: no style (default) — keeps them visually neutral
- **KPI / summary cards**: a contrasting style to draw attention
- **Chart / table cards**: a uniform style for the detail tier

Apply the same style mapping on every page in the app for visual consistency. The same card can have different styles on different pages, but keeping them consistent across pages reduces cognitive load.

---

## Theme Management

The `theme` object inside the app controls all visual styling — colors, fonts, card styles, navigation appearance, page background, and layout density. It is updated via the full-body `app-studio update` command.

```bash
# Read current app (includes theme)
community-domo-cli --output json app-studio get $APP_ID > app.json

# Modify theme in Python
python3 - <<'PYEOF'
import json
app = json.load(open('app.json'))
theme = app['theme']
# ... modify theme ...
json.dump(app, open('app_updated.json', 'w'))
PYEOF

# Apply
community-domo-cli --output json -y app-studio update $APP_ID --body-file app_updated.json
```

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

App Studio's theme has 60 color slots (`c1`-`c60`) organized by tag group. Map your custom palette following this structure:


| Slot range | Tag                              | Purpose                             | Example mapping                             |
| ---------- | -------------------------------- | ----------------------------------- | ------------------------------------------- |
| c1-c7      | TINTED_GRAY                      | Neutral grayscale dark->light       | neutral-950, 900, 600, 300, 200, 100, white |
| c8-c14     | PRIMARY (ORDER_SOURCE at c8)     | Brand series base->tints            | brand-500, 400, 300, 200, 100, 50, 50       |
| c15-c21    | PRIMARY                          | Brand darker shades                 | brand-600->950                              |
| c22-c28    | SECONDARY (ORDER_SOURCE at c22)  | 2nd series base->tints              | teal-600->50                                |
| c29-c35    | TERTIARY (ORDER_SOURCE at c29)   | 3rd series base->tints              | amber-600->50                               |
| c36-c42    | QUATERNARY (ORDER_SOURCE at c36) | 4th series base->tints              | red-600->50                                 |
| c43-c57    | GRAYSCALE                        | Nav/sidebar/text/borders dark->light| neutral-950->white                          |
| c58-c59    | FONT                             | Dark/light font                     | neutral-950, white                          |
| c60        | AUTOMATIC_COLOR                  | Do NOT modify                       | Automatic dark/light switching              |


**Colors**: Update via `color_entry['value'] = {'value': '#HEX', 'type': 'RGB_HEX'}`. All hex values **MUST be uppercase**. Skip `c60`.

#### Chart Color Palette (`chartColorPalette`)

The theme's `c8-c42` color slots control UI chrome (nav, pills, buttons, backgrounds) but **NOT chart series colors**. Chart series colors are controlled exclusively by the `chartColorPalette` theme field.

`**chartColorPalette`** accepts only `{"id": "<palette name>", "type": "DOMO"}` where the palette name references a Brand Kit chart color palette. The only built-in valid name is `"Domo Default Palette"`. Setting an unrecognized name results in `null` (charts fall back to theme color families c8/c15/c22/c29/c36 or hardcoded defaults).

**To apply custom chart colors to native App Studio cards:**

1. **Preferred: Create a Brand Kit palette** through the Domo Admin UI (Admin > Brand Kit > Chart Colors > New Palette). Use the same brand/teal/amber/red hex values from the custom palette. After creating and activating it, reference its name in the theme:
  ```python
   theme['chartColorPalette'] = {'id': '<Brand Kit Palette Name>', 'type': 'DOMO'}
  ```
2. **Fallback: Set chartColorPalette to null** by using an invalid name (`{'id': 'Custom', 'type': 'DOMO'}`). Charts may fall back to the theme's color families (c8, c15, c22, c29, c36).

**Important:** The `chartColorPalette` field does NOT accept `type: "CUSTOM"` with inline colors — the API returns `400 Bad Request`. There is no public API for programmatic Brand Kit palette creation; it must be done through the Admin UI.

1. **Most reliable: Set series colors per card via overrides.** Read the card, fix format mismatches, add overrides, then update:
  ```bash
  # Read card definition
  community-domo-cli --output json cards definition $CARD_ID > card_def.json
  
  # Modify in Python — add series colors and fix format mismatches
  python3 - <<'PYEOF'
  import json
  SERIES_COLORS = ['#3B82C8', '#0D9488', '#D97706', '#DC2626',
                   '#2661A3', '#059669', '#7C3AED', '#DB2777']
  # ... fix format mismatches, add overrides ...
  PYEOF
  
  # Update
  community-domo-cli --output json -y cards update $CARD_ID --body-file card_updated.json
  ```
   **Gotcha — Read/Write format mismatches:** The READ endpoint returns simplified formats that the WRITE endpoint rejects. You MUST fix these before updating:
  - `formulas`: read returns `[]` -> write needs `{"dsUpdated": [], "dsDeleted": [], "card": []}`
  - `conditionalFormats`: read returns `[]` -> write needs `{"card": [], "datasource": []}`
  - `annotations`: read returns `[]` -> write needs `{"new": [], "modified": [], "deleted": []}`
  - `segments`: read has `{"active": [], "definitions": []}` -> write needs `{"active": [], "create": [], "update": [], "delete": []}`
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

**Root cause**: `c60` is an `AUTOMATIC_COLOR` with `dark` -> `c58` and `light` -> `c59` variants. The Clarion theme treats itself as "light mode" regardless of actual background colors, so it always picks `c59` (dark text). On dark backgrounds, this produces invisible text on cards, navigation, headers, filters, and components.

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


| Slot    | Light mode                 | Dark mode                                                |
| ------- | -------------------------- | -------------------------------------------------------- |
| c1-c7   | dark->light grays          | light->dark (c1=page bg dark, c5=text light, c7=white)  |
| c43-c54 | dark nav/sidebar grays     | dark backgrounds matching page bg                        |
| c55     | page bg (ultra-light gray) | page bg (**dark**, e.g., #1E1C1A)                        |
| c56     | card surface (white)       | card surface (**dark**, e.g., #302C28)                   |
| c58     | dark font                  | **light font** (e.g., #F5F3F0) — primary text on dark bg |
| c59     | light/white font           | **dark font** (e.g., #1E1C1A) — inverse text             |


**Dark mode sidebar colors** — match the banner gradient:

```python
for c in theme['colors']:
    if c['id'] == 'c43': c['value'] = {'value': '#1E1C1A', 'type': 'RGB_HEX'}  # nav bg
    if c['id'] == 'c44': c['value'] = {'value': '#302C28', 'type': 'RGB_HEX'}  # nav hover
    if c['id'] == 'c45': c['value'] = {'value': '#3A3632', 'type': 'RGB_HEX'}  # nav active
```

**Font**: Use `Sans` family throughout (not `Slab`). Map to domo-app-theme typography:


| Font ID | Role          | Family | Weight | Size |
| ------- | ------------- | ------ | ------ | ---- |
| f1      | Page title    | Sans   | 700    | 22   |
| f2      | Header h1     | Sans   | 700    | 22   |
| f3      | Section title | Sans   | 600    | 16   |
| f4      | Card title    | Sans   | 600    | 16   |
| f5      | Body semibold | Sans   | 600    | 13   |
| f6      | Body text     | Sans   | 400    | 13   |
| f7      | Captions      | Sans   | 400    | 12   |
| f8      | Button text   | Sans   | 600    | 13   |
| f9      | Small/badge   | Sans   | 600    | 11   |


### Border Radius — ZERO EVERYWHERE (MANDATORY)

**All border-radius values MUST be 0.** No rounded corners on any element — cards, containers, buttons, inputs, filters, tables, notebooks, components, tabs, forms, or pills. This is a strict global rule.


| Element                               | Radius | Notes                            |
| ------------------------------------- | ------ | -------------------------------- |
| Cards (`borderRadius`)                | **0**  | Zero rounding on all card styles |
| Tables (`borderRadius`)               | **0**  | Zero rounding                    |
| Notebooks (`borderRadius`)            | **0**  | Zero rounding                    |
| Components outer (`borderRadius`)     | **0**  | Zero rounding                    |
| Components inner (`itemBorderRadius`) | **0**  | Zero rounding                    |
| Buttons (`borderRadius`)              | **0**  | Zero rounding                    |
| Tabs (`borderRadius`)                 | **0**  | Zero rounding                    |
| Forms (`borderRadius`)                | **0**  | Zero rounding                    |
| Pills (`radius`)                      | **0**  | Zero rounding                    |


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

### Card Styles (ca1-ca8) — Reference Configuration (MANDATORY)

All card styles MUST follow this reference configuration. Zero border-radius, zero border weight, zero padding, no drop shadow, no content spacing:

```python
# ca1-ca7 — clean surface, zero chrome (default for all content cards)
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


| Setting                    | Value            | API property                                  |
| -------------------------- | ---------------- | --------------------------------------------- |
| Rounded corners            | **0 px**         | `borderRadius: 0`                             |
| Border weight              | **0 px**         | `borderWidth: 0`                              |
| Drop shadow                | **None**         | `dropShadow: 'NONE'`                          |
| Controls color             | **#2563BE**      | Theme color `c8` -> `#2563BE`                 |
| Card inner padding         | **Custom, 0 px** | `padding: {left:0, right:0, top:0, bottom:0}` |
| Card content spacing       | **Nil**          | `contentSpacing: None` (null)                 |
| Space below header content | **0 px**         | `headerBottomSpacing: 0`                      |


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
2. **Page-level**: Each page layout's `isDynamic` (via layout-set) should also be `false`

```python
# Fixed-width — ALWAYS apply this
for page in theme.get('pages', []):
    page['isDynamic'] = False
    page['density'] = {'compact': 8, 'standard': 8}
```

The theme-level setting controls the default; page-level can override.

### Sidebar-Banner Color Tie

When using a dark gradient banner, tie the sidebar/navigation background to the same color palette. The nav theme uses color references `c43` (background), `c44` (hover), `c45` (active). Set these to match the banner's gradient endpoints:

```python
# Banner gradient: oklch(0.280 0.020 256) -> oklch(0.374 0.014 256)
for c in theme['colors']:
    if c['id'] == 'c43': c['value'] = {'value': '#2A2E35', 'type': 'RGB_HEX'}  # nav bg
    if c['id'] == 'c44': c['value'] = {'value': '#353A42', 'type': 'RGB_HEX'}  # nav hover
    if c['id'] == 'c45': c['value'] = {'value': '#3F454D', 'type': 'RGB_HEX'}  # nav active
```

This creates visual continuity between the sidebar and page banners. Always do this when building apps with dark banner headers.

### Navigation Icons

Icons are set via the navigation reorder endpoint. The body must be the **full navigation array** as returned by GET — partial payloads cause `400 Bad Request`.

**HOME icon**: Always set `icon.value = "home"` for the HOME navigation item.

**WARNING**: Google Material icon names (`monetization_on`, `trending_up`, `inventory_2`, `assignment_return`) do NOT render in Domo's left nav. Domo uses its own internal icon set. **ONLY use icons from the catalog below.** If an icon name is wrong, the nav item renders with no visible icon (blank space).

#### Recommended icons by page type


| Page type                | Recommended icons (pick one)                                                          |
| ------------------------ | ------------------------------------------------------------------------------------- |
| Overview / Dashboard     | `analytics`, `pop-chart`, `chart-bar-vertical`, `select-chart`, `badge-layout-8`      |
| Production / Operations  | `gauge`, `dataflow`, `cube-filled`, `completed-submissions`                           |
| Quality / Compliance     | `certified`, `checkbox-marked-outline`, `check-in-icon`, `approval-center`            |
| Supply Chain / Logistics | `globe`, `data-app`, `local_shipping`, `warehouse`, `shopping_cart`                   |
| Retail / Store           | `store`, `cube-filled`, `numbers`, `toolbox`                                          |
| Financial                | `money-universal`, `money`, `benchmark`, `books`, `calculator`                        |
| People / HR / Patients   | `people`, `person`, `person-card`, `person-plus`, `people-plus`, `heart`              |
| Time / Scheduling        | `clock`, `calendar-simple`, `calendar-time`, `alarm`, `interrupting-timer`            |
| Documents / Reports      | `document`, `document-outline`, `books`, `newspaper`, `clipboard-copy`                |
| AI / ML / Intelligence   | `ai-chat`, `magic`, `wand`, `lightbulb`, `lightning-bolt`, `sciency-data`, `analyzer` |
| Marketing / Campaigns    | `area-chart`, `funnel`, `bell-outline`, `video`, `image`                              |
| Settings / Admin         | `controls`, `pages-gear`, `code-tags`, `pencil-box`, `lock-closed`                    |
| Geography / Location     | `globe`, `map-marker`, `building`                                                     |
| Forecasting / Goals      | `forecast`, `goals`, `trophy`, `exclamation-triangle`                                 |
| Education                | `graduation-cap`, `domo-university`                                                   |
| Health / Safety          | `heart`, `glasses`, `adc`                                                             |
| Inventory / Products     | `cube-filled`, `domobox`, `table`, `tag-multiple`, `badge-layout-small`               |


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


| Issue                                             | Detail                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| ------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Write lock handled by CLI**                     | The CLI's `layout-set` command automatically acquires and releases write locks. No manual lock management needed. If using raw API calls, you must `PUT /content/v4/pages/layouts/{layoutId}/writelock` before and `DELETE` after.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **Cards go to appendix by default**               | When you add a card via `pages add-card` or `cards create --page-id`, it goes to the appendix. You must update the layout via `layout-set` to move it to the canvas.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **layoutId != pageId**                            | Each page has its own `layoutId` (a different numeric ID). Get it from `layout-get`. The `layout-set` body **must contain `layoutId`** or the CLI raises an error.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **viewId = pageId**                               | In App Studio, the `viewId` from the app structure IS the `pageId` for card and layout operations.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **Template must account for ALL content keys**    | Every `contentKey` present in the `content` array MUST have a corresponding entry in BOTH `standard.template` AND `compact.template`. If any key is missing from either template, the PUT returns `400 Bad Request` with no detail. This is the #1 cause of layout update failures.                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Appendix artifacts MUST be preserved**          | When Domo adds cards to the appendix, it auto-generates `PAGE_BREAK` and `SEPARATOR` entries in the template with `contentKey` values that do NOT exist in the `content` array. These template-only entries MUST be included in your updated template (keep them as `virtualAppendix: true, virtual: true`). Removing them causes `400 Bad Request`. Always diff `content` keys vs `template` keys before building your new layout.                                                                                                                                                                                                                                                                                                                  |
| **Content keys may have gaps**                    | Domo assigns `contentKey` values incrementally, but gaps occur (e.g., 1,2,3,4,5,6,7,8,9,11,12 — key 10 is skipped). Never assume sequential keys. Always read the layout to get actual keys.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
| **standard + compact both required**              | The layout body must include both `standard` (desktop) and `compact` (mobile) template arrays. Both must contain entries for all content keys.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                       |
| **Content array is managed by Domo**              | When creating cards on a page, Domo auto-populates the `content` array with full card properties (`hideTitle`, `hideFooter`, `acceptFilters`, etc.). You can modify these entries (e.g., change header `text`) but should not add or remove `CARD` entries manually — only move them between canvas and appendix via the template.                                                                                                                                                                                                                                                                                                                                                                                                                   |
| **LEFT nav requires `showDomoNavigation: false`** | Setting `navOrientation` to `LEFT` while `showDomoNavigation` is `true` causes `400 Bad Request`. All LEFT-nav apps in production have `showDomoNavigation: false`. Set both in the same update.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **View creation body format**                     | `create-view` requires the `view` sub-object directly as the body — NOT wrapped in `{"view": {...}}` or `{"title": "..."}`. The body must include `type: "dataappview"`, `title`, `pageName`, and an `owners` array.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **App update requires full body**                 | The `app-studio update` command rejects partial bodies with `400 Bad Request`. You must send the complete app object from `app-studio get`. Read-only fields like `userAccess`, `isOwner`, `isFavorite`, `canEdit` are safely ignored by the server.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **New apps have `isDynamic: false`**              | Newly created App Studio apps have `isDynamic: false` in their layout (unlike apps created via the UI which may have `isDynamic: true`). This does not affect layout operations.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
| **New apps have `enabled: true`**                 | Newly created apps include an `enabled` field in the layout response. Preserve this when updating layouts.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **Style is per-content-entry**                    | Card styles (`"style": {"sourceId": "ca8"}`) are set in the `content` array, not in the template. The same card can have different styles on different pages.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        |
| **No card duplication**                           | Adding the same card to multiple pages doesn't duplicate it — it's the same card rendered on each page. Filter interactions are shared.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Overview page is `-100000`**                    | The Domo overview/home page has the special page ID `-100000`. Use `pages add-card -- -100000 $CARD_ID` (note `--` before the negative ID).                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Cards on overview != cards in App Studio**      | Adding a card to page `-100000` puts it on the Domo overview page. It does NOT appear inside App Studio views. To have cards in App Studio, add them to the specific view `pageId`. These are independent assignments.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Cards from different datasets on same page**    | An App Studio page can contain cards powered by different datasets. There is no restriction. This was verified with a page containing 23 cards across 2 datasets.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Hex values MUST be uppercase**                  | Color hex values in the theme (e.g., `#3F454D`) must use uppercase letters. Lowercase hex (e.g., `#3f454d`) causes `400 Bad Request` on update.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                      |
| **Card padding max is 16**                        | Card `padding` values (left/right/top/bottom) cannot exceed 16. Values like 20 cause `400 Bad Request`. Use 16 for maximum padding.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  |
| **Nav reorder requires full array**               | The navigation reorder endpoint requires the complete navigation array. Sending a subset causes `400`. **CRITICAL: Preserve all default system nav items** (HOME, AI_ASSISTANT, CONTROLS, DISTRIBUTE, MORE/Details). **If HOME is missing (some new apps don't include it), add it explicitly**: `{"entity": "HOME", "title": "Home", "icon": {"type": "NAME", "value": "home"}, "visible": true}`. Without HOME, users cannot navigate back to the Domo portal.                                                                                                                                                                                                                                                                                     |
| **Theme pages[0].isDynamic controls fixed width** | Setting `theme.pages[0].isDynamic = false` with `density: {'compact': 8, 'standard': 8}` creates a fixed-width layout. This is independent of per-page layout `isDynamic`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                           |
| **LEFT nav: hide title and logo**                 | For `navOrientation: 'LEFT'`, set `showTitle: false` and `showLogo: false`. The page names in the left nav already identify the app — the title wastes vertical space.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               |
| **Sidebar color must match banner**               | When using a dark gradient banner, update `c43`/`c44`/`c45` to match the banner's gradient palette. Mismatched sidebar and banner colors break visual continuity.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Pro-code cards: no own shadow**                 | Pro-code apps embedded in App Studio should set `background: transparent` and no `box-shadow`. The App Studio card style (ca1) provides the card chrome. Duplicate shadows create a double-border effect.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **Daily tick density**                            | Time-series pro-code charts with >30 data points must thin ticks using an interval formula. Target ~18 visible labels. See `app-studio-pro-code` for the `calcTickInterval` function.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                |
| **Banner height = 14**                            | Banners should use height 14 (not 7) in standard template to accommodate subheader text. Compact: height 8.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                          |
| **Dark mode: c60 invisible text**                 | `c60` (AUTOMATIC_COLOR) does NOT reliably detect dark card/page backgrounds. On dark themes, it defaults to dark text — making ALL native text invisible. **MANDATORY**: Replace every `c60` font color reference across cards, navigation, headers, and components with `c58` (your light text color). See "Dark Mode Theme" section. This is the #1 dark mode failure.                                                                                                                                                                                                                                                                                                                                                                             |
| **Dark mode: font property names**                | Theme font properties use `family`, `weight`, `size`, `style` (not `fontFamily`/`fontWeight`/`fontSize`). Setting the wrong property names silently fails — fonts revert to theme defaults on next GET.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              |
| **Pro-code colors are NOT inherited**             | Pro-code components render in iframes and use their own CSS — they do NOT inherit the App Studio theme colors. When the theme palette changes, every pro-code component (banners, charts) must be manually updated with the new hex values AND republished via `domo publish`. Forgetting this creates jarring green-charts-on-copper-theme mismatches.                                                                                                                                                                                                                                                                                                                                                                                              |
| **Font family must match across all surfaces**    | The App Studio theme `fonts[].family` (Sans/Serif/Slab) must match all pro-code CSS `font-family` stacks. Mixing Serif native cards with Sans pro-code charts looks broken. When updating fonts, update BOTH the theme AND every pro-code `app.css`.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 |
| **Nav icons: use only catalog names**             | Domo uses its own internal icon set (133 verified names). Google Material icon names like `inventory_2`, `assignment_return`, `trending_up` render as blank/invisible. See the "Complete Domo icon catalog" section above. Always pick from the verified catalog.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    |
| **Chart types require `badge_` prefix**           | All native chart type names use the `badge_` prefix: `badge_vert_bar` (not `bar`), `badge_two_trendline` (not `line`), `badge_pie` (not `pie`), etc. Using short names like `"chartType": "bar"` causes `400 Bad Request` with no detail. See the Quick Reference table above or `card-creation/SKILL.md` for the full catalog of 207 chart type names.                                                                                                                                                                                                                                                                                                                                                                                              |
| **`badge_line` always returns 400**               | `badge_line` is the only known broken chart type — always returns HTTP 400 on creation regardless of body structure. Use `badge_two_trendline` (full-featured, 203 overrides) or `badge_spark_line` (compact, 40 overrides) instead. Verified broken as of February 2026.                                                                                                                                                                                                                                                                                                                                                                                                                                                                            |
| **`badge_area` is not a valid type**              | There is no `badge_area` chart type. Use `badge_vert_area_overlay` for standard area charts, `badge_vert_curved_area_overlay` for curved area, or `badge_stackedtrend` for stacked area. All area types use the `badge_vert_*` or `badge_horiz_*` prefix pattern.                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   |


### Layout Update Debugging Checklist

If a layout update returns `400 Bad Request`, check these in order:

1. **Missing template entries**: Compare content keys (from `content` array) with template keys (from `standard.template`). Every content key must appear in both `standard` and `compact` templates.
2. **Missing appendix artifacts**: Check for `PAGE_BREAK` and `SEPARATOR` entries in the existing template that have `contentKey` values NOT in the `content` array. These must be preserved.
3. **Template key mismatch**: Ensure the same set of `contentKey` values appears in `standard.template` and `compact.template`.
4. **Children field**: Every template entry must include `"children": null` (or be omitted). Observed in all working layouts.
5. **Missing layoutId in body**: The CLI requires `layoutId` in the body JSON to build the lock/PUT/unlock URLs.

```python
# Debugging helper — run this before any layout update
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

---

## Endpoint Reference

| Operation | CLI command | Notes |
|---|---|---|
| List apps | `app-studio list` | |
| Get app | `app-studio get APP_ID` | Includes views, nav, theme |
| Create app | `app-studio create --body-file` | Returns dataAppId + landingViewId |
| Update app | `app-studio update APP_ID --body-file` | Full body required |
| Create view | `app-studio create-view APP_ID --body-file` | Returns view + layout |
| **List views** | *(use `app-studio get`, read `views[]`)* | Dedicated endpoint is dead (405) |
| Get layout | `app-studio layout-get APP_ID VIEW_ID` | |
| Update layout | `app-studio layout-set APP_ID VIEW_ID --body-file` | Auto write lock |
| Get navigation | `pages nav-get` | Instance-wide |
| Reorder pages | `pages nav-reorder --body` | |
| List page cards | `pages list-cards PAGE_ID` | |
| Add card to page | `pages add-card PAGE_ID CARD_ID` | Goes to appendix |
| Create card | `cards create --page-id PAGE_ID --body-file` | Goes to appendix |
| Update card | `cards update CARD_ID --body-file` | |
| Read card definition | `cards definition CARD_ID` | Fix format mismatches before write |
| Dataset schema | `datasets schema DATASET_ID` | |
| Upload file/icon | `files upload --file-path FILE` | |
| DomoApps context | `domoapps context-create --body-file` | |
| DomoApps card | `domoapps card-create --page-id PAGE_ID --body` | |
| Create variable | `beast-modes create --body-file` | Set `variable: true` |
