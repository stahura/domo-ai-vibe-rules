# Rule: Domo App Platform Code Engine

You are building a Domo Custom App that needs to call a Code Engine function. Code Engine functions are server-side functions that have already been created in Domo — your job is to call them from the client-side app.

**Note:** This rule covers how to CALL Code Engine functions from your app, not how to write the server-side Code Engine code itself.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- Code Engine function(s) must already exist in Domo Code Engine
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

---

## Calling a Code Engine Function

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

// Example: call function with parameters
startFunction('myFunction', {
  parameter1: 'value1',
  parameter2: 123
});
```

The request body is simply an object with the input parameters:
```json
{
  "parameter1": "value1",
  "parameter2": 123
}
```

---

## manifest.json Configuration

Every Code Engine function your app calls MUST be declared in `manifest.json` under the `packageMapping` array.

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
    }
  ]
}
```

Key points:
- `packageMapping` is an **array** of function mappings
- Each function has an `alias` (used in API calls)
- `parameters` array defines inputs with `alias`, `type`, `nullable`, `isList`, and `children`
- `output` object defines the expected return structure
- The actual function ID is mapped at publish time in Domo Design Studio

---

## Input Parameters

You need to know what input parameters the Code Engine function expects. Check with whoever created the function, or look at the function configuration in Domo.

Parameter types include:
- `string`
- `number`
- `boolean`
- `object`
- `isList: true` for arrays

Example with different parameter types:
```javascript
domo.post('/domo/codeengine/v2/packages/processData', {
  userName: 'John',           // string
  userId: 12345,              // number
  isActive: true,             // boolean
  filters: ['a', 'b', 'c']    // array (isList: true)
});
```

---

## Output Types

**Important:** The output type varies based on how the Code Engine function was configured. It could be:
- A string
- A number
- A boolean
- An object
- An array

**You will likely need to test and inspect the actual response.** Check the browser console or Network tab to see what the function returns, then update your code accordingly.

```javascript
domo.post('/domo/codeengine/v2/packages/myFunction', { input: 'test' })
  .then(response => {
    // Inspect what you actually get back
    console.log('Response:', response);
    console.log('Type:', typeof response);

    // Then handle it appropriately based on actual structure
    // response might be: "success", 123, true, { result: "data" }, [1,2,3], etc.
  });
```

---

## Async/Await Pattern

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

// Usage
const result = await callCodeEngine('myFunction', { param1: 'value' });
```

---

## Checklist
- [ ] Code Engine function exists in Domo
- [ ] Function mapped in `manifest.json` under `packageMapping` array
- [ ] You know the expected input parameter names and types
- [ ] You've tested to confirm the actual output type/structure
- [ ] Function ID mapped in Domo Design Studio at publish time
