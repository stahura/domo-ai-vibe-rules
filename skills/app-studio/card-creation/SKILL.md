---
name: card-creation
description: Domo Product API for KPI card CRUD — chart types, columns, beast modes, overrides; curl and session auth patterns.
---

# Domo Card CRUD API Reference

> **CLI vs API**: The Java CLI supports `backup-card` and `restore-card` for duplicating existing cards to new pages. **Try CLI first** for simple card copy operations. Fall back to this REST API when you need to create cards from scratch with full control over chart type, columns, beast modes, and overrides — or when CLI `restore-card` fails (it does not support all chart types).

Complete reference for programmatic KPI card management via the Domo Product API.
Verified February 2026 against live Domo instance. All 207 chart types documented with complete override data. 206/207 confirmed working for card creation (only `badge_line` fails). All edit operations (title, description, aliases, overrides, chart type changes) verified working.

> **Source code**: `gemini/documentation/_shared/tools/domo_card_tools.py` (10 tool functions, production-ready)
> **Last verified**: 2026-02-27

---

## Table of Contents

1. [CRUD Endpoints](#1-crud-endpoints)
2. [Complete Body Schema](#2-complete-body-schema)
3. [Column Mapping](#3-column-mapping)
4. [Beast Modes](#4-beast-modes)
5. [Chart Types Reference](#5-chart-types-reference)
6. [Conditional Formats](#6-conditional-formats)
7. [Code Examples](#7-code-examples)
8. [Gotchas](#8-gotchas)

---

## 1. CRUD Endpoints

**Base URL**: `https://{instance}.domo.com/api`
**Auth Header**: `X-Domo-Authentication: {SID}` (preferred — use a session SID from `domo login` / ryuu token exchange) or `X-DOMO-Developer-Token: {your_token}` (fallback — some endpoints reject dev tokens; SID works universally)
**Content-Type**: `application/json`

| Operation | Method | Endpoint | Notes |
|-----------|--------|----------|-------|
| **CREATE** | `PUT` | `/content/v3/cards/kpi?pageId=:pageId` | `pageId` query param is REQUIRED. No card ID in path. |
| **READ** | `PUT` | `/content/v3/cards/kpi/definition` | Unusual: uses PUT for a read. Body required (see below). |
| **UPDATE** | `PUT` | `/content/v3/cards/kpi/:cardId` | `cardId` in path. No `pageId` needed. Full body replacement. |
| **COPY** | `POST` | `/content/v1/cards/:id/copy` | Body: `{}`. Returns complete new card object. |
| **DELETE** | `DELETE` | `/content/v1/cards/:id` | No request body needed. Permanent, cannot be undone. |

### READ Request Body

The READ endpoint is unusual -- it uses PUT, not GET, and requires a specific body:

```json
{
  "dynamicText": true,
  "variables": true,
  "urn": "CARD_ID_HERE"
}
```

### Supporting Endpoints

| Operation | Method | Endpoint | Purpose |
|-----------|--------|----------|---------|
| Search datasets | `POST` | `/data/ui/v3/datasources/search` | Find datasets by name |
| Get schema | `GET` | `/query/v1/datasources/:id/schema/indexed?includeHidden=true` | Column names and types |
| Query SQL | `POST` | `/query/v1/execute/:datasetId` | Run SQL against dataset |
| Create beast mode | `POST` | `/query/v1/functions/template?strict=false` | Create calculated field |
| Add to workspace | `POST` | `/nav/v1/workspaces/bulk/execute` | Add card to workspace |

---

## 2. Complete Body Schema

This is the exact structure required for CREATE and UPDATE operations. Copied from the verified `_build_card_body()` function.

```json
{
  "definition": {
    "subscriptions": {
      "big_number": {
        "name": "big_number",
        "columns": [
          {
            "column": "Revenue",
            "aggregation": "SUM",
            "alias": "Revenue",
            "format": {"type": "abbreviated", "format": "#A"}
          }
        ],
        "filters": []
      },
      "main": {
        "name": "main",
        "columns": [
          {"column": "Team", "mapping": "ITEM"},
          {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM"}
        ],
        "filters": [],
        "orderBy": [],
        "groupBy": [{"column": "Team"}],
        "fiscal": false,
        "projection": false,
        "distinct": false
      }
    },
    "formulas": {
      "dsUpdated": [],
      "dsDeleted": [],
      "card": []
    },
    "annotations": {
      "new": [],
      "modified": [],
      "deleted": []
    },
    "conditionalFormats": {
      "card": [],
      "datasource": []
    },
    "controls": [],
    "segments": {
      "active": [],
      "create": [],
      "update": [],
      "delete": []
    },
    "charts": {
      "main": {
        "component": "main",
        "chartType": "badge_vert_bar",
        "overrides": {},
        "goal": null
      }
    },
    "dynamicTitle": {
      "text": [{"text": "My Card Title", "type": "TEXT"}]
    },
    "dynamicDescription": {
      "text": [{"text": "Card description here", "type": "TEXT"}],
      "displayOnCardDetails": true
    },
    "chartVersion": "12",
    "inputTable": false,
    "noDateRange": false,
    "title": "My Card Title",
    "description": "Card description here"
  },
  "dataProvider": {
    "dataSourceId": "DATASET_UUID_HERE"
  },
  "variables": true,
  "columns": false
}
```

### Field-by-Field Explanation

#### Root Level

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `definition` | object | Yes | Contains all card configuration |
| `dataProvider.dataSourceId` | string | Yes | Dataset UUID. **Must use `dataSourceId`, NOT `dsId`!** |
| `variables` | boolean | Yes | **Must be `true`**. Required for API to work correctly. |
| `columns` | boolean | Yes | **Must be `false`**. Required for API to work correctly. |

#### definition.subscriptions.big_number

Controls the summary number shown at the top of the card. The subscription object is always required, but its `columns` array should be **empty for single-value chart types** (`badge_singlevalue`) since the card itself already displays the number — populating `big_number` would show it twice.

For all other chart types (bars, lines, tables, etc.), populate `columns` with the first VALUE column from `main`.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Always `"big_number"` |
| `columns` | array | Empty `[]` for `badge_singlevalue`. First VALUE column for all other chart types. |
| `columns[].column` | string | Column name (for dataset columns) |
| `columns[].formulaId` | string | Beast mode ID (for calculated fields) |
| `columns[].aggregation` | string | `SUM`, `AVG`, `COUNT`, `MIN`, `MAX` |
| `columns[].alias` | string | Display name |
| `columns[].format` | object | `{"type": "abbreviated", "format": "#A"}` |
| `filters` | array | Always `[]` for big_number |

#### definition.subscriptions.main

The primary data subscription. This is where columns, filters, and groupings live.

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Always `"main"` |
| `columns` | array | All column definitions with mappings (see Section 3) |
| `filters` | array | Filter objects (see below) |
| `orderBy` | array | Sort definitions |
| `groupBy` | array | Auto-built from ITEM and SERIES columns: `[{"column": "Name"}]` |
| `fiscal` | boolean | Use fiscal calendar (`false` default) |
| `projection` | boolean | Enable projections (`false` default) |
| `distinct` | boolean | Distinct values only (`false` default) |

**Filter object structure:**
```json
{
  "column": "Type",
  "values": ["New Business"],
  "filterType": "LEGACY",
  "operand": "IN"
}
```

#### definition.formulas

Beast mode (calculated field) storage.

| Field | Type | Description |
|-------|------|-------------|
| `dsUpdated` | array | Dataset-level formulas that were updated |
| `dsDeleted` | array | Dataset-level formulas that were deleted |
| `card` | array | **Card-level beast modes** (see Section 4) |

#### definition.annotations

| Field | Type | Description |
|-------|------|-------------|
| `new` | array | New annotations |
| `modified` | array | Modified annotations |
| `deleted` | array | Deleted annotations |

#### definition.conditionalFormats

**CRITICAL: Must be an object, NOT an array.**

| Field | Type | Description |
|-------|------|-------------|
| `card` | array | Card-level conditional formatting rules |
| `datasource` | array | Dataset-level conditional formatting rules |

#### definition.controls

Array of interactive filter controls. Empty array `[]` for most cards.

#### definition.segments

**CRITICAL: Must be an object, NOT an array.**

| Field | Type | Description |
|-------|------|-------------|
| `active` | array | Currently active segments |
| `create` | array | Segments to create |
| `update` | array | Segments to update |
| `delete` | array | Segments to delete |

#### definition.charts.main

| Field | Type | Description |
|-------|------|-------------|
| `component` | string | Always `"main"` |
| `chartType` | string | One of 207 documented types (see Section 5) |
| `overrides` | object | Chart styling overrides (key-value pairs) |
| `goal` | null/object | Goal line configuration |

#### definition.dynamicTitle / dynamicDescription

```json
{
  "text": [{"text": "Title goes here", "type": "TEXT"}]
}
```

`dynamicDescription` also has `"displayOnCardDetails": true`.

#### Other definition fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `chartVersion` | string | `"12"` | Chart rendering version |
| `inputTable` | boolean | `false` | Whether card is an input table |
| `noDateRange` | boolean | `false` | Disable date range filtering |
| `title` | string | -- | Plain text title (also set dynamicTitle) |
| `description` | string | -- | Plain text description |

---

## 3. Column Mapping

Columns define what data appears in the card and how it maps to visual elements.

### Mapping Types

| Mapping | Visual Role | Required | Description |
|---------|-------------|----------|-------------|
| `ITEM` | X-axis / Category | Yes (most charts) | The dimension/category axis |
| `VALUE` | Y-axis / Measure | Yes | The numeric value being measured |
| `SERIES` | Color / Legend | No | Groups data into colored series |

### Column Object Structure

**For dataset columns:**
```json
{
  "column": "Team",
  "mapping": "ITEM",
  "aggregation": "SUM",
  "alias": "Team Name",
  "format": {"type": "number", "format": "###,##0"}
}
```

**For beast mode columns:**
```json
{
  "formulaId": "calculation_123456",
  "mapping": "VALUE",
  "aggregation": "SUM",
  "alias": "Win Rate %"
}
```

### Field Reference

| Field | Required | Description |
|-------|----------|-------------|
| `column` | Yes* | Column name from the dataset |
| `formulaId` | Yes* | Beast mode legacy ID (use instead of `column` for calculated fields) |
| `mapping` | Yes | `ITEM`, `VALUE`, or `SERIES` |
| `aggregation` | No | `SUM`, `AVG`, `COUNT`, `MIN`, `MAX`, `UNIQUE` |
| `alias` | No | Display name override |
| `format` | No | Number/date formatting object |

*One of `column` or `formulaId` is required.

### Examples by Chart Type

**Bar chart** (category + measure):
```json
[
  {"column": "Region", "mapping": "ITEM"},
  {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM"}
]
```

**Stacked bar** (category + measure + series):
```json
[
  {"column": "Region", "mapping": "ITEM"},
  {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM"},
  {"column": "Product Line", "mapping": "SERIES"}
]
```

**Single value** (measure only):
```json
[
  {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM", "alias": "Total Revenue"}
]
```

**Table** (multiple items):
```json
[
  {"column": "Name", "mapping": "ITEM"},
  {"column": "Department", "mapping": "ITEM"},
  {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM"},
  {"column": "Deals", "mapping": "VALUE", "aggregation": "COUNT"}
]
```

### groupBy Auto-Generation

The `groupBy` array in `subscriptions.main` is auto-built from ITEM and SERIES columns:
```python
group_by = []
for c in columns:
    if c.get("mapping") in ("ITEM", "SERIES") and "column" in c:
        group_by.append({"column": c["column"]})
```

---

## 4. Beast Modes

Beast Modes are Domo's calculated fields -- custom formulas that create new virtual columns from existing data.

### Card-Level vs Dataset-Level

| Scope | Storage | Visibility | How to Reference |
|-------|---------|------------|-----------------|
| **Card-level** | `definition.formulas.card[]` | Only on this card | Included inline in card body |
| **Dataset-level** | Created via API, stored on dataset | All cards using that dataset | Referenced by `formulaId` in column objects |

### Creating a Beast Mode (Dataset-Level)

**Endpoint**: `POST /query/v1/functions/template?strict=false`

```json
{
  "name": "Revenue per Deal",
  "owner": 705231757,
  "locked": false,
  "global": false,
  "expression": "SUM(`Distinct Closed Won ACV`) / COUNT(`Opportunity ID`)",
  "links": [
    {
      "resource": {"type": "DATA_SOURCE", "id": "DATASET_UUID"},
      "visible": true,
      "active": false,
      "valid": "VALID"
    }
  ],
  "aggregated": true,
  "analytic": false,
  "nonAggregatedColumns": [],
  "dataType": "DECIMAL",
  "status": "VALID",
  "cacheWindow": "non_dynamic",
  "columnPositions": [],
  "functions": [],
  "functionTemplateDependencies": [],
  "archived": false,
  "hidden": false,
  "variable": false
}
```

The response includes `id` (new UUID) and `legacyId` -- the `legacyId` is what you use as `formulaId` when referencing it in card columns.

### dataType Options

| Value | Use For |
|-------|---------|
| `DECIMAL` | Currency, percentages, ratios (default) |
| `LONG` | Whole numbers, counts |
| `DOUBLE` | High-precision decimals |
| `STRING` | Text/category results |
| `DATE` | Date calculations |

### Card-Level Beast Mode Structure

Card-level beast modes go in `definition.formulas.card[]` with full metadata including the formula expression, data type, and link to the dataset.

### Referencing in Columns

Once created, reference a beast mode by its `formulaId` (the `legacyId` from the creation response):

```json
{
  "formulaId": "calculation_123456789",
  "mapping": "VALUE",
  "aggregation": "SUM",
  "alias": "Revenue per Deal"
}
```

Note: Use `formulaId` instead of `column` -- they are mutually exclusive.

---

## 5. Chart Types Reference

Complete reference for all **207 chart types** available in Domo's card API. Every type listed below has been verified to have override options and is available for programmatic card creation. Data sourced from the complete chart type options extraction (`chart_type_options_complete.json`).

> **Important**: `badge_line` is the only known type that returns HTTP 400 on creation. Use `badge_two_trendline` or `badge_spark_line` instead.

### Summary Table -- All 207 Chart Types

| # | Chart Type | Overrides | Group |
|---|-----------|-----------|-------|
| 1 | `badge_vert_bar` | 171 | Bar |
| 2 | `badge_horiz_bar` | 152 | Bar |
| 3 | `badge_vert_stackedbar` | 178 | Bar |
| 4 | `badge_horiz_stackedbar` | 158 | Bar |
| 5 | `badge_vert_multibar` | 179 | Bar |
| 6 | `badge_horiz_multibar` | 147 | Bar |
| 7 | `badge_vert_nestedbar` | 129 | Bar |
| 8 | `badge_horiz_nestedbar` | 122 | Bar |
| 9 | `badge_vert_percentbar` | 104 | Bar |
| 10 | `badge_horiz_percentbar` | 101 | Bar |
| 11 | `badge_vert_100pct` | 125 | Bar |
| 12 | `badge_horiz_100pct` | 123 | Bar |
| 13 | `badge_vert_dual_stackedbar` | 123 | Bar |
| 14 | `badge_horiz_dual_stackedbar` | 118 | Bar |
| 15 | `badge_vert_rtbar` | 135 | Bar |
| 16 | `badge_horiz_rtbar` | 118 | Bar |
| 17 | `badge_vert_rtmultibar` | 136 | Bar |
| 18 | `badge_horiz_rtmultibar` | 118 | Bar |
| 19 | `badge_vert_rtstackedbar` | 142 | Bar |
| 20 | `badge_horiz_rtstackedbar` | 124 | Bar |
| 21 | `badge_vert_bar_overlay` | 123 | Bar |
| 22 | `badge_horiz_bar_overlay` | 117 | Bar |
| 23 | `badge_vert_symbol` | 134 | Bar |
| 24 | `badge_spark_bar` | 35 | Bar |
| 25 | `badge_trendline` | 180 | Line |
| 26 | `badge_two_trendline` | 203 | Line |
| 27 | `badge_curvedline` | 194 | Line |
| 28 | `badge_stepline` | 163 | Line |
| 29 | `badge_symbolline` | 190 | Line |
| 30 | `badge_rttrendline` | 144 | Line |
| 31 | `badge_stackedtrend` | 136 | Line |
| 32 | `badge_variance_line` | 143 | Line |
| 33 | `badge_spark_line` | 40 | Line |
| 34 | `badge_curved_symbolline` | 194 | Line |
| 35 | `badge_horiz_trendline` | 142 | Line |
| 36 | `badge_horiz_curvedline` | 142 | Line |
| 37 | `badge_horiz_stepline` | 138 | Line |
| 38 | `badge_horiz_symbolline` | 141 | Line |
| 39 | `badge_horiz_curved_symbolline` | 141 | Line |
| 40 | `badge_horiz_stackedtrend` | 131 | Line |
| 41 | `badge_line_bar` | 147 | Combo |
| 42 | `badge_line_stackedbar` | 147 | Combo |
| 43 | `badge_line_clusterbar` | 144 | Combo |
| 44 | `badge_vert_bar_line` | 131 | Combo |
| 45 | `badge_horiz_bar_line` | 126 | Combo |
| 46 | `badge_curved_line_bar` | 130 | Combo |
| 47 | `badge_curved_line_stackedbar` | 136 | Combo |
| 48 | `badge_horiz_line_bar` | 127 | Combo |
| 49 | `badge_horiz_line_clusterbar` | 129 | Combo |
| 50 | `badge_horiz_line_stackedbar` | 133 | Combo |
| 51 | `badge_vert_100pct_linebar` | 131 | Combo |
| 52 | `badge_horiz_100pct_linebar` | 127 | Combo |
| 53 | `badge_vert_nested_linebar` | 137 | Combo |
| 54 | `badge_horiz_nested_linebar` | 132 | Combo |
| 55 | `badge_symbol_bar` | 138 | Combo |
| 56 | `badge_symbol_stackedbar` | 144 | Combo |
| 57 | `badge_horiz_symbol_bar` | 124 | Combo |
| 58 | `badge_horiz_symbol_stackedbar` | 130 | Combo |
| 59 | `badge_vert_area_overlay` | 109 | Area |
| 60 | `badge_horiz_area_overlay` | 107 | Area |
| 61 | `badge_vert_100pct_area` | 92 | Area |
| 62 | `badge_horiz_100pct_area` | 91 | Area |
| 63 | `badge_vert_curved_area_overlay` | 109 | Area |
| 64 | `badge_horiz_curved_area_overlay` | 107 | Area |
| 65 | `badge_vert_curved_stacked_area` | 112 | Area |
| 66 | `badge_horiz_curved_stacked_area` | 110 | Area |
| 67 | `badge_vert_curved_100pct_area` | 92 | Area |
| 68 | `badge_horiz_curved_100pct_area` | 91 | Area |
| 69 | `badge_vert_step_area_overlay` | 109 | Area |
| 70 | `badge_horiz_step_area_overlay` | 107 | Area |
| 71 | `badge_vert_step_stacked_area` | 133 | Area |
| 72 | `badge_horiz_step_stacked_area` | 131 | Area |
| 73 | `badge_vert_step_100pct_area` | 92 | Area |
| 74 | `badge_horiz_step_100pct_area` | 91 | Area |
| 75 | `badge_vert_dotplot_overlay` | 121 | Dot Plot |
| 76 | `badge_horiz_dotplot_overlay` | 117 | Dot Plot |
| 77 | `badge_vert_multi_dotplot` | 144 | Dot Plot |
| 78 | `badge_horiz_multi_dotplot` | 139 | Dot Plot |
| 79 | `badge_vert_stacked_dotplot` | 149 | Dot Plot |
| 80 | `badge_horiz_stacked_dotplot` | 144 | Dot Plot |
| 81 | `badge_vert_line_multi_dotplot` | 131 | Dot Plot |
| 82 | `badge_horiz_line_multi_dotplot` | 125 | Dot Plot |
| 83 | `badge_vert_line_stacked_dotplot` | 134 | Dot Plot |
| 84 | `badge_horiz_line_stacked_dotplot` | 128 | Dot Plot |
| 85 | `badge_pie` | 47 | Pie/Donut/Rose |
| 86 | `badge_donut` | 51 | Pie/Donut/Rose |
| 87 | `badge_nautilus` | 44 | Pie/Donut/Rose |
| 88 | `badge_nautilus_donut` | 40 | Pie/Donut/Rose |
| 89 | `badge_nightingale_rose` | 41 | Pie/Donut/Rose |
| 90 | `badge_basic_table` | 131 | Tables |
| 91 | `badge_pivot_table` | 135 | Tables |
| 92 | `badge_flex_table` | 71 | Tables |
| 93 | `badge_table` | 70 | Tables |
| 94 | `badge_heatmap_table` | 74 | Tables |
| 95 | `badge_singlevalue` | 25 | Single Value / Gauges |
| 96 | `badge_filledgauge` | 35 | Single Value / Gauges |
| 97 | `badge_gauge` | 51 | Single Value / Gauges |
| 98 | `badge_facegauge` | 11 | Single Value / Gauges |
| 99 | `badge_shapegauge` | 58 | Single Value / Gauges |
| 100 | `badge_compgauge` | 20 | Single Value / Gauges |
| 101 | `badge_compfillgauge_basic` | 15 | Single Value / Gauges |
| 102 | `badge_compfillgauge_adv` | 15 | Single Value / Gauges |
| 103 | `badge_progressbar` | 20 | Single Value / Gauges |
| 104 | `badge_radial_progress` | 24 | Single Value / Gauges |
| 105 | `badge_multi_radial_progress` | 15 | Single Value / Gauges |
| 106 | `badge_in_range_gauge` | 22 | Single Value / Gauges |
| 107 | `badge_imagegauge` | 4 | Single Value / Gauges |
| 108 | `badge_bullet` | 98 | Single Value / Gauges |
| 109 | `badge_multi_value` | 69 | Multi-Value |
| 110 | `badge_multi_value_cols` | 63 | Multi-Value |
| 111 | `badge_world_map` | 113 | Maps |
| 112 | `badge_map` | 116 | Maps |
| 113 | `badge_map_us_state` | 116 | Maps |
| 114 | `badge_map_us_county` | 116 | Maps |
| 115 | `badge_map_latlong` | 27 | Maps |
| 116 | `badge_map_latlong_route` | 19 | Maps |
| 117 | `badge_map_africa` | 114 | Maps |
| 118 | `badge_map_asia` | 114 | Maps |
| 119 | `badge_map_australia` | 114 | Maps |
| 120 | `badge_map_austria` | 114 | Maps |
| 121 | `badge_map_brazil` | 114 | Maps |
| 122 | `badge_map_canada` | 114 | Maps |
| 123 | `badge_map_chile` | 114 | Maps |
| 124 | `badge_map_china` | 114 | Maps |
| 125 | `badge_map_europe` | 114 | Maps |
| 126 | `badge_map_france` | 114 | Maps |
| 127 | `badge_map_france2016` | 114 | Maps |
| 128 | `badge_map_france_dept` | 115 | Maps |
| 129 | `badge_map_germany` | 114 | Maps |
| 130 | `badge_map_ghana` | 114 | Maps |
| 131 | `badge_map_india` | 114 | Maps |
| 132 | `badge_map_indonesia` | 114 | Maps |
| 133 | `badge_map_italy` | 114 | Maps |
| 134 | `badge_map_japan` | 114 | Maps |
| 135 | `badge_map_malaysia` | 114 | Maps |
| 136 | `badge_map_mexico` | 114 | Maps |
| 137 | `badge_map_middle_east` | 114 | Maps |
| 138 | `badge_map_new_zealand` | 114 | Maps |
| 139 | `badge_map_nigeria` | 114 | Maps |
| 140 | `badge_map_north_america` | 114 | Maps |
| 141 | `badge_map_panama` | 114 | Maps |
| 142 | `badge_map_peru` | 114 | Maps |
| 143 | `badge_map_philippines` | 114 | Maps |
| 144 | `badge_map_portugal` | 114 | Maps |
| 145 | `badge_map_south_america` | 114 | Maps |
| 146 | `badge_map_south_korea` | 114 | Maps |
| 147 | `badge_map_spain` | 114 | Maps |
| 148 | `badge_map_switzerland` | 114 | Maps |
| 149 | `badge_map_uae` | 114 | Maps |
| 150 | `badge_map_uk_area` | 114 | Maps |
| 151 | `badge_map_uk_postal` | 114 | Maps |
| 152 | `badge_map_united_kingdom` | 114 | Maps |
| 153 | `badge_treemap` | 67 | Specialty |
| 154 | `badge_funnel` | 38 | Specialty |
| 155 | `badge_funnel_bars` | 7 | Specialty |
| 156 | `badge_funnel_swing` | 9 | Specialty |
| 157 | `badge_waffle` | 32 | Specialty |
| 158 | `badge_word_cloud` | 16 | Specialty |
| 159 | `badge_stream` | 64 | Specialty |
| 160 | `badge_stream_funnel` | 61 | Specialty |
| 161 | `badge_slope` | 67 | Specialty |
| 162 | `badge_bump` | 77 | Specialty |
| 163 | `badge_pareto` | 52 | Specialty |
| 164 | `badge_heatmap` | 97 | Specialty |
| 165 | `badge_gantt` | 80 | Gantt/Calendar |
| 166 | `badge_gantt_dep` | 85 | Gantt/Calendar |
| 167 | `badge_gantt_percent` | 80 | Gantt/Calendar |
| 168 | `badge_calendar` | 89 | Gantt/Calendar |
| 169 | `badge_ds_forecasting` | 132 | Data Science |
| 170 | `badge_ds_outliers` | 107 | Data Science |
| 171 | `badge_ds_pred_modeling` | 109 | Data Science |
| 172 | `badge_ds_spc` | 153 | Data Science |
| 173 | `badge_correlation_matrix` | 45 | Data Science |
| 174 | `badge_confusion_matrix` | 16 | Data Science |
| 175 | `badge_pop_trendline` | 107 | Period over Period |
| 176 | `badge_pop_trendline_var` | 119 | Period over Period |
| 177 | `badge_pop_rttrendline` | 137 | Period over Period |
| 178 | `badge_pop_bar_line` | 109 | Period over Period |
| 179 | `badge_pop_bar_line_var` | 121 | Period over Period |
| 180 | `badge_pop_line_bar` | 109 | Period over Period |
| 181 | `badge_pop_line_bar_var` | 122 | Period over Period |
| 182 | `badge_pop_vert_multibar` | 107 | Period over Period |
| 183 | `badge_pop_filledgauge` | 32 | Period over Period |
| 184 | `badge_pop_shapegauge` | 56 | Period over Period |
| 185 | `badge_pop_multi_value` | 55 | Period over Period |
| 186 | `badge_pop_progressbar` | 8 | Period over Period |
| 187 | `badge_pop_flex_table` | 70 | Period over Period |
| 188 | `badge_vert_histogram` | 33 | Histogram |
| 189 | `badge_horiz_histogram` | 32 | Histogram |
| 190 | `badge_vert_boxplot` | 107 | Box Plot |
| 191 | `badge_horiz_boxplot` | 88 | Box Plot |
| 192 | `badge_vert_waterfall` | 104 | Waterfall |
| 193 | `badge_horiz_waterfall` | 106 | Waterfall |
| 194 | `badge_xy_line` | 119 | Scatter/Bubble |
| 195 | `badge_xybubble` | 141 | Scatter/Bubble |
| 196 | `badge_checkbox_selector` | 13 | Selectors/Controls |
| 197 | `badge_date_selector` | 20 | Selectors/Controls |
| 198 | `badge_dropdown_selector` | 8 | Selectors/Controls |
| 199 | `badge_radio_selector` | 13 | Selectors/Controls |
| 200 | `badge_range_selector` | 7 | Selectors/Controls |
| 201 | `badge_slicer` | 19 | Selectors/Controls |
| 202 | `badge_textbox` | 13 | Text/Display |
| 203 | `badge_dynamic_textbox` | 23 | Text/Display |
| 204 | `badge_vert_marimekko` | 77 | Marimekko |
| 205 | `badge_horiz_marimekko` | 78 | Marimekko |
| 206 | `badge_vert_facetedbar` | 101 | Faceted Bar |
| 207 | `badge_horiz_facetedbar` | 89 | Faceted Bar |

---

### 5.1 Bar Charts (24 types)

Standard, stacked, nested, percent, multi-axis, running total, overlay, and symbol bar variants.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_bar` | 171 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_horiz_bar` | 152 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_stackedbar` | 178 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, regression_line, last_value_projection, multi-period_projection, colors, gradient_colors |
| `badge_horiz_stackedbar` | 158 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_multibar` | 179 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_horiz_multibar` | 147 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_nestedbar` | 129 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_nestedbar` | 122 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_percentbar` | 104 | general, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_percentbar` | 101 | general, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_100pct` | 125 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_100pct` | 123 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_dual_stackedbar` | 123 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_dual_stackedbar` | 118 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_rtbar` | 135 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, multi-period_projection, gradient_colors, colors |
| `badge_horiz_rtbar` | 118 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_rtmultibar` | 136 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, multi-period_projection, gradient_colors, colors |
| `badge_horiz_rtmultibar` | 118 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_rtstackedbar` | 142 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, multi-period_projection, gradient_colors, colors |
| `badge_horiz_rtstackedbar` | 124 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_bar_overlay` | 123 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_(left), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_bar_overlay` | 117 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_symbol` | 134 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_spark_bar` | 35 | general, value_options, change_value_options, hover_text_settings, number_format, colors |

**Notable overrides unique to bar charts:**
- `width_percentage` / `height_percentage` -- Control bar thickness
- `fixed_bar_width` / `fixed_bar_height` -- Absolute bar sizing
- `allow_wide_bars` / `allow_tall_bars` -- Allow bars to exceed default width
- `datalabel_show_total` -- Show stacked bar totals
- `regression_line` -- Trend line on bar charts (vert_bar, vert_stackedbar)
- `last_value_projection` / `multi-period_projection` -- Forecasting on bar charts
- `value_scale_(left)` / `value_scale_(right)` -- Dual Y axes on multibar
- `show_as_trellis` -- Small multiples / trellis mode

---

### 5.2 Line Charts (16 types)

Trend lines, curved lines, step lines, symbol lines, stacked trends, and variance lines.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_trendline` | 180 | general, legend, grid_lines, data_label_settings, value_scale_y, line_labels_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_two_trendline` | 203 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), line_labels_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, total_line, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_curvedline` | 194 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), line_labels_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_stepline` | 163 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), category_scale_x, hover_text_settings, hints, data_table, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_symbolline` | 190 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_rttrendline` | 144 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), line_labels_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, multi-period_projection, gradient_colors, colors |
| `badge_stackedtrend` | 136 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_variance_line` | 143 | general, actual_line, target_line, legend, grid_lines, data_label_settings, value_scale_(left), line_labels_(right), category_scale_x, hover_text_settings, hints, number_format, scale_marker |
| `badge_spark_line` | 40 | general, value_options, change_value_options, line_options, hover_text_settings, number_format, colors |
| `badge_curved_symbolline` | 194 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), line_labels_(right), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, outlier_filtering, scale_marker_range, scale_marker, regression_line, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_horiz_trendline` | 142 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_horiz_curvedline` | 142 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_horiz_stepline` | 138 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_horiz_symbolline` | 141 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_horiz_curved_symbolline` | 141 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, outlier_filtering, scale_marker, gradient_colors, colors |
| `badge_horiz_stackedtrend` | 131 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |

**Notable overrides unique to line charts:**
- `line_style` -- Solid, Dashed, Dotted
- `line_thickness` -- Line weight
- `outlier_filtering` -- `outliers_above`, `outliers_below` to filter outlier data points
- `scale_marker_range` -- Shaded range bands (`sm_min_val`, `sm_max_val`, `mkr_color`)
- `total_line` -- Show aggregated total line (badge_two_trendline)
- `line_labels_(right)` -- `show_line_labels`, `right_label_scale_display`
- `actual_line` / `target_line` -- Variance line actual vs target styling
- `show_linear_regression` -- Trend/regression line overlay
- `last_value_projection` / `multi-period_projection` -- Forecasting projections

---

### 5.3 Combo Charts (18 types)

Line + bar, symbol + bar, curved line + bar, and nested line + bar combinations.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_line_bar` | 147 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, last_bar_value_projection, last_line_value_projection, gradient_colors, colors |
| `badge_line_stackedbar` | 147 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_line_clusterbar` | 144 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_bar_line` | 131 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_bar, value_scale_line, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_bar_line` | 126 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_bar, value_scale_line, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_curved_line_bar` | 130 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_curved_line_stackedbar` | 136 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_line_bar` | 127 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_line_clusterbar` | 129 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_line_stackedbar` | 133 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_100pct_linebar` | 131 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_100pct_linebar` | 127 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_nested_linebar` | 137 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_nested_linebar` | 132 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_symbol_bar` | 138 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_symbols, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_symbol_stackedbar` | 144 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_symbols, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_symbol_bar` | 124 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_symbols, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_symbol_stackedbar` | 130 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_symbols, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |

**Notable overrides unique to combo charts:**
- `set_line_count` -- Number of series rendered as lines vs bars
- `value_scale_line` / `value_scale_bar` -- Separate Y axes for line and bar
- `value_scale_symbols` -- Dedicated scale for symbol overlays
- `last_bar_value_projection` -- Bar-specific projection (`project_bar_val_method`, `proj_bar_value`)
- `last_line_value_projection` -- Line-specific projection (`project_line_val_method`, `proj_line_value`)
- `title_line` / `title_bar` -- Separate axis titles for line and bar scales

---

### 5.4 Area Charts (16 types)

Overlay, stacked, 100% area, with curved and step variants in both vertical and horizontal orientations.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_area_overlay` | 109 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_area_overlay` | 107 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_100pct_area` | 92 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, gradient_colors, colors |
| `badge_horiz_100pct_area` | 91 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_vert_curved_area_overlay` | 109 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_curved_area_overlay` | 107 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_curved_stacked_area` | 112 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_curved_stacked_area` | 110 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_curved_100pct_area` | 92 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, gradient_colors, colors |
| `badge_horiz_curved_100pct_area` | 91 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_vert_step_area_overlay` | 109 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_step_area_overlay` | 107 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_step_stacked_area` | 133 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_step_stacked_area` | 131 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_step_100pct_area` | 92 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, gradient_colors, colors |
| `badge_horiz_step_100pct_area` | 91 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |

**Notable overrides unique to area charts:**
- Area charts share standard chart overrides (grid_lines, data_labels, scales)
- No bar_settings (unlike bar and combo charts)
- Vertical variants include `data_table`; horizontal variants do not
- 100% area variants omit `scale_marker` (value axis is always 0-100%)
- Curved, step, and standard line interpolation variants share identical override structures

---

### 5.5 Dot Plot Charts (10 types)

Single, multi-series, stacked, and line+dot combinations.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_dotplot_overlay` | 121 | general, legend, grid_lines, data_label_settings, value_scale_(left), category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_dotplot_overlay` | 117 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_multi_dotplot` | 144 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_multi_dotplot` | 139 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_stacked_dotplot` | 149 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_stacked_dotplot` | 144 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_line_multi_dotplot` | 131 | general, legend, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_line_multi_dotplot` | 125 | general, legend, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |
| `badge_vert_line_stacked_dotplot` | 134 | general, legend, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, trellis_tiered_date_settings, data_table, number_format, scale_marker, gradient_colors, colors |
| `badge_horiz_line_stacked_dotplot` | 128 | general, legend, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_y, hover_text_settings, hints, trellis_tiered_date_settings, number_format, scale_marker, gradient_colors, colors |

**Notable overrides unique to dot plot charts:**
- Dot plots use standard axis/grid/label overrides (no bar_settings)
- Line + dot variants have dual scales: `value_scale_line` and `value_scale_bar`
- Stacked dot plots have the highest override counts in the group (149 vert, 144 horiz)
- All dot plot types support trellis_tiered_date_settings for small multiples

---

### 5.6 Pie / Donut / Rose (5 types)

Circular charts including standard pie, donut, nautilus spiral, and nightingale rose.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_pie` | 47 | general, legend, hover_legend, data_label_settings, hover_text_settings, number_format, gradient_colors, colors |
| `badge_donut` | 51 | general, legend, hover_legend, data_label_settings, hover_text_settings, number_format, gradient_colors, colors |
| `badge_nautilus` | 44 | general, legend, hover_legend, data_label_settings, hover_text_settings, number_format, gradient_colors, colors |
| `badge_nautilus_donut` | 40 | general, legend, hover_legend, hover_text_settings, number_format, gradient_colors, colors |
| `badge_nightingale_rose` | 41 | general, legend, hover_legend, data_label_settings, number_format, gradient_colors, colors |

**Notable overrides unique to pie/donut/rose:**
- `max_before_other` -- Number of slices before grouping into "Other"
- `other_fill_color` -- Color for the "Other" slice
- `border_color` -- Slice border color
- `hide_pie_labels` -- Toggle slice labels
- `legend_value` -- Show values in the legend
- `hvr_legend_title_text` / `hvr_legend_title_value` -- Hover legend customization
- `hide_hover_legend` -- Toggle hover legend panel

---

### 5.7 Tables (5 types)

Basic, pivot, flex, standard, and heatmap table variants.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_basic_table` | 131 | general, row_height, sorting, header_row, total_row, subtotal_rows, alignment, colors, heatmap, excel_export |
| `badge_pivot_table` | 135 | general, row_height, sorting, header_row, header_col, totals, subtotals, colors, excel_export |
| `badge_flex_table` | 71 | general, column_definitions, header_row, graph_settings, graph_data_label_settings, change_value_options, regression_line, colors |
| `badge_table` | 70 | general, header_row, total_row, subtotal_rows, alignment, attribute, colors |
| `badge_heatmap_table` | 74 | theme, general, scale, header_row, total_row, subtotal_rows, alignment, attribute, colors |

**Notable overrides unique to tables:**
- `padding` / `header_padding` / `total_padding` -- Row height controls
- `enable_sorting` / `alphanumeric_sorting` -- Interactive sorting
- `header_row_fill_color` / `header_row_font_color` -- Header styling
- `total_row` / `total_row_label` / `total_row_suppress_count` -- Total row config
- `subtotal_rows` / `all_group_names` -- Subtotal grouping
- `use_heatmap_colors` / `color_theme` / `range_by_column` -- Heatmap mode (basic_table)
- `column_definitions` -- Inline chart config (flex_table)
- `graph_settings` / `graph_data_label_settings` -- Inline chart styling (flex_table)
- `excel_export_row_limit` -- Export limits
- `use_logscale` -- Log scale for heatmap_table

---

### 5.8 Single Value & Gauges (14 types)

Big numbers, filled gauges, radial gauges, shape gauges, progress bars, and comparison gauges.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_singlevalue` | 25 | general, header_footer, hover_text_settings, number_format, colors |
| `badge_filledgauge` | 35 | general, target, min_max, number_format |
| `badge_gauge` | 51 | general, value_label, radial_labels, range_1 through range_6 |
| `badge_facegauge` | 11 | general, green_range, yellow_range, red_range |
| `badge_shapegauge` | 58 | general, range_1 through range_10, out_of_range, data_label_settings, hover_text_settings |
| `badge_compgauge` | 20 | general, hover_text_settings, number_format |
| `badge_compfillgauge_basic` | 15 | general, hover_text_settings, number_format |
| `badge_compfillgauge_adv` | 15 | general, hover_text_settings, number_format |
| `badge_progressbar` | 20 | general, color_range_1 through color_range_4 |
| `badge_radial_progress` | 24 | general, hover_text_settings, color_range_1 through color_range_4 |
| `badge_multi_radial_progress` | 15 | general, data_label_settings, hover_text_settings |
| `badge_in_range_gauge` | 22 | general, fixed_values, value_text, range_text, label_text |
| `badge_imagegauge` | 4 | general |
| `badge_bullet` | 98 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, colors |

**Notable overrides unique to gauges:**
- `value_type` / `value_format` / `value_label` -- Value display config
- `target_value` / `target_label` / `target_line_color` -- Target line (filledgauge)
- `min_value` / `max_value` / `hide_min_value` / `hide_max_value` -- Gauge range
- `radial_style` / `radial_indicator` -- Gauge appearance (gauge)
- `range1_min` through `range10_max` / `range1_color` through `range10_color` -- Up to 10 color ranges (shapegauge)
- `out_of_range_fill_color` / `out_of_range_symbol` -- Out-of-range handling (shapegauge)
- `shape_bkg_fill` -- Shape background (shapegauge)
- `green_range` / `yellow_range` / `red_range` -- Traffic light ranges (facegauge)
- `color_direction` / `gauge_val_displayed` -- Comparison gauge config
- `fill_color` / `bkg_ring_style` / `bkg_ring_fill_color` -- Radial progress styling
- `image_fit` / `default_imageurl` / `url_prefix` -- Image gauge (imagegauge, only 4 overrides)
- `gauge_style` / `gauge_width_pct` / `in_rng_fill_color` -- In-range gauge config

---

### 5.9 Multi-Value (2 types)

Multi-metric summary cards with individual value formatting.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_multi_value` | 69 | general, title_options, value_options, change_value_options, additional_text_options, date_grain_options, tooltip_options, number_format |
| `badge_multi_value_cols` | 63 | general, title_options, value_options, change_value_options, additional_text_options, tooltip_options, number_format |

**Notable overrides unique to multi-value:**
- `gauge_layout` / `gauge_sizing` / `item_padding` -- Layout configuration
- `title_text` / `title_font_color` / `title_font_family` -- Per-value title styling
- `hide_single_value` / `single_value_type` / `value_font_color` -- Value display
- `hide_change_value` / `comp_val_displayed` / `comp_data_used` -- Comparison value config
- `addl_text` / `addl_text_font_color` -- Additional text per metric
- `show_date_grain` / `date_grain_font_color` -- Date grain display (multi_value only)
- `tooltip1_value_type` through `tooltip3_value_type` -- Tooltip metric selection

---

### 5.10 Maps (42 types)

World map, US state/county, lat/long, route, and 36 country-specific maps.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_world_map` | 113 | theme, general, diverging, hover_legend, data_label_settings, hover_text, values, number_format, ranges, cities |
| `badge_map` | 116 | theme, general, diverging, hover_legend, data_label_settings, hover_text, values, number_format, ranges, cities |
| `badge_map_us_state` | 116 | theme, general, diverging, hover_legend, data_label_settings, hover_text, values, number_format, ranges, cities |
| `badge_map_us_county` | 116 | theme, general, diverging, hover_legend, data_label_settings, hover_text, values, number_format, ranges, cities |
| `badge_map_latlong` | 27 | general, symbols, scale, legend, hover_text, background, cities |
| `badge_map_latlong_route` | 19 | general, routes, scale, legend, hover_text, background, cities |

**Country/region maps** (all 114 overrides, identical categories: theme, general, diverging, hover_legend, data_label_settings, hover_text, values, number_format, ranges, cities):

`badge_map_africa`, `badge_map_asia`, `badge_map_australia`, `badge_map_austria`, `badge_map_brazil`, `badge_map_canada`, `badge_map_chile`, `badge_map_china`, `badge_map_europe`, `badge_map_france`, `badge_map_france2016`, `badge_map_france_dept` (115), `badge_map_germany`, `badge_map_ghana`, `badge_map_india`, `badge_map_indonesia`, `badge_map_italy`, `badge_map_japan`, `badge_map_malaysia`, `badge_map_mexico`, `badge_map_middle_east`, `badge_map_new_zealand`, `badge_map_nigeria`, `badge_map_north_america`, `badge_map_panama`, `badge_map_peru`, `badge_map_philippines`, `badge_map_portugal`, `badge_map_south_america`, `badge_map_south_korea`, `badge_map_spain`, `badge_map_switzerland`, `badge_map_uae`, `badge_map_uk_area`, `badge_map_uk_postal`, `badge_map_united_kingdom`

**Notable overrides unique to maps:**
- `color_theme` / `use_custom_gradient_colors` / `num_colors` -- Choropleth theming
- `balanced_distribution` / `auto_zoom` / `hide_no_data_items` -- Map behavior
- `show_diverging` / `diverging_range_count` / `midpoint_value_type` -- Diverging color scale
- `range_1_text` / `range_1_min` / `range_1_max` -- Manual range definitions
- `show_cities` -- City markers overlay
- `hover_always_on_map` -- Persistent hover tooltips
- `symbol_color` / `symbol_size` / `symbol_transparency` -- Lat/long point styling
- `map_bkg_color` / `bkg_area_fill_color` / `ocean_fill_color` -- Map background (latlong)
- `routes` -- Route path config (latlong_route)
- `region_stroke_color` -- Border styling (latlong)

---

### 5.11 Specialty (12 types)

Treemap, funnel, waffle, word cloud, stream, slope, bump, pareto, and heatmap.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_treemap` | 67 | general, label_settings, hover_legend, hover_text_settings, color_value_settings, diverging, color_ranges, gradient_colors, colors |
| `badge_funnel` | 38 | general, legend, data_label_settings, hover_text_settings, number_format, gradient_colors, colors |
| `badge_funnel_bars` | 7 | general, gradient_colors |
| `badge_funnel_swing` | 9 | general, gradient_colors |
| `badge_waffle` | 32 | general, label, percentage_value, hover_text_settings, color_range_1 through color_range_4 |
| `badge_word_cloud` | 16 | general, gradient_colors |
| `badge_stream` | 64 | general, legend, data_label_settings, category_scale_x, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_stream_funnel` | 61 | general, legend, data_label_settings, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_slope` | 67 | general, legend, data_label_settings, left_scale_(y), right_scale_(y), category_scale_x, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_bump` | 77 | general, legend, data_label_settings, rank_scale, label_scale, category_scale_x, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_pareto` | 52 | general, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hints, number_format, gradient_colors |
| `badge_heatmap` | 97 | general, legend, diverging, data_label_settings, category_scale_y, category_scale_x, total_row_col, hover_text_settings, number_format, ranges, theme |

**Notable overrides unique to specialty charts:**
- `text_position` / `label_text` -- Treemap label placement
- `default_color_theme` / `force_max_value` -- Treemap color value settings
- `series_height` / `legacy_funnel` -- Funnel sizing
- `fnl_display_in_legend` / `fnl_legend_pct` -- Funnel legend with percentages
- `larger_rank_higher` -- Bump chart rank direction
- `rank_scale` / `label_scale` -- Bump chart dedicated scales
- `left_scale_(y)` / `right_scale_(y)` -- Slope chart dual Y scales
- `total_row_col` -- Heatmap totals row/column

---

### 5.12 Gantt / Calendar (4 types)

Project timeline, dependency, percent complete, and calendar heatmap.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_gantt` | 80 | general, legend, bar_settings, data_label_settings, category_scale_y, time_scale_(x), hover_text_settings, scale_marker, gradient_colors, colors |
| `badge_gantt_dep` | 85 | general, duration, legend, bar_settings, data_label_settings, category_scale_y, time_scale_(x), hover_text_settings, scale_marker, gradient_colors, colors |
| `badge_gantt_percent` | 80 | general, legend, bar_settings, data_label_settings, category_scale_y, time_scale_(x), hover_text_settings, scale_marker, gradient_colors, colors |
| `badge_calendar` | 89 | general, legend, hover_text_settings, ranges, number_format, theme |

**Notable overrides unique to Gantt/calendar:**
- `x_time_scale_show_weekends` -- Show/hide weekends on time axis
- `gantt_time_scale_show_labels` -- Time axis labels
- `x_time_scale_pos` -- Time axis position
- `height_percentage` -- Gantt bar height
- `hover_date_output_format` -- Date format in tooltips
- `duration_type` / `hours_in_day` / `weekends_included_in_duration` -- Duration config (gantt_dep only)
- `ranges` / `color_theme` -- Calendar heatmap color ranges

---

### 5.13 Data Science (6 types)

Forecasting, outlier detection, predictive modeling, SPC control charts, and correlation/confusion matrices.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_ds_forecasting` | 132 | general, legend, grid_lines, data_label_settings, value_scale_y, value_scale_x, hover_text_settings, hints, number_format, scale_marker, colors |
| `badge_ds_outliers` | 107 | general, grid_lines, data_label_settings, value_scale_y, value_scale_x, hover_text_settings, hints, number_format, scale_marker, colors |
| `badge_ds_pred_modeling` | 109 | general, grid_lines, data_label_settings, value_scale_y, value_scale_x, hover_text_settings, hints, number_format, scale_marker, colors |
| `badge_ds_spc` | 153 | general, control_chart_rules, limit_lines, legend, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, data_table, number_format, scale_marker, regression_line, colors |
| `badge_correlation_matrix` | 45 | general, legend, data_label_settings, category_scale_y, category_scale_x, hover_text_settings, number_format |
| `badge_confusion_matrix` | 16 | general |

**Notable overrides unique to data science charts:**
- `spc_symbol_type` -- SPC chart data point symbol
- `control_chart_rules` -- SPC out-of-control rules (`spc_rule_beyond_limits`, `spc_beyond_limits_fill_color`)
- `limit_lines` -- SPC control limits (`spc_avg_line_color`, `spc_ul_line_color`, `spc_avg_line_style`)
- `spc_ooc_fill_color` -- Out-of-control point color
- `spc_legend_show` -- SPC-specific legend toggle
- Data science charts use both `value_scale_y` and `value_scale_x` (XY-style axes)

---

### 5.14 Period over Period (13 types)

Trend lines, bar+line combos, gauges, multi-value, and tables with period comparison.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_pop_trendline` | 107 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_trendline_var` | 119 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_rttrendline` | 137 | general, legend, grid_lines, data_label_settings, value_scale_(left), value_scale_(right), category_scale_x, hover_text_settings, hints, data_table, number_format, outlier_filtering, scale_marker_range, multi-period_projection, gradient_colors, colors |
| `badge_pop_bar_line` | 109 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_bar_line_var` | 121 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_bar, value_scale_line, category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_line_bar` | 109 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, colors, scale_marker, gradient_colors |
| `badge_pop_line_bar_var` | 122 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_line, value_scale_bar, category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_vert_multibar` | 107 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_pop_filledgauge` | 32 | general, previous_period, min_max, number_format |
| `badge_pop_shapegauge` | 56 | general, range_1 through range_10, out_of_range, data_label_settings, hover_text_settings |
| `badge_pop_multi_value` | 55 | general, title_options, value_options, change_value_options, additional_text_options, number_format |
| `badge_pop_progressbar` | 8 | general |
| `badge_pop_flex_table` | 70 | general, column_definitions, header_row, graph_settings, graph_data_label_settings, change_value_options, regression_line, colors |

**Notable overrides unique to period-over-period:**
- `_var` suffix types have dual value scales for variance display
- `previous_period` category -- `hide_target_label`, `target_label`, `target_line_color` (pop_filledgauge)
- `range_by_val_or_pct` -- Range definition method (pop_shapegauge)
- PoP types mirror their base chart types but with period comparison built in
- `line_width` (instead of `line_thickness`) in some PoP line types

---

### 5.15 Histogram (2 types)

Frequency distribution charts.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_histogram` | 33 | general, bar_settings, grid_lines, bottom_scale, hints, scale_marker, gradient_colors |
| `badge_horiz_histogram` | 32 | general, bar_settings, grid_lines, hints, scale_marker, gradient_colors |

**Notable overrides unique to histograms:**
- `histogram_bins` -- Number of bins/buckets
- `symbol_color` -- Bar color (in bar_settings, not in a colors category)
- `bottom_scale` / `cat_scale_manual_rotate` -- Axis label rotation
- No legend, data_label_settings, or number_format categories (minimal config)

---

### 5.16 Box Plot (2 types)

Statistical distribution visualization with quartiles, median, and outliers.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_boxplot` | 107 | general, grid_lines, data_label_settings, value_scale_y, category_scale_x, hints, hover_text_settings, number_format, scale_marker |
| `badge_horiz_boxplot` | 88 | general, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker |

**Notable overrides unique to box plots:**
- Standard axis/grid/label overrides only -- no legend, colors, or gradient categories
- No trellis/tiered date settings
- No regression line or projection capabilities

---

### 5.17 Waterfall (2 types)

Running total visualizations showing incremental positive and negative contributions.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_waterfall` | 104 | general, bar_settings, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, scale_marker, bar_colors |
| `badge_horiz_waterfall` | 106 | general, bar_settings, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, scale_marker, bar_colors |

**Notable overrides unique to waterfall charts:**
- `sum_initial_group` / `initial_group_text` -- Initial value bar config
- `show_summary_bars` -- Summary/subtotal bars
- `summary_datalabel_text` / `summary_hover_text` -- Summary bar labels
- `bar_colors` category (unique to waterfall):
  - `start_bar_color_from_value` -- Color bars by positive/negative
  - `start_bar_fill_color` / `end_bar_fill_color` -- Start/end bar colors
  - Positive, negative, and subtotal bar colors

---

### 5.18 Scatter / Bubble (2 types)

XY scatter plots and bubble charts with size dimension.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_xy_line` | 119 | general, legend, grid_lines, data_label_settings, value_scale_y, value_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |
| `badge_xybubble` | 141 | general, legend, regression, quadrant_lines, grid_lines, data_label_settings, value_scale_y, value_scale_x, hover_text_settings, hints, number_format, scale_marker, gradient_colors, colors |

**Notable overrides unique to scatter/bubble:**
- `no_auto_sort` -- Disable automatic data sorting (xy_line)
- `regression` category -- `show_regression_lines`, `regression_line_style`, `regression_line_thickness`
- `quadrant_lines` -- `x_scale_value`, `y_scale_value` reference lines creating 4 quadrants
- Both `value_scale_y` and `value_scale_x` (XY axes, not category + value)
- `legend_position` -- Full position control (not just top/bottom)

---

### 5.19 Selectors / Controls (6 types)

Interactive filter controls for dashboard interactivity.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_checkbox_selector` | 13 | general, hover_label |
| `badge_date_selector` | 20 | general, calendar_view, presets_view |
| `badge_dropdown_selector` | 8 | general |
| `badge_radio_selector` | 13 | general, hover_label |
| `badge_range_selector` | 7 | general |
| `badge_slicer` | 19 | general, hover_label |

**Notable overrides unique to selectors:**
- `view_search` -- Enable search within selector (checkbox, radio, slicer)
- `show_hover_label` -- Hover label visibility
- `starting_view` / `selected_fill_color` -- Date selector appearance
- `calendar_view` -- `highlight_today`, `view`, `dates_from` (date_selector)
- `presets_view` -- `presets_only`, `presets_style`, `hide_day_presets` (date_selector)
- `allow_multi_select` -- Multi-select toggle (dropdown_selector)
- `dropdown_label_text` / `dropdown_label_pos` -- Dropdown label config
- `selector_fill_color` / `use_integers_only` -- Range selector config

#### Selector Card Subscription Requirements

**CRITICAL**: Selector cards MUST have a non-empty `big_number.columns` array. An empty `columns` array causes `400 {"message":"big_number subscription missing select columns"}`.

For dropdown/checkbox/radio/slicer selectors, use `COUNT` aggregation on the filtering column:

```python
"big_number": {
    "name": "big_number",
    "columns": [{"column": "PlantName", "aggregation": "COUNT",
                 "alias": "PlantName",
                 "format": {"type": "abbreviated", "format": "#A"}}],
    "filters": [],
}
```

For date selectors, use `MAX` aggregation on the date column:

```python
"big_number": {
    "name": "big_number",
    "columns": [{"column": "OrderDate", "aggregation": "MAX",
                 "alias": "OrderDate",
                 "format": {"type": "abbreviated", "format": "#A"}}],
    "filters": [],
}
```

The `main` subscription provides the values for the selector:
- Dropdown/checkbox/radio: `columns: [{"column": "PlantName", "mapping": "ITEM"}]` with `groupBy: [{"column": "PlantName"}]`
- Date selector: `columns: [{"column": "OrderDate", "mapping": "ITEM"}]` with `groupBy: []` (empty)

#### App Studio Filter Card Best Practices

When used as page-level filters in App Studio, filter cards MUST be **extremely low-profile** — transparent background, no borders, minimal height. They are controls, not content, and should blend into the page without competing visually with heroes or charts.

| Content property | Value | Why |
|-----------------|-------|-----|
| `hideSummary` | `true` | Hides the distracting count above the dropdown |
| `hideMargins` | `true` | Removes internal padding for tight fit |
| `fitToFrame` | `true` | Scales the control to fill its frame |
| `hideTitle` | `true` | Hide card title — dropdown already renders its own field label. Avoids redundant/coded text. |
| `hideDescription` | `true` | Not needed for filter controls |
| `hideFooter` | `true` | Not needed for filter controls |
| `hideTimeframe` | `true` | Not needed for filter controls |
| `hideBorder` | `true` | Removes card border for seamless look |
| `style` | `null` | **NO colored style.** Do NOT use `ca3` or any themed style. Transparent/default only. Colored backgrounds (green, blue, etc.) make filters visually polarizing. |

Use standard template height of **6** (not 10) for minimal vertical footprint.

#### Global Card Styling (MANDATORY)

All cards in App Studio MUST follow the zero-chrome reference configuration. Apply via theme update:

| Setting | Value | API property |
|---------|-------|-------------|
| Rounded corners | **0 px** | `borderRadius: 0` |
| Border weight | **0 px** | `borderWidth: 0` |
| Drop shadow | **None** | `dropShadow: 'NONE'` |
| Card inner padding | **0 px** | `padding: {left:0, right:0, top:0, bottom:0}` |
| Content spacing | **Nil** | `contentSpacing: None` |
| Header bottom spacing | **0 px** | `headerBottomSpacing: 0` |

These are applied globally to all card styles (ca1–ca8) via the theme `cards` array. See `app-studio` skill § "Card Styles" for the full implementation.

---

### 5.20 Text / Display (2 types)

Static and dynamic text content cards.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_textbox` | 13 | general |
| `badge_dynamic_textbox` | 23 | general, change_value_options |

**Notable overrides unique to text/display:**
- `text` -- The actual text content (supports rich text)
- `gauge_sizing` -- Auto or fixed sizing
- `abbrev_values` -- Abbreviate inline values (dynamic_textbox)
- `apply_chg_val_to_first` / `apply_chg_val_to_last` / `apply_chg_val_to_min` -- Change value application (dynamic_textbox)

---

### 5.21 Marimekko (2 types)

Proportional area charts showing both category share and segment composition.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_marimekko` | 77 | general, legend, grid_lines, data_label_settings, value_scale_y, category_scale_x, hover_text_settings, hints, number_format, gradient_colors, colors |
| `badge_horiz_marimekko` | 78 | general, legend, grid_lines, data_label_settings, value_scale_x, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |

**Notable overrides unique to marimekko:**
- Standard axis/grid/label overrides (similar to bar charts)
- No bar_settings category (bar widths are proportional to data)
- No trellis, regression, or projection capabilities

---

### 5.22 Faceted Bar (2 types)

Small multiples bar charts with separate panels per category.

| Chart Type | Overrides | Key Categories |
|-----------|-----------|----------------|
| `badge_vert_facetedbar` | 101 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale, label_scale, category_scale_x, hover_text_settings, hints, data_table, number_format, last_value_projection, multi-period_projection, gradient_colors, colors |
| `badge_horiz_facetedbar` | 89 | general, legend, bar_settings, grid_lines, data_label_settings, value_scale_x, label_scale, category_scale_y, hover_text_settings, hints, number_format, gradient_colors, colors |

**Notable overrides unique to faceted bar:**
- `facet_bar_space_percent` -- Space between faceted panels
- `label_scale` -- Dedicated scale for facet labels (`hide_labels`, `label_scale_position`)
- `value_scale` (generic, not _y or _x) on vertical variant

---

### Common Override Categories

Most chart types share a standard set of override categories. Here is what each controls:

| Category | Purpose | Key Overrides |
|----------|---------|---------------|
| **general** | Fonts, sorting, limits | `default_font_family` (Sans/Serif/Slab/Condensed/Monospace), `font_size` (Smaller/Larger/Largest), `total_sort` (Ascending/Descending/A-Z/Z-A), `display_limit`, `hide_interactivity`, `disable_animation` |
| **legend** | Legend position and styling | `lrg_legend_position` (Top/Bottom/Hide), `details_legend_position` (Auto/Right/Bottom/Top/Hide), `legend_font_family`, `legend_font_size` |
| **bar_settings** | Bar width/height | `width_percentage`, `fixed_bar_width`, `allow_wide_bars` |
| **grid_lines** | Grid, zero lines, calculated lines | `hide_value_gridlines`, `grid_line_color`, `zero_line_color`, `calculated_line` (Median/Average), `show_max_line`, `show_min_line` |
| **data_label_settings** | Value labels on chart | `show_data_label` (Always/Always - Rotated), `datalabel_position` (Outside Top/Inside Top/Center), `datalabel_fnt_clr` (Gray/Black/White/Complimentary), `datalabel_font_size`, `decimal_places_dl` |
| **value_scale_y** | Y-axis formatting | `title_y`, `label_format_y` (Number/Currency/Percentage), `divide_value_scale_by_y` (Thousands/Millions/Billions), `value_scale_min`, `value_scale_max`, `log_scale_y`, `include_zero_y` |
| **category_scale_x** | X-axis formatting | `title_x`, `cat_scale_show_labels` (Always/Never), `cat_scale_manual_rotate` (30 Degrees/90 Degrees), `max_label_length`, `never_use_time_scale` |
| **hover_text_settings** | Tooltip formatting | `hover_text`, `hover_format` (Number/Currency/Percentage), `decimal_places_hvr` |
| **number_format** | Currency/decimal config | `currency_symbol`, `currency_sym_position` (Before/After), `decimal_separator`, `thousands_separator` |
| **gradient_colors** | Color gradients | `use_gradient_colors`, `gradient_start_fill_color`, `gradient_end_fill_color`, `gradient_by_value`, `reverse_gradient_direction` |
| **scale_marker** | Reference lines/ranges | `sm_type` (Line/Range/Quantiles), `sm_val_type` (Manual/Average/Median/Percentile), `sm_value`, `sm_line_color`, `sm_line_style` (Solid/Dashed) |
| **regression_line** | Trend lines | `show_linear_regression`, `regression_line_style` (Dashed/Solid), `regression_line_thickness` |
| **trellis_tiered_date_settings** | Small multiples | `show_as_trellis` (Trellis Categories/Tiered Dates), `date_grouping` (2 Levels/3 Levels) |
| **colors** | Series colors | `series_1_color` (hex string) |

### Override Value Types

| Type | Format | Example |
|------|--------|---------|
| `boolean` | `"true"` or `"false"` (as strings) | `"use_gradient_colors": "true"` |
| `string` | Free text or hex color | `"gradient_start_fill_color": "#99CCEEFF"` |
| `float` | Number as string | `"display_limit": "10"` |
| `select_list` | One of the predefined values | `"font_size": "Largest"` |

**All override values are strings**, even booleans and numbers.

---

## 6. Conditional Formats

Conditional formats allow color-coding values based on rules. The structure **must be an object**, not an array.

### Required Structure

```json
"conditionalFormats": {
  "card": [],
  "datasource": []
}
```

### Conditional Format Rule Structure

```json
{
  "card": [
    {
      "type": "COLOR",
      "column": "Revenue",
      "rules": [
        {
          "min": 0,
          "max": 50000,
          "color": "#FF0000",
          "label": "Below Target"
        },
        {
          "min": 50000,
          "max": 100000,
          "color": "#FFAA00",
          "label": "Near Target"
        },
        {
          "min": 100000,
          "color": "#00AA00",
          "label": "Above Target"
        }
      ]
    }
  ],
  "datasource": []
}
```

### Common Mistakes

- Passing `conditionalFormats` as an array `[]` instead of object `{card:[], datasource:[]}` -- causes HTTP 400
- The Domo UI returns the format as an array when reading cards -- you must convert it to the object format before sending it back in an update

---

## 7. Code Examples

### Python: Create a Card

```python
import json
import urllib.request

INSTANCE = "domo.domo.com"
API_KEY = "your-developer-token"
PAGE_ID = "1227718422"
DATASET_ID = "d118d4fb-474a-487d-9e88-2b721a1b8a7f"

body = {
    "definition": {
        "subscriptions": {
            "big_number": {
                "name": "big_number",
                "columns": [{
                    "column": "Revenue",
                    "aggregation": "SUM",
                    "alias": "Revenue",
                    "format": {"type": "abbreviated", "format": "#A"}
                }],
                "filters": []
            },
            "main": {
                "name": "main",
                "columns": [
                    {"column": "Team", "mapping": "ITEM"},
                    {"column": "Revenue", "mapping": "VALUE", "aggregation": "SUM"}
                ],
                "filters": [],
                "orderBy": [],
                "groupBy": [{"column": "Team"}],
                "fiscal": False,
                "projection": False,
                "distinct": False
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
                "chartType": "badge_vert_bar",
                "overrides": {
                    "font_size": "Larger",
                    "use_gradient_colors": "true",
                    "gradient_start_fill_color": "#99CCEEFF"
                },
                "goal": None
            }
        },
        "dynamicTitle": {"text": [{"text": "Revenue by Team", "type": "TEXT"}]},
        "dynamicDescription": {"text": [], "displayOnCardDetails": True},
        "chartVersion": "12",
        "inputTable": False,
        "noDateRange": False,
        "title": "Revenue by Team",
        "description": ""
    },
    "dataProvider": {"dataSourceId": DATASET_ID},
    "variables": True,
    "columns": False
}

url = f"https://{INSTANCE}/api/content/v3/cards/kpi?pageId={PAGE_ID}"
headers = {
    "X-DOMO-Developer-Token": API_KEY,
    "Content-Type": "application/json"
}
data = json.dumps(body).encode()
req = urllib.request.Request(url, data=data, method="PUT", headers=headers)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print(f"Created card: {result['id']}")
```

### Python: Read a Card

```python
url = f"https://{INSTANCE}/api/content/v3/cards/kpi/definition"
body = {"dynamicText": True, "variables": True, "urn": "CARD_ID"}
data = json.dumps(body).encode()
req = urllib.request.Request(url, data=data, method="PUT", headers=headers)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    chart_type = result["definition"]["charts"]["main"]["chartType"]
    title = result["definition"]["dynamicTitle"]["text"][0]["text"]
    print(f"Card: {title} ({chart_type})")
```

### Python: Update a Card

```python
# Same body structure as CREATE, but endpoint includes cardId
url = f"https://{INSTANCE}/api/content/v3/cards/kpi/{CARD_ID}"
body["definition"]["title"] = "Updated Title"
body["definition"]["dynamicTitle"]["text"][0]["text"] = "Updated Title"
body["definition"]["charts"]["main"]["chartType"] = "badge_pie"

data = json.dumps(body).encode()
req = urllib.request.Request(url, data=data, method="PUT", headers=headers)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print(f"Updated card: {result['id']}")
```

### Python: Copy a Card

```python
url = f"https://{INSTANCE}/api/content/v1/cards/{CARD_ID}/copy"
data = json.dumps({}).encode()
req = urllib.request.Request(url, data=data, method="POST", headers=headers)

with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    print(f"Copied to new card: {result['id']}")
```

### Python: Delete a Card

```python
url = f"https://{INSTANCE}/api/content/v1/cards/{CARD_ID}"
req = urllib.request.Request(url, method="DELETE", headers=headers)

with urllib.request.urlopen(req) as resp:
    print(f"Deleted card {CARD_ID}")
```

### curl: Create a Card

```bash
curl -X PUT "https://domo.domo.com/api/content/v3/cards/kpi?pageId=1227718422" \
  -H "X-DOMO-Developer-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "definition": {
      "subscriptions": {
        "big_number": {
          "name": "big_number",
          "columns": [{"column":"Revenue","aggregation":"SUM","alias":"Revenue","format":{"type":"abbreviated","format":"#A"}}],
          "filters": []
        },
        "main": {
          "name": "main",
          "columns": [
            {"column":"Team","mapping":"ITEM"},
            {"column":"Revenue","mapping":"VALUE","aggregation":"SUM"}
          ],
          "filters": [], "orderBy": [], "groupBy": [{"column":"Team"}],
          "fiscal": false, "projection": false, "distinct": false
        }
      },
      "formulas": {"dsUpdated":[],"dsDeleted":[],"card":[]},
      "annotations": {"new":[],"modified":[],"deleted":[]},
      "conditionalFormats": {"card":[],"datasource":[]},
      "controls": [],
      "segments": {"active":[],"create":[],"update":[],"delete":[]},
      "charts": {"main":{"component":"main","chartType":"badge_vert_bar","overrides":{},"goal":null}},
      "dynamicTitle": {"text":[{"text":"Revenue by Team","type":"TEXT"}]},
      "dynamicDescription": {"text":[],"displayOnCardDetails":true},
      "chartVersion": "12", "inputTable": false, "noDateRange": false,
      "title": "Revenue by Team", "description": ""
    },
    "dataProvider": {"dataSourceId": "YOUR_DATASET_UUID"},
    "variables": true,
    "columns": false
  }'
```

### curl: Read a Card

```bash
curl -X PUT "https://domo.domo.com/api/content/v3/cards/kpi/definition" \
  -H "X-DOMO-Developer-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"dynamicText":true,"variables":true,"urn":"CARD_ID"}'
```

### curl: Copy a Card

```bash
curl -X POST "https://domo.domo.com/api/content/v1/cards/CARD_ID/copy" \
  -H "X-DOMO-Developer-Token: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### curl: Delete a Card

```bash
curl -X DELETE "https://domo.domo.com/api/content/v1/cards/CARD_ID" \
  -H "X-DOMO-Developer-Token: YOUR_TOKEN"
```

---

## 8. Gotchas

### Critical -- Will Cause Failures

| Gotcha | Details |
|--------|---------|
| **`dataProvider.dataSourceId` NOT `dsId`** | The field name is `dataSourceId`. Using `dsId` silently fails or creates a broken card. |
| **`variables: true` required at root** | Must be present at the root level of the request body. Without it, the API may return incomplete or broken results. |
| **`columns: false` required at root** | Must be present at the root level. Setting to `true` changes the response format and can break card creation. |
| **Both subscriptions required** | Must include BOTH `big_number` AND `main` subscriptions. Missing either causes HTTP 400. |
| **`conditionalFormats` must be object** | Must be `{"card":[], "datasource":[]}`. Passing `[]` (array) causes HTTP 400. |
| **`segments` must be object** | Must be `{"active":[], "create":[], "update":[], "delete":[]}`. Passing `[]` causes HTTP 400. |
| **`badge_line` fails** | Always returns HTTP 400. Use `badge_two_trendline` or `badge_spark_line` instead. |
| **CREATE requires `pageId`** | `PUT /content/v3/cards/kpi?pageId=:pageId` -- the `pageId` query parameter is mandatory. |
| **UPDATE uses NO `pageId`** | `PUT /content/v3/cards/kpi/:cardId` -- the card ID goes in the path, no `pageId` query param. |
| **READ uses PUT, not GET** | The read definition endpoint is `PUT /content/v3/cards/kpi/definition` -- an unusual PUT for what is logically a read operation. |

### Important -- Affects Behavior

| Gotcha | Details |
|--------|---------|
| **Override values are strings** | Even booleans (`"true"`, `"false"`) and numbers (`"10"`) must be passed as strings in the overrides object. |
| **UPDATE replaces entire definition** | The update endpoint does a full replacement. You must include ALL fields, not just the ones you want to change. Always read first, modify, then write back. |
| **READ→WRITE format mismatches** | The READ endpoint returns simplified formats that the WRITE endpoint rejects. Fix before updating: `formulas` (read=`[]`, write=`{"dsUpdated":[],"dsDeleted":[],"card":[]}`), `conditionalFormats` (read=`[]`, write=`{"card":[],"datasource":[]}`), `annotations` (read=`[]`, write=`{"new":[],"modified":[],"deleted":[]}`), `segments` (read=`{"active":[],"definitions":[]}`, write=`{"active":[],"create":[],"update":[],"delete":[]}`). Also add missing fields (`title`, `description`, `noDateRange`), remove read-only fields (`modified`, `allowTableDrill`), and always provide `dataProvider.dataSourceId`. |
| **SID auth works for v3 cards** | `X-Domo-Authentication: {SID}` works for all `/content/v3/cards/kpi` endpoints (create, read, update), not just `X-DOMO-Developer-Token`. |
| **`groupBy` auto-generation** | Build `groupBy` from all ITEM and SERIES columns. Missing this causes charts to display incorrectly (no grouping = all values aggregated into one). |
| **`big_number` auto-generation** | For most chart types, populate with the first VALUE column. **Exception: `badge_singlevalue`** — leave `columns: []` to avoid a duplicative summary number (the card itself is the number). |
| **PoP cards need `dateRangeFilter`** | `badge_pop_*` cards show "0" comparison unless: (1) date column in `main.columns` with `mapping:"ITEM"`, `aggregation:"MAX"`; (2) `dateRangeFilter` on the `main` subscription with `dateTimeRange` and `periods`; (3) `time_period` subscription with the same date column. If `dateGrain` exists on the subscription, remove it before adding `periods` (they conflict: "Cannot save dategrain with periods"). |
| **Workspace operations: one at a time** | When adding/removing cards from workspaces via `/nav/v1/workspaces/bulk/execute`, send one entity per request. Batch `contents` arrays cause HTTP 500. |
| **`badge_line` workaround** | Use `badge_spark_line` for compact line charts or `badge_two_trendline` for full-featured line charts. Both are verified working. |
| **Copy keeps same title** | `POST /content/v1/cards/:id/copy` duplicates everything including the title. Call update_card after to rename the copy. |
| **Delete is permanent** | `DELETE /content/v1/cards/:id` cannot be undone. Remove from workspaces first if needed. |

### Workspace API (Related)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| Add entity | `POST /nav/v1/workspaces/bulk/execute` | `operation: "ADD"` |
| Remove entity | `POST /nav/v1/workspaces/bulk/execute` | `operation: "REMOVE"` |
| List contents | `GET /nav/v1/workspaces/:guid/walk?includeDetails=true` | Browse workspace |
| Search | `POST /nav/v1/workspaces/:guid/addContentQuery` | Search within workspace |

Workspace entity types: `card`, `page`, `dataset`, `data_app`, `dataflow`, `workflow_model`.

---

## Appendix: Quick Reference Card

```
CREATE:  PUT  /content/v3/cards/kpi?pageId=PAGE_ID        (full body)
READ:    PUT  /content/v3/cards/kpi/definition             ({"dynamicText":true,"variables":true,"urn":"ID"})
UPDATE:  PUT  /content/v3/cards/kpi/CARD_ID                (full body)
COPY:    POST /content/v1/cards/CARD_ID/copy               ({})
DELETE:  DELETE /content/v1/cards/CARD_ID                   (no body)

Auth:    X-DOMO-Developer-Token: YOUR_TOKEN
Base:    https://{instance}.domo.com/api

Required root fields: variables=true, columns=false
Required data field:  dataProvider.dataSourceId (NOT dsId)
Required subscriptions: big_number AND main (big_number.columns=[] for badge_singlevalue)
conditionalFormats:   {card:[], datasource:[]}  (OBJECT, not array)
segments:             {active:[], create:[], update:[], delete:[]}  (OBJECT, not array)

Line charts:          badge_two_trendline (NOT badge_line)
Documented chart types: 207 total (206 work via API, badge_line fails)
```
