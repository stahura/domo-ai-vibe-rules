---
name: data-api
description: High-level entry skill for Domo data access. Routes detailed query work to dataset-query.
---

# Rule: Domo App Platform Data Access (Toolkit-First)

This rule is **toolkit/query-first**. Use `@domoinc/query` for dataset reads in apps.

> Legacy endpoint-first guidance has been archived to `archive/legacy-rules/domo-data-api.md`.

## Canonical Query Approach

### 1) Use `@domoinc/query` for dataset queries
```bash
yarn add @domoinc/query
```

```typescript
import Query from '@domoinc/query';

const salesByRegion = await new Query()
  .select(['region', 'Sales_Amount'])
  .groupBy('region', { Sales_Amount: 'sum' })
  .orderBy('Sales_Amount', 'descending')
  .fetch('sales');
```

### 2) Keep SQL as exception-only
If you use SQL (`SqlClient`), remember it does **not** automatically respect page filters in dashboards.

```typescript
import { SqlClient } from '@domoinc/toolkit';

const sqlClient = new SqlClient();
const result = await sqlClient.get(
  'sales',
  'SELECT region, SUM(Sales_Amount) AS total FROM sales GROUP BY region'
);
const rows = result.body.rows;
```

## Required Manifest Wiring

Every dataset still must be declared in `manifest.json` under `datasetsMapping`.

```json
{
  "datasetsMapping": [
    { "alias": "sales", "dataSetId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee", "fields": [] }
  ]
}
```

Critical gotcha:
- `fields` must exist (can be `[]`) to avoid manifest parsing errors.

## Local Development

- Use `@domoinc/ryuu-proxy` for local API routing.
- Authenticate with `domo login`.

## Canonical Rules References

- Query patterns and caveats: `.cursor/rules/03-query.mdc`
- Performance constraints: `.cursor/rules/10-performance-optimization.mdc`
- Query gotchas: `.cursor/rules/09-gotchas.mdc`

## Checklist
- [ ] `datasetsMapping` aliases configured and valid
- [ ] Queries implemented with `Query` (not raw `/data/v1` by default)
- [ ] Aggregations use actual dataset field names
- [ ] `.aggregate()` not used
