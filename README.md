# Domo Agent Skills

> Unofficial community repository of Domo agent skills and rules.

A library of markdown-only Agent Skills and high-level rules for building Domo custom apps, embedding Domo content, and developing connectors.
The structure is modeled after Google’s `stitch-skills` repository style: skill catalog at the root, one entrypoint file per skill, and simple install/discovery guidance.

## Installation & Discovery

Install skills from a GitHub repository with the `skills` CLI:

```bash
# List skills in this repository
npx skills add stahura/domo-ai-vibe-rules --list

# Install one skill globally
npx skills add stahura/domo-ai-vibe-rules --skill cap-apps-domo-js --global
```

For new Domo app builds, ask your agent to start with the `pb-apps-initial-build` skill first, then follow its recommended skill order.

## Why This Taxonomy

Domo is a broad platform — "data query" means something completely different when you're querying from a custom app vs. a Python script vs. an embedded dashboard. A flat list of skills becomes ambiguous fast, so every skill is categorized by **type**, **feature area**, and **name** using the pattern `{type}-{feature}-{name}`.

### Skill types

| Prefix | Type | What it is | Example |
|--------|------|-----------|---------|
| `cap-` | **Capability** | Atomic, single-topic skill. One API, one tool, one concept. | `cap-apps-appdb` |
| `wf-` | **Workflow** | Multi-step procedure that composes several capabilities for a bounded job. | `wf-apps-migrate-lovable` |
| `pb-` | **Playbook** | End-to-end orchestration runbook for a full outcome. References capabilities and workflows in order. | `pb-apps-initial-build` |

### Feature areas

| Segment | Scope |
|---------|-------|
| `apps-` | Domo App Platform custom apps |
| `de-` | Domo Everywhere (embedding) |
| `connector-` | Custom Connector IDE |

More feature areas (e.g. `dataflow-`, `sdk-`) can be added as new skills are contributed.

## Available Skills

### Playbooks (`pb-`)

- `pb-apps-initial-build` - Kickoff sequence for new Domo app builds; routes to the right rules and skills in order.

### Capabilities (`cap-`)

**App Platform**
- `cap-apps-da-cli` - Recommended for advanced users using DA CLI; ask your agent to use this skill for advanced scaffolding, generation, and manifest instance workflows.
- `cap-apps-publish` - Build and publish flow (`npm run build`, `cd dist`, `domo publish`).
- `cap-apps-domo-js` - `ryuu.js` usage, navigation/events, and import safety.
- `cap-apps-dataset-query` - Detailed `@domoinc/query` syntax and constraints.
- `cap-apps-data-api` - High-level data-access routing skill; points to query skill.
- `cap-apps-toolkit` - `@domoinc/toolkit` client usage and response handling.
- `cap-apps-appdb` - Toolkit-first AppDB CRUD/query patterns.
- `cap-apps-ai-service-layer` - Toolkit-first AI client usage and parsing.
- `cap-apps-code-engine` - Code Engine function invocation patterns and contracts.
- `cap-apps-workflow` - Workflow start/status patterns and input contracts.
- `cap-apps-manifest` - `manifest.json` mapping requirements and gotchas.
- `cap-apps-sql-query` - SqlClient raw SQL query patterns and response parsing.
- `cap-apps-performance` - Data query performance rules.

**Domo Everywhere (Embed)**
- `cap-de-programmatic-filters` - Server-side programmatic filtering and dataset switching for embedded Domo dashboards and cards.
- `cap-de-edit-embed` - Embedded edit experience via the Domo Identity Broker with JWT authentication and role-based access.
- `cap-de-jsapi-filters` - Client-side JS API filter methods for embedded Domo content.

**Connectors**
- `cap-connector-dev` - Connector IDE auth/data processing patterns (not for Domo app/card builds).

### Workflows (`wf-`)

- `wf-apps-migrate-lovable` - Convert SSR-heavy generated apps to Domo-compatible client apps.
- `wf-apps-migrate-googleai` - Convert AI Studio-origin projects to Domo static deploy contract.

## Repository Structure

```text
skills/<skill-name>/
└── SKILL.md

rules/
├── core-custom-apps-rule.md
└── custom-app-gotchas.md
```

## Rules Philosophy

- `rules/` contains only always-applicable, high-level guardrails.
- `skills/` contains specialized, task-scoped implementation guidance.

## Skills vs Rules

- **Skills** are installable modules (via `npx skills add ...`) and are invoked for specific tasks.
- **Rules** are always-on guidance files and are **not** installed by `skills` CLI.

### One-time rules setup

If you are non-technical, use this mental model:

- install **skills** with one command
- copy **rules** once
- after that, just chat with your agent normally

#### Cursor users (simple steps)

1. Open your app project in Cursor.
2. Make sure your project has a `.cursor/rules/` folder.
3. Copy both files from this repo's `rules/` folder into your project’s `.cursor/rules/`:
   - `core-custom-apps-rule.md`
   - `custom-app-gotchas.md`

#### Claude Code users (simple steps)

1. Open your app project.
2. Create a `rules/` folder in your project root (if it does not exist).
3. Copy both files from this repo's `rules/` folder into your project `rules/` folder:
   - `core-custom-apps-rule.md`
   - `custom-app-gotchas.md`

#### Cortex Code users (simple steps)

1. Open your app project.
2. Create a `rules/` folder in your project root (if it does not exist).
3. Copy both files from this repo's `rules/` folder into your project `rules/` folder:
   - `core-custom-apps-rule.md`
   - `custom-app-gotchas.md`

Skills can also be loaded directly by asking your agent to read the skill file, e.g.:
```text
Please read skills/pb-apps-initial-build/SKILL.md from stahura/domo-ai-vibe-rules and follow it.
```

#### Easiest option: ask your agent to do it for you

You can paste this directly to your agent:

```text
Please install this Domo package for me:
1) Install skills from stahura/domo-ai-vibe-rules using npx skills add.
2) Copy rules/core-custom-apps-rule.md and rules/custom-app-gotchas.md into my project rules location.
3) Verify files are in place and tell me done.
```

## Compatibility

This repo is tool-agnostic by design (Cursor, Claude Code, Cortex Code, and others).  
Unlike older setups, it does not rely on Cursor/Claude preamble files in the root.

## If `npx skills add` is blocked

Some corporate environments block `npx` or GitHub access.  
If that happens, ask your agent to manually copy the specific `skills/<name>/SKILL.md` files into your local skills directory.
