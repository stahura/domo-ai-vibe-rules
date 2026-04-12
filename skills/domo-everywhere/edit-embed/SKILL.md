---
name: edit-embed
description: Set up Domo's embedded edit experience — external users create, edit, save, and share Domo content via an embedded iframe. Covers Identity Broker, JWT auth, role-based access (Admin/Privileged/Editor/Participant), instance mapping, and edit URL generation. Use for any Domo edit-mode embedding. Not for read-only embeds (use programmatic-filters) or client-side filtering (use jsapi-filters).
---

> **Child instance observability:** To inspect lineage, usage, stale content, or provision API credentials for a Domo Everywhere child instance, see `administration/lineage-observability/SKILL.md`.

# Domo Embedded Edit Experience

Let external users create, edit, save, and share Domo content (dashboards, cards, alerts, reports, data sources) through an embedded iframe. Uses the **Domo Identity Broker** with JWT auth — fundamentally different from read-only embeds.

For read-only embeds, see `programmatic-filters`. For client-side filtering, see `jsapi-filters`.

## How It Works

1. Your server authenticates the user and creates a **JWT** with identity, role, and routing attributes
2. JWT is signed with a shared secret from Domo
3. Server constructs edit URL: `{IDP_URL}/jwt?token={jwt_token}`
4. Client renders URL directly as iframe `src` (no POST form needed)
5. **Identity Broker** validates JWT, routes user to correct Domo instance by role

Key difference: read-only = OAuth → embed token → POST form. Edit = JWT → Identity Broker URL → iframe src.

## Prerequisites

Work with your Domo CSM to set up the Identity Broker. Provide: your Domo instance URL, auth method (JWT), routing attribute key, and attribute-to-instance mappings.

You receive: Identity Broker URL, JWT signing secret (UUID), and attribute key config.

**Required env vars:** `IDP_URL` (Broker URL), `JWT_SECRET` (signing secret), `KEY_ATTRIBUTE` (routing attribute name).

---

## The Domo Identity Broker

Authenticates users (validates JWT signature) and routes them to the correct Domo instance based on the mapping attribute. Supports SAML2, OIDC, JWT, OAuth2 — JWT is most common for embeds.

### Instance Mapping

Each mapping attribute value corresponds to a Domo instance:

| Attribute Value | Domo Instance    |
| --------------- | ---------------- |
| `acme-corp`     | acme.domo.com    |
| `globex`        | globex.domo.com  |
| `initech`       | initech.domo.com |

Configured via your CSM (webform dataset or Excel). Comma-separated values route to multiple instances.

---

## JWT Token Structure

### Required Fields

| Field             | Type               | Description                                                                |
| ----------------- | ------------------ | -------------------------------------------------------------------------- |
| `sub`             | string             | The user's identifier — typically their email address                      |
| `exp`             | number             | Expiration time (EPOCH timestamp). Keep this short (5 minutes recommended) |
| `jti`             | string             | Unique token identifier. Use a UUID v4 to prevent replay attacks           |
| `{KEY_ATTRIBUTE}` | string or string[] | The routing attribute that maps the user to a Domo instance                |

### Common Optional Fields

| Field         | Type     | Description                                                  |
| ------------- | -------- | ------------------------------------------------------------ |
| `name`        | string   | Display name for the user in Domo                            |
| `email`       | string   | User's email address                                         |
| `role`        | string   | Domo role: `Admin`, `Privileged`, `Editor`, or `Participant` |
| `employee_id` | string   | Employee identifier                                          |
| `title`       | string   | Job title                                                    |
| `department`  | string   | Department name                                              |
| `location`    | string   | Location                                                     |
| `phone`       | string   | Phone number                                                 |
| `locale`      | string   | Locale preference                                            |
| `timezone`    | string   | Timezone preference                                          |
| `groups`      | string[] | Group assignments within Domo                                |

### Domo Roles

| Role          | Capabilities                                                            |
| ------------- | ----------------------------------------------------------------------- |
| `Admin`       | Full access — manage users, data, content, and settings                 |
| `Privileged`  | Create/edit dashboards, cards, dataflows; manage data sources           |
| `Editor`      | Create/edit dashboards and cards; limited data source access            |
| `Participant` | View and interact with shared content only (default if omitted)         |

Most external users should be `Editor` or `Participant`.

---

## Server-Side Implementation

### Step 1: Create the JWT Token

**Node.js / TypeScript:**

