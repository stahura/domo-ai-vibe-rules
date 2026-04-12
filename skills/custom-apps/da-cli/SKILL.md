---
name: da-cli
description: Advanced DA CLI usage for scaffolding, generation, and manifest instances.
---

# @domoinc/da CLI - App Scaffolding and Code Generation

The DA CLI (`@domoinc/da`) is a command-line tool for scaffolding Domo custom apps and generating boilerplate code. It's the **recommended way** to create new Domo apps and generate components.

## Purpose

DA CLI provides:
- **Project scaffolding** - Creates new Domo apps with correct structure (Vite + React 18 + TypeScript)
- **Code generation** - Generates components, reducers, and other boilerplate with proper Domo patterns
- **Manifest management** - Manages environment-specific manifest configurations
- **Best practices** - Ensures projects follow Domo conventions from the start

## Installation

```bash
# Install globally
pnpm add -g @domoinc/da

# Or with npm
npm install -g @domoinc/da
```

## Creating a New App

```bash
# Create new Domo app (recommended - Vite + React 18 + TypeScript)
da new my-app-name
cd my-app-name

# With custom template
da new my-app --template @myorg/custom-template
da new my-app --template github.com/user/repo
da new my-app --template ./local-template
```

**Project Structure Created:**
```
my-app/
├── public/
│   ├── manifest.json      # Domo app configuration
│   └── thumbnail.png      # App icon in Domo
├── src/
│   ├── components/        # React components
│   ├── reducers/          # Redux slices (if using)
│   ├── services/          # API service layers
│   ├── types/             # TypeScript definitions
│   └── index.tsx          # App entry point
├── package.json
└── vite.config.ts
```

## Code Generation

```bash
# Generate component with styles, tests, and Storybook
da generate component MyComponent
# Creates:
#   src/components/MyComponent/MyComponent.tsx
#   src/components/MyComponent/MyComponent.module.scss
#   src/components/MyComponent/MyComponent.test.tsx
#   src/components/MyComponent/MyComponent.stories.tsx

# Shorthand
da g component MyComponent

# Generate Redux slice (auto-imports to store)
da generate reducer myFeature
# Creates: src/reducers/myFeature/slice.ts

# Shorthand
da g reducer myFeature
```

## Manifest Management

DA CLI helps manage multiple Domo environments (dev, staging, prod):

```bash
# Create environment-specific manifest overrides
da manifest instance.prod "Production on customer.domo.com"
da manifest instance.dev "Development on dev.domo.com"

# Apply an override before publishing
da apply-manifest instance.prod
yarn upload
```

**Override file structure:**
```json
{
  "instance.prod": {
    "description": "Production environment",
    "manifest": {
      "id": "prod-app-design-id",
      "proxyId": "prod-card-id"
    }
  }
}
```

---

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

#### Step 6: Port Components

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
- [ ] Update routing to `HashRouter`
- [ ] Configure Vite with `base: './'`
- [ ] Replace environment variables (use Domo APIs instead)
- [ ] Update imports (remove Next.js/Remix specific)
- [ ] Test all data fetching works with Domo APIs
- [ ] Verify app builds and runs locally
- [ ] Publish to Domo and test in platform

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



---

## Additional Reference: CODE_BLOCKS_DA_CLI.md

# Code Blocks to Add: DA CLI and Conversion Guide

Add this section after the "Build & Deploy Workflow" section and before "Base Path Configuration".

---

## @domoinc/da CLI - App Scaffolding and Code Generation

The DA CLI (`@domoinc/da`) is a command-line tool for scaffolding Domo custom apps and generating boilerplate code. It's the **recommended way** to create new Domo apps and generate components.

### Purpose

DA CLI provides:
- **Project scaffolding** - Creates new Domo apps with correct structure (Vite + React 18 + TypeScript)
- **Code generation** - Generates components, reducers, and other boilerplate with proper Domo patterns
- **Manifest management** - Manages environment-specific manifest configurations
- **Best practices** - Ensures projects follow Domo conventions from the start

### Installation

```bash
# Install globally
pnpm add -g @domoinc/da

# Or with npm
npm install -g @domoinc/da
```

### Creating a New App

```bash
# Create new Domo app (recommended - Vite + React 18 + TypeScript)
da new my-app-name
cd my-app-name

# With custom template
da new my-app --template @myorg/custom-template
da new my-app --template github.com/user/repo
da new my-app --template ./local-template
```

**Project Structure Created:**
```
my-app/
├── public/
│   ├── manifest.json      # Domo app configuration
│   └── thumbnail.png      # App icon in Domo
├── src/
│   ├── components/        # React components
│   ├── reducers/          # Redux slices (if using)
│   ├── services/          # API service layers
│   ├── types/             # TypeScript definitions
│   └── index.tsx          # App entry point
├── package.json
└── vite.config.ts
```

### Code Generation

```bash
# Generate component with styles, tests, and Storybook
da generate component MyComponent
# Creates:
#   src/components/MyComponent/MyComponent.tsx
#   src/components/MyComponent/MyComponent.module.scss
#   src/components/MyComponent/MyComponent.test.tsx
#   src/components/MyComponent/MyComponent.stories.tsx

# Shorthand
da g component MyComponent

# Generate Redux slice (auto-imports to store)
da generate reducer myFeature
# Creates: src/reducers/myFeature/slice.ts

# Shorthand
da g reducer myFeature
```

### Manifest Management

DA CLI helps manage multiple Domo environments (dev, staging, prod):

