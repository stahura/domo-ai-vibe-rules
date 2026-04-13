---
name: domo-auth
description: Unified Domo authentication for CLI tools and MCP servers. Covers credential resolution (ryuu session, dev token, env vars), the full SID token exchange flow, multi-instance support, and when to use each auth header.
---
# Domo Authentication

## Purpose

Authenticate programmatically against Domo instance APIs. This skill covers how credentials are stored, how to resolve them, and how to exchange them for the headers Domo's APIs expect.

Use this as the foundation for any tool, script, or MCP server that needs to call Domo REST APIs outside of the custom app iframe context.

---

## Two Auth Headers

Domo instance APIs accept two authentication headers. Know which one you need:

| Header | Source | Exchange needed? | Best for |
|--------|--------|-----------------|----------|
| `X-Domo-Authentication: {SID}` | Ryuu CLI refresh token | Yes — 3-step exchange | Interactive tools, auto-refresh, piggybacking `domo login` |
| `X-Domo-Developer-Token: {token}` | Admin Console > Security > Access Tokens | No — use directly | CI/CD, headless scripts, env var config |

**SID** is preferred for interactive use because it auto-refreshes from the stored refresh token. **Developer tokens** are preferred for automation because they require no exchange step.

> **App Studio REST APIs**: Some endpoints (card creation, layout updates) work with both headers. Others silently fail with developer tokens but succeed with SID. When in doubt, use SID.

---

## Credential Resolution Order

When building a tool that authenticates to Domo, resolve credentials in this priority order:

### 1. Explicit environment variables (CI / headless)

```bash
export DOMO_INSTANCE=company.domo.com
export DOMO_TOKEN=DDCI27236b8d8690ab86cf...
```

If both are set, use `DOMO_TOKEN` directly as `X-Domo-Developer-Token`. No exchange needed.

### 2. Ryuu CLI configstore (interactive / piggybacking `domo login`)

After a user runs `domo login`, credentials are stored at:

```
~/.config/configstore/ryuu/{instance}.json
```

Example: `~/.config/configstore/ryuu/company.domo.com.json`

```json
{
  "instance": "company.domo.com",
  "refreshToken": "eyJhbGciOiJub25lIi...",
  "devToken": false
}
```

| Field | Description |
|-------|-------------|
| `instance` | Domo instance hostname |
| `refreshToken` | JWT refresh token (long-lived) or developer token |
| `devToken` | `false` = OAuth refresh token, `true` = developer token stored as refreshToken |

**Multi-instance support:** Each instance gets its own JSON file. To auto-detect the most recently used instance, pick the file with the latest `mtime`.

**XDG compliance:** The configstore directory follows XDG conventions. If `$XDG_CONFIG_HOME` is set, credentials are at `$XDG_CONFIG_HOME/configstore/ryuu/` instead of `~/.config/configstore/ryuu/`.

### 3. Fail with a helpful message

If no credentials are found, tell the user what to do:

```
No Domo credentials found.
Run 'domo login' to authenticate, or set DOMO_INSTANCE and DOMO_TOKEN environment variables.
```

If credentials exist but no instance is specified, list available instances:

```
No instance specified. Available instances from 'domo login':
  company.domo.com, sandbox.domo.com, demo.domo.com
Set DOMO_INSTANCE or pass --instance.
```

---

## SID Token Exchange

When using a refresh token (not a developer token), exchange it for a session ID in two steps.

### Step 1: Refresh token → Access token

```
POST https://{instance}/api/oauth2/token
Content-Type: application/x-www-form-urlencoded;charset=utf-8

client_id=domo:internal:devstudio
grant_type=refresh_token
refresh_token={refreshToken}
```

**Response:**
```json
{
  "access_token": "eyJ...",
  "token_type": "Bearer",
  "expires_in": 3600
}
```

### Step 2: Access token → Session ID

```
GET https://{instance}/api/oauth2/sid
Authorization: Bearer {access_token}
```

**Response:**
```json
{
  "sid": "eyJjdXN0b21lcklkIjoi..."
}
```

### Step 3: Use the SID

```
GET https://{instance}/api/content/v2/users/me
X-Domo-Authentication: {sid}
```

### Caching

