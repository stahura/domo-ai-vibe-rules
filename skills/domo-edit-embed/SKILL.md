---
name: domo-edit-embed
description: Use this skill when a user wants to set up Domo's embedded edit experience, allowing external users to create, edit, save, and share Domo content (dashboards, cards, alerts, reports) through an embedded interface. Covers the Domo Identity Broker, JWT authentication for edit mode, role-based access (Admin, Privileged, Editor, Participant), instance mapping with user attributes, and the full server-side flow for generating edit URLs. Trigger whenever someone needs to embed Domo in edit mode (not just read-only), configure the Identity Broker, set up JWT tokens for Domo edit access, map external users to Domo instances, assign Domo roles for embedded editing, or enable external users to build and modify Domo content. Do NOT trigger for read-only embedding with programmatic filters (use domo-programmatic-filters), client-side runtime filtering (use domo-client-filters), creating embed IDs, or Domo SSO for internal users.
---

# Domo Embedded Edit Experience

The embedded edit experience lets external users create, edit, save, and share Domo content through an embedded interface in your application. Unlike read-only embeds (which use embed tokens and programmatic filters), edit embeds authenticate users through the **Domo Identity Broker** using JWT tokens, giving them a role-based Domo session where they can build dashboards, create alerts, schedule reports, connect data sources, and transform data.

Use this when you want external customers or partners to:

- Build and modify their own dashboards and cards
- Create alerts and scheduled reports
- Connect and transform data sources
- Collaborate on content within their scoped environment

For read-only embedded viewing with data filtering, see `domo-programmatic-filters`. For client-side runtime filtering, see `domo-client-filters`.

## How It Works

The edit embed flow is fundamentally different from read-only embeds:

1. Your server authenticates the user against your own system
2. Your server creates a **JWT token** containing the user's identity, role, and routing attributes
3. The JWT is signed with a shared secret provided by Domo
4. Your server constructs an edit URL: `{IDP_URL}/jwt?token={jwt_token}`
5. The client renders this URL directly in an iframe — no POST form submission needed
6. The **Domo Identity Broker** validates the JWT, maps the user to the correct Domo instance, and grants access based on their role

The key difference: read-only embeds use OAuth client credentials → embed token → POST form. Edit embeds use JWT → Identity Broker URL → direct iframe src.

## Prerequisites

Before implementing edit embeds, you need to work with your Domo CSM (Customer Success Manager) to set up:

1. **Identity Broker configuration** — Provide your CSM with:
   - Your Domo instance URL
   - Your preferred authentication method (JWT is most common)
   - The user attribute key you'll use for routing (e.g., `customer`, `keyAttribute`)
   - Attribute-to-account mappings (which attribute values map to which Domo instances)

2. **In return, you receive:**
   - The Identity Broker URL (e.g., `https://yourcompany.identity.domo.com`)
   - A JWT signing secret (UUID format)
   - Configuration for the attribute key

3. **Environment variables** your server needs:
   - `IDP_URL` — The Identity Broker URL
   - `JWT_SECRET` — The signing secret
   - `KEY_ATTRIBUTE` — The attribute key name for instance routing

---

## The Domo Identity Broker

The Identity Broker is the gateway that authenticates users and routes them to the correct Domo environment. It supports SAML2, OIDC, JWT, and OAuth2, but JWT is the most common for embedded edit experiences because it's simple and server-side.

The broker does two things:

1. **Authenticates** the user by validating the JWT signature against the shared secret
2. **Routes** the user to the correct Domo instance based on the mapping attribute in the JWT payload

### Instance Mapping

Each value of your mapping attribute corresponds to a Domo instance (or a scoped environment within an instance). For example:

| Attribute Value | Domo Instance    |
| --------------- | ---------------- |
| `acme-corp`     | acme.domo.com    |
| `globex`        | globex.domo.com  |
| `initech`       | initech.domo.com |

The mapping is configured on Domo's side (via your CSM) using either a webform dataset or an Excel sheet. Changes to mappings require a support ticket.

Users with multiple mapping values (comma-separated) can be routed to multiple instances.

