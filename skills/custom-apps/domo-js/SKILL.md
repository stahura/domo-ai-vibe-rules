---
name: domo-js
description: Use ryuu.js (domo.js) APIs for env, events, navigation, and data calls.
---

# domo.js (ryuu.js) SDK

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

Access environment information. **WARNING: Can be spoofed! Do not use for security.**

```javascript
console.log(domo.env.userId);    // User ID (spoofable!)
console.log(domo.env.customer);  // Customer/instance name
console.log(domo.env.pageId);    // Current page ID
console.log(domo.env.locale);    // Locale (e.g., 'en-US')
console.log(domo.env.platform);  // 'desktop' or 'mobile'
```

**For secure user verification:**
```javascript
// ✅ SECURE - Server-verified identity
const verifiedEnv = await domo.get('/domo/environment/v1/');
const { userId, userName, userEmail } = verifiedEnv;

// Or use IdentityClient from toolkit
import { IdentityClient } from '@domoinc/toolkit';
const response = await IdentityClient.get();
const user = response.body; // { id, displayName, emailAddress, role }
```

### Event Listeners

#### Dataset Updates

```javascript
domo.onDataUpdated((alias) => {
  console.log(`Dataset ${alias} was updated`);
  // Refresh your data or do nothing to prevent auto-reload
});
```

#### Page Filter Changes (`onFiltersUpdated` / `onFiltersUpdate`)

Fires when native filter cards on the same App Studio page (or dashboard) change. Register at the top level — outside any React component or `useEffect`.
Use `onFiltersUpdate` when available on newer `ryuu.js` versions, and fall back to `onFiltersUpdated` for compatibility.

```javascript
const registerFilterListener = (handler) => {
  try {
    if (typeof domo.onFiltersUpdate === "function") return domo.onFiltersUpdate(handler);
    if (typeof domo.onFiltersUpdated === "function") return domo.onFiltersUpdated(handler);
  } catch (_) {
    // Listener registry can be uninitialized in some runtimes.
  }
};

registerFilterListener((filters) => {
  if (!Array.isArray(filters) || filters.length === 0) return;

  filters.forEach(({ column, operand, values, dataType }) => {
    switch (column?.toUpperCase()) {
      case "YEAR_OF_EVENT":
        if (operand === "BETWEEN" && values?.length === 2) {
          state.yearRange = { min: Number(values[0]), max: Number(values[1]) };
        } else if (operand === "IN" && values.length > 0) {
          const nums = values.map(Number).sort((a, b) => a - b);
          state.yearRange = { min: nums[0], max: nums[nums.length - 1] };
        }
        break;
      case "CATEGORY":
        if (operand === "IN") {
          state.categories = values.length > 0 ? values : ["ALL"];
        }
        break;
    }
  });

  fetchData(); // Refetch immediately — no "apply" step for page filters
});
```

**Filter object shape** — each element in the `filters` array:

| Field | Type | Values |
|-------|------|--------|
| `column` | string | Dataset column name |
| `operand` | string | `BETWEEN`, `IN`, `GREATER_THAN_EQUAL`, `LESS_THAN_EQUAL`, `EQUALS` |
| `values` | array | For `BETWEEN`: `[min, max]`. For `IN`: selected values. For scalar: `[value]`. |
| `dataType` | string | `LONG`, `STRING`, `DATE`, etc. |

**The field is `operand`, not `operator`.** Incoming filters use `operand`. Outgoing filters (via `requestFiltersUpdate`) use `operator`. This asymmetry is a known Domo API inconsistency.

#### Variable Changes (`onVariablesUpdated`)

Fires when App Studio variable controls change. Variables are identified by numeric string IDs. Register at the top level.

```javascript
domo.onVariablesUpdated((variables) => {
  if (!variables || typeof variables !== "object") return;

  const typeVar = variables["860"];
  if (typeVar?.parsedExpression?.value) {
    const label = typeVar.parsedExpression.value; // display label, e.g., "Cumulative"
    state.pendingType = MY_LABEL_MAP[label];      // map to internal value
  }

  updateUI(); // Show pending state, don't refetch yet — wait for Apply
});
```

**Variable object shape** — `variables` is keyed by numeric function ID strings:

```javascript
{
  "858": { "parsedExpression": { "exprType": "LITERAL", "value": "Year Sold" } },
  "860": { "parsedExpression": { "exprType": "LITERAL", "value": "Cumulative" } }
}
```

Variables deliver display labels that need mapping to internal values. Use a pending/commit pattern: store in staging state on change, commit and refetch only when the user clicks Apply.

#### Update Variables Programmatically (`requestVariablesUpdate`)

Write App Studio variables from within a custom app. Primary use: dependent dropdowns — when variable A changes, set variable B.

```javascript
domo.requestVariablesUpdate(
  [{ functionId: 873, value: "Initial Service" }],
  (ack) => { console.log("acknowledged"); },
  (reply) => { console.log("completed"); }
);
```

**Loop prevention**: Updating a variable fires `onVariablesUpdated` again. Guard with a flag:

```javascript
state.isUpdatingVariable = true;
domo.requestVariablesUpdate(updates, onAck, (reply) => {
  state.isUpdatingVariable = false;
});
// In onVariablesUpdated: if (state.isUpdatingVariable) return;
```

The payload uses `functionId` (a number), not a string. The callbacks are `onAck` (queued) and `onReply` (completed).

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
