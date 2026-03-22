# Domo Programmatic Filtering — API Endpoints

## Table of Contents
1. [Access Token](#access-token)
2. [Embed Token — Dashboard](#embed-token--dashboard)
3. [Embed Token — Card](#embed-token--card)
4. [Embed URLs](#embed-urls)

---

## Access Token

Exchange OAuth client credentials for an access token.

```
GET https://api.domo.com/oauth/token?grant_type=client_credentials&scope=data%20audit%20user%20dashboard
Authorization: Basic base64(CLIENT_ID:CLIENT_SECRET)
```

**Response:**
```json
{
  "access_token": "eyJhbGci...",
  "token_type": "bearer",
  "expires_in": 3599,
  "scope": "data audit user dashboard",
  "customer": "example",
  "env": "prod1",
  "userId": 123456789,
  "role": "Admin",
  "jti": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}
```

**Notes:**
- `expires_in` is in seconds (typically 3599 = ~1 hour)
- Cache and reuse the token until near expiry
- The scope parameter controls what APIs the token can access

---

## Embed Token — Dashboard

Generate an embed token for one or more dashboards, with optional programmatic filters.

```
POST https://api.domo.com/v1/stories/embed/auth
Authorization: Bearer {access_token}
Content-Type: application/json
```

**Request body:**
```json
{
  "sessionLength": 1440,
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "filters": [
        {
          "column": "Region",
          "operator": "IN",
          "values": ["West"],
          "datasourceId": "optional-uuid"
        }
      ],
      "sqlFilters": [
        {
          "sqlFilter": "`Column` = 'value'",
          "datasourceIds": ["optional-uuid"]
        }
      ],
      "policies": []
    }
  ]
}
```

**Response:**
```json
{
  "id": 12345,
  "authentication": "eyJhbGci...",
  "expiration": 1234567890000
}
```

The `authentication` field is the embed token to submit via POST form.

---

## Embed Token — Card

Same structure as dashboard, different endpoint.

```
POST https://api.domo.com/v1/cards/embed/auth
Authorization: Bearer {access_token}
Content-Type: application/json
```

Request and response structure are identical to the dashboard endpoint.

---

## Embed URLs

Where to POST the embed token for rendering:

| Type | URL Pattern |
|------|-------------|
| Dashboard | `https://public.domo.com/embed/pages/{embed_id}` |
| Card | `https://public.domo.com/cards/{embed_id}` |

Submit via hidden form with `embedToken` as a form field, targeting an iframe:

```html
<form action="{embed_url}" method="POST" target="{iframe_name}">
  <input type="hidden" name="embedToken" value="{authentication_token}" />
</form>
```

---

## Error Responses

Common error codes from the embed token endpoints:

| Status | Meaning | Common Cause |
|--------|---------|--------------|
| 401 | Unauthorized | Expired or invalid access token |
| 403 | Forbidden | Client doesn't have embed permissions |
| 404 | Not Found | Invalid embed ID |
| 400 | Bad Request | Malformed filter structure, invalid operator, or missing required fields |

When you get a 401, refresh your access token and retry. For 400 errors, check that filter column names match the dataset exactly and operator names use the correct casing.

---

## Dataset Switching (datasetRedirects)

Dataset switching is passed as part of the embed token authorization payload, not as a separate API call.

Add `datasetRedirects` to the authorization object in the embed token request:

```json
{
  "sessionLength": 1440,
  "authorizations": [
    {
      "token": "<embed_id>",
      "permissions": ["READ", "FILTER", "EXPORT"],
      "filters": [],
      "datasetRedirects": {
        "<original_dataset_uuid>": "<target_dataset_uuid>"
      }
    }
  ]
}
```

- Keys are the dataset UUIDs the dashboard was originally built on
- Values are the dataset UUIDs to swap in at render time
- Target datasets must have matching column schemas (names and types)
- Compatible with `filters`, `sqlFilters`, and `policies` in the same authorization
