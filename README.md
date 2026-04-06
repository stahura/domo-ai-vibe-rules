# Domo Agent Skills

> Unofficial community repository of Domo agent skills and rules.

A library of markdown-only Agent Skills and high-level rules for building Domo custom apps, embedding Domo content, and developing connectors. Made primarily for **Claude Code** users but compatible with other AI coding tools.

Skills follow the [Agent Skills open standard](https://code.claude.com/docs/en/skills) — see the Claude docs for full details on how skills work, frontmatter options, and advanced patterns.

## Installation

Skills install into `~/.claude/skills/` on your machine. This folder is hidden by default in Finder and most file browsers — if you can’t find it, ask your AI agent:

> Check that Domo skills are installed in ~/.claude/skills/ and list what’s there.

**Easiest way — tell your agent:**

> Install the Domo skills from https://github.com/stahura/domo-ai-vibe-rules/skills

**Or run it yourself:**

```bash
npx skills add https://github.com/stahura/domo-ai-vibe-rules/skills --all -g
```

The `-g` flag installs skills globally so they are available in every project. Leave it off to install only in your current directory — but you will need to re-install in each new project you start.

For new Domo app builds, ask your agent to start with the `basic-app-build` skill first — it sequences the other skills for you.

## Why This Organization

Domo is a broad platform — "data query" means something completely different when you're querying from a custom app vs. a Python script vs. an embedded dashboard. A flat list of skills becomes ambiguous fast, so skills are organized into **feature directories** with short, descriptive names.

### Feature directories

| Directory | Scope |
|-----------|-------|
| `apps/` | Domo App Platform custom apps |
| `domo-everywhere/` | Embedding Domo content in external applications |
| `connectors/` | Custom Connector IDE |
| `orchestrator-skills/` | End-to-end orchestration runbooks that reference other skills in order |
| `documents/` | Document and slide deck generation |
| `cli/` | Command-line tooling and lifecycle workflows |
| `themes/` | UI theme reference and design tokens |

More directories can be added as new skills are contributed.

### Orchestrator skills vs. skills

**Orchestrator skills** are end-to-end orchestration skills that reference sub-skills to perform many Domo operations in sequence (e.g. building an app from scratch). Regular skills are atomic — one API, one tool, one concept. Orchestrator skills compose them.

## Available Skills

### Orchestrator Skills (`skills/orchestrator-skills/`)

- `basic-app-build` — Kickoff sequence for new Domo app builds; routes to the right rules and skills in order.

### Apps (`skills/apps/`)

- `da-cli` — Recommended for advanced users using DA CLI; ask your agent to use this skill for advanced scaffolding, generation, and manifest instance workflows.
- `publish` — Build and publish flow (`npm run build`, `cd dist`, `domo publish`).
- `domo-js` — `ryuu.js` usage, navigation/events, and import safety.
- `dataset-query` — Detailed `@domoinc/query` syntax and constraints.
- `data-api` — High-level data-access routing skill; points to query skill.
- `toolkit` — `@domoinc/toolkit` client usage and response handling.
- `appdb` — Toolkit-first AppDB CRUD/query patterns.
- `ai-service-layer` — Toolkit-first AI client usage and parsing.
- `code-engine` — Code Engine function invocation patterns and contracts.
- `workflow` — Workflow start/status patterns and input contracts.
- `manifest` — `manifest.json` mapping requirements and gotchas.
- `sql-query` — SqlClient raw SQL query patterns and response parsing.
- `performance` — Data query performance rules.
- `migrate-lovable` — Convert SSR-heavy generated apps to Domo-compatible client apps.
- `migrate-googleai` — Convert AI Studio-origin projects to Domo static deploy contract.

### Domo Everywhere (`skills/domo-everywhere/`)

- `programmatic-filters` — Server-side programmatic filtering and dataset switching for embedded Domo dashboards and cards.
- `edit-embed` — Embedded edit experience via the Domo Identity Broker with JWT authentication and role-based access.
- `jsapi-filters` — Client-side JS API filter methods for embedded Domo content.
- `embed-portal` — Full external-user portal build: auth, user management, data isolation, and Domo embed integration.

### Documents (`skills/documents/`)

- `html-deck` — Build HTML slide decks from source content and convert to pixel-perfect PDF via Puppeteer.

### Connectors (`skills/connectors/`)

- `connector-dev` — Connector IDE auth/data processing patterns (not for Domo app/card builds). This skill needs to be called manually in order to apply correctly.  LLMs have a lot of knowledge in this area so they will try to do it themselves.  

### CLI (`skills/cli/`)

- `code-engine-create` — CLI-first Code Engine package creation and datatype contract mapping.
- `code-engine-update` — CLI-first Code Engine package update/version workflows and drift synchronization.
- `appdb-collection-create` — CLI-first AppDB collection creation workflow that includes required datastore provisioning.

### Themes (`skills/themes/`)

- `domo-app-theme` — Clean, professional dashboard theme with CSS custom properties, layout patterns, and typography for Domo custom apps.

## Repository Structure

```text
skills/
├── apps/
│   ├── appdb/SKILL.md
│   ├── dataset-query/SKILL.md
│   ├── domo-js/SKILL.md
│   └── ...
├── domo-everywhere/
│   ├── edit-embed/SKILL.md
│   ├── jsapi-filters/SKILL.md
│   ├── programmatic-filters/SKILL.md
│   └── embed-portal/SKILL.md
├── connectors/
│   └── connector-dev/SKILL.md
├── orchestrator-skills/
│   └── basic-app-build/SKILL.md
├── documents/
│   └── html-deck/SKILL.md
├── cli/
├── themes/
│   └── domo-app-theme/SKILL.md

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
3. Copy these files from this repo’s `rules/` folder into your project’s `.cursor/rules/`:
   - `core-custom-apps-rule.md`
   - `custom-app-gotchas.md`

#### Claude Code users (simple steps)

1. Open your app project.
2. Create a `rules/` folder in your project root (if it does not exist).
3. Copy these files from this repo's `rules/` folder into your project `rules/` folder:
   - `core-custom-apps-rule.md`
   - `custom-app-gotchas.md`

#### Easiest option: ask your agent to do it for you

You can paste this directly to your agent:

```text
Please install this Domo package for me:
1) Install skills from stahura/domo-ai-vibe-rules using npx skills add.
2) Copy rules/core-custom-apps-rule.md and rules/custom-app-gotchas.md into my project rules location.
3) Verify files are in place and tell me done.
```

## Compatibility

This repo is tool-agnostic by design (Cursor, Claude Code, and others).  
Unlike older setups, it does not rely on Cursor/Claude preamble files in the root.

## If `npx skills add` is blocked

Some corporate environments block `npx` or GitHub access.  
If that happens, ask your agent to manually copy the specific `skills/<name>/SKILL.md` files into your local skills directory.
