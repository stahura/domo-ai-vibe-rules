---
name: code-engine-create
description: Create Domo Code Engine packages from CLI workflows with deterministic payload contracts, automatic function parameter datatype mapping, and manifest packagesMapping follow-up guidance. Use when an agent must create a new package/versioned package container rather than only invoke an existing function from app runtime code.
---

# Code Engine Package Create (CLI)

Use this skill for package creation workflows, payload generation, and post-create mapping sync.

## Intent

This skill covers lifecycle operations that are out of scope for app-runtime invocation skills:

- create new package shell
- publish first package content payload
- infer and normalize function input/output datatypes
- update app `manifest.json` `packagesMapping` entries after create

For in-app function invocation patterns, use `skills/custom-apps/code-engine/SKILL.md`.

## Primary Execution Path

Prefer `community-domo-cli`:

```bash
community-domo-cli --instance <instance> code-engine create-package --body-file payload.json
```

Fallback endpoint when CLI path is unavailable:

```http
POST /api/codeengine/v2/packages
```

## Release Safety Rule

Hard rule: never call any Code Engine release endpoint unless the user explicitly says **"release"**.

- Do not infer release from context.
- Do not release as part of "finish", "publish", or "make it work".
- If release appears necessary, stop and ask for explicit release approval first.

## Required Payload Shape

```json
{
  "name": "My Package",
  "description": "Optional",
  "code": "// JS source",
  "environment": "LAMBDA",
  "language": "JAVASCRIPT",
  "manifest": {
    "functions": [
      {
        "name": "myFunction",
        "displayName": "My Function",
        "description": "",
        "inputs": [],
        "parameters": [],
        "output": {}
      }
    ],
    "configuration": {
      "accountsMapping": []
    }
  }
}
```

Create semantics:

- `POST /api/codeengine/v2/packages` creates a package or version payload target.
- For a new version on an existing package, include `id` and `version` in the create body and send full code/manifest payload.

## Datatype Mapping Rules (Auto-Map)

When generating `manifest.functions[].inputs/parameters/output`, apply these defaults:

- `payload`, `params`, `config`, `data`, `body`, `options` => `object`
- names indicating counts/limits/offsets => `decimal`
- boolean-like names (`is*`, `has*`, `enabled`, `required`) => `boolean`
- identifiers/text fields (`*id`, `name`, `query`, `message`) => `text`
- unknowns => `text`
- output default => `object`

Use the same type value for `type` and `dataType` when both fields are present.

## Post-Create Manifest Follow-up

After successful create, update app `manifest.json` `packagesMapping`:

- set `packageId` to created package id
- set `version` to returned version (or explicit target version)
- ensure each mapped function has matching `parameters` and `output`

If package ID/version changes, treat existing mapping as drift and sync immediately unless user requests otherwise.

## Post-Create Verification (Required)

After create, verify target package/version before declaring success:

1. `GET /api/codeengine/v2/packages/{packageId}`
2. Confirm target version exists and includes expected function names.
3. Confirm function inputs/outputs have expected datatypes and nullability.

If create returns an incomplete version shell (for example missing function contracts), hand off to update flow:

- `PUT /api/codeengine/v2/packages/{id}/versions/{version}` via `code-engine-update`
- Re-run verification after update

## Checklist

- [ ] CLI-first create attempted
- [ ] Endpoint fallback documented if CLI unavailable
- [ ] Payload contains `manifest.functions`
- [ ] Datatype mapping applied to each function input/output
- [ ] Release was **not** called unless user explicitly requested release
- [ ] Post-create verification completed on target package/version
- [ ] Incomplete create result routed to `code-engine-update` and re-verified
- [ ] `packagesMapping` updated in manifest after create
- [ ] Result includes package id/version for downstream steps
