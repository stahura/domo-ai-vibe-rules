---
name: workflow-builder
description: This skill should be used when the user asks to "build a Domo workflow", "create a workflow", "design a workflow definition", "author a workflow model", "set up workflow triggers", "add a workflow form", "create a workflow queue", "list workflow instances", or "inspect workflow runs". Covers the full Domo Workflow authoring lifecycle using the community-domo-cli: creating models, writing definitions, validating, forms, triggers, queues, and monitoring instances.
---

# Domo Workflow Builder

Build and manage Domo Workflow models using `community-domo-cli`. This skill covers the full authoring lifecycle — from model creation through definition, validation, triggers, and instance inspection.

For app-side runtime usage (starting workflows from a custom app via `WorkflowClient`), see `skills/custom-apps/workflow/SKILL.md`.

## Authoring Lifecycle

### Phase 1 — Discover Existing Resources

Before creating anything, check what already exists:

```bash
# Find datasets for use in dataset-query steps
community-domo-cli datasets search --name "Sales"    # search by name (preferred)
community-domo-cli datasets list                     # paginated list (use --offset for large instances)
community-domo-cli datasets schema <dataset_id>

# Find Code Engine packages to reuse as service task functions
community-domo-cli code-engine list-packages
community-domo-cli code-engine search-packages --query "email"   # search by keyword; add --owned-by-id only if user specifies an owner
community-domo-cli code-engine get-package <package_id>          # full function definitions
community-domo-cli code-engine get-function-signature <package_id> <function_name>  # inputs/outputs only

# Find existing workflows
community-domo-cli workflows list

# Find users and groups for task assignment steps
community-domo-cli users list
community-domo-cli users list-groups

# Find existing queues for task routing
community-domo-cli queues list
```

**Built-in AI primitives (no CE package needed):** The platform ships three AI tiles available as standalone `serviceTaskNode`s OR as tools inside an AI_AGENT node — `TEXT_GENERATION` (text completion), `IMAGE_TO_TEXT` (extract text from a file), `TEXT_TO_SQL` (NL → SQL against a dataset). Reach for these before writing CE for AI work. For LLM-driven multi-step reasoning with structured output, use an `AI_AGENT` node with `instructions`, `tools[]`, `context` (datasets/directories/files as knowledge), and a `result` of `dataType: "object"`. See `references/definition-schema.md` for both shapes.

**When no built-in function covers the need:** Before accepting a limitation, check whether a custom Code Engine package could fill the gap. See `skills/apps/code-engine/SKILL.md` and `skills/cli/code-engine-create/SKILL.md`.

- **Custom CE is viable for pure logic gaps** — string manipulation, math, data transformation, list operations. No external dependencies, no API knowledge required.
- **Custom CE is NOT viable for Domo platform API gaps** (e.g. finding a group by name, looking up a user, querying a dataset) unless the user provides the necessary endpoint and request details. Writing a CE function that calls Domo's own APIs requires knowing the exact endpoint shape and how CE authenticates against the instance — do not guess. If the user supplies that information, CE can bridge the gap; otherwise surface the limitation clearly and ask the user to provide the missing values directly.

**Deployment requirement:** A custom CE package must be published in the Domo UI before the workflow can execute. The workflow definition can be uploaded (`update-definition`) referencing an unpublished package and the upload will succeed — but `validate` will return an error indicating the package is not found or not published. The CLI does not have publish/deploy permission. Always inform the user that after the package is created they need to go into Domo and publish it before validation will pass and the workflow can run.

### Phase 2 — Create Workflow Shell

```bash
community-domo-cli workflows create --name "My Workflow" --description "..."
```

> **Confirmation prompt:** This is a mutating command. The CLI will ask `Execute mutating action: create workflow 'My Workflow'? [y/N]` before proceeding. Pass `--yes` to the root command to skip it in scripts: `community-domo-cli --yes workflows create ...`

Returns `{ id, versions: [{ version }] }`. Capture `id` and the integer `version` — both are required for every subsequent call.

### Phase 3 — Build and Persist Definition

Construct the workflow definition JSON locally using the schema documented in `references/definition-schema.md`, then write it to the version:

```bash
community-domo-cli workflows update-definition <workflow_id> <version> --body-file definition.json
```

