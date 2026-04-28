# Domo Workflow API Reference

Full endpoint reference for Domo Workflow authoring operations. All paths are relative to `https://<instance>.domo.com/api`.

## Workflow Models

### List Models
```
GET /workflow/v2/models
```
**Params:** `limit`, `offset`

---

### Get Model
```
GET /workflow/v1/models/{workflowId}?parts=users
```

---

### Create Model Shell
```
POST /workflow/v2/models
```
**Body:**
```json
{
  "name": "My Workflow",
  "description": "Optional description",
  "versions": [{ "version": "1.0.0" }]
}
```
**Returns:** `{ id, versions: [{ version }] }` — `version` in the response is an integer (e.g., `1`). Use this integer (not `"1.0.0"`) for all subsequent version-scoped calls.

---

### Update Definition (PUT)
```
PUT /workflow/v2/models/{workflowId}/versions/{semver}/definition
```
**Body:** Full workflow definition object. See `definition-schema.md`.

`{semver}` must be a full semantic version string (e.g., `1.0.0` or `1.0.1`), NOT a bare integer. Passing an integer returns a 400 SemanticVersion conversion error. The CLI `update-definition` command auto-converts for you.

This is the primary authoring operation. Must be a `PUT` — the path does not accept `POST`.

---

### Get Definition (GET)
```
GET /workflow/v2/models/{workflowId}/versions/{semver}/definition
```
Returns the stored workflow definition for a specific version. Use this to:
- Inspect what was actually persisted (debugging)
- Fetch a reference definition to adapt for a new workflow
- Verify a push succeeded

`{semver}` follows the same semver format requirement as Update Definition. The CLI `get-definition` command auto-converts bare integers.

---

### Validate Definition
```
POST /workflow/v2/models/validate
```
**Body:** Full workflow definition object.

Non-mutating. Returns structural validation errors (missing fields, disconnected nodes, invalid types). Does not validate SQL queries or Code Engine input names.

---

### Validate Dataset Query (in workflow context)
```
POST /workflow/v1/models/{workflowId}/versions/{version}/servicetasks/datasetQuery
```
**Body:**
```json
{
  "variables": {
    "dataset": "<dataset-uuid>",
    "query": "SELECT region, SUM(amount) FROM table GROUP BY region"
  }
}
```
Validates SQL against the dataset within the context of the specific workflow version. Use this for every dataset-query step before treating the definition final.

---

### List Instances (Runs)
```
GET /workflow/v1/models/{workflowId}/instances
```
**Params:** `limit`, `offset`

---

### Get Instance
```
GET /workflow/v1/models/{workflowId}/instances/{instanceId}
```

---

## Triggers

### Create Trigger
```
POST /workflow/v2/triggers
```
**Body:**
```json
{
  "modelId": "<workflow-id>",
  "type": "SCHEDULED",
  "schedule": {
    "cron": "0 9 * * MON-FRI"
  }
}
```

---

### List Triggers
```
GET /workflow/v2/triggers
```
**Params:** `modelId` (optional, filter by workflow)

---

## Forms

### Create Workflow Form (Start or Task)
The same endpoint creates both start forms (triggered at workflow entry) and user task forms (shown to the approver/reviewer during a `userTaskNode` step). Set `domainId` to `"<workflow-id> - <version>"` for both types; the distinction is which node references the returned `formId`.

```
POST /forms/v2
```
**Body:**
```json
{
  "name": "My Form Name",
  "domainId": "<workflow-id> - <version>",
  "domainType": "WORKFLOW",
  "settings": {},
  "attributes": [{ "type": "paragraph", "children": [{ "text": "" }] }],
  "sections": [
    {
      "id": "<uuid>",
      "title": "",
      "description": "",
      "fields": [ ... ]
    }
  ],
  "fieldConfiguration": { "<field-uuid>": { "targetMapping": { "target": "<field-alias>" } } },
  "submitConfiguration": { "type": "WORKFLOW" },
  "searchable": false
}
```

**`submitConfiguration.type`** differs between form kinds:
- **Start form** → `"WORKFLOW"` — form fires the workflow on submit.
- **User task form** → `"UNASSIGNED"` — form is shown as part of a pending user task; the node (not the form) decides the assignee. Also add a top-level `"submitConfigurationType": "UNASSIGNED"` field to match what the API stores.

