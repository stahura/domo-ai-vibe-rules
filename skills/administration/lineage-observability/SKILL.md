---
name: lineage-observability
description: "Answer questions about the lineage, usage, and health of Domo content. Use when asked about upstream/downstream dataset lineage, unused or stale content, card/page view history, dataset health, dataflow dependencies, workflow dataset usage, or provisioning credentials for Domo Everywhere child instances. Works against any Domo instance using only standard APIs and a single dev token."
---

# Domo Lineage & Observability Skill

Answer questions about the lineage, usage, and health of Domo content — datasets, dataflows, cards, pages, apps, and workflows. Works against any Domo instance using only standard APIs.

---

## Quick Decision Guide

Before writing any code, orient using this:

**What credentials do I have?**
- Dev token only → use `{BASE}/...` internal endpoints with `X-DOMO-Developer-Token` header
- OAuth client_id + secret → also use `https://api.domo.com/...` public endpoints
- Neither → see "Sub-Instance Bootstrap" to provision credentials

**What is the user asking?**

| Question type | Go to |
|---|---|
| Dataset health / freshness / schedule | Datasets + Streams sections |
| What cards/flows use this dataset? | Card→Dataset Mapping + Lineage Questions |
| What's upstream/downstream of a dataset? | Lineage Questions |
| Which content is unused / stale? | Usage & Activity section |
| Who viewed what and when? | User Audits API (no DomoStats needed) |
| What workflows touch this dataset? | Workflows section |
| Set up a new instance / sub-instance | Sub-Instance Bootstrap section |

**Do I need DomoStats?**
No — `GET /audit/v1/user-audits` covers virtually all usage questions without it. DomoStats adds SQL flexibility and deeper history if available. Check for it by scanning dataset names for "activity log" or "domostats". If found, note the dataset ID.

---

## Configuration

```python
import os, requests, json
from datetime import datetime, timedelta
from collections import defaultdict

INSTANCE      = os.environ["DOMO_INSTANCE"]        # e.g. "modocorp" (no .domo.com)
DEV_TOKEN     = os.environ["DOMO_DEVELOPER_TOKEN"]  # "DDCI..." string
CLIENT_ID     = os.environ["DOMO_CLIENT_ID"]        # UUID
CLIENT_SECRET = os.environ["DOMO_CLIENT_SECRET"]    # hex string

BASE = f"https://{INSTANCE}.domo.com/api"
H    = {"X-DOMO-Developer-Token": DEV_TOKEN, "Content-Type": "application/json"}

def get_oauth_token():
    r = requests.get("https://api.domo.com/oauth/token",
        params={"grant_type": "client_credentials", "scope": "data user audit dashboard"},
        auth=(CLIENT_ID, CLIENT_SECRET), timeout=15)
    return r.json()["access_token"]

# OAuth header — needed for public api.domo.com endpoints and DomoStats SQL queries
PH = {"Authorization": f"Bearer {get_oauth_token()}", "Content-Type": "application/json"}
```

Run all queries as inline python3 via bash. Never hardcode credentials.

---

## Sub-Instance Bootstrap (Domo Everywhere)

Domo Everywhere child instances are independent Domo instances with their own URLs (e.g. `child.domo.com`). **All APIs documented here work identically against child instances** — just change `INSTANCE`. There is no parent-level management API; each instance is addressed directly.

**Credential requirements:** One dev token per instance, created once by a human in the UI (Admin > Security > Access Tokens). From that single token, everything else can be provisioned via API.

### Step 1 — Create OAuth client credentials (client_id + secret)

```
GET    {BASE}/identity/v1/developer-tokens      — list existing credentials
POST   {BASE}/identity/v1/developer-tokens      — create new (returns 201)
DELETE {BASE}/identity/v1/developer-tokens/{id} — revoke (returns 204)
```

Auth: **dev token only** — OAuth bearer returns 401 on this endpoint.

```python
r = requests.post(f"https://{instance}.domo.com/api/identity/v1/developer-tokens",
    headers={"X-DOMO-Developer-Token": bootstrap_dev_token, "Content-Type": "application/json"},
    json={
        "name": "automation",
        "description": "Auto-provisioned",
        "scopes": ["data", "dashboard", "user", "audit", "workflow"]
    }, timeout=10)
creds = r.json()
client_id     = creds["clientId"]      # UUID
client_secret = creds["clientSecret"]  # only returned on creation — store immediately
cred_id       = creds["id"]            # numeric, for DELETE
```

