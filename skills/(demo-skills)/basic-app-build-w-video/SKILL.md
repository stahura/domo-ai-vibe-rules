---
name: basic-app-build-w-video
description: Orchestrates a new Domo custom app build with Remotion-compatible styling, sample data generation, and automatic demo video creation. Use when you want to build a Domo app AND produce a polished 10-15 second demo video of it in one workflow.
---

# Domo App + Demo Video Build Playbook

## When to use

- Building a new Domo custom app that needs a demo video for stakeholders, documentation, or marketing.
- Taking over an existing app and producing a visual demo alongside normalization.

## How this differs from `basic-app-build`

This playbook wraps the standard Domo app build with three additions:

1. **Remotion-compatible styling constraints** are enforced from Phase 0 so the app's UI can be captured and animated in Remotion without rework.
2. **Sample data generation** (Phase 3A) produces realistic mock data so the demo renders a populated UI without needing live Domo datasets or credentials.
3. **Demo video creation** (Phase 10) uses Remotion to produce a 10-15 second polished video of the finished app.

---

## Progress checklist

Copy this checklist and update it as you work.

```
Demo-Ready Build Progress:
- [ ] Phase 0 : Rules loaded (platform + Remotion styling constraints)
- [ ] Phase 1 : Manifest & contracts
- [ ] Phase 2 : App shell (domo.js)
- [ ] Phase 3 : Data access
- [ ] Phase 3A: Sample data generation
- [ ] Phase 4 : App storage (if needed)
- [ ] Phase 5 : Toolkit clients (if needed)
- [ ] Phase 6 : Feature skills (AI / Code Engine / Workflow — as needed)
- [ ] Phase 7 : UI build (Remotion-safe styling)
- [ ] Phase 8 : Performance review
- [ ] Phase 9 : Build & publish
- [ ] Phase 10: Demo video (Remotion)
- [ ] Phase 11: Verification
```

---

## Phase 0 — Load rules (always-on)

Apply before writing any code:

- `rules/core-custom-apps-rule.md`
- `rules/custom-app-gotchas.md`

### Remotion styling constraints (enforce throughout all phases)

These rules ensure every UI component you build can be screenshot-captured or directly rendered inside a Remotion composition without rework.

| Rule | Why |
|---|---|
| **No CSS `transition-*` or `animation-*` properties** | Remotion cannot capture CSS-driven motion. All animation in the demo will be driven by `useCurrentFrame()`. Static styling (colors, borders, shadows, transforms at rest) is fine. |
| **No Tailwind `transition-*` or `animate-*` utility classes** | Same reason. All other Tailwind utilities are fine and encouraged. |
| **Use inline `style` objects or Tailwind for layout** | Remotion renders React components to frames; CSS modules and scoped styles work, but CSS-in-JS runtime libraries (styled-components, Emotion) may cause hydration issues in the Remotion render pipeline. Prefer inline styles or Tailwind. |
| **Use `<img>` normally in the Domo app** | In the *app* code, use standard `<img>` tags. The Remotion demo will use its own `<Img>` component when composing scenes. This constraint is about **not** relying on lazy-loading or intersection-observer patterns that won't fire in a Remotion frame capture. |
| **Keep visual state deterministic** | Every UI state the demo will show must be reproducible from props/data alone, not from user interaction history or timers. Build components so that passing in sample data produces the exact visual you want in the demo. |
| **Design for 1920x1080** | Ensure the app layout looks good at 1920x1080, since this is the demo video's native resolution. Responsive design is still fine; just verify the 1080p breakpoint. |

---

## Phase 1 — Manifest & contracts

Use `manifest`.

Define all external resource mappings first: datasets, collections, workflows, Code Engine packages. Everything else depends on this.

Use alias-safe names only (`^[A-Za-z][A-Za-z0-9]*$`), no spaces or special characters.

Check root folder for an existing `thumbnail.png` to copy into the app's `public/` folder.

