# Creating Magic ETL Dataflows Programmatically in Domo

## Overview

Magic ETL dataflows in Domo can be created, updated, and executed entirely through the API. The dataflow is defined as a JSON document describing a directed acyclic graph (DAG) of actions — input nodes, transforms, and output nodes.

**CLI-First: Use the Java CLI for read/run operations, fall back to REST API for creation.**

| Operation | Use CLI? | Use REST API? |
|-----------|----------|---------------|
| List dataflows | `list-dataflow -dt MAGIC` | — |
| Export dataflow definition | `list-dataflow -i <ID> -d -f <FILE>` | — |
| Run a dataflow | `dataflow-run-now -i <ID>` | `POST .../executions` (more reliable for new dataflows) |
| Check execution status | `list-dataflow -i <ID> -e -l 1` | `GET .../executions?limit=1` |
| **Create** a dataflow | `set-dataflow-properties -d <file> -c` (but gets 403 with dev tokens) | `POST /api/dataprocessing/v1/dataflows` (requires SID auth, creates in DRAFT) |
| **Update** a dataflow | `set-dataflow-properties -i <id> -d <file>` | `PUT /api/dataprocessing/v1/dataflows/<ID>` |
| **Rename/enable** | `set-dataflow-properties -i <id> -n/-e/-s` | `PUT /api/dataprocessing/v1/dataflows/<ID>/patch` |

**Important:** Creating dataflows via API (POST) requires SID auth and produces a DRAFT dataflow that cannot be executed until saved once in the Domo UI. The CLI's create command (`-d <file> -c`) calls the same endpoint but fails with dev token auth (403). The CLI can export, rename, enable/disable, and run existing dataflows.

## CLI Commands for Dataflows

### List All Magic ETL Dataflows

```
list-dataflow -dt MAGIC
```

### Get a Dataflow Definition (Export to JSON)

```
list-dataflow -i <DATAFLOW_ID> -d -f <OUTPUT_FILE>
```

This exports the full JSON definition including all actions, inputs, outputs, and GUI positions. This is the best way to understand the JSON structure — export an existing dataflow and study it.

### Run a Dataflow

```
dataflow-run-now -i <DATAFLOW_ID>
```

### List Dataflow Executions

```
list-dataflow -i <DATAFLOW_ID> -e -l <LIMIT>
```

### Check Execution Status via API

```bash
curl -s "https://<instance>.domo.com/api/dataprocessing/v1/dataflows/<ID>/executions?limit=1&offset=0" \
  -H "x-domo-developer-token: <TOKEN>"
```

Returns execution state (`SUCCESS`, `FAILED_DATA_FLOW`, `CREATED`, `RUNNING`), row counts, errors, etc.

## Creating a Dataflow via the API

### Endpoint

```
POST https://<instance>.domo.com/api/dataprocessing/v1/dataflows
```

**Auth (March 2026):** This endpoint requires **SID-based auth**, not developer tokens. Developer tokens get 403 Forbidden. Use the SID exchange: refresh token → `oauth2/token` → access token → `oauth2/sid` → SID.

Headers:
```
Content-Type: application/json
X-Domo-Authentication: <SID>
```

The body **must** include `"databaseType": "MAGIC"`. The created dataflow will be in DRAFT state — see Gotcha #7 and #11 for limitations.

> **Note:** `x-domo-developer-token` works for GET (list/read) and for updating/running **existing** (non-DRAFT) dataflows, but not for POST (create).

### Updating an Existing Dataflow

```
PUT https://<instance>.domo.com/api/dataprocessing/v1/dataflows/<DATAFLOW_ID>
```

Same headers and body format as POST. Include the full definition.

## Dataflow JSON Structure

### Top-Level Fields

```json
{
  "name": "My Magic ETL",
  "databaseType": "MAGIC",
  "responsibleUserId": 149955692,
  "draft": false,
  "enabled": true,
  "runState": "ENABLED",
  "engineProperties": {
    "kettle.mode": "STRICT"
  },
  "inputs": [ ... ],
  "outputs": [ ... ],
  "actions": [ ... ]
}
```

| Field | Description |
|---|---|
| `name` | Display name of the dataflow |
| `databaseType` | Must be `"MAGIC"` for Magic ETL |
| `responsibleUserId` | Numeric user ID of the owner |
| `draft` | `false` for a published dataflow |
| `enabled` | `true` to allow execution |
| `runState` | `"ENABLED"` to allow scheduled runs |
| `engineProperties` | `{"kettle.mode": "STRICT"}` is standard |
| `inputs` | Array of input dataset references |
| `outputs` | Array of output dataset references |
| `actions` | Array of action nodes (the DAG) |

### Inputs Array

Each input references a Domo dataset that feeds into the dataflow:

```json
"inputs": [
  {
    "dataSourceId": "422efbf4-6c96-4576-907b-eacae8379d5d",
    "executeFlowWhenUpdated": false,
    "dataSourceName": "RAW | SFDC | Accounts",
    "onlyLoadNewVersions": false,
    "recentVersionCutoffMs": 0
  }
]
```

| Field | Description |
|---|---|
| `dataSourceId` | UUID of the input dataset |
| `dataSourceName` | Display name (for readability) |
| `executeFlowWhenUpdated` | `true` to auto-trigger the dataflow when this input updates |
| `onlyLoadNewVersions` | `true` to only process new data versions |

### Outputs Array

For a **new** dataflow where the output dataset doesn't exist yet:

```json
"outputs": [
  {
    "dataSourceId": null,
    "dataSourceName": "SFDC | Account Summary",
    "versionChainType": "REPLACE"
  }
]
```

Setting `dataSourceId` to `null` tells Domo to create a new dataset on first run. After the first successful run, Domo assigns a UUID.

For an **existing** output dataset:

```json
"outputs": [
  {
    "dataSourceId": "8fe448eb-231d-4ff5-95f1-86db64336e96",
    "dataSourceName": "SFDC | Account Opportunity Summary",
    "versionChainType": "REPLACE"
  }
]
```

`versionChainType`: `"REPLACE"` replaces all data each run. Other options include `"APPEND"`.

## Action Types

