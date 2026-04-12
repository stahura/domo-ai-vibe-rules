---
description: Always-on high-level Domo App Platform guardrails and skill routing.
alwaysApply: true
---

# Domo App Platform Core Rule

## Platform constraints (always apply)
- Domo custom apps are client-side only static apps.
- Do not use SSR patterns (`getServerSideProps`, Remix loaders/actions, SvelteKit server files, Nuxt server routes, `pages/api`, `app/api`, `"use server"`).
- If SSR is detected, stop and explicitly recommend client-side refactor (React + Vite) or Code Engine for server logic.
- **Exception — Embed host applications:** The embed skills (`programmatic-filters`, `edit-embed`) target the *host* application that embeds Domo content, not a Domo custom app. These require server-side code (API routes for OAuth token exchange, JWT signing) and use the Domo public API (`api.domo.com`) and Identity Broker — this is expected and correct. The client-only constraint does not apply to embed host apps.
- If a Domo custom app needs server-side functionality, require Code Engine package lifecycle steps (create/update package + manifest mapping sync) before adding runtime invocation calls.

## API boundary
- Use Domo App Platform APIs (`domo.js`, `@domoinc/query`, `@domoinc/toolkit`).
- Do not confuse with Domo public/product APIs unless explicitly requested.
- **Exception — Embed skills:** `programmatic-filters` and `edit-embed` use the Domo public API and Identity Broker by design. When these skills are active, public API usage (`api.domo.com/oauth/token`, `api.domo.com/v1/stories/embed/auth`, Identity Broker URLs) is expected.

## Build/routing non-negotiables
- Use relative asset base for Domo hosting (`base: './'`).
- Prefer `HashRouter` unless rewrite behavior is known and intentional.

## CLI skills are optional
- All skills under `skills/cli/` use the **community-domo-cli** (not the official Domo CLI `@domoinc/ryuu`). They automate tasks like creating AppDB collections, Code Engine packages, or fetching dataset/resource IDs.
- **Before using any `cli/` skill**, read `skills/cli/community-cli-howto/SKILL.md` first for install, auth setup, supported commands, and troubleshooting.
- These skills are **strictly optional helpers**. If the community CLI is not installed or the user does not want to use it, **skip those skills gracefully** and fall back to asking the user to provide the needed IDs/resources manually or perform the step in the Domo UI.
- Other skills (e.g. `code-engine`, `appdb`) may suggest using a `cli/` skill first. That suggestion is a convenience, not a requirement — it must **never block the build**.

## App Studio vs custom apps
- **`skills/custom-apps/`** — code that runs *inside* a Domo custom app card (data, AppDB, toolkit, manifest, publish).
- **`skills/app-studio/`** — building and operating *App Studio* apps (pages, layouts, native KPI cards, variables, beast modes, pro-code iframes). Start with `basic-app-studio` for copy-paste CLI operations; use `advanced-app-studio` for the full layout/theme/reference material.

## API index
- Data API
- AppDB
- AI Service Layer
- Code Engine
- Workflows
- Embed (Programmatic Filters, Dataset Switching, Edit Embed / Identity Broker)
- Files / Filesets / Groups / User / Task Center

## Skill routing
- New app build playbook -> `skills/(demo-skills)/basic-app-build/SKILL.md`
- App Studio micro-demo orchestration (pages, theme, heroes) -> `skills/(demo-skills)/app-studio-demo/SKILL.md`
- Dataset querying -> `skills/custom-apps/dataset-query/SKILL.md`
- Data API overview -> `skills/custom-apps/data-api/SKILL.md`
- domo.js usage -> `skills/custom-apps/domo-js/SKILL.md`
- Toolkit usage -> `skills/custom-apps/toolkit/SKILL.md`
- AppDB -> `skills/custom-apps/appdb/SKILL.md`
- Community CLI howto (start here for any CLI skill) -> `skills/cli/community-cli-howto/SKILL.md`
- AppDB collection create (datastore + collection lifecycle) -> `skills/cli/appdb-collection-create/SKILL.md`
- AI services -> `skills/custom-apps/ai-service-layer/SKILL.md`
- Code Engine -> `skills/custom-apps/code-engine/SKILL.md`
- Code Engine package create -> `skills/cli/code-engine-create/SKILL.md`
- Code Engine package update -> `skills/cli/code-engine-update/SKILL.md`
- Workflows -> `skills/custom-apps/workflow/SKILL.md`
- SQL queries -> `skills/custom-apps/sql-query/SKILL.md`
- Manifest wiring -> `skills/custom-apps/manifest/SKILL.md`
- Build/publish -> `skills/custom-apps/publish/SKILL.md`
- DA CLI -> `skills/custom-apps/da-cli/SKILL.md`
- Performance -> `skills/custom-apps/performance/SKILL.md`
- Filesets API -> `skills/custom-apps/fileset-api/SKILL.md`
- Migration from Lovable/v0 -> `skills/custom-apps/migrate-lovable/SKILL.md`
- Migration from Google AI Studio -> `skills/custom-apps/migrate-googleai/SKILL.md`
- App Studio (CLI operations only) -> `skills/app-studio/basic-app-studio/SKILL.md`
- App Studio (full CLI + reference) -> `skills/app-studio/advanced-app-studio/SKILL.md`
- App Studio pro-code embedded custom apps -> `skills/app-studio/app-studio-pro-code/SKILL.md`
- App Studio walkthrough video capture (Playwright) -> `skills/app-studio/app-studio-demo-capture/SKILL.md`
- Native KPI/card CRUD (Product API) -> `skills/app-studio/card-creation/SKILL.md`
- Beast modes -> `skills/app-studio/beast-mode-creation/SKILL.md`
- Card variables / controls -> `skills/app-studio/variable-creation/SKILL.md`
- Connector IDE -> `skills/connectors/connector-dev/SKILL.md`
- Programmatic embed filters / dataset switching -> `skills/domo-everywhere/programmatic-filters/SKILL.md`
- JS API filters -> `skills/domo-everywhere/jsapi-filters/SKILL.md`
- Edit embed / Identity Broker -> `skills/domo-everywhere/edit-embed/SKILL.md`
- Embed portal (full external-user portal) -> `skills/domo-everywhere/embed-portal/SKILL.md`
- HTML slide deck to PDF -> `skills/documents/html-deck/SKILL.md`
- Default app theme -> `skills/themes/domo-app-theme/SKILL.md`
