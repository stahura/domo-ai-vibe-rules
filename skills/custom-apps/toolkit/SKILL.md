---
name: toolkit
description: Toolkit client usage for AIClient, AppDBClient, WorkflowClient, and CodeEngineClient.
---

# @domoinc/toolkit - Service Clients

The toolkit provides typed client classes for Domo services.

```bash
yarn add @domoinc/toolkit
```

```typescript
import {
  AppDBClient,
  AIClient,
  IdentityClient,
  SqlClient,
  UserClient,
  GroupClient,
  FileClient,
  CodeEngineClient,
  WorkflowClient,
  DomoClient
} from '@domoinc/toolkit';
```

## Response Wrapper

Most toolkit methods return a response wrapper:

```typescript
interface ToolkitResponse<T> {
  body: T;        // The actual data
  status: number; // HTTP status code
  headers?: Record<string, string>;
}

// Usage
const response = await IdentityClient.get();
const user = response.body;  // Access the data
const status = response.status;
```

**Exception:** `AIClient` often returns payload under `response.data`. Handle AI responses with:

```typescript
const body = response.data || response.body || response;
const output = body.output || body.choices?.[0]?.output;
```

## AppDBClient - NoSQL Document Store

**PREFERRED for CRUD apps and long text storage.** Collections can sync to Domo datasets.

### DocumentsClient

```typescript
// Define your document type
interface Task {
  title: string;
  description: string;
  status: 'active' | 'completed';
  priority: 'Low' | 'High' | 'Urgent';
  dueDate?: string;
}

// Create client for a collection
const tasksClient = new AppDBClient.DocumentsClient<Task>('TasksCollection');
```

**Create Documents:**
```typescript
// Create single document
const response = await tasksClient.create({
  title: 'New Task',
  description: 'Task description',
  status: 'active',
  priority: 'High'
});
const newTask = response.body;
// Returns: { id: 'uuid', content: {...}, owner: 'userId', createdOn: '...', updatedOn: '...' }

// Create multiple documents
const response = await tasksClient.create([
  { title: 'Task 1', status: 'active', priority: 'Low' },
  { title: 'Task 2', status: 'active', priority: 'High' }
]);
```

**Read/Query Documents:**
```typescript
// Get all documents
const response = await tasksClient.get();
const tasks = response.body;

// Filter with MongoDB-style queries
const activeTasks = await tasksClient.get({
  status: { $eq: 'active' }
});

const highPriority = await tasksClient.get({
  priority: { $in: ['High', 'Urgent'] },
  status: { $ne: 'completed' }
});

// Complex queries
const filtered = await tasksClient.get({
  $and: [
    { status: { $eq: 'active' } },
    { priority: { $in: ['High', 'Urgent'] } }
  ]
});

const either = await tasksClient.get({
  $or: [
    { priority: { $eq: 'Urgent' } },
    { status: { $eq: 'completed' } }
  ]
});

// With pagination and sorting
const paginated = await tasksClient.get(
  { status: { $eq: 'active' } },
  {
    limit: 10,
    offset: 0,
    orderby: ['priority', 'dueDate']
  }
);

// Aggregations
const statusCounts = await tasksClient.get(
  {},
  {
    groupby: ['status'],
    count: 'id'
  }
);

const priorityStats = await tasksClient.get(
  {},
  {
    groupby: ['priority'],
    count: 'id',
    avg: ['estimatedHours']
  }
);
```

**CRITICAL response shape note:**
- `.get()` returns document wrappers with metadata; your app fields are in `doc.content`.
- Do not assume `docs[0].fieldName`; use `docs[0].content.fieldName`.

```typescript
const response = await tasksClient.get();
const rawDocs = response.body || response;
const docs = Array.isArray(rawDocs) ? rawDocs : [];

const parsed = docs.map((doc) => ({
  id: doc.id,
  ...doc.content
}));
```

**MongoDB Query Operators:**
- `$eq` - Equals
- `$ne` - Not equals
- `$gt` - Greater than
- `$gte` - Greater than or equal
- `$lt` - Less than
- `$lte` - Less than or equal
- `$in` - In array
- `$nin` - Not in array
- `$regex` - Regular expression match
- `$and` - Logical AND
- `$or` - Logical OR

**Update Documents:**
```typescript
// Full update (replace content)
const response = await tasksClient.update({
  id: 'document-uuid',
  content: {
    title: 'Updated Title',
    description: 'Updated description',
    status: 'completed',
    priority: 'Low'
  }
});

// Bulk update
const bulkResponse = await tasksClient.update([
  { id: 'uuid-1', content: { title: 'Updated 1', status: 'active', priority: 'Low' } },
  { id: 'uuid-2', content: { title: 'Updated 2', status: 'active', priority: 'High' } }
]);
// Returns: { body: { updated: 2, inserted: 0 } }

// Partial update with MongoDB operators
const count = await tasksClient.partialUpdate(
  { status: { $eq: 'active' } },  // Filter
  { $set: { status: 'archived' } }  // Operation
);
// Returns number of documents updated

// Partial update operators
await tasksClient.partialUpdate(
  { priority: { $eq: 'Low' } },
  {
    $set: { priority: 'Medium', updatedAt: new Date().toISOString() },
    $unset: { tempField: 1 },
    $inc: { viewCount: 1 }
  }
);
```

