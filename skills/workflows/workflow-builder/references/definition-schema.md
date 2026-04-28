# Workflow Definition Schema (v2)

Notes on the workflow definition JSON structure for `update-definition` and `validate`.

## Authoring Strategy

1. Build the definition incrementally — start with the happy path (root → steps → end), then add branches and loops.
2. Call `validate` after each major change. The validator returns structural errors that are easier to fix incrementally.
3. For dataset-query steps, use `validate-dataset-query` to confirm SQL validity in context.
4. Use `get-definition` to inspect what's stored after a push (useful for debugging mismatches between what you sent and what Domo accepted).

## Top-Level Shape

```json
{
  "version": 2,
  "designElements": [ ... ],
  "dataList": [ ... ],
  "schema": {
    "input": [ ... ],
    "output": [ ... ]
  }
}
```

- `**designElements**` — All nodes AND edges in a flat array (not separated).
- `**dataList**` — Workflow-scoped variables (parameters) referenced across steps.
- `**schema.input**` — Parameters the workflow accepts at start time (mapped from a form or trigger).
- `**schema.output**` — Parameters the workflow exposes on completion.

---

## Nodes

### rootNode (Start)

**Without a form** (trigger-only or programmatic start):

```json
{
  "id": "startNode_1",
  "type": "rootNode",
  "position": { "x": 400, "y": 0 },
  "data": {
    "_designNode": "rootNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "Start"
  }
}
```

**With a start form** (user submits a form to launch the workflow):

```json
{
  "id": "startNode_1",
  "type": "rootNode",
  "position": { "x": 400, "y": 0 },
  "data": {
    "_designNode": "rootNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "Start",
    "configType": "form",
    "formId": "<uuid from create-form response>",
    "isFormStart": true,
    "input": [
      {
        "id": "<form-field-uuid from create-form response>",
        "formFieldId": "<form-field-uuid from create-form response>",
        "paramName": "<form field alias>",
        "displayName": "<human-readable label>",
        "visible": true,
        "acceptsInput": false,
        "required": true,
        "mappedTo": "<dataList-variable-id>",
        "value": null,
        "dataType": "text",
        "isList": false,
        "customMappingType": "form_start",
        "flag": "input",
        "configType": "form"
      }
    ]
  }
}
```

**Key rules for form-start rootNode:**

