---
name: beast-mode-creation
description: Create and validate Domo beast modes (calculated fields); MySQL-style formulas, API validation, card vs dataset scope, curl output.
---

# Beast Mode Generator

Create Domo beast modes (calculated fields) and output curl commands to execute them.

Beast modes are virtual columns computed from existing dataset columns using MySQL-style formulas. They can be scoped to a single card or shared across all cards on a dataset.

## When to Use This Skill

- User asks for a field that doesn't exist in the schema
- A visualization needs a derived metric (percentages, concatenations, conditionals)
- User mentions "beast mode", "calculated field", "formula", or describes a computation
- You're building a card and realize the needed column must be computed

## Core Workflow

```
1. Identify what to compute and from which columns
2. Build the formula (MySQL syntax, backticks around column names)
3. Fetch the column schema (if not already available)
4. Validate the formula via the Domo API
5. Choose scope: dataset-level (default) or card-level
6. Generate curl command(s)
```

---

## Prerequisites

These values are typically available from the CLI tool context:


| Parameter      | Source                                            | Required                        |
| -------------- | ------------------------------------------------- | ------------------------------- |
| `instanceUrl`  | Domo instance (e.g., `domo-gordon-pont.domo.com`) | Always                          |
| `devToken`     | CLI auth / developer token                        | Always                          |
| `dataSourceId` | Dataset UUID                                      | Always                          |
| `cardId`       | Card ID                                           | For attaching to a card         |
| `userId`       | Current user's Domo ID                            | For dataset-level (owner field) |


If any are missing, ask the user before generating commands.

---

## Step 1: Build the Formula

Write formulas using MySQL syntax. Always wrap column names in backticks.

```sql
SUM(`hourly_cost_rate`)                              -- aggregate
CONCAT(`first_name`, ' ', `last_name`)               -- string
(`revenue` - `cost`) / `revenue` * 100               -- ratio
CASE WHEN `status` = 'active' THEN 1 ELSE 0 END      -- conditional
```

For a comprehensive list of supported functions and formula patterns, read `references/formula-examples.md`.

**Quick syntax rules:**

- Column names must be in backticks: ``column_name``
- String literals use single quotes: `'active'`
- CASE requires WHEN and END: `CASE WHEN ... THEN ... ELSE ... END`
- Domo follows older MySQL syntax — most standard MySQL functions work

**Before writing the formula**, check that every column you reference actually exists in the dataset schema. If you already have the schema (from context or a prior fetch), compare the user's requested columns against it. If a column doesn't exist, stop and tell the user — don't generate a formula with columns that aren't in the data. This catches errors early, before you even reach the validation step.

---

## Step 2: Fetch the Column Schema

If you don't already have the dataset's columns, fetch them first. The schema is needed for formula validation and to confirm column names are correct.

```bash
curl -X GET "https://{instanceUrl}/api/query/v1/datasources/{dataSourceId}/schema/indexed?includeHidden=true" \
  -H "X-DOMO-Developer-Token: {devToken}"
```

The response returns an array of column objects. Each has `name`, `type`, and other metadata. Save this — you'll need it for validation.

---

## Step 3: Validate the Formula

Always validate before generating the creation curl. This catches typos, missing columns, and syntax errors before they hit the API.

**Endpoint:** `POST /api/query/v1/functions/validateFormulas`

```bash
curl -X POST "https://{instanceUrl}/api/query/v1/functions/validateFormulas" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "dataSourceId": "{dataSourceId}",
    "columns": [
      {
        "id": "first_name",
        "name": "first_name",
        "label": "first_name",
        "type": "string",
        "isCalculation": false,
        "isVariable": false,
        "isAggregatable": true,
        "columnName": "first_name"
      }
    ],
    "formulas": {
      "{formulaId}": {
        "id": "{formulaId}",
        "name": "{fieldName}",
        "formula": "{formula}",
        "status": "valid",
        "dataType": "{dataType}"
      }
    }
  }'
```

The `columns` array must include every column in the dataset (use the schema response from Step 2). The `formulas` object is keyed by a unique ID you generate (e.g., `calculation_abc123`).

**Success response:**

```json
{
  "allValid": true,
  "results": {
    "{formulaId}": {
      "status": "VALID",
      "dataType": "LONG",
      "containsAggregation": true,
      "columnPositions": [{"columnName": "`hourly_cost_rate`", "columnPosition": 4}]
    }
  }
}
```

**If validation fails**, check:

- `invalidColumns` — column name doesn't exist (typo? check schema)
- `status: "INVALID"` — formula syntax error
- Show the user the error and ask them to clarify before proceeding

**Use the validation response** to populate fields in the creation payload:

- `dataType` from the result (the API infers the correct return type)
- `containsAggregation` → maps to `aggregated` in the creation payload
- `columnPositions` → include in the creation payload

---

## Step 4: Choose Scope

**Default to dataset-level** — it's reusable across all cards on the dataset and is the more common need.

Use **card-level** only when the user explicitly says it's single-use, or the formula is specific to one visualization's configuration.

Don't ask unless you genuinely can't tell. If the formula represents a business metric (revenue, margin, count, status flag), it almost certainly belongs on the dataset.

---

## Step 5: Generate Curl Commands

### Dataset-Level (Default) — Two Steps

**Step 5a: Create the beast mode on the dataset**

