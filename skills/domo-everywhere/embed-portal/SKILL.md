---
name: embed-portal
description: "Use for any project where external users need a login to view or interact with Domo dashboards — regardless of what the user calls it. If someone wants clients, customers, or partners to have accounts and see Domo content (their data only, branded, filtered per user), this is the right skill. Covers the full build from scratch — auth, user management, data isolation, and Domo embed integration. Trigger on phrases like 'give clients a login to see dashboards,' 'sell access to our analytics,' 'white-label reporting for customers,' 'client portal with Domo,' 'productize our Domo data,' or 'external users should see their own dashboards.' Skip only if they already have a working portal and need just one specific sub-feature (edit embeds → use edit-embed, JS API filters → use jsapi-filters, programmatic filters → use programmatic-filters)."
---

# Build a Domo Embed Portal

This skill runs an end-to-end workflow: it gathers requirements, then delegates to existing capability skills for the Domo-specific implementation details. Do not duplicate content from those skills — read them at the appropriate step.

**Sub-skills used:**
- `programmatic-filters` — Read-only embed token flow, server-side filters, dataset switching
- `edit-embed` — Edit embed via Identity Broker, JWT auth, Domo roles
- `jsapi-filters` — Client-side filtering, drill events, iframe communication

---

## Phase 1: Gather Requirements

Before writing any code, collect three pieces of information. Ask conversationally — don't dump all questions at once. If answers are already clear from context, skip ahead.

### 1. Brand Guidelines

Ask: "What branding should the portal use? I need a color palette (primary, secondary, accent), fonts, and a logo if you have one."

Reasonable defaults if they don't have strong opinions:
- Primary: `#1A1A2E`, Secondary: `#16213E`, Accent: `#0F3460`, Text on dark: `#E0E0E0`
- Font: Inter (or system font stack)
- Logo: placeholder with app name

### 2. Embed Mode

Ask: "Should your users be able to **view dashboards only** (read-only), **edit dashboards** (create/modify content in Domo), or **both**?"

| Mode | What it means | Prerequisites |
|------|--------------|---------------|
| **Read-only** | Users view filtered dashboards via embed tokens | Domo API client (client ID + secret), embed IDs |
| **Edit** | Users get a full Domo editing session via Identity Broker | Identity Broker setup with Domo CSM, JWT secret, IDP URL |
| **Both** | Some dashboards are view-only, some are editable | Both sets of prerequisites |

### 3. User Management Approach

Ask: "How do you want to manage portal users?"

- **Domo AppDB** (recommended for Domo-native teams) — users, roles, and dashboard assignments stored in Domo's cloud database. No external infrastructure needed.
- **External database** (Postgres, MySQL, Supabase, etc.) — standard approach if you already have infrastructure.
- **Third-party auth provider** (Auth0, Clerk, Firebase Auth) — fastest login setup, handles password reset/MFA out of the box.

Default recommendation: **Domo AppDB** — keeps everything in the Domo ecosystem.

---

## Phase 2: Scaffold the Application

Suggest **Next.js** (App Router, TypeScript, Tailwind CSS) — it handles both the API layer and UI in one project, keeping the embed token flow secure. If the user prefers a different framework, adapt — the core patterns are framework-agnostic.

### Project Structure

```
src/
├── app/
│   ├── api/
│   │   ├── login/route.ts          # Login endpoint
│   │   ├── logout/route.ts         # Logout endpoint
│   │   ├── users/
│   │   │   ├── route.ts            # CRUD users (GET list, POST create)
│   │   │   └── [id]/route.ts       # Single user ops (PUT, DELETE)
│   │   ├── me/route.ts             # Current user session
│   │   ├── dashboards/
│   │   │   ├── route.ts            # Dashboard registry (GET list, POST create)
│   │   │   └── [id]/route.ts       # Single dashboard ops (PUT rename, DELETE)
│   │   ├── getembedtoken/route.ts  # Read-only embed tokens  (if read-only or both)
│   │   ├── editembed/route.ts      # Edit-mode JWT           (if edit or both)
│   │   └── password-reset/route.ts # Password reset flow
│   ├── login/page.tsx              # Login page
│   ├── home/
│   │   ├── layout.tsx              # Authenticated layout with sidebar
│   │   ├── page.tsx                # Default redirect
│   │   ├── [embedId]/page.tsx      # Dashboard embed view
│   │   └── admin/page.tsx          # Admin panel (users + dashboards + filters)
│   └── layout.tsx                  # Root layout with JS API init
├── lib/
│   ├── domoAppDb.ts                # AppDB CRUD wrapper (if AppDB chosen)
│   ├── jsapi.ts                    # Domo JS API handler
│   ├── verifyToken.ts              # JWT verification helper
│   └── constants.ts                # Config: URLs, collection IDs
├── middleware.ts                    # Protect routes, check auth
└── tailwind.config.ts              # Brand colors/fonts
```

