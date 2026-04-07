# App Studio Integration Reference

Production-tested patterns for pro-code custom apps interacting with App Studio page filters and variables. Derived from verified production deployments.

## Page Filter Listener — Complete Pattern

Register at the top level of your app, outside any React component or lifecycle hook. The handler must process every filter in the array, map column names to internal state keys, and trigger a data refetch.

```javascript
domo.onFiltersUpdated((filters) => {
  console.log("Filters received:", JSON.stringify(filters, null, 2));

  if (!Array.isArray(filters) || filters.length === 0) return;

  filters.forEach((filter) => {
    const { column, operand, values, dataType } = filter;

    switch (column?.toUpperCase()) {

      // Range filter (numeric) — handles BETWEEN, IN, and one-sided bounds
      case "YEAR_OF_EVENT":
      case "YEAROFEVENT":
      case "YEAR OF EVENT":
        if (operand === "BETWEEN" && values?.length === 2) {
          state.filters.yearOfEvent = { min: Number(values[0]), max: Number(values[1]) };
        } else if (operand === "IN" && Array.isArray(values) && values.length > 0) {
          const nums = values.map(Number).sort((a, b) => a - b);
          state.filters.yearOfEvent = { min: nums[0], max: nums[nums.length - 1] };
        } else if (operand === "GREATER_THAN_EQUAL" && values?.length >= 1) {
          state.filters.yearOfEvent.min = Number(values[0]);
        } else if (operand === "LESS_THAN_EQUAL" && values?.length >= 1) {
          state.filters.yearOfEvent.max = Number(values[0]);
        }
        break;

      // Categorical filter — IN with string values
      case "CONTRACT_LENGTH":
      case "CONTRACT_LENGTH_TEXT":
      case "CONTRACTLENGTH":
        if (operand === "IN" && Array.isArray(values)) {
          state.filters.contractLength = values.length > 0 ? values : ["ALL"];
        }
        break;

      // Boolean/scalar filter
      case "IS_SUBSCRIBER":
      case "ISSUBSCRIBER":
        if (values?.length >= 1) {
          state.filters.isSubscriber = Number(values[0]);
        }
        break;

      default:
        console.log(`Unknown filter column: "${column}" — skipping`);
    }
  });

  fetchData();
});
```

### Key Implementation Rules

1. **Register at top level**: `domo.onFiltersUpdated` must be called at the module's top scope. In React apps, this means outside any component — or in a `useEffect` with an empty dependency array, but only if the handler closes over mutable refs rather than stale state.

2. **Column name variants**: Domo may deliver column names in different formats depending on how the dataset was imported. Always `toUpperCase()` and handle common variants (underscored, camelCase, space-separated).

3. **Empty IN = ALL**: When a user clears all selections in a multi-select filter, Domo sends `operand: "IN"` with an empty `values` array. Treat this as "no filter" / "ALL".

4. **Immediate refetch**: Unlike variables (which stage), page filters should trigger an immediate data refetch. Users expect the visualization to update as soon as they change a filter.

5. **`operand` not `operator`**: The field name in the filter object is `operand`. Using `operator` will read `undefined`.

## Variable Listener — Complete Pattern

Variables arrive as a keyed object where keys are numeric function IDs (strings). Values contain a `parsedExpression.value` with the display label.