**Existing-app takeover?** Audit the current `manifest.json` against actual code usage before changing anything.

---

## Phase 2 — App shell

Use `domo-js`.

Set up the baseline: `ryuu.js` import, navigation via `domo.navigate()`, event listeners, environment info.

**DA CLI users:** Also use `da-cli` for scaffolding if the user explicitly requests it.

---

## Phase 3 — Data access

Use `dataset-query` (primary) and `data-api` (routing overview).

Build queries with `@domoinc/query`. Before writing UI/data-mapping logic, fetch the real schema for every dataset in `manifest.json datasetsMapping` and create an explicit field map.

**Need raw SQL?** Use `sql-query`, but know that SQL ignores page filters.

---

## Phase 3A — Sample data generation

This is the critical addition for demo-readiness. Generate realistic sample data that:

1. **Populates every view** the demo will show (dashboard, detail panels, charts, tables, chat messages, etc.)
2. **Contains no real customer/user data** — all names, emails, IDs, and metrics are synthetic
3. **Is deterministic** — the same seed produces the same data so screenshots and Remotion captures are reproducible

### How to implement

Create a `src/sample-data/` directory in the app with:

```
src/sample-data/
  index.ts          # Re-exports all sample datasets; single import point
  datasets/
    <alias>.ts      # One file per manifest dataset alias, exporting typed arrays
  README.md         # Documents the shape and purpose of each sample dataset
```

#### For each dataset alias in `manifest.json`:

1. Create a TypeScript file exporting a typed array matching the dataset's field map from Phase 3.
2. Generate 20-100 rows of realistic data (enough to fill charts and tables convincingly).
3. Use the actual field names from the dataset schema — not guesses.
4. Include a range of values that produces interesting visual patterns (trends, outliers, category distribution).

```typescript
// src/sample-data/datasets/sales.ts
export type SalesRow = {
  Date: string;
  Region: string;
  Product: string;
  Revenue: number;
  Units: number;
};

export const salesData: SalesRow[] = [
  { Date: "2026-01-15", Region: "West", Product: "Widget A", Revenue: 12400, Units: 62 },
  { Date: "2026-01-16", Region: "East", Product: "Widget B", Revenue: 8750, Units: 35 },
  // ... 20-100 rows with realistic distribution
];
```

#### Wire sample data into the app

Create a data-access layer that switches between live Domo queries and sample data:

```typescript
// src/data/use-dataset.ts
import { salesData } from "../sample-data/datasets/sales";

const USE_SAMPLE_DATA = !window.__DOMO_ENV__; // true outside Domo runtime

export async function fetchSalesData(): Promise<SalesRow[]> {
  if (USE_SAMPLE_DATA) {
    return salesData;
  }
  // Real query via @domoinc/query
  return new Query().select([...]).fetch("sales");
}
```

This ensures:
- **In Domo:** the app queries real datasets as normal.
- **Locally / in Remotion:** the app renders with sample data, no credentials needed.
- **Security:** no real data is ever baked into the demo video.

#### Sample data for non-dataset sources

| Source | Sample strategy |
|---|---|
| AppDB collections | Export sample document arrays in `src/sample-data/collections/<name>.ts` |
| AI responses | Export canned response strings in `src/sample-data/ai-responses.ts` |
| User identity | Export a mock user object: `{ displayName: "Alex Demo", email: "alex@example.com", role: "Admin" }` |
| Workflow results | Export sample status objects in `src/sample-data/workflows/<name>.ts` |

---

## Phase 4 — App storage (if needed)

Use `appdb` and `appdb-collection-create` when storage must be created.

Skip if the app only reads datasets.

---

## Phase 5 — Toolkit clients (if needed)

Use `toolkit`.

Use typed `@domoinc/toolkit` clients where they add value.

---

## Phase 6 — Feature skills (as needed)

Only load the skills your app actually requires:

| Feature needed | Skill |
|---|---|
| AI text generation or text-to-SQL | `ai-service-layer` |
| Server-side functions (secrets, external APIs) | `code-engine` + `code-engine-create` + `code-engine-update` |
| Triggering automation workflows | `workflow` |

Skip this phase if none of these features are needed.

---

## Phase 7 — UI build (Remotion-safe styling)

Build the app's UI components. This is standard React development with the Remotion constraints from Phase 0 enforced:

- Use Tailwind utilities or inline `style` objects for all styling.
- No `transition-*`, `animate-*`, or CSS keyframe animations.
- All visual states must be reproducible from props + sample data (Phase 3A).
- Verify the layout at 1920x1080.
- Every "scene" the demo will show (loading state, populated dashboard, detail view, etc.) should be reachable by passing different sample data, not by simulating user clicks.

### Component design for demo-ability

Structure components so each visual state is a function of data:

```tsx
// Good: demo can render any state by passing props
<ChatPanel messages={sampleMessages} isTyping={false} />
<ChatPanel messages={sampleMessages} isTyping={true} />

// Bad: state is internal and requires user interaction to reach
<ChatPanel /> // internally manages messages via useState
```

You don't need to refactor the entire app this way — just the views you want in the demo. Expose the 3-5 key visual states as prop-driven variants.

---

## Phase 8 — Performance review

Use `performance`.

Review all queries. Check for full-dataset fetches, missing aggregations, unnecessary columns.

---

## Phase 9 — Build & publish

Use `publish`.

`npm run build` -> `cd dist` -> `domo publish`. Copy generated `id` back to source manifest on first publish.

---

## Phase 10 — Demo video (Remotion)

The demo video renders the **actual app components** directly inside Remotion — not screenshots, not title cards, not marketing slides. The viewer should see the real UI populated with sample data, with animated scrolling or view changes to show all parts of the app.

### 10.1 — Scaffold the Remotion project

Create a `demo/` directory alongside the app source:

```
my-app/
  src/            # Domo app source
  demo/           # Remotion demo project
    src/
      Root.tsx
      DemoVideo.tsx
      index.ts
    remotion.config.ts  # Webpack alias to import app components
    package.json
```

#### package.json

The demo project must include the same UI dependencies the app uses (e.g., `recharts`) so Remotion can render the actual components:

```json
{
  "dependencies": {
    "@remotion/cli": "^4.0.0",
    "@remotion/transitions": "^4.0.0",
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "recharts": "^2.12.0",
    "remotion": "^4.0.0"
  }
}
```

Add any other UI library the app uses (chart libraries, UI component kits, etc.).

#### remotion.config.ts — Webpack alias for app imports

This is critical. Configure a `@app` alias so demo code can import directly from the app's `src/`:

```ts
import { Config } from '@remotion/cli/config';
import path from 'path';

Config.overrideWebpackConfig((currentConfiguration) => ({
  ...currentConfiguration,
  resolve: {
    ...currentConfiguration.resolve,
    alias: {
      ...currentConfiguration.resolve?.alias,
      '@app': path.resolve(process.cwd(), '..', 'src'),
    },
  },
}));
```

#### index.ts — Remotion entry point

```ts
import { registerRoot } from 'remotion';
import { RemotionRoot } from './Root';
registerRoot(RemotionRoot);
```

#### tsconfig.json — Path mapping

```json
{
  "compilerOptions": {
    "paths": { "@app/*": ["../src/*"] },
    "baseUrl": "."
  },
  "include": ["src", "../src"]
}
```

### 10.2 — AnimatedCursor component

Create a reusable cursor that moves between positions and shows click pulses. This sells the illusion of someone using the app.

Place in `demo/src/components/AnimatedCursor.tsx`:

```tsx
import React from 'react';
import { useCurrentFrame, useVideoConfig, interpolate, spring, Easing } from 'remotion';

export type CursorWaypoint = {
  x: number;       // Pixel position from left
  y: number;       // Pixel position from top
  atFrame: number; // Frame at which cursor should arrive here
  click?: boolean; // Show a click pulse when arriving
};

type Props = {
  waypoints: CursorWaypoint[];
  size?: number;  // Default 20
};

export const AnimatedCursor: React.FC<Props> = ({ waypoints, size = 20 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  if (waypoints.length === 0) return null;

  // Find which two waypoints we're interpolating between
  let fromWp = waypoints[0];
  let toWp = waypoints[0];
  for (let i = 0; i < waypoints.length - 1; i++) {
    if (frame >= waypoints[i].atFrame) {
      fromWp = waypoints[i];
      toWp = waypoints[i + 1];
    }
  }
  if (frame >= waypoints[waypoints.length - 1].atFrame) {
    fromWp = waypoints[waypoints.length - 1];
    toWp = fromWp;
  }

  const easing = Easing.inOut(Easing.quad);
  const x = fromWp === toWp ? fromWp.x
    : interpolate(frame, [fromWp.atFrame, toWp.atFrame], [fromWp.x, toWp.x],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing });
  const y = fromWp === toWp ? fromWp.y
    : interpolate(frame, [fromWp.atFrame, toWp.atFrame], [fromWp.y, toWp.y],
        { extrapolateLeft: 'clamp', extrapolateRight: 'clamp', easing });

  // Click pulse at waypoints marked click: true
  let pulseOpacity = 0;
  let pulseScale = 0;
  for (const wp of waypoints) {
    if (wp.click && frame >= wp.atFrame && frame < wp.atFrame + 20) {
      const p = spring({ frame: frame - wp.atFrame, fps, config: { damping: 20, stiffness: 200 } });
      pulseScale = interpolate(p, [0, 1], [0.5, 1.5]);
      pulseOpacity = interpolate(frame - wp.atFrame, [0, 20], [0.5, 0], { extrapolateRight: 'clamp' });
    }
  }

  return (
    <div style={{ position: 'absolute', inset: 0, pointerEvents: 'none', zIndex: 9999 }}>
      {pulseOpacity > 0 && (
        <div style={{
          position: 'absolute', left: x - 15, top: y - 15,
          width: 30, height: 30, borderRadius: '50%',
          border: '2px solid rgba(255,255,255,0.8)',
          transform: `scale(${pulseScale})`, opacity: pulseOpacity,
        }} />
      )}
      <svg style={{ position: 'absolute', left: x, top: y, width: size, height: size,
        filter: 'drop-shadow(0 2px 4px rgba(0,0,0,0.5))' }} viewBox="0 0 24 24" fill="none">
        <path d="M5 3L19 12L12 12L8 21L5 3Z" fill="white" stroke="#1e293b"
          strokeWidth="1.5" strokeLinejoin="round" />
      </svg>
    </div>
  );
};
```

### 10.3 — Root.tsx

```tsx
import { Composition } from 'remotion';
import { DemoVideo } from './DemoVideo';

export const RemotionRoot = () => (
  <Composition
    id="AppDemo"
    component={DemoVideo}
    durationInFrames={300}  // 10s at 30fps
    fps={30}
    width={1920}
    height={1080}
  />
);
```

### 10.4 — Demo patterns by app type

Pick the pattern that matches your app and combine them if needed. All patterns import the real app components via `@app/`.

#### Pattern A: Single-view scroll (dashboards, tables, long forms)

Render the component and animate `translateY` to scroll through it.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';
import { Dashboard } from '@app/App';
import { sampleData } from '@app/sample-data';
import { AnimatedCursor } from './components/AnimatedCursor';

