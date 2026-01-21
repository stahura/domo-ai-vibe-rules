# Rule: Domo App Platform Workflow Integration

You are building a Domo Custom App that needs to trigger Domo Workflows. Workflows are automation pipelines in Domo that can orchestrate data operations, notifications, and integrations.

**Important:** Workflows return success or failure only — they do NOT return data. If you need to get data back from a server-side operation, use Code Engine instead.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- Workflow(s) must be created in Domo's Workflow editor
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

---

## Triggering a Workflow

```javascript
const startWorkflow = async (workflowAlias, body) => {
  const instance = await domo.post(
    `/domo/workflow/v1/models/${workflowAlias}/start`,
    body
  );
  return instance;
};

// Example usage
const result = await startWorkflow('workflow1', {
  num1: 10,
  num2: 20
});
console.log('Workflow started:', result.id);
```

The request body contains the workflow parameters:
```json
{
  "parameter1": "value1",
  "parameter2": 123
}
```

---

## Response Format

```json
{
  "id": "2052e10a-d142-4391-a731-2be1ab1c0188",
  "modelId": "a8afdc89-9491-4ee4-b7c3-b9e9b86c0138",
  "modelName": "AddTwoNumbers",
  "modelVersion": "1.1.0",
  "createdBy": "8811501",
  "createdOn": "2023-11-15T15:28:57.479Z",
  "updatedBy": "8811501",
  "updatedOn": "2023-11-15T15:28:57.479Z",
  "status": "null"
}
```

Response fields:
- `id` - ID of this workflow execution
- `modelId` - ID of the workflow instance/definition
- `modelName` - Name of the workflow
- `modelVersion` - Workflow version number
- `createdBy` / `updatedBy` - User ID
- `status` - Execution status

---

## manifest.json Configuration

Every Workflow your app triggers MUST be declared in `manifest.json` under the `workflowMapping` array.

```json
{
  "name": "My Custom App",
  "version": "1.0.0",
  "size": {
    "width": 4,
    "height": 4
  },
  "workflowMapping": [
    {
      "alias": "workflow1",
      "parameters": [
        {
          "aliasedName": "num1",
          "type": "number",
          "list": false,
          "children": null
        },
        {
          "aliasedName": "num2",
          "type": "number",
          "list": false,
          "children": null
        }
      ]
    },
    {
      "alias": "sendReport",
      "parameters": [
        {
          "aliasedName": "reportType",
          "type": "string",
          "list": false,
          "children": null
        },
        {
          "aliasedName": "recipients",
          "type": "string",
          "list": true,
          "children": null
        }
      ]
    }
  ]
}
```

Key points:
- `workflowMapping` is an **array** of workflow mappings
- Each workflow has an `alias` (used in API calls)
- `parameters` array defines inputs with `aliasedName`, `type`, `list`, `value` (optional default), and `children`
- The workflow ID is mapped at publish time in Domo Design Studio
- Use `list: true` for array parameters

---

## Error Handling

```javascript
async function triggerWorkflow(alias, params) {
  try {
    const result = await domo.post(`/domo/workflow/v1/models/${alias}/start`, params);
    console.log('Workflow triggered successfully:', result.id);
    return { success: true, id: result.id };
  } catch (error) {
    console.error(`Workflow error (${alias}):`, error);
    return { success: false, error };
  }
}
```

---

## Use Cases for Workflows

1. **Data Refresh** - Trigger dataset refreshes on demand
2. **Report Generation** - Create and distribute reports
3. **Approval Processes** - Route items for approval with notifications
4. **Data Export** - Export data to external systems
5. **Notifications** - Send alerts via email, Slack, etc.
6. **Scheduled Operations** - Combine with Domo scheduling
7. **Multi-step Processes** - Orchestrate complex operations

---

## Design Considerations

1. **Input Parameters**
   - Define parameters in manifest with `aliasedName` (not `alias` like Code Engine)
   - Use `list: true` for array inputs
   - Set default `value` when appropriate

2. **No Data Return**
   - Workflows only return success/failure
   - If you need data back, use Code Engine instead
   - For results, have the workflow write to AppDB or a dataset

3. **Error Handling**
   - Always wrap workflow calls in try/catch
   - Provide user feedback on success/failure

4. **Long-Running Workflows**
   - Workflows may take time to complete
   - The trigger returns immediately — it doesn't wait for completion
   - Consider showing a "workflow started" message rather than waiting

---

## Checklist
- [ ] Workflow(s) created in Domo Workflow editor
- [ ] Workflow mapped in `manifest.json` under `workflowMapping` array
- [ ] Each workflow has an `alias` used in API calls
- [ ] `parameters` array defines all inputs with `aliasedName` and correct types
- [ ] Use `list: true` for array parameters
- [ ] Workflow ID mapped in Domo Design Studio at publish time
- [ ] Error handling for trigger failures
- [ ] User feedback (success/error messages)
