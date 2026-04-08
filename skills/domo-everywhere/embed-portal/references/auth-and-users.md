# Authentication, User Management & Dashboard Registry

Detailed implementation patterns for login, session management, user CRUD, dashboard management, and per-user filter configuration. Choose the approach that matches your user management decision.

## Table of Contents
- [Domo AppDB Approach](#domo-appdb-approach)
- [External Database Approach](#external-database-approach)
- [Third-Party Auth Approach](#third-party-auth-approach)
- [Login API Route](#login-api-route)
- [Session Verification](#session-verification)
- [User CRUD API](#user-crud-api)
- [Password Reset](#password-reset)
- [Route Protection Middleware](#route-protection-middleware)
- [Dashboard Registry API](#dashboard-registry-api)
- [Admin Panel: Dashboard Management UI](#admin-panel-dashboard-management-ui)
- [Admin Panel: Per-User Filter Editor](#admin-panel-per-user-filter-editor)
- [Dynamic Sidebar Navigation](#dynamic-sidebar-navigation)

---

## Domo AppDB Approach

AppDB is a document store built into Domo — no infrastructure to manage. Each "collection" holds JSON documents keyed by ID.

### Setup

1. In Domo, go to **Admin > Auth > Developer Tokens** and create a token
2. Create collections for your data (Users, EmbedIds, LoginLogs, etc.) via the AppDB API or Domo UI
3. Store the collection IDs in your constants file

### AppDB CRUD Wrapper

```typescript
// lib/domoAppDb.ts
const BASE_URL = process.env.DOMO_APPDB_BASE_URL
const TOKEN = process.env.APPDB_TOKEN

// Collection keys map to UUIDs — store these in constants
const COLLECTIONS: Record<string, string> = {
  Users: 'your-collection-uuid',
  EmbedIds: 'your-collection-uuid',
  LoginLogs: 'your-collection-uuid',
}

async function appDbFetch(path: string, options: RequestInit = {}) {
  const res = await fetch(`${BASE_URL}/api/datastores/v1/collections/${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      'X-DOMO-Developer-Token': TOKEN!,
      ...options.headers,
    },
  })
  if (!res.ok) throw new Error(`AppDB ${res.status}: ${await res.text()}`)
  return res.json()
}

export async function listDocuments(collectionKey: string) {
  const id = COLLECTIONS[collectionKey]
  const data = await appDbFetch(`${id}/documents/`)
  // AppDB wraps content — unwrap it
  // Spread content first, then id — AppDB's doc.id always wins as the identifier
  return data.map((doc: any) => ({ ...doc.content, id: doc.id }))
}

export async function getDocument(collectionKey: string, docId: string) {
  const id = COLLECTIONS[collectionKey]
  const doc = await appDbFetch(`${id}/documents/${docId}`)
  return { ...doc.content, id: doc.id }
}

export async function createDocument(collectionKey: string, content: any) {
  const id = COLLECTIONS[collectionKey]
  return appDbFetch(`${id}/documents/`, {
    method: 'POST',
    body: JSON.stringify({ content }),
  })
}

export async function updateDocument(collectionKey: string, docId: string, content: any) {
  const id = COLLECTIONS[collectionKey]
  return appDbFetch(`${id}/documents/${docId}`, {
    method: 'PUT',
    body: JSON.stringify({ content }),
  })
}

export async function deleteDocument(collectionKey: string, docId: string) {
  const id = COLLECTIONS[collectionKey]
  return appDbFetch(`${id}/documents/${docId}`, { method: 'DELETE' })
}

export async function findByField(collectionKey: string, field: string, value: string) {
  const docs = await listDocuments(collectionKey)
  return docs.find((doc: any) => doc[field]?.toLowerCase() === value.toLowerCase())
}
```

---

## External Database Approach

If using Postgres, MySQL, or similar, replace the AppDB wrapper with your ORM (Prisma, Drizzle, Knex, etc.). The user schema stays the same — just swap the data access layer.

**Prisma example schema:**

```prisma
model User {
  id            String   @id @default(uuid())
  username      String   @unique
  email         String?  @unique
  password      String   // bcrypt hash
  role          String   @default("viewer")
  domoRole      String?
  mappingValue  String?
  dashboards    Json     @default("[]")
  lastLogin     DateTime?
  createdAt     DateTime @default(now())
}
```

The rest of the auth flow (JWT signing, cookie management, route protection) stays identical.

---

## Third-Party Auth Approach

Auth0, Clerk, or Firebase Auth handle the login UI, password hashing, MFA, and password reset for you. Your app still needs:

- A way to store Domo-specific user data (dashboard assignments, filters, roles) — either in the auth provider's metadata or in a separate database
- A session token or cookie that your API routes can verify
- The embed token generation logic (unchanged)

**Clerk + Next.js example:**

```typescript
// middleware.ts — Clerk handles auth
import { clerkMiddleware } from '@clerk/nextjs/server'
export default clerkMiddleware()

// API route — get Domo-specific data from Clerk metadata
import { currentUser } from '@clerk/nextjs/server'

export async function GET() {
  const user = await currentUser()
  const domoConfig = user?.publicMetadata?.domo as DomoUserConfig
  // domoConfig.dashboards, domoConfig.role, etc.
}
```

---

## Login API Route

**Next.js App Router (AppDB example):**

```typescript
// app/api/login/route.ts
import { NextRequest, NextResponse } from 'next/server'
import bcrypt from 'bcryptjs'
import jwt from 'jsonwebtoken'
import { findByField, updateDocument } from '@/lib/domoAppDb'

export async function POST(req: NextRequest) {
  const { username, password } = await req.json()

  if (!username || !password) {
    return NextResponse.json({ message: 'Username and password required' }, { status: 400 })
  }

  // Look up user by username or email (case-insensitive)
  const normalized = username.toLowerCase().trim()
  let user = await findByField('Users', 'username', normalized)
  if (!user) {
    user = await findByField('Users', 'email', normalized)
  }
  if (!user) {
    return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 })
  }

  // Verify password
  const valid = await bcrypt.compare(password, user.password)
  if (!valid) {
    return NextResponse.json({ message: 'Invalid credentials' }, { status: 401 })
  }

  // Update last login
  await updateDocument('Users', user.id, { ...user, lastLogin: new Date().toISOString() })

  // Issue session token
  const token = jwt.sign(
    { id: user.id, role: user.role },
    process.env.APP_JWT_SECRET!,
    { expiresIn: '1h' }
  )

  const response = NextResponse.json({ message: 'Login successful' })
  response.cookies.set('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 3600,
    path: '/',
  })

  return response
}
```

**Express equivalent:**

```typescript
app.post('/api/login', async (req, res) => {
  const { username, password } = req.body
  const user = await findByField('Users', 'username', username.toLowerCase())

  if (!user || !(await bcrypt.compare(password, user.password))) {
    return res.status(401).json({ message: 'Invalid credentials' })
  }

  const token = jwt.sign({ id: user.id, role: user.role }, process.env.APP_JWT_SECRET, {
    expiresIn: '1h',
  })

  res.cookie('token', token, { httpOnly: true, secure: true, sameSite: 'lax', maxAge: 3600000 })
  res.json({ message: 'Login successful' })
})
```

---

## Session Verification

Reusable helper to verify the session token and look up the user:

```typescript
// lib/verifyToken.ts
import jwt from 'jsonwebtoken'
import { getDocument } from '@/lib/domoAppDb'

interface TokenPayload {
  id: string
  role: string
}

export async function verifyToken(token: string) {
  try {
    const decoded = jwt.verify(token, process.env.APP_JWT_SECRET!) as TokenPayload
    const user = await getDocument('Users', decoded.id)
    if (!user) return { status: 404, message: 'User not found' }
    return { status: 200, data: { user } }
  } catch (err) {
    return { status: 401, message: 'Invalid or expired token' }
  }
}
```

Use in API routes:

```typescript
const token = req.cookies.get('token')?.value
if (!token) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

const result = await verifyToken(token)
if (result.status !== 200) {
  return NextResponse.json({ message: result.message }, { status: result.status })
}
const user = result.data!.user
```

---

## User CRUD API

### Create User

```typescript
// POST /api/users
export async function POST(req: NextRequest) {
  const token = req.cookies.get('token')?.value
  const auth = await verifyToken(token!)
  if (auth.status !== 200) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const currentUser = auth.data!.user

  // Role-based creation rules
  if (currentUser.role === 'viewer') {
    return NextResponse.json({ message: 'Insufficient permissions' }, { status: 403 })
  }

  const body = await req.json()
  const { username, email, password, role, dashboards } = body

  // Editors can only create viewers
  if (currentUser.role === 'editor' && role !== 'viewer') {
    return NextResponse.json({ message: 'Editors can only create viewers' }, { status: 403 })
  }

  // Check for duplicates
  const existing = await findByField('Users', 'username', username.toLowerCase())
  if (existing) {
    return NextResponse.json({ message: 'Username already exists' }, { status: 409 })
  }

  const hashedPassword = await bcrypt.hash(password, 10)

  const newUser = {
    username: username.toLowerCase(),
    email: email?.toLowerCase(),
    password: hashedPassword,
    role: role || 'viewer',
    dashboards: dashboards || [],
    domoRole: body.domoRole,
    mappingValue: body.mappingValue,
    createdBy: currentUser.id,
  }

  await createDocument('Users', newUser)
  const { password: _, ...safeUser } = newUser
  return NextResponse.json(safeUser, { status: 201 })
}
```

### List Users

```typescript
// GET /api/users
export async function GET(req: NextRequest) {
  const token = req.cookies.get('token')?.value
  const auth = await verifyToken(token!)
  if (auth.status !== 200) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const currentUser = auth.data!.user
  let users = await listDocuments('Users')

  // Non-admins only see users they created or users in their scope
  if (currentUser.role !== 'admin') {
    users = users.filter((u: any) => u.createdBy === currentUser.id || u.id === currentUser.id)
  }

  // Strip passwords from response
  return NextResponse.json(users.map(({ password, ...u }: any) => u))
}
```

### Update and Delete

Follow the same pattern — verify auth, check role permissions, perform the operation. Admins can update/delete anyone; editors can only manage users they created; viewers cannot manage users.

---

## Password Reset

### Rate Limiting (in-memory, single instance)

```typescript
const ipLimits = new Map<string, { count: number; resetAt: number }>()
const emailLimits = new Map<string, { count: number; resetAt: number }>()

function checkRateLimit(
  map: Map<string, { count: number; resetAt: number }>,
  key: string,
  maxRequests: number,
  windowMs: number
): boolean {
  const now = Date.now()
  const entry = map.get(key)

  if (!entry || now > entry.resetAt) {
    map.set(key, { count: 1, resetAt: now + windowMs })
    return true
  }

  if (entry.count >= maxRequests) return false
  entry.count++
  return true
}
```

### Reset Flow

```typescript
// POST /api/password-reset — initiate
// 1. Rate-limit by IP (100/15min) and email (5/1hr)
// 2. Find user by email
// 3. Generate a reset code (UUID or random token)
// 4. Store the code with expiration (e.g., 15 minutes)
// 5. Send email with reset link (via Domo Workflow, SendGrid, etc.)

// POST /api/password-reset/complete — verify and update
// 1. Validate the reset code exists and hasn't expired
// 2. Hash the new password with bcrypt
// 3. Update the user's password
// 4. Delete the reset code
```

---

## Route Protection Middleware

**Next.js middleware example:**

```typescript
// middleware.ts
import { NextRequest, NextResponse } from 'next/server'
import { jwtVerify } from 'jose'

const protectedPaths = ['/home', '/api/users', '/api/getembedtoken', '/api/editembed']
const adminPaths = ['/api/admin']

export async function middleware(req: NextRequest) {
  const path = req.nextUrl.pathname

  const isProtected = protectedPaths.some(p => path.startsWith(p))
  const isAdmin = adminPaths.some(p => path.startsWith(p))

  if (!isProtected && !isAdmin) return NextResponse.next()

  const token = req.cookies.get('token')?.value
  if (!token) {
    return path.startsWith('/api')
      ? NextResponse.json({ message: 'Unauthorized' }, { status: 401 })
      : NextResponse.redirect(new URL('/login', req.url))
  }

  try {
    const secret = new TextEncoder().encode(process.env.APP_JWT_SECRET)
    const { payload } = await jwtVerify(token, secret)

    if (isAdmin && payload.role !== 'admin') {
      return NextResponse.json({ message: 'Forbidden' }, { status: 403 })
    }

    return NextResponse.next()
  } catch {
    return path.startsWith('/api')
      ? NextResponse.json({ message: 'Invalid token' }, { status: 401 })
      : NextResponse.redirect(new URL('/login', req.url))
  }
}

export const config = {
  matcher: ['/home/:path*', '/api/:path*'],
}
```

---

## Dashboard Registry API

The dashboard registry stores the list of available embed IDs. Any authenticated user can list dashboards; only admins can create, rename, or delete them.

If using AppDB, add a `Dashboards` collection alongside `Users` in your constants:

```typescript
export const COLLECTIONS: Record<string, string> = {
  Users: 'your-users-collection-uuid',
  Dashboards: 'your-dashboards-collection-uuid',
}
```

### List and Create Dashboards

```typescript
// app/api/dashboards/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { verifyToken } from '@/lib/verifyToken'
import { listDocuments, createDocument, findByField } from '@/lib/domoAppDb'

export async function GET(req: NextRequest) {
  const token = req.cookies.get('token')?.value
  if (!token) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const auth = await verifyToken(token)
  if (auth.status !== 200) return NextResponse.json({ message: auth.message }, { status: auth.status })

  const dashboards = await listDocuments('Dashboards')
  return NextResponse.json(dashboards)
}

export async function POST(req: NextRequest) {
  const token = req.cookies.get('token')?.value
  if (!token) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const auth = await verifyToken(token)
  if (auth.status !== 200) return NextResponse.json({ message: auth.message }, { status: auth.status })
  if (auth.data!.user.role !== 'admin') {
    return NextResponse.json({ message: 'Forbidden' }, { status: 403 })
  }

  const { embedID, name } = await req.json()
  if (!embedID || !name) {
    return NextResponse.json({ message: 'embedID and name are required' }, { status: 400 })
  }

  const existing = await findByField('Dashboards', 'embedID', embedID)
  if (existing) {
    return NextResponse.json({ message: 'Dashboard with this embed ID already exists' }, { status: 409 })
  }

  const result = await createDocument('Dashboards', { embedID, name })
  return NextResponse.json({ id: result.id, embedID, name }, { status: 201 })
}
```

### Rename and Delete a Dashboard

```typescript
// app/api/dashboards/[id]/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { verifyToken } from '@/lib/verifyToken'
import { deleteDocument, updateDocument } from '@/lib/domoAppDb'

export async function PUT(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const token = req.cookies.get('token')?.value
  if (!token) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const auth = await verifyToken(token)
  if (auth.status !== 200) return NextResponse.json({ message: auth.message }, { status: auth.status })
  if (auth.data!.user.role !== 'admin') return NextResponse.json({ message: 'Forbidden' }, { status: 403 })

  const { embedID, name } = await req.json()
  if (!embedID || !name) {
    return NextResponse.json({ message: 'embedID and name are required' }, { status: 400 })
  }

  await updateDocument('Dashboards', id, { embedID, name })
  return NextResponse.json({ id, embedID, name })
}

export async function DELETE(req: NextRequest, { params }: { params: Promise<{ id: string }> }) {
  const { id } = await params
  const token = req.cookies.get('token')?.value
  if (!token) return NextResponse.json({ message: 'Unauthorized' }, { status: 401 })

  const auth = await verifyToken(token)
  if (auth.status !== 200) return NextResponse.json({ message: auth.message }, { status: auth.status })
  if (auth.data!.user.role !== 'admin') return NextResponse.json({ message: 'Forbidden' }, { status: 403 })

  await deleteDocument('Dashboards', id)
  return NextResponse.json({ message: 'Dashboard deleted' })
}
```

---

## Admin Panel: Dashboard Management UI

Build a tabbed admin page with **Users** and **Dashboards** tabs. The Dashboards tab provides a table of registered dashboards with add, rename, and delete actions.

### Dashboard Table

Display each dashboard's name and embed ID. Actions column includes Rename and Delete buttons.

```tsx
// Inside the admin page component — Dashboards tab content

const [dashboards, setDashboards] = useState<Dashboard[]>([])
const [showAddDashboard, setShowAddDashboard] = useState(false)
const [newDashboardName, setNewDashboardName] = useState('')
const [newDashboardEmbedID, setNewDashboardEmbedID] = useState('')
const [renamingDashboard, setRenamingDashboard] = useState<Dashboard | null>(null)
const [renameValue, setRenameValue] = useState('')

const fetchDashboards = async () => {
  const res = await fetch('/api/dashboards', { credentials: 'include' })
  if (res.ok) setDashboards(await res.json())
}

const handleAddDashboard = async (e: React.FormEvent) => {
  e.preventDefault()
  const res = await fetch('/api/dashboards', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ embedID: newDashboardEmbedID, name: newDashboardName }),
    credentials: 'include',
  })
  if (res.ok) {
    setShowAddDashboard(false)
    setNewDashboardName('')
    setNewDashboardEmbedID('')
    fetchDashboards()
  }
}

const handleRenameDashboard = async (e: React.FormEvent) => {
  e.preventDefault()
  if (!renamingDashboard || !renameValue.trim()) return
  const res = await fetch(`/api/dashboards/${renamingDashboard.id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ embedID: renamingDashboard.embedID, name: renameValue.trim() }),
    credentials: 'include',
  })
  if (res.ok) {
    setRenamingDashboard(null)
    setRenameValue('')
    fetchDashboards()
  }
}

const handleDeleteDashboard = async (id: string) => {
  if (!confirm('Delete this dashboard? Users who have it assigned will no longer see it.')) return
  await fetch(`/api/dashboards/${id}`, { method: 'DELETE', credentials: 'include' })
  fetchDashboards()
}
```

### Add Dashboard Modal

Two fields: **Name** (display name) and **Embed ID** (the 5-character ID from Domo's embed dialog). Validate both are non-empty before submitting.

### Rename Dashboard Modal

Pre-populate the current name. Show the embed ID as read-only context (embed IDs don't change — if a user needs a different embed ID, they delete and re-add).

---

## Admin Panel: Per-User Filter Editor

When editing a user, each assigned dashboard should expand to show a filter configuration section. This is the admin interface for the portal's core data isolation feature — without it, `UserDashboard.filters` is always empty and every user sees all data.

### Filter Editor Component

For each dashboard the user is assigned to, render the filter rows beneath the checkbox:

```tsx
// Inside the edit user modal — replace the simple dashboard checkbox list

{dashboards.map(d => {
  const assignedDashboard = editingUser.dashboards?.find(ud => ud.embedID === d.embedID)
  const assigned = !!assignedDashboard
  return (
    <div key={d.embedID} className="rounded-lg border border-white/5 overflow-hidden">
      {/* Dashboard toggle */}
      <label className="flex items-center gap-2 text-sm text-white cursor-pointer px-3 py-2.5 bg-content-bg/50">
        <input
          type="checkbox"
          checked={assigned}
          onChange={() => {
            const updatedDashboards = assigned
              ? editingUser.dashboards.filter(ud => ud.embedID !== d.embedID)
              : [...(editingUser.dashboards || []), { embedID: d.embedID, name: d.name, filters: [] }]
            setEditingUser({ ...editingUser, dashboards: updatedDashboards })
          }}
        />
        {d.name} <span className="text-gray-500 text-xs font-mono">({d.embedID})</span>
      </label>

      {/* Filter editor — only shown when dashboard is assigned */}
      {assigned && (
        <div className="px-3 py-2 border-t border-white/5 space-y-2">
          <p className="text-xs text-gray-500">
            Filters restrict what data this user sees on this dashboard.
          </p>

          {/* Existing filter rows */}
          {(assignedDashboard.filters || []).map((f, fi) => (
            <div key={fi} className="flex items-center gap-1.5">
              <input
                type="text"
                value={f.column}
                onChange={e => {
                  const filters = [...assignedDashboard.filters]
                  filters[fi] = { ...filters[fi], column: e.target.value }
                  const updatedDashboards = editingUser.dashboards.map(ud =>
                    ud.embedID === d.embedID ? { ...ud, filters } : ud
                  )
                  setEditingUser({ ...editingUser, dashboards: updatedDashboards })
                }}
                placeholder="Column"
                className="w-24 px-2 py-1 bg-content-bg border border-white/10 rounded text-xs"
              />
              <select
                value={f.operator}
                onChange={e => {
                  const filters = [...assignedDashboard.filters]
                  filters[fi] = { ...filters[fi], operator: e.target.value }
                  const updatedDashboards = editingUser.dashboards.map(ud =>
                    ud.embedID === d.embedID ? { ...ud, filters } : ud
                  )
                  setEditingUser({ ...editingUser, dashboards: updatedDashboards })
                }}
                className="w-20 px-1.5 py-1 bg-content-bg border border-white/10 rounded text-xs"
              >
                <option value="EQUALS">EQUALS</option>
                <option value="NOT_EQUALS">NOT_EQUALS</option>
                <option value="IN">IN</option>
                <option value="NOT_IN">NOT_IN</option>
                <option value="GREATER_THAN">GREATER_THAN</option>
                <option value="LESS_THAN">LESS_THAN</option>
                <option value="BETWEEN">BETWEEN</option>
                <option value="LIKE">LIKE</option>
              </select>
              <input
                type="text"
                value={f.values.join(', ')}
                onChange={e => {
                  const filters = [...assignedDashboard.filters]
                  filters[fi] = {
                    ...filters[fi],
                    values: e.target.value.split(',').map(v => v.trim()).filter(Boolean)
                  }
                  const updatedDashboards = editingUser.dashboards.map(ud =>
                    ud.embedID === d.embedID ? { ...ud, filters } : ud
                  )
                  setEditingUser({ ...editingUser, dashboards: updatedDashboards })
                }}
                placeholder="Values (comma-separated)"
                className="flex-1 px-2 py-1 bg-content-bg border border-white/10 rounded text-xs"
              />
              <button
                type="button"
                onClick={() => {
                  const filters = assignedDashboard.filters.filter((_, i) => i !== fi)
                  const updatedDashboards = editingUser.dashboards.map(ud =>
                    ud.embedID === d.embedID ? { ...ud, filters } : ud
                  )
                  setEditingUser({ ...editingUser, dashboards: updatedDashboards })
                }}
              >
                ✕
              </button>
            </div>
          ))}

          {/* Add filter button */}
          <button
            type="button"
            onClick={() => {
              const filters = [
                ...(assignedDashboard.filters || []),
                { column: '', operator: 'EQUALS', values: [] }
              ]
              const updatedDashboards = editingUser.dashboards.map(ud =>
                ud.embedID === d.embedID ? { ...ud, filters } : ud
              )
              setEditingUser({ ...editingUser, dashboards: updatedDashboards })
            }}
            className="text-xs text-accent hover:text-accent-hover"
          >
            + Add filter
          </button>
        </div>
      )}
    </div>
  )
})}
```

### How It Connects

The filters saved here flow through the embed token request automatically:

1. Admin sets filter `Region = "West"` on Dashboard 1 for a user
2. User logs in, navigates to Dashboard 1
3. `GET /api/getembedtoken` reads `user.dashboards[].filters`
4. Filters are passed to the Domo embed token request (see `programmatic-filters` skill)
5. Domo enforces the filter server-side — the user only sees West region data

Empty filters (`[]`) means no restrictions — the user sees all data on that dashboard.

---

## Dynamic Sidebar Navigation

The authenticated layout must build the sidebar from dynamic data, not hardcoded embed IDs.

```tsx
// app/home/layout.tsx — relevant state and fetch logic

const [user, setUser] = useState<User | null>(null)
const [allDashboards, setAllDashboards] = useState<Dashboard[]>([])

useEffect(() => {
  fetch('/api/me', { credentials: 'include' })
    .then(res => res.ok ? res.json() : Promise.reject())
    .then(setUser)
    .catch(() => router.push('/login'))
}, [])

useEffect(() => {
  fetch('/api/dashboards', { credentials: 'include' })
    .then(res => res.ok ? res.json() : [])
    .then(setAllDashboards)
    .catch(() => {})
}, [])

// Admins see all registered dashboards; others see only their assignments
const dashboards = user?.role === 'admin'
  ? allDashboards.map(d => ({ embedID: d.embedID, name: d.name }))
  : user?.dashboards?.map(d => ({ embedID: d.embedID, name: d.name })) || []
```

Each dashboard entry renders as a sidebar link to `/home/{embedID}`. The `[embedId]/page.tsx` route handles fetching the embed token and rendering the iframe.
