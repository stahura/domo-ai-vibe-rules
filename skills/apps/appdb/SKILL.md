---
name: appdb
description: Toolkit-first AppDB document CRUD, query operators, and collection wiring.
---

# Rule: Domo App Platform AppDB (Toolkit-First)

This rule is **toolkit-first**. Use `AppDBClient` instead of raw `domo.get/post/put/delete` endpoints.

> Legacy endpoint-first guidance has been archived to `archive/legacy-rules/domo-appdb.md`.

## Canonical Client

```bash
yarn add @domoinc/toolkit
```

```typescript
import { AppDBClient } from '@domoinc/toolkit';

type Task = {
  title: string;
  status: 'active' | 'completed';
  priority: 'Low' | 'High' | 'Urgent';
};

const tasksClient = new AppDBClient.DocumentsClient<Task>('TasksCollection');
```

## Core Operations

### Create
```typescript
const created = await tasksClient.create({
  title: 'New Task',
  status: 'active',
  priority: 'High'
});
const task = created.body;
```

### Read / query
```typescript
const all = await tasksClient.get();
const active = await tasksClient.get({ status: { $eq: 'active' } });
const highOpen = await tasksClient.get({
  $and: [{ status: { $ne: 'completed' } }, { priority: { $in: ['High', 'Urgent'] } }]
});
```

## AppDB response structure (critical)

Documents returned by `.get()` are wrapped with metadata and your fields live inside `doc.content`.

What `.create()` accepts:
```typescript
{ vendor: 'Acme', riskLevel: 'High', notes: 'Late payments' }
```

What `.get()` returns (shape):
```json
[
  {
    "id": "04b1756e-7b6d-4d77-842f-7975a6474d8a",
    "datastoreId": "a3b85171-...",
    "collectionId": "ba194a7d-...",
    "syncRequired": true,
    "owner": 767612617,
    "createdOn": "2026-03-22T02:22:42.030Z",
    "updatedOn": "2026-03-22T02:22:42.030Z",
    "updatedBy": 767612617,
    "content": {
      "vendor": "Acme",
      "riskLevel": "High",
      "notes": "Late payments"
    }
  }
]
```

Key points:
- Your app fields are nested inside `doc.content`, not at the top level.
- `doc.id` is the document ID used for `.update()` and `.delete()`.
- Metadata fields (`datastoreId`, `collectionId`, `owner`, `createdOn`, etc.) are top-level.
- Overall result may be in `response.body` or directly the array.

Required parsing pattern:
```typescript
const response = await tasksClient.get();
const rawDocs = response.body || response;
const docs = Array.isArray(rawDocs) ? rawDocs : [];

const parsed = docs.map((doc) => ({
  id: doc.id,
  ...doc.content
}));
```

Common mistake:
```typescript
// WRONG: fields are inside content
const docs = response.body || response;
docs[0].vendor; // undefined

// CORRECT
docs[0].content.vendor; // "Acme"
```

### Update
```typescript
await tasksClient.update({
  id: 'document-uuid',
  content: { title: 'Updated', status: 'completed', priority: 'Low' }
});

await tasksClient.partialUpdate(
  { status: { $eq: 'active' } },
  { $set: { status: 'archived' } }
);
```

### Delete
```typescript
await tasksClient.delete('document-uuid');
await tasksClient.delete(['uuid-1', 'uuid-2']);
```

## Manifest Requirements

Collections still must exist in `manifest.json` under `collections`.

```json
{
  "collections": [
    {
      "name": "TasksCollection",
      "schema": {
        "columns": [
          { "name": "title", "type": "STRING" },
          { "name": "status", "type": "STRING" }
        ]
      }
    }
  ]
}
```

## Canonical Rules References

- Toolkit AppDB patterns: `.cursor/rules/04-toolkit.mdc`
- AppDB gotchas and sync caveats: `.cursor/rules/09-gotchas.mdc`

## Checklist
- [ ] `collections` mapping exists in manifest
- [ ] `AppDBClient.DocumentsClient` used for CRUD
- [ ] `.get()` results are unwrapped from `doc.content` before UI/use
- [ ] Query/update operators (`$eq`, `$in`, `$set`, `$inc`, etc.) used correctly
- [ ] Error handling and loading states included in UI flows