SIDs last approximately 60 minutes. Cache the SID and refresh it at ~55 minutes to avoid mid-request expiration. A single SID can be used across many parallel requests.

---

## Implementation Reference

### Node.js / TypeScript

```typescript
import { readFileSync, readdirSync, statSync, existsSync } from "node:fs";
import { join } from "node:path";
import { homedir } from "node:os";

// ── Read credentials ─────────────────────────────────────────────

const RYUU_DIR = join(
  process.env.XDG_CONFIG_HOME ?? join(homedir(), ".config"),
  "configstore",
  "ryuu"
);

function readCredentials(instance: string) {
  const filePath = join(RYUU_DIR, `${instance}.json`);
  if (!existsSync(filePath)) return null;
  const raw = JSON.parse(readFileSync(filePath, "utf-8"));
  return {
    instance: raw.instance,
    refreshToken: raw.refreshToken,
    devToken: !!raw.devToken,
  };
}

function getMostRecentInstance(): string | null {
  if (!existsSync(RYUU_DIR)) return null;
  const files = readdirSync(RYUU_DIR).filter(f => f.endsWith(".json"));
  let newest: { name: string; mtime: number } | null = null;
  for (const f of files) {
    const { mtimeMs } = statSync(join(RYUU_DIR, f));
    if (!newest || mtimeMs > newest.mtime) {
      newest = { name: f.replace(/\.json$/, ""), mtime: mtimeMs };
    }
  }
  return newest?.name ?? null;
}

// ── Token exchange ───────────────────────────────────────────────

async function exchangeForSID(instance: string, refreshToken: string) {
  // Step 1: refresh → access token
  const tokenRes = await fetch(`https://${instance}/api/oauth2/token`, {
    method: "POST",
    headers: { "content-type": "application/x-www-form-urlencoded;charset=utf-8" },
    body: new URLSearchParams({
      client_id: "domo:internal:devstudio",
      grant_type: "refresh_token",
      refresh_token: refreshToken,
    }).toString(),
  });
  if (!tokenRes.ok) throw new Error(`Token exchange failed (${tokenRes.status})`);
  const { access_token } = await tokenRes.json();

  // Step 2: access token → SID
  const sidRes = await fetch(`https://${instance}/api/oauth2/sid`, {
    headers: { Authorization: `Bearer ${access_token}` },
  });
  if (!sidRes.ok) throw new Error(`SID exchange failed (${sidRes.status})`);
  const { sid } = await sidRes.json();

  return sid;
}

// ── Resolve and authenticate ─────────────────────────────────────

async function getAuthHeaders(instanceOverride?: string) {
  // Priority 1: env vars
  const envToken = process.env.DOMO_TOKEN;
  const envInstance = process.env.DOMO_INSTANCE;
  if (envToken && envInstance) {
    return {
      instance: envInstance,
      headers: { "X-Domo-Developer-Token": envToken },
    };
  }

  // Priority 2: ryuu configstore
  const instance = instanceOverride ?? envInstance ?? getMostRecentInstance();
  if (!instance) throw new Error("No Domo credentials found. Run 'domo login' first.");

  const creds = readCredentials(instance);
  if (!creds) throw new Error(`No credentials for '${instance}'. Run 'domo login -i ${instance}'.`);

  if (creds.devToken) {
    return {
      instance: creds.instance,
      headers: { "X-Domo-Developer-Token": creds.refreshToken },
    };
  }

  const sid = await exchangeForSID(creds.instance, creds.refreshToken);
  return {
    instance: creds.instance,
    headers: { "X-Domo-Authentication": sid },
  };
}
```

### Python

```python
import json, os, time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.parse import urlencode

RYUU_DIR = Path(
    os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
) / "configstore" / "ryuu"


def read_credentials(instance: str) -> dict | None:
    path = RYUU_DIR / f"{instance}.json"
    if not path.exists():
        return None
    data = json.loads(path.read_text())
    return {
        "instance": data["instance"],
        "refresh_token": data["refreshToken"],
        "dev_token": bool(data.get("devToken", False)),
    }


def get_most_recent_instance() -> str | None:
    if not RYUU_DIR.exists():
        return None
    files = sorted(RYUU_DIR.glob("*.json"), key=lambda f: f.stat().st_mtime, reverse=True)
    return files[0].stem if files else None