`<version>` accepts either an integer (`1`) or full semver (`1.0.1`) — the CLI auto-converts to semver for the API URL.

To validate dataset SQL queries as part of the same operation, pass them in the body alongside the definition. See `references/definition-schema.md` for the full definition structure.

To validate a specific dataset query independently before embedding it:

```bash
community-domo-cli workflows validate-dataset-query <workflow_id> <version> \
  --dataset <dataset_id> --query "SELECT region, SUM(amount) FROM table GROUP BY region"
```

### Phase 4 — Validate

Always validate the definition before treating it final. Validation is non-mutating:

```bash
community-domo-cli workflows validate --body-file definition.json
```

Validation catches structural errors (disconnected nodes, missing required fields, invalid implementation types). It does **not** catch Code Engine input name mismatches or dataset SQL errors — validate those separately.

### Phase 5 — Add Forms (Optional)

The `create-form` command creates both **start forms** (shown when a workflow is submitted) and **user task forms** (shown to the assignee during a `userTaskNode` step). Both use the same `/forms/v2` endpoint — the distinction is which node in the definition references the returned `formId`.

```bash
community-domo-cli workflows create-form <workflow_id> <version> --body-file form.json
```

**The API ignores any `id` field in the request body.** Always capture the UUID from the response and use that as the `formId` in your definition.

After creating a form, verify the stored field IDs and fieldTypes:

```bash
community-domo-cli workflows get-form <form_id>
```

Each field in the form body requires a unique UUID `id`. See `references/api-reference.md` for the full form body shape.

### Phase 6 — Add Trigger (Optional)

To schedule the workflow or fire it on an event:

```bash
community-domo-cli workflows create-trigger --body-file trigger.json
```

List existing triggers for a workflow:

```bash
community-domo-cli workflows list-triggers --workflow-id <workflow_id>
```

### Phase 7 — Monitor Instances

After the workflow is live, inspect runs:

```bash
community-domo-cli workflows list-instances <workflow_id>
community-domo-cli workflows instance-get <workflow_id> <instance_id>
```

## CLI Quick Reference

```bash
# Workflow models
community-domo-cli workflows list
community-domo-cli workflows get <id>
community-domo-cli workflows create --name "..." --description "..."
community-domo-cli workflows update-definition <id> <version> --body-file definition.json
community-domo-cli workflows get-definition <id> <version>
community-domo-cli workflows validate --body-file definition.json
community-domo-cli workflows validate-dataset-query <id> <version> --dataset <ds_id> --query "..."
community-domo-cli workflows create-form <id> <version> --body-file form.json
community-domo-cli workflows get-form <form_id>

# Instances
community-domo-cli workflows list-instances <id>
community-domo-cli workflows instance-get <id> <instance_id>

# Triggers
community-domo-cli workflows list-triggers --workflow-id <id>
community-domo-cli workflows create-trigger --body-file trigger.json

# Code Engine (discovery for service task wiring)
community-domo-cli code-engine list-packages
community-domo-cli code-engine search-packages --query "*" --count 100   # search all packages; add --owned-by-id only if user specifies an owner
community-domo-cli code-engine get-package <package_id>
community-domo-cli code-engine get-function-signature <package_id> <function_name>

# Queues
community-domo-cli queues list
community-domo-cli queues create --body-file queue.json

# Datasets (discovery)
community-domo-cli datasets search --name "keyword"  # search by name
community-domo-cli datasets list --limit 50 --offset 0

# Users / groups (for task assignment resolution)
community-domo-cli users list
community-domo-cli users list-groups
```

## Critical Gotchas

**CRITICAL — `--yes` is a ROOT-LEVEL flag, not a subcommand flag**
`--yes` must come immediately after `community-domo-cli`, BEFORE the subcommand name:
```bash
community-domo-cli --yes workflows create-form ...   # ✅ correct
community-domo-cli workflows create-form --yes ...   # ❌ still prompts — flag ignored
```
Always use the root-level position for all mutating commands.

**CRITICAL — `update-definition` version accepts integer OR semver**
Pass `1` or `"1.0.1"` — the CLI auto-converts to the semver form (`1.0.0`) required by the API URL. Passing a bare integer directly to the API returns a 400 error about SemanticVersion conversion. `validate-dataset-query` and `create-form` use the v1 API which accepts an integer directly.