### Environment Variables

Generate `.env.example` — include only what's relevant to the user's choices:

```bash
# === Domo OAuth (required for read-only embeds) ===
DOMO_CLIENT_ID=           # From developer.domo.com > My Account > New Client
DOMO_CLIENT_SECRET=

# === Domo AppDB (if using AppDB for user management) ===
APPDB_TOKEN=              # Developer token from Domo > Admin > Auth > Developer Tokens
DOMO_APPDB_BASE_URL=      # e.g. https://yourinstance.domo.com

# === Identity Broker (required for edit embeds) ===
IDP_URL=                  # e.g. https://yourcompany.identity.domo.com
JWT_SECRET=               # UUID shared secret from Domo CSM
KEY_ATTRIBUTE=            # Routing attribute name (e.g. "keyAttribute")

# === App Auth ===
APP_JWT_SECRET=           # Your own secret for login session tokens (separate from Domo's)
```

---

## Phase 3: Build — Implementation Order

Build in this order. Steps 1–3 are portal-specific (implemented here). Steps 4–6 are owned by sub-skills — your job is to wire the portal's data model into them, not re-implement them.

### Step 1: Authentication & Login

Read `references/auth-and-users.md` for full implementation patterns.

This is portal-specific — the sub-skills don't cover it. Build:
- Login page with the user's branding
- Login API route: validate credentials, issue session JWT as HttpOnly cookie
- Session verification helper used by all protected routes
- Route protection middleware

Key decisions:
- Passwords hashed with bcrypt (10+ salt rounds)
- Session JWT signed with `APP_JWT_SECRET` (your app's own secret, NOT Domo's `JWT_SECRET`)
- 1-hour token lifetime, HttpOnly + Secure + SameSite=Lax cookie
- Two different JWTs in this app: one for your login sessions, one for Domo edit embeds — keep them separate

### Step 2: User Management

Read `references/auth-and-users.md` for full implementation patterns.

Also portal-specific. Build:
- User CRUD API routes with role-based access
- Admin UI component for managing users

**User data model:**

```typescript
interface PortalUser {
  id: string
  username: string
  email?: string
  password: string              // bcrypt hash
  role: 'admin' | 'viewer' | 'editor'
  domoRole?: string             // For edit mode: Admin | Privileged | Editor | Participant
  mappingValue?: string | string[]  // For edit mode: Identity Broker routing
  dashboards: UserDashboard[]   // Assigned embeds with per-user filters
  lastLogin?: string
}

interface UserDashboard {
  embedID: string
  name: string
  filters: DashboardFilter[]
  datasetRedirects?: Record<string, string>
}

interface DashboardFilter {
  column: string
  operator: string
  values: (string | number)[]
  datasourceId?: string
}
```

Each user's `dashboards` array defines what they can see and what filters restrict their data. This feeds directly into the embed token request in Step 4.

Role hierarchy:
- **Admin**: full CRUD on all users, manage dashboard registry, can assign any role
- **Editor**: can create viewers; if edit mode is enabled, can also edit dashboards in Domo
- **Viewer**: view assigned dashboards only, no user management

#### Per-User Filter Configuration UI

The user edit modal must include a filter editor for each assigned dashboard. Without this, filters can only be set by directly editing the database — which means the portal's core data isolation feature has no admin interface.

For each dashboard checkbox that is checked, expand a filter section beneath it where admins can:
- Add filter rules (column name, operator dropdown, comma-separated values)
- Edit existing filter rules inline
- Remove individual filter rules
- See all Domo-supported operators: `EQUALS`, `NOT_EQUALS`, `IN`, `NOT_IN`, `GREATER_THAN`, `LESS_THAN`, `BETWEEN`, `LIKE`

Read `references/auth-and-users.md` for the full filter editor component implementation.

