---
name: basic-app-studio
description: Lean App Studio automation via community-domo-cli — auth, conventions, and operational commands for apps, views, layouts, and cards without raw HTTP. Omits DELETE and deep reference tables (those live in advanced-app-studio). Use when you need copy-paste CLI steps and minimal prose for App Studio CRUD.
---

# App Studio Skill — CLI Edition

This is the `community-domo-cli` variant of the App Studio skill. Use this file instead of
`SKILL.md` when the CLI is available. All operations use CLI commands. No raw API calls or
destructive operations (DELETE) are included in this skill.

Key concepts are unchanged — see `SKILL.md` for Layout Structure, Card Styles, Theme Management,
Page Layout Patterns, and all reference tables. This file covers only the **operational API
surface**: how to invoke each operation.

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

## App Operations

### Create App

```bash
community-domo-cli --output json -y app-studio create \
  --body '{"title": "My Dashboard App", "description": "Description"}' \
  > app_response.json

APP_ID=$(python3 -c "import json; print(json.load(open('app_response.json'))['dataAppId'])")
PAGE_ID=$(python3 -c "import json; print(json.load(open('app_response.json'))['landingViewId'])")
```

The `landingViewId` is the `viewId` of the auto-created page, which doubles as `pageId` for
card and layout operations.

### Get App Structure

Returns views, navigations, theme, and all app-level settings.

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

**Key fields changeable via update**: `navOrientation` (`TOP`/`LEFT`/`BOTTOM`),
`showDomoNavigation`, `showNavigation`, `showTitle`, `showLogo`, `title`, `description`,
`iconDataFileId`, `navIconDataFileId`, `theme`.

The PUT does NOT update navigation labels/icons — use the navigation endpoint below for that.

### Custom App Icon

**Step 1 — Generate or prepare a 256×256 PNG** (see `SKILL.md` for the Pillow generator).

**Step 2 — Upload via CLI**

```bash
community-domo-cli --output json -y files upload --file-path icon.png > icon_response.json
DATA_FILE_ID=$(python3 -c "import json; print(json.load(open('icon_response.json'))['dataFileId'])")
```

**Step 3 — Set on the app** (include in the GET→modify→PUT flow above):

```python
app['iconDataFileId']    = data_file_id
app['navIconDataFileId'] = data_file_id  # same file for both
```

**Note**: The CLI uses `mimetypes.guess_type()` for content type. PNG files are correctly
detected as `image/png`. The CLI does not send `?name=&public=true` query params — the
`dataFileId` is still returned and works for icon assignment.

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

The response includes both `view` (with `pageId`) and `layout` (with `layoutId`). The new view
automatically gets a navigation entry.

---

## Navigation

Navigation cannot be updated via `app-studio update` — changes to `navigations[]` in the PUT
body are silently ignored. Use the `pages` CLI commands below.

> **Endpoint note**: The CLI `pages` commands use global Domo page navigation endpoints, which
> differ from the App Studio-specific navigation endpoints used in `SKILL.md`. For App Studio
> apps, these commands work for reading nav state and reordering pages. Icon and label updates
> for App Studio nav items are not supported by the current CLI commands.

### Read Navigation

```bash
community-domo-cli --output json pages nav-get > nav.json
```

Returns all navigation entries across the instance. Filter to your app's views by matching
`entityId` values against your `views[]` from `app-studio get`.

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