export const DemoVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scrollY = interpolate(frame, [2 * fps, 6 * fps], [0, -500], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad),
  });

  return (
    <AbsoluteFill style={{ backgroundColor: '#0f172a', overflow: 'hidden' }}>
      <div style={{ transform: `translateY(${scrollY}px)`, width: '100%' }}>
        <Dashboard data={sampleData} />
      </div>
      <AnimatedCursor waypoints={[
        { x: 700, y: 400, atFrame: 0 },
        { x: 700, y: 500, atFrame: Math.round(3 * fps) },
        { x: 500, y: 450, atFrame: Math.round(6 * fps) },
      ]} />
    </AbsoluteFill>
  );
};
```

#### Pattern B: Tabbed / multi-view apps (most common)

Use `<Sequence>` to switch between views. The cursor moves to the tab/button, a click pulse fires, and the next Sequence renders the new view.

```tsx
import { AbsoluteFill, Sequence, useCurrentFrame, useVideoConfig, interpolate, Easing } from 'remotion';
import { Dashboard } from '@app/App';
import { sampleData } from '@app/sample-data';
import { AnimatedCursor } from './components/AnimatedCursor';

const OverviewScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scrollY = interpolate(frame, [2 * fps, 4 * fps], [0, -350], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad),
  });

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <div style={{ transform: `translateY(${scrollY}px)`, width: '100%' }}>
        <Dashboard data={sampleData} activeTab="overview" />
      </div>
      <AnimatedCursor waypoints={[
        { x: 700, y: 400, atFrame: 0 },
        { x: 900, y: 450, atFrame: Math.round(3 * fps) },
        // End near the target tab button
        { x: 1195, y: 48, atFrame: Math.round(4.5 * fps) },
      ]} />
    </AbsoluteFill>
  );
};

const DetailScene: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const scrollY = interpolate(frame, [2 * fps, 4 * fps], [0, -200], {
    extrapolateLeft: 'clamp', extrapolateRight: 'clamp',
    easing: Easing.inOut(Easing.quad),
  });

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <div style={{ transform: `translateY(${scrollY}px)`, width: '100%' }}>
        <Dashboard data={sampleData} activeTab="detail" selectedItem={sampleData.items[0]} />
      </div>
      <AnimatedCursor waypoints={[
        { x: 1195, y: 48, atFrame: 0, click: true },  // Click the tab
        { x: 600, y: 300, atFrame: Math.round(0.8 * fps) },
        { x: 500, y: 400, atFrame: Math.round(3 * fps) },
      ]} />
    </AbsoluteFill>
  );
};

export const DemoVideo: React.FC = () => {
  const { fps } = useVideoConfig();
  return (
    <AbsoluteFill>
      <Sequence from={0} durationInFrames={5 * fps} premountFor={fps}>
        <OverviewScene />
      </Sequence>
      <Sequence from={5 * fps} durationInFrames={5 * fps} premountFor={fps}>
        <DetailScene />
      </Sequence>
    </AbsoluteFill>
  );
};
```

**Key:** The cursor's last waypoint in Scene 1 and first waypoint in Scene 2 should be at the same position (the tab button) to create a seamless "click" effect across the cut.

#### Pattern C: AI chat / conversational apps

Render the chat component with progressively more messages using frame-based array slicing. This shows messages "arriving" without needing actual interaction.

```tsx
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from 'remotion';
import { ChatPanel } from '@app/components/ChatPanel';
import { sampleMessages } from '@app/sample-data';
import { AnimatedCursor } from './components/AnimatedCursor';

// Pre-define which messages are visible at which frame
const messageTimeline = [
  { visibleCount: 2, atFrame: 0 },    // Start with 2 messages already visible
  { visibleCount: 3, atFrame: 60 },   // User message appears at 2s
  { visibleCount: 3, typingIndicator: true, atFrame: 90 },  // AI typing at 3s
  { visibleCount: 4, atFrame: 120 },  // AI response appears at 4s
  { visibleCount: 5, atFrame: 180 },  // Another user message at 6s
  { visibleCount: 5, typingIndicator: true, atFrame: 210 },
  { visibleCount: 6, atFrame: 240 },  // Final AI response at 8s
];