**CRITICAL — definition update is PUT, not POST**
`update-definition` issues a `PUT` to `/workflow/v2/models/{id}/versions/{v}/definition`. A POST to that path will 405. Omitting the version segment returns a 404.

**CRITICAL — conditionEdge outgoing from gateway, NOT defaultEdge**
Outgoing edges from a `conditionalGatewayNode` MUST use `"type": "conditionEdge"`. Using `"type": "defaultEdge"` causes a 400 deployment error ("Unable to deploy workflow on cluster") and the UI renders a "+" placeholder instead of the pill shape. See `references/definition-schema.md` for the full conditionEdge structure.

**CRITICAL — Basic vs Advanced conditionEdge**
Use `"type": "Basic"` with a `rules` array for simple variable comparisons (equals, not equals, contains). Use `"type": "Advanced"` with an `advancedRule` Slate array only for expressions requiring calculation, list length checks, or arithmetic. Basic pill width = 200; Advanced pill width = 260. Both branches of a gateway can be Basic, both Advanced, or mixed.

**CRITICAL — advancedRule lives on the edge, not the gateway**
The condition expression goes on the `conditionEdge`'s `data.advancedRule` (Advanced) or `data.rules` (Basic). The `conditionalGatewayNode` itself has NO rule field.

**CRITICAL — `dataList` variable shape: use `paramName` + numeric `value`, not `name` + `defaultValue`**
The variable shape that actually round-trips and resolves at runtime:
```json
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
}
```
- Use `paramName` (NOT `name`).
- Use `value` (NOT `defaultValue`). For numeric vars, the value MUST be a typed integer/decimal (`0`, not `"0"`).
- Wrong field names are ACCEPTED on write but silently ignored, leaving the variable effectively undefined. Symptom: cascading `ODY_026` "variable referenced but not found / wrong type" on every node that touches the variable, often pointing to seemingly unrelated nodes downstream in the flow.
- For object-typed vars, declare every sub-field as a child with id `<parentId>.<childName>` (dotted notation). See `references/definition-schema.md` for the structured-object pattern.

**CRITICAL — serviceTaskNode requires `selectedTaskTitle` and `selectedTaskDescription` on data**
The PARAMETERS & MAPPING panel in the workflow UI only renders when `selectedTaskTitle` and `selectedTaskDescription` are set on the node's `data` object. These come from the function's `displayName` and `description` fields in `get-function-signature`. Do NOT put `displayName` inside `metadata` — it belongs on `data`.

**CRITICAL — serviceTaskNode input/output entry `id` must be a 15-char random alphanumeric**
Every entry in a service task's `input` and `output` arrays needs a unique `"id"` that is a random 15-character alphanumeric string (e.g. `"aBcDeFgHiJkLmNo"`). If omitted, the API falls back to using the `paramName` as the id, which breaks UI rendering of the parameter list.

**CRITICAL — `mappedTo` vs `value` on all node entries**
For variable-mapped entries (service tasks, form nodes, schema): set `"mappedTo": "<dataList-var-id>"` and `"value": null`. For literal values: set `"value": "<literal>"` and `"mappedTo": null`. Never put a variable ID string in `value` — it will be treated as a literal, not a variable reference.

**CRITICAL — `metadata.settings: {}` is required on serviceTaskNode**
All service task `metadata` objects must include `"settings": {}`. Omitting it causes the Code Engine tile to show "Version: undefined" in the UI.

**CRITICAL — `isList: true` params require JSON array values**
For inputs where the CE function signature declares `isList: true` (e.g. `people`, `users`, `groups`), the `value` field must be a JSON array: `["userId"]`, not `"userId"`. Passing a string causes a 400 deserialization error.

**CRITICAL — `dataType` must match the CE function signature**
Use the exact type from `get-function-signature`: `"dataset"`, `"DIRECTORY"`, `"person"`, `"group"`, `"object"`, `"text"`, `"number"`, `"decimal"`, `"boolean"`. Do not default everything to `"text"`.

**CRITICAL — entity-typed input `value` shape: bare ID for most, full entity for `DIRECTORY`**
When passing a literal value (not `mappedTo` a variable), the shape of `value` depends on the entity type. There's no "decision tree" — it's a fixed table.