def exchange_for_sid(instance: str, refresh_token: str) -> str:
    # Step 1: refresh -> access token
    body = urlencode({
        "client_id": "domo:internal:devstudio",
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }).encode()
    req = Request(
        f"https://{instance}/api/oauth2/token",
        data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded;charset=utf-8"},
    )
    with urlopen(req) as resp:
        access_token = json.loads(resp.read())["access_token"]

    # Step 2: access token -> SID
    req = Request(
        f"https://{instance}/api/oauth2/sid",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    with urlopen(req) as resp:
        return json.loads(resp.read())["sid"]


def get_auth_headers(instance: str | None = None) -> tuple[str, dict]:
    """Returns (instance, headers_dict)."""
    # Priority 1: env vars
    env_token = os.environ.get("DOMO_TOKEN")
    env_instance = os.environ.get("DOMO_INSTANCE")
    if env_token and env_instance:
        return env_instance, {"X-Domo-Developer-Token": env_token}

    # Priority 2: ryuu configstore
    instance = instance or env_instance or get_most_recent_instance()
    if not instance:
        raise RuntimeError("No Domo credentials found. Run 'domo login' first.")

    creds = read_credentials(instance)
    if not creds:
        raise RuntimeError(f"No credentials for '{instance}'. Run 'domo login -i {instance}'.")

    if creds["dev_token"]:
        return creds["instance"], {"X-Domo-Developer-Token": creds["refresh_token"]}

    sid = exchange_for_sid(creds["instance"], creds["refresh_token"])
    return creds["instance"], {"X-Domo-Authentication": sid}
```

### curl (manual testing)

```bash
# Using a developer token
curl -s "https://company.domo.com/api/content/v2/users/me" \
  -H "X-Domo-Developer-Token: DDCI27236b8d8690ab86cf..."

# Using ryuu refresh token (3-step exchange)
INSTANCE="company.domo.com"
REFRESH_TOKEN=$(jq -r .refreshToken ~/.config/configstore/ryuu/$INSTANCE.json)

ACCESS_TOKEN=$(curl -s "https://$INSTANCE/api/oauth2/token" \
  -d "client_id=domo:internal:devstudio&grant_type=refresh_token&refresh_token=$REFRESH_TOKEN" \
  -H "Content-Type: application/x-www-form-urlencoded" | jq -r .access_token)

SID=$(curl -s "https://$INSTANCE/api/oauth2/sid" \
  -H "Authorization: Bearer $ACCESS_TOKEN" | jq -r .sid)

curl -s "https://$INSTANCE/api/content/v2/users/me" \
  -H "X-Domo-Authentication: $SID"
```

---

## Gotchas

| Issue | Detail |
|-------|--------|
| **SID vs developer token on App Studio** | Some App Studio endpoints (`/content/v3/cards/kpi`, `/content/v4/pages/layouts`) silently reject developer tokens. SID works universally. |
| **Refresh token expiry** | If `domo login` was run months ago, the refresh token may have expired. Re-run `domo login` to get a fresh one. The exchange will return a clear `401` when this happens. |
| **Multi-instance cookie collision** | Ryuu stores one file per instance. If a tool reads the wrong file, check that the instance hostname matches exactly (e.g., `company.domo.com` not `company`). |
| **Configstore permissions** | Credential files are created with `600` permissions. If your tool runs as a different user, it won't be able to read them. |
| **Domo Everywhere (embed) auth is separate** | Embed flows use OAuth client credentials against `api.domo.com` (not instance APIs). That's a different credential pair — `client_id` + `client_secret` from the Domo Admin Console. Don't mix these with instance auth. |

---

## Checklist

Before shipping a tool that authenticates to Domo:

- [ ] Resolves credentials from env vars OR ryuu configstore (not hardcoded)
- [ ] Handles multi-instance (user may have 10+ logins)
- [ ] Caches SID for reuse (~55 min TTL)
- [ ] Fails with a clear message when no credentials found
- [ ] Uses `X-Domo-Authentication` (SID) for App Studio / content APIs
- [ ] Uses `X-Domo-Developer-Token` only when explicitly configured
- [ ] Does not store credentials in version control