```bash
curl -X POST "https://{instanceUrl}/api/query/v1/functions/template?strict=false" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "{fieldName}",
    "owner": {userId},
    "locked": false,
    "global": false,
    "expression": "{formula}",
    "links": [
      {
        "resource": {"type": "DATA_SOURCE", "id": "{dataSourceId}"},
        "visible": true,
        "active": false,
        "valid": "VALID"
      }
    ],
    "aggregated": {true|false},
    "analytic": false,
    "nonAggregatedColumns": [],
    "dataType": "{dataType}",
    "status": "VALID",
    "cacheWindow": "non_dynamic",
    "columnPositions": [{from validation response}],
    "functions": [],
    "functionTemplateDependencies": [],
    "archived": false,
    "hidden": false,
    "variable": false
  }'
```

**Response** — save the `id` and `legacyId`:

```json
{
  "id": "calculation_549b9c1f-71cc-4227-bb9c-3ae5064be416",
  "legacyId": "calculation_549b9c1f-71cc-4227-bb9c-3ae5064be416",
  "templateId": 1161,
  ...
}
```

**Step 5b: Read the existing card, merge, and update**

The card update endpoint (`PUT /content/v3/cards/kpi/{cardId}`) replaces the full definition. You must read the card first, add the beast mode to `formulas.dsUpdated`, and PUT the whole thing back.

**Read the card:**

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

**Merge the beast mode into the response** by adding to `definition.formulas.dsUpdated`:

```json
{
  "name": "{fieldName}",
  "id": "{legacyId from Step 5a response}",
  "persistedOnDataSource": true,
  "initialPersistedOnDataSource": false,
  "label": "{fieldName}",
  "type": "{dataType}",
  "formula": "{formula}",
  "value": "{formula}",
  "isVariable": false,
  "isCalculation": true,
  "isAggregatable": false,
  "status": "VALID",
  "dataType": "{dataType}",
  "templateId": {templateId from Step 5a response},
  "owner": {userId},
  "locked": false,
  "saved": false,
  "query": "{formula}",
  "containsAggregation": {true|false},
  "containsAnalytic": false,
  "cacheWindow": "non_dynamic",
  "columnPositions": [{from validation response}],
  "formulaId": "{id from Step 5a response}",
  "formulaDependencies": [],
  "legacyId": "{legacyId from Step 5a response}",
  "isControlled": false
}
```

**PUT the merged card back:**

```bash
curl -X PUT "https://{instanceUrl}/api/content/v3/cards/kpi/{cardId}" \
  -H "X-DOMO-Developer-Token: {devToken}" \
  -H "Content-Type: application/json" \
  -d '{merged card body}'
```

---

### Card-Level — Single Step

Read the existing card first (same as above), then add to `definition.formulas.card[]` instead:

```json
{
  "id": "{generate a UUID like calculation_<uuid>}",
  "name": "{fieldName}",
  "formula": "{formula}",
  "status": "VALID",
  "dataType": "{dataType}",
  "persistedOnDataSource": false,
  "isAggregatable": false,
  "bignumber": false,
  "nonAggregatedColumns": [],
  "templateId": -1,
  "legacyId": "{same as id}",
  "variable": false,
  "isCalculation": true,
  "initialPersistedOnDataSource": false,
  "saved": false,
  "query": "{formula}",
  "cacheWindow": "non_dynamic",
  "containsAggregation": {true|false},
  "containsAnalytic": false,
  "invalidColumns": [],
  "nonAggregatedExpressions": [],
  "formulaTemplateDependencies": [],
  "columnPositions": [{from validation response}],
  "formulaId": "{generate another UUID}",
  "formulaDependencies": [],
  "isControlled": false
}
```

Then PUT the full merged card body.

---

## Key Differences: Card-Level vs Dataset-Level


| Aspect                    | Card-Level             | Dataset-Level                               |
| ------------------------- | ---------------------- | ------------------------------------------- |
| **Where in payload**      | `formulas.card[]`      | `formulas.dsUpdated[]`                      |
| **persistedOnDataSource** | `false`                | `true`                                      |
| **templateId**            | `-1`                   | Server-assigned integer                     |
| **owner**                 | Not included           | Required (user ID)                          |
| **Visibility**            | This card only         | All cards on this dataset                   |
| **API calls**             | 1 (read + merge + PUT) | 2 (POST to create, then read + merge + PUT) |
| **Reusable**              | No                     | Yes                                         |


---

## Data Types

Use the type returned by the validation endpoint when possible. Common values:


| Type      | Use For                                       |
| --------- | --------------------------------------------- |
| `LONG`    | Integers, counts, boolean flags (0/1)         |
| `DECIMAL` | Currency, percentages, ratios                 |
| `DOUBLE`  | High-precision decimals                       |
| `STRING`  | Text results (CONCAT, CASE returning strings) |
| `DATE`    | Date calculations                             |


---

## Troubleshooting


| Problem                                | Cause                                     | Fix                                                            |
| -------------------------------------- | ----------------------------------------- | -------------------------------------------------------------- |
| Validation returns `invalidColumns`    | Column name typo or missing backticks     | Check schema, wrap in backticks                                |
| Validation returns `INVALID` status    | Formula syntax error                      | Check parentheses, CASE/WHEN/END                               |
| PUT card returns 400                   | Incomplete card body                      | Make sure you read the card first and PUT the full merged body |
| Beast mode not visible in UI           | Wrong `persistedOnDataSource` value       | `false` = card-level, `true` = dataset-level                   |
| Card loses its chart/columns after PUT | PUT only included formulas, not full body | Always read the card definition first, merge, then PUT         |


---

## Output Format

When generating curl commands for the user, provide:

1. **What it does** — one sentence explaining the beast mode
2. **The formula** — so they can verify the logic
3. **Numbered curl commands** — in execution order, ready to copy/paste
4. **What to do with each response** — especially saving `legacyId` from Step 5a
5. **Verify** — tell them to check the card in Domo after running

