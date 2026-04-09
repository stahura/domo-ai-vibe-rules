# Domo Workspace API (Reverse-Engineered)

> **CLI vs API**: The Java CLI has no workspace commands. All workspace operations require the REST API via curl.

> **Status**: Undocumented / reverse-engineered as of March 2026
> **Base URL**: `https://<instance>.domo.com`
> **Auth**: `X-DOMO-Developer-Token` header

## Overview

Workspaces in Domo are organizational containers that group related content -- cards, pages, datasets, apps, and other assets -- into a single navigable collection. The Workspace API is **not publicly documented** by Domo. These endpoints were reverse-engineered from the Domo web client and verified through testing.

Supported operations:
- **Add** content (cards, pages, datasets) to a workspace
- **Remove** content from a workspace
- **List** all contents of a workspace
- **Search** within a workspace for specific content

---

## Endpoints

### 1. Add Content to Workspace (Recommended)

Adds a single content item to a workspace. This is the **confirmed working** endpoint.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/nav/v1/workspaces/:guid/contents` |
| **Content-Type** | `application/json` |

**Request Body**:

```json
{
  "entityId": "728638278",
  "entityType": "CARD"
}
```

**Response** (success):

```json
{
  "id": 6,
  "entityType": "CARD",
  "entityId": "728638278",
  "addedAt": "2026-03-04 16:37:52",
  "addedBy": 149955692
}
```

**Supported entityType values**: `CARD`, `PAGE`, `DATASET`, `DATA_APP`, `WORKSPACE_URL`

> **Verified**: This endpoint was tested by adding 22 cards to a workspace in March 2026. All 22 succeeded.

### 1b. Add Content to Workspace (Bulk - UNRELIABLE)

The bulk endpoint exists but returned **400 Bad Request** in testing across all format variations. **Use the single-item endpoint above instead.**

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/nav/v1/workspaces/bulk/execute` |
| **Content-Type** | `application/json` |

**Request Body** (documented but unreliable):

```json
{
  "operations": [
    {
      "operation": "ADD",
      "workspace": "99bf62b4-21f8-474b-985b-9bb83c773998",
      "contents": [
        {
          "id": "CARD_OR_CONTENT_ID",
          "type": "CARD"
        }
      ]
    }
  ]
}
```

> **WARNING**: This endpoint returned 400 errors in March 2026 testing regardless of `id`/`entityId` format, string/number types, or content type values (`CARD`, `card`, `KPI_CARD`). The single-item `/contents` endpoint is the reliable alternative.

---

### 2. Remove Content from Workspace

Removes content from a workspace without deleting it from Domo. Use the content's workspace-internal `id` (the numeric ID returned when adding, or from listing workspace contents), NOT the card/dataset ID.

| Field | Value |
|-------|-------|
| **Method** | `DELETE` |
| **Path** | `/nav/v1/workspaces/:guid/contents/:contentId` |

Where `:contentId` is the workspace-internal numeric ID (the `id` field from list/add responses).

**Alternative** (bulk endpoint - may be unreliable, see note on Section 1b):

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/nav/v1/workspaces/bulk/execute` |
| **Content-Type** | `application/json` |

```json
{
  "operations": [
    {
      "operation": "REMOVE",
      "workspace": "99bf62b4-21f8-474b-985b-9bb83c773998",
      "contents": [
        {
          "id": "CARD_OR_CONTENT_ID",
          "type": "CARD"
        }
      ]
    }
  ]
}
```

---

### 3. List Workspace Contents

Returns all content objects in a workspace with optional detail.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/nav/v1/workspaces/:guid/walk?includeDetails=true` |

**Path Parameters**:
- `:guid` -- The workspace GUID (e.g., `99bf62b4-21f8-474b-985b-9bb83c773998`)

**Query Parameters**:
- `includeDetails` (boolean) -- When `true`, returns full metadata for each content item

**Response structure**:

```json
{
  "current": null,
  "pins": [],
  "sorts": [],
  "folders": [],
  "contents": [
    {
      "id": 6,
      "entityType": "CARD",
      "entityId": "728638278",
      "addedAt": "2026-03-04 16:37:52",
      "addedBy": 149955692,
      "attributes": {
        "entityType": "card",
        "databaseId": "728638278",
        "winnerText": "Revenue by Department",
        ...
      }
    }
  ]
}
```

Key fields per content item:
- `id` -- Workspace-internal numeric ID (use for remove operations)
- `entityType` -- `CARD`, `DATA_APP`, `WORKSPACE_URL`, etc.
- `entityId` -- The Domo entity ID (card ID, dataset ID, etc.)
- `attributes.winnerText` -- The display name/title

### 3b. List All Workspaces

Returns all workspaces the authenticated user has access to.

| Field | Value |
|-------|-------|
| **Method** | `GET` |
| **Path** | `/nav/v1/workspaces` |

**Response structure**:

```json
{
  "results": [
    {
      "guid": "579394f2-5ec2-4152-b2b7-7e2c6c7a1305",
      "name": "Claude",
      "createdAt": "2026-03-04 16:31:32",
      "createdBy": 149955692,
      "icon": "ai",
      "iconColor": "#e4715d",
      "members": [...],
      "contents": [],
      "folders": []
    }
  ]
}
```