Valid scopes: `account`, `audit`, `buzz`, `cards`, `data`, `dashboard`, `user`, `workflow`
Do NOT include `userId` — causes 400.

### Step 2 — Create additional dev tokens (optional)

```
GET    {BASE}/data/v1/accesstokens      — list tokens (values not returned)
POST   {BASE}/data/v1/accesstokens      — create token (value only returned here)
DELETE {BASE}/data/v1/accesstokens/{id} — revoke
```

```python
import time
r = requests.post(f"https://{instance}.domo.com/api/data/v1/accesstokens", headers=H,
    json={
        "name": "automation-token",
        "ownerId": 12345678,   # user ID on the target instance
        "expires": int(time.time() * 1000) + (365 * 86400 * 1000)  # 1 year
    }, timeout=15)
result = r.json()
dev_token = result["token"]  # "DDCI..." — only time it's visible
token_id  = result["id"]     # for DELETE
```

### Full bootstrap sequence

```python
# One-time: human creates bootstrap_dev_token in the UI. Then:

# 1. Create OAuth credentials
H_boot = {"X-DOMO-Developer-Token": bootstrap_dev_token, "Content-Type": "application/json"}
creds = requests.post(f"https://{instance}.domo.com/api/identity/v1/developer-tokens",
    headers=H_boot,
    json={"name": "automation", "description": "auto", "scopes": ["data","dashboard","user","audit","workflow"]},
    timeout=10).json()

client_id, client_secret = creds["clientId"], creds["clientSecret"]

# 2. Get OAuth bearer token (reuse until expiry, then refresh)
oauth = requests.get("https://api.domo.com/oauth/token",
    params={"grant_type": "client_credentials", "scope": "data user audit dashboard"},
    auth=(client_id, client_secret), timeout=15).json()["access_token"]

# 3. Use OAuth bearer for all subsequent calls
```

---

## Datasets

```
GET {BASE}/data/v3/datasources?limit=50&offset=0
```

Returns `{dataSources: [...], _metaData: {totalCount}}`. Max 50 per page — always paginate.

**Key fields:**

| Field | Meaning |
|---|---|
| `id` | Dataset UUID |
| `name` | Dataset name |
| `owner.name` | Owner display name |
| `displayType` | Connector label (salesforce, hubspot, api, dataflow, etc.) |
| `cardInfo.cardCount` | Cards directly built on this dataset |
| `cardInfo.cardViewCount` | Lifetime total card views (0 = nobody looks at it) |
| `lastUpdated` | ms epoch — last successful data load |
| `nextUpdate` | ms epoch — next scheduled update (null if unscheduled) |
| `scheduleActive` | Whether refresh schedule is active |
| `status` | `SUCCESS`, `ERROR`, `INVALID`, etc. |
| `rowCount` | Current row count |
| `streamId` | Present if connector-based — use to fetch schedule/execution detail |

**Full impact counts** (detail endpoint only):
```
GET {BASE}/data/v3/datasources/{datasetId}?includeAllDetails=true
```

| Field | Meaning |
|---|---|
| `cardCount` | Direct cards |
| `impactCardCount` | **Total cards downstream through all dataflows** — best "importance" signal |
| `dataFlowCount` | Direct dataflow consumers |
| `impactDataFlowCount` | Total downstream dataflows |
| `dataSourceCount` | Datasets directly depending on this one |
| `impactDataSourceCount` | Total downstream datasets |
| `alertCount` / `impactAlertCount` | Alerts direct / downstream |

```python
# Composite impact scores
direct_impact = alertCount + cardCount + dataSourceCount + dataFlowCount
total_impact  = impactDataSourceCount + impactDataFlowCount + impactAlertCount + impactCardCount
```

**Paginate all datasets:**
```python
datasets, offset = [], 0
while True:
    data = requests.get(f"{BASE}/data/v3/datasources", headers=H,
                        params={"limit": 50, "offset": offset}, timeout=30).json()
    batch = data.get("dataSources", [])
    if not batch: break
    datasets.extend(batch)
    if len(batch) < 50: break
    offset += 50
```