export const DemoVideo: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Find current state based on frame
  let currentState = messageTimeline[0];
  for (const state of messageTimeline) {
    if (frame >= state.atFrame) currentState = state;
  }

  const visibleMessages = sampleMessages.slice(0, currentState.visibleCount);

  return (
    <AbsoluteFill style={{ overflow: 'hidden' }}>
      <ChatPanel
        messages={visibleMessages}
        isTyping={currentState.typingIndicator ?? false}
      />
      <AnimatedCursor waypoints={[
        { x: 960, y: 800, atFrame: 0 },
        // Cursor moves to input area before "sending" a message
        { x: 700, y: 950, atFrame: 50, click: true },
        { x: 960, y: 600, atFrame: 90 },   // Watches AI type
        { x: 700, y: 950, atFrame: 170, click: true },  // Sends another
        { x: 960, y: 500, atFrame: 240 },  // Reads response
      ]} />
    </AbsoluteFill>
  );
};
```

**Key for chat apps:** The `ChatPanel` component must accept `messages` and `isTyping` as props (Phase 7 enforces this). The sample data in Phase 3A should include a realistic conversation thread.

#### Pattern D: Button / interaction-heavy apps (dispatch boards, forms)

Render different prop states in sequence to simulate button clicks. Use the cursor to point at the button, fire a click pulse, and switch to the "after" state.

```tsx
// Scene 1: Empty form state, cursor fills in a field
<Sequence from={0} durationInFrames={4 * fps}>
  <FormView formData={emptyForm} />
  <AnimatedCursor waypoints={[
    { x: 500, y: 300, atFrame: 0 },
    { x: 500, y: 300, atFrame: 30, click: true },
  ]} />
</Sequence>

// Scene 2: Filled form, cursor clicks submit
<Sequence from={4 * fps} durationInFrames={3 * fps}>
  <FormView formData={filledForm} />
  <AnimatedCursor waypoints={[
    { x: 500, y: 600, atFrame: 0 },
    { x: 500, y: 600, atFrame: 30, click: true },  // Click "Submit"
  ]} />
</Sequence>

// Scene 3: Success state
<Sequence from={7 * fps} durationInFrames={3 * fps}>
  <FormView formData={filledForm} submitSuccess={true} />
</Sequence>
```

### 10.5 — Cursor waypoint positioning tips

- **Finding coordinates:** Run `npx remotion studio`, hover over the preview, and note the pixel coordinates where buttons/tabs/elements are rendered.
- **Match across Sequences:** When the cursor "clicks" a tab at the end of Scene 1, its first position in Scene 2 should be the same coordinates — this creates a seamless transition.
- **Movement speed:** Keep moves to 30-60 frames (1-2s). Faster looks frantic, slower looks boring.
- **Don't over-animate:** 2-3 cursor moves per scene is enough. The cursor should guide attention, not distract.

### 10.6 — Preview and render

```bash
cd demo
npx remotion studio          # Preview in browser
npx remotion render AppDemo  # Render to out/AppDemo.mp4
```

---

## Phase 11 — Verification

After publishing, confirm:

- App loads without console errors in Domo
- All dataset aliases resolve (no 404s on data calls)
- AppDB collections are wired in the card UI (if used)
- Page filters propagate correctly (if app is embedded in a dashboard)
- Navigation uses `domo.navigate()`, not `<a href>`
- Thumbnail has been copied into the `public/` folder
- **Sample data renders correctly** when running outside Domo (no undefined/null errors)
- **Demo video renders** without blank frames or missing assets (`npx remotion render AppDemo`)
- **Demo video shows populated UI** — not empty states or loading spinners

---

## Build-time guardrails

- Client-side only: no SSR/server routes/server components.
- Use Vite `base: './'`.
- Prefer `HashRouter` unless rewrites are intentionally handled.
- Treat `domo.env.*` as convenience only; use verified identity for trust decisions.
- **No CSS transitions or animations** in any component the demo will capture.
- **Sample data must contain zero real customer data.**
- **All demo visual states must be prop-driven**, not interaction-driven.