---

### 4. Search Workspace Contents

Searches within a workspace for content matching a query.

| Field | Value |
|-------|-------|
| **Method** | `POST` |
| **Path** | `/nav/v1/workspaces/:guid/addContentQuery` |
| **Content-Type** | `application/json` |

**Path Parameters**:
- `:guid` -- The workspace GUID

**Example**:

```
POST /nav/v1/workspaces/99bf62b4-21f8-474b-985b-9bb83c773998/addContentQuery
```

---

## Authentication

All requests require a Domo Developer Token passed as a header:

```
X-DOMO-Developer-Token: your_token_here
```

Generate a token from **Admin > Security > Access Tokens** in the Domo UI.

---

## Code Examples

### Python (requests)

```python
import requests

DOMO_BASE = "https://your-instance.domo.com/api"
TOKEN = "your_domo_developer_token"
WORKSPACE_GUID = "579394f2-5ec2-4152-b2b7-7e2c6c7a1305"

headers = {
    "X-DOMO-Developer-Token": TOKEN,
    "Content-Type": "application/json",
}


def add_card_to_workspace(card_id: str) -> dict:
    """Add a single card to the workspace (confirmed working)."""
    url = f"{DOMO_BASE}/nav/v1/workspaces/{WORKSPACE_GUID}/contents"
    body = {"entityId": card_id, "entityType": "CARD"}
    resp = requests.post(url, json=body, headers=headers)
    resp.raise_for_status()
    return resp.json()


def add_multiple_cards_to_workspace(card_ids: list[str]) -> list[dict]:
    """Add multiple cards one at a time."""
    results = []
    for card_id in card_ids:
        result = add_card_to_workspace(card_id)
        results.append(result)
    return results


def list_workspace_contents() -> dict:
    """List all contents of the workspace with details."""
    url = f"{DOMO_BASE}/nav/v1/workspaces/{WORKSPACE_GUID}/walk"
    params = {"includeDetails": "true"}
    resp = requests.get(url, params=params, headers=headers)
    resp.raise_for_status()
    return resp.json()


def list_all_workspaces() -> dict:
    """List all workspaces the user has access to."""
    url = f"{DOMO_BASE}/nav/v1/workspaces"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()


def search_workspace(query_body: dict) -> dict:
    """Search for content within the workspace."""
    url = f"{DOMO_BASE}/nav/v1/workspaces/{WORKSPACE_GUID}/addContentQuery"
    resp = requests.post(url, json=query_body, headers=headers)
    resp.raise_for_status()
    return resp.json()
```

### curl

**Add a card to the workspace** (confirmed working):

```bash
curl -X POST "https://your-instance.domo.com/api/nav/v1/workspaces/WORKSPACE_GUID/contents" \
  -H "X-DOMO-Developer-Token: $DOMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"entityId": "123456789", "entityType": "CARD"}'
```

**List all workspaces**:

```bash
curl -X GET "https://your-instance.domo.com/api/nav/v1/workspaces" \
  -H "X-DOMO-Developer-Token: $DOMO_TOKEN"
```

**List workspace contents**:

```bash
curl -X GET "https://your-instance.domo.com/api/nav/v1/workspaces/WORKSPACE_GUID/walk?includeDetails=true" \
  -H "X-DOMO-Developer-Token: $DOMO_TOKEN"
```

**Search workspace**:

```bash
curl -X POST "https://your-instance.domo.com/api/nav/v1/workspaces/WORKSPACE_GUID/addContentQuery" \
  -H "X-DOMO-Developer-Token: $DOMO_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## Gotchas and Known Issues

| Issue | Detail |
|-------|--------|
| **Bulk endpoint returns 400** | The `/nav/v1/workspaces/bulk/execute` endpoint returned 400 Bad Request in March 2026 testing across all format variations (`id`/`entityId`, string/number, `CARD`/`card`/`KPI_CARD`). **Use `/nav/v1/workspaces/:guid/contents` instead** — this is confirmed working. |
| **Use `/contents` not `/bulk/execute`** | The single-item `POST /nav/v1/workspaces/:guid/contents` endpoint with `{"entityId": "...", "entityType": "CARD"}` is the reliable way to add content. Verified with 22 cards in a single session. |
| **entityType values** | Confirmed from existing workspace data: `CARD`, `DATA_APP`, `WORKSPACE_URL`. Also documented: `PAGE`, `DATASET`. |
| **Undocumented API** | These endpoints are not in the official Domo API docs. They were reverse-engineered from the Domo web client and may change without notice. |
| **GUID format** | Workspace identifiers use UUID/GUID format (e.g., `579394f2-5ec2-4152-b2b7-7e2c6c7a1305`), not numeric IDs. |
| **Response has internal ID** | When you add content, the response includes an `id` field (e.g., `6`). This is the workspace-internal content ID, different from the card/dataset ID. Use this for remove operations. |
| **URL must include `/api` prefix** | The workspace endpoints use the `/api/nav/v1/...` path. Omitting `/api` returns 404. |
