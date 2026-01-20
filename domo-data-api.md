# Rule: Domo App Platform Data API

You are building a Domo Custom App that needs to read data from Domo datasets. The Data API allows your app to query datasets that have been mapped in the manifest.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

## manifest.json Configuration

Every dataset your app uses MUST be declared in `manifest.json` under the `datasetsMapping` array. Each dataset is referenced by an alias (not the actual dataset ID).

```json
{
  "name": "My Custom App",
  "version": "1.0.0",
  "size": {
    "width": 4,
    "height": 4
  },
  "datasetsMapping": [
    {
      "alias": "sales",
      "dataSetId": "aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee",
      "fields": [
        {
          "alias": "amount",
          "columnName": "Sales Amount"
        },
        {
          "alias": "name",
          "columnName": "Client Name"
        },
        {
          "alias": "startDate",
          "columnName": "Contract Initiation Date"
        }
      ]
    },
    {
      "alias": "inventory",
      "dataSetId": "ffffffff-1111-2222-3333-444444444444",
      "fields": [
        {
          "alias": "sku",
          "columnName": "SKU"
        },
        {
          "alias": "quantity",
          "columnName": "Quantity On Hand"
        }
      ]
    }
  ]
}
```

Key points:
- `datasetsMapping` is an **array** of dataset objects
- Each dataset has an `alias` (used in API calls), `dataSetId` (GUID from Domo), and `fields`
- Note: `dataSetId` has a capital "S"
- `fields` is an array of objects with `alias` (used in code) and `columnName` (actual column name in dataset)
- Field aliases let you use simple names in code even if the dataset has spaces/special characters in column names

---

## Using domo.js to Query Data

### Basic Query (all data)
```javascript
// Using the alias defined in manifest.json
domo.get('/data/v1/sales')
  .then(data => {
    console.log(data); // Array of row objects
  });
```

### Query with SQL
```javascript
domo.post('/sql/v1/sales', 'SELECT date, SUM(amount) as total FROM sales GROUP BY date', {
  contentType: 'text/plain'
})
  .then(data => {
    console.log(data);
  });
```

**Important:** The SQL API does NOT interact with Domo page filters. If your app needs to respect page-level filtering applied by users in Domo dashboards, use the Data API (`/data/v1/`) instead of the SQL API.

### Query with Filters
```javascript
domo.get('/data/v1/sales?fields=date,amount&filter=region=West&orderby=date&limit=100')
  .then(data => {
    console.log(data);
  });
```

### Query Parameters
- `fields` - Comma-separated list of columns to return (use field aliases)
- `filter` - Filter expression (e.g., `region=West`, `amount>1000`)
- `groupby` - Group by columns
- `orderby` - Sort by column (prefix with `-` for descending)
- `limit` - Maximum rows to return
- `offset` - Skip N rows (for pagination)

---

## Local Development Setup

For local development, install and configure ryuu-proxy:

```bash
npm install --save-dev @domoinc/ryuu-proxy
```

Create or update your dev server to use the proxy. For Vite:

```javascript
// vite.config.js
import { defineConfig } from 'vite';
import { createProxyMiddleware } from '@domoinc/ryuu-proxy';

export default defineConfig({
  base: './',
  server: {
    proxy: {
      '/data': {
        target: 'https://your-instance.domo.com',
        changeOrigin: true,
        configure: (proxy, options) => {
          // ryuu-proxy handles auth
        }
      }
    }
  }
});
```

Run `domo login` first to authenticate your CLI.

---

## Common Patterns

### Fetch on component mount (React)
```javascript
import { useEffect, useState } from 'react';

function SalesChart() {
  const [data, setData] = useState([]);

  useEffect(() => {
    domo.get('/data/v1/sales')
      .then(setData)
      .catch(console.error);
  }, []);

  return <Chart data={data} />;
}
```

### Error handling
```javascript
domo.get('/data/v1/sales')
  .then(data => {
    if (!data || data.length === 0) {
      console.warn('No data returned');
      return [];
    }
    return data;
  })
  .catch(error => {
    console.error('Data API error:', error);
    // Handle error appropriately
  });
```

---

## Checklist
- [ ] Dataset(s) declared in `manifest.json` under `datasetsMapping` array
- [ ] Each dataset has a unique `alias`
- [ ] `dataSetId` (capital S) contains valid GUID from your Domo instance
- [ ] `fields` array maps `alias` to `columnName` for each field you need
- [ ] Using alias (not dataset ID) in API calls
- [ ] Error handling in place for API calls
- [ ] Local dev proxy configured if developing outside Domo