```bash
# Create environment-specific manifest overrides
da manifest instance.prod "Production on customer.domo.com"
da manifest instance.dev "Development on dev.domo.com"

# Apply an override before publishing
da apply-manifest instance.prod
yarn upload
```

**Override file structure:**
```json
{
  "instance.prod": {
    "description": "Production environment",
    "manifest": {
      "id": "prod-app-design-id",
      "proxyId": "prod-card-id"
    }
  }
}
```

---

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

#### Step 6: Port Components

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
- [ ] Update routing to `HashRouter`
- [ ] Configure Vite with `base: './'`
- [ ] Replace environment variables (use Domo APIs instead)
- [ ] Update imports (remove Next.js/Remix specific)
- [ ] Test all data fetching works with Domo APIs
- [ ] Verify app builds and runs locally
- [ ] Publish to Domo and test in platform

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

---



---

## Additional Reference: PR_DA_CLI_DESCRIPTION.md

# Add DA CLI Documentation and Lovable/v0 Conversion Guide

## Summary

This PR adds comprehensive documentation for the `@domoinc/da` CLI tool and a guide for converting Lovable/v0 (or similar LLM-generated) apps to functioning Domo apps.

## What's Added

1. **DA CLI Documentation**
   - Purpose and capabilities of the DA CLI
   - Installation and setup
   - Code generation commands (components, reducers)
   - Manifest management for multiple environments
   - Project structure overview

2. **Converting Generated Apps Guide**
   - Step-by-step process for converting Lovable/v0 apps to Domo
   - Recommended pattern using DA CLI as reference
   - Common incompatibilities and how to fix them
   - Data fetching migration patterns
   - Routing and build configuration updates

## Why This Matters

Many developers use AI tools like Lovable or v0 to generate app prototypes, but these tools create Next.js/Remix apps with server-side rendering that are incompatible with Domo's client-side-only architecture. This guide provides a clear path for conversion.

## Key Highlights

- **DA CLI Purpose**: Explains that DA CLI is a scaffolding tool, not a conversion tool, but can be used as a reference structure
- **Conversion Pattern**: Step-by-step guide for manually porting components and logic
- **SSR Detection**: Reinforces the importance of detecting and removing server-side code
- **API Migration**: Clear patterns for replacing backend calls with Domo APIs

## Location

Added after the "Build & Deploy Workflow" section, before "Base Path Configuration".



---

## Additional Reference: PR_DA_CLI_SUGGESTIONS.md

# PR Suggestions: DA CLI Documentation and Conversion Guide

## Overview

This PR adds documentation for the `@domoinc/da` CLI tool and a comprehensive guide for converting Lovable/v0 (or similar LLM-generated) apps to functioning Domo custom apps.

## Rationale

### DA CLI Documentation Gap

The current `.cursorrules` file mentions DA CLI briefly but doesn't explain:
- What DA CLI is and why it exists
- Its full capabilities (code generation, manifest management)
- How it differs from other setup methods
- When to use it vs. manual setup

### Conversion Guide Need

Many developers use AI tools (Lovable, v0, etc.) to generate app prototypes, but these tools create:
- Next.js apps with SSR (incompatible with Domo)
- API routes (no backend in Domo)
- Framework-specific patterns (need Domo equivalents)

There's currently no guidance on how to convert these apps. This PR fills that gap.

## Impact Assessment

**High Value Addition:**
- **DA CLI docs** - Helps developers understand the recommended tooling
- **Conversion guide** - Saves hours of trial-and-error for developers with generated apps
- **Pattern guidance** - Provides clear migration path from common frameworks

**Developer Benefits:**
- Understand when and how to use DA CLI
- Clear process for converting generated apps
- Avoid common pitfalls (SSR, API routes, routing)
- Know what DA CLI can and cannot do

## Proposed Addition Location

Insert after the "Build & Deploy Workflow" section and before "Base Path Configuration". This placement makes sense because:
1. It's about project setup and workflow
2. Conversion is part of the development process
3. It comes before technical configuration details

## Content Structure

The addition includes:

### 1. DA CLI - Purpose and Capabilities
- What DA CLI is (scaffolding and code generation tool)
- Installation and basic usage
- Code generation commands
- Manifest management
- Project structure it creates

### 2. Converting Generated Apps to Domo
- The conversion challenge (SSR, API routes, etc.)
- Recommended conversion pattern
- Step-by-step process:
  1. Use DA CLI to generate reference structure
  2. Detect and remove SSR code
  3. Replace data fetching with Domo APIs
  4. Update routing (HashRouter)
  5. Fix build configuration
- What DA CLI helps with (reference structure, component generation)
- What DA CLI doesn't do (no automatic conversion)

## Key Highlights

### Critical Information Included:
- **DA CLI is not a conversion tool** - Important clarification
- **Use DA CLI as reference** - Recommended pattern for conversion
- **SSR detection** - Reinforces existing warning about server-side code
- **API migration patterns** - Clear examples of replacing backend calls
- **Step-by-step process** - Actionable conversion workflow

### Code Examples:
- DA CLI installation and usage
- Component generation examples
- Manifest management for environments
- Conversion pattern examples
- Data fetching migration (Next.js → Domo APIs)

## Testing Notes

This documentation is based on:
- Official DA CLI documentation patterns
- Common conversion scenarios from Lovable/v0 apps
- Best practices for Domo app architecture
- Integration with existing SSR detection warnings

## Files to Update

- `.cursorrules` - Add DA CLI section and conversion guide
