---
name: code-engine
description: Execute Code Engine functions from apps with domo.post and strict packagesMapping input/output contracts.
---

# Rule: Domo App Platform Code Engine (Toolkit-First)

Use a contract-first pattern for Code Engine calls.
In practice, prefer direct `domo.post('/domo/codeengine/v2/packages/{alias}', params)` when wiring app calls.

Package lifecycle operations are handled by CLI skills:

- `skills/cli/code-engine-create/SKILL.md`
- `skills/cli/code-engine-update/SKILL.md`

Use this skill for runtime invocation patterns inside app code, not package create/update orchestration.

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

// Some package contracts return nested envelopes:
// { response: { ... } } or { response: { response: { ... } } }
const unwrapResponse = (value: unknown) => {
  let current = value as any;
  let depth = 0;
  while (current && typeof current === 'object' && 'response' in current && depth < 6) {
    current = current.response;
    depth += 1;
  }
  return current;
};
const normalized = unwrapResponse(body);

// Handle common output shapes
const output =
  normalized?.output ??
  normalized?.result ??
  normalized?.value ??
  normalized;

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

Version pinning rule:
- If the user expects a fixed package build, set `"version": "x.y.z"` explicitly in each `packagesMapping` entry.
- Do not leave `version` as `null` unless the user explicitly wants unpinned/latest behavior.

## Required contract disclosure to user

When recommending or generating Code Engine calls, the agent must explicitly tell the user:
- exact input parameter names, types, and `nullable` expectations
- expected output name, type, and shape (number/string/object)
- whether output is wrapped in a `response` envelope (and if nested envelopes are possible)

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

## Discovering function names on global Domo packages

When calling a **Domo-provided global package** (e.g. DOMO Notifications, DOMO DataSets, DOMO Users),
the exported function names and their exact parameter signatures are not discoverable via the REST API
— `GET /api/codeengine/v2/packages/{id}/versions/{v}` returns `"functions": []` for all global packages.

**How to find them:** navigate to the package source in the Domo UI:

```
https://{instance}.domo.com/codeengine/{packageId}
```

This opens the Code Engine editor showing the full JavaScript source for the package. Read it to find:
- Exact exported function names (e.g. `sendEmail`, `sendBuzzRequest`)
- Positional parameter names and order (Code Engine maps by **position**, not key name)
- Which parameters are optional / nullable

> **Why this matters:** guessing function names against the API returns 404 for every wrong name,
> giving no indication of what the correct name is. Without reading the source first, you will
> burn multiple round-trips and may need the user to paste the source manually.

### Example — DOMO Notifications (`03ba6971-98d0-4654-9bfd-aa897816df33`)

Key functions found in source:

| Function | Parameters (positional) | Notes |
|---|---|---|
| `sendEmail` | `recipientEmails, subject, body, personRecipients, groupRecipients, attachments, attachment, includeReplyAll` | `recipientEmails` is a single comma-separated string, not an array |
| `sendEmailToListOfEmails` | `to, subject, body, attachments, attachment, includeReplyAll` | `to` is an array of strings |
| `sendBuzzRequest` | `channelId, message` | `channelId` must be a valid UUID |
| `sendExternalEmail` | `to, subject, body, attachments, attachment, includeReplyAll` | Validates against authorized domain whitelist |

> **Gotcha:** `sendEmail` takes `recipientEmails` as a plain string (e.g. `"user@example.com"`),
> not an array. Passing an array causes silent failure or incorrect routing.

## Checklist
- [ ] Read package source at `https://{instance}.domo.com/codeengine/{packageId}` before writing any call
- [ ] Exact function name confirmed from source (do not guess)
- [ ] Parameter names and types confirmed from source JSDoc comments
- [ ] Calls use `domo.post('/domo/codeengine/v2/packages/{alias}', params)` pattern
- [ ] Manifest uses `packagesMapping` (not `packageMapping`)
- [ ] `packagesMapping.version` is explicitly pinned when deterministic package behavior is required
- [ ] `packagesMapping.parameters` and `output` include full contract fields (`name`, `displayName`, `type`, `value`, `nullable`, `isList`, `children`, `entitySubType`, `alias`)
- [ ] Agent states input parameter names, types, and nullable status to user
- [ ] Agent states expected output name/type/shape to user
- [ ] First implementation logs response and validates real response shape
- [ ] Output parsing handles `body`/`data`/raw response shape and nested `response` envelopes
- [ ] Errors handled and surfaced to UI or logs