> **Naming note:** `DIRECTORY` is the API/`dataType` name for what users now see as **Documents** in the Domo UI (previously called **FileSets** — the function names in the `DOMO FileSets` package and the `/api/files/v1/filesets/...` endpoint paths still use the old name). All three terms refer to the same resource. Use `DIRECTORY` everywhere in the workflow definition `dataType` field regardless of UI rename.

| `dataType`  | `value` shape                                                                  | Example                                                              |
| ----------- | ------------------------------------------------------------------------------ | -------------------------------------------------------------------- |
| `dataset`   | bare UUID string                                                               | `"value": "b8d2fb52-c949-47f7-bff3-cf37e815194d"`                    |
| `person`    | bare user-id string                                                            | `"value": "1317417586"`                                              |
| `group`     | bare group-id string                                                           | `"value": "1234567"`                                                 |
| `DIRECTORY` | full entity object `{id, type, subType, path, name}`                           | `"value": {"id": "92599d92-…", "type": "DIRECTORY", "subType": null, "path": "", "name": null}` |
| `text` / `number` / `decimal` / `boolean` | the typed literal                                | `"value": 1234.56`, `"value": "hello"`, `"value": true`              |

For `isList: true` inputs, wrap the value in a JSON array regardless of type. Common 400 if you get this wrong:
- `dataset` with entity wrapper `{id: ...}` → `Cannot deserialize value of type java.util.UUID from Object value`.
- `DIRECTORY` with bare UUID string → `Cannot construct instance of Entity ... no String-argument constructor`.
- `DIRECTORY` entity missing `path` → `Path must be provided for DIRECTORY type`.

**CRITICAL — rootNode `customMappingType` is `"form_start"`, not `"form"`**
Input entries on a `rootNode` with a start form must use `"customMappingType": "form_start"`. Using `"form"` causes the start form parameters to not appear in the UI. userTaskNode input/output entries correctly use `"customMappingType": "form"`.

**CRITICAL — rootNode form entries: `acceptsInput: false`, `visible: true`**
Each input entry on a form-start rootNode must have `"acceptsInput": false` and `"visible": true`. The opposite of what you might expect — the form outputs data from the user, so the workflow side does not "accept input" from upstream.

**No `mappingType` field on service task input/output entries**
The UI does not set `mappingType` on individual entries. Omit it entirely. The `mappedTo`/`value` pattern determines whether an entry is variable-mapped or literal without needing this field.

**CRITICAL — AI_AGENT `data.result` must always be a structured object, even for single-value returns**
Set `data.result.dataType: "object"` with at least one entry in `children[]` (and a matching object-typed `dataList` variable with the same children). For a one-value return, declare a single child like `summary` with `dataType: "text"` and an `aiDescription`. The agent runtime has structured-output / function-calling behavior baked in: when `result` is declared as a plain text variable, the agent can still emit an object at runtime, and any downstream Slate `{ "type": "variable" }` reference will render the literal string `[object Object]`. Forcing the object shape on the node is the only reliable contract — no symptom appears at validate time, only at runtime in downstream text. See `references/definition-schema.md`.

**CRITICAL — AI_AGENT structured output collapses list-of-objects on single-item runs**
Do NOT model multi-item agent output as a child with `isList: true` (e.g. `result.children[0]: {paramName: "invoices", isList: true, children: [...]}`). The agent runtime's structured-output emits a bare object instead of a single-element array, then downstream `getListOfObjLength`/`getObjectFromList` 400 with `Expected list value, found {...}`. **Pattern that works:** enumerate items deterministically with a service task FIRST (e.g. `searchFiles` for FileSet content, a dataset-query for rows), then run a per-item AI_AGENT INSIDE the loop with `result.dataType: "object"` and no top-level list. The agent processes one item per iteration; the loop produces the multi-item behavior.

