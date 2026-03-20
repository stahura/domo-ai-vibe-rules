# Domo Agent Skills

> Unofficial community repository of Domo App Platform agent skills and rules.

A library of markdown-only Agent Skills and high-level rules for building Domo App Platform custom apps.  
The structure is modeled after Google’s `stitch-skills` repository style: skill catalog at the root, one entrypoint file per skill, and simple install/discovery guidance.

## Installation & Discovery

Install skills from a GitHub repository with the `skills` CLI:

```bash
# List skills in this repository
npx skills add stahura/domo-ai-vibe-rules --list

# Install one skill globally
npx skills add stahura/domo-ai-vibe-rules --skill domo-js --global
```

## Available Skills

- `domo-da-cli` - Advanced DA CLI scaffolding, generation, and manifest instance workflows.
- `domo-app-publish` - Build and publish flow (`npm run build`, `cd dist`, `domo publish`).
- `domo-js` - `ryuu.js` usage, navigation/events, and import safety.
- `domo-dataset-query` - Detailed `@domoinc/query` syntax and constraints.
- `domo-data-api` - High-level data-access routing skill; points to query skill.
- `domo-toolkit-wrapper` - `@domoinc/toolkit` client usage and response handling.
- `domo-appdb` - Toolkit-first AppDB CRUD/query patterns.
- `domo-ai-service-layer` - Toolkit-first AI client usage and parsing.
- `domo-code-engine` - Code Engine function invocation patterns and contracts.
- `domo-workflow` - Workflow start/status patterns and input contracts.
- `domo-manifest` - `manifest.json` mapping requirements and gotchas.
- `domo-performance-optimizations` - Data query performance rules.
- `migrating-lovable-to-domo` - Convert SSR-heavy generated apps to Domo-compatible client apps.
- `migrating-googleai-to-domo` - Convert AI Studio-origin projects to Domo static deploy contract.
- `domo-custom-connector-ide` - Connector IDE auth/data processing patterns.

## Repository Structure

```text
skills/<skill-name>/
└── SKILL.md

rules/
├── core-platform-rule.md
└── domo-gotchas.md
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
   - `core-platform-rule.md`
   - `domo-gotchas.md`

#### Claude Code users (simple steps)
1. Open your app project.
2. Create a `rules/` folder in your project root (if it does not exist).
3. Copy both files from this repo's `rules/` folder into your project `rules/` folder:
   - `core-platform-rule.md`
   - `domo-gotchas.md`

#### Easiest option: ask your agent to do it for you

You can paste this directly to your agent:

```text
Please install this Domo package for me:
1) Install skills from stahura/domo-ai-vibe-rules using npx skills add.
2) Copy rules/core-platform-rule.md and rules/domo-gotchas.md into my project rules location.
3) Verify files are in place and tell me done.
```

## Compatibility

This repo is tool-agnostic by design (Cursor, Claude Code, and others).  
Unlike older setups, it does not rely on Cursor/Claude preamble files in the root.

## If `npx skills add` is blocked

Some corporate environments block `npx` or GitHub access.  
If that happens, ask your agent to manually copy the specific `skills/<name>/SKILL.md` files into your local skills directory.