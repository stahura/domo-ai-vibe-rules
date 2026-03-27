---
name: pb-apps-initial-build
description: "Orchestrates a new Domo custom app build or existing-app takeover from scratch. Loads rules, sequences capability skills, and tracks progress through manifest, data, UI, and publish phases. Use when starting a new Domo app project, taking over an existing app, or normalizing an app to platform best practices."
globs: "**/manifest.json"
---

# Domo App Initial Build Playbook

## When to use

- Use at project kickoff for a brand-new Domo custom app.
- Use when taking over an existing app and normalizing it to platform best practices.

## Progress checklist

Copy this checklist and update it as you work:

```
Build Progress:
- [ ] Phase 0: Rules loaded
- [ ] Phase 1: Manifest & contracts
- [ ] Phase 2: App shell (domo.js)
- [ ] Phase 3: Data access
- [ ] Phase 4: App storage (if needed)
- [ ] Phase 5: Toolkit clients (if needed)
- [ ] Phase 6: Feature skills (AI / Code Engine / Workflow — as needed)
- [ ] Phase 7: Performance review
- [ ] Phase 8: Build & publish
- [ ] Phase 9: Verification
```

## Phase 0 — Load rules (always-on)

Apply before writing any code:

- `rules/core-custom-apps-rule.md`
- `rules/custom-app-gotchas.md`

## Phase 1 — Manifest & contracts

Use `cap-apps-manifest`.

Define all external resource mappings first — datasets, collections, workflows, Code Engine packages. Everything else depends on this.

In addition to creation of the manifest.json, check root folder for an existing thumbnail.png to copy into the public folder of the new app.

**Existing-app takeover?** Audit the current `manifest.json` against actual code usage before changing anything.

## Phase 2 — App shell

Use `cap-apps-domo-js`.

Set up the baseline: `ryuu.js` import, navigation via `domo.navigate()`, event listeners, environment info.

**Advanced users using DA CLI?** Ask the agent to also use `cap-apps-da-cli` for scaffolding and manifest instance workflows.Should not be used unless user explicitly asks agent to use it.

## Phase 3 — Data access (if domo datasets need to be queried)

Use `cap-apps-dataset-query` (primary) and `cap-apps-data-api` (routing overview).

Build queries with `@domoinc/query`. Use the Query API for all dataset reads — it respects page filters and does server-side aggregation.

**Need raw SQL?** Use `cap-apps-sql-query`, but know that SQL ignores page filters.

## Phase 4 — App storage (if appdb , or any user data entry is needed)

Use `cap-apps-appdb`.

Skip if the app only reads datasets. Use AppDB when you need to persist app-specific state, user preferences, or document-style data.

## Phase 5 — Toolkit clients (if appdb, domo workflows, or domo sql query is needed)

Use `cap-apps-toolkit`.

Move to typed `@domoinc/toolkit` clients where they add value (structured responses, type safety). Not required for simple apps.

## Phase 6 — Feature skills (as needed)

Only load the skills your app actually requires (3 examples are listed here but you have access to many more skills):


| Feature needed                                 | Skill                       |
| ---------------------------------------------- | --------------------------- |
| AI text generation or text-to-SQL              | `cap-apps-ai-service-layer` |
| Server-side functions (secrets, external APIs) | `cap-apps-code-engine`      |
| Triggering automation workflows                | `cap-apps-workflow`         |


**Decision guide:** If the user hasn't mentioned AI, Code Engine, or Workflows, skip this phase entirely. Don't add complexity the app doesn't need.

## Phase 7 — Performance review

Use `cap-apps-performance`.

Review all queries before finalizing. Check for full-dataset fetches, missing aggregations, and unnecessary columns.

## Phase 8 — Build & publish

Use `cap-apps-publish`.

`npm run build` → `cd dist` → `domo publish`. On first publish, copy the generated `id` back to your source manifest.

## Phase 9 — Verification

After publishing, confirm:

- App loads without console errors in Domo
- All dataset aliases resolve (no 404s on data calls)
- AppDB collections are wired in the card UI (if used)
- Page filters propagate correctly (if app is embedded in a dashboard)
- Navigation uses `domo.navigate()`, not `<a href>`
- Thumbnail has been copied into public folder

## Build-time guardrails

- Client-side only: no SSR/server routes/server components.
- Use Vite `base: './'`.
- Prefer `HashRouter` unless rewrites are intentionally handled.
- Treat `domo.env.`* as convenience only; use verified identity for trust decisions.