---

## Streams — Schedule & Execution Health

When a dataset has a `streamId`, fetch full schedule and execution detail:
```
GET {BASE}/data/v1/streams/{streamId}?fields=all
```

| Field | Meaning |
|---|---|
| `scheduleExpression` | Cron expression |
| `advancedScheduleJson` | Human-readable schedule |
| `updateMethod` | `REPLACE` or `APPEND` |
| `scheduleState` | `ACTIVE`, `INACTIVE`, etc. |
| `inactiveScheduleCode` | Why it's inactive (null if active) |
| `lastExecution.currentState` | `SUCCESS`, `FAILED`, etc. |
| `lastExecution.endedAt` | Unix ms timestamp of last run |
| `lastSuccessfulExecution.endedAt` | Last *successful* run — compare to spot stuck failures |
| `currentExecution` | Non-null if a run is in progress |

---

## Dataflows — Lineage Graph

The only universal source of dataset-to-dataset lineage. No dedicated lineage API exists — build the graph from this.

```
GET {BASE}/dataprocessing/v1/dataflows?limit=50&offset=0
```

Paginate until batch size < 50.

| Field | Meaning |
|---|---|
| `id` | Integer flow ID |
| `name` | Flow name |
| `inputs[].dataSourceId` | UUID of each upstream dataset |
| `inputs[].dataSourceName` | Name of each upstream dataset |
| `outputs[].dataSourceId` | UUID of each output/downstream dataset |
| `magic` / `databaseType` | `MAGIC` = MagicETL, `ADR`/`SQL` = SQL-based |
| `enabled` / `paused` / `deleted` | Health flags |
| `lastExecution` | Last run metadata |

**Paginate all dataflows:**
```python
flows, offset = [], 0
while True:
    batch = requests.get(f"{BASE}/dataprocessing/v1/dataflows", headers=H,
                         params={"limit": 50, "offset": offset}, timeout=30).json()
    if not batch: break
    flows.extend(batch)
    if len(batch) < 50: break
    offset += 50
```

---

## Workflows — Agentic Automation

Domo Workflows are separate from dataflows. They contain agentic/automation steps that can read from and write to datasets.

```
GET {BASE}/workflow/v1/models?limit=50       — list all workflows
GET {BASE}/workflow/v1/models/{id}/versions  — all versions (each has savedJson)
```

The `savedJson` field on each version contains the full step graph. Parse it to find dataset references.

**Two confirmed patterns — both use UUID dataset IDs (exact match, not names):**

Pattern 1 — write/truncate steps (`Append To Dataset`, `Truncate Dataset`, `Query With SQL`):
```json
"input": [{"paramName": "dataset", "value": "8431aeb7-490a-4245-98f4-dc01e5d5c67d"}]
```

Pattern 2 — query steps (`Query Dataset`, `Get User Information`):
```json
"dataset": {"dataType": "dataset", "value": "d4ab01e0-178b-46c3-ac5f-845c0b1ab93f"}
```

**Find all datasets used across all workflows:**
```python
def extract_workflow_datasets(models):
    workflow_datasets = {}
    for m in models:
        rv = requests.get(BASE + f"/workflow/v1/models/{m['id']}/versions", headers=H, timeout=10)
        latest = sorted(rv.json(), key=lambda v: v["version"])[-1]
        saved = json.loads(latest.get("savedJson", "{}"))
        ds_ids = set()
        for el in saved.get("designElements", []):
            el_data = el.get("data", {})
            for inp in el_data.get("input", []):
                v = inp.get("value")
                if inp.get("paramName") == "dataset" and isinstance(v, str) and len(v) == 36:
                    ds_ids.add(v)
            ds_field = el_data.get("dataset")
            if isinstance(ds_field, dict):
                v = ds_field.get("value")
                if isinstance(v, str) and len(v) == 36:
                    ds_ids.add(v)
        if ds_ids:
            workflow_datasets[m["name"]] = list(ds_ids)
    return workflow_datasets
```

---

## Card → Dataset Mapping