### Step 3: Dashboard Registry

Read `references/auth-and-users.md` for full implementation patterns.

Portal-specific. The list of available dashboards (embed IDs) must be **dynamic, not hardcoded**. Store them in the same data layer as users (AppDB, external DB, etc.) and manage them through the admin UI.

Build:
- Dashboard CRUD API routes (admin-only for create/update/delete, authenticated for list)
- Admin UI for adding new dashboards (name + embed ID), renaming, and deleting
- Sidebar navigation that reads from the dashboard registry dynamically

**Dashboard data model:**

```typescript
interface PortalDashboard {
  id: string       // Document ID from storage
  embedID: string  // Domo embed ID (5-char from embed dialog)
  name: string     // Display name in sidebar and admin UI
}
```

If using AppDB, create a `Dashboards` collection alongside `Users`. The sidebar fetches `GET /api/dashboards` on mount. Admins see all dashboards; non-admin users see only their assigned dashboards (from their `user.dashboards` array).

**Why this matters:** Hardcoding embed IDs means a code change and redeployment every time a dashboard is added or removed. A dynamic registry lets admins self-serve — add a new Domo embed, register it in the portal, and assign it to users, all without touching code.

### Step 4: Read-Only Embeds (if read-only or both)

> **Sub-skill handoff — required, even for focused questions.** The OAuth → embed token flow is owned entirely by `programmatic-filters`. Implementing it here would duplicate a maintained skill and create a second source of truth that drifts over time. The sub-skill has the complete implementation including edge cases, token size limits, SQL filters, and dataset switching that are easy to miss. Users who skip it and follow an inline version often hit production issues. Your response must explicitly name `programmatic-filters` and provide only the portal wiring below.

In your response, tell the user:

> "For the embed token flow (OAuth → access token → embed token → iframe), follow the **`programmatic-filters`** skill. Here's the portal-specific wiring that connects your user data to it:"

Then provide **only** this wiring — nothing from inside the embed token flow itself:

```typescript
// app/api/getembedtoken/route.ts — portal wiring only
// OAuth + embed token implementation: follow programmatic-filters

export async function POST(req: NextRequest) {
  // 1. Verify portal session (Step 1)
  const token = req.cookies.get('token')?.value
  const auth = await verifyToken(token!)
  if (auth.status !== 200) return NextResponse.json({ message: 'Unauthorized' }, { status: auth.status })

  const user = auth.data!.user
  const { embedID } = await req.json()

  // 2. Portal authorization: user must have this dashboard assigned (Step 2 data model)
  //    Admins can access any dashboard in the registry (Step 3)
  const dashboard = user.dashboards?.find((d: any) => d.embedID === embedID)
  if (!dashboard && user.role !== 'admin') {
    return NextResponse.json({ message: 'Dashboard not assigned' }, { status: 403 })
  }

  // 3. Hand off to programmatic-filters with these portal values:
  //    embedID         → authorization[].token
  //    dashboard.filters          → authorization[].filters
  //    dashboard.datasetRedirects → authorization[].datasetRedirects
  // programmatic-filters handles the OAuth call, embed token request, and response format.
}
```

### Step 5: Edit Embeds (if edit or both)

> **Sub-skill handoff — required, even when the user is asking specifically about edit embeds.** The Identity Broker JWT flow is owned entirely by `edit-embed`. This is non-negotiable: do not write `jwt.sign()`, do not construct the IDP URL, do not write the iframe component inline. Here's why this matters — the sub-skill covers replay protection (jti uniqueness), multi-instance routing edge cases, Domo's HS256 requirement, and the session-persistence behaviour after the 5-minute JWT expires. An inline implementation will miss at least some of these. The user needs to follow that skill for a production-safe result. Your value here is providing the portal wiring that connects their user data to it — not reimplementing it.

In your response, tell the user:

> "For the Identity Broker JWT flow (JWT creation, IDP URL, iframe rendering), follow the **`edit-embed`** skill. Here's the portal-specific wiring that connects your user data to it:"

Then provide **only** this wiring — nothing from inside the JWT or iframe flow:

```typescript
// app/api/editembed/route.ts — portal wiring only
// Identity Broker JWT implementation: follow edit-embed

export async function POST(req: NextRequest) {
  // 1. Verify portal session (Step 1)
  const token = req.cookies.get('token')?.value
  const auth = await verifyToken(token!)
  if (auth.status !== 200) return NextResponse.json({ message: 'Unauthorized' }, { status: auth.status })

  const user = auth.data!.user

  // 2. Hand off to edit-embed with these portal values:
  //    user.username / user.email → sub, name, email JWT fields
  //    user.domoRole              → role field (Admin|Privileged|Editor|Participant)
  //    user.mappingValue          → KEY_ATTRIBUTE field (split comma-separated → array)
  // edit-embed handles jwt.sign(), IDP URL construction, and iframe rendering.
  // Sign with JWT_SECRET (Domo's secret) — NOT APP_JWT_SECRET (your login sessions secret).
}
```

This step also has a critical distinction to flag to the user: **two secrets, two purposes** — `APP_JWT_SECRET` signs your portal login sessions (Step 1), `JWT_SECRET` signs Domo Identity Broker tokens (this step). They must never be swapped.

### Step 6: Client-Side Interactivity (optional)

> **Sub-skill handoff — required.** The MessagePort setup, filter API, and event handling are owned entirely by `jsapi-filters`. Implementing them here would duplicate that skill. Your job is only the portal mounting pattern.

In your response, tell the user:

> "For the JS API (MessagePort setup, filter application, drill events, iframe resize), follow the **`jsapi-filters`** skill. Here's how to mount it in the portal:"

Then provide **only** the mounting pattern:

```tsx
// app/layout.tsx — mount before any Domo iframe loads
// Full JS API implementation: follow jsapi-filters

import DomoJsApiInitializer from './components/DomoJsApiInitializer'

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <DomoJsApiInitializer /> {/* Must be in root layout, before iframes render */}
        {children}
      </body>
    </html>
  )
}
```

Common portal patterns to mention (jsapi-filters implements all of these):
- Filter bar above the embed → `applyFilters()` from the sub-skill
- Drill in one embed → filters another via `applyFiltersToEmbed(referenceId, ...)`
- iframe auto-resize → `onFrameSizeChange` event in the sub-skill

### Step 7: Apply Branding

With the functional pieces in place, apply the brand guidelines collected in Phase 1:

**Tailwind config:**
```typescript
export default {
  theme: {
    extend: {
      colors: {
        primary: '{user_primary}',
        secondary: '{user_secondary}',
        accent: '{user_accent}',
      },
      fontFamily: {
        sans: ['{user_font}', ...defaultTheme.fontFamily.sans],
      },
    },
  },
}
```

Apply brand colors to header, sidebar, buttons, forms, and the login page. Use the logo in the header and login page. The dashboards are the main content — the portal chrome should frame them, not compete.

---

## Combining Read-Only and Edit Mode

If the user chose "both" modes, tell them to build a single `EmbedDashboard` component with two branches:

- **Read-only branch**: follows `programmatic-filters` (POST form → iframe)
- **Edit branch**: follows `edit-embed` (direct iframe `src` → Identity Broker URL)

The only portal-specific wiring is detecting which mode to use based on the dashboard assignment:

```tsx
// EmbedDashboard.tsx — mode detection only; each branch follows its sub-skill
const isEditMode = dashboard.isEditable // flag on the UserDashboard object
const endpoint = isEditMode ? '/api/editembed' : '/api/getembedtoken'
// Read-only rendering: follow programmatic-filters
// Edit rendering: follow edit-embed
```

---

## Password Reset

If using AppDB or an external DB (not a third-party auth provider), implement password reset. Read `references/auth-and-users.md` for the implementation pattern including rate limiting.

---

## Security Checklist

Before production:

- [ ] All secrets in env vars, never in client-side code
- [ ] Passwords hashed with bcrypt (10+ salt rounds)
- [ ] Session tokens in HttpOnly cookies (not localStorage)
- [ ] Embed tokens generated server-side only
- [ ] Admin routes protected by middleware
- [ ] Programmatic filters enforced server-side (client-side filters are UX only)
- [ ] Edit JWT tokens short-lived (5 minutes)
- [ ] Rate limiting on login and password reset endpoints

---

## Deployment

Common options:

- **Vercel / Netlify** — easiest for Next.js
- **Docker** — Node.js Alpine image for on-prem or cloud VMs
- **Domo Code Engine** — keeps everything in Domo (check current limitations)

```dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./
ENV NODE_ENV=production
CMD ["npm", "start"]
```
