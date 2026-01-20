# Rule: Domo App Platform Workflow Integration

You are building a Domo Custom App that needs to trigger or interact with Domo Workflows. Workflows are automation pipelines in Domo that can orchestrate data operations, notifications, and integrations.

## Prerequisites
- The domo.js library must be available (included automatically when running in Domo)
- Workflows must be created in Domo's Workflow editor
- Workflows must be configured to allow triggering via API
- For local development, use `@domoinc/ryuu-proxy` to proxy API calls

## manifest.json Configuration

Every Workflow your app uses MUST be declared in `manifest.json` under the `workflowMapping` array.

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
      "alias": "workflow2",
      "parameters": [
        {
          "aliasedName": "thing1",
          "type": "number",
          "list": false,
          "value": 2,
          "children": null
        },
        {
          "aliasedName": "thing2",
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
- The workflow ID is mapped at publish time in the Domo Design Studio
- Use `list: true` for array parameters

---

## Triggering Workflows

### Basic workflow trigger
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

### Response format
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

### Trigger with parameters
```javascript
const result = await startWorkflow('sendReport', {
  reportType: 'weekly',
  recipients: ['team@example.com', 'manager@example.com']
});
console.log('Workflow ID:', result.id);
```

---

## Checking Workflow Status

### Get execution status
```javascript
// Use the 'id' from the start response
const workflowId = 'id-from-start-response';

domo.get(`/domo/workflow/v1/executions/${workflowId}`)
  .then(status => {
    console.log('Status:', status.state); // RUNNING, COMPLETED, FAILED
    console.log('Output:', status.output);
  });
```

### Poll for completion
```javascript
async function waitForWorkflow(workflowId, maxWaitMs = 60000) {
  const startTime = Date.now();

  while (Date.now() - startTime < maxWaitMs) {
    const status = await domo.get(`/domo/workflow/v1/executions/${workflowId}`);

    if (status.state === 'COMPLETED') {
      return { success: true, output: status.output };
    }

    if (status.state === 'FAILED') {
      return { success: false, error: status.error };
    }

    // Wait before polling again
    await new Promise(resolve => setTimeout(resolve, 2000));
  }

  return { success: false, error: 'Timeout waiting for workflow' };
}
```

---

## Common Patterns

### React hook for workflow management
```javascript
import { useState, useCallback } from 'react';

function useWorkflow(workflowAlias) {
  const [executing, setExecuting] = useState(false);
  const [lastExecution, setLastExecution] = useState(null);

  const trigger = useCallback(async (parameters = {}) => {
    setExecuting(true);

    try {
      const response = await domo.post(
        `/domo/workflow/v1/models/${workflowAlias}/start`,
        parameters
      );

      setLastExecution({
        id: response.id,
        modelName: response.modelName,
        status: response.status,
        startedAt: new Date()
      });

      return response.id;
    } catch (error) {
      console.error('Workflow trigger error:', error);
      throw error;
    } finally {
      setExecuting(false);
    }
  }, [workflowAlias]);

  const checkStatus = useCallback(async (workflowId) => {
    const status = await domo.get(`/domo/workflow/v1/executions/${workflowId}`);
    setLastExecution(prev => ({ ...prev, ...status }));
    return status;
  }, []);

  const triggerAndWait = useCallback(async (parameters = {}, maxWaitMs = 60000) => {
    const workflowId = await trigger(parameters);

    const startTime = Date.now();
    while (Date.now() - startTime < maxWaitMs) {
      const status = await checkStatus(workflowId);

      if (status.state === 'COMPLETED') {
        return { success: true, output: status.output };
      }
      if (status.state === 'FAILED') {
        return { success: false, error: status.error };
      }

      await new Promise(resolve => setTimeout(resolve, 2000));
    }

    return { success: false, error: 'Timeout' };
  }, [trigger, checkStatus]);

  return { trigger, checkStatus, triggerAndWait, executing, lastExecution };
}
```

### Workflow service
```javascript
// services/workflow.js
export const workflowService = {
  async calculate(num1, num2) {
    return domo.post('/domo/workflow/v1/models/workflow1/start', {
      num1, num2
    });
  },

  async sendReport(reportType, recipients) {
    return domo.post('/domo/workflow/v1/models/sendReport/start', {
      reportType, recipients
    });
  },

  async getStatus(workflowId) {
    return domo.get(`/domo/workflow/v1/executions/${workflowId}`);
  }
};
```

### UI component for workflow trigger
```javascript
function CalculateButton() {
  const { trigger, executing, lastExecution } = useWorkflow('workflow1');

  const handleClick = async () => {
    try {
      await trigger({ num1: 10, num2: 20 });
      // Optionally show success notification
    } catch (error) {
      // Handle error
    }
  };

  return (
    <div>
      <button onClick={handleClick} disabled={executing}>
        {executing ? 'Running...' : 'Calculate'}
      </button>
      {lastExecution && (
        <span>Status: {lastExecution.status}</span>
      )}
    </div>
  );
}
```

---

## Workflow Design Considerations

1. **Input Parameters**
   - Define parameters in manifest with `aliasedName` (not `alias` like Code Engine)
   - Use `list: true` for array inputs
   - Set default `value` when appropriate
   - Document required vs optional parameters

2. **Output Data**
   - Workflows can return output data
   - Keep output concise for API responses
   - Store large results in datasets/AppDB

3. **Error Handling**
   - Workflows should handle their own errors gracefully
   - Return meaningful error messages
   - Consider retry logic within workflows

4. **Timeouts**
   - Long-running workflows need appropriate timeout handling
   - Consider async patterns for very long operations
   - Provide progress updates via AppDB or other means

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

## Checklist
- [ ] Workflow(s) created in Domo Workflow editor
- [ ] Workflow mapped in `manifest.json` under `workflowMapping` array
- [ ] Each workflow has an `alias` used in API calls
- [ ] `parameters` array defines all inputs with `aliasedName` and correct types
- [ ] Use `list: true` for array parameters
- [ ] Workflow ID mapped in Domo Design Studio at publish time
- [ ] Error handling for trigger failures
- [ ] Status polling implemented if needed
- [ ] Timeout handling for long-running workflows
- [ ] User feedback (loading states, success/error messages)
