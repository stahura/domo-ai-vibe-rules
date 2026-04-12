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
- Dataset querying -> `~/.agents/skills/dataset-query/SKILL.md`
- Data API overview -> `~/.agents/skills/data-api/SKILL.md`
- domo.js usage -> `~/.agents/skills/domo-js/SKILL.md`
- Toolkit usage -> `~/.agents/skills/toolkit/SKILL.md`
- AppDB -> `~/.agents/skills/appdb/SKILL.md`
- AI services -> `~/.agents/skills/ai-service-layer/SKILL.md`
- Code Engine -> `~/.agents/skills/code-engine/SKILL.md`
- Workflows -> `~/.agents/skills/workflow/SKILL.md`
- SQL queries -> `~/.agents/skills/sql-query/SKILL.md`
- Manifest wiring -> `~/.agents/skills/manifest/SKILL.md`
- Build/publish -> `~/.agents/skills/publish/SKILL.md`
- DA CLI -> `~/.agents/skills/da-cli/SKILL.md`
- Performance -> `~/.agents/skills/performance/SKILL.md`
- Filesets API -> `~/.agents/skills/fileset-api/SKILL.md`
- Migration from Lovable/v0 -> `~/.agents/skills/migrate-lovable/SKILL.md`
- Migration from Google AI Studio -> `~/.agents/skills/migrate-googleai/SKILL.md`
- Programmatic embed filters / dataset switching -> `~/.agents/skills/programmatic-filters/SKILL.md`
- JS API filters -> `~/.agents/skills/jsapi-filters/SKILL.md`
- Edit embed / Identity Broker -> `~/.agents/skills/edit-embed/SKILL.md`
- Embed portal (full external-user portal) -> `~/.agents/skills/embed-portal/SKILL.md`
- HTML slide deck to PDF -> `~/.agents/skills/html-deck/SKILL.md`
- Default app theme -> `~/.agents/skills/domo-app-theme/SKILL.md`