```bash
community-domo-cli --output json app-studio layout-get $APP_ID $VIEW_ID > layout.json

LAYOUT_ID=$(python3 -c "import json; print(json.load(open('layout.json'))['layoutId'])")
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

## Card Operations on Pages

### List Cards on a Page

```bash
community-domo-cli --output json pages list-cards $VIEW_ID > page_cards.json
```

Returns array of card objects with `id`, `title`, `type`, `urn`.

> **Endpoint note**: CLI uses `GET /content/v3/stacks/{pageId}/cards` (v3 stacks endpoint).
> Response shape may differ slightly from the v1 cards endpoint — same cards, different wrapper.

### Add an Existing Card to a Page

Cards added this way go to the **appendix**. Use `layout-set` to move them to the canvas.

```bash
community-domo-cli -y pages add-card $VIEW_ID $CARD_ID
# Returns empty body on success
```

### Add Card to the Domo Overview Page

The Domo overview/home page uses the special page ID `-100000`:

```bash
community-domo-cli -y pages add-card -- -100000 $CARD_ID
```

Note the `--` separator before the negative page ID to prevent it being parsed as a flag.

---

## Create a Card on a Page

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

**CRITICAL — `badge_line` is broken**: Always returns HTTP 400. Use `badge_two_trendline`
(full-featured) or `badge_spark_line` (compact) instead. `badge_area` is also not a valid
type — use `badge_vert_area_overlay` for area charts.

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

---

## Dataset Schema

Before creating cards, get the exact column names and types from the dataset:

```bash
community-domo-cli --output json datasets schema $DATASET_ID > schema.json