---

## JWT Token Structure

The JWT token contains the user's identity and determines what they can do in the embedded edit experience.

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

The `role` field controls what the user can do in the embedded edit experience:

| Role          | Capabilities                                                            |
| ------------- | ----------------------------------------------------------------------- |
| `Admin`       | Full access — manage users, data, content, and settings                 |
| `Privileged`  | Create and edit dashboards, cards, dataflows; manage data sources       |
| `Editor`      | Create and edit dashboards and cards; limited data source access        |
| `Participant` | View and interact with shared content only (default if role is omitted) |

Choose the minimum role needed. Most external users should be `Editor` or `Participant`.

---

## Server-Side Implementation

### Step 1: Create the JWT Token

Sign a JWT with the user's identity, role, and routing attribute using the shared secret from Domo.

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

The edit URL sends the JWT to the Identity Broker, which validates it and redirects the user to the Domo edit experience:

```typescript
const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}`;
```

You can optionally append a `destination` parameter to deep-link to a specific page:

```typescript
const editUrl = `${process.env.IDP_URL}/jwt?token=${editToken}&destination=/page/${pageId}`;
```

### Step 3: Build the API Route

Create a server-side endpoint that authenticates your user, generates the JWT, and returns the edit URL.

**Next.js App Router example:**

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

Unlike read-only embeds (which require a POST form submission), edit embeds load directly via the iframe's `src` attribute:

```tsx
// React component
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

**Comparison with read-only embed rendering:**

- **Read-only:** Fetch embed token → create hidden form → POST to iframe target
- **Edit:** Fetch edit URL → set as iframe `src` directly

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
  // (handle embedToken + form submission as in domo-programmatic-filters skill)
}
```

---

## User Management for Edit Embeds

Users who access the edit experience need additional fields beyond what read-only users need:

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

Use the `destination` parameter to send users directly to a specific page or dashboard in the edit experience:

```typescript
// Link to a specific page
const editUrl = `${IDP_URL}/jwt?token=${editToken}&destination=/page/${pageId}`;

// Link to a specific card
const editUrl = `${IDP_URL}/jwt?token=${editToken}&destination=/kpicard/${cardId}`;
```

This is useful when you want to open the editor to a specific piece of content rather than the Domo home screen.

---

## Gotchas and Best Practices

### Token Expiration

Keep JWT tokens short-lived (5 minutes is recommended). The token is only used for the initial authentication — once the user is in the Domo session, the token is no longer needed. Short-lived tokens reduce the risk of token theft or replay.

### Signing Algorithm

Use `HS256` (HMAC-SHA256) for JWT signing. This is what Domo expects for the Identity Broker.

### JTI Uniqueness

Always use a UUID v4 for the `jti` field. This prevents replay attacks where a captured token is reused. Domo may reject tokens with previously-seen JTI values.

### Mapping Value Handling

The `KEY_ATTRIBUTE` field name is configurable — it's whatever you agreed on with your CSM. Common choices are `customer`, `keyAttribute`, or `tenant`. Make sure the values match exactly what's configured in the instance mapping on Domo's side.

### Secret Management

The `JWT_SECRET` is a shared secret between your server and Domo's Identity Broker. Treat it like a password:

- Never expose it in client-side code
- Store it in environment variables or a secrets manager
- Don't commit it to version control

### Edit vs Read-Only Security Model

- **Read-only embeds** use OAuth client credentials (CLIENT_ID/SECRET) → embed token. The token is scoped to specific dashboards with specific filters.
- **Edit embeds** use JWT → Identity Broker. The user gets a full Domo session with their assigned role. The scope is controlled by the role (Admin/Privileged/Editor/Participant) and the instance mapping.

Edit embeds give users more power. Be thoughtful about role assignment — most external users should be `Editor` or `Participant`, not `Admin` or `Privileged`.

### Instance Mapping Changes

Changing which attribute values map to which Domo instances requires a support ticket to Domo. Plan your mapping strategy upfront and use stable, predictable values (like tenant IDs rather than company names that might change).

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