```javascript
// Label-to-internal-value mapping tables
const RETENTION_TYPE_MAP = {
  "Cumulative": "CUMULATIVE",
  "Marginal": "ADJUSTED_MARGINAL_RETENTION",
  "Lifetime": "LIFETIME",
};

const RETENTION_BASE_MAP = {
  "Days": "REMAINING_DAYS",
  "Months": "REMAINING_MONTHS",
  "Revenue Collected": "REMAINING_COLLECTED_DOLLARS",
  "Payments Collected": "REMAINING_COMPLETED_PAYMENTS",
};

const RETENTION_GROUP_MAP = {
  "Year Sold": "YEAR_SOLD",
  "Year of Event": "YEAR_OF_EVENT",
  "Billing Frequency": "BILLING_FREQUENCY_TEXT",
  "Contract Length": "CONTRACT_LENGTH_TEXT",
  "Area Name": "AREA_NAME",
  "State": "STATE",
  "Region": "REGION_NAME",
};

domo.onVariablesUpdated((variables) => {
  if (!variables || typeof variables !== "object") return;

  // Skip if we triggered this update ourselves
  if (state.isUpdatingVariable) return;

  const newPending = {
    retentionType: null,
    retentionBase: null,
    retentionGroup: null,
    eventType: null,
    eventSubtype: null,
  };

  // Retention Type (variable ID 860)
  const typeVar = variables["860"];
  if (typeVar?.parsedExpression?.value) {
    const label = typeVar.parsedExpression.value;
    const mapped = RETENTION_TYPE_MAP[label];
    if (mapped) newPending.retentionType = { label, value: mapped };
  }

  // Retention Base (variable ID 859)
  const baseVar = variables["859"];
  if (baseVar?.parsedExpression?.value) {
    const label = baseVar.parsedExpression.value;
    const mapped = RETENTION_BASE_MAP[label];
    if (mapped) newPending.retentionBase = { label, value: mapped };
  }

  // Retention Group (variable ID 858)
  const groupVar = variables["858"];
  if (groupVar?.parsedExpression?.value) {
    const label = groupVar.parsedExpression.value;
    const mapped = RETENTION_GROUP_MAP[label];
    if (mapped) newPending.retentionGroup = { label, value: mapped };
  }

  // Event Type (variable ID 872)
  const eventTypeVar = variables["872"];
  if (eventTypeVar?.parsedExpression?.value) {
    const eventTypeValue = eventTypeVar.parsedExpression.value;
    newPending.eventType = { label: eventTypeValue, value: eventTypeValue };

    // Dependent variable: when event type changes, fetch and update event subtypes
    if (state.lastFetchedEventType !== eventTypeValue) {
      state.lastFetchedEventType = eventTypeValue;
      fetchAndUpdateEventSubtypes(eventTypeValue);
    }
  }

  // Event Subtype (variable ID 873)
  const eventSubtypeVar = variables["873"];
  if (eventSubtypeVar?.parsedExpression?.value) {
    const val = eventSubtypeVar.parsedExpression.value;
    newPending.eventSubtype = { label: val, value: val };
  }

  state.pendingValues = newPending;
  updateUI();
});
```

### Key Implementation Rules

1. **Numeric string keys**: Variable IDs are always strings — `"858"`, not `858`. Access with bracket notation.

2. **parsedExpression.value**: The actual user-selected value is always at `variables[id].parsedExpression.value`. Check for existence of both `parsedExpression` and `value`.

3. **Label mapping is required**: Variables deliver display labels from the App Studio control (e.g., `"Days"`, `"Year Sold"`). The custom app must maintain a mapping table to translate these into the internal values used by its data queries.

4. **Pending/commit pattern**: Store variable changes in a `pendingValues` staging area. Only commit to active state (and refetch data) when the user clicks Apply. This prevents rapid-fire API calls while the user adjusts multiple controls.

5. **All variables arrive together**: When any single variable changes, `onVariablesUpdated` fires with the current state of ALL variables. Process them all each time.

## Variable Write-Back — Complete Pattern

Use `domo.requestVariablesUpdate` to update App Studio variables from within the custom app. The primary use case is dependent dropdowns — when one variable changes, fetch new options and set the dependent variable.

```javascript
async function fetchAndUpdateEventSubtypes(eventType) {
  const response = await domo.get(
    `/data/v1/eventTypes?fields=EVENT_SUBTYPE&filter=EVENT_TYPE="${eventType}"&groupby=EVENT_SUBTYPE&orderby=EVENT_SUBTYPE`
  );

  const subtypes = response
    .map(row => row.EVENT_SUBTYPE)
    .filter(val => val != null && val !== "")
    .sort();

  if (subtypes.length > 0) {
    updateVariable(873, subtypes[0]);
  }
}

function updateVariable(functionId, value) {
  state.isUpdatingVariable = true;

  domo.requestVariablesUpdate(
    [{ functionId, value }],
    (ack) => {
      // Acknowledged — update is queued
      setTimeout(() => { state.isUpdatingVariable = false; }, 500);
    },
    (reply) => {
      // Completed — safe to proceed
      state.isUpdatingVariable = false;
    }
  );
}
```

### Key Implementation Rules

1. **`functionId` not `variableId`**: The payload uses `functionId` (a number, not a string) to identify which variable to update.

2. **Loop guard**: Setting a variable triggers `onVariablesUpdated`. Without a guard flag (`isUpdatingVariable`), the app enters an infinite loop: update → listener fires → update → listener fires → ...

3. **Timeout fallback**: The `onAck` callback fires before `onReply`. Use a `setTimeout` in `onAck` as a safety net — if `onReply` never fires (edge case), the guard resets after 500ms.

4. **Dependent variable cascade**: When variable A changes, query the dataset for valid values of variable B, then call `requestVariablesUpdate` to set variable B. This keeps App Studio's variable controls in sync with the data.

## Apply Button Pattern

The apply button bridges pending variable changes and committed state. It commits all pending values, clears the staging area, updates the UI, and triggers a data refetch.