### Single card or batch
```
GET {BASE}/content/v1/cards?urns={cardId}&parts=datasources
```
`parts=datasources` is mandatory — omitting it returns no datasource info. Comma-separate urns for batch: `?urns=123,456,789&parts=datasources`.

```python
r = requests.get(f"{BASE}/content/v1/cards", headers=H,
                 params={"urns": card_id, "parts": "datasources"}, timeout=15)
for ds in r.json()[0].get("datasources", []):
    print(f"{ds['dataSourceId']} — {ds['dataSourceName']}")
```

### Full page bulk fetch (preferred for dashboards)
```
GET {BASE}/content/v3/stacks/{pageId}/cards?parts=metadata,datasources
```

```python
r = requests.get(f"{BASE}/content/v3/stacks/{page_id}/cards", headers=H,
                 params={"parts": "metadata,datasources"}, timeout=15)
for card in r.json().get("cards", []):
    ds_ids = [ds["dataSourceId"] for ds in card.get("datasources", [])]
    print(f"Card {card['id']} ({card.get('title','?')[:40]}): {ds_ids}")
```

---

## Usage & Activity

### User Audits API — primary usage source (no DomoStats needed)

```
GET {BASE}/audit/v1/user-audits
```

Supports real server-side filtering by object type, event type, and epoch ms date range. Auth: dev token. Paginate with `offset`.

**Parameters:**

| Param | Notes |
|---|---|
| `objectType` | See table below — filters server-side |
| `eventType` | See table below — filters server-side |
| `start` / `end` | Epoch ms date range |
| `offset` / `limit` | Pagination (limit up to 200) |

**Response fields:** `userName`, `userId`, `userType`, `actionType`, `objectName`, `objectId`, `objectType`, `time` (epoch ms int)

**Confirmed objectType + eventType combinations:**

| objectType | eventType | What it tracks |
|---|---|---|
| `CARD` | `VIEWED` | Card views (includes AI chat card views) |
| `PAGE` | `VIEWED` | Dashboard/page views |
| `DATA_SOURCE` | `VIEWED` | Dataset views |
| `USER` | `LOGGEDIN` | Standard logins (also returns `PROXY_LOGGEDIN` — admin impersonation) |
| `USER` | `LOGGEDIN_SSO` | SSO logins |
| `BEAST_MODE_FORMULA` | *(omit)* | Beast mode create/update/rename events |
| `CODEENGINE_PACKAGE` | `VIEWED` | Code engine package usage |

Omitting `eventType` returns all event types for that `objectType`.

**Paginate all card views in last 30 days:**
```python
end_ms   = int(datetime.now().timestamp() * 1000)
start_ms = int((datetime.now() - timedelta(days=30)).timestamp() * 1000)

all_events, offset = [], 0
while True:
    batch = requests.get(f"{BASE}/audit/v1/user-audits", headers=H,
        params={"objectType": "CARD", "eventType": "VIEWED",
                "start": start_ms, "end": end_ms,
                "offset": offset, "limit": 200}, timeout=15).json()
    if not batch: break
    all_events.extend(batch)
    if len(batch) < 200: break
    offset += len(batch)

# Aggregate by card
card_stats = defaultdict(lambda: {"views": 0, "last_viewed": 0, "name": ""})
for e in all_events:
    s = card_stats[e["objectId"]]
    s["views"] += 1
    s["name"] = e["objectName"]
    if e["time"] > s["last_viewed"]:
        s["last_viewed"] = e["time"]
```

### DomoStats Activity Log — optional, adds SQL flexibility

If available (scan dataset names for "activity log" or "domostats"), query via OAuth:
```
POST https://api.domo.com/v1/datasets/query/execute/{datasetId}
Body: {"sql": "SELECT ..."}
```

**Key columns:** `Object_ID`, `Object_Name`, `Object_Type`, `Action`, `Event_Time` (ISO string), `Display Name`, `User ID`, `Device`

**SQL dialect rules (confirmed quirks):**
- Do NOT double-quote column names — causes silent 400 failures when combined with date filters and GROUP BY
- `CURRENT_DATE` / `NOW()` do not compare reliably against DATETIME columns — compute the cutoff in Python and inject as a string literal
- Single-quoted string values are fine