**CRITICAL — built-in `IMAGE_TO_TEXT` does NOT work on Domo FileSet files**
The platform-internal `IMAGE_TO_TEXT` tool (package `030b06a3-…`) declares `fileId` as `dataType: "number"`. Domo FileSet file ids are UUID strings — the agent recognizes the mismatch in its transcript ("UUID vs numeric ID mismatch") and silently fails extraction. **For FileSet content, attach `agentImageToTextWithFileSet` from the `DOMO FileSets` package (`72b71b3e-b6d2-4313-8202-29e0d99081c1`) as the agent tool instead.** It takes `fileSetId` (text) + `path` (text) and works with FileSet UUIDs. Pin `fileSetId` as a static value on the tool input and let the agent fill `path` from the prompt.

**Built-in AI tiles use the literal string `"artificialIntelligence"` as packageId**
The standalone Text Generation, Image-to-Text, and Text-to-SQL tiles are `serviceTaskNode`s with `taskType: "artificialIntelligence"` and `metadata.packageId: "artificialIntelligence"` — both literal strings, not UUIDs. `metadata.functionName` is `TEXT_GENERATION`, `IMAGE_TO_TEXT`, or `TEXT_TO_SQL`; `packageVersion: "2.0.0"`. Don't try to look these up via `code-engine list-packages` — they're platform-internal and won't appear there. See `references/definition-schema.md` for the full shape.

**AI Agent and built-in AI tiles are different node shapes**
Both ship with the platform but are authored differently. An AI Agent step (instructions + tools + knowledge + optional structured object output) uses `type: "AI_AGENT"` with `_designNode: "AI_AGENT"` and its config under `data.agent` / `data.prompt` / `data.result`. The standalone AI tiles are `serviceTaskNode`s as above. When an AI Agent calls Image-to-Text or Text-to-SQL as a tool, the tool entry inside `data.agent.tools[]` uses the real CE package id `030b06a3-874e-4943-a317-874f69a0020b` v `2.0.0` (not the `"artificialIntelligence"` literal). The agent's model is set globally via the AI Service Layer — there is no `model` field on the AI_AGENT node itself.

**CRITICAL — Slate variable interpolation has two non-obvious rules**
Slate-rich-text values (used in `sendEmail.body`, AI_AGENT `data.prompt.value`, `combineText`-style inputs, etc.) only interpolate `{ "type": "variable" }` nodes when BOTH of the following are true. Either rule violated and the variable renders as the literal `name` string (e.g. the prompt comes out as `Parse the invoice file with id   id   (filename   name  )`).
1. **The variable must be an inline child of a paragraph that ALSO contains the surrounding text.** Putting each text segment and each variable in its own paragraph (`[paragraph(text), paragraph(var), paragraph(text)]`) breaks interpolation. Correct: `[paragraph(text, var, text, var, text)]`.
2. **For child-variable references on an object, `name` must be the FULL DOTTED PATH, not just the leaf.** A variable with `id: "var_currentFile.id"` needs `name: "currentFile.id"`. A variable with `id: "var_topLevel"` uses `name: "topLevel"`. Foolproof helper: `name = id.replace(/^var_/, "")`.

**CRITICAL — `appendToDataset` does NOT CSV-escape values**
The `appendToDataset` (DOMO DataSets package) `values` input is split by the `delimiter` you pass — there is no quoting/escaping mechanism. If any field can contain the delimiter character, the row will explode into the wrong number of columns and the function 400s with `There are too many columns. Expected N`. Formatted currency strings (`$1,234.56`) trip this constantly. Pick a delimiter that won't appear in any value (`|` or `\t` are safe) and pass it on both sides.

**CRITICAL — validate after every definition change**
Run `validate` after each `update-definition`. A definition that passes validation can still fail at runtime if Code Engine function input names don't exactly match the step's `inputs` map — use `get-function-signature` to verify input names before wiring steps.

**Form fields use `fieldType`, not `type`**
The form fields API (`POST /forms/v2`) requires `fieldType` (e.g., `"fieldType": "SHORT_ANSWER"`), NOT `"type"`. Additionally, each field must include `optional`, `alias`, `options`, `useExternalValues`, and `displayAsDropdown` — omitting any of these causes "This has not been properly configured" in the UI.

**Form `options` must be `{}` (empty object), not `[]` (array)**
Even for fields with no selectable choices, `options` must be an empty object `{}`. Passing an array causes a 400 error. For choice-based fields like `SINGLE_CHOICE`, use `options: { "values": ["Option A", "Option B"], "acceptsOther": false }`.

