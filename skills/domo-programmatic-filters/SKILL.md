---
name: domo-programmatic-filters
description: Use this skill when a user is embedding a Domo dashboard or card and wants to control which rows of data each viewer sees, or swap the underlying dataset at embed time. Common scenarios: a sales rep should only see their region, tenants in a SaaS app should only see their own data, admins see everything but regular users see a subset, filters need to target specific datasets in a multi-dataset dashboard, or each tenant has their own dataset and needs dataset switching/redirects. Also covers SQL filters for complex WHERE logic (OR, BETWEEN, LIKE), JWT/token size limits when filter value lists are large, building the server-side embed token request with filter and datasetRedirects payloads, and the full OAuth access token to embed token flow. Trigger whenever someone has an embedded Domo visualization and needs per-viewer, per-role, per-tenant, or per-dataset data restrictions or dataset redirection. Do NOT trigger for Domo SSO setup, embed styling/branding, creating embed IDs, client-side Domo JS API filtering, Domo PDP policies inside Domo itself, or embedding non-Domo platforms like Tableau.
---

# Domo Programmatic Filtering

Programmatic filtering and dataset switching let you control what data each viewer sees in an embedded Domo dashboard or card — without provisioning individual Domo accounts. Filters and dataset redirects are applied server-side when generating an embed token, so they're enforced by Domo and can't be bypassed by the end user.

This skill covers server-side programmatic filtering and dataset switching. For client-side runtime filtering via the JS API, see the `domo-client-filters` skill.

## How It Works

A single Domo service account (proxy user) acts on behalf of all viewers. When someone loads your embedded content, your server:

1. Authenticates with Domo using OAuth client credentials → gets an **access token**
2. Requests an **embed token** from Domo, passing filters specific to that viewer
3. Returns the embed token to the client, which submits it to Domo via a POST form in an iframe

Domo enforces the filters at render time. The viewer only sees data that passes the filter criteria.

## Prerequisites

Before implementing programmatic filtering, you need:

- A Domo API client (created at developer.domo.com under My Account > New Client)
- The `CLIENT_ID` and `CLIENT_SECRET` from that API client
- An embed ID for your dashboard or card (the 5-character ID from the embed dialog, not the page URL)
- Knowledge of the dataset column names and IDs you want to filter on

**Important:** Authentication must happen server-side due to CORS restrictions. Never expose your client credentials or make token requests from the browser.

## The Embed Token Flow

### Step 1: Get an Access Token

Exchange your client credentials for an access token using Basic Auth:

```
POST https://api.domo.com/oauth/token?grant_type=client_credentials&scope=data%20audit%20user%20dashboard
Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)
```

The response includes an `access_token` you'll use in the next step.

**Example (Node.js):**
```typescript
const credentials = Buffer.from(`${CLIENT_ID}:${CLIENT_SECRET}`).toString('base64')

const response = await fetch(
  'https://api.domo.com/oauth/token?grant_type=client_credentials&scope=data%20audit%20user%20dashboard',
  {
    method: 'GET',
    headers: { Authorization: `Basic ${credentials}` }
  }
)

const { access_token } = await response.json()
```

**Example (Python):**
```python
import requests
from base64 import b64encode

credentials = b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()

response = requests.get(
    "https://api.domo.com/oauth/token",
    params={"grant_type": "client_credentials", "scope": "data audit user dashboard"},
    headers={"Authorization": f"Basic {credentials}"}
)

access_token = response.json()["access_token"]
```

### Step 2: Request an Embed Token with Filters

Use the access token to request an embed token, including your filters in the `authorizations` payload:

**For dashboards:**
```
POST https://api.domo.com/v1/stories/embed/auth
Authorization: Bearer {access_token}
Content-Type: application/json
```

**For cards:**
```
POST https://api.domo.com/v1/cards/embed/auth
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Payload structure:**
```json
{
  "sessionLength": 1440,
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "filters": [],
      "policies": []
    }
  ]
}
```

- `sessionLength`: Token validity in minutes (1440 = 24 hours)
- `token`: The embed ID for the dashboard or card
- `permissions`: Array of granted permissions — `READ`, `FILTER`, `EXPORT`
- `filters`: Array of standard filter objects (see below)
- `policies`: Array of PDP policy IDs to apply (optional)

The response includes an `authentication` property containing the embed token.

### Step 3: Render the Embed

Submit the embed token to Domo via a hidden POST form targeting an iframe:

**Dashboard URL:** `https://public.domo.com/embed/pages/{embed_id}`
**Card URL:** `https://public.domo.com/cards/{embed_id}`

