---

## name: variable-creation
description: "Use this skill to create and manage Domo card variables (interactive controls). When a user needs a dropdown, slider, pill, textbox, or date picker control on a card — whether they call it a variable, control, parameter, or describe wanting dynamic/interactive filtering that isn't a standard filter — use this skill. Covers variable formula construction, validation, and the 3-step creation flow (create function template, register control, save card). Use this proactively when you notice a card would benefit from user-adjustable parameters."

# Variable Creation

Create Domo card variables (interactive controls) and output curl commands or CLI commands to execute them.

Variables are user-adjustable values that feed into Beast Mode formulas, enabling dynamic what-if analysis. They appear as dropdown, pill, slider, textbox, or date picker controls on cards and dashboards.

## When to Use This Skill

- User asks for a dropdown, slider, or interactive control on a card
- User mentions "variable", "parameter", or describes wanting dynamic/adjustable values
- A card needs what-if analysis or user-selectable inputs
- You're building a card and realize a beast mode needs a user-controlled input

## Core Workflow — 3-Step Creation

Variable creation requires three sequential API calls. All three are mandatory — skipping the middle step causes a 400 error on the card save.

```
1. Check name uniqueness (GET /query/v1/functions/variables/uniqueName)
2. Create the function template WITH embedded control (POST /query/v1/functions/template)
3. Register the variable control (PUT /content/v1/variable/controls)
4. Read the current card definition (PUT /content/v3/cards/kpi/definition)
5. Save the card with the new control (PUT /content/v3/cards/kpi/{cardId})
```

---

## Prerequisites


| Parameter      | Source                                            | Required                     |
| -------------- | ------------------------------------------------- | ---------------------------- |
| `instanceUrl`  | Domo instance (e.g., `domo-gordon-pont.domo.com`) | Always                       |
| `devToken`     | CLI auth / developer token                        | Always                       |
| `cardId`       | Card ID                                           | Always                       |
| `dataSourceId` | Dataset UUID (from card definition or columns)    | For validation and card save |


---

## Variable Data Types


| Data Type | Expression Examples              | Compatible Controls             |
| --------- | -------------------------------- | ------------------------------- |
| `string`  | `'TEST'`, `'Option A'`           | DROPDOWN, PILL, TEXTBOX         |
| `numeric` | `100`, `0.5`                     | DROPDOWN, PILL, SLIDER, TEXTBOX |
| `date`    | `CURRENT_DATE()`, `'2024-01-01'` | DROPDOWN, DATE_PICKER           |


---

## Variable Control Types


| Type          | Description                             | Best For                                    |
| ------------- | --------------------------------------- | ------------------------------------------- |
| `DROPDOWN`    | Select from a list of predefined values | Categorical selections, string/numeric/date |
| `PILL`        | Inline toggle chips                     | Small number of options (2-5)               |
| `SLIDER`      | Numeric range slider                    | Numeric ranges with min/max                 |
| `TEXTBOX`     | Free-text input                         | Open-ended string/numeric input             |
| `DATE_PICKER` | Calendar date selector                  | Date variables                              |


### Expression Types by Data Type


| Data Type | `exprType`      |
| --------- | --------------- |
| `string`  | `STRING_VALUE`  |
| `numeric` | `NUMERIC_VALUE` |
| `date`    | `DATE_VALUE`    |


### Values Array

For DROPDOWN and PILL controls, the `values` array defines the selectable options:

```json
{"expression": {"value": "Option Text", "exprType": "STRING_VALUE"}}
```

For SLIDER controls, values define the min/max range:

```json
[
  {"expression": {"value": "0", "exprType": "NUMERIC_VALUE"}},
  {"expression": {"value": "100", "exprType": "NUMERIC_VALUE"}}
]
```

---

## Step 1: Check Name Uniqueness

**Endpoint:** `GET /api/query/v1/functions/variables/uniqueName?name={name}`

```bash
curl -X GET "https://{instanceUrl}/api/query/v1/functions/variables/uniqueName?name={variableName}" \
  -H "X-DOMO-Developer-Token: {devToken}"
```

Returns `[]` if the name is available. Returns an array of function template IDs if the name is already in use. Variable names must be globally unique across the entire Domo instance.

---

## Step 2: Create the Function Template

**Endpoint:** `POST /api/query/v1/functions/template`

This creates the variable's function template. The request body must include an embedded `control` object — this is critical and differs from regular beast mode creation.