**Form API ignores your top-level `id` — always use the response UUID**
Any `id` field in the form creation body is silently discarded. The API assigns its own UUID. Always read the `id` from the response and use that as `formId` in your workflow definition. Using a self-generated UUID that wasn't returned by the API causes the definition to reference a non-existent form.

**Form `customMappingType` must be `""`, not `null`**
All input/output parameter objects in the form body must have `"customMappingType": ""` (empty string). Using `null` causes a 400: "Instantiation of WorkflowFormInputOutput failed for JSON property customMappingType due to missing (therefore NULL) value".

**Form field IDs must be unique UUIDs**
Generate UUID `id` values for each entry in the form `fields` array before calling `create-form`. The API rejects duplicate or missing field IDs.

**`userTaskNode` — assignee must have permission to be assigned workflow tasks**
The `assignedTo.value` field (a user ID as a string) is validated by the workflow validator. If the specified user does not have the appropriate role or permission to be assigned workflow tasks, validation returns ODY_033. Use `users list` to find a valid assignee, or verify that the user has an Admin or Privileged role.

**`userTaskNode` — selectedQueue must exist in the instance**
The `selectedQueue` field is validated against the queues in your Domo instance. A queue ID copied from another instance causes ODY_046. Always resolve queue IDs with `queues list` before embedding them in a definition.

**`userTaskNode` forms — `readOnly` + mixed input/output is the usual shape**
A user-task form typically mixes three kinds of fields: (1) read-only displays of workflow variables, (2) editable fields pre-populated with a workflow variable, and (3) blank response fields the assignee fills in. The form field must set `readOnly: true` + `acceptsInput: true, acceptsOutput: false` for kind 1; `acceptsInput: true, acceptsOutput: true` for kind 2; `acceptsInput: false, acceptsOutput: true` for kind 3. On the node side, kind-1 fields go in `input[]`, kind-3 in `output[]`, and kind-2 in BOTH. `submitConfiguration.type` on user-task forms is `"UNASSIGNED"` (not `"WORKFLOW"` — that's only for start forms). See the worked example in `references/definition-schema.md`.

**Queues vs workflow task steps**
A Domo Queue (`queues create`) is a general user-task inbox, not a workflow step type. Workflow steps route to users, groups, or queues by their resolved IDs — resolve them with `users list`, `users list-groups`, or `queues list` first.

**Workflow model path is `/workflow/v2/models`**
The Domo Workflows API uses `/workflow/v2/models` for model CRUD (not `/workflow/v2/workflows`, which is a legacy alias that the platform redirects internally).

## ODY Validation Error Codes

The `validate` command returns messages with codes in the form `ODY_NNN`. Severity levels: `ERROR` blocks deployment; `WARNING` may block; `INFO` is advisory.

| Code | Severity | Meaning |
|------|----------|---------|
| ODY_003 | ERROR | Node is not connected / structural graph error |
| ODY_010 | INFO | Variable declared in dataList but never used |
| ODY_011 | ERROR | Variable type mismatch (e.g. text assigned to number) |
| ODY_022 | ERROR | rootNode configuration issue |
| ODY_026 | ERROR | Variable mapping issue — variable referenced but not found or wrong type |
| ODY_031 | ERROR | Form configuration issue on a node |
| ODY_033 | ERROR | `assignedTo` user does not have permission to be assigned workflow tasks (insufficient role) |
| ODY_034 | ERROR | `userTaskNode` is missing a `selectedQueue` value |
| ODY_017 | WARN | Both branches of a gateway have explicit conditions (neither is a default/else branch). Safe to ignore — does not block deployment. |
| ODY_046 | ERROR | `selectedQueue` ID does not exist in this Domo instance |
| ODY_048 | ERROR | `userTaskNode` has no form configured (`configType` is null or missing) |
| ODY_052 | INFO | Optional input parameter is not mapped |
| ODY_053 | INFO | Optional output parameter is not mapped |

## Additional Resources

- **`references/api-reference.md`** — Full API endpoint reference for all Domo Workflow operations: paths, methods, parameters, and response shapes
- **`references/definition-schema.md`** — Workflow definition JSON structure, node types (service task, user task, gateway), dataset query steps, Code Engine function wiring, and iterative authoring tips