- `isFormStart` must be `true`.
- `customMappingType` on each input entry must be `"form_start"` (NOT `"form"` — that's for userTaskNode).
- `acceptsInput` must be `false` and `visible` must be `true` on every input entry.
- `mappedTo` holds the dataList variable ID; `value` must be `null`.
- `paramName` must match the `alias` field set on the corresponding form field when you called `create-form`. This is how form fields link to workflow variables.
- `id` and `formFieldId` on each entry should both be the form field's UUID (from the `create-form` response — not self-generated).

### endNode

```json
{
  "id": "endNode_1",
  "type": "endNode",
  "data": {
    "_designNode": "endNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "End"
  }
}
```

### serviceTaskNode (Code Engine function call)

```json
{
  "id": "node_myStep",
  "type": "serviceTaskNode",
  "position": { "x": 400, "y": 200 },
  "data": {
    "_designNode": "serviceTaskNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "Send Email",
    "description": "<function description from get-function-signature>",
    "taskType": "nebulaFunction",
    "metadata": {
      "packageId": "<package-uuid>",
      "functionName": "sendEmail",
      "version": "<exact version string e.g. 2.1.13>",
      "settings": {}
    },
    "selectedTaskTitle": "<function displayName from get-function-signature>",
    "selectedTaskDescription": "<function description from get-function-signature>",
    "usesStructuredOutputs": false,
    "input": [
      {
        "id": "<unique 15-char alphanumeric e.g. aBcDeFgHiJkLmNo>",
        "paramName": "recipientEmails",
        "displayName": "recipientEmails",
        "visible": true,
        "customMappingType": null,
        "dataType": "text",
        "isList": false,
        "value": "person@example.com",
        "mappedTo": null,
        "aiDescription": null,
        "children": [],
        "configType": null,
        "entitySubType": null,
        "flag": "input",
        "required": false
      },
      {
        "id": "<unique 15-char alphanumeric>",
        "paramName": "subject",
        "displayName": "subject",
        "visible": true,
        "customMappingType": null,
        "dataType": "text",
        "isList": false,
        "value": null,
        "mappedTo": "var_mySubjectVariable",
        "aiDescription": null,
        "children": [],
        "configType": null,
        "entitySubType": null,
        "flag": "input",
        "required": false
      }
    ],
    "output": [
      {
        "id": "<unique 15-char alphanumeric>",
        "paramName": "isSent",
        "displayName": "isSent",
        "visible": true,
        "customMappingType": null,
        "dataType": "boolean",
        "isList": false,
        "value": null,
        "mappedTo": "var_emailSent",
        "aiDescription": null,
        "children": [],
        "configType": null,
        "entitySubType": null,
        "flag": "output",
        "required": false
      }
    ]
  },
  "style": { "zIndex": 3, "outline": "none" },
  "index": 1,
  "type": "serviceTaskNode"
}
```

**Key rules:**

- **Always call `get-function-signature` first.** `paramName` on every input/output must exactly match the CE function's declared parameter name. Mismatches fail silently at runtime.
- `**metadata.settings: {}`** is required. Omitting it causes tiles to show "Version: undefined" in the UI.
- `**selectedTaskTitle` and `selectedTaskDescription**` must be set on `data` (from the function's `displayName` and `description` fields in `get-function-signature`). These are what make the PARAMETERS & MAPPING panel render in the UI. Do NOT put `displayName` inside `metadata`.
- **Input/output entry `id`** must be a unique 15-character alphanumeric string (e.g. `"aBcDeFgHiJkLmNo"`). If omitted, the API falls back to the `paramName` string, which breaks UI rendering of the parameter list.
- `**mappedTo` vs `value**`: For variable-mapped entries, set `"mappedTo": "<dataList-var-id>"` and `"value": null`. For literal values, set `"value": "<literal>"` and `"mappedTo": null`. Never put a variable ID in `value`.
- `**dataType**` must match the function signature type — `"dataset"`, `"DIRECTORY"`, `"person"`, `"group"`, `"object"`, `"text"`, `"number"`, `"decimal"`, `"boolean"` etc. Do not default everything to `"text"`.
- **`DIRECTORY` naming note:** `DIRECTORY` is the API/`dataType` name for what users now see as **Documents** in the Domo UI (previously called **FileSets** — the `DOMO FileSets` package function names and `/api/files/v1/filesets/...` endpoint paths still use the old name). All three terms refer to the same resource. Use `DIRECTORY` in the workflow `dataType` field regardless of UI rename.
- **Literal `value` shape by `dataType`** (when passing a literal, not `mappedTo`):

  | `dataType`        | `value` shape                                          | Example                                                                                          |
  | ----------------- | ------------------------------------------------------ | ------------------------------------------------------------------------------------------------ |
  | `dataset`         | bare UUID string                                       | `"value": "b8d2fb52-c949-47f7-bff3-cf37e815194d"`                                                |
  | `person`          | bare user-id string                                    | `"value": "1317417586"`                                                                          |
  | `group`           | bare group-id string                                   | `"value": "1234567"`                                                                             |
  | `DIRECTORY`       | full entity `{id, type, subType, path, name}`          | `"value": {"id": "92599d92-…", "type": "DIRECTORY", "subType": null, "path": "", "name": null}` |
  | `text` / `number` / `decimal` / `boolean` | the typed literal                  | `"value": 1234.56`, `"value": true`                                                              |

  Confusing-the-shapes errors:
  - `dataset` with entity wrapper → `Cannot deserialize value of type java.util.UUID from Object value`.
  - `DIRECTORY` with bare UUID string → `Cannot construct instance of Entity ... no String-argument constructor`.
  - `DIRECTORY` entity missing `path` → `Path must be provided for DIRECTORY type`.
- `**isList: true` params require array values** — e.g. `"value": ["userId1"]`, not `"value": "userId1"`. Passing a string for a list param causes a 400 deserialization error.
- **No `mappingType` field** on input/output entries. The UI does not set it; omit it entirely.
- `**displayName`** on each entry should be the lowercase param name (matching the CE function signature's `displayName` field, e.g. `"recipientEmails"` not `"Recipient Emails"`).
- `**description` on node data** should be the function's description string (same value as `selectedTaskDescription`).

**Email body as rich text:** The `sendEmail` function's `body` input accepts a Slate rich-text array as its `value`, allowing inline variable interpolation without a separate string-concatenation step:

```json
{
  "paramName": "body",
  "displayName": "body",
  "value": [
    {
      "type": "paragraph",
      "children": [
        { "text": "Hello, ", "bold": false, "italic": false, "underlined": false, "sql": false },
        {
          "type": "variable",
          "children": [{ "text": "", "bold": false, "italic": false, "underlined": false, "sql": false }],
          "dataType": "text",
          "id": "var_personName",
          "name": "personName",
          "isList": false
        },
        { "text": "!", "bold": false, "italic": false, "underlined": false, "sql": false }
      ]
    }
  ],
  "mappedTo": null
}
```

**CRITICAL — two Slate interpolation rules.** Either rule violated and the variable renders as the literal `name` string (e.g. the email body shows the literal text `personName` instead of the resolved value):

1. **Variables must be INLINE children of a paragraph that also contains the surrounding text.** A variable in its own paragraph (e.g. `[paragraph(text), paragraph(var), paragraph(text)]`) does NOT interpolate. Correct: `[paragraph(text, var, text, var, text)]` — ONE paragraph, multiple inline children, as in the example above. This applies to multi-line HTML email bodies too: keep ALL the text + variable children inside a single `paragraph`, not split across multiple paragraphs.
2. **For child-variable references (object sub-fields), `name` must be the FULL DOTTED PATH, not the leaf.** A variable with `id: "var_currentFile.id"` needs `name: "currentFile.id"`, NOT `name: "id"`. Top-level variables use the leaf (`id: "var_personName"` → `name: "personName"`). Foolproof helper: `name = id.replace(/^var_/, "")`.

The same rules apply to AI_AGENT `data.prompt.value`, conditionEdge `data.advancedRule`, and any other input that accepts a Slate array as its `value`.

### serviceTaskNode (Dataset Query)

```json
{
  "id": "node_queryData",
  "type": "serviceTaskNode",
  "data": {
    "_designNode": "serviceTaskNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "Query Sales Data",
    "implementationType": "DATASET_QUERY",
    "implementation": {
      "datasetId": "<dataset-uuid>",
      "query": "SELECT region, SUM(amount) AS total FROM sales_table GROUP BY region"
    },
    "inputs": [],
    "outputs": [
      {
        "name": "result",
        "mappingType": "VARIABLE",
        "customMappingType": "",
        "value": "<dataList-variable-id>"
      }
    ]
  }
}
```

### userTaskNode (Human Task / Approval Step)

A `userTaskNode` pauses the workflow and presents a form to a specific user, group, or queue for completion. The node is wired to a task form created via `create-form`.

```json
{
  "id": "node_approvalTask",
  "type": "userTaskNode",
  "position": { "x": 80, "y": 220 },
  "data": {
    "dimensions": { "width": 200, "height": 60 },
    "title": "Approval Task",
    "_designNode": "userTaskNode",
    "configType": "form",
    "selectedUserTaskTitle": "Task Form Title",
    "selectedUserTaskDescription": "",
    "input": [],
    "output": [],
    "fieldOptions": [],
    "formId": "<uuid-from-create-form-response>",
    "selectedQueue": "<queue-uuid>",
    "assignedTo": {
      "aiDescription": null,
      "children": [],
      "configType": null,
      "customMappingType": null,
      "dataType": "person",
      "displayName": "Assigned To",
      "entitySubType": null,
      "flag": "input",
      "id": "<unique-15-char-id>",
      "isList": false,
      "mappedTo": null,
      "paramName": "DOMO_ASSIGNED_TO_",
      "required": true,
      "value": "<user-id-as-string>",
      "visible": true
    }
  },
  "style": { "zIndex": 3, "outline": "none" },
  "index": 1,
  "type": "userTaskNode"
}
```

**Key rules:**

- `configType` must be `"form"` (not `null`). Missing or null causes ODY_048.
- `formId` must be the UUID returned from `create-form` — not a UUID you invented. See `references/api-reference.md`.
- `selectedQueue` must reference a queue that exists in the instance. A queue from another instance causes ODY_046. Resolve with `queues list`.
- `assignedTo.value` is a user ID (string). The user must have permission to be assigned workflow tasks. If not, validation returns ODY_033. Use `users list` to find a valid assignee.
- `input` entries feed workflow variable values INTO the form (displayed to the assignee). `output` entries capture what the assignee fills in and write it back to workflow variables.
- A single field can be listed in BOTH `input` and `output` — that's how you pre-fill an editable field with the current value of a workflow variable (e.g. show a requested budget but let the approver adjust it). The form field itself must have `acceptsInput: true, acceptsOutput: true` for this to render correctly.
- `customMappingType` on userTaskNode input/output entries is `"form"` (NOT `"form_start"` — that's rootNode only).
- `mappedTo` holds the dataList variable ID on both inputs and outputs; `value` must be `null`.
- **Form-side vs node-side wiring must agree.** If a form field has `readOnly: true, acceptsInput: true, acceptsOutput: false`, it MUST be listed in `userTaskNode.input[]` (not `output`). Mismatches produce confusing "field disappeared" symptoms at runtime. See `api-reference.md` for the role/flag table.

**userTaskNode input/output entry shape:**

```json
{
  "id": "<form-field-uuid from create-form response>",
  "formFieldId": "<form-field-uuid from create-form response>",
  "paramName": "<form field alias>",
  "displayName": "<human-readable label>",
  "visible": true,
  "mappedTo": "<dataList-variable-id>",
  "value": null,
  "dataType": "text",
  "isList": false,
  "customMappingType": "form",
  "flag": "input",
  "configType": "form"
}
```

### Worked example — userTaskNode with mixed read-only and response fields

This is the canonical shape for an approval task form where the assignee sees some pre-populated values (read-only), can edit a pre-filled value, and fills in a brand-new decision. The **form** declares all five fields; the **userTaskNode** splits them across `input[]` and `output[]` based on which direction data flows.

**Form side** (sent to `POST /forms/v2`):

```json
{
  "name": "Event Approval",
  "domainId": "<workflow-id> - 1",
  "domainType": "WORKFLOW",
  "sections": [{
    "id": "<section-uuid>",
    "title": "",
    "description": "",
    "fields": [
      {
        "id": "<field-uuid-eventName>",
        "label": "Event Name",
        "fieldType": "SHORT_ANSWER", "dataType": "text",
        "acceptsInput": true, "acceptsOutput": false, "readOnly": true,
        "alias": "eventName",
        "optional": true, "options": {},
        "useExternalValues": false, "displayAsDropdown": false, "isList": false
      },
      {
        "id": "<field-uuid-budget>",
        "label": "Budget",
        "fieldType": "SHORT_ANSWER", "dataType": "number",
        "acceptsInput": true, "acceptsOutput": true,
        "alias": "budget", "defaultValue": 0,
        "optional": false, "options": {},
        "useExternalValues": false, "displayAsDropdown": false, "isList": false
      },
      {
        "id": "<field-uuid-notes>",
        "label": "Requester Notes",
        "fieldType": "PARAGRAPH", "dataType": "text",
        "acceptsInput": true, "acceptsOutput": false, "readOnly": true,
        "alias": "requesterNotes",
        "optional": true, "options": {},
        "useExternalValues": false, "displayAsDropdown": false, "isList": false
      },
      {
        "id": "<field-uuid-approved>",
        "label": "Approved",
        "fieldType": "SINGLE_CHOICE", "dataType": "text",
        "acceptsInput": false, "acceptsOutput": true,
        "alias": "approved",
        "optional": false,
        "options": { "values": ["Yes", "No"], "acceptsOther": false },
        "useExternalValues": false, "displayAsDropdown": false, "isList": false
      },
      {
        "id": "<field-uuid-approvalNotes>",
        "label": "Approval Notes",
        "fieldType": "PARAGRAPH", "dataType": "text",
        "acceptsInput": false, "acceptsOutput": true,
        "alias": "approvalNotes",
        "optional": true, "options": {},
        "useExternalValues": false, "displayAsDropdown": false, "isList": false
      }
    ]
  }],
  "settings": {},
  "attributes": [{ "type": "paragraph", "children": [{ "text": "" }] }],
  "fieldConfiguration": {
    "<field-uuid-eventName>":     { "targetMapping": { "target": "eventName" } },
    "<field-uuid-budget>":        { "targetMapping": { "target": "budget" } },
    "<field-uuid-notes>":         { "targetMapping": { "target": "requesterNotes" } },
    "<field-uuid-approved>":      { "targetMapping": { "target": "approved" } },
    "<field-uuid-approvalNotes>": { "targetMapping": { "target": "approvalNotes" } }
  },
  "submitConfiguration": { "type": "UNASSIGNED", "isDatasetOwner": false },
  "submitConfigurationType": "UNASSIGNED",
  "searchable": false
}
```

**Node side** (inside `userTaskNode.data` in the workflow definition):

```json
{
  "input": [
    { "id": "<field-uuid-eventName>", "formFieldId": "<field-uuid-eventName>",
      "paramName": "eventName", "displayName": "Event Name",
      "mappedTo": "var_eventName", "value": null,
      "dataType": "text", "isList": false,
      "customMappingType": "form", "flag": "input", "configType": "form", "visible": true },
    { "id": "<field-uuid-budget>", "formFieldId": "<field-uuid-budget>",
      "paramName": "budget", "displayName": "Budget",
      "mappedTo": "var_budget", "value": null,
      "dataType": "number", "isList": false,
      "customMappingType": "form", "flag": "input", "configType": "form", "visible": true },
    { "id": "<field-uuid-notes>", "formFieldId": "<field-uuid-notes>",
      "paramName": "requesterNotes", "displayName": "Requester Notes",
      "mappedTo": "var_requesterNotes", "value": null,
      "dataType": "text", "isList": false,
      "customMappingType": "form", "flag": "input", "configType": "form", "visible": true }
  ],
  "output": [
    { "id": "<field-uuid-budget>", "formFieldId": "<field-uuid-budget>",
      "paramName": "budget", "displayName": "Budget",
      "mappedTo": "var_budget", "value": null,
      "dataType": "number", "isList": false,
      "customMappingType": "form", "flag": "output", "configType": "form", "visible": true },
    { "id": "<field-uuid-approved>", "formFieldId": "<field-uuid-approved>",
      "paramName": "approved", "displayName": "Approved",
      "mappedTo": "var_approved", "value": null,
      "dataType": "text", "isList": false,
      "customMappingType": "form", "flag": "output", "configType": "form", "visible": true },
    { "id": "<field-uuid-approvalNotes>", "formFieldId": "<field-uuid-approvalNotes>",
      "paramName": "approvalNotes", "displayName": "Approval Notes",
      "mappedTo": "var_approvalNotes", "value": null,
      "dataType": "text", "isList": false,
      "customMappingType": "form", "flag": "output", "configType": "form", "visible": true }
  ]
}
```

Notes on this shape:

- `eventName` and `requesterNotes` appear only in `input[]` — the assignee sees them as read-only text because the form field has `readOnly: true`.
- `budget` appears in BOTH `input[]` and `output[]` — it is pre-filled with the current value of `var_budget` AND the assignee's edited value is written back to the same variable. The form field has `acceptsInput: true, acceptsOutput: true` (no `readOnly`).
- `approved` and `approvalNotes` appear only in `output[]` — fresh responses from the assignee. The form fields have `acceptsInput: false, acceptsOutput: true`.
- Every field UUID appears in `fieldConfiguration` under its alias — copy the `alias` from the form body into `targetMapping.target`.
- `submitConfiguration.type` is `"UNASSIGNED"` for user-task forms (NOT `"WORKFLOW"` — that's only for start forms).

### AI_AGENT node (Agent with instructions, tools, knowledge, structured output)

An AI Agent runs an LLM with four configurable parts, mirroring the three tabs of the agent editor in the UI:

- **General** — `prompt` (rich-text, supports inline workflow variables), `instructions` (system prompt), and the agent's `result` shape. The model itself is set globally by the AI Service Layer, not on the node.
- **Tools** — built-in or CE functions the agent may call. Each tool can pin specific inputs to a static value or leave them blank for the agent to fill at runtime, and may carry per-input descriptions to guide the agent.
- **Knowledge** — attached datasets, FileSets (directories), and individual files the agent may read.

Both `type` and `_designNode` are `"AI_AGENT"` — this is its own node kind, not a `serviceTaskNode`.

```json
{
  "id": "node_invoiceAgent",
  "type": "AI_AGENT",
  "position": { "x": 80, "y": 220 },
  "data": {
    "_designNode": "AI_AGENT",
    "dimensions": { "width": 200, "height": 60 },
    "title": "agent",
    "description": "",
    "prompt": {
      "id": "<unique-15-char-id>",
      "paramName": "prompt",
      "displayName": "Prompt",
      "dataType": "text",
      "isList": false,
      "flag": "input",
      "required": true,
      "visible": true,
      "mappedTo": null,
      "value": [
        {
          "type": "paragraph",
          "children": [
            { "text": "FileID: ", "bold": false, "italic": false, "underlined": false, "sql": false },
            {
              "type": "variable",
              "children": [{ "text": "", "bold": false, "italic": false, "underlined": false, "sql": false }],
              "dataType": "number",
              "id": "<dataList-variable-id>",
              "name": "fileID",
              "isList": false
            },
            { "text": "", "bold": false, "italic": false, "underlined": false, "sql": false }
          ]
        }
      ],
      "aiDescription": null,
      "children": [],
      "configType": null,
      "customMappingType": null,
      "entitySubType": null
    },
    "result": {
      "id": "<unique-15-char-id>",
      "paramName": "result",
      "displayName": "Result",
      "dataType": "object",
      "isList": false,
      "flag": "output",
      "required": true,
      "visible": true,
      "mappedTo": "<dataList-object-variable-id>",
      "value": null,
      "aiDescription": null,
      "configType": null,
      "customMappingType": null,
      "entitySubType": null,
      "children": [
        {
          "id": "<dataList-object-variable-id>.<unique-15-char-id>",
          "paramName": "Vendor",
          "dataType": "text",
          "isList": false,
          "flag": "output",
          "required": true,
          "visible": true,
          "mappedTo": "<dataList-object-variable-id>.<child-id>",
          "value": null,
          "displayName": "",
          "aiDescription": null,
          "configType": null,
          "customMappingType": null,
          "entitySubType": null,
          "children": []
        },
        {
          "id": "<dataList-object-variable-id>.<unique-15-char-id>",
          "paramName": "Amount",
          "dataType": "number",
          "isList": false,
          "flag": "output",
          "required": true,
          "visible": true,
          "mappedTo": "<dataList-object-variable-id>.<child-id>",
          "value": null,
          "children": []
        },
        {
          "id": "<dataList-object-variable-id>.<unique-15-char-id>",
          "paramName": "approvalRequired",
          "dataType": "boolean",
          "isList": false,
          "flag": "output",
          "required": true,
          "visible": true,
          "mappedTo": "<dataList-object-variable-id>.<child-id>",
          "value": null,
          "children": []
        }
      ]
    },
    "agent": {
      "instructions": "Take the FileID and run it through image-to-text to extract vendor, amount, and description. Then run a SQL query against the lookup dataset for the vendor's status. Based on status and amount thresholds (GOLD < $500 = false, PLATINUM < $1500 = false, otherwise true) set approvalRequired and return the structured object.",
      "tools": [
        {
          "id": "<unique-15-char-id>",
          "type": "FUNCTION",
          "functionName": "IMAGE_TO_TEXT",
          "functionDescription": "Extract text from an image, include instructions to give the AI better context on what it is designed to do, include a model to specify the AI Model to use",
          "name": "Image to Text",
          "description": "Extract text from an image, include instructions to give the AI better context on what it is designed to do, include a model to specify the AI Model to use",
          "packageId": "030b06a3-874e-4943-a317-874f69a0020b",
          "packageVersion": "2.0.0",
          "inputs": [
            { "id": "<id1>", "paramName": "input",        "displayName": "input",        "dataType": "text",   "flag": "input", "required": false, "visible": true, "isList": false, "mappedTo": null, "value": null,             "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null },
            { "id": "<id2>", "paramName": "fileId",       "displayName": "fileId",       "dataType": "number", "flag": "input", "required": true,  "visible": true, "isList": false, "mappedTo": null, "value": null,             "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null },
            { "id": "<id3>", "paramName": "model",        "displayName": "model",        "dataType": "text",   "flag": "input", "required": false, "visible": true, "isList": false, "mappedTo": null, "value": "domo.domo_ai", "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null },
            { "id": "<id4>", "paramName": "instructions", "displayName": "instructions", "dataType": "text",   "flag": "input", "required": false, "visible": true, "isList": false, "mappedTo": null, "value": null,             "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null }
          ],
          "inputDescriptions": { "<id1>": "", "<id2>": "", "<id3>": "", "<id4>": "" },
          "output": {
            "id": "<id5>", "paramName": "result", "displayName": "result", "dataType": "text",
            "flag": "output", "required": true, "visible": true, "isList": false,
            "mappedTo": null, "value": null,
            "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null
          }
        },
        { "id": "<unique-15-char-id>", "type": "FUNCTION",
          "functionName": "TEXT_TO_SQL",
          "name": "Text to SQL",
          "packageId": "030b06a3-874e-4943-a317-874f69a0020b",
          "packageVersion": "2.0.0",
          "inputs": [
            { "paramName": "input",   "dataType": "text",    "required": true,  "value": null, "...": "..." },
            { "paramName": "dataSet", "dataType": "dataset", "required": true,  "value": null, "...": "..." },
            { "paramName": "model",   "dataType": "text",    "required": false, "value": "domo.domo_ai", "...": "..." }
          ],
          "output": { "paramName": "result", "dataType": "text", "...": "..." }
        }
      ],
      "context": {
        "datasets":    [{ "id": "<dataset-uuid>" }],
        "directories": [{ "id": "<fileset-uuid>", "path": "" }],
        "files":       [{ "id": "<file-uuid>", "path": "", "name": "renodex.png" }],
        "isEmpty": false
      },
      "outputDescriptions": {}
    }
  },
  "style": { "zIndex": 3, "outline": "none" },
  "index": 1
}
```

**General tab:**

- `data.prompt.value` is a single Slate rich-text array (not an array of inputs). To embed a workflow variable inline, insert a `{ "type": "variable", "id": "<dataList-var-id>", "name": "<var-name>", "dataType": "...", "isList": false, "children": [{ "text": "" ... }] }` node. Always leave `mappedTo: null` on the prompt object — the rich-text content lives entirely in `value`.
- `agent.instructions` is a plain string (not Slate). This is the system prompt that shapes the agent's behavior.
- The model is **not** set on the node — the agent uses whatever model is configured in the instance's AI Service Layer. Do not add a `model` field on `data.agent` or on the prompt.
- **Always declare `data.result` as a structured object — even for single-value returns.** Set `dataType: "object"` and list every field the agent should return under `children[]`. The corresponding `dataList` variable mirrors the structure: `dataType: "object"` with matching `children[]`, and child IDs use dotted notation `<parentVarId>.<childId>` on both sides. Each child's `mappedTo` points at the matching dotted child variable id; `value` stays `null`. If you only want a single text blob back, declare a single child (e.g. `summary` with `dataType: "text"`) and give it an `aiDescription` describing what to put there. **Why:** the agent runtime has structured-output / function-calling baked in, so even when `result` is declared `dataType: "text"` it can still hand back an object. Any downstream Slate `{ "type": "variable" }` reference to that text variable then renders as the literal string `[object Object]`. Forcing the object shape is the only reliable contract.

**Tools tab:**

- Each entry in `agent.tools[]` is the function signature copied in: `type: "FUNCTION"`, `functionName`, `packageId`, `packageVersion`, full `inputs[]` and `output`. For CE functions, get this from `code-engine get-function-signature`.
- Built-in agent tools (Image to Text, Text to SQL, Text Generation) all live in package `030b06a3-874e-4943-a317-874f69a0020b` v `2.0.0`. Their input `paramName`s: `IMAGE_TO_TEXT` → `input`, `fileId`, `model`, `instructions`; `TEXT_TO_SQL` → `input`, `dataSet`, `model`; `TEXT_GENERATION` → `input`, `instructions`, `model`. Output is always `result` (text).
- **`value` on a tool input ↔ "Static Value" checkbox in the UI.** Set `value` to pin the input to a constant the agent always passes (e.g. `model: "domo.domo_ai"`); leave `value: null` to let the agent decide at runtime based on the prompt.
- `agent.inputDescriptions` (and `agent.outputDescriptions`) is an optional object keyed by input/output `id` with free-text guidance shown to the agent for that parameter. Omit it or pass `{}` if you have nothing to add.

**Knowledge tab:**

- `agent.context.datasets[]` ← UI "DataSets" — list of `{ id }`.
- `agent.context.directories[]` ← UI **"FileSets"** (the JSON name is `directories`, but the UI calls them FileSets) — list of `{ id, path }`. `path` is `""` for the root.
- `agent.context.files[]` ← UI "Files" — list of `{ id, path, name }`.
- Set `isEmpty: true` when all three lists are empty, `false` otherwise.

**Other notes:**

- Edges in and out of an AI_AGENT are regular `defaultEdge`s.
- Do not add `metadata`, `taskType`, or `selectedTaskTitle` on `data` — those are serviceTaskNode fields and don't apply here.

### serviceTaskNode (Built-in AI tile — Text Generation, Image-to-Text, Text-to-SQL)

The same three AI primitives that an `AI_AGENT` can call as tools are also available as standalone serviceTaskNode tiles when you don't need an agent's reasoning loop. These use the platform-internal `"artificialIntelligence"` package, NOT a CE package UUID.

```json
{
  "id": "node_describeMore",
  "type": "serviceTaskNode",
  "position": { "x": 80, "y": 360 },
  "data": {
    "_designNode": "serviceTaskNode",
    "dimensions": { "width": 200, "height": 60 },
    "title": "Text Generation",
    "description": "Completes or generates text based on an input prompt, include instructions to give the AI better context on what it is designed to do, include a model to specify the AI Model to use",
    "taskType": "artificialIntelligence",
    "metadata": {
      "packageId": "artificialIntelligence",
      "functionName": "TEXT_GENERATION",
      "packageVersion": "2.0.0",
      "allowsCustomOutput": true
    },
    "selectedTaskTitle": "Text Generation",
    "selectedTaskDescription": "Completes or generates text based on an input prompt, include instructions to give the AI better context on what it is designed to do, include a model to specify the AI Model to use",
    "usesStructuredOutputs": false,
    "input": [
      {
        "id": "<unique-15-char-id>",
        "paramName": "input", "displayName": "input",
        "dataType": "text", "isList": false,
        "flag": "input", "required": true, "visible": true,
        "mappedTo": "<dataList-var-id>", "value": null,
        "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null
      },
      {
        "id": "<unique-15-char-id>",
        "paramName": "instructions", "displayName": "instructions",
        "dataType": "text", "isList": false,
        "flag": "input", "required": false, "visible": true,
        "mappedTo": null,
        "value": [
          {
            "type": "paragraph",
            "children": [
              { "text": "Take this description and give me a better description.", "bold": false, "italic": false, "underlined": false, "sql": false }
            ]
          }
        ],
        "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null
      },
      {
        "id": "<unique-15-char-id>",
        "paramName": "model", "displayName": "model",
        "dataType": "text", "isList": false,
        "flag": "input", "required": false, "visible": true,
        "mappedTo": null, "value": "domo.domo_ai",
        "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null
      }
    ],
    "output": [
      {
        "id": "<unique-15-char-id>",
        "paramName": "result", "displayName": "result",
        "dataType": "text", "isList": false,
        "flag": "output", "required": true, "visible": true,
        "mappedTo": "<dataList-var-id>", "value": null,
        "aiDescription": null, "children": [], "configType": null, "customMappingType": null, "entitySubType": null
      }
    ]
  },
  "style": { "zIndex": 4, "outline": "none" },
  "index": 2
}
```

**Notes:**

- `taskType: "artificialIntelligence"` and `metadata.packageId: "artificialIntelligence"` are both the literal string — not a UUID. This is how the UI renders the AI tile chrome instead of the generic CE service-task chrome.
- `metadata.functionName` is one of `TEXT_GENERATION`, `IMAGE_TO_TEXT`, or `TEXT_TO_SQL`. `packageVersion: "2.0.0"`.
- `metadata.allowsCustomOutput` and `usesStructuredOutputs` are observed on captured definitions but their author-side requirement is not confirmed — copy them through if present in a captured definition; if you're authoring from scratch and the tile doesn't render correctly, try `allowsCustomOutput: true` on `metadata` for `TEXT_GENERATION`.
- The `instructions` input accepts a Slate rich-text array as `value` so you can interpolate workflow variables inline; a plain string also works.
- `model` defaults to `"domo.domo_ai"`. Leave the default unless the user has specified another instance-supported model string.
- Input/output `paramName`s match the agent-tool signatures above (`TEXT_GENERATION`: `input`, `instructions`, `model` → `result`; `IMAGE_TO_TEXT`: `input`, `fileId`, `model`, `instructions` → `result`; `TEXT_TO_SQL`: `input`, `dataSet`, `model` → `result`).
- These tiles return a single text `result`. For typed structured output (multiple named fields), use an `AI_AGENT` node with `data.result.dataType: "object"` instead.

### conditionalGatewayNode (Exclusive Gateway / XOR)

The gateway itself has NO rule or condition expression — those live on the outgoing conditionEdges.

```json
{
  "id": "node_condition",
  "type": "conditionalGatewayNode",
  "data": {
    "_designNode": "conditionalGatewayNode",
    "inclusive": false,
    "dimensions": { "width": 200, "height": 60 },
    "title": "More Items?"
  }
}
```

---

## Edges

### defaultEdge (Normal Flow)

**CRITICAL — `path` is required.** The API returns a 400 error if `path` is missing from `defaultEdge.data` (`WorkflowEdgeData$Default.path` is non-nullable). Always include a 4-point coordinate array.

Path formula for vertical connections (source above target):

- `centerX = nodeX + nodeWidth/2`
- `midY = (sourceBottom + targetTop) / 2`

```json
{
  "id": "edge-startNode_1-node_myStep-abc123",
  "source": "startNode_1",
  "target": "node_myStep",
  "type": "defaultEdge",
  "arrowHeadType": "arrow",
  "style": {},
  "data": {
    "sourcePosition": "bottom",
    "targetPosition": "top",
    "path": [
      [300, 60],
      [300, 100],
      [300, 100],
      [300, 140]
    ]
  }
}
```

Where `[300, 60]` = `[centerX, sourceBottom]`, `[300, 100]` = midpoint, `[300, 140]` = `[centerX, targetTop]`.

### conditionEdge (Gateway Branch — renders as pill shape in UI)

Outgoing edges from a `conditionalGatewayNode` MUST be `"type": "conditionEdge"`. Using `"defaultEdge"` causes a 400 deployment error and the UI shows a "+" placeholder instead of the pill shape.

The pill shape is NOT a separate node — it is rendered directly from the edge when `_designNode: "condition"` + `position` + `dimensions` + rule data are set in `data`.

**Two rule modes — choose based on complexity:**


| Mode     | `data.type`  | Use when                                                         | Pill width |
| -------- | ------------ | ---------------------------------------------------------------- | ---------- |
| Basic    | `"Basic"`    | Simple variable comparisons (equals, contains, etc.)             | 200        |
| Advanced | `"Advanced"` | Calculations, list sizes, arithmetic, multi-variable expressions | 260        |


---

**Basic conditionEdge** (preferred for simple equality/contains checks):

```json
{
  "id": "edge-node_condition-node_nextStep-sBvJkLpQnXrWmYt",
  "source": "node_condition",
  "target": "node_nextStep",
  "type": "conditionEdge",
  "arrowHeadType": "arrow",
  "style": {},
  "index": 0,
  "data": {
    "sourcePosition": "bottom",
    "targetPosition": "top",
    "path": [
      [gatewayX + 100, gatewayY + 60],
      [gatewayX + 100, pillY],
      [gatewayX + 100, pillY + 40],
      [gatewayX + 100, targetY]
    ],
    "entryPosition": "top",
    "exitPosition": "bottom",
    "description": "",
    "title": "Yes",
    "type": "Basic",
    "nodeId": "sBvJkLpQnXrWmYt",
    "position": { "x": gatewayX, "y": pillY },
    "dimensions": { "width": 200, "height": 40 },
    "splitIndex": 2,
    "_designNode": "condition",
    "rules": [
      [
        {
          "variable": {
            "id": "<dataList-variable-id>",
            "paramName": "<variable-name>",
            "dataType": "text",
            "isList": false,
            "children": [],
            "showChildren": false,
            "entitySubType": null,
            "value": null,
            "isOutput": false
          },
          "operator": "Equals",
          "valueType": "Custom",
          "value": "Approved"
        }
      ]
    ]
  }
}
```

`rules` structure: outer array = OR groups; inner array = AND conditions within a group.

Available `operator` values: `"Equals"`, `"NotEquals"`, `"Contains"`, `"NotContains"`

Available `valueType` values: `"Custom"` (literal string), `"Null"`, `"Variable"` (compare to another variable)

---

**Advanced conditionEdge** (for expressions involving calculations, list lengths, or multi-variable arithmetic):

```json
{
  "id": "edge-node_condition-node_nextStep-sBvJkLpQnXrWmYt",
  "source": "node_condition",
  "target": "node_nextStep",
  "type": "conditionEdge",
  "arrowHeadType": "arrow",
  "style": {},
  "index": 0,
  "data": {
    "sourcePosition": "bottom",
    "targetPosition": "top",
    "path": [
      [gatewayX + 100, gatewayY + 60],
      [gatewayX + 100, pillY],
      [gatewayX + 100, pillY + 40],
      [gatewayX + 100, targetY]
    ],
    "entryPosition": "top",
    "exitPosition": "bottom",
    "description": "",
    "title": "Yes",
    "type": "Advanced",
    "nodeId": "sBvJkLpQnXrWmYt",
    "position": { "x": gatewayX, "y": pillY },
    "dimensions": { "width": 260, "height": 40 },
    "splitIndex": 2,
    "_designNode": "condition",
    "advancedRule": [
      {
        "type": "paragraph",
        "children": [
          { "text": "= ", "bold": false, "italic": false, "underlined": false, "sql": false },
          {
            "type": "variable",
            "children": [{ "text": "", "bold": false, "italic": false, "underlined": false, "sql": false }],
            "dataType": "number",
            "id": "<dataList-variable-id-for-counter>",
            "name": "<variable-name>",
            "isList": false
          },
          { "text": " < ", "bold": false, "italic": false, "underlined": false, "sql": false },
          {
            "type": "variable",
            "children": [{ "text": "", "bold": false, "italic": false, "underlined": false, "sql": false }],
            "dataType": "number",
            "id": "<dataList-variable-id-for-length>",
            "name": "<variable-name>",
            "isList": false
          }
        ]
      }
    ]
  }
}
```

### conditionEdge path coordinates (CRITICAL)

**Yes (vertical, gateway → step below):**

- Point 1: (gatewayCenterX, gatewayBottom) = (gatewayX + 100, gatewayY + 60)
- Point 2: (gatewayCenterX, pillY)          ← exactly the pill top
- Point 3: (gatewayCenterX, pillY + 40)     ← exactly the pill bottom (height = 40)
- Point 4: (gatewayCenterX, targetTop)

**No (horizontal, gateway → node to the right):**

- All four points at `y = gatewayCenterY = gatewayY + 30`
- Passes through pill center (pillY + 20 = gatewayY + 30)
- pill x = somewhere between gatewayRight and endNodeLeft, centered

**Pill positioning:**

- Yes pill: `x = gatewayX` (left-aligns with gateway), `y = gatewayY + 60 + gap` (e.g., +70 gap)
- No pill: `x = (gatewayRight + endNodeLeft) / 2 - 130` (centered), `y = gatewayY + 10`
- End node must be far enough right that the 260px No pill fits with room on both sides (minimum ~400px gap from gateway right edge to end node left edge)

### Edge ID and nodeId format

- Edge ID: `edge-{sourceId}-{targetId}-{randomAlphanumericSuffix}`
- `nodeId`: unique 15-character alphanumeric string, different for every edge in every workflow

---

## dataList (Variables)

```json
"dataList": [
  {
    "id": "var_counter",
    "paramName": "counter",
    "dataType": "number",
    "isList": false,
    "children": [],
    "showChildren": false,
    "entitySubType": null,
    "value": 0,
    "isOutput": false
  },
  {
    "id": "var_listLength",
    "paramName": "listLength",
    "dataType": "number",
    "isList": false,
    "children": [],
    "showChildren": false,
    "entitySubType": null,
    "value": null,
    "isOutput": false
  },
  {
    "id": "var_peopleList",
    "paramName": "peopleList",
    "dataType": "person",
    "isList": true,
    "children": [],
    "showChildren": false,
    "entitySubType": null,
    "value": null,
    "isOutput": false
  }
]
```

Common `dataType` values: `"text"`, `"number"`, `"decimal"`, `"boolean"`, `"person"`, `"date"`, `"dataset"`, `"object"`.

**CRITICAL — required-field cheat sheet.** The shape above is what actually round-trips and resolves at runtime. Two field-name traps:

- Use `paramName`, NOT `name`. The API silently accepts `name` on write but the variable will not resolve at runtime, causing cascading `ODY_026` errors on every node that references it (often pointing at unrelated downstream nodes).
- Use `value`, NOT `defaultValue`. `defaultValue` is silently ignored. For numeric vars the value MUST be a typed numeric literal (`0`, `1.5`) — strings like `"0"` are also ignored.

Always include the full set: `id`, `paramName`, `dataType`, `isList`, `children` (`[]` for scalars), `showChildren: false`, `entitySubType: null`, `value`, `isOutput: false`. Missing the trailing fields tends to cascade into validator confusion.

**Structured-object variables (used as the `mappedTo` target of an AI_AGENT `result`):** Use `dataType: "object"` with a `children[]` array. Each child has its own id in dotted form `<parentId>.<childId>` and its own `dataType`. The AI_AGENT's `data.result.children[]` mirrors these one-for-one. Example:

```json
{
  "id": "var_invoiceResult",
  "paramName": "result",
  "dataType": "object",
  "isList": false,
  "showChildren": false,
  "entitySubType": null,
  "value": null,
  "isOutput": false,
  "children": [
    { "id": "var_invoiceResult.amt", "paramName": "Amount",           "dataType": "number",  "isList": false, "children": [], "showChildren": false, "entitySubType": null, "value": null, "isOutput": false },
    { "id": "var_invoiceResult.req", "paramName": "approvalRequired", "dataType": "boolean", "isList": false, "children": [], "showChildren": false, "entitySubType": null, "value": null, "isOutput": false },
    { "id": "var_invoiceResult.ven", "paramName": "Vendor",           "dataType": "text",    "isList": false, "children": [], "showChildren": false, "entitySubType": null, "value": null, "isOutput": false }
  ]
}
```

**Write/read normalization:** Always submit `paramName` — see the cheat sheet above. The API does not error on `name`, but the variable fails to resolve at runtime, so `name` is effectively a write-only no-op. `get-definition` returns the stored shape with `paramName`.

---

## schema (Form Inputs / Outputs)

```json
"schema": {
  "input": [
    {
      "id": "schema_voterName",
      "paramName": "voterName",
      "displayName": "Voter name",
      "dataType": "text",
      "isList": false,
      "customMappingType": null,
      "value": null,
      "mappedTo": "var_voterName",
      "visible": true
    },
    {
      "id": "schema_peopleList",
      "paramName": "peopleList",
      "displayName": "People list",
      "dataType": "person",
      "isList": true,
      "customMappingType": null,
      "value": null,
      "mappedTo": "var_peopleList",
      "visible": true
    }
  ],
  "output": []
}
```

- Use `mappedTo` (not `value`) for variable references; set `value: null`.
- `customMappingType` is `null` (not `""`).
- `paramName` is the variable name exposed externally (used when triggering programmatically or from an app).

**Write/read normalization:** Submit `schema.input` as an array (as shown above). The API normalizes it on storage to `schema.inputs` — an object keyed by field IDs — which is what `get-definition` returns. This divergence is expected. Do not try to match the stored shape when authoring; always write the array form. The API also re-keys entries: `schema_*` IDs you write may be replaced by the form field UUIDs that were bound at create-form time.

---

## Counter-Based Loop Pattern

To iterate over a list using Code Engine list utilities:

```
rootNode
  → getListLength (CODE_ENGINE: getLength, output → var_listLength)
  → setCounter (CODE_ENGINE: addNumbers with 0+0=0, output → var_counter)
  → conditionalGatewayNode "More to process?"
      ↓ conditionEdge "Yes" (advancedRule: = counter < listLength)
        → getFromList (CODE_ENGINE: getFromList, index=counter, output → var_currentItem)
        → processItem (CODE_ENGINE: your function, input=var_currentItem)
        → incrementCounter (CODE_ENGINE: addNumbers, inputs: a=counter, b=1, output → var_counter)
        → [loop back to conditionalGatewayNode via defaultEdge]
      → conditionEdge "No" (Default, no advancedRule)
        → endNode_1
```

The loop-back edge is a `defaultEdge` from the last step in the loop body back to the gateway node.

---

## Iterative Update Pattern

```bash
# 1. Write your definition
community-domo-cli workflows update-definition <id> <version> --body-file definition.json

# 2. Validate
community-domo-cli workflows validate --body-file definition.json

# 3. Verify dataset queries
community-domo-cli workflows validate-dataset-query <id> <version> --dataset <ds_id> --query "..."

# 4. Debug: confirm what was actually stored
community-domo-cli workflows get-definition <id> <version>

# 5. Inspect runs after live tests
community-domo-cli workflows list-instances <id>
community-domo-cli workflows instance-get <id> <instance_id>
```

