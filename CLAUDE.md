# Domo App Platform Custom App Development

You are helping build a Domo App Platform Custom App. This is a client-side web application that runs inside the Domo platform and uses Domo's App Framework APIs.

**Important:** Do NOT confuse the App Platform/Framework APIs with Domo's Public API or Product API - they are different. The App Platform APIs are specifically for custom apps running inside Domo.

---

## Domo App Framework APIs

The following APIs are available to custom apps via the `domo.js` library (automatically included when running in Domo):

| API | Purpose |
|-----|---------|
| **Data API** | Query datasets mapped in manifest (`/data/v1/`, `/sql/v1/`) |
| **AppDB** | Document-style collections for app storage (`/domo/datastores/v1/collections/`) |
| **AI Service Layer** | Text generation, image-to-text (`/domo/ai/v1/`) |
| **Code Engine** | Server-side functions for secure operations (`/domo/codeengine/v2/packages/`) |
| **Workflows** | Trigger automation workflows (`/domo/workflow/v1/models/`) |
| **Files** | File storage and retrieval |
| **Filesets** | Grouped file management |
| **Groups** | Domo group information |
| **User** | Current user context |
| **Task Center** | Task management |

See the individual rule files in this repo for detailed usage of each API.

---

## Installing domo.js (ryuu.js)

**React / npm projects:**
```bash
npm install ryuu.js
```
```javascript
import domo from 'ryuu.js';
```

**Vanilla JavaScript (CDN):**
```html
<script src="https://app.unpkg.com/ryuu.js@5.1.2"></script>
```

---

## domo.js Utilities

Beyond the APIs, domo.js provides useful utilities for interacting with the Domo environment:

### Environment Info
```javascript
console.log(domo.env.userId);    // Current user ID
console.log(domo.env.customer);  // Customer/instance name
console.log(domo.env.pageId);    // Current page ID
console.log(domo.env.locale);    // Locale (e.g., 'en-US')
console.log(domo.env.platform);  // 'desktop' or 'mobile'
```

### Event Listeners
```javascript
// React to dataset updates on the page
domo.onDataUpdated((alias) => {
  console.log(`Dataset ${alias} was updated`);
  // Refresh your data or do nothing to prevent auto-reload
});

// React to page filter changes
domo.onFiltersUpdated((filters) => {
  console.log('Filters changed:', filters);
  // Apply filters to your visualization
});

// React to Domo variable changes
domo.onVariablesUpdated((variables) => {
  console.log('Variables updated:', variables);
});
```

### Navigation
**Important:** Standard anchor tags with `href` do NOT work properly in Domo apps. You must use `domo.navigate()`:

```javascript
// Navigate within Domo
domo.navigate('/page/123456789');

// Open in new tab
domo.navigate('/page/123456789', true);

// External URLs also work
domo.navigate('https://example.com', true);
```

### Fetch Multiple Datasets
```javascript
// Load multiple datasets in parallel
const [sales, customers, products] = await domo.getAll([
  '/data/v1/sales',
  '/data/v1/customers',
  '/data/v1/products'
]);
```

### Update Page Filters Programmatically
```javascript
domo.requestFiltersUpdate(
  [
    {
      column: 'category',
      operator: 'IN',
      values: ['Electronics', 'Clothing'],
      dataType: 'STRING'
    }
  ],
  true, // apply to page
  () => console.log('Filter update acknowledged'),
  (response) => console.log('Filter update completed:', response)
);
```

---

## manifest.json

The `manifest.json` file is critical - it declares all external resources your app needs. Domo uses this to:
1. Know which datasets, collections, workflows, and code engine functions to connect
2. Map aliases (used in your code) to actual Domo resource IDs (configured at publish time)

### Basic structure
```json
{
  "name": "My App Name",
  "version": "1.0.0",
  "id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "fullpage": true,
  "size": {
    "width": 4,
    "height": 3
  },
  "datasetsMapping": [],
  "collections": [],
  "workflowMapping": [],
  "packageMapping": []
}
```

### Key properties
- `name` / `version` - App metadata
- `id` - **Generated on first publish** (see deployment section)
- `fullpage` - Set `true` for full-page apps
- `size` - Card dimensions (width/height in grid units)
- `datasetsMapping` - Datasets the app can query
- `collections` - AppDB collections for storage
- `workflowMapping` - Workflows the app can trigger
- `packageMapping` - Code Engine functions the app can call

---

## Build & Deploy Workflow

### Prerequisites
- Node.js installed
- Domo CLI installed (`npm install -g @domoinc/ryuu`)

### Local development
```bash
npm install          # Install dependencies
npm run dev          # Start dev server (usually Vite)
```

For API calls to work locally, you need ryuu-proxy configured and `domo login` authenticated.

### Build for production
```bash
npm run build        # Outputs to dist/ (Vite) or build/ (CRA)
```

### Domo CLI Authentication
```bash
domo login           # Authenticate with your Domo instance
```

You'll be prompted for your Domo instance URL and credentials.

### Publishing
```bash
cd dist              # Change to build output directory
domo publish         # Publish to Domo
```

**Important - First publish:**
- On first publish, Domo generates a new `id` for your app
- This ID appears in the published `manifest.json` in your dist folder
- **You must copy this ID back to your source `manifest.json`** (e.g., `public/manifest.json`)
- If you don't, every publish creates a NEW app instead of updating the existing one

```bash
# After first publish, copy the generated ID:
# dist/manifest.json → public/manifest.json (just the "id" field)
```

### Subsequent publishes
Once the ID is in your source manifest:
```bash
npm run build && cd dist && domo publish
```

---

## Base Path Configuration (Vite)

Domo serves apps from a subpath, not root. Configure Vite for relative paths:

```javascript
// vite.config.js
export default defineConfig({
  base: './',
  // ... other config
});
```

---

## Routing (React Router)

If using client-side routing, prefer `HashRouter` for App Platform:

```javascript
import { HashRouter } from 'react-router-dom';

// HashRouter works without server rewrites
<HashRouter>
  <App />
</HashRouter>
```

`BrowserRouter` requires server-side rewrite rules which Domo doesn't provide by default.

---

## Project-Specific Instructions

Add your project-specific rules below this line:

---