**MongoDB Update Operators:**
- `$set` - Set field values
- `$unset` - Remove fields
- `$inc` - Increment numeric fields
- `$push` - Add to array fields

**Delete Documents:**
```typescript
// Delete single document
await tasksClient.delete('document-uuid');

// Bulk delete
const response = await tasksClient.delete(['uuid-1', 'uuid-2', 'uuid-3']);
// Returns: { body: { deleted: 3 } }
```

### CollectionsClient

```typescript
const collectionsClient = new AppDBClient.CollectionsClient();

// List all collections
const collections = await collectionsClient.list();

// Create collection
await collectionsClient.create({
  name: 'NewCollection',
  schema: {
    columns: [
      { name: 'field1', type: 'STRING' },
      { name: 'field2', type: 'LONG' }
    ]
  }
});

// Delete collection
await collectionsClient.delete('CollectionName');

// Export all collections
const exportData = await collectionsClient.export();
```

## IdentityClient - Current User (SECURE)

**Use this instead of Domo.env for security-sensitive operations.**

```typescript
// Get current authenticated user
const response = await IdentityClient.get();
const user = response.body;
// {
//   id: 12345,
//   displayName: 'John Doe',
//   userName: 'jdoe',
//   emailAddress: 'jdoe@company.com',
//   avatarKey: 'abc123',
//   role: 'Admin',
//   groups: [{ id: 1, name: 'Everyone' }, ...]
// }

// With options
const response = await IdentityClient.get(
  5000,  // timeout in ms
  false  // includeGroups - set false for faster response
);
```

## SqlClient - Direct SQL Queries

**Note:** SQL endpoint does NOT respect page filters. Use Query endpoint for dashboard-embedded apps.

```typescript
const sqlClient = new SqlClient();

// Execute SQL query
const response = await sqlClient.get(
  'sales-dataset-alias',
  'SELECT region, SUM(amount) as total FROM sales-dataset-alias GROUP BY region ORDER BY total DESC'
);
const result = response.body;
// {
//   columns: ['region', 'total'],
//   rows: [{ region: 'North', total: 50000 }, ...],
//   numRows: 4,
//   numColumns: 2
// }

// Complex query
const response = await sqlClient.get(
  'sales',
  `SELECT 
    DATE_TRUNC('month', order_date) as month,
    product_category,
    SUM(revenue) as revenue,
    COUNT(*) as orders
   FROM sales
   WHERE order_date >= '2024-01-01'
   GROUP BY 1, 2
   ORDER BY 1, 3 DESC`
);

// Parse page filters into SQL (static method)
const predicates = SqlClient.parsePageFilters(['dataset1', 'dataset2']);
// Returns: { 'dataset1': [{ where: '"column" = \'value\'', having: '' }], ... }

// Get concatenated clauses
const clauses = SqlClient.parsePageFilters(['dataset1'], true);
// Returns: { 'dataset1': { whereClause: 'WHERE ...', havingClause: '' } }
```

## UserClient - User API

```typescript
// Get paginated list of users
const response = await UserClient.get(
  50,    // limit
  0,     // offset
  true   // includeDetails
);
const users = response.body;

// Get specific user
const response = await UserClient.getUser(
  12345,  // user ID
  true    // includeDetails
);
const user = response.body;

// Get user avatar
const avatarBlob = await UserClient.getAvatar(
  'avatar-key-from-user',
  'medium'  // 'small' | 'medium' | 'large'
);
```

## GroupClient - Groups API

```typescript
// Get all groups
const response = await GroupClient.get(50, 0);  // limit, offset
const groups = response.body;

// Get specific group
const response = await GroupClient.getGroup(456);
const group = response.body;

// Get group members
const response = await GroupClient.getMembers(456);
const members = response.body;  // Array of User objects
```

## FileClient - File Storage

```typescript
const fileClient = new FileClient();

// Upload file
const response = await fileClient.upload(
  fileObject,        // File object
  'report.pdf',      // Display name
  'Monthly report',  // Description (optional)
  true,              // isPublic (optional, default true)
  10000              // timeout (optional)
);
const fileId = response.body.id;

// Upload new revision
const response = await fileClient.uploadRevision(
  newFileObject,
  existingFileId
);

// Download file
const blob = await fileClient.download(
  fileId,
  'filename.pdf',
  revisionId  // optional, latest if omitted
);

// List files with details
const response = await fileClient.detailsList(
  [123, 456],  // File IDs (empty for all)
  ['metadata', 'permissions', 'revisions']  // Expand options
);

// Get/update permissions
const perms = await fileClient.getPermissions(fileId);
await fileClient.updatePermissions(fileId, JSON.stringify({
  public: false,
  users: [123, 456],
  groups: [789]
}));

// Delete file revision
await fileClient.delete(fileId, revisionId);
```