```python
cutoff = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')

# Cards viewed recently
sql1 = ("SELECT Object_ID FROM table"
        " WHERE Action = 'VIEWED' AND Object_Type = 'CARD' AND Event_Time >= '" + cutoff + "'"
        " GROUP BY Object_ID")
recently_viewed = set(row[0] for row in
    requests.post(f"https://api.domo.com/v1/datasets/query/execute/{ds_id}",
        headers=PH, json={"sql": sql1}, timeout=30).json().get("rows", []))

# All cards with last view date
sql2 = ("SELECT Object_ID, Object_Name, MAX(Event_Time) as last_viewed, COUNT(*) as view_count"
        " FROM table WHERE Action = 'VIEWED' AND Object_Type = 'CARD'"
        " GROUP BY Object_ID, Object_Name ORDER BY last_viewed ASC")
all_cards = requests.post(f"https://api.domo.com/v1/datasets/query/execute/{ds_id}",
    headers=PH, json={"sql": sql2}, timeout=60).json().get("rows", [])

stale = [row for row in all_cards if row[0] not in recently_viewed]
```

Other confirmed `Action`/`Object_Type` combos in DomoStats: `VIEWED/PAGE`, `VIEWED/DATA_SOURCE`, `VIEWED/DATA_LINEAGE`, `CREATED/CARD`, `UPDATED/CARD`, `DELETED/CARD`, `FAVORITED/CARD`, `DUPLICATED/CARD`, `VIEWED_EMBEDDED/PAGE`, `MANUALLY_RAN/DATAFLOW_TYPE`

---

## Pages & Apps

**List pages:**
```
GET {BASE}/content/v1/pages?limit=50&offset=0
```
Fields: `id`, `title`, `type`, `owner`, `owners`, `locked`, `children`

**Cards on a page (OAuth — includes cardIds):**
```
GET https://api.domo.com/v1/pages/{pageId}   (Authorization: Bearer {oauth_token})
```
Returns `cardIds[]` — the reliable way to get which cards live on a page.

**List App Studio apps:**
```
GET {BASE}/content/v1/dataapps?limit=50&offset=0
GET {BASE}/content/v1/dataapps/{appId}?includeHiddenViews=true
```
Fields: `dataAppId`, `title`, `views[]`, `owners`, `theme`, `lastUpdated`, `enabled`

---

## Answering Lineage Questions

### "What feeds dataset X?" (upstream)

```python
for flow in flows:
    if any(o["dataSourceId"] == TARGET for o in flow.get("outputs", [])):
        print(f"Dataflow: {flow['name']} (id={flow['id']})")
        for inp in flow.get("inputs", []):
            print(f"  ← {inp['dataSourceName']} ({inp['dataSourceId']})")
```

### "What does dataset X feed?" (downstream — dataflows + workflows)

```python
# Dataflows
for flow in flows:
    if any(i["dataSourceId"] == TARGET for i in flow.get("inputs", [])):
        print(f"Dataflow: {flow['name']}")
        for out in flow.get("outputs", []):
            print(f"  → {out['dataSourceName']} ({out['dataSourceId']})")

# Workflows
wf_datasets = extract_workflow_datasets(models)  # see Workflows section
for wf_name, ds_ids in wf_datasets.items():
    if TARGET in ds_ids:
        print(f"Workflow: {wf_name}")
```

### "Walk the full lineage chain" (multi-hop)

```python
upstream = {}
downstream = {}

for flow in flows:
    for inp in flow.get("inputs", []):
        for out in flow.get("outputs", []):
            downstream.setdefault(inp["dataSourceId"], []).append(
                {"to_ds": out["dataSourceName"], "to_id": out["dataSourceId"], "flow": flow["name"]})
            upstream.setdefault(out["dataSourceId"], []).append(
                {"from_ds": inp["dataSourceName"], "from_id": inp["dataSourceId"], "flow": flow["name"]})

def trace_up(ds_id, depth=0, seen=None):
    seen = seen or set()
    if ds_id in seen: return
    seen.add(ds_id)
    for link in upstream.get(ds_id, []):
        print("  " * depth + f"← {link['from_ds']}  [via {link['flow']}]")
        trace_up(link["from_id"], depth + 1, seen)

def trace_down(ds_id, depth=0, seen=None):
    seen = seen or set()
    if ds_id in seen: return
    seen.add(ds_id)
    for link in downstream.get(ds_id, []):
        print("  " * depth + f"→ {link['to_ds']}  [via {link['flow']}]")
        trace_down(link["to_id"], depth + 1, seen)
```

