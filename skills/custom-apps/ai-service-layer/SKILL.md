---
name: ai-service-layer
description: Toolkit-first AIClient patterns for generation, text-to-sql, and response parsing.
---

# Rule: Domo App Platform AI (Toolkit-First)

This rule is **toolkit-first**. Use `AIClient` from `@domoinc/toolkit`.

## Canonical Client

```bash
yarn add @domoinc/toolkit
```

```typescript
import { AIClient } from '@domoinc/toolkit';
```

## Critical: AIClient methods are static

Do **not** instantiate `AIClient` for these methods.

Wrong:
```typescript
const ai = new AIClient();
await ai.text_to_sql('...');
```

Correct:
```typescript
await AIClient.text_to_sql('...');
```

## Text Generation

```typescript
const response = await AIClient.generate_text(
  'Explain this sales trend in simple terms',
  { template: 'You are a business analyst. ${input}' },
  { tone: 'professional' },
  undefined,
  { temperature: 0.7 }
);

const body = response.data || response.body || response;
const text = body.output || body.choices?.[0]?.output;
```

## Additional AI Methods

### `text_to_sql` schema argument must be an array

Wrong:
```typescript
await AIClient.text_to_sql('Show top vendors by spend', {
  dataSourceName: 'vendorPayments',
  columns: [{ name: 'amount', type: 'number' }]
});
```

Correct:
```typescript
await AIClient.text_to_sql('Show top vendors by spend', [
  {
    dataSourceName: 'vendorPayments',
    description: 'Vendor payment invoices',
    columns: [
      { name: 'vendor', type: 'string' },
      { name: 'amount', type: 'number' },
      { name: 'date', type: 'date' }
    ]
  }
]);
```

## Signature reference

(Approximate; check installed toolkit typings for exact current signature.)

```typescript
AIClient.text_to_sql(
  input: string,
  dataSourceSchemas?: DataSourceSchema[], // array
  promptTemplate?: any,
  parameters?: Record<string, string>,
  model?: string,
  modelConfiguration?: Record<string, Object>
): Promise<Response<TextAIResponse>>;
```

Why array: this supports multi-table SQL generation (including join-aware SQL) when multiple schemas are provided.

## text_to_sql usage note

`text_to_sql` is great for ad-hoc SQL, but `/sql/v1` does **not** automatically apply dashboard/page filters.
If filter-awareness is required in embedded cards, use Query API (`/data/v1` via `@domoinc/query`) for execution.

```typescript
const sqlResult = await AIClient.text_to_sql('Show total sales by region', [
  {
    dataSourceName: 'Sales',
    description: 'Sales transactions',
    columns: [{ name: 'region', type: 'string' }, { name: 'amount', type: 'number' }]
  }
]);

const beastModeResult = await AIClient.text_to_beastmode(
  'Calculate year over year growth percentage',
  { dataSourceName: 'Revenue', columns: [{ name: 'revenue', type: 'number' }, { name: 'date', type: 'date' }] }
);
```

## Response Handling Rule

`AIClient` responses are not always shaped like other toolkit clients:
- often uses `response.data`
- may include both `output` and `choices`

Use defensive parsing plus a strict string guard:

```typescript
const body = response?.data ?? response?.body ?? response;
const outputCandidate = body?.output ?? body?.choices?.[0]?.output;
const output = typeof outputCandidate === 'string' ? outputCandidate.trim() : '';

if (!output) throw new Error('AI returned no usable output');
```

## Checklist
- [ ] `AIClient` methods use snake_case (`generate_text`, `text_to_sql`, etc.)
- [ ] `AIClient` methods are called statically (for example `AIClient.text_to_sql(...)`, not instance methods)
- [ ] `AIClient.text_to_sql` second argument is `DataSourceSchema[]` (array), not a single object
- [ ] Responses parsed from `data`/`body` fallback
- [ ] Output extraction includes string guard and empty-output handling
- [ ] Error handling and loading state in UI