```typescript
import jwt from "jsonwebtoken";
import { v4 as uuidv4 } from "uuid";

function createEditToken(user: {
  username: string;
  email: string;
  domoRole?: string;
  mappingValue?: string | string[];
}) {
  const jwtBody: Record<string, unknown> = {
    sub: user.username,
    name: user.username,
    email: user.email,
    role: user.domoRole || "Participant",
    jti: uuidv4(),
  };

  // Add the routing attribute for instance mapping
  const keyAttribute = process.env.KEY_ATTRIBUTE;
  if (keyAttribute && user.mappingValue) {
    jwtBody[keyAttribute] = user.mappingValue;
  }

  return jwt.sign(jwtBody, process.env.JWT_SECRET!, {
    expiresIn: "5m",
    algorithm: "HS256",
  });
}
```

**Python:**

```python
import jwt
import uuid
import time
import os

def create_edit_token(user):
    payload = {
        'sub': user['username'],
        'name': user['username'],
        'email': user['email'],
        'role': user.get('domo_role', 'Participant'),
        'jti': str(uuid.uuid4()),
        'exp': int(time.time()) + 300  # 5 minutes
    }

    key_attribute = os.environ.get('KEY_ATTRIBUTE')
    if key_attribute and user.get('mapping_value'):
        payload[key_attribute] = user['mapping_value']

    return jwt.encode(payload, os.environ['JWT_SECRET'], algorithm='HS256')
```

### Step 2: Construct the Edit URL

```typescript
const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}`;
```

Optionally deep-link to a specific page:

```typescript
const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}&destination=/page/${pageId}`;
```

### Step 3: Build the API Route

**Next.js App Router:**