```javascript
function handleApply() {
  if (state.pendingValues.retentionBase) {
    state.retentionBase = state.pendingValues.retentionBase.value;
  }
  if (state.pendingValues.retentionType) {
    state.retentionType = state.pendingValues.retentionType.value;
  }
  if (state.pendingValues.retentionGroup) {
    state.grouping = state.pendingValues.retentionGroup.value;
  }
  if (state.pendingValues.eventType) {
    state.eventAType = state.pendingValues.eventType.value;
  }
  if (state.pendingValues.eventSubtype) {
    state.eventBType = state.pendingValues.eventSubtype.value;
  }

  // Clear pending
  state.pendingValues = {
    retentionType: null, retentionBase: null,
    retentionGroup: null, eventType: null, eventSubtype: null,
  };

  updateUI();
  fetchData();
}
```

Disable the Apply button when no pending values exist. Enable it as soon as any variable delivers a value different from the current committed state.

## React Integration Pattern

In React apps, the same patterns apply but use hooks. The `onVariablesUpdated` listener from the production React version:

```tsx
useEffect(() => {
  domo.onVariablesUpdated((variables) => {
    const newPending = { retentionType: null, retentionBase: null, ... };

    const typeVar = variables["860"];
    if (typeVar?.parsedExpression?.value) {
      const label = typeVar.parsedExpression.value;
      const mapped = RETENTION_TYPE_MAP[label];
      if (mapped) newPending.retentionType = { label, value: mapped };
    }

    // ... process other variables ...

    setPendingValues(newPending);
  });
}, []);

const handleApply = useCallback(() => {
  if (pendingValues.retentionBase) setRetentionBase(pendingValues.retentionBase.value);
  if (pendingValues.retentionType) setRetentionType(pendingValues.retentionType.value);
  // ... commit other values ...
}, [pendingValues]);
```

The listener registers once (empty dependency array). The `handleApply` callback depends on `pendingValues` and commits each pending value to the corresponding `useState` setter. State changes trigger re-renders that include the updated values in the next data fetch.

## Filter State Defaults

Initialize filter state with "ALL" or full-range defaults so that the app works correctly before any page filters are applied:

```javascript
const defaultFilters = {
  // Range filters — set to the widest expected range
  yearOfEvent: { min: 2016, max: 2025 },
  nationalPinScore: { min: 1, max: 20 },
  initialPrice: { min: 0, max: 3500 },

  // Boolean/scalar — set to the most common default
  isSubscriber: 1,

  // Categorical — "ALL" means no filter
  nationalPinQuartile: ["ALL"],
  contractLength: ["ALL"],
  billingFrequency: ["ALL"],
  subscriptionType: ["ALL"],
  areaName: ["ALL"],
  repPartnerName: ["ALL"],
};
```

When building a query (SQL, stored procedure, etc.), treat `["ALL"]` as "no filter" — omit the WHERE clause or pass NULL for that parameter.

## Data API v1 Filter Passthrough

For simple use cases, `domo.get("/data/v1/alias")` automatically respects page filters without requiring `onFiltersUpdated`. The platform applies active page filters server-side before returning data. This works for straightforward data reads but has limitations:

- Only applies to Data API v1 (`/data/v1/alias`) calls
- Does NOT apply to Code Engine calls (`/domo/codeengine/...`)
- Does NOT apply to SQL queries via SqlClient
- Does NOT give the app visibility into which filters are active
- Does NOT allow the app to transform or combine filter values before querying

Use `onFiltersUpdated` when you need to:
- Pass filter values as parameters to a stored procedure or Code Engine function
- Combine multiple filter values into a single query parameter
- Display active filter state in the app's UI
- Apply filters to non-Data-API data sources

## Checklist

Before publishing a pro-code app that integrates with App Studio filters/variables:

- [ ] `domo.onFiltersUpdated` registered at top level (if the app needs to react to page filters)
- [ ] Filter handler normalizes column names via `toUpperCase()`
- [ ] Filter handler uses `operand` (not `operator`)
- [ ] Empty `IN` values treated as "ALL"
- [ ] Filter changes trigger immediate data refetch
- [ ] `domo.onVariablesUpdated` registered at top level (if the app uses App Studio variables)
- [ ] Variable values extracted from `parsedExpression.value`
- [ ] Label-to-value mapping tables defined for all variable controls
- [ ] Pending/commit pattern implemented with Apply button
- [ ] Apply button disabled when no pending changes exist
- [ ] `isUpdatingVariable` guard prevents infinite loops on `requestVariablesUpdate`
- [ ] Content entry has `acceptFilters: true` and `acceptDateFilter: true`
- [ ] Default filter state covers the full range (app works before any filters are applied)
