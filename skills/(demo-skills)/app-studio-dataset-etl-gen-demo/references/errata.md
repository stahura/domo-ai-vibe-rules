# Skill Errata — Statements That Directly Caused Errors

These are specific lines in existing docs that commonly trigger API errors or wasted debugging.

---

## 1) Theme JSON import format vs API format

- UI import examples (index/tag style) are not directly usable for API updates.
- API update format requires slot ids and wrapped values:
  - `{"id":"c1","value":{"value":"#HEX","type":"RGB_HEX"},"tags":[...]}`

---

## 2) Card style `dropShadow`

- Valid values: `null`, `"FLOATING"`, `"STANDARD"`
- Invalid: `"NONE"` (causes 400)

---

## 3) Font payload format

- `weight` must be numeric (300/400/500/600/700)
- `size` must be integer (not `"22px"`)
- `style` should be `"Regular"`

---

## 4) Card padding format

- Use object format:
  - `{"left": 0, "right": 0, "top": 0, "bottom": 0}`
- Do not use scalar integer padding in API bodies.

---

## 5) Navigation icon automation expectation

- Reorder is supported by CLI.
- Icon assignment is not reliably programmable through current CLI-exposed endpoints.
- Set icons manually in the App Studio UI.
