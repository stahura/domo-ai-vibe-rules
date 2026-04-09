---
name: fileset-api
description: Build Domo custom apps that use FileSets for file storage, upload, download, and AI document search — all via fetch('/api/files/v1/') with no manifest.json entry required. Use this whenever a Domo app needs file upload via FormData/fetch (not domo.post), file download as a blob, file listing via POST /files/search, AI document queries via the /query endpoint, or fileset CRUD. Also use when the user asks about /api/files/v1 vs /domo/files/v1, whether filesets need manifest.json wiring, how to build a file browser in React, or how to make a document Q&A chatbot in Domo.
---

# Domo FileSets — App Framework API

> **Status:** This API is in BETA and subject to change. Build defensively — wrap calls in try/catch and surface meaningful errors to the user.

FileSets are Domo's file storage system. From a custom app you can upload and download files, browse directory trees, search by name, and run AI-powered semantic queries against file content.

## Setup — no manifest wiring needed

Unlike datasets, filesets don't need a `manifest.json` entry. Just define the fileset ID as a constant in your service file:

```javascript
// src/services/api.js
const FILESET_ID = 'b6ebf7e9-64ae-4e6d-b8ca-b356fe62923f'; // replace with your fileset ID
```

Get the fileset ID from the Domo UI or via the `fileset-cli` skill (`filesets search --name "..."`).

---

## URL pattern: `/api/` vs `/domo/`

Within a Domo custom app you have two valid approaches:

| Pattern | When to use |
|---------|-------------|
| `fetch('/api/files/v1/...')` | Simplest. Use for all JSON and binary calls. No import needed. |
| `domo.get('/domo/files/v1/...')` | Use when you want the domo.js proxy (e.g. already using `domo.*` elsewhere). JSON only — no binary. |

The examples below use `fetch('/api/...')` because it handles both JSON and binary (uploads/downloads) consistently. For binary operations you must use `fetch` regardless.

---

## Files

### List files in a fileset

```javascript
const response = await fetch(`/api/files/v1/filesets/${FILESET_ID}/files/search`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fieldSort: [{ field: 'created', order: 'DESC' }],
    filters: [],
    dateFilters: []
  })
});
const data = await response.json();
const files = data.files; // array of file objects
```

**With directory and name filter:**

```javascript
const response = await fetch(
  `/api/files/v1/filesets/${FILESET_ID}/files/search` +
  `?directoryPath=/reports&immediateChildren=true&limit=50`,
  {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      fieldSort: [{ field: 'name', order: 'ASC' }],
      filters: [{ field: 'name', value: ['.pdf'], operator: 'LIKE' }],
      dateFilters: []
    })
  }
);
```

**Paginate** using the `next` token from `data.pageContext.next`:

```javascript
// data.pageContext shape: { next, offset, limit, total }
if (data.pageContext.next) {
  const nextPage = await fetch(
    `/api/files/v1/filesets/${FILESET_ID}/files/search?next=${data.pageContext.next}`,
    { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({}) }
  );
}
```

### Get file metadata

```javascript
// By file ID
const response = await fetch(`/api/files/v1/filesets/${FILESET_ID}/files/${fileId}`);
const file = await response.json();
// { id, path, name, fileType, contentType, size, hash, created, createdBy }

// By path (when you know the directory structure)
const response = await fetch(
  `/api/files/v1/filesets/${FILESET_ID}/path?path=${encodeURIComponent('/reports/march.pdf')}`
);
```

### Download a file

Use `fetch` and create a temporary download link. The download endpoint returns binary content:

```javascript
async function downloadFile(fileId, filename) {
  const response = await fetch(
    `/api/files/v1/filesets/${FILESET_ID}/files/${fileId}/download`
  );
  if (!response.ok) throw new Error(`Download failed: ${response.status}`);

  const blob = await response.blob();
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  a.click();
  URL.revokeObjectURL(url);
}
```

For text-based files you can also use `.text()` instead of `.blob()` to read content directly:

```javascript
const response = await fetch(`/api/files/v1/filesets/${FILESET_ID}/files/${fileId}/download`);
const text = await response.text(); // use for .txt, .csv, .md, etc.
```

### Upload a file

Use `FormData` with two parts — the binary file and the directory metadata. Don't set `Content-Type`; the browser sets it with the correct multipart boundary automatically:

```javascript
async function uploadFile(file, directoryPath = '/') {
  const formData = new FormData();
  formData.append('file', file);                                           // File or Blob
  formData.append('createFileRequest', JSON.stringify({ directoryPath })); // metadata

  const response = await fetch(`/api/files/v1/filesets/${FILESET_ID}/files`, {
    method: 'POST',
    body: formData
    // ⚠️ Do NOT set Content-Type header — browser handles it
  });

  if (!response.ok) throw new Error(`Upload failed: ${response.status}`);
  return response.json(); // returns the new file object
}
```

