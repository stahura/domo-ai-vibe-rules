---
name: community-domo-cli
description: Uses the community-domo-cli project correctly for Domo Product API operations. Use when the user asks to run this CLI, test endpoints, configure ryuu-session auth, or troubleshoot command failures in this repository.
---
# Community Domo CLI

## Purpose

Run and troubleshoot `community-domo-cli` commands in this repository with the current locked endpoint surface.

## Install and run

Recommended for users:

```bash
pipx install "git+https://github.com/stahura/community-domo-cli.git"
community-domo-cli --help
```

Contributor/testing path:

```bash
python3 -m pip install -e .
community-domo-cli --help

# alternate module invocation for local dev
python3 -m community_domo_cli --help
```

## Auth setup (Ryuu session)

Prereq — install the Domo CLI and log in once:

```bash
npm install -g ryuu
domo login -i modocorp.domo.com
```

Then set env vars before running commands:

```bash
export DOMO_INSTANCE=modocorp
export DOMO_AUTH_MODE=ryuu-session
community-domo-cli datasets list
```

- CLI reads the login file from `~/.config/configstore/ryuu/<instance>.json`
- It reuses refresh/session behavior from `domo login`

## Important implementation constraints

- Product API base is `https://<instance>.domo.com/api` (the CLI already handles `/api`).
- No delete operations are supported.
- No `raw` passthrough command exists.
- Use `--dry-run` first for mutating operations when validating payloads.

## Supported command surface (current)

### datasets

- `datasets list`
- `datasets schema <dataset_id>`
- `datasets sql <dataset_id> --body/--body-file`

### appdb

- `appdb collections`
- `appdb collection-get <collection_id>`
- `appdb document-create <collection_id> --body/--body-file`

### code-engine

- `code-engine get-package <package_id>`
- `code-engine create-package --body/--body-file`
- `code-engine update-version <package_id> <version> --body/--body-file`

### workflows

- `workflows get <workflow_id>`

### filesets

- `filesets get <fileset_id>`
- `filesets file-get <fileset_id> <file_id>`
- `filesets upload <fileset_id> --body/--body-file`
- `filesets download <fileset_id> <file_id> --output <path>`

## Troubleshooting checklist

1. Confirm invocation style:
   - Prefer `community-domo-cli ...`
   - `python3 -m community_domo_cli ...` is mainly for local contributor testing
   - Do not run `python3 community_domo_cli ...`
2. Confirm auth inputs:
   - `DOMO_INSTANCE` and `DOMO_AUTH_MODE=ryuu-session` are set
   - `domo login` has been run successfully for the target instance
3. Confirm identifier type:
   - dataset UUID for datasets commands
   - fileset UUID and file UUID for filesets commands
4. For 400/404 issues, retry a known-good GET first:
   - `datasets list`
   - `appdb collections`
5. For mutating calls, validate payload with `--dry-run` before real execution.

## Response style for this project

- Be terse and concrete.
- Provide exact commands, not high-level instructions.
- Prefer giving a direct fix command first, then brief explanation.