## AIClient - AI Services

All methods are static and use **snake_case** naming.

**Response Structure:**
**IMPORTANT:** AIClient uses `data` instead of `body` for the response payload! The toolkit wraps responses in `{ data, status, statusCode }`. The API response includes both a top-level `output` field and a `choices` array. Prefer the top-level `output` field when available.

```typescript
// Text generation
const response = await AIClient.generate_text(
  'Explain this sales trend in simple terms',
  { template: 'You are a business analyst. ${input}' },  // promptTemplate
  { tone: 'professional' },  // parameters for template
  'model-id',  // optional model override
  { temperature: 0.7 }  // model configuration
);

// Response structure: { data: { output: string, choices: [{ output: string }], ... }, status: "OK", statusCode: 200 }
// NOTE: AIClient uses 'data' not 'body'!
// Prefer top-level output field (more reliable)
const responseBody = response.data || response.body || response;
const text = responseBody.output || responseBody.choices?.[0]?.output;

// Text to SQL
const response = await AIClient.text_to_sql(
  'Show me total sales by region for Q4',
  [{
    dataSourceName: 'Sales',
    description: 'Sales transactions table',
    columns: [
      { name: 'region', type: 'string' },
      { name: 'amount', type: 'number' },
      { name: 'order_date', type: 'date' }
    ]
  }]
);
const responseBody = response.data || response.body || response;
const sql = responseBody.output || responseBody.choices?.[0]?.output;
// NOTE: second argument must be DataSourceSchema[] (array), not a single schema object.
// Passing an array allows multi-dataset SQL generation.

// Text to Beast Mode (calculated field)
const response = await AIClient.text_to_beastmode(
  'Calculate year over year growth percentage',
  {
    dataSourceName: 'Revenue',
    columns: [
      { name: 'revenue', type: 'number' },
      { name: 'date', type: 'date' }
    ]
  }
);
const responseBody = response.data || response.body || response;
const beastMode = responseBody.output || responseBody.choices?.[0]?.output;

// Text summarization
const response = await AIClient.summarize(
  longTextContent,
  undefined,  // promptTemplate
  undefined,  // parameters
  undefined,  // model
  undefined,  // modelConfiguration
  undefined,  // system prompt
  [],         // chatContext
  { separatorType: 'paragraph' },  // chunkingConfiguration
  'bullets',  // outputStyle: 'paragraph' | 'bullets'
  100         // outputWordLength
);
const responseBody = response.data || response.body || response;
const summary = responseBody.output || responseBody.choices?.[0]?.output;
```

## CodeEngineClient - Serverless Functions

In app implementations, prefer the working direct-call pattern via `domo.post` and `packagesMapping` contracts.
If you use Toolkit docs examples, verify runtime behavior in your environment.

```typescript
import domo from 'ryuu.js';

// Execute function by alias
const response = await domo.post('/domo/codeengine/v2/packages/calculateTax', {
  amount: 1000,
  state: 'CA'
});

// Inspect first run response shape
console.log('Code Engine response:', response);

const body = response?.body ?? response?.data ?? response;
const result =
  body?.output ??
  body?.result ??
  body?.value ??
  body;
```

Manifest note: use `packagesMapping` (with `s`) and include full parameter/output schema fields.

## WorkflowClient - Domo Workflows

```typescript
// List available workflow models
const response = await WorkflowClient.getAllModels();
const models = response.body;
const modelsWithPermissions = await WorkflowClient.getAllModels(true);

// Get model details by workflow alias from manifest workflowMapping.alias
const response = await WorkflowClient.getModelDetails('myWorkflow');
const model = response.body;

// Start workflow instance by alias (NOT UUID)
const response = await WorkflowClient.startModel(
  'myWorkflow',
  { inputVar: 'value', anotherVar: 123 }
);
const instance = response.body;
// { id: 'instance-uuid', modelId: '...', status: 'RUNNING', ... }

// Check instance status by alias + instanceId
const response = await WorkflowClient.getInstance('myWorkflow', 'instance-uuid');
const status = response.body;
// { id: '...', status: 'COMPLETED' | 'RUNNING' | 'FAILED', ... }
```

All `WorkflowClient` methods are alias-based in app code:
- `WorkflowClient.startModel(workflowAlias, variables)`
- `WorkflowClient.getAllModels()` / `WorkflowClient.getAllModels(true)`
- `WorkflowClient.getModelDetails(workflowAlias)`
- `WorkflowClient.getInstance(workflowAlias, instanceId)`

The workflow UUID lives in `manifest.json` under `workflowMapping[].modelId`; runtime client calls pass the alias.

## DomoClient - Alternative to ryuu.js

```typescript
// Same as Domo.get/post/put/delete but from toolkit
const data = await DomoClient.get('/data/v1/sales');
await DomoClient.post('/api/items', { name: 'test' });
await DomoClient.put('/api/items/123', { name: 'updated' });
await DomoClient.delete('/api/items/123');
```
