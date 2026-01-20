# Rule: Domo App Platform AppDB (Collections)

You are building a Domo Custom App that needs to store and retrieve app-specific data. AppDB provides document-style collections for persistent storage within your app.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

## manifest.json Configuration

Every AppDB collection your app uses MUST be declared in `manifest.json` under the `collections` array.

```json
{
  "name": "My Custom App",
  "version": "1.0.0",
  "size": {
    "width": 4,
    "height": 4
  },
  "collections": [
    {
      "name": "CommentsTable",
      "schema": {
        "columns": [
          { "name": "user", "type": "STRING" },
          { "name": "comment", "type": "STRING" }
        ]
      },
      "syncEnabled": true
    },
    {
      "name": "Users"
    },
    {
      "name": "Settings",
      "schema": {
        "columns": [
          { "name": "key", "type": "STRING" },
          { "name": "value", "type": "STRING" },
          { "name": "updatedAt", "type": "LONG" }
        ]
      }
    }
  ]
}
```

Key points:
- `collections` is an **array** of collection objects
- Each collection has a `name` (used as the identifier in API calls)
- `schema` is optional - defines column structure with `columns` array
- Each column has `name` and `type` (STRING, LONG, DOUBLE, DATETIME)
- `syncEnabled` (optional) - enables data sync features

---

## AppDB API Endpoints

Base path: `/domo/datastores/v1/collections/{collectionName}`

### List all documents in a collection
```javascript
domo.get('/domo/datastores/v1/collections/CommentsTable/documents')
  .then(documents => {
    console.log(documents); // Array of documents
  });
```

### Get a single document by ID
```javascript
domo.get('/domo/datastores/v1/collections/CommentsTable/documents/doc-id-here')
  .then(doc => {
    console.log(doc);
  });
```

### Create a new document
```javascript
domo.post('/domo/datastores/v1/collections/CommentsTable/documents', {
  content: {
    user: 'john.doe',
    comment: 'This is a great feature!'
  }
})
  .then(created => {
    console.log('Created:', created.id);
  });
```

### Update a document
```javascript
domo.put('/domo/datastores/v1/collections/CommentsTable/documents/doc-id-here', {
  content: {
    user: 'john.doe',
    comment: 'Updated comment text'
  }
})
  .then(updated => {
    console.log('Updated:', updated);
  });
```

### Delete a document
```javascript
domo.delete('/domo/datastores/v1/collections/CommentsTable/documents/doc-id-here')
  .then(() => {
    console.log('Deleted successfully');
  });
```

### Query with filters
```javascript
// Query documents where user equals 'john.doe'
domo.get('/domo/datastores/v1/collections/CommentsTable/documents?user=john.doe')
  .then(docs => {
    console.log(docs);
  });
```

---

## Bulk Operations

### Bulk create
```javascript
domo.post('/domo/datastores/v1/collections/CommentsTable/documents/bulk', [
  { content: { user: 'user1', comment: 'Comment 1' } },
  { content: { user: 'user2', comment: 'Comment 2' } }
])
  .then(results => {
    console.log('Created documents:', results);
  });
```

### Bulk update
```javascript
domo.put('/domo/datastores/v1/collections/CommentsTable/documents/bulk', [
  { id: 'doc-1', content: { user: 'user1', comment: 'Updated 1' } },
  { id: 'doc-2', content: { user: 'user2', comment: 'Updated 2' } }
])
  .then(results => {
    console.log('Updated documents:', results);
  });
```

---

## Common Patterns

### React hook for AppDB
```javascript
import { useEffect, useState } from 'react';

function useAppDB(collectionName) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    domo.get(`/domo/datastores/v1/collections/${collectionName}/documents`)
      .then(setDocuments)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, [collectionName]);

  const addDocument = async (content) => {
    const created = await domo.post(
      `/domo/datastores/v1/collections/${collectionName}/documents`,
      { content }
    );
    setDocuments(prev => [...prev, created]);
    return created;
  };

  const updateDocument = async (id, content) => {
    const updated = await domo.put(
      `/domo/datastores/v1/collections/${collectionName}/documents/${id}`,
      { content }
    );
    setDocuments(prev => prev.map(d => d.id === id ? updated : d));
    return updated;
  };

  const deleteDocument = async (id) => {
    await domo.delete(`/domo/datastores/v1/collections/${collectionName}/documents/${id}`);
    setDocuments(prev => prev.filter(d => d.id !== id));
  };

  return { documents, loading, addDocument, updateDocument, deleteDocument };
}
```

### Upsert pattern (create or update)
```javascript
async function upsertSetting(key, value) {
  // Try to find existing
  const existing = await domo.get(`/domo/datastores/v1/collections/Settings/documents?key=${key}`);

  const content = { key, value, updatedAt: Date.now() };

  if (existing && existing.length > 0) {
    return domo.put(
      `/domo/datastores/v1/collections/Settings/documents/${existing[0].id}`,
      { content }
    );
  } else {
    return domo.post(
      '/domo/datastores/v1/collections/Settings/documents',
      { content }
    );
  }
}
```

---

## Checklist
- [ ] Collection(s) declared in `manifest.json` under `collections` array
- [ ] Each collection has a unique `name`
- [ ] Schema defined with appropriate column types (optional but recommended)
- [ ] Using collection `name` in API calls
- [ ] Proper error handling for all CRUD operations
- [ ] Consider bulk operations for multiple documents
- [ ] Document IDs are properly managed (stored after creation)
