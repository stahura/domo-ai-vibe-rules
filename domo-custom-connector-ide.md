# Rule: Domo Custom Connector Development

You are building a custom Domo connector (data connector or writeback connector) using the Domo IDE. Custom connectors allow you to integrate external APIs and data sources into Domo.

**Note:** This rule covers custom connector development in the Domo IDE, not custom app development. Custom connectors run server-side after being published via the custom connector IDE

## Prerequisites
- Access to Domo's Custom Connector IDE
- Understanding of the external API you're integrating with
- Knowledge of JavaScript (connectors are written in JavaScript)

---

## File Structure

Custom connectors consist of JavaScript files:

- **`authentication.js`** — Validates credentials and authenticates with the external API
- **`dataProcessing.js`** — Fetches and processes data from the external API
- **`README.md`** — Documents available reports/parameters for the connector

All files should be written in JavaScript (`.js`).

---

## Common Patterns

### Authentication Pattern
```javascript
// Validate input format
let tokenFormat = /^[a-zA-Z0-9_-]+$/;
let accessToken = metadata.account.apikey;

if (tokenFormat.test(accessToken)) {
    httprequest.addHeader('Accept', 'application/json');
    httprequest.addHeader('Authorization', `Bearer ${accessToken}`);
    
    // Test authentication with a simple API call
    let res = httprequest.get('https://api.example.com/test');
    let statusCode = httprequest.getStatusCode();
    
    if (statusCode === 200) {
        auth.authenticationSuccess();
    } else {
        auth.authenticationFailed('Authentication failed. Please check your credentials.');
    }
} else {
    auth.authenticationFailed('Invalid token format.');
}
```

### Data Processing Pattern
```javascript
// Set headers
httprequest.addHeader('Accept', 'application/json');
httprequest.addHeader('Authorization', `Bearer ${metadata.account.apikey}`);

// Determine endpoint based on report selection
let endpoint = '';
switch(metadata.report) {
    case 'Report1':
        endpoint = 'https://api.example.com/data1';
        break;
    case 'Report2':
        endpoint = 'https://api.example.com/data2';
        break;
}

// Fetch and process data with pagination
let URL = endpoint;
do {
    let res = httprequest.get(URL);
    let statusCode = httprequest.getStatusCode();
    
    if (statusCode !== 200) {
        throw new Error(`API request failed: ${statusCode}`);
    }
    
    let responseData = JSON.parse(res);
    
    // Parse JSON array into Domo dataset
    datagrid.magicParseJSON(responseData.results);
    
    // Handle pagination
    URL = responseData.paging?.next?.link || false;
} while (URL);
```

### Error Handling
```javascript
try {
    let res = httprequest.get(url);
    let statusCode = httprequest.getStatusCode();
    
    if (statusCode !== 200) {
        let errorMsg = `Request failed: ${statusCode}`;
        try {
            let errorData = JSON.parse(res);
            if (errorData.message) {
                errorMsg = errorData.message;
            }
        } catch (e) {
            errorMsg += `. Response: ${res.substring(0, 200)}`;
        }
        throw new Error(errorMsg);
    }
    
    // Process successful response
    let data = JSON.parse(res);
    datagrid.magicParseJSON(data.results);
    
} catch (error) {
    // Handle error appropriately
    throw error;
}
```

---

## Important Notes

1. **Input Sanitization** — Always sanitize inputs (like API keys) to prevent cross-site scripting and SQL injection attacks
2. **Consistent Columns** — Every row in the dataset must have the same number of columns (use `null` for missing values)
3. **Use Domo-provided JavaScript Library** - These methods are provided by Domo in the Connector Dev Studio to make it easier for you to build your custom connector. You can reference them here: https://developer.domo.com/portal/e415bb99d21b2-reference
4. **JSON Parsing** — When APIs return JSON arrays, use `datagrid.magicParseJSON(jsonString)` instead of manual parsing
5. **Error Messages** — Provide clear, actionable error messages in `auth.authenticationFailed()`

---

## Checklist
- [ ] `authentication.js` validates input format and tests credentials
- [ ] `authentication.js` calls `auth.authenticationSuccess()` or `auth.authenticationFailed()` appropriately
- [ ] `dataProcessing.js` handles pagination correctly
- [ ] `dataProcessing.js` checks HTTP status codes before parsing JSON
- [ ] `dataProcessing.js` uses `datagrid.magicParseJSON()` for JSON arrays
- [ ] All inputs are sanitized to prevent security vulnerabilities
- [ ] Error handling provides clear messages
- [ ] `README.md` documents all available reports/parameters
- [ ] All rows have consistent column counts