### "Is dataset X healthy / fresh?"

```python
ds = requests.get(f"{BASE}/data/v3/datasources/DATASET-UUID",
                  headers=H, params={"includeAllDetails": "true"}, timeout=15).json()

last_updated = datetime.fromtimestamp(ds["lastUpdated"] / 1000)
days_stale   = (datetime.now() - last_updated).days

print(f"Status:             {ds['status']}")
print(f"Last updated:       {last_updated.date()} ({days_stale}d ago)")
print(f"Rows:               {ds['rowCount']:,}")
print(f"Direct cards:       {ds.get('cardCount', ds['cardInfo']['cardCount'])}")
print(f"Impact cards:       {ds.get('impactCardCount', '?')}  ← full downstream chain")
print(f"Direct dataflows:   {ds.get('dataFlowCount', '?')}")

stream_id = ds.get("streamId")
if stream_id:
    stream = requests.get(f"{BASE}/data/v1/streams/{stream_id}",
                          headers=H, params={"fields": "all"}, timeout=15).json()
    le  = stream.get("lastExecution", {})
    lse = stream.get("lastSuccessfulExecution", {})
    print(f"Schedule:           {stream.get('advancedScheduleJson')} ({stream.get('scheduleState')})")
    print(f"Last run:           {le.get('currentState')} at {datetime.fromtimestamp(le['endedAt']) if le.get('endedAt') else '?'}")
    print(f"Last success:       {datetime.fromtimestamp(lse['endedAt']) if lse.get('endedAt') else '?'}")
```

### "What datasets are completely orphaned?"

Orphaned = no cards AND not a dataflow input AND not used by any workflow.

```python
flow_inputs = set()
for flow in flows:
    for inp in flow.get("inputs", []):
        flow_inputs.add(inp["dataSourceId"])

wf_inputs = set(ds_id for ds_ids in extract_workflow_datasets(models).values() for ds_id in ds_ids)

orphans = []
for ds in datasets:  # full paginated dataset list
    if (ds["cardInfo"]["cardCount"] == 0
            and ds["id"] not in flow_inputs
            and ds["id"] not in wf_inputs):
        orphans.append(ds)

for ds in sorted(orphans, key=lambda x: x["lastUpdated"]):
    age = (datetime.now() - datetime.fromtimestamp(ds["lastUpdated"] / 1000)).days
    print(f"{ds['name'][:60]}  |  {age}d old  |  owner={ds['owner']['name']}  |  type={ds['displayType']}")
```

### "Which datasets have dead content?"

Cards exist but have never been viewed — content nobody looks at.

```python
dead = [ds for ds in datasets
        if ds["cardInfo"]["cardCount"] > 0 and ds["cardInfo"]["cardViewCount"] == 0]

print(f"{len(dead)} datasets with cards that have never been viewed")
for ds in dead[:20]:
    print(f"  {ds['name'][:60]} | {ds['cardInfo']['cardCount']} cards | owner={ds['owner']['name']}")
```

### "What is the full downstream impact of dataset X?"

`impactCardCount` is the lineage-aware importance score — cards reachable downstream through any number of dataflows, not just direct cards.

```python
ds = requests.get(f"{BASE}/data/v3/datasources/DATASET-UUID",
                  headers=H, params={"includeAllDetails": "true"}, timeout=15).json()

print(f"Direct impact:    {ds.get('alertCount',0) + ds.get('cardCount',0) + ds.get('dataSourceCount',0) + ds.get('dataFlowCount',0)}")
print(f"Total downstream: {ds.get('impactDataSourceCount',0) + ds.get('impactDataFlowCount',0) + ds.get('impactAlertCount',0) + ds.get('impactCardCount',0)}")
print(f"  ↳ {ds.get('impactCardCount','?')} cards  |  {ds.get('impactDataFlowCount','?')} dataflows  |  {ds.get('impactDataSourceCount','?')} datasets")
```
