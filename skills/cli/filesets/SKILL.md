---
name: fileset-cli
description: Use community-domo-cli to create, discover, browse, upload, download, and query files in Domo FileSets from the command line. Use this whenever the user needs to interact with Domo FileSets via CLI or automation — including listing filesets, browsing file directories, pulling files locally, pushing binary files, or running AI queries over file content.
---

# Domo FileSets — CLI Commands

FileSets are Domo's managed file storage containers. Each fileset holds files organized in directory paths with metadata, access controls, and optional AI-powered search.

**Prerequisites:** Set up a profile once with `community-domo-cli config set-profile` — see the `community-cli-howto` skill for the full setup. After that, all commands below work without any extra flags.

## Command reference

### FileSets (containers)

|---------|-------------|
| `filesets search` | List/search filesets; filter by name |
| `filesets get <fileset_id>` | Fetch fileset metadata |
| `filesets create --name <name>` | Create a new fileset container |

### Files within a fileset

| Command | What it does |
|---------|-------------|
| `filesets files-search <fileset_id>` | List/search files; filter by name, directory, pagination |
| `filesets file-get <fileset_id> <file_id>` | Fetch a single file's metadata by UUID |
| `filesets file-get-by-path <fileset_id> --path <path>` | Fetch a file's metadata by its path |
| `filesets download <fileset_id> <file_id> --output <path>` | Download file bytes to a local path |
| `filesets upload <fileset_id> --file-path <path>` | Upload a binary file into a fileset directory |
| `filesets query <fileset_id> --query <text>` | AI semantic search over file content |

All IDs are UUIDs. Delete operations are intentionally excluded.

---

## FileSets (containers)

### Search / list filesets

```bash
# List all (sorted by most recently updated)
community-domo-cli filesets search

# Filter by name
community-domo-cli filesets search --name "Monthly Reports"

# Paginate
community-domo-cli filesets search --limit 25 --offset 25
```

Response includes an array of fileset objects:
```json
[
  {
    "id": "abc123-fileset-id",
    "name": "Monthly Reports",
    "description": "Automated PDF outputs",
    "created": "2024-01-15T10:00:00Z",
    "createdBy": 12345
  }
]
```

### Get a fileset

```bash
community-domo-cli filesets get abc123-fileset-id
```

### Create a fileset

```bash
community-domo-cli filesets create --name "Q1 Reports" --description "Quarterly output files"
```

Prompts for confirmation unless `--yes` is passed. Returns the new fileset object including its ID.

---

## Files within a fileset

### Browse / search files

This is the primary way to discover file IDs before downloading:

```bash
# List all files in a fileset
community-domo-cli filesets files-search abc123-fileset-id

# Browse a specific directory
community-domo-cli filesets files-search abc123-fileset-id \
  --directory-path /reports/2024

# List only direct children (non-recursive)
community-domo-cli filesets files-search abc123-fileset-id \
  --directory-path /reports --immediate-children

# Filter by filename
community-domo-cli filesets files-search abc123-fileset-id --name ".pdf"

# Paginate using the next token from a previous response
community-domo-cli filesets files-search abc123-fileset-id \
  --next-token <token-from-pageContext.next>
```

Response shape:
```json
{
  "files": [
    {
      "id": "xyz789-file-id",
      "path": "/reports/2024/march.pdf",
      "name": "march.pdf",
      "contentType": "application/pdf",
      "size": 204800,
      "created": "2024-03-01T08:00:00Z",
      "createdBy": 12345
    }
  ],
  "pageContext": {
    "next": "pagination-token-or-null",
    "offset": 0,
    "limit": 100,
    "total": 42
  }
}
```

### Get file metadata

```bash
# By UUID
community-domo-cli filesets file-get abc123-fileset-id xyz789-file-id

# By path (useful when you know the directory structure)
community-domo-cli filesets file-get-by-path abc123-fileset-id \
  --path /reports/2024/march.pdf
```

### Download a file

```bash
community-domo-cli filesets download abc123-fileset-id xyz789-file-id \
  --output ./downloads/march.pdf
```

Preview without writing:
```bash
community-domo-cli --dry-run filesets download abc123-fileset-id xyz789-file-id \
  --output ./march.pdf
```

### Upload a file

```bash
# Upload to root of fileset
community-domo-cli filesets upload abc123-fileset-id \
  --file-path ./report.xlsx

# Upload to a specific directory
community-domo-cli filesets upload abc123-fileset-id \
  --file-path ./report.xlsx \
  --directory-path /reports/2024
```

Always dry-run first on unfamiliar filesets:
```bash
community-domo-cli --dry-run filesets upload abc123-fileset-id \
  --file-path ./report.xlsx \
  --directory-path /reports/2024
```

Dry-run shows filename, byte size, and target directory without uploading. Prompts for confirmation on live runs unless `--yes` is passed.

### AI query (semantic search)

Requires the fileset to have `aiEnabled: true`. Runs a natural-language question against the file content:

```bash
community-domo-cli filesets query abc123-fileset-id \
  --query "What were the key revenue drivers last quarter?"

# Restrict to a directory and return more matches
community-domo-cli filesets query abc123-fileset-id \
  --query "Any mentions of churn risk?" \
  --directory-path /reports/2024 \
  --top-k 10
```

Response:
```json
{
  "matches": [
    {
      "id": "xyz789-file-id",
      "node": { "id": "...", "name": "q4-analysis.pdf", "path": "/reports/2024/q4-analysis.pdf" },
      "score": 0.89
    }
  ]
}
```

---

## Typical workflow: discover then download

```bash
# 1. Find the right fileset
community-domo-cli filesets search --name "Monthly Reports"

# 2. Browse its files
community-domo-cli filesets files-search abc123-fileset-id --directory-path /reports/2024

# 3. Download the file you want
community-domo-cli filesets download abc123-fileset-id xyz789-file-id \
  --output ./march.pdf
```

---

## Output formats

All commands support `--output-format` (default: `json`):

```bash
community-domo-cli --output-format yaml filesets search
community-domo-cli --output-format table filesets files-search abc123-fileset-id
```

---

## Building apps that use FileSets

For interacting with FileSets from within a Domo custom app (upload/download from the browser, AI query, etc.), see the `fileset-api` skill.
