---
name: migrate-lovable
description: Convert SSR-heavy Lovable/v0 apps into client-only Domo apps.
---

# Migrating Lovable to Domo

## Converting Generated Apps (Lovable/v0) to Domo

Many developers use AI tools like Lovable, v0, or similar LLM-based generators to create app prototypes. However, these tools typically generate apps with server-side rendering (SSR) that are **incompatible with Domo's client-side-only architecture**.

### The Conversion Challenge

Generated apps often include:
- **Server-side rendering** (Next.js, Remix, SvelteKit, Nuxt)
- **API routes** (`pages/api/` or `app/api/` directories)
- **Server-side data fetching** (`getServerSideProps`, loaders, etc.)
- **Framework-specific routing** (Next.js App Router, Remix routes)

Domo apps must be:
- **Pure client-side React** - No server rendering
- **Static file-based** - Domo serves static files only
- **Domo API integration** - Use `domo.get()`, `Query`, `AppDBClient`, etc. instead of backend endpoints

### Recommended Conversion Pattern

**DA CLI is NOT a conversion tool** - it doesn't automatically convert apps. However, you can use it as a reference structure and starting point.

#### Step 1: Generate Reference Structure

```bash
# Create a fresh Domo app to use as reference
da new my-converted-app
cd my-converted-app

# This gives you the correct structure to compare against
```

#### Step 2: Detect and Remove SSR Code

**Check for SSR indicators:**
- `getServerSideProps`, `getStaticProps` (Next.js)
- `loader`, `action` functions (Remix)
- `+page.server.js`, `+server.js` (SvelteKit)
- `pages/api/` or `app/api/` directories
- Server-side `process.env` usage
- Database connections in components

**Action:** Remove all server-side code. Domo apps run entirely in the browser.

#### Step 3: Replace Data Fetching

**Before (Next.js example):**
```typescript
// ❌ Server-side data fetching
export async function getServerSideProps() {
  const res = await fetch('https://api.example.com/data');
  const data = await res.json();
  return { props: { data } };
}

// ❌ API route
// pages/api/users.ts
export default async function handler(req, res) {
  const users = await db.users.findMany();
  res.json(users);
}
```

**After (Domo):**
```typescript
// ✅ Client-side with Domo APIs
import domo from 'ryuu.js';
import Query from '@domoinc/query';
import { AppDBClient } from '@domoinc/toolkit';

// Fetch from Domo dataset
const data = await domo.get('/data/v1/sales');

// Or use Query API for filtered/aggregated data
const summary = await new Query()
  .select(['region', 'sales'])
  .groupBy('region', { sales: 'sum' })
  .fetch('sales-dataset');

// Or use AppDB for document storage
const tasksClient = new AppDBClient.DocumentsClient('Tasks');
const tasks = await tasksClient.get();
```

#### Step 4: Update Routing

**Before (Next.js):**
```typescript
// ❌ Next.js routing
import Link from 'next/link';
<Link href="/dashboard">Dashboard</Link>
```

**After (Domo):**
```typescript
// ✅ HashRouter for client-side routing
import { HashRouter, Routes, Route } from 'react-router-dom';
import domo from 'ryuu.js';

// Use HashRouter (works without server rewrites)
<HashRouter>
  <Routes>
    <Route path="/" element={<Home />} />
    <Route path="/dashboard" element={<Dashboard />} />
  </Routes>
</HashRouter>

// For Domo navigation, use domo.navigate()
domo.navigate('/page/123456789');
```

#### Step 5: Fix Build Configuration

**Before (Next.js):**
```javascript
// next.config.js
module.exports = {
  // Next.js config
}
```

**After (Domo - Vite):**
```javascript
// vite.config.js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: './',  // CRITICAL: Relative paths for Domo
  plugins: [react()],
});
```

**Remove Lovable-specific Vite plugins** like `lovable-tagger`:
```javascript
// ❌ Remove this
import { componentTagger } from "lovable-tagger";
plugins: [react(), mode === "development" && componentTagger()].filter(Boolean),

// ✅ Replace with
plugins: [react()],
```

#### Step 6: Remove Lovable-Specific Dependencies

Lovable/v0 apps include tooling that must be removed:

**Dependencies to remove:**
- `next-themes` — SSR theme provider; replace `useTheme()` with a hardcoded theme string (e.g. `"light"`)
- `lovable-tagger` — Lovable's dev-only component tagger

**Files to delete:**
- `playwright.config.ts` — Uses `lovable-agent-playwright-config`
- `playwright-fixture.ts` — Re-exports Lovable test fixtures
- `bun.lock` / `bun.lockb` — Lovable uses Bun; standardize on npm
- `App.css` — Often unused in generated apps (verify first)

**Fix `next-themes` usage in Sonner toaster:**
```typescript
// ❌ Before (depends on next-themes)
import { useTheme } from "next-themes";
const { theme = "system" } = useTheme();
<Sonner theme={theme as ToasterProps["theme"]} />

// ✅ After (hardcoded, no SSR dependency)
<Sonner theme="light" />
```

#### Step 7: Create Domo Manifest

