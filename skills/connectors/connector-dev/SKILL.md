---
name: connector-dev
description: "**Custom Domo connector authorship** — invoke when someone is writing the JavaScript code that defines a custom Domo connector. Primary signals: questions about authentication.js, dataProcessing.js, or Domo's connector APIs (datagrid, httprequest, auth, metadata). Covers all connector coding topics: auth credential validation, API pagination loops, writeback connectors, column consistency, connector README docs. The user is *building* a connector in Connector Dev Studio, not using a pre-built one. Skip for: pre-built connectors (Salesforce, Postgres, Snowflake), Python connector, Domo App Platform cards/apps, Workflows, Federated Connectors."
---

# Scope

This skill is for **Domo Custom Connector IDE** projects — not Domo App Platform custom app/card builds. Custom connectors run server-side after being published via the Connector Dev Studio.

---

## File Structure

- **`authentication.js`** — Validates credentials and authenticates with the external API
- **`dataProcessing.js`** — Fetches and processes data from the external API
- **`README.md`** — Documents available reports and parameters

---

## Key Patterns

### Authentication
- Sanitize credential inputs (regex validate API keys/tokens) before use
- Set required headers, then make a lightweight test request to verify credentials
- Call `auth.authenticationSuccess()` or `auth.authenticationFailed('reason')` — never leave authentication ambiguous

### Data Processing
- Check `httprequest.getStatusCode()` before parsing the response body
- Use `datagrid.magicParseJSON(jsonArray)` for JSON array responses — avoids manual column mapping
- Handle pagination in a `do...while` loop; use the next-page link or cursor from the response as the loop condition
- Use `metadata.report` to branch between report types; use `metadata.account.*` for credentials

### Error Handling
- Catch HTTP errors by status code; try to parse the error body for a human-readable message
- Fall back to the raw response substring if the error body isn't parseable JSON
- Re-throw errors so the connector runtime surfaces them correctly

---

## Rules

1. **Input sanitization** — Always sanitize inputs (API keys, user params) to prevent injection attacks
2. **Consistent columns** — Every row must have the same columns; use `null` for missing values
3. **Domo library** — Use Domo-provided methods (`httprequest`, `datagrid`, `auth`, `metadata`); see [reference docs](https://developer.domo.com/portal/e415bb99d21b2-reference)
4. **Clear error messages** — `auth.authenticationFailed()` messages should tell the user what to fix

---

## Code Examples

If you need full boilerplate for authentication, data processing, or error handling patterns, read `references/examples.md`.

---

## Checklist
- [ ] `authentication.js` validates input format and tests credentials
- [ ] `authentication.js` calls `auth.authenticationSuccess()` or `auth.authenticationFailed()` appropriately
- [ ] `dataProcessing.js` handles pagination correctly
- [ ] `dataProcessing.js` checks HTTP status codes before parsing JSON
- [ ] `dataProcessing.js` uses `datagrid.magicParseJSON()` for JSON arrays
- [ ] All inputs are sanitized
- [ ] Error messages are clear and actionable
- [ ] `README.md` documents all reports/parameters
- [ ] All rows have consistent column counts
