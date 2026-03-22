# Domo Identity Broker Reference

## Table of Contents
1. [Overview](#overview)
2. [Supported Authentication Methods](#supported-authentication-methods)
3. [Setup Process](#setup-process)
4. [JWT Token Details](#jwt-token-details)
5. [Instance Mapping](#instance-mapping)
6. [URL Construction](#url-construction)

---

## Overview

The Domo Identity Broker is a centralized authentication gateway that:
- Authenticates users via JWT (or SAML2, OIDC, OAuth2)
- Maps users to the correct Domo instance based on a routing attribute
- Grants access based on the role specified in the token

The broker URL follows the pattern: `https://{company}.identity.domo.com`

---

## Supported Authentication Methods

| Method | Common Use Case |
|--------|----------------|
| JWT | Embedded edit experiences (most common, simplest for server-side) |
| SAML2 | Enterprise SSO integrations |
| OIDC | Modern SSO with identity providers like Okta, Auth0 |
| OAuth2 | API-to-API authentication |

For embedded edit experiences, JWT is the standard choice because the token is generated server-side with full control over claims.

---

## Setup Process

### What You Provide to Your CSM

1. Your Domo instance URL
2. Preferred authentication method (JWT)
3. User routing attribute name (e.g., `customer`, `keyAttribute`)
4. Attribute value → Domo instance mappings

### What You Receive

1. **Identity Broker URL** — `https://{company}.identity.domo.com`
2. **JWT signing secret** — UUID format (e.g., `22127d03-c655-4c27-a266-ad45104dab1e`)
3. **Certificate** (if using SAML2)
4. Confirmation of the attribute key name

---

## JWT Token Details

### Signing

| Property | Value |
|----------|-------|
| Algorithm | HS256 (HMAC-SHA256) |
| Secret | The UUID provided by Domo |
| Library | `jsonwebtoken` (Node.js), `PyJWT` (Python), or equivalent |

### Required Claims

```json
{
  "sub": "user@example.com",
  "jti": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "exp": 1711234567,
  "{KEY_ATTRIBUTE}": "tenant-id-or-mapping-value"
}
```

### Full Example Payload

```json
{
  "sub": "jane.doe@acme.com",
  "name": "Jane Doe",
  "email": "jane.doe@acme.com",
  "role": "Editor",
  "jti": "f47ac10b-58cc-4372-a567-0e02b2c3d479",
  "exp": 1711234867,
  "keyAttribute": "acme-corp",
  "title": "Data Analyst",
  "department": "Analytics",
  "groups": ["dashboard-editors", "sales-team"]
}
```

### Role Reference

| Role | Create Content | Edit Content | Manage Data | Manage Users |
|------|---------------|-------------|-------------|-------------|
| Admin | Yes | Yes | Yes | Yes |
| Privileged | Yes | Yes | Yes | No |
| Editor | Yes | Yes | Limited | No |
| Participant | No | No | No | No |

---

## Instance Mapping

### How It Works

The Identity Broker uses the value of your `KEY_ATTRIBUTE` claim to determine which Domo instance to route the user to. The mapping is maintained on Domo's side.

### Mapping Management Methods

1. **Webform dataset** — A dataset within the main Domo instance that maps attribute values to instance URLs. Changes take effect after the dataset is updated.

2. **Excel sheet** — Managed by Domo engineering. Changes require a support ticket.

### Multi-Instance Users

Users can be mapped to multiple instances by providing an array for the routing attribute:

```json
{
  "keyAttribute": ["acme-corp", "globex"]
}
```

Or as a comma-separated string that your server parses into an array before including in the JWT.

### Changing Mappings

Updating which attribute values route to which instances requires:
1. Updating the webform dataset or Excel sheet
2. If using the Excel method, submitting a support ticket
3. Changes typically take effect within minutes

---

## URL Construction

### Basic Edit URL

```
{IDP_URL}/jwt?token={jwt_token}
```

Example:
```
https://modocorp.identity.domo.com/jwt?token=eyJhbGciOiJIUzI1NiJ9...
```

### With Destination (Deep Link)

```
{IDP_URL}/jwt?token={jwt_token}&destination=/page/{page_id}
```

Supported destination paths:
- `/page/{page_id}` — Open a specific dashboard page
- `/kpicard/{card_id}` — Open a specific card

### Token Delivery

The JWT is passed as a URL query parameter. Since JWTs can be long, ensure your server and any proxies support URLs of sufficient length. The 5-minute expiration means the URL is only valid briefly.