```html
<iframe id="domo-embed" name="domo-embed" width="100%" height="600"></iframe>

<form id="embed-form" action="https://public.domo.com/embed/pages/{embed_id}" method="POST" target="domo-embed">
  <input type="hidden" name="embedToken" value="{embed_token}" />
</form>

<script>document.getElementById('embed-form').submit();</script>
```

The POST-based submission is required by Domo for security — it prevents the token from appearing in URLs or browser history.

---

## Filter Types

There are two ways to define programmatic filters: **standard filters** and **SQL filters**. Both are passed in the embed token request payload.

### Standard Filters

Passed via the `filters` array in the authorization object. Each filter targets a column with an operator and one or more values.

```json
{
  "column": "Region",
  "operator": "IN",
  "values": ["West", "East"]
}
```

**Required properties:**

| Property | Type | Description |
|----------|------|-------------|
| `column` | string | The exact column name in the dataset |
| `operator` | string | The comparison operator (see table below) |
| `values` | array | Values to filter against |

**Optional properties:**

| Property | Type | Description |
|----------|------|-------------|
| `datasourceId` | string (UUID) | Restrict filter to a specific dataset. Without this, the filter applies to all datasets in the embed that have a matching column name. |

#### Operators

| Operator | Description | Typical Use |
|----------|-------------|-------------|
| `IN` | Column value is in the list | Multi-value match |
| `NOT_IN` | Column value is not in the list | Exclusion |
| `EQUALS` | Column value equals | Single-value exact match |
| `NOT_EQUALS` | Column value does not equal | Single-value exclusion |
| `GREATER_THAN` | Column value is greater than | Numeric/date range |
| `GREATER_THAN_EQUALS_TO` | Column value is greater than or equal | Numeric/date range |
| `LESS_THAN` | Column value is less than | Numeric/date range |
| `LESS_THAN_EQUALS_TO` | Column value is less than or equal | Numeric/date range |

#### Standard Filter Examples

**Single filter — show only West region:**
```json
{
  "filters": [
    {
      "column": "Region",
      "operator": "IN",
      "values": ["West"]
    }
  ]
}
```

**Multiple filters — West region, revenue over 10000:**
```json
{
  "filters": [
    {
      "column": "Region",
      "operator": "IN",
      "values": ["West"]
    },
    {
      "column": "Revenue",
      "operator": "GREATER_THAN",
      "values": [10000]
    }
  ]
}
```