Actions are the nodes in the DAG. Each action has a unique `id`, a `type`, and references its upstream dependencies via `dependsOn`.

### Common Action Fields

Every action has these fields:

```json
{
  "type": "ActionType",
  "id": "unique-action-id",
  "name": "Human-readable name",
  "dependsOn": ["upstream-action-id-1", "upstream-action-id-2"],
  "settings": {
    "preferredDatabaseEntityType": "TEMP_VIEW"
  },
  "gui": {
    "x": 128,
    "y": 128,
    "color": null,
    "colorSource": null,
    "sampleJson": null
  },
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `id` | Unique identifier for this action node. Can be any string, but convention is `TypeName-uuid` |
| `dependsOn` | Array of action IDs that must complete before this one runs |
| `gui.x` / `gui.y` | Position in the visual Magic ETL canvas. Space nodes ~224px apart horizontally |
| `settings.preferredDatabaseEntityType` | Always `"TEMP_VIEW"` |
| `tables` | Always `[{}]` |

### LoadFromVault (Input Node)

Loads data from a Domo dataset into the dataflow.

```json
{
  "type": "LoadFromVault",
  "id": "LoadFromVault-accounts",
  "name": "RAW | SFDC | Accounts",
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 128, "y": 128, "color": null, "colorSource": null, "sampleJson": null},
  "previewRowLimit": 10000,
  "propagateAi": false,
  "filterPolicy": "LEGACY",
  "dataSourceId": "422efbf4-6c96-4576-907b-eacae8379d5d",
  "sourceType": "AUTO",
  "executeFlowWhenUpdated": false,
  "pseudoDataSource": false,
  "truncateTextColumns": false,
  "truncateRows": false,
  "onlyLoadNewVersions": false,
  "recentVersionCutoffMs": 0,
  "tables": [{}]
}
```

Key fields:
- `dataSourceId`: UUID of the dataset to load
- `name`: Should match the dataset name for clarity
- No `dependsOn` — this is a root node

### MergeJoin (Join)

Joins two upstream actions on specified keys.

```json
{
  "type": "MergeJoin",
  "id": "MergeJoin-accounts-opps",
  "name": "Join Accounts & Opp Summary",
  "dependsOn": ["LoadFromVault-accounts", "GroupBy-opp-summary"],
  "disabled": false,
  "removeByDefault": false,
  "notes": [],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 576, "y": 320, "color": null, "colorSource": null, "sampleJson": null},
  "previewRowLimit": null,
  "joinType": "LEFT OUTER",
  "relationshipType": "MTM",
  "step1": "LoadFromVault-accounts",
  "step2": "GroupBy-opp-summary",
  "keys1": ["Id"],
  "keys2": ["AccountId"],
  "on": null,
  "schemaModification1": [],
  "schemaModification2": [
    {"name": "AccountId", "rename": "Opp_AccountId", "remove": true}
  ]
}
```

| Field | Description |
|---|---|
| `joinType` | `"LEFT OUTER"`, `"INNER"`, `"RIGHT OUTER"`, `"FULL OUTER"` |
| `relationshipType` | **`"MTM"`** — use this abbreviation, NOT `"MANY_TO_MANY"` (causes validation errors) |
| `step1` | Action ID for the left side of the join |
| `step2` | Action ID for the right side of the join |
| `keys1` | Array of column names from step1 to join on |
| `keys2` | Array of column names from step2 to join on (matched positionally with keys1) |
| `schemaModification1` | Rename or remove columns from step1 (left side) |
| `schemaModification2` | Rename or remove columns from step2 (right side) to avoid name collisions |
| `dependsOn` | Must include both `step1` and `step2` action IDs |

**Note:** Keys can be asymmetric — `keys1: ["fldWorkCodeID"]` / `keys2: ["ID"]`. Domo matches by array position, not by column name.

#### schemaModification1 / schemaModification2

When two datasets share column names (e.g., both have `Id`, `Name`, `Description`), use `schemaModification2` to rename or remove the conflicting columns from the right-side (step2) dataset:

```json
"schemaModification2": [
  {"name": "Description", "rename": "Opportunities.Description", "remove": false},
  {"name": "Id", "rename": "Opportunities.Id", "remove": false},
  {"name": "Name", "rename": "Opportunities.Name", "remove": false},
  {"name": "AccountId", "rename": "Opp_AccountId", "remove": true}
]
```

- `remove: true` — drops the column entirely from the output
- `remove: false` — keeps the column but renames it to the `rename` value

### GroupBy (Aggregation)

Aggregates data by grouping columns and applying aggregation functions.

```json
{
  "type": "GroupBy",
  "id": "GroupBy-opp-summary",
  "name": "Summarize Opportunities per Account",
  "dependsOn": ["LoadFromVault-opportunities"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 352, "y": 512, "color": null, "colorSource": null, "sampleJson": null},
  "input": "LoadFromVault-opportunities",
  "addLineNumber": false,
  "giveBackRow": false,
  "allRows": false,
  "groups": [
    {"name": "AccountId"}
  ],
  "fields": [
    {"name": "Opportunity Count", "source": "Id", "type": "COUNT_ALL", "valuefield": null, "expression": null, "settings": null},
    {"name": "Total Amount", "source": "Amount", "type": "SUM", "valuefield": null, "expression": null, "settings": null},
    {"name": "Avg Amount", "source": "Amount", "type": "AVERAGE", "valuefield": null, "expression": null, "settings": null},
    {"name": "Total Expected Revenue", "source": "ExpectedRevenue", "type": "SUM", "valuefield": null, "expression": null, "settings": null},
    {"name": "Avg Probability", "source": "Probability", "type": "AVERAGE", "valuefield": null, "expression": null, "settings": null}
  ],
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `input` | Action ID of the upstream data |
| `groups` | Array of columns to group by. Each entry: `{"name": "ColumnName"}` |
| `fields` | Array of aggregation definitions |

#### Aggregation Field Definition

```json
{
  "name": "Total Amount",
  "source": "Amount",
  "type": "SUM",
  "valuefield": null,
  "expression": null,
  "settings": null
}
```

| Field | Description |
|---|---|
| `name` | Output column name for the aggregated value |
| `source` | Source column name to aggregate |
| `type` | Aggregation function (see below) |

#### Aggregation Types

| Type | Description | Confirmed |
|---|---|---|
| `SUM` | Sum of values | Yes |
| `AVERAGE` | Mean of values | Yes |
| `COUNT_ALL` | Count of all rows (including nulls) | Yes |
| `COUNT_DISTINCT` | Count of distinct values | |
| `MIN` | Minimum value | Yes |
| `MAX` | Maximum value | |
| `FIRST` | First value in group | |
| `LAST` | Last value in group | |
| `CONCAT_COMMA` | Concatenate values with comma separator | |

**Important:** The API uses `MIN` and `MAX`, not `MINIMUM` or `MAXIMUM`. Using `MINIMUM` returns a validation error: `"The value is invalid for expected type... AggregateType"`. This was discovered through testing.

#### Expression-Based Aggregations (Advanced)

Instead of using `source` + `type`, you can use full SQL aggregation expressions. Set `source`, `type`, and `valuefield` to `null` and put the full expression in `expression`:

```json
{
  "name": "Total Hours",
  "source": null,
  "type": null,
  "valuefield": null,
  "expression": "SUM(IFNULL(`Hours`,0))",
  "settings": null
}
```

**CRITICAL:** The `expression` must be a **full SQL aggregation expression** — NOT just the function name.
- `"expression": "SUM(IFNULL(\`Hours\`,0))"` with `"source": null` — CORRECT
- `"expression": "SUM"` with `"valuefield": "Hours"` — WRONG (treats "SUM" as a column name)

This allows embedding complex logic like CASE WHEN directly in the GroupBy without needing a pre-GroupBy ExpressionEvaluator:

```json
{
  "name": "LTM_Revenue",
  "source": null, "type": null, "valuefield": null,
  "expression": "SUM(CASE WHEN `Date` >= DATE_SUB(CURRENT_TIMESTAMP(), INTERVAL 12 MONTH) THEN IFNULL(`Revenue`,0) ELSE 0 END)",
  "settings": null
}
```

### WindowAction (Rank & Window)

Applies window functions — ranking, row numbering, lag/lead offsets — partitioned by group columns and ordered by sort columns. This is the programmatic equivalent of the "Rank & Window" tile in the Magic ETL UI.

```json
{
  "type": "WindowAction",
  "id": "WindowAction-first-order",
  "name": "First Order Date per Customer",
  "dependsOn": ["LoadFromVault-finance"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 352, "y": 128, "color": null, "colorSource": null, "sampleJson": null},
  "input": "LoadFromVault-finance",
  "groupRules": [
    {"column": "customer", "caseSensitive": false}
  ],
  "orderRules": [
    {"column": "date_ymd", "caseSensitive": false, "ascending": true}
  ],
  "additions": [
    {
      "name": "Customer Order Rank",
      "operation": {
        "type": "RANKING",
        "operationType": "ROW_NUMBER",
        "column": null,
        "defaultValue": null,
        "amount": null
      }
    }
  ],
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `input` | Action ID of the upstream data |
| `groupRules` | Partition columns — the window function is applied within each group |
| `orderRules` | Sort order within each partition |
| `additions` | Array of window function definitions to add as new columns |

#### groupRules

Defines the `PARTITION BY` columns:

```json
"groupRules": [
  {"column": "customer", "caseSensitive": false},
  {"column": "region", "caseSensitive": false}
]
```

Each entry partitions the data by that column. Multiple entries create a composite partition key.

#### orderRules

Defines the `ORDER BY` within each partition:

```json
"orderRules": [
  {"column": "date_ymd", "caseSensitive": false, "ascending": true}
]
```

| Field | Description |
|---|---|
| `column` | Column to sort by |
| `caseSensitive` | Whether string sorting is case-sensitive |
| `ascending` | `true` for ASC, `false` for DESC |

Multiple orderRules create a composite sort key.

#### additions (Window Function Definitions)

Each addition creates a new column with the result of a window function:

```json
{
  "name": "Output Column Name",
  "operation": {
    "type": "RANKING",
    "operationType": "ROW_NUMBER",
    "column": null,
    "defaultValue": null,
    "amount": null
  }
}
```

#### Window Operation Types

**Ranking operations** (`type: "RANKING"`):

| operationType | Description | column | amount |
|---|---|---|---|
| `ROW_NUMBER` | Sequential number within partition (1, 2, 3...) | `null` | `null` |
| `RANK` | Rank with gaps for ties (1, 2, 2, 4...) | `null` | `null` |
| `DENSE_RANK` | Rank without gaps for ties (1, 2, 2, 3...) | `null` | `null` |

**Offset operations** (`type: "OFFSET"`):

| operationType | Description | column | amount |
|---|---|---|---|
| `LAG` | Value from N rows before in the partition | Source column name | Number of rows to look back |
| `LEAD` | Value from N rows ahead in the partition | Source column name | Number of rows to look ahead |

Example — LAG to get previous day's revenue:

```json
{
  "name": "Previous Day Revenue",
  "operation": {
    "type": "OFFSET",
    "operationType": "LAG",
    "column": "revenue",
    "defaultValue": null,
    "amount": 1
  }
}
```

Example — ROW_NUMBER to rank orders per customer:

```json
{
  "name": "Customer Order Rank",
  "operation": {
    "type": "RANKING",
    "operationType": "ROW_NUMBER",
    "column": null,
    "defaultValue": null,
    "amount": null
  }
}
```

#### Combining WindowAction with GroupBy

A common pattern is to use `WindowAction` for row-level ranking, then `GroupBy` for aggregation. For example, to find the first order date per customer:

1. **WindowAction**: Partition by `customer`, order by `date_ymd` ASC, add `ROW_NUMBER`
2. **GroupBy**: Group by `customer`, use `MIN` on `date_ymd` to get the first order date, plus `SUM`/`AVERAGE` on numeric columns

The `WindowAction` passes through all original columns plus the new additions, so downstream actions have access to everything.

### Filter (Row Filtering)

Filters rows based on column conditions. This is the programmatic equivalent of the "Filter Rows" tile in the Magic ETL UI.

```json
{
  "type": "Filter",
  "id": "Filter-exclude-florida",
  "name": "Exclude Florida",
  "dependsOn": ["LoadFromVault-sales"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 352, "y": 256, "color": null, "colorSource": null, "sampleJson": null},
  "input": "LoadFromVault-sales",
  "filterList": [
    {
      "leftField": "state",
      "rightField": null,
      "rightValue": {"value": "Florida", "type": "STRING"},
      "rightExpr": "'Florida'",
      "operator": "NE",
      "expression": null,
      "andFilterList": []
    }
  ],
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `input` | Action ID of the upstream data |
| `filterList` | Array of filter conditions (combined with OR logic) |
| `andFilterList` | Nested array within a filter for AND logic |

#### Filter Condition Fields

| Field | Description |
|---|---|
| `leftField` | Column name to filter on |
| `operator` | Comparison operator (see table below) |
| `rightValue` | Typed value object: `{"value": "Florida", "type": "STRING"}` |
| `rightExpr` | String expression of the value, wrapped in single quotes for strings: `"'Florida'"` |
| `rightField` | Column name to compare against (for column-to-column comparisons, otherwise `null`) |

**Important:** For string comparisons, `rightValue` must be a typed object with `value` and `type` fields, and `rightExpr` must wrap the value in single quotes. Using a plain string for `rightValue` returns a `VALIDATION-DE` error.

#### Expression-Based Filters (Alternative)

Instead of using `leftField`/`operator`/`rightValue`, you can use a raw SQL `expression` for complex conditions:

```json
{
  "leftField": null,
  "rightField": null,
  "rightValue": null,
  "rightExpr": null,
  "operator": null,
  "expression": "IFNULL(TRIM(`column_name`),'') <> ''",
  "andFilterList": []
}
```

This is useful for multi-condition filters or filters with function calls. The expression is a SQL WHERE clause fragment.

#### Filter Operators

| Operator | Description | Confirmed |
|---|---|---|
| `NE` | Not equal | Yes |
| `EQ` | Equal | |
| `LT` | Less than | |
| `GT` | Greater than | |
| `LE` | Less than or equal | |
| `GE` | Greater than or equal | |
| `NN` | Is not null | Yes (from existing dataflow) |
| `NL` | Is null | |
| `NIN` | Not in list | |
| `IN` | In list | |

#### rightValue Type Values

| Type | Use For |
|---|---|
| `STRING` | Text comparisons |
| `NUMERIC` | Number comparisons |
| `DATE` | Date comparisons |

### ExpressionEvaluator (Add Formula)

Adds calculated columns using Domo's expression language. This is the programmatic equivalent of the "Add Formula" tile in the Magic ETL UI.

```json
{
  "type": "ExpressionEvaluator",
  "id": "ExpressionEvaluator-month-trunc",
  "name": "Add Month Column",
  "dependsOn": ["Filter-exclude-florida"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 480, "y": 256, "color": null, "colorSource": null, "sampleJson": null},
  "input": "Filter-exclude-florida",
  "expressions": [
    {
      "expression": "concat(year(`date_ymd`),MONTHNAME(`date_ymd`))",
      "fieldName": "Year_Month",
      "settings": {}
    }
  ],
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `input` | Action ID of the upstream data |
| `expressions` | Array of formula definitions |

#### Expression Definition

```json
{
  "expression": "concat(year(`date_ymd`),MONTHNAME(`date_ymd`))",
  "fieldName": "Year_Month",
  "settings": {}
}
```

| Field | Description |
|---|---|
| `expression` | Domo formula expression. Column names must be wrapped in backticks. |
| `fieldName` | Name of the new output column |
| `settings` | Empty object `{}` |

#### Known Working Functions

| Function | Description | Example |
|---|---|---|
| `year()` | Extract year from date | `year(\`date_ymd\`)` |
| `MONTH()` | Extract month number (1-12) | `MONTH(\`date_ymd\`)` |
| `MONTHNAME()` | Extract month name from date | `MONTHNAME(\`date_ymd\`)` |
| `concat()` | Concatenate strings | `concat(year(\`date_ymd\`), MONTHNAME(\`date_ymd\`))` |
| `DATE()` | Convert to date type | `DATE(\`date_ymd\`)` |
| `DATE_FORMAT()` | Format date as string | `DATE_FORMAT(\`date_ymd\`, 'yyyy-MM-dd')` |
| `LEFT()` | Left substring | `LEFT(\`Date\`, 7)` for year-month from "2025-01-15" |
| `LPAD()` | Left-pad string | `LPAD(MONTH(\`date\`), 2, '0')` |
| `IFNULL()` | Null replacement (2 args only) | `IFNULL(\`col\`, 0)` |
| `COALESCE()` | Null replacement (multi-arg) | `COALESCE(\`a\`, \`b\`, 'default')` |
| `TRIM()` | Remove whitespace | `TRIM(\`col\`)` |
| `CAST()` | Type casting | `CAST(NULL AS DATETIME)` |
| `LAST_DAY()` | Last day of month | `LAST_DAY(\`date\`)` |
| `DATE_SUB()` | Subtract interval | `DATE_SUB(\`date\`, INTERVAL 12 MONTH)` |
| `CONVERT_TZ()` | Timezone conversion | `CONVERT_TZ(CURRENT_TIMESTAMP(),'UTC','US/Eastern')` |
| `CURRENT_TIMESTAMP()` | Current datetime | `CURRENT_TIMESTAMP()` |

**Important:** `TRUNC_MONTH()` is NOT a valid function and returns `"Unknown function: TRUNC_MONTH"`. To truncate dates to month level, use `concat(year(...), MONTHNAME(...))` or similar string-based approaches.

#### Expression Behavior Rules

- Expressions are processed **in order** — later expressions CAN reference fields computed by earlier ones in the same tile
- Adding an expression with the same `fieldName` as an existing column **replaces** that column's value (useful for type casting or reformatting)
- `IFNULL()` takes exactly 2 args; use `COALESCE(a, b, c)` for multi-arg null handling
- `CAST(NULL AS DATETIME)` works for creating null typed columns

Multiple expressions can be added in a single ExpressionEvaluator action — each creates a new column (or replaces an existing one). All original columns are passed through.

### Unique (Deduplicate)

Removes duplicate rows based on specified key columns. This is the programmatic equivalent of the "Remove Duplicates" tile.

```json
{
  "type": "Unique",
  "id": "Unique-dedup",
  "name": "Deduplicate",
  "dependsOn": ["SelectValues-final"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 800, "y": 256, "color": null, "colorSource": null, "sampleJson": null},
  "input": "SelectValues-final",
  "countRows": false,
  "fields": [
    {"name": "ColA", "caseInsensitive": false},
    {"name": "ColB", "caseInsensitive": false}
  ],
  "tables": [{}]
}
```

| Field | Description |
|---|---|
| `input` | Action ID of the upstream data |
| `countRows` | `true` to add a count column showing how many duplicates were found |
| `fields` | Array of columns that define uniqueness. Rows with identical values across all listed columns are deduplicated |
| `fields[].caseInsensitive` | `true` for case-insensitive string matching |

**Tip:** Add a Unique tile after joins that might fan out rows (e.g., many-to-many joins).

### SelectValues (Column Selection / Rename)

Selects specific columns and optionally renames them.

```json
{
  "type": "SelectValues",
  "id": "SelectValues-final",
  "name": "Select Final Columns",
  "dependsOn": ["MergeJoin-final"],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 1024, "y": 320, "color": null, "colorSource": null, "sampleJson": null},
  "input": "MergeJoin-final",
  "select": [
    {"name": "Id", "rename": "Account ID"},
    {"name": "Name", "rename": "Account Name"},
    {"name": "Industry"},
    {"name": "Contact Count"},
    {"name": "Total Amount"}
  ],
  "tables": [{}]
}
```

- Only columns listed in `select` are passed through; all others are dropped
- Omit `rename` to keep the original column name

**Alternative format** — uses `fields` instead of `select`. **Only list columns you want to KEEP** (with optional rename). Unlisted columns are dropped. Do NOT add `remove: true` entries — they cause `DP-0003` validation errors.

```json
"fields": [
  {"name": "ID", "rename": "Dataflow ID"},
  {"name": "Display Name", "rename": "Dataflow Name"},
  {"name": "Link", "rename": "Dataflow Link"}
]
```

The minimal field entry is just `{"name": "...", "rename": "..."}`. Do NOT include `type`, `dateFormat`, `settings`, or `remove` — these cause `DP-0003 Action is improperly configured` errors on the fields format.

### PublishToVault (Output Node)

Writes the final data to a Domo dataset.

```json
{
  "type": "PublishToVault",
  "id": "PublishToVault-output",
  "name": "SFDC | Account Summary",
  "dependsOn": ["MergeJoin-final"],
  "disabled": false,
  "removeByDefault": false,
  "notes": [],
  "settings": {"preferredDatabaseEntityType": "TEMP_VIEW"},
  "gui": {"x": 1248, "y": 320, "color": null, "colorSource": null, "sampleJson": null},
  "previewRowLimit": null,
  "dataSource": {
    "type": "DataFlow",
    "name": "SFDC | Account Summary",
    "cloudId": "domo"
  },
  "versionChainType": "REPLACE",
  "partitionIdColumns": [],
  "upsertColumns": [],
  "retainPartitionExpression": ""
}
```

| Field | Description |
|---|---|
| `dependsOn` | Array with a single action ID — the final transform step |
| `dataSource.type` | `"DataFlow"` |
| `dataSource.name` | Name for the output dataset |
| `dataSource.guid` | UUID of existing output dataset — **omit entirely for new datasets** |
| `dataSource.cloudId` | `"domo"` |
| `versionChainType` | `"REPLACE"` (full replace) or `"APPEND"` |
| `partitionIdColumns` | `[]` — always empty unless using partitioning |
| `upsertColumns` | `[]` — always empty unless doing upserts |
| `retainPartitionExpression` | `""` — always empty string |

**CRITICAL:** Do NOT include `inputs`, `schemaSource`, `partitioned`, or `tables` in PublishToVault. These fields cause `DP-DSCF` commit failures where the ETL processes all rows successfully but then fails to write to the output dataset. This was confirmed through extensive testing (April 2026).

For new dataflows, omit `guid` entirely. Domo assigns a real output dataset UUID on the first successful run.

## Complete Example: Account Summary ETL

This example creates a dataflow that:
1. Loads 3 Salesforce datasets (Accounts, Contacts, Opportunities)
2. Aggregates contacts per account (count)
3. Aggregates opportunities per account (count, total amount, avg amount, expected revenue, avg probability)
4. Left joins both aggregations to the accounts table
5. Outputs one row per account with all summary metrics

### Pipeline Diagram

```
LoadFromVault(Accounts) ─────────────────────┐
                                              ├─ MergeJoin(LEFT) ──┐
LoadFromVault(Opportunities)                  │   on Id=AccountId   │
  └─ GroupBy(AccountId) ─────────────────────┘                     │
       COUNT(Id) → Opportunity Count                               ├─ MergeJoin(LEFT) ─── PublishToVault
       SUM(Amount) → Total Amount                                  │   on Id=AccountId
       AVG(Amount) → Avg Amount                                    │
       SUM(ExpectedRevenue) → Total Expected Revenue               │
       AVG(Probability) → Avg Probability                          │
                                                                   │
LoadFromVault(Contacts)                                            │
  └─ GroupBy(AccountId) ──────────────────────────────────────────┘
       COUNT(Id) → Contact Count
```

### Creation Command

```bash
curl -s -X POST "https://<instance>.domo.com/api/dataprocessing/v1/dataflows" \
  -H "Content-Type: application/json" \
  -H "x-domo-developer-token: <TOKEN>" \
  -d @sfdc_account_summary_etl.json
```

### Execution

```bash
# Via CLI
echo -e "connect -server <instance>.domo.com -token <TOKEN>\ndataflow-run-now -i <DATAFLOW_ID>\nquit" \
  | java -jar domoutil.jar

# Via API
curl -s -X POST "https://<instance>.domo.com/api/dataprocessing/v1/dataflows/<ID>/executions" \
  -H "x-domo-developer-token: <TOKEN>"
```

## Complete Example: Customer Summary with Rank & Window

This example creates a dataflow that:
1. Loads a finance dataset (329,460 rows with customer, date, sales, revenue, cogs)
2. Uses a WindowAction to rank orders per customer by date (ROW_NUMBER)
3. Aggregates per customer: first order date (MIN), SUM and AVERAGE for sales/revenue/cogs, order count

### Pipeline Diagram

```
LoadFromVault(Mododata | Finance)  329,460 rows
  └── WindowAction: ROW_NUMBER partitioned by customer, ordered by date_ymd ASC
       └── GroupBy(customer):
            MIN(date_ymd)  → First Order Date
            SUM(sales)     → Total Sales
            AVG(sales)     → Avg Sales
            SUM(revenue)   → Total Revenue
            AVG(revenue)   → Avg Revenue
            SUM(cogs)      → Total COGS
            AVG(cogs)      → Avg COGS
            COUNT(date_ymd)→ Order Count
              └── PublishToVault  →  104 customer rows
```

### Key JSON Snippets

WindowAction (Rank & Window tile):
```json
{
  "type": "WindowAction",
  "id": "WindowAction-first-order",
  "name": "First Order Date per Customer",
  "dependsOn": ["LoadFromVault-finance"],
  "input": "LoadFromVault-finance",
  "groupRules": [
    {"column": "customer", "caseSensitive": false}
  ],
  "orderRules": [
    {"column": "date_ymd", "caseSensitive": false, "ascending": true}
  ],
  "additions": [
    {
      "name": "Customer Order Rank",
      "operation": {
        "type": "RANKING",
        "operationType": "ROW_NUMBER",
        "column": null,
        "defaultValue": null,
        "amount": null
      }
    }
  ]
}
```

GroupBy with MIN for first order date:
```json
{
  "type": "GroupBy",
  "id": "GroupBy-customer-summary",
  "name": "Customer Aggregations",
  "dependsOn": ["WindowAction-first-order"],
  "input": "WindowAction-first-order",
  "groups": [{"name": "customer"}],
  "fields": [
    {"name": "First Order Date", "source": "date_ymd", "type": "MIN"},
    {"name": "Total Sales", "source": "sales", "type": "SUM"},
    {"name": "Avg Sales", "source": "sales", "type": "AVERAGE"},
    {"name": "Total Revenue", "source": "revenue", "type": "SUM"},
    {"name": "Avg Revenue", "source": "revenue", "type": "AVERAGE"},
    {"name": "Total COGS", "source": "cogs", "type": "SUM"},
    {"name": "Avg COGS", "source": "cogs", "type": "AVERAGE"},
    {"name": "Order Count", "source": "date_ymd", "type": "COUNT_ALL"}
  ]
}
```

### Result

Output dataset: 104 rows (one per customer) with columns: `customer`, `First Order Date`, `Total Sales`, `Avg Sales`, `Total Revenue`, `Avg Revenue`, `Total COGS`, `Avg COGS`, `Order Count`.

## Complete Example: Monthly Dept Metrics with Filter & Formula

This example creates a dataflow that:
1. Loads a sales dataset (481,643 rows)
2. Filters out rows where state = 'Florida'
3. Adds a `Year_Month` column using `concat(year(), MONTHNAME())`
4. Aggregates by Year_Month + department + metric_name: SUM and AVERAGE for revenue, store_revenue, web_revenue, mobile_revenue, total_costs, visits

### Pipeline Diagram

```
LoadFromVault(Mododata | Sales)  481,643 rows
  └── Filter: state != 'Florida'
       └── ExpressionEvaluator: Year_Month = concat(year(date_ymd), MONTHNAME(date_ymd))
            └── GroupBy(Year_Month, department, metric_name):
                 SUM/AVG for revenue, store_revenue, web_revenue,
                 mobile_revenue, total_costs, visits
                   └── PublishToVault  →  14,057 rows
```

### Key JSON Snippets

Filter (exclude a specific value):
```json
{
  "type": "Filter",
  "id": "Filter-exclude-florida",
  "name": "Exclude Florida",
  "dependsOn": ["LoadFromVault-sales"],
  "input": "LoadFromVault-sales",
  "filterList": [
    {
      "leftField": "state",
      "rightField": null,
      "rightValue": {"value": "Florida", "type": "STRING"},
      "rightExpr": "'Florida'",
      "operator": "NE",
      "expression": null,
      "andFilterList": []
    }
  ]
}
```

ExpressionEvaluator (date to year-month string):
```json
{
  "type": "ExpressionEvaluator",
  "id": "ExpressionEvaluator-month-trunc",
  "name": "Add Month Column",
  "dependsOn": ["Filter-exclude-florida"],
  "input": "Filter-exclude-florida",
  "expressions": [
    {
      "expression": "concat(year(`date_ymd`),MONTHNAME(`date_ymd`))",
      "fieldName": "Year_Month",
      "settings": {}
    }
  ]
}
```

### Result

Output: 14,057 rows (1 row per month x department x metric_name, excluding Florida). Granularity reduced from 481K daily rows to 14K monthly aggregated rows.

## ETL Error Codes Reference

When a dataflow execution fails, the error object in `lastExecution.errors[]` contains a `code` field. Use this table to diagnose:

| Code | Category | Meaning | Typical Fix |
|------|----------|---------|-------------|
| `DP-DSNF` | Missing input | Required dataset does not exist | Recreate dataset or remove the LoadFromVault tile |
| `DP-61100` | Missing input | Same as DP-DSNF (alternate code) | Same as above |
| `DP-0001` | Schema mismatch | Column referenced but not found | Upstream schema changed — update column references |
| `DP-0059` | Formula error | Syntax error in expression | Fix formula (e.g., missing `END` on CASE statement) |
| `DP-0118` | Code/model crash | Transform job failure | Check Python script or AI model tile |
| `DP-TGTFR` | Data volume | Batch Text Generation needs >= 100 rows | Ensure input has enough rows |
| `MYSQL-601072` | Join key missing | Key column doesn't exist in table | Update join key column names |
| `DP-0000` | Unknown | No API-level details | Inspect in Domo UI |

### Tracing Errors to Specific Tiles

Error objects contain a `parameters` map with `_actionId` (UUID of the failing tile). Match it against `actions[].id` in the dataflow:

```python
errors = dataflow.get("lastExecution", {}).get("errors", [])
actions_by_id = {a["id"]: a for a in dataflow.get("actions", [])}
for e in errors:
    action_id = e.get("parameters", {}).get("_actionId", "")
    tile = actions_by_id.get(action_id, {})
    print(f'Error: [{e["code"]}] {e["localizedMessage"]}')
    print(f'Tile: "{tile.get("name", "?")}" (type: {tile.get("type", "?")})')
    print(f'Property: {e.get("parameters", {}).get("_propertyPath", "")}')
```

| `_actionId` tile type | What to inspect |
|---|---|
| `ExpressionEvaluator` | `expressions[].expression` — the formula text |
| `LoadFromVault` | `dataSourceId` — the input dataset UUID |
| `MergeJoin` | `keys1` / `keys2` — join key column names |
| `SelectValues` | `fields[].name` — column names being selected |
| `Filter` | `filterList[].leftField` — filter column |
| `PublishToVault` | `dataSource.guid` — output dataset UUID |

## Common Pitfalls

### 1. `DP-DSCF` Commit Failure — Wrong PublishToVault Structure

The error `"Failed to commit data to data source <UUID>"` (code `DP-DSCF`) is caused by incorrect `PublishToVault` fields. The ETL will process all rows successfully but then fail at the commit step.

**Root cause (confirmed April 2026):** Using `inputs`, `schemaSource`, `partitioned`, or `tables` in the `PublishToVault` action.

**Fix:** Use this exact structure — `partitionIdColumns`, `upsertColumns`, `retainPartitionExpression` — and omit `inputs`, `schemaSource`, `partitioned`, `tables`:

```json
{
  "type": "PublishToVault",
  "dataSource": {"type": "DataFlow", "name": "Output Name", "cloudId": "domo"},
  "versionChainType": "REPLACE",
  "partitionIdColumns": [],
  "upsertColumns": [],
  "retainPartitionExpression": ""
}
```

### 2. SelectValues `fields` Format — Only List Columns to Keep

The `fields` format of `SelectValues` causes `DP-0003 Action is improperly configured` if you include entries with `"remove": true` or extra fields like `type`, `dateFormat`, `settings`. Only list columns you want to **keep**:

```json
"fields": [
  {"name": "ID", "rename": "Dataset ID"},
  {"name": "Name", "rename": "Dataset Name"}
]
```

Columns not listed are automatically dropped. Do NOT add remove entries.

### 3. Column Name Conflicts in Joins

When joining two datasets that share column names (e.g., `Id`, `Name`, `Description`), you must use `schemaModification2` on the MergeJoin to rename or remove conflicting columns from the right-side dataset. Failing to do this results in ambiguous column names downstream.

### 4. Action IDs Must Be Unique

Every action in the `actions` array needs a unique `id` string. Convention is `TypeName-uuid` (e.g., `"LoadFromVault-b71d89d7-6c08-44ad-a503-ebed046377e0"`), but any unique string works (e.g., `"LoadFromVault-accounts"`).

### 5. dependsOn Must Match step1/step2/input

For `MergeJoin`, the `dependsOn` array must contain both `step1` and `step2` action IDs. For `GroupBy`, the `dependsOn` must contain the `input` action ID. Mismatches will cause the dataflow to fail.

### 6. GUI Positions Affect the Visual Canvas

The `gui.x` and `gui.y` values determine where nodes appear in the Domo Magic ETL visual editor. Space nodes approximately 224px apart horizontally and 192px vertically for a clean layout. Input nodes typically start at `x: 128`.

### 7. Dataflow Creation via API — Auth (Updated April 2026)

**Auth:** `POST /api/dataprocessing/v1/dataflows` works with developer tokens (`DDCI...`) on most instances (confirmed April 2026). The body **must** include `"databaseType": "MAGIC"`. The created dataflow is NOT in DRAFT state and can be executed immediately via API — no UI save required.

**Outputs:** When POST includes `"outputs": [{"dataSourceId": null, "dataSourceName": "...", "versionChainType": "REPLACE"}]`, Domo assigns a real output dataset UUID immediately. The first successful execution creates the actual dataset.

**CLI:** The `domo` (ryuu) CLI is for Custom App publishing only and has no dataflow commands. The Java CLI (`domoutil.jar`) has dataflow commands but requires separate setup.

### 8. Aggregation Type Names Are Not What You'd Expect

The GroupBy `type` field uses `MIN` and `MAX`, not `MINIMUM` or `MAXIMUM`. Using `MINIMUM` returns a validation error:

```
{"code":"VALIDATION-DIV","message":"The value is invalid for expected type.","path":"actions[2].fields[0].type","parameters":{"field":"type","type":"AggregateType","rejected":"MINIMUM"}}
```

Confirmed working types: `SUM`, `AVERAGE`, `COUNT_ALL`, `MIN`. Use these exact strings.

### 9. Filter rightValue Must Be a Typed Object

The Filter action's `rightValue` cannot be a plain string. It must be a typed object:

```json
// WRONG — returns VALIDATION-DE error
"rightValue": "Florida"

// CORRECT
"rightValue": {"value": "Florida", "type": "STRING"}
```

Additionally, `rightExpr` must wrap string values in single quotes: `"'Florida'"`. Both `rightValue` and `rightExpr` should be set together.

### 10. TRUNC_MONTH and Other Date Functions Don't Exist

The ExpressionEvaluator does not support `TRUNC_MONTH()`, `DATE_TRUNC()`, or similar date truncation functions. To get a year-month value, use string concatenation:

```
concat(year(`date_ymd`), MONTHNAME(`date_ymd`))
```

Known working functions: `year()`, `MONTHNAME()`, `concat()`, `DATE()`.

### 11. Dataflows Created via POST Can Be Executed Immediately (Updated April 2026)

Contrary to earlier notes, dataflows created via `POST /api/dataprocessing/v1/dataflows` with a dev token are NOT in DRAFT state and **can be executed immediately** via `POST .../executions`. The `outputs` array IS populated on creation when `dataSourceId: null` is passed. No UI save required. Executions return a valid execution ID and run to completion.

### 12. CLI dataflow-run-now Can Fail on New Dataflows

The Java CLI `dataflow-run-now` command may return 500 errors for newly created dataflows. Always use the API for running (`POST /api/dataprocessing/v1/dataflows/{id}/executions`) — it's more reliable.

### 13. responsibleUserId Is Optional

No need to specify `responsibleUserId` in the POST body — it defaults to the authenticated user.

### 14. LoadFromVault Nodes Can Feed Multiple Branches

A single LoadFromVault node can feed multiple downstream branches — just reference its ID in multiple `dependsOn` arrays. This avoids loading the same dataset twice.

### 15. PublishToVault — Use `dependsOn` Only, NOT `inputs`

The `PublishToVault` action uses `dependsOn` to reference its upstream action. Do NOT include an `inputs` array — it is not part of the working format and contributes to `DP-DSCF` commit failures. If `numOutputs` = 0 after creation, the `dataSource` object is likely missing from the action — PUT the corrected definition to fix.

### 16. API Token Authentication

The REST API uses the same developer token as the CLI:

```
x-domo-developer-token: <TOKEN>
```

This is different from OAuth — no client ID/secret exchange is needed.

### 19. All Non-LoadFromVault Actions Require `disabled`, `removeByDefault`, `notes`

Every action except `LoadFromVault` must include these fields or the dataflow may behave unexpectedly in the UI:

```json
"disabled": false,
"removeByDefault": false,
"notes": [],
"previewRowLimit": null
```

`MergeJoin` additionally requires `"on": null` and explicit `"schemaModification1": []` and `"schemaModification2": []` (even when empty).

`LoadFromVault` uses `"previewRowLimit": 10000` (not null).

### 20. `relationshipType` Must Be `"MTM"` Not `"MANY_TO_MANY"`

The `MergeJoin` field `relationshipType` must be the abbreviated form `"MTM"`. Using `"MANY_TO_MANY"` causes validation errors. Other valid values: `"OTO"`, `"OTM"`, `"MTO"`.

### 21. Always Ask for a Master Dataset Anchor Before Building Lineage ETLs

Before building any dataset lineage ETL, ask: **"Is there a master 'My Datasets' or similar list dataset that every output row should be tied back to?"** This anchor dataset (typically containing Dataset ID, Name, Link, Owner, etc.) should be loaded as the LEFT side of the final join so all datasets appear in the output — even those with no card/ETL associations (standalone datasets). Missing this anchor means the output only covers datasets that happen to appear in other metadata tables, missing any standalone ones.

### 17. Do NOT Use `?hydrate=full` When Fetching Dataflows

`GET /api/dataprocessing/v1/dataflows/{id}?hydrate=full` returns `400 Bad Request` for some dataflows. The non-hydrated endpoint (`GET /api/dataprocessing/v1/dataflows/{id}`) already returns the full `actions[]` array with all tile details. Always use the non-hydrated version.

### 18. PUT Replaces the Entire Dataflow Definition

When updating a dataflow via `PUT /api/dataprocessing/v1/dataflows/{id}`:

- **Send the full dataflow object** — PUT replaces the entire definition. Always start from a fresh GET.
- **PUT only saves** — it does not run the dataflow. Trigger execution separately with `POST .../executions`.
- **Version tracking** — each successful PUT increments `onboardFlowVersion.versionNumber`. The execution response includes `dataFlowVersion` to confirm which version ran.

## Known Action Types

All action types discovered across existing dataflows in the instance:

| Action Type | Description | Confirmed Working |
|---|---|---|
| `LoadFromVault` | Input node — loads a Domo dataset | Yes |
| `PublishToVault` | Output node — writes to a Domo dataset | Yes |
| `MergeJoin` | Join two upstream actions on keys | Yes |
| `GroupBy` | Aggregate with SUM, AVERAGE, MIN, COUNT_ALL, etc. | Yes |
| `WindowAction` | Rank & Window — ROW_NUMBER, RANK, LAG, LEAD | Yes |
| `SelectValues` | Select and rename columns | Yes (but can cause commit errors before PublishToVault) |
| `Filter` | Filter rows based on conditions (NE, EQ, NN, etc.) | Yes |
| `ExpressionEvaluator` | Add calculated columns / formulas (concat, year, MONTHNAME, DATE) | Yes |
| `Unique` | Deduplicate rows by key columns | Documented (from patterns guide) |
| `Metadata` | Change column types or metadata | Seen in existing dataflows |
| `SplitColumnAction` | Split a column into multiple columns | Seen in existing dataflows |
| `FixedInput` | Hardcoded/constant input data | Seen in existing dataflows |

## Workflow: Creating a New Magic ETL

### Pre-Flight Questions (ask before building)
- What are all the input dataset IDs and their column schemas? (query each via `/api/query/v1/execute/<UUID>` with `SELECT * FROM table LIMIT 2`)
- Is there a **master/anchor dataset** (e.g., "My Datasets") that every output row should tie back to? If yes, get its UUID — it becomes the LEFT side of the final join.
- What are the exact desired output column names and which input fields map to each?

### Build Steps
1. **Get input dataset schemas** — `POST /api/query/v1/execute/<UUID>` with `{"sql": "SELECT * FROM table LIMIT 2"}` on each input dataset
2. **Build the JSON definition** — use the confirmed working action structures from this skill doc
3. **Create via API** — `POST /api/dataprocessing/v1/dataflows` with dev token — works immediately, no UI save needed
4. **Execute** — `POST /api/dataprocessing/v1/dataflows/<ID>/executions`
5. **Check status** — `GET /api/dataprocessing/v1/dataflows/<ID>/executions/<EXEC_ID>` — poll until `state` is `SUCCESS` or `FAILED_DATA_FLOW`
6. **On failure** — check `errors[]` array in execution response for `actionId` and `localizedMessage`, fix the specific action, `PUT` the updated definition, re-run
7. **Export for debugging** — `GET /api/dataprocessing/v1/dataflows/<ID>` returns the full saved definition including any server-assigned GUIDs