**From a file input element:**

```javascript
document.getElementById('file-input').addEventListener('change', async (e) => {
  const file = e.target.files[0];
  const record = await uploadFile(file, '/uploads/2024');
  console.log('Uploaded:', record.id, record.path);
});
```

**From a generated Blob (e.g. CSV export):**

```javascript
const csv = 'name,value\nAlice,100\nBob,200';
const blob = new Blob([csv], { type: 'text/csv' });
const file = new File([blob], 'export.csv', { type: 'text/csv' });
await uploadFile(file, '/exports');
```

### Delete a file

```javascript
// By file ID
await fetch(`/api/files/v1/filesets/${FILESET_ID}/files/${fileId}`, { method: 'DELETE' });

// By path
await fetch(
  `/api/files/v1/filesets/${FILESET_ID}/path?path=${encodeURIComponent('/reports/march.pdf')}`,
  { method: 'DELETE' }
);
```

---

## FileSets (containers)

You can create and manage fileset containers from within the app, though typically the fileset already exists and the app just uses the hardcoded ID.

### Search filesets

```javascript
const response = await fetch('/api/files/v1/filesets/search?limit=50', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fieldSort: [{ field: 'updated', order: 'DESC' }],
    filters: [{ field: 'name', value: ['reports'], operator: 'LIKE' }],
    dateFilters: []
  })
});
```

### Create a fileset

```javascript
const response = await fetch('/api/files/v1/filesets', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'Monthly Reports', description: 'Automated PDF outputs' })
});
const fileset = await response.json();
const filesetId = fileset.id;
```

---

## AI-powered file query

Requires `aiEnabled: true` on the fileset. Runs a natural-language question against file content and returns ranked matches with relevance scores:

```javascript
const response = await fetch(`/api/files/v1/filesets/${FILESET_ID}/query`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'What were the key revenue drivers last quarter?',
    directoryPath: '/reports/2024',
    topK: 5
  })
});
const data = await response.json();
// data.matches: [{ id, node: { file object }, score: 0.89 }, ...]
```

---

## File object shape

```json
{
  "id": "xyz789-file-id",
  "path": "/reports/2024/march.pdf",
  "name": "march.pdf",
  "fileType": "PDF",
  "contentType": "application/pdf",
  "size": 204800,
  "hash": "sha256:abc...",
  "hashAlgorithm": "SHA256",
  "created": "2024-03-01T08:00:00Z",
  "createdBy": 12345
}
```

---

## Complete example: file browser service

A clean service module pattern for a React app:

```javascript
// src/services/filesetApi.js

const FILESET_ID = 'your-fileset-id-here';
const BASE = `/api/files/v1/filesets/${FILESET_ID}`;

export async function listFiles(directoryPath = null, nameFilter = null) {
  const params = new URLSearchParams({ limit: '100' });
  if (directoryPath) params.set('directoryPath', directoryPath);

  const filters = nameFilter
    ? [{ field: 'name', value: [nameFilter], operator: 'LIKE' }]
    : [];

  const response = await fetch(`${BASE}/files/search?${params}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ fieldSort: [{ field: 'name', order: 'ASC' }], filters, dateFilters: [] })
  });
  if (!response.ok) throw new Error(`List failed: ${response.status}`);
  const data = await response.json();
  return data.files ?? [];
}

export async function downloadFileContent(fileId) {
  const response = await fetch(`${BASE}/files/${fileId}/download`);
  if (!response.ok) throw new Error(`Download failed: ${response.status}`);
  return response.text(); // swap for .blob() for binary files
}

export async function uploadFile(file, directoryPath = '/') {
  const form = new FormData();
  form.append('file', file);
  form.append('createFileRequest', JSON.stringify({ directoryPath }));
  const response = await fetch(`${BASE}/files`, { method: 'POST', body: form });
  if (!response.ok) throw new Error(`Upload failed: ${response.status}`);
  return response.json();
}

export async function queryFiles(question, directoryPath = null, topK = 5) {
  const body = { query: question, topK };
  if (directoryPath) body.directoryPath = directoryPath;
  const response = await fetch(`${BASE}/query`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body)
  });
  if (!response.ok) throw new Error(`Query failed: ${response.status}`);
  const data = await response.json();
  return data.matches ?? [];
}
```

---

## Managing filesets from CLI

To discover fileset IDs, browse files, download to disk, or run commands outside an app, use the `fileset-cli` skill.