**Dataset-specific filter — only apply to one dataset in a multi-dataset dashboard:**
```json
{
  "filters": [
    {
      "column": "Region",
      "operator": "IN",
      "values": ["West"],
      "datasourceId": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

### SQL Filters

For complex filtering logic (OR conditions, BETWEEN, LIKE, nested expressions), use SQL WHERE clause syntax via the `sqlFilters` property. SQL filters are a sibling to `filters` in the authorization object, not nested inside it.

```json
{
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "filters": [],
      "sqlFilters": [
        {
          "sqlFilter": "`Region` IN ('West', 'East') AND `Revenue` > 10000",
          "datasourceIds": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"]
        }
      ]
    }
  ]
}
```

**Required properties:**

| Property | Type | Description |
|----------|------|-------------|
| `sqlFilter` | string | SQL WHERE clause syntax |

**Optional properties:**

| Property | Type | Description |
|----------|------|-------------|
| `datasourceIds` | string[] | Array of dataset UUIDs to apply the filter to |

#### SQL Filter Syntax Rules

- Wrap column names in **backticks**: `` `Column Name` ``
- Wrap string values in **single quotes**: `'value'`
- Numeric values need no quoting: `> 10000`
- Supports standard SQL operators: `IN`, `NOT IN`, `BETWEEN`, `LIKE`, `AND`, `OR`, `IS NULL`, `IS NOT NULL`
- Use parentheses for grouping complex logic

#### SQL Filter Examples

**OR condition (not possible with standard filters alone):**
```json
{
  "sqlFilter": "`Region` = 'West' OR `Department` = 'Sales'"
}
```

**BETWEEN for date ranges:**
```json
{
  "sqlFilter": "`Order Date` BETWEEN '2024-01-01' AND '2024-12-31'"
}
```

**LIKE for partial matching:**
```json
{
  "sqlFilter": "`Product Name` LIKE '%Pro%'"
}
```

**Complex nested logic:**
```json
{
  "sqlFilter": "(`Region` IN ('West', 'East') AND `Revenue` > 10000) OR `Priority` = 'Critical'"
}
```

**Targeting specific datasets:**
```json
{
  "sqlFilter": "`Status` = 'Active'",
  "datasourceIds": [
    "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"
  ]
}
```

### Combining Standard and SQL Filters

You can use both `filters` and `sqlFilters` in the same authorization. Standard filters are applied first, then SQL filters further narrow the results. This is useful when you have simple per-column filters alongside more complex logic:

```json
{
  "token": "<embed_id>",
  "permissions": ["READ", "FILTER", "EXPORT"],
  "filters": [
    {
      "column": "Region",
      "operator": "IN",
      "values": ["West"]
    }
  ],
  "sqlFilters": [
    {
      "sqlFilter": "`Revenue` > 10000 OR `Priority` = 'Critical'"
    }
  ]
}
```

---

## Common Patterns

### Per-User Filtering

The most common pattern: each user sees only their own data. Store the user-to-filter mapping in your application's database and look it up at embed time.

```typescript
// Pseudocode — adapt to your framework and data layer
async function getEmbedTokenForUser(userId: string, embedId: string) {
  const user = await getUser(userId)
  const dashboard = user.dashboards.find(d => d.embedId === embedId)

  const filters = dashboard.filters.map(f => ({
    column: f.column,
    operator: f.operator,
    values: f.values
  }))

  const accessToken = await getDomoAccessToken()
  const embedToken = await getDomoEmbedToken(accessToken, embedId, filters)

  return embedToken
}
```

### Role-Based Filtering

Apply different filters based on user role rather than individual assignments:

```typescript
function getFiltersForRole(role: string): Filter[] {
  switch (role) {
    case 'regional-manager':
      return [{ column: 'Region', operator: 'IN', values: [user.region] }]
    case 'executive':
      return [] // No filters — sees everything
    case 'analyst':
      return [{ column: 'Department', operator: 'EQUALS', values: [user.department] }]
    default:
      return [{ column: 'Public', operator: 'EQUALS', values: ['true'] }]
  }
}
```

---

## Dataset Switching

Dataset switching lets you dynamically redirect the underlying data of an embedded dashboard at embed time. Instead of combining all customer data into one master dataset and filtering with PDP or programmatic filters, you can maintain separate datasets per customer (or tenant, region, etc.) and swap them in when generating the embed token.

This is useful when:
- Each customer has their own isolated dataset (common in multi-tenant architectures)
- You want to reuse a single dashboard template across different data sources
- Datasets have the same schema but different data (e.g., per-region copies)

### How It Works

Pass a `datasetRedirects` mapping in the authorization object. The keys are the original dataset IDs (the ones the dashboard was built on), and the values are the target dataset IDs to swap in:

```json
{
  "sessionLength": 1440,
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "filters": [],
      "datasetRedirects": {
        "original-dataset-uuid-1": "target-dataset-uuid-1",
        "original-dataset-uuid-2": "target-dataset-uuid-2"
      }
    }
  ]
}
```

The target datasets must have the same column schema (column names and types) as the originals. If they don't, cards that reference missing or mismatched columns will break.

### Combining Dataset Switching with Filters

Dataset switching and programmatic filters work together. First the dataset is swapped, then filters are applied to the swapped dataset:

```json
{
  "sessionLength": 1440,
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "datasetRedirects": {
        "a19d0ef1-ca31-4bfd-b168-018b93109671": "a19d0ef1-ca31-4bfd-b168-018b93109672"
      },
      "filters": [
        { "column": "Color", "operator": "IN", "values": ["Red"] },
        { "column": "Model", "operator": "IN", "values": ["Mountain", "Road", "Commuter"] }
      ]
    }
  ]
}
```

This is the most powerful pattern for multi-tenant embedding: swap to the tenant's dataset, then further filter rows within it.

### Per-User Dataset Switching

A typical implementation maps each user or tenant to their own dataset IDs:

```typescript
function getDatasetRedirects(tenant: Tenant): Record<string, string> {
  // The template dashboard was built on these "original" datasets
  const templateDatasets = {
    sales: 'aaaa-bbbb-cccc-dddd',
    inventory: 'eeee-ffff-gggg-hhhh'
  }

  // Each tenant has their own copies
  return {
    [templateDatasets.sales]: tenant.salesDatasetId,
    [templateDatasets.inventory]: tenant.inventoryDatasetId
  }
}
```

### Important Notes

- **Schema must match:** Target datasets must have the same column names and types as the originals. The dashboard's cards, filters, and calculated fields all reference columns by name.
- **Multiple datasets:** A single dashboard can use multiple datasets. You can redirect all, some, or none of them. Only include redirects for datasets you want to swap.
- **Works with all filter types:** Dataset switching is compatible with standard filters, SQL filters, and PDP policies. Redirects are applied first, then filters run against the redirected data.

---

## Gotchas and Best Practices

### JWT Size Limit
Browsers enforce a ~8KB limit on the JWT used for programmatic filters. If you have filters with extremely long value lists (hundreds of entries), you'll hit this limit. Solutions:
- Transform your data in Domo to create aggregated or grouped columns that reduce the number of filter values needed
- Use SQL filters with subqueries if your filter logic can be simplified
- Split across multiple datasets with `datasourceId` targeting

### Column Name Matching
- Standard filters match by exact column name — spelling and case must match the dataset column
- SQL filters use backtick-quoted column names: `` `My Column` ``
- If a column name exists in multiple datasets on the same dashboard and you don't specify `datasourceId`/`datasourceIds`, the filter applies to all of them

### Token Refresh
Access tokens and embed tokens both expire. Build refresh logic into your server:
- Cache the access token and refresh it before expiry
- Generate embed tokens per-request (they're scoped to a specific session)

### Empty Filters
Passing an empty `filters` array (`[]`) means no filtering — the viewer sees all data the proxy user has access to. This is valid for users who should see everything. Never omit the `filters` key entirely; always pass at least an empty array.

### Filter Validation
Validate filters server-side before sending them to Domo. Common issues:
- `values` must be an array, even for single-value operators like `EQUALS` — pass `["value"]` not `"value"`
- Numeric values should be actual numbers, not strings: `[10000]` not `["10000"]`
- Operator names are exact: `GREATER_THAN_EQUALS_TO` not `GREATER_THAN_OR_EQUAL`

### Security
- Never generate embed tokens client-side — your OAuth credentials would be exposed
- Validate that the requesting user is authorized to view the requested embed ID
- Validate filter values server-side to prevent users from manipulating their own filters
- Use the minimum necessary `permissions` array — don't grant `EXPORT` if users shouldn't export data

---

## TypeScript Type Definitions

For reference, here are useful type definitions when implementing programmatic filtering:

```typescript
type FilterOperator =
  | 'IN'
  | 'NOT_IN'
  | 'EQUALS'
  | 'NOT_EQUALS'
  | 'GREATER_THAN'
  | 'GREATER_THAN_EQUALS_TO'
  | 'LESS_THAN'
  | 'LESS_THAN_EQUALS_TO'

interface StandardFilter {
  column: string
  operator: FilterOperator
  values: (string | number)[]
  datasourceId?: string
}

interface SqlFilter {
  sqlFilter: string
  datasourceIds?: string[]
}

type EmbedPermission = 'READ' | 'FILTER' | 'EXPORT'

interface EmbedAuthorization {
  token: string
  permissions: EmbedPermission[]
  filters: StandardFilter[]
  sqlFilters?: SqlFilter[]
  policies?: string[]
  datasetRedirects?: Record<string, string>  // originalDatasetId → targetDatasetId
}

interface EmbedTokenRequest {
  sessionLength: number
  authorizations: EmbedAuthorization[]
}
```

---

## Quick Reference

Read `references/api-endpoints.md` for the complete list of Domo API endpoints used in programmatic filtering.