**`fieldConfiguration`** maps each field UUID to `{ "targetMapping": { "target": "<alias>" } }`. This is what the UI reads to display the mapping between fields and their aliases. It is not strictly required on create for start forms (you can pass `{}`), but user-task forms with mixed read-only/response fields behave more predictably when each field is listed here. Populate it for every field using the field's `alias`.

**IMPORTANT — `id` field:** The API ignores any top-level `id` you provide in the request body and assigns its own UUID. Always capture the `id` from the response and use that as the `formId` in your definition — do not reuse the UUID you sent.

Each field in `fields` must have a unique UUID `id`.

**Field shape (CRITICAL):** Use `fieldType` (NOT `type`). Every field must include `optional`, `alias`, `options`, `useExternalValues`, and `displayAsDropdown` — omitting any causes "This has not been properly configured" in the UI.

Each field has two independent properties that map to the two dropdowns in the form builder UI:
- **`fieldType`** — the *answer type* (how the field renders)
- **`dataType`** — the *data type* of the value stored

```json
{
  "id": "<uuid>",
  "label": "Voter Name",
  "description": "Enter your name",
  "fieldType": "SHORT_ANSWER",
  "dataType": "text",
  "required": true,
  "isList": false,
  "acceptsInput": true,
  "acceptsOutput": false,
  "readOnly": false,
  "optional": false,
  "alias": "voterName",
  "options": {},
  "useExternalValues": false,
  "displayAsDropdown": false
}
```

**The three field roles on a user task form** — a single form can contain all three:

| Role in task | `acceptsInput` | `acceptsOutput` | `readOnly` | Node wiring |
|---|---|---|---|---|
| Read-only display (shows workflow variable to the assignee) | `true` | `false` | `true` | `userTaskNode.input[]` |
| Editable with pre-filled value (shows current value AND captures edit) | `true` | `true` | — (omit or `false`) | Listed in BOTH `userTaskNode.input[]` and `userTaskNode.output[]` |
| Response only (blank entry captured from assignee) | `false` | `true` | — | `userTaskNode.output[]` |

- `readOnly: true` is what prevents the assignee from editing a field that's used to display workflow data. Without it, a field with `acceptsInput: true, acceptsOutput: false` still renders as editable in some UIs.
- For a start form (rootNode), every field is effectively response-only from the user's perspective — use `acceptsInput: true, acceptsOutput: false` (and omit `readOnly`) so the user can fill in the initial value that becomes the workflow variable.
- `alias` must match the `paramName` used in the rootNode/userTaskNode entries that bind the field to a workflow variable.

**`fieldType` + `dataType` combinations:**

| UI Answer Type | `fieldType` | `dataType` | Notes |
|---|---|---|---|
| Short Answer (text) | `SHORT_ANSWER` | `text` | Single-line text input |
| Short Answer (number) | `SHORT_ANSWER` | `number` | Single-line, numeric |
| Short Answer (decimal) | `SHORT_ANSWER` | `decimal` | Single-line, decimal |
| Paragraph | `PARAGRAPH` | `text` | Multi-line textarea |
| Date / Time | `DATE_TIME` | `date` | Date picker |
| Single Choice - Radio | `SINGLE_CHOICE` | `text` | Radio buttons |
| Single Choice - Dropdown | `SINGLE_CHOICE` | `text` | Use `displayAsDropdown: true` |
| Multiple Choice - Checkbox | `MULTI_CHOICE` | `text` | Checkboxes |
| Multiple Choice - Dropdown | `MULTI_CHOICE` | `text` | Use `displayAsDropdown: true` |
| Person | `SHORT_ANSWER` | `person` | Person picker |
| Dataset | `SHORT_ANSWER` | `dataset` | Dataset picker |
| Group | `SHORT_ANSWER` | `group` | Group picker |

**`options` must be `{}` (empty object, NOT `[]` array).** The API rejects an array value for `options`, even for fields that have no choices. For choice-based fields use `{ "values": ["Option A", "Option B"], "acceptsOther": false }`.

