---
name: manifest
description: Configure manifest mappings for datasets, workflows, collections, and Code Engine packagesMapping contracts.
---

# manifest.json

The `manifest.json` file is critical - it declares all external resources your app needs. Domo uses this to:
1. Know which datasets, collections, workflows, and code engine functions to connect
2. Map aliases (used in your code) to actual Domo resource IDs (configured at publish time)

For package create/update lifecycle details that feed `packagesMapping`, use:

- `skills/cli/code-engine-create/SKILL.md`
- `skills/cli/code-engine-update/SKILL.md`

## Basic structure
```json
{
  "name": "My App Name",
  "version": "1.0.0",
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "fullpage": true,
  "size": {
    "width": 4,
    "height": 3
  },
  "datasetsMapping": [],
  "collections": [],
  "workflowMapping": [],
  "packagesMapping": []
}
```

## Key properties
- `name` / `version` - App metadata
- `id` - **Generated on first publish** (see deployment section)
- `fullpage` - Set `true` for full-page apps
- `size` - Card dimensions (width/height in grid units)
- `datasetsMapping` - Datasets the app can query
- `collections` - AppDB collections for storage
- `workflowMapping` - Workflows the app can trigger
- `packagesMapping` - Code Engine function mappings and contracts

## Required files
- `manifest.json` - App configuration (required)
- `thumbnail.png` - App thumbnail image (required, must be 300x300 pixels, must be alongside manifest.json)

## Dataset Mapping Structure

```json
{
  "datasetsMapping": [
    {
      "alias": "transactions",           // Used in code: new Query().fetch('transactions')
      "dataSetId": "abc-123-def-456",   // ⚠️ Use 'dataSetId' NOT 'id'
      "fields": []                       // ⚠️ REQUIRED - must be present even if empty
    }
  ]
}
```

**Critical points:**
- Use `dataSetId` (not `id`) for the dataset identifier
- `fields` array is **required** - must be present even if empty `[]`
- Omitting `fields` causes: `Cannot read properties of undefined (reading 'map')`
- Alias names must be identifier-safe: letters/numbers only (recommended `^[A-Za-z][A-Za-z0-9]*$`)
- Do not use spaces, hyphens, dots, or other special characters in aliases

## Alias naming constraints (all mappings)

Applies to dataset aliases, Code Engine aliases, workflow aliases, and any alias your app code references.

```text
✅ Good: storeSales, Sales2026, RevenuePulse
❌ Bad: store-sales, store sales, store.sales, store@sales
```

If an alias includes special characters, runtime calls can fail or mappings can be hard to resolve consistently.

## Code Engine packagesMapping structure

```json
{
  "packagesMapping": [
    {
      "name": "myPackage",
      "alias": "myFunction",
      "packageId": "00000000-0000-0000-0000-000000000000",
      "version": "1.0.0",
      "functionName": "myFunction",
      "parameters": [
        {
          "name": "param1",
          "displayName": "param1",
          "type": "decimal",
          "value": null,
          "nullable": false,
          "isList": false,
          "children": [],
          "entitySubType": null,
          "alias": "param1"
        }
      ],
      "output": {
        "name": "result",
        "displayName": "result",
        "type": "number",
        "value": null,
        "nullable": false,
        "isList": false,
        "children": [],
        "entitySubType": null,
        "alias": "result"
      }
    }
  ]
}
```

Code Engine manifest gotchas:
- Use `packagesMapping` (with `s`), not `packageMapping`.
- Include full contract fields on each parameter and output.
- Ensure parameter names/types/nullability match what app code actually sends.
- Set explicit `packagesMapping[].version` (for example `"1.0.0"`) when you want deterministic behavior.
- `version: null` is treated as unpinned/latest behavior and will usually remain/display as `null` after publish.

## Collection Mapping Structure (`collectionsMapping`)

When wiring an app to an existing AppDB collection in published manifests, use `collectionsMapping` entries with `id` + `name`.

```json
{
  "collectionsMapping": [
    {
      "id": "47bd2c9e-b22d-4436-8265-4798be8b218e",
      "name": "RandomFunIdeas",
      "syncEnabled": false
    }
  ]
}
```

Collection mapping gotchas:
- Do not use ad-hoc keys like `alias` + `collectionId` in `collectionsMapping`; this can fail manifest parsing.
- `name` is required for mapped collection objects.
- For existing collection wiring, default `syncEnabled` to `false` unless app requirements explicitly call for synchronized dataset behavior.

## FileSets — no manifest entry needed

FileSets are the exception to the "declare everything in manifest" pattern. There is no `filesetsMapping` or equivalent key. Reference the fileset ID directly as a constant in your service code:

```javascript
// src/services/filesetApi.js
const FILESET_ID = 'b6ebf7e9-64ae-4e6d-b8ca-b356fe62923f';
```

The fileset ID is a UUID you get from the Domo UI or via `community-domo-cli filesets search`. See the `fileset-api` skill for the full API pattern.