Domo requires a `manifest.json` in the publish directory:

```json
{
  "name": "My App Name",
  "version": "1.0.0",
  "size": {
    "width": 10,
    "height": 10
  },
  "mapping": [],
  "fileName": "index.html",
  "id": "",
  "proxyId": ""
}
```

- `name` — Display name in Domo
- `size` — Card dimensions (columns x rows on the Domo dashboard grid)
- `mapping` — Dataset mappings (empty array if using mock data or AppDB)
- `fileName` — Entry HTML file (always `index.html`)
- `id` — Leave empty; `domo publish` fills this on first publish

#### Step 8: Create Thumbnail

**REQUIRED** — `domo publish` will fail without this.

Place a **300x300 PNG** named `thumbnail.png` in the project root. This is used in the Domo Appstore and mobile app.

```bash
# Generate a simple thumbnail programmatically (Python + Pillow)
python3 -c "
from PIL import Image, ImageDraw, ImageFont
img = Image.new('RGB', (300, 300), color=(15, 23, 42))
draw = ImageDraw.Draw(img)
draw.rectangle([0, 0, 300, 6], fill=(99, 102, 241))
try:
    font = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 72)
except: font = ImageFont.load_default()
bbox = draw.textbbox((0, 0), 'EF', font=font)
draw.text(((300-(bbox[2]-bbox[0]))/2, 110), 'EF', fill='white', font=font)
img.save('thumbnail.png')
"
```

Or use any 300x300 PNG image.

#### Step 9: Publish from `dist/` Directory

**CRITICAL** — Running `domo publish` from the project root causes a `400: Unable to parse form content` error because the CLI tries to upload `node_modules`, source files, and config files, creating an oversized payload.

**Solution:** Copy `manifest.json` and `thumbnail.png` into `dist/`, then publish from there:

```bash
# Manual publish
npm run build
cp manifest.json thumbnail.png dist/
cd dist && domo publish
```

**Automate it** by updating `package.json` scripts:
```json
{
  "scripts": {
    "build": "vite build && cp manifest.json thumbnail.png dist/",
    "publish": "npm run build && cd dist && domo publish"
  }
}
```

This ensures only built assets, the manifest, and thumbnail are uploaded.

#### Step 10: Port Components

Use DA CLI to generate new components with correct structure, then port logic:

```bash
# Generate component structure
da generate component SalesChart

# Copy component logic from generated app
# Replace data fetching with Domo APIs
# Update imports and dependencies
```

### What DA CLI Helps With

✅ **Reference structure** - Shows correct Domo app organization  
✅ **Component generation** - Creates properly structured components  
✅ **Pattern examples** - Demonstrates Domo conventions  
✅ **Starting fresh** - If conversion is too complex, start new and port logic  

### What DA CLI Doesn't Do

❌ **No automatic conversion** - Doesn't transform SSR to client-side  
❌ **No migration wizard** - No step-by-step conversion tool  
❌ **No code transformation** - Doesn't rewrite framework-specific code  
❌ **No API migration** - Doesn't replace backend calls automatically  

### Complete Conversion Checklist

- [ ] Detect and remove all SSR code
- [ ] Remove API routes (`pages/api/`, `app/api/`)
- [ ] Replace `fetch()` calls to backend with Domo APIs
- [ ] Update routing from `BrowserRouter` to `HashRouter`
- [ ] Configure Vite with `base: './'`
- [ ] Remove Lovable-specific plugins (`lovable-tagger`) from Vite config
- [ ] Remove `next-themes` and replace `useTheme()` with hardcoded theme
- [ ] Delete Lovable files (`playwright.config.ts`, `playwright-fixture.ts`, `bun.lock*`)
- [ ] Add `ryuu.js` dependency for Domo API integration
- [ ] Replace environment variables (use Domo APIs instead)
- [ ] Update imports (remove Next.js/Remix/Lovable specific)
- [ ] Create `manifest.json` with app name, version, and size
- [ ] Create `thumbnail.png` (300x300 PNG) in project root
- [ ] Update build script to copy `manifest.json` + `thumbnail.png` into `dist/`
- [ ] Test all data fetching works with Domo APIs
- [ ] Verify app builds and runs locally (`npm run build`)
- [ ] Publish from `dist/` directory (`cd dist && domo publish`)

### Example: Converting a Simple Dashboard

**Original (Lovable/Next.js):**
```typescript
// pages/dashboard.tsx
export async function getServerSideProps() {
  const sales = await fetch('http://api.company.com/sales').then(r => r.json());
  return { props: { sales } };
}

export default function Dashboard({ sales }) {
  return <div>{/* Render sales data */}</div>;
}
```

**Converted (Domo):**
```typescript
// src/components/Dashboard/Dashboard.tsx
import { useEffect, useState } from 'react';
import domo from 'ryuu.js';

export default function Dashboard() {
  const [sales, setSales] = useState([]);

  useEffect(() => {
    // Fetch from Domo dataset instead of backend
    domo.get('/data/v1/sales').then(setSales);
  }, []);

  return <div>{/* Render sales data */}</div>;
}
```
