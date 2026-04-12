# Domo Skills — Comprehensive Update Plan

**Date:** 2026-04-12
**Context:** Produced after a failed manufacturing demo build exposed broken cross-references, CLI confusion, duplicate skills, and content gaps. This file is a complete work order for another agent to execute changes against the **source skill repo** before re-publishing.

---

## Table of Contents

1. [Background](#1-background)
2. [Part A — Fix all cross-references to use flat installed paths](#2-part-a--fix-all-cross-references-to-use-flat-installed-paths)
3. [Part B — Add two-CLI boundary rule to core-custom-apps-rule.md](#3-part-b--add-two-cli-boundary-rule)
4. [Part C — Update core-custom-apps-rule.md skill routing table](#4-part-c--update-skill-routing-table)
5. [Part D — Remove nested duplicate directories from installed skills](#5-part-d--remove-nested-duplicate-directories)
6. [Part E — Content fixes from manufacturing demo build](#6-part-e--content-fixes-from-manufacturing-demo-build)
7. [Verification checklist](#7-verification-checklist)

---

## 1. Background

### Two CLIs exist


| CLI                                           | Binary               | Purpose                                                                                                                                                                       |
| --------------------------------------------- | -------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Ryuu** (official Domo CLI, `@domoinc/ryuu`) | `domo`               | `domo login`, `domo dev`, `domo publish` — custom app lifecycle ONLY                                                                                                          |
| **Community CLI** (`community-domo-cli`)      | `community-domo-cli` | ALL Domo Product API operations — datasets, app-studio, cards, dataflows, appdb, code-engine, filesets, workflows, pages, users, pdp, domoapps, beast-modes, variables, files |


The model tried `domo datasets get-schema` (which doesn't exist) instead of `community-domo-cli datasets schema` because:

- The core rule only mentions the community CLI in a "CLI skills are optional" footnote
- The demo orchestrator skill says "fetch schema" without specifying which CLI
- The reference files that would have shown the correct CLI couldn't be read because their paths were wrong

### Flat vs nested path problem

Skills are organized in nested directories in the source repo (e.g., `skills/cli/community-cli-howto/`) but `npx skills add` installs them flat (e.g., `~/.agents/skills/community-cli-howto/`). Cross-references written as nested paths fail at runtime.

### Duplicate installations

Nearly every skill exists twice — a flat copy AND a nested copy under `~/.agents/skills/`. Many pairs have DIFFERENT content (the flat copy may be newer). The nested copies are stale remnants that should be removed.

---

## 2. Part A — Fix all cross-references to use flat installed paths

Every path referencing another skill must use the flat format: `~/.agents/skills/<skill-name>/...`

### A1. `app-studio-dataset-etl-gen-demo/SKILL.md` (14 broken refs)

These are the reference file paths in the "Read these helper scripts" section (lines 12-18):


| Line | Current (broken)                                                                                 | Replace with                                                                       |
| ---- | ------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------- |
| 12   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/cli_helpers.py`       | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/cli_helpers.py`       |
| 13   | `~/.agents/skills/app-studio/advanced-app-studio/references/card_templates.py`                   | `~/.agents/skills/advanced-app-studio/references/card_templates.py`                |
| 14   | `~/.agents/skills/app-studio/advanced-app-studio/references/layout_assembler.py`                 | `~/.agents/skills/advanced-app-studio/references/layout_assembler.py`              |
| 15   | `~/.agents/skills/themes/domo-app-theme/references/theme_transform.py`                           | `~/.agents/skills/domo-app-theme/references/theme_transform.py`                    |
| 16   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/theme_loader.py`      | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/theme_loader.py`      |
| 17   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/vertical_detector.py` | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/vertical_detector.py` |
| 18   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/errata.md`            | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/errata.md`            |


### A2. `app-studio-dataset-etl-gen-demo/references/vertical_detector.py` (5 broken refs)

Lines 38-42 contain path constants for vertical pack files:


| Line | Current (broken)                                                                                  | Replace with                                                                        |
| ---- | ------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 38   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/manufacturing.md`      | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/manufacturing.md`      |
| 39   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/retail-ecommerce.md`   | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/retail-ecommerce.md`   |
| 40   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/healthcare.md`         | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/healthcare.md`         |
| 41   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/logistics.md`          | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/logistics.md`          |
| 42   | `~/.agents/skills/(demo-skills)/app-studio-dataset-etl-gen-demo/references/financial-services.md` | `~/.agents/skills/app-studio-dataset-etl-gen-demo/references/financial-services.md` |


### A3. `appdb-collection-create/SKILL.md` (2 broken refs)


| Line | Current (broken)                    | Replace with                      |
| ---- | ----------------------------------- | --------------------------------- |
| 19   | `skills/custom-apps/appdb/SKILL.md` | `~/.agents/skills/appdb/SKILL.md` |
| 88   | `skills/custom-apps/appdb/SKILL.md` | `~/.agents/skills/appdb/SKILL.md` |


### A4. `code-engine/SKILL.md` (2 broken refs)


| Line | Current (broken)                         | Replace with                                   |
| ---- | ---------------------------------------- | ---------------------------------------------- |
| 13   | `skills/cli/code-engine-create/SKILL.md` | `~/.agents/skills/code-engine-create/SKILL.md` |
| 14   | `skills/cli/code-engine-update/SKILL.md` | `~/.agents/skills/code-engine-update/SKILL.md` |


### A5. `code-engine-create/SKILL.md` (1 broken ref)


| Line | Current (broken)                          | Replace with                            |
| ---- | ----------------------------------------- | --------------------------------------- |
| 19   | `skills/custom-apps/code-engine/SKILL.md` | `~/.agents/skills/code-engine/SKILL.md` |


### A6. `code-engine-update/SKILL.md` (1 broken ref)


| Line | Current (broken)                          | Replace with                            |
| ---- | ----------------------------------------- | --------------------------------------- |
| 19   | `skills/custom-apps/code-engine/SKILL.md` | `~/.agents/skills/code-engine/SKILL.md` |


### A7. `manifest/SKILL.md` (2 broken refs)


| Line | Current (broken)                         | Replace with                                   |
| ---- | ---------------------------------------- | ---------------------------------------------- |
| 14   | `skills/cli/code-engine-create/SKILL.md` | `~/.agents/skills/code-engine-create/SKILL.md` |
| 15   | `skills/cli/code-engine-update/SKILL.md` | `~/.agents/skills/code-engine-update/SKILL.md` |


### A8. `publish/SKILL.md` (2 broken refs)


| Line | Current (broken)                         | Replace with                                   |
| ---- | ---------------------------------------- | ---------------------------------------------- |
| 40   | `skills/cli/code-engine-create/SKILL.md` | `~/.agents/skills/code-engine-create/SKILL.md` |
| 41   | `skills/cli/code-engine-update/SKILL.md` | `~/.agents/skills/code-engine-update/SKILL.md` |


### A9. Backtick-style skill refs (correct format, just verify)

These use the format ``skill-name/SKILL.md`` which is ambiguous but works because the flat name matches. Found in:

- `advanced-app-studio/SKILL.md` — references `card-creation/SKILL.md` (5 occurrences)
- `app-studio/SKILL.md` — references `card-creation/SKILL.md` (5 occurrences)
- `basic-app-build/SKILL.md` — references `app-studio/SKILL.md`, `card-creation/SKILL.md`, `app-studio-pro-code/SKILL.md`
- `basic-app-studio/SKILL.md` — references `card-creation/SKILL.md` (2 occurrences)

**Action:** These are fine as-is (relative name matches flat layout). No changes needed.

---

## 3. Part B — Add two-CLI boundary rule

### File: `~/.claude/rules/core-custom-apps-rule.md`

**Add the following section BEFORE the existing "CLI skills are optional" section (before line 24).** This is the single highest-impact change — it prevents the model from ever using `domo` for API operations. REMOVE THE CLI SKILLS ARE OPTIONAL. MAKE IT REQUIRED. TELL THE USER THEY NEED THE COMMUNITY CLI FOR THESE SKILLS TO WORK

```markdown
## Two CLIs — know which to use
- **`domo` (official Domo CLI, `@domoinc/ryuu`)**: ONLY for `domo login`, `domo dev`, `domo publish`. It has NO dataset, card, app-studio, dataflow, or API commands.
- **`community-domo-cli`**: ALL Domo Product API operations — datasets, app-studio, cards, dataflows, appdb, code-engine, filesets, workflows, pages, beast-modes, variables, domoapps, files, users, pdp.
- If you need to fetch a dataset schema, create a card, list dataflows, or call any Domo API from the command line, the command ALWAYS starts with `community-domo-cli`, NEVER `domo`.
- Auth: run `domo login` once (creates ryuu session), then all `community-domo-cli` commands reuse that session via `DOMO_INSTANCE` and `DOMO_AUTH_MODE=ryuu-session` env vars.
```

### Also update the existing "CLI skills are optional" section

Change line 26 from:

```
- **Before using any `cli/` skill**, read `skills/cli/community-cli-howto/SKILL.md` first...
```

To:

```
- **Before using any CLI skill**, read `~/.agents/skills/community-cli-howto/SKILL.md` first for install, auth setup, supported commands, and troubleshooting.
```

---

## 4. Part C — Update skill routing table

### File: `~/.claude/rules/core-custom-apps-rule.md`

Replace lines 43-81 (the entire "Skill routing" section) with flat paths. Also update lines 30-32 ("App Studio vs custom apps") which reference nested category dirs.

**Replace lines 30-32 with:**

```markdown
## App Studio vs custom apps
- **Custom app skills** (`dataset-query`, `appdb`, `toolkit`, `manifest`, `publish`, etc.) — code that runs *inside* a Domo custom app card.
- **App Studio skills** (`basic-app-studio`, `advanced-app-studio`, `card-creation`, `beast-mode-creation`, `variable-creation`, `app-studio-pro-code`) — building and operating *App Studio* apps. Start with `basic-app-studio` for copy-paste CLI operations; use `advanced-app-studio` for the full layout/theme/reference material.
```

**Replace lines 43-81 with:**

```markdown
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
- Full end-to-end demo stack -> `~/.agents/skills/full-domo-stack/SKILL.md`
- Workspaces admin -> `~/.agents/skills/workspaces/SKILL.md`
```

---

## 5. Part D — Remove nested duplicate directories

After all cross-references are updated to flat paths, the nested directories under `~/.agents/skills/` are dead weight that can cause the model to read stale content. Delete these entire directories:

```
~/.agents/skills/apps/                        (contains: ai-service-layer, appdb, code-engine, da-cli, data-api, dataset-query, domo-js, manifest, migrate-googleai, migrate-lovable, performance, publish, sql-query, toolkit, workflow)
~/.agents/skills/cli/                         (contains: appdb-collection-create, code-engine-create, code-engine-update, community-cli-howto)
~/.agents/skills/visualization/               (contains: app-studio, app-studio-pro-code, beast-mode-creation, card-creation, variable-creation)
~/.agents/skills/themes/                      (contains: domo-app-theme)
~/.agents/skills/connectors/                  (contains: connector-dev, data-upload-java-cli, json-no-code-connector)
~/.agents/skills/domo-everywhere/             (contains: edit-embed, embed-portal, jsapi-filters, programmatic-filters)
~/.agents/skills/documents/                   (contains: html-deck)
~/.agents/skills/datagen/                     (contains: domo-data-generator)
~/.agents/skills/orchestrator-skills/         (contains: basic-app-build, basic-app-build-w-video, initial-build)
~/.agents/skills/administration/              (contains: workspaces)
~/.agents/skills/transformation/              (contains: magic-etl)
```

**IMPORTANT:** Before deleting, verify each flat copy exists and is the newer/correct version. For pairs marked DIFFERENT in the audit, the flat copy should be kept. Here's the full list of duplicate pairs and their status:


| Skill                   | Flat hash | Nested hash | Status                    |
| ----------------------- | --------- | ----------- | ------------------------- |
| ai-service-layer        | f59acff9  | 2cce500f    | DIFFERENT — keep flat     |
| app-studio              | 3bdd4646  | f68ed1f4    | DIFFERENT — keep flat     |
| app-studio-pro-code     | d1684c24  | b11b69a7    | DIFFERENT — keep flat     |
| appdb                   | 8432cece  | baa23a96    | DIFFERENT — keep flat     |
| appdb-collection-create | fbb1757f  | a2c14006    | DIFFERENT — keep flat     |
| basic-app-build         | 00050c39  | 233db94f    | DIFFERENT — keep flat     |
| basic-app-build-w-video | 1e54e0db  | 2c20e7f2    | DIFFERENT — keep flat     |
| beast-mode-creation     | 9613ad81  | f8cf40e4    | DIFFERENT — keep flat     |
| card-creation           | 5561ec47  | 21131aef    | DIFFERENT — keep flat     |
| code-engine             | 67820338  | a20e091d    | DIFFERENT — keep flat     |
| code-engine-create      | c0f8f816  | 71437d8a    | DIFFERENT — keep flat     |
| code-engine-update      | 29bd489a  | 034c6ca7    | DIFFERENT — keep flat     |
| community-cli-howto     | d441d2bb  | 5d3be572    | DIFFERENT — keep flat     |
| connector-dev           | c539f1fe  | c539f1fe    | IDENTICAL — delete nested |
| da-cli                  | 456a45bd  | 456a45bd    | IDENTICAL — delete nested |
| data-api                | 6ef545c2  | 61a6bac4    | DIFFERENT — keep flat     |
| data-upload-java-cli    | 89fc097f  | a87600c3    | DIFFERENT — keep flat     |
| dataset-query           | dfd2e251  | dfd2e251    | IDENTICAL — delete nested |
| domo-app-theme          | 34e25b29  | 58f79b3f    | DIFFERENT — keep flat     |
| domo-data-generator     | f73ba8b3  | df890049    | DIFFERENT — keep flat     |
| domo-js                 | b1e7dae9  | 99acfa00    | DIFFERENT — keep flat     |
| edit-embed              | 83f39ba7  | 83f39ba7    | IDENTICAL — delete nested |
| embed-portal            | 72ab7a8b  | 63187e64    | DIFFERENT — keep flat     |
| html-deck               | d0c07266  | 2ea6d092    | DIFFERENT — keep flat     |
| initial-build           | d7e84da4  | d7e84da4    | IDENTICAL — delete nested |
| jsapi-filters           | 3f0a1115  | 3f0a1115    | IDENTICAL — delete nested |
| json-no-code-connector  | 8f332003  | 956ab322    | DIFFERENT — keep flat     |
| magic-etl               | 0682ee6e  | 0682ee6e    | IDENTICAL — delete nested |
| manifest                | c8785dce  | 195497a3    | DIFFERENT — keep flat     |
| migrate-googleai        | 4e8258f2  | 4e8258f2    | IDENTICAL — delete nested |
| migrate-lovable         | 0b5010b4  | 0b5010b4    | IDENTICAL — delete nested |
| performance             | 529892fa  | 529892fa    | IDENTICAL — delete nested |
| programmatic-filters    | 7eccd538  | 7eccd538    | IDENTICAL — delete nested |
| publish                 | c59c8c60  | c59c8c60    | IDENTICAL — delete nested |
| sql-query               | bd0dc2db  | bd0dc2db    | IDENTICAL — delete nested |
| toolkit                 | 66f5c0ea  | 66f5c0ea    | IDENTICAL — delete nested |
| variable-creation       | cc24bba2  | 9ccae065    | DIFFERENT — keep flat     |
| workflow                | 88254a9a  | 6db3ca82    | DIFFERENT — keep flat     |
| workspaces              | cb567d38  | cdbd89d3    | DIFFERENT — keep flat     |


---

## 6. Part E — Content fixes from manufacturing demo build

These are bugs and gaps discovered during a real end-to-end demo build on 2026-04-12. Each fix is specific to one skill.

### E1. `magic-etl-cli/SKILL.md` — Document `PublishToVault` output action (CRITICAL)

**Problem:** The skill documents input actions (`LoadFromVault`), transforms (`MergeJoin`, `GroupBy`, etc.), but never documents the output action type. Without this, no programmatically created dataflow can produce output. The model guessed `SaveToVault` which failed with `DP-0069: Illegal action type`.

**Fix:** Add a `PublishToVault (Output Node)` section with the full JSON structure:

```json
{
  "type": "PublishToVault",
  "id": "PublishToVault-my-output",
  "name": "Output Dataset Name",
  "dependsOn": ["last-action-id"],
  "settings": {"preferredDatabaseEntityType": "DYNAMIC_TABLE"},
  "inputs": ["last-action-id"],
  "dataSource": {
    "guid": null,
    "type": "DataFlow",
    "name": "Output Dataset Name",
    "description": "",
    "cloudId": null
  },
  "versionChainType": "REPLACE",
  "schemaSource": "DATAFLOW",
  "partitioned": false,
  "tables": [{}]
}
```

Also add a valid action type list at the top of the "Action Types" section:

```
Valid types: LoadFromVault, PublishToVault, MergeJoin, GroupBy,
WindowAction, Filter, ExpressionEvaluator, SQL

NOT valid (will fail with DP-0069): SaveToVault, SelectValues, RenameColumns
```

### E2. `magic-etl-cli/SKILL.md` — Document `SelectValues` is invalid

**Problem:** `SelectValues` was guessed as an action type and failed. The skill doesn't provide a definitive list of valid vs invalid types.

**Fix:** Covered by the valid/invalid list in E1 above.

### E3. `domo-data-generator/SKILL.md` — Add `weighted_choice` YAML example

**Problem:** The skill lists `weighted_choice` as a generator option but never shows the correct YAML format. The model used a list-of-objects format that failed.

**Fix:** Add a concrete example in the Generator Column Options table or in a subsection:

```yaml
generator: weighted_choice
choices:
  "Tier 1": 0.40
  "Tier 2": 0.35
  "Tier 3": 0.25
```

### E4. `domo-data-generator/SKILL.md` — Entity pool requirement note

**Problem:** Running `datagen generate` before `datagen pool regenerate` fails even if the schema doesn't use `entity_ref` generators.

**Fix:** Add a note in the `generate` command section: "Requires entity pool. Run `datagen pool regenerate` first if not already done, even if your schema doesn't use `entity_ref` generators."

### E5. `domo-data-generator/SKILL.md` — Clarify auth model vs community CLI

**Problem:** This skill lists `DOMO_CLIENT_ID`, `DOMO_CLIENT_SECRET`, and `DOMO_DEVELOPER_TOKEN` as required env vars. The community CLI has deprecated token auth. When skills are chained, it's confusing which auth model is in play.

**Fix:** Add a note: "This tool uses the Domo public API with OAuth credentials for dataset upload — it does NOT use `community-domo-cli` or the ryuu session. The `DOMO_DEVELOPER_TOKEN` is used by the datagen tool's own HTTP calls, not by the community CLI."

### E6. `community-cli-howto/SKILL.md` — Note token auth is deprecated

**Problem:** The skill doesn't mention that `auth_mode: "token"` is no longer supported by the community CLI.

**Fix:** Add to the Auth setup section: "**Token auth (`auth_mode: token`) is deprecated.** The only supported auth mode is `ryuu-session`. If you see `Token auth mode is no longer supported`, re-run `domo login -i <instance>` and set `DOMO_AUTH_MODE=ryuu-session`."

### E7. Theme DESIGN.md files — Document UI import vs API format difference

**Problem:** The "Importable JSON" in theme DESIGN.md files uses a simplified format (`index`, string weights, `"22px"` sizes) intended for the App Studio UI import dialog. The programmatic API expects a different format (`id` like `"c1"`/`"f1"`, numeric weights, bare integer sizes, nested value objects). Every programmatic theme application hits this mismatch.

**Affects:** All theme files under `~/.agents/skills/domo-app-theme/references/themes/*.DESIGN.md`

**Fix for each DESIGN.md:** Add a warning block above or below Section 10 (Importable JSON):

```markdown
> **UI Import vs API format:** The JSON below is for the App Studio UI import dialog
> (Theme Editor -> Import). For programmatic updates via `community-domo-cli app-studio update`:
> - Colors: use `id` (e.g., `"c1"`) not `index`; value is `{"value": "#HEX", "type": "RGB_HEX"}` not a flat string; preserve the `tags` array
> - Fonts: use `id` (e.g., `"f1"`) not `index`; `weight` must be numeric (300/400/600/700) not string; `size` must be numeric (no "px"); `style` must be `"Regular"` not `"normal"`
> - Card styles: use `id` (e.g., `"ca1"`) not `index`; `dropShadow` valid values are `"NONE"`, `"SMALL"`, `"MEDIUM"`, `"LARGE"` (not boolean); `padding` is `{left:N, right:N, top:N, bottom:N}` not a single integer
> - **Do not replace** the entire colors/fonts/cards array — iterate existing entries and update `value` fields to preserve tags/metadata the UI import format omits.
```

### E8. `advanced-app-studio/SKILL.md` — Add API-compatible theme format notes

**Problem:** The Theme Management section doesn't explicitly document the color/font/card object formats the API expects.

**Fix:** In the Theme Management section, add:

```markdown
### API Color Object Format
{"id": "c1", "value": {"value": "#141008", "type": "RGB_HEX"}, "tags": ["THEME", "PRIMARY", "TINTED_GRAY"]}

### API Font Object Format
{"id": "f1", "family": "Sans", "weight": 600, "size": 22, "style": "Regular"}

### API Card Style Object Format
{"id": "ca1", "borderRadius": 0, "borderWidth": 0, "dropShadow": "NONE", "padding": {"left": 0, "right": 0, "top": 0, "bottom": 0}}

### Valid dropShadow values
"NONE", "SMALL", "MEDIUM", "LARGE"
```

### E9. `app-studio-dataset-etl-gen-demo/SKILL.md` — Add explicit CLI guidance at step 0

**Problem:** Step 0 says "Fetch schema/columns for the provided datasets first" but doesn't specify which CLI to use.

**Fix:** Change step 0 text to:

```markdown
0. **If user provides dataset IDs, detect vertical before pack selection**:
   - Fetch schema/columns using `community-domo-cli datasets schema <dataset_id>` for each provided dataset.
   - Match columns to a reference vertical using this map:
```

### E10. `app-studio-dataset-etl-gen-demo/SKILL.md` — Nav icons manual step

**Problem:** Step 10 says "Navigation: LEFT orientation, reorder pages, HOME first, showTitle false" as a build step without noting icons require manual UI work.

**Fix:** The current skill text already has "INFORM USER icons must be set manually in App Studio UI" — verify this is present. If missing, add: "Icons must be set manually in the App Studio UI after the programmatic build (hover page name in left nav -> click icon to change)."

---

## 7. Verification checklist

After all changes are applied, run this verification:

```bash
# 1. No nested path references remain in flat skills
grep -r "skills/\(cli\|custom-apps\|app-studio\|themes\|demo-skills\|(demo-skills)\|transformation\|visualization\|connectors\|domo-everywhere\|documents\|datagen\|orchestrator-skills\|administration\|apps\)/" ~/.agents/skills/*/SKILL.md ~/.agents/skills/*/references/*.py ~/.agents/skills/*/references/*.md 2>/dev/null

# 2. No nested duplicate directories remain
ls -d ~/.agents/skills/apps/ ~/.agents/skills/cli/ ~/.agents/skills/visualization/ ~/.agents/skills/themes/ ~/.agents/skills/connectors/ ~/.agents/skills/domo-everywhere/ ~/.agents/skills/documents/ ~/.agents/skills/datagen/ ~/.agents/skills/orchestrator-skills/ ~/.agents/skills/administration/ ~/.agents/skills/transformation/ 2>/dev/null
# Expected: all "No such file or directory"

# 3. All flat skills still have SKILL.md
for d in ~/.agents/skills/*/; do
  [ -f "$d/SKILL.md" ] || echo "MISSING: $d/SKILL.md"
done

# 4. Core rule routing table paths all resolve
grep '~/.agents/skills/' ~/.claude/rules/core-custom-apps-rule.md | sed 's/.*`\(.*\)`.*/\1/' | while read p; do
  eval test -f "$p" || echo "BROKEN: $p"
done

# 5. "domo datasets" or "domo appdb" etc. never appear as CLI commands in any skill
grep -rn '\bdomo \(datasets\?\|appdb\|app-studio\|cards\|pages\|filesets\?\|code-engine\|workflows\?\|dataflows\?\|beast-mode\|variables\?\|users\?\|pdp\|domoapps\|files\) ' ~/.agents/skills/*/SKILL.md 2>/dev/null
# Expected: no matches (only "community-domo-cli" should precede these subcommands)
# Note: "domo.get()", "domo.post()", "domo publish", "domo login", "domo dev" are fine — those are JS SDK or ryuu CLI
```

---

## Summary of scope


| Part | Files affected                          | Changes                          |
| ---- | --------------------------------------- | -------------------------------- |
| A    | 8 skill files                           | 29 path fixes (find-and-replace) |
| B    | 1 rule file                             | Add ~6 lines                     |
| C    | 1 rule file                             | Rewrite ~40 lines                |
| D    | 11 nested dirs                          | Delete after verification        |
| E    | 6 skill files + N theme DESIGN.md files | Content additions                |


**Execution order:** B and C first (core rule), then A (cross-refs), then E (content), then D (cleanup) last.