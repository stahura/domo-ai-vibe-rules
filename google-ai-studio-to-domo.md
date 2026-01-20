# Rule: Migrate Google AI Studio prototype to Domo App Platform Custom App (static dist deploy)

You are converting a project that began in Google AI Studio (often Cloud Run / preview oriented) into a Domo App Platform Custom App deployed as static assets via the Domo CLI.
The required deployment contract is:
1) `npm run build` must produce a self-contained `dist/` folder
2) `cd dist && domo publish` must work (Domo serves the app from a subpath, not from site root)
3) The app must load assets correctly and not break on refresh/navigation

## Detect AI Studio origin
Treat the project as "AI Studio-origin" if you see any of:
- README mentions Google AI Studio / Gemini API / "Build" mode / Cloud Run
- cloudbuild.yaml, Dockerfile, or Cloud Run deploy instructions
- use of `process.env.GEMINI_API_KEY` or placeholders described as "provided by AI Studio"
- structure that runs via a server/container rather than static hosting

If detected, apply the steps below.

---

## Primary objective
Make the project a conventional front-end that:
- runs locally with `npm run dev`
- produces production files with `npm run build` into `dist/`
- can be hosted from a non-root subpath (Domo App Platform)
- does NOT require any server runtime to render the UI

---

## Step 1 — Ensure a standard build pipeline exists
Open `package.json` and ensure scripts exist and are correct for the chosen toolchain:

- If it is Vite:
  - `dev`: `vite`
  - `build`: `vite build`
  - `preview`: `vite preview`
  - Confirm output is `dist/`

- If it is CRA:
  - `build` outputs `build/` by default (NOT acceptable for our contract)
  - Either:
    A) migrate to Vite (preferred for App Platform), OR
    B) update Domo publish docs/commands accordingly (only if user explicitly wants CRA)

Default to Vite if uncertain.

Acceptance criteria:
- `npm install` succeeds
- `npm run build` creates `dist/` with `index.html` and `assets/*`

---

## Step 2 — Fix base path so assets work in Domo (subpath hosting)
Domo App Platform does NOT host your app at `/`. It’s under a nested path.
Therefore asset paths MUST be relative or explicitly configured.

- If Vite: set base to relative
  - in `vite.config.*`: `base: './'`

- If other bundler: ensure the equivalent "public path" is relative.

Acceptance criteria:
- Opening the built `dist/index.html` from a nested path still loads JS/CSS assets (no 404s).
- No hardcoded absolute asset paths like `/assets/...` unless you know the host root.

---

## Step 3 — Make routing robust for static hosting
If the app uses React Router (or any client router):
- Prefer HashRouter for App Platform unless you know the platform provides SPA rewrites.
- If switching to HashRouter is too invasive, document that refresh on deep routes will 404 unless Domo is configured with a rewrite rule.

Default action:
- If router is present and no rewrite control is known: switch to `HashRouter`.

Acceptance criteria:
- Built app can navigate and refresh without server rewrites.

---

## Step 4 — Environment variables and secrets: remove AI Studio-only assumptions
AI Studio can "magically" provide placeholders (e.g., Gemini API key) during its hosted run.
In Domo App Platform, the browser cannot safely hold secrets.

Rules:
- Do NOT ship any raw API keys in client code.
- If the UI needs Gemini/LLM calls:
  - Prefer Domo AI APIs via domo.js if available/allowed, OR
  - Proxy through a backend (e.g., Domo Code Engine) that injects secrets server-side.
- Replace `process.env.*` patterns with toolchain-native env usage:
  - Vite: `import.meta.env.VITE_*`
- Add `.env.example` documenting required variables (non-secret only).

Acceptance criteria:
- No committed secrets.
- No runtime crashes from missing AI Studio env injection.

---

## Step 5 — Domo deploy contract
Ensure the final developer workflow is:
- `npm run build`
- `cd dist`
- `domo publish`

If a Domo manifest/config file is required by the App Platform project (e.g., `manifest.json`), ensure it is located where Domo expects it OR copied into `dist/` during build.

If the platform expects the manifest in the root but publishes `dist/`, implement one of:
- Copy required config/manifest into `dist/` as part of build (postbuild script)
- Or adjust publish strategy if the user’s established standard differs

Default:
- Add a `postbuild` script to copy required app platform files into `dist/` if they are missing there.

Acceptance criteria:
- `dist/` contains everything needed to publish and run.
- `domo publish` from inside `dist/` works without manual file copying.

---

## Output requirements (what you must deliver as the assistant)
After applying changes, provide:
1) A short list of files changed
2) The exact commands to run locally
3) A "done checklist" confirming:
   - build produces `dist/`
   - assets load under subpath
   - routing works (hash router or documented rewrite need)
   - no secrets in client

Be decisive; implement changes rather than asking follow-up questions unless blocked by missing files.