```bash
curl -X POST "https://{instanceUrl}/api/query/v1/functions/template" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "{variableName}",
    "formula": "{defaultExpression}",
    "status": "VALID",
    "dataType": "{dataType}",
    "persistedOnDataSource": false,
    "isAggregatable": true,
    "bignumber": false,
    "owner": null,
    "nonAggregatedColumns": [],
    "legacyId": "calculation_{uuid}",
    "variable": true,
    "isCalculation": true,
    "initialPersistedOnDataSource": false,
    "saved": true,
    "query": "{defaultExpression}",
    "control": {
      "format": {"type": "default"},
      "controlType": "VARIABLE",
      "function": {
        "name": "{variableName}",
        "dataType": "{dataType}",
        "expression": "{defaultExpression}",
        "id": -201
      },
      "saveOverride": true,
      "description": "",
      "values": [
        {"expression": {"value": "{value1}", "exprType": "{exprType}"}},
        {"expression": {"value": "{value2}", "exprType": "{exprType}"}}
      ],
      "type": "{controlType}",
      "unsaved": true,
      "name": "{variableName}",
      "id": -101
    },
    "description": "",
    "locked": false,
    "cacheWindow": "non_dynamic",
    "containsAggregation": false,
    "containsAnalytic": false,
    "invalidColumns": [],
    "nonAggregatedExpressions": [],
    "formulaTemplateDependencies": [],
    "columnPositions": [],
    "formulaId": "calculation_{another_uuid}",
    "formulaDependencies": [],
    "isControlled": false,
    "global": true,
    "unsaved": true,
    "expression": "{defaultExpression}"
  }'
```

**Key fields:**

- `variable: true` — marks this as a variable function (not a regular beast mode)
- `control` — the embedded control definition with placeholder IDs (`-201`, `-101`)
- `legacyId` and `formulaId` — generate unique UUIDs in the format `calculation_{uuid}`
- `global: true` — variables are instance-wide
- `owner: null` — server assigns the owner

**Response** — save the `id` (numeric function template ID):

```json
{
  "id": 1172,
  "name": "{variableName}",
  "legacyId": "calculation_{uuid}",
  "variable": true,
  ...
}
```

---

## Step 3: Register the Variable Control

**Endpoint:** `PUT /api/content/v1/variable/controls`

This step registers the control with the Domo control system. Without this step, the card save will return 400.

```bash
curl -X PUT "https://{instanceUrl}/api/content/v1/variable/controls" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '[
    {
      "format": {"type": "default"},
      "controlType": "VARIABLE",
      "function": {
        "name": "{variableName}",
        "dataType": "{dataType}",
        "expression": "{defaultExpression}",
        "id": {functionTemplateId from Step 2}
      },
      "saveOverride": true,
      "description": "",
      "values": [
        {"expression": {"value": "{value1}", "exprType": "{exprType}"}},
        {"expression": {"value": "{value2}", "exprType": "{exprType}"}}
      ],
      "type": "{controlType}",
      "unsaved": false,
      "name": "{variableName}"
    }
  ]'
```

**Key differences from Step 2's control:**

- `function.id` is now the real template ID from Step 2 (not `-201`)
- `unsaved: false` (not `true`)
- No `id: -101` at the control level
- Body is an **array** of control objects

**Response** — returns an array with the registered control, including server-assigned `id`:

```json
[
  {
    "id": 145,
    "function": {"id": 1172, ...},
    "type": "DROPDOWN",
    "values": [...],
    "controlType": "VARIABLE",
    ...
  }
]
```

---

## Step 4: Read the Current Card Definition

```bash
curl -X PUT "https://{instanceUrl}/api/content/v3/cards/kpi/definition" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "dynamicText": true,
    "variables": true,
    "urn": "{cardId}"
  }'
```

Save the full response. You need `definition.subscriptions`, `definition.controls`, `definition.charts`, `definition.modified`, etc.

Get the `dataSourceId` from `columns[].sourceId` in the response.

---

## Step 5: Save the Card with the New Control

**Endpoint:** `PUT /api/content/v3/cards/kpi/{cardId}`

Build the update payload by merging the new control into the card definition.

```bash
curl -X PUT "https://{instanceUrl}/api/content/v3/cards/kpi/{cardId}" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "definition": {
      "subscriptions": {existing subscriptions from card def — do NOT add dataSourceId here},
      "formulas": {"dsUpdated": [], "dsDeleted": [], "card": []},
      "annotations": {"new": [], "modified": [], "deleted": []},
      "conditionalFormats": {"card": [], "datasource": []},
      "controls": [{existing controls with saveOverride: true}, {new control}],
      "segments": {"active": [], "create": [], "update": [], "delete": []},
      "charts": {existing charts},
      "dynamicTitle": {existing dynamicTitle},
      "dynamicDescription": {"text": []},
      "chartVersion": "{existing chartVersion}",
      "allowTableDrill": true,
      "inputTable": false,
      "modified": {existing modified timestamp},
      "title": "{card title}",
      "description": ""
    },
    "dataProvider": {"dataSourceId": "{dataSourceId}"},
    "variables": true,
    "columns": false
  }'
```

**Critical payload notes:**