**Do NOT use `fieldType: "NUMBER"`, `"DATE"`, or `"LONG_ANSWER"`** — these are not valid form field types. Use the correct `fieldType` + `dataType` combinations from the table above (e.g. `SHORT_ANSWER` + `number` for a number field, `PARAGRAPH` + `text` for a textarea, `DATE_TIME` + `date` for a date picker).

**`customMappingType` must be `""` (empty string, NOT null)** on all input/output parameter objects. Passing `null` returns:
> Instantiation of WorkflowFormInputOutput failed for JSON property customMappingType due to missing (therefore NULL) value

---

### Get Form
```
GET /forms/v2/{formId}
```
Returns the full form JSON as stored, including the actual field UUIDs assigned by the API. Use this to:
- Retrieve real field IDs after creation (needed for wiring `rootNode.input[].formFieldId` and `userTaskNode.input/output[]` in the definition)
- Verify `fieldType` normalization didn't change expected types
- Debug form configuration issues

---

## Queues

### List Queues
```
GET /queues/v1?combineAttributes=true&archived=false
```

---

### Create Queue
```
POST /queues/v1
```
**Body:** Queue payload (name, description, type, assignment rules).

---

## Code Engine (Discovery for Workflow Service Tasks)

### List Packages
```
GET /codeengine/v2/packages
```
**Params:** `ownedById` (optional)

---

### Get Package (Full Function Definitions)
```
GET /codeengine/v2/packages/{packageId}?parts=functions
```
Returns the full package object including all versions and their function definitions. The CLI (`code-engine get-package`) strips `thumbnail` fields from the response automatically.

---

### Search Packages
```
POST /search/v1/query
```
Used by `community-domo-cli code-engine search-packages`. The CLI strips `thumbnail` fields automatically.

**Response shape** (critical — non-obvious):
```json
{
  "searchObjects": [
    {
      "uuid": "<packageId>",
      "name": "DOMO Groups",
      "description": "...",
      "ownedById": "27",
      "ownedByName": "DomoSupport",
      "functions": [...],
      "packageLanguage": "JAVASCRIPT"
    }
  ],
  "totalResultCount": 39,
  "facetMap": { ... }
}
```

- The package ID is in **`uuid`**, NOT `id` or `databaseId`. Use `searchObjects[i].uuid` as the `packageId` in subsequent `get-package` and `get-function-signature` calls.
- Results live under `searchObjects`, not `packages` or `results`.
- Each `searchObjects` entry is type `"package"` (confirmed by `entityType` field).

---

### Get Function Signature (Lightweight)
```
GET /codeengine/v2/packages/{packageId}/versions/{version}?parts=functions
```
Filter to one function client-side by `name`. Returns `inputs` and `output` for that function.

**Use this to verify exact input parameter names before wiring a workflow step.** A mismatch between step `inputs` keys and the function's declared parameter names causes silent runtime failures.

---

## Datasets (Discovery for Dataset-Query Steps)

### Search Datasets
```
POST /data/ui/v3/datasources/search
```
**Body:**
```json
{
  "entities": ["DATASET"],
  "filters": [{ "field": "name_sort", "filterType": "wildcard", "query": "*keyword*" }],
  "combineResults": true,
  "query": "*",
  "count": 100,
  "offset": 0,
  "sort": { "isRelevance": false, "fieldSorts": [{ "field": "create_date", "sortOrder": "DESC" }] }
}
```
**Returns:** `{ dataSources: [{ id, name }] }`

---

### Get Dataset Schema
```
GET /query/v1/datasources/{datasetId}/schema/indexed?includeHidden=true
```
Returns column names and types. Use to confirm column names before writing SQL in dataset-query steps.

---

## Users and Groups (ID Resolution for Task Assignments)

### Search Users
```
POST /identity/v1/users/search?explain=false
```
**Body:**
```json
{
  "filters": [],
  "sort": { "field": "displayName", "order": "ASC" },
  "count": 50,
  "offset": 0
}
```

---

### List Groups
```
GET /content/v2/groups/grouplist?ascending=true&sort=name&limit=100&offset=0&includeFullMembership=false
```
