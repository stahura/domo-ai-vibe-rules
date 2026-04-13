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

## Two CLIs — know which to use
- **`domo` (official Domo CLI, `@domoinc/ryuu`)**: only for `domo login`, `domo dev`, and `domo publish`.
- **`community-domo-cli`**: required for Domo Product API operations (datasets, app-studio, cards, dataflows, appdb, code-engine, filesets, workflows, pages, beast-modes, variables, domoapps, files, users, pdp).
- **`python -m datagen` (`domo_data_generator`)**: separate tool for sample-data generation and dataset create/upload flows that call Domo public APIs directly. This is the current path for datagen dataset provisioning until equivalent coverage lands in `community-domo-cli`.
- If you need schema fetches, card create/update, dataflow commands, or Product API CLI calls, the command must start with `community-domo-cli` (never `domo`).
- Auth flow: run `domo login` once, then run `community-domo-cli` using `DOMO_INSTANCE` plus `DOMO_AUTH_MODE=ryuu-session`.
- Datagen auth is different from ryuu session: create a local `.env` with `DOMO_CLIENT_ID` and `DOMO_CLIENT_SECRET` (and other datagen vars) before running `python -m datagen ...`.
- **Before using any CLI skill**, read `~/.agents/skills/community-cli-howto/SKILL.md` first for install, auth setup, supported commands, and troubleshooting.

## App Studio vs custom apps
- **Custom app skills** (`dataset-query`, `appdb`, `toolkit`, `manifest`, `publish`, etc.) — code that runs *inside* a Domo custom app card.
- **App Studio skills** (`basic-app-studio`, `advanced-app-studio`, `card-creation`, `beast-mode-creation`, `variable-creation`, `app-studio-pro-code`) — building and operating *App Studio* apps. Start with `basic-app-studio` for copy-paste CLI operations; use `advanced-app-studio` for full layout/theme/reference material.

## API index
- Data API
- AppDB
- AI Service Layer
- Code Engine
- Workflows
- Embed (Programmatic Filters, Dataset Switching, Edit Embed / Identity Broker)
- Files / Filesets / Groups / User / Task Center

## Skill routing
- New app build playbook -> `~/.agents/skills/basic-custom-app-build/SKILL.md`
- App Studio + dataset/ETL vertical demo -> `~/.agents/skills/app-studio-dataset-etl-gen-demo/SKILL.md`
- Dataset querying -> `~/.agents/skills/dataset-query/SKILL.md`
- Data API overview -> `~/.agents/skills/data-api/SKILL.md`
- domo.js usage -> `~/.agents/skills/domo-js/SKILL.md`
- Toolkit usage -> `~/.agents/skills/toolkit/SKILL.md`
- AppDB -> `~/.agents/skills/appdb/SKILL.md`
- Community CLI howto (start here for any CLI skill) -> `~/.agents/skills/community-cli-howto/SKILL.md`
- AppDB collection create (datastore + collection lifecycle) -> `~/.agents/skills/appdb-collection-create/SKILL.md`
- AI services -> `~/.agents/skills/ai-service-layer/SKILL.md`
- Code Engine -> `~/.agents/skills/code-engine/SKILL.md`
- Code Engine package create -> `~/.agents/skills/code-engine-create/SKILL.md`
- Code Engine package update -> `~/.agents/skills/code-engine-update/SKILL.md`
- Workflows -> `~/.agents/skills/workflow/SKILL.md`
- SQL queries -> `~/.agents/skills/sql-query/SKILL.md`
- Manifest wiring -> `~/.agents/skills/manifest/SKILL.md`
- Build/publish -> `~/.agents/skills/publish/SKILL.md`
- DA CLI -> `~/.agents/skills/da-cli/SKILL.md`
- Performance -> `~/.agents/skills/performance/SKILL.md`
- Filesets API -> `~/.agents/skills/fileset-api/SKILL.md`
- Filesets CLI -> `~/.agents/skills/fileset-cli/SKILL.md`
- Migration from Lovable/v0 -> `~/.agents/skills/migrate-lovable/SKILL.md`
- Migration from Google AI Studio -> `~/.agents/skills/migrate-googleai/SKILL.md`
- App Studio (CLI operations only) -> `~/.agents/skills/basic-app-studio/SKILL.md`
- App Studio (full CLI + reference) -> `~/.agents/skills/advanced-app-studio/SKILL.md`
- App Studio pro-code embedded custom apps -> `~/.agents/skills/app-studio-pro-code/SKILL.md`
- App Studio walkthrough video capture (Playwright) -> `~/.agents/skills/app-studio-demo-capture/SKILL.md`
- Native KPI/card CRUD (Product API) -> `~/.agents/skills/card-creation/SKILL.md`
- Beast modes -> `~/.agents/skills/beast-mode-creation/SKILL.md`
- Card variables / controls -> `~/.agents/skills/variable-creation/SKILL.md`
- Connector IDE -> `~/.agents/skills/connector-dev/SKILL.md`
- Programmatic embed filters / dataset switching -> `~/.agents/skills/programmatic-filters/SKILL.md`
- JS API filters -> `~/.agents/skills/jsapi-filters/SKILL.md`
- Edit embed / Identity Broker -> `~/.agents/skills/edit-embed/SKILL.md`
- Embed portal (full external-user portal) -> `~/.agents/skills/embed-portal/SKILL.md`
- HTML slide deck to PDF -> `~/.agents/skills/html-deck/SKILL.md`
- Default app theme -> `~/.agents/skills/domo-app-theme/SKILL.md`
- Magic ETL (API-first / mixed) -> `~/.agents/skills/magic-etl/SKILL.md`
- Magic ETL (community-domo-cli dataflows) -> `~/.agents/skills/magic-etl-cli/SKILL.md`
- Sample data generation + upload -> `~/.agents/skills/domo-data-generator/SKILL.md`
- Workspaces admin -> `~/.agents/skills/workspaces/SKILL.md`