- `variables: true` and `columns: false` at the top level
- `dataSourceId` goes in `dataProvider` only — NOT in `subscriptions.main`
- `formulas` uses the `{dsUpdated, dsDeleted, card}` structure (not the array format from the read response)
- Existing controls must be passed in their full server format with `saveOverride: true` added
- The new control uses the simplified format with `function.id` = the template ID from Step 2
- The `modified` timestamp must match the card definition's value

---

## Optional: Validate the Variable Formula

**Endpoint:** `POST /api/query/v1/functions/validateFormulas`

Validation is optional but recommended before creating. The formula entry must have `"variable": true`.

```bash
curl -X POST "https://{instanceUrl}/api/query/v1/functions/validateFormulas" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSourceId": "{dataSourceId}",
    "columns": [{column schema array}],
    "formulas": {
      "{formulaId}": {
        "id": "{formulaId}",
        "name": "{variableName}",
        "formula": "{defaultExpression}",
        "status": "valid",
        "dataType": "{dataType}",
        "variable": true,
        "templateId": null,
        "legacyId": "{formulaId}",
        "formulaDependencies": []
      }
    }
  }'
```

---

## Using the Variable in a Beast Mode

A variable has no effect on a card unless it's referenced in a Beast Mode formula:

```sql
CASE
  WHEN `My Variable` = 'Option A' THEN `column_a`
  WHEN `My Variable` = 'Option B' THEN `column_b`
  ELSE `column_a`
END
```

Variables are referenced by name in backticks, just like dataset columns.

---

## Three-Tier Control Hierarchy

Variables have three levels of override:

1. **Default Control** — Set in Beast Mode Editor (or via API). Baseline value.
2. **Card Variable Control** — Override in Analyzer for a specific card. Does NOT transfer to dashboards.
3. **Dashboard Variable Control** — Override on a specific dashboard. Resets on page refresh.

---

## Using the CLI

The community-domo-cli handles the full 3-step flow automatically:

```bash
# Check if a variable name is available
community-domo-cli variables check-name "My Variable"

# List variables on a card
community-domo-cli variables list {cardId}

# Create a variable (handles all 3 steps internally)
community-domo-cli variables create {cardId} --body-file variable.json

# Validate a variable formula
community-domo-cli variables validate --body-file validate-payload.json

# Read full card definition (includes controls)
community-domo-cli cards definition {cardId}
```

### Example: Create a string dropdown variable via CLI

**variable.json:**

```json
{
  "name": "Region Selector",
  "type": "DROPDOWN",
  "function": {
    "name": "Region Selector",
    "dataType": "string",
    "expression": "'North'"
  },
  "description": "Select a region to filter by",
  "values": [
    {"expression": {"value": "North", "exprType": "STRING_VALUE"}},
    {"expression": {"value": "South", "exprType": "STRING_VALUE"}},
    {"expression": {"value": "East", "exprType": "STRING_VALUE"}},
    {"expression": {"value": "West", "exprType": "STRING_VALUE"}}
  ]
}
```

```bash
community-domo-cli variables create 1810280719 --body-file variable.json --yes
```

The CLI automatically:

1. Checks name uniqueness
2. Creates the function template with embedded control
3. Registers the control via `PUT /content/v1/variable/controls`
4. Reads the card definition
5. Merges and saves the card

---

## Troubleshooting


| Problem                                 | Cause                                            | Fix                                                                  |
| --------------------------------------- | ------------------------------------------------ | -------------------------------------------------------------------- |
| Variable not visible on card            | Not referenced in any beast mode                 | Create a beast mode that uses the variable                           |
| Card save returns 400                   | Missing `PUT /content/v1/variable/controls` step | Must register the control before saving the card                     |
| Card save returns 400                   | `dataSourceId` in `subscriptions.main`           | Remove it — only put `dataSourceId` in `dataProvider`                |
| Card save returns 400                   | Existing controls not in full server format      | Pass existing controls as-is from card def with `saveOverride: true` |
| 500 Internal database error             | Duplicate variable name                          | Check name with `GET /query/v1/functions/variables/uniqueName` first |
| Validation returns `INVALID`            | Bad expression syntax                            | Check quotes for strings, function syntax for dates                  |
| Dashboard doesn't show variable control | Card-level override doesn't propagate            | Set the control at dashboard level                                   |
| Variable resets on dashboard refresh    | Expected behavior                                | Dashboard controls reset to default on page load                     |


---

## Output Format

When generating commands for the user, provide:

1. **What it does** — one sentence explaining the variable
2. **The variable definition** — name, type, default, control type, options
3. **Numbered commands** — in execution order (all 3 steps), ready to copy/paste
4. **What to do with each response** — especially saving the function template ID from Step 2
5. **Beast mode integration** — show the formula that references the variable
6. **Verify** — tell them to check the card in Domo after running