```typescript
// app/api/editembed/route.ts
import type { NextRequest } from "next/server";
import { NextResponse } from "next/server";
import jwt from "jsonwebtoken";
import { v4 as uuidv4 } from "uuid";

export async function POST(req: NextRequest) {
  try {
    const { embedID } = await req.json();

    // Authenticate the user against your own auth system
    const token = req.cookies.get("token")?.value;
    if (!token) {
      return NextResponse.json(
        { message: "Unauthorized: Please log in" },
        { status: 401 },
      );
    }

    const user = await verifyAndGetUser(token);
    if (!user) {
      return NextResponse.json({ message: "User not found" }, { status: 404 });
    }

    // Handle comma-separated mapping values
    let mappingValue = user.mappingValue;
    if (typeof mappingValue === "string" && mappingValue.includes(",")) {
      mappingValue = mappingValue.split(",").map((s: string) => s.trim());
    }

    // Build the JWT payload
    const jwtBody: Record<string, unknown> = {
      sub: user.username,
      name: user.username,
      role: user.domoRole || "Participant",
      email: user.email,
      jti: uuidv4(),
    };

    const keyAttr = process.env.KEY_ATTRIBUTE;
    if (keyAttr && mappingValue) {
      jwtBody[keyAttr] = mappingValue;
    }

    // Sign the token
    const editToken = jwt.sign(jwtBody, process.env.JWT_SECRET || "", {
      expiresIn: "5m",
    });

    // Return the Identity Broker URL
    const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}`;
    return NextResponse.json(editUrl);
  } catch (error) {
    console.error("Error in /api/editembed:", error);
    return NextResponse.json(
      { message: "Server error occurred" },
      { status: 500 },
    );
  }
}
```

**Express example:**

```typescript
app.post("/api/editembed", authenticateUser, (req, res) => {
  const user = req.user;

  let mappingValue = user.mappingValue;
  if (typeof mappingValue === "string" && mappingValue.includes(",")) {
    mappingValue = mappingValue.split(",").map((s) => s.trim());
  }

  const jwtBody = {
    sub: user.username,
    name: user.username,
    role: user.domoRole || "Participant",
    email: user.email,
    jti: uuidv4(),
  };

  const keyAttr = process.env.KEY_ATTRIBUTE;
  if (keyAttr && mappingValue) {
    jwtBody[keyAttr] = mappingValue;
  }

  const editToken = jwt.sign(jwtBody, process.env.JWT_SECRET, {
    expiresIn: "5m",
  });

  const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}`;
  res.json(editUrl);
});
```

### Step 4: Render in an Iframe

Edit embeds load directly via iframe `src` (no POST form like read-only embeds):

```tsx
function EditEmbed({ editUrl }: { editUrl: string }) {
  return (
    <iframe
      src={editUrl}
      style={{ width: "100%", height: "100%", border: "none" }}
      allow="fullscreen"
    />
  );
}
```

---

## Handling Read-Only vs Edit Mode

If your app supports both read-only and edit modes, your embed component needs to handle both flows:

```tsx
function EmbedDashboard({ embedID }: { embedID: string }) {
  const [embedURL, setEmbedURL] = useState<string | null>(null);
  const [embedToken, setEmbedToken] = useState<string | null>(null);
  const isEditMode = embedID === "edit";

  useEffect(() => {
    const endpoint = isEditMode ? "/api/editembed" : "/api/getembedtoken";

    fetch(endpoint, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ embedID }),
      credentials: "include",
    })
      .then((res) => res.json())
      .then((data) => {
        if (isEditMode) {
          setEmbedURL(data); // Edit returns a direct URL string
          setEmbedToken(null);
        } else {
          setEmbedURL(data.embedUrl); // Read-only returns { embedUrl, embedToken }
          setEmbedToken(data.embedToken);
        }
      });
  }, [embedID, isEditMode]);

  // Edit mode: direct iframe src
  if (isEditMode && embedURL) {
    return (
      <iframe
        src={embedURL}
        style={{ width: "100%", height: "100%", border: "none" }}
      />
    );
  }

  // Read-only mode: POST form submission to iframe
  // (handle embedToken + form submission as in programmatic-filters skill)
}
```

---

## User Management for Edit Embeds

### Key User Properties

| Property       | Purpose                              | Example                                    |
| -------------- | ------------------------------------ | ------------------------------------------ |
| `domoRole`     | Controls edit capabilities           | `'Editor'`, `'Participant'`                |
| `mappingValue` | Routes user to correct Domo instance | `'acme-corp'` or `['acme-corp', 'globex']` |
| `email`        | Required for Domo user identity      | `'user@example.com'`                       |

### Multi-Instance Users

If a user needs access to multiple Domo instances, store their `mappingValue` as a comma-separated string or array:

```typescript
// Single instance
user.mappingValue = "acme-corp";

// Multiple instances
user.mappingValue = "acme-corp, globex";
// or
user.mappingValue = ["acme-corp", "globex"];
```

When building the JWT, handle both formats:

```typescript
let mappingValue = user.mappingValue;
if (typeof mappingValue === "string" && mappingValue.includes(",")) {
  mappingValue = mappingValue.split(",").map((s) => s.trim());
}
```

---

## Deep Linking

```typescript
const editUrl = `${IDP_URL}/jwt?token=${editToken}&destination=/page/${pageId}`;
const editUrl = `${IDP_URL}/jwt?token=${editToken}&destination=/kpicard/${cardId}`;
```

---

## Gotchas and Best Practices

- **Token expiration:** Keep JWTs short-lived (5 min recommended). Only used for initial auth — session persists after.
- **Signing algorithm:** Use `HS256`. Domo expects this for the Identity Broker.
- **JTI uniqueness:** Always UUID v4. Domo may reject reused JTI values (replay protection).
- **Mapping values:** `KEY_ATTRIBUTE` name is whatever you agreed on with your CSM (`customer`, `keyAttribute`, `tenant`). Values must match Domo's instance mapping exactly.
- **Secret management:** Never expose `JWT_SECRET` client-side. Use env vars or a secrets manager.
- **Security model:** Read-only embeds scope to specific dashboards with filters. Edit embeds give a full Domo session per role — be conservative with role assignment.
- **Instance mapping changes:** Use stable values (tenant IDs, not company names that might change).

---

## Environment Variables Reference

| Variable        | Description                         | Example                                 |
| --------------- | ----------------------------------- | --------------------------------------- |
| `IDP_URL`       | Identity Broker URL                 | `https://yourcompany.identity.domo.com` |
| `JWT_SECRET`    | Shared signing secret (UUID format) | `aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeee`    |
| `KEY_ATTRIBUTE` | Attribute key for instance routing  | `keyAttribute`, `customer`, `tenant`    |

---

## TypeScript Type Definitions

```typescript
type DomoRole = "Admin" | "Privileged" | "Editor" | "Participant";

interface EditEmbedUser {
  username: string;
  email: string;
  domoRole?: DomoRole;
  mappingValue?: string | string[];
}

interface EditJwtPayload {
  sub: string;
  name?: string;
  email?: string;
  role?: DomoRole;
  jti: string;
  exp?: number;
  [keyAttribute: string]: unknown; // dynamic routing attribute
}
```

---

## Quick Reference

Read `references/identity-broker.md` for additional details on Identity Broker configuration and instance mapping management.