python3 -c "
import json
schema = json.load(open('schema.json'))
columns = schema['tables'][0]['columns']
for col in columns:
    print(f\"{col['name']:40s} {col['type']}\")
"
```

---

## Beast Modes and Variables

### Create a Variable (for App Studio variable controls)

```bash
python3 -c "
import json
body = {
    'name': 'Selected Region',
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

`FUNCTION_ID` (numeric) is used by pro-code apps via `domo.onVariablesUpdated` /
`domo.requestVariablesUpdate`. `LEGACY_ID` (`calculation_...`) is used in Beast Mode
references.

---

## Pro-Code Card Instances (DomoApps)

### Step 1 — Create a Context

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

For apps with no datasets (banners), use `"mapping": []`.

### Step 2 — Create the Card

```bash
community-domo-cli --output json -y domoapps card-create \
  --page-id $VIEW_ID \
  --body "{\"contextId\": \"$CONTEXT_ID\", \"id\": \"$CONTEXT_ID\"}" \
  > domoapps_card_response.json
```

The `id` field must be the **context ID**, NOT the design ID.

---

## Complete Workflow: Build a Full Dashboard App Programmatically

```bash
INSTANCE="myco.domo.com"
DATASET_ID="xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"

# 1. Create the app
community-domo-cli --output json -y app-studio create \
  --body '{"title": "Sales Dashboard", "description": "Sales performance metrics"}' \
  > app.json
APP_ID=$(python3 -c "import json; print(json.load(open('app.json'))['dataAppId'])")
PAGE_ID=$(python3 -c "import json; print(json.load(open('app.json'))['landingViewId'])")
echo "App: $APP_ID  Page: $PAGE_ID"

# 2. Discover dataset schema
community-domo-cli --output json datasets schema $DATASET_ID > schema.json
python3 -c "
import json
cols = json.load(open('schema.json'))['tables'][0]['columns']
print('Columns:', [(c['name'], c['type']) for c in cols[:5]])
"

# 3. Create cards (repeat for each card definition)
community-domo-cli --output json -y cards create \
  --body-file card_kpi.json --page-id $PAGE_ID > card1.json
CARD1=$(python3 -c "import json; print(json.load(open('card1.json'))['id'])")

# 4. Get layout and inspect content keys
community-domo-cli --output json app-studio layout-get $APP_ID $PAGE_ID > layout.json
python3 -c "
import json
layout = json.load(open('layout.json'))
print('layoutId:', layout['layoutId'])
for c in layout['content']:
    print(f\"  key={c['contentKey']} type={c['type']} card={c.get('cardId','')}\")
"

# 5. Build and apply the updated layout
python3 - <<'PYEOF'
import json

layout = json.load(open('layout.json'))
layout_id = layout['layoutId']

# Build your template arrays (see SKILL.md for grid system and sizing)
std_template = []
cmp_template = []
y, cy = 0, 0

# Header
std_template.append({"type":"HEADER","contentKey":1,"x":0,"y":y,"width":60,"height":4,"virtualAppendix":False,"virtual":False,"children":None})
cmp_template.append({"type":"HEADER","contentKey":1,"x":0,"y":cy,"width":12,"height":3,"virtualAppendix":False,"virtual":False,"children":None})
y += 4; cy += 3

# Update header text
for c in layout['content']:
    if c['type'] == 'HEADER' and c['contentKey'] == 1:
        c['text'] = 'Sales Overview'

# CRITICAL: preserve appendix artifacts (PAGE_BREAK, SEPARATOR template-only entries)
content_keys = {c['contentKey'] for c in layout['content']}
for entry in layout['standard']['template']:
    if entry['contentKey'] not in content_keys:
        std_template.append({**entry, 'virtual': True, 'virtualAppendix': True})
for entry in layout['compact']['template']:
    if entry['contentKey'] not in content_keys:
        cmp_template.append({**entry, 'virtual': True, 'virtualAppendix': True})

layout['standard']['template'] = std_template
layout['compact']['template'] = cmp_template
json.dump(layout, open('layout_updated.json', 'w'))
print('Layout written')
PYEOF

# 6. Apply layout — CLI handles write lock automatically
community-domo-cli --output json -y app-studio layout-set $APP_ID $PAGE_ID \
  --body-file layout_updated.json

echo "Done"
```

---

## Complete Workflow: Add Filter Cards to All Pages

### Step 1 — Create filter cards on the first page

```bash
community-domo-cli --output json -y cards create \
  --body-file filter_region.json --page-id $PAGE_ID > filter1.json
FILTER1=$(python3 -c "import json; print(json.load(open('filter1.json'))['id'])")
```

### Step 2 — Add same cards to other pages (goes to appendix)

```bash
for PAGE in $PAGE2 $PAGE3 $PAGE4; do
  community-domo-cli -y pages add-card $PAGE $FILTER1
done
```

### Step 3 — Move cards from appendix to canvas on each page

```bash
for PAGE in $PAGE2 $PAGE3 $PAGE4; do
  # Get layout
  community-domo-cli --output json app-studio layout-get $APP_ID $PAGE > layout_p.json

  # Modify layout (set virtualAppendix=false, virtual=false, set x/y/width/height)
  python3 - <<'PYEOF'
import json, sys
layout = json.load(open('layout_p.json'))
# ... position your filter cards ...
json.dump(layout, open('layout_p_updated.json', 'w'))
PYEOF

  # Apply — write lock handled by CLI
  community-domo-cli --output json -y app-studio layout-set $APP_ID $PAGE \
    --body-file layout_p_updated.json
done
```

---

## Endpoint Reference

| Operation | Method | CLI command | Raw API fallback |
|---|---|---|---|
| List apps | GET | `app-studio list` | — |
| Get app | GET | `app-studio get APP_ID` | — |
| Create app | POST | `app-studio create` | — |
| Update app | PUT | `app-studio update APP_ID` | — |
| Create view | POST | `app-studio create-view APP_ID` | — |
| **List views** | GET | *(use `app-studio get`, read `views[]`)* | 405 — endpoint dead |
| Get layout | GET | `app-studio layout-get APP_ID VIEW_ID` | — |
| Update layout | PUT | `app-studio layout-set APP_ID VIEW_ID` | — |
| **Write lock acquire** | PUT | *(handled by `layout-set`)* | `/content/v4/pages/layouts/{id}/writelock` |
| **Write lock release** | DELETE | *(handled by `layout-set`)* | `/content/v4/pages/layouts/{id}/writelock` |
| Get navigation | GET | `pages nav-get` | — |
| Reorder pages | PUT | `pages nav-reorder` | — |
| List page cards | GET | `pages list-cards PAGE_ID` | — |
| Add card to page | POST | `pages add-card PAGE_ID CARD_ID` | — |
| Create card | PUT | `cards create --page-id PAGE_ID` | — |
| Update card | PUT | `cards update CARD_ID` | — |
| Read card definition | PUT | `cards definition CARD_ID` | — |
| Dataset schema | GET | `datasets schema DATASET_ID` | — |
| Upload file/icon | POST | `files upload --file-path FILE` | — |
| DomoApps context | POST | `domoapps context-create` | — |
| DomoApps card | POST | `domoapps card-create --page-id PAGE_ID` | — |
| Create variable/beast mode | POST | `beast-modes create` | — |
