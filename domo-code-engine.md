# Rule: Domo App Platform Code Engine

You are building a Domo Custom App that needs server-side functionality. Code Engine allows you to run backend code (JavaScript/Node.js functions) that can securely access secrets, call external APIs, and perform operations that shouldn't happen in the browser.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- Code Engine functions must be created in the Domo Code Engine editor
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

## manifest.json Configuration

Every Code Engine function your app uses MUST be declared in `manifest.json` under the `packageMapping` array.

```json
{
  "name": "My Custom App",
  "version": "1.0.0",
  "size": {
    "width": 4,
    "height": 4
  },
  "packageMapping": [
    {
      "alias": "awesomeFunction",
      "parameters": [
        {
          "alias": "number1AppInput",
          "type": "number",
          "nullable": false,
          "isList": false,
          "children": null
        },
        {
          "alias": "number2AppInput",
          "type": "number",
          "nullable": false,
          "isList": false,
          "children": null
        }
      ],
      "output": {
        "alias": "sumAppOutput",
        "type": "number",
        "children": null
      }
    },
    {
      "alias": "sendEmail",
      "parameters": [
        {
          "alias": "to",
          "type": "string",
          "nullable": false,
          "isList": false,
          "children": null
        },
        {
          "alias": "subject",
          "type": "string",
          "nullable": false,
          "isList": false,
          "children": null
        },
        {
          "alias": "body",
          "type": "string",
          "nullable": false,
          "isList": false,
          "children": null
        }
      ],
      "output": {
        "alias": "result",
        "type": "object",
        "children": null
      }
    }
  ]
}
```

Key points:
- `packageMapping` is an **array** of function mappings
- Each function has an `alias` (used in API calls)
- `parameters` array defines inputs with `alias`, `type`, `nullable`, `isList`, and `children`
- `output` object defines the return value structure with `alias`, `type`, and `children`
- The function ID is mapped at publish time in the Domo Design Studio

---

## Calling Code Engine Functions

### Basic function call
```javascript
const startFunction = (functionAlias, inputParameters = {}) => {
  domo.post(`/domo/codeengine/v2/packages/${functionAlias}`, inputParameters)
    .then(data => {
      console.log(data);
    })
    .catch(err => {
      console.log(err);
    });
};

// Example usage
startFunction('awesomeFunction', {
  number1AppInput: 5,
  number2AppInput: 10
});
```

### With async/await
```javascript
async function callCodeEngine(alias, params) {
  try {
    const result = await domo.post(`/domo/codeengine/v2/packages/${alias}`, params);
    return result;
  } catch (error) {
    console.error(`Code Engine error (${alias}):`, error);
    throw error;
  }
}

// Example usage
const sum = await callCodeEngine('awesomeFunction', {
  number1AppInput: 5,
  number2AppInput: 10
});
console.log(sum); // Returns the output defined in Code Engine function
```

### Sending email example
```javascript
domo.post('/domo/codeengine/v2/packages/sendEmail', {
  to: 'user@example.com',
  subject: 'Report Ready',
  body: 'Your daily report is ready to view.'
})
  .then(response => {
    console.log('Email sent:', response);
  });
```

---

## Writing Code Engine Functions

Code Engine functions are written in JavaScript/Node.js and run server-side in the Domo Code Engine editor.

### Basic function structure
```javascript
// In Code Engine editor
const codeengine = require('codeengine');

async function myFunction(request, response) {
  const { number1AppInput, number2AppInput } = request.body;

  // Perform calculation
  const sum = number1AppInput + number2AppInput;

  // Return result (matches output defined in manifest/Code Engine config)
  response.json({ sumAppOutput: sum });
}

module.exports = myFunction;
```

### Accessing secrets securely
```javascript
const codeengine = require('codeengine');

async function sendEmail(request, response) {
  const { to, subject, body } = request.body;

  // Access secrets securely (never exposed to client)
  const apiKey = await codeengine.getSecret('SENDGRID_API_KEY');

  // Call external API
  const result = await fetch('https://api.sendgrid.com/v3/mail/send', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${apiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      personalizations: [{ to: [{ email: to }] }],
      from: { email: 'noreply@company.com' },
      subject,
      content: [{ type: 'text/plain', value: body }]
    })
  });

  response.json({ success: true, status: result.status });
}

module.exports = sendEmail;
```

### Accessing Domo data from Code Engine
```javascript
const codeengine = require('codeengine');

async function processData(request, response) {
  // Query a dataset
  const data = await codeengine.sendRequest('get', '/data/v1/sales?limit=1000');

  // Process and return
  const summary = data.reduce((acc, row) => {
    acc.total += row.amount;
    acc.count += 1;
    return acc;
  }, { total: 0, count: 0 });

  response.json(summary);
}

module.exports = processData;
```

---

## Common Patterns

### React service for Code Engine
```javascript
// services/codeEngine.js
export const codeEngineService = {
  async calculate(num1, num2) {
    return domo.post('/domo/codeengine/v2/packages/awesomeFunction', {
      number1AppInput: num1,
      number2AppInput: num2
    });
  },

  async sendEmail(to, subject, body) {
    return domo.post('/domo/codeengine/v2/packages/sendEmail', {
      to, subject, body
    });
  },

  async fetchExternalData(params) {
    return domo.post('/domo/codeengine/v2/packages/fetchExternalData', params);
  }
};
```

### Error handling
```javascript
async function callCodeEngine(functionAlias, payload) {
  try {
    const response = await domo.post(
      `/domo/codeengine/v2/packages/${functionAlias}`,
      payload
    );
    return { success: true, data: response };
  } catch (error) {
    console.error(`Code Engine error (${functionAlias}):`, error);

    // Handle specific error types
    if (error.status === 504) {
      return { success: false, error: 'Function timed out' };
    }
    if (error.status === 500) {
      return { success: false, error: 'Server error in function' };
    }

    return { success: false, error: error.message || 'Unknown error' };
  }
}
```

---

## Use Cases for Code Engine

1. **Secure API Calls** - Store API keys as secrets, call external services
2. **Data Processing** - Heavy computations that would be slow in browser
3. **Email/Notifications** - Send emails via SendGrid, Slack messages, etc.
4. **Data Aggregation** - Combine data from multiple sources
5. **Webhooks** - Receive and process webhook payloads
6. **Scheduled Tasks** - Run periodic jobs (with Domo Workflows)

---

## Checklist
- [ ] Code Engine function(s) created in Domo Code Engine editor
- [ ] Function mapped in `manifest.json` under `packageMapping` array
- [ ] Each function has an `alias` used in API calls
- [ ] `parameters` array defines all input fields with correct types
- [ ] `output` object defines the return structure
- [ ] Secrets stored securely in Code Engine (not in app code)
- [ ] Proper error handling for function calls
- [ ] Timeout handling for long-running functions
- [ ] Function ID mapped in Domo Design Studio at publish time
