---
name: cap-apps-code-engine
description: Execute Code Engine functions from apps with domo.post and strict packagesMapping input/output contracts.
---

# Rule: Domo App Platform Code Engine (Toolkit-First)

Use a contract-first pattern for Code Engine calls.
In practice, prefer direct `domo.post('/domo/codeengine/v2/packages/{alias}', params)` when wiring app calls.

> Legacy endpoint-first guidance has been archived to `archive/legacy-rules/domo-code-engine.md`.

## Working call pattern (`domo.post`)

```bash
npm install ryuu.js
```

```typescript
import domo from 'ryuu.js';

const response = await domo.post('/domo/codeengine/v2/packages/calculateTax', {
  amount: 1000,
  state: 'CA'
});
```

## Response parsing requirement

```typescript
// First integration pass: inspect exact response shape for this function
console.log('Code Engine response:', response);

const body = response?.body ?? response?.data ?? response;

// Handle common output shapes
const output =
  body?.output ??
  body?.result ??
  body?.value ??
  body;

if (typeof output === 'number') {
  // numeric output
} else if (typeof output === 'string') {
  // string output
} else if (output && typeof output === 'object') {
  // structured object output
} else {
  throw new Error('Code Engine returned no usable output');
}
```

## Manifest requirement: `packagesMapping` (with `s`)

Use `packagesMapping` and define full parameter/output contracts.

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

## Required contract disclosure to user

When recommending or generating Code Engine calls, the agent must explicitly tell the user:
- exact input parameter names, types, and `nullable` expectations
- expected output name, type, and shape (number/string/object)

This is required so the user can build a matching Code Engine function and manifest contract.

## Error Handling Pattern

```typescript
async function executeFunction(alias: string, payload: Record<string, unknown>) {
  try {
    const response = await domo.post(`/domo/codeengine/v2/packages/${alias}`, payload);
    console.log('Code Engine response:', response);
    return response?.body ?? response?.data ?? response;
  } catch (error) {
    console.error(`Code Engine call failed for alias ${alias}`, error);
    throw error;
  }
}
```

## Related Skills & Rules

- Toolkit patterns: `cap-apps-toolkit`
- Manifest mapping details: `cap-apps-manifest`
- Operational gotchas: `rules/custom-app-gotchas.md`

## Checklist
- [ ] Calls use `domo.post('/domo/codeengine/v2/packages/{alias}', params)` pattern
- [ ] Manifest uses `packagesMapping` (not `packageMapping`)
- [ ] `packagesMapping.parameters` and `output` include full contract fields (`name`, `displayName`, `type`, `value`, `nullable`, `isList`, `children`, `entitySubType`, `alias`)
- [ ] Agent states input parameter names, types, and nullable status to user
- [ ] Agent states expected output name/type/shape to user
- [ ] First implementation logs response and validates real response shape
- [ ] Output parsing handles `body`/`data`/raw response shape
- [ ] Errors handled and surfaced to UI or logs
