---
name: app-studio-demo-capture
description: Capture animated demo videos of deployed Domo App Studio apps using Playwright browser automation. Navigates pages, scrolls content, records smooth video of the real production UI (left-nav, native cards, pro-code cards, theme, data). No sample data or Remotion — captures what the user actually sees. Use when a deployed App Studio app needs a polished walkthrough video, animated GIF, or multi-page screenshot set.
---

# App Studio Demo Capture

> **What this is**: A Playwright-based pipeline that opens a real Domo App Studio app in an authenticated headless browser, navigates through pages, scrolls, and records a polished demo video. Captures the full production experience — left-nav, native cards, pro-code iframes, applied theme, live data.
>
> **What this is NOT**: This is not Remotion. It does not render React components in Node.js or use sample data. If you need component-level rendering with synthetic data and animated cursors, use `demo-ready-build` instead.

## When to Use

- After deploying an App Studio app (via `app-studio` + `app-studio-pro-code` pipeline) and you want a walkthrough video
- When the user says "demo", "walkthrough", "animated preview", "record the app", or "show me what it looks like"
- When generating eval screenshots for comparison or documentation
- When producing content for pitch decks, stakeholder reviews, or marketing

## Prerequisites

1. **App is deployed** — the App Studio app exists on the Domo instance with all pages, cards, themes, and data
2. **Playwright installed** — `npm install playwright` in the project directory
3. **Domo authentication** — a valid session ID obtainable via `domo login` or the `upload_bridge.get_sid()` helper
4. **ffmpeg installed** (for post-processing) — `brew install ffmpeg` on macOS

## Pipeline Overview

```
┌─────────────┐     ┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│ Authenticate │ ──▶ │ Capture      │ ──▶ │ Post-process  │ ──▶ │ Output       │
│ (get SID)    │     │ (Playwright) │     │ (ffmpeg)      │     │ (.mp4/.gif)  │
└─────────────┘     └──────────────┘     └───────────────┘     └──────────────┘
```

Three capture modes, in order of complexity:

| Mode | Method | Output | Best for |
|------|--------|--------|----------|
| **Screenshots** | `page.screenshot()` per page | PNGs | Static eval, deck slides, documentation |
| **Scroll video** | Playwright `recordVideo` + scripted scroll | Raw MP4 per page | Smooth page walkthroughs |
| **Full walkthrough** | Playwright `recordVideo` + nav + scroll across all pages | Single MP4 | Polished demo videos |

## Mode 1: Multi-Page Screenshots (Proven Pattern)

This is the existing `screenshot.js` pattern — battle-tested across dozens of App Studio apps.

### Usage

```bash
node screenshot.js app <appId> '<json-pageIds>' [outputDir]
```

### Example

```bash
node screenshot.js app 396231467 '{"Overview":"1942764543","Sales":"1942764544","Inventory":"1942764545","Performance":"1942764546"}' ./demo-output/screenshots
```

### Integration in Python build scripts

```python
import subprocess, json

page_ids = {"Overview": str(overview_id), "Sales": str(sales_id), ...}
subprocess.run([
    "node", "screenshot.js", "app", str(app_id),
    json.dumps(page_ids), f"./{app_name}/screenshots"
], check=True)
```

### Key implementation details (from proven `screenshot.js`)

- **Viewport**: 1440x900 with `deviceScaleFactor: 2` (produces 2880x1800 retina PNGs)
- **Auth**: Inject `X-Domo-Authentication` header via `page.route('**/*')` interception
- **Wait strategy**: `waitUntil: 'networkidle'` + additional `waitForTimeout(8000)` for pro-code iframes to render
- **Full page**: `fullPage: true` captures content below the fold
- **Error recovery**: On navigation failure, capture an `_error.png` for debugging

### Also capture supporting assets

```bash
# Dataset details pages
node screenshot.js datasets '{"sales":"guid1","inventory":"guid2"}' ./demo-output/datasets

# Magic ETL dataflow graph
node screenshot.js etl <dataflowId> ./demo-output/etl

# Arbitrary Domo URLs
node screenshot.js urls '{"landing":"https://modocorp.domo.com/page/123"}' ./demo-output/urls
```

---

## Mode 2: Per-Page Scroll Video

Record a smooth scroll-through of each page individually. Produces one MP4 per page.

### Script: `demo-capture.js`

```javascript
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const INSTANCE = 'modocorp';

function getSid() {
  const result = execSync(
    `cd "${path.join(__dirname, 'domo_data_generator')}" && python3 -c "from upload_bridge import get_sid; print(get_sid('${INSTANCE}'));"`,
    { encoding: 'utf-8' }
  ).trim();
  return result.split('\n').pop().trim();
}

async function capturePageVideo(browser, sid, appId, pageName, pageId, outputDir, options = {}) {
  const {
    scrollDistance = 600,
    scrollStepPx = 2,
    scrollIntervalMs = 16,
    holdTopMs = 3000,
    holdBottomMs = 2000,
    loadWaitMs = 8000,
  } = options;

  const videoDir = path.join(outputDir, '_raw_video');
  fs.mkdirSync(videoDir, { recursive: true });

  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: videoDir, size: { width: 1440, height: 900 } },
  });

  const page = await context.newPage();

  await page.route('**/*', (route, request) => {
    const url = request.url();
    if (url.includes('.domo.com') || url.includes('domoapps.')) {
      route.continue({ headers: { ...request.headers(), 'X-Domo-Authentication': sid } });
    } else {
      route.continue();
    }
  });

  const url = `https://${INSTANCE}.domo.com/app-studio/${appId}/pages/${pageId}`;
  console.log(`  Recording ${pageName}: ${url}`);

  await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(loadWaitMs);

  // Hold at top
  await page.waitForTimeout(holdTopMs);

  // Smooth scroll down
  const scrollSteps = Math.ceil(scrollDistance / scrollStepPx);
  for (let i = 0; i < scrollSteps; i++) {
    await page.evaluate((px) => window.scrollBy(0, px), scrollStepPx);
    await page.waitForTimeout(scrollIntervalMs);
  }

  // Hold at bottom
  await page.waitForTimeout(holdBottomMs);

  // Close context to finalize video
  const videoPath = await page.video().path();
  await context.close();

  // Move to final location
  const finalPath = path.join(outputDir, `${pageName}.webm`);
  fs.renameSync(videoPath, finalPath);
  console.log(`  Saved: ${finalPath}`);

  return finalPath;
}

async function captureAllPages(appId, pageIds, outputDir, options = {}) {
  fs.mkdirSync(outputDir, { recursive: true });
  const sid = getSid();
  console.log(`SID obtained (${sid.substring(0, 12)}...)`);

  const browser = await chromium.launch({ headless: true });
  const videoPaths = [];

  for (const [pageName, pageId] of Object.entries(pageIds)) {
    const vp = await capturePageVideo(browser, sid, appId, pageName, pageId, outputDir, options);
    videoPaths.push(vp);
  }

  await browser.close();
  console.log('All pages recorded.');
  return videoPaths;
}

// CLI
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node demo-capture.js <appId> <json-pageIds> [outputDir] [scrollDistance]');
  process.exit(1);
}

const appId = args[0];
const pageIds = JSON.parse(args[1]);
const outputDir = args[2] || path.join(__dirname, 'demo-output', `app-${appId}`);
const scrollDistance = args[3] ? parseInt(args[3]) : 600;

captureAllPages(appId, pageIds, outputDir, { scrollDistance })
  .catch(err => { console.error('Fatal:', err); process.exit(1); });
```

### Usage

```bash
node demo-capture.js 396231467 '{"Overview":"1942764543","Sales":"1942764544"}' ./demo-output 800
```

---

## Mode 3: Full Walkthrough Video

Record a single continuous video that navigates through all pages — simulating a user clicking through the left-nav. This produces the most polished output.

### Script: `demo-walkthrough.js`

```javascript
const { chromium } = require('playwright');
const { execSync } = require('child_process');
const path = require('path');
const fs = require('fs');

const INSTANCE = 'modocorp';

function getSid() {
  const result = execSync(
    `cd "${path.join(__dirname, 'domo_data_generator')}" && python3 -c "from upload_bridge import get_sid; print(get_sid('${INSTANCE}'));"`,
    { encoding: 'utf-8' }
  ).trim();
  return result.split('\n').pop().trim();
}

async function recordWalkthrough(appId, pageIds, outputDir, options = {}) {
  const {
    scrollDistance = 600,
    scrollStepPx = 2,
    scrollIntervalMs = 16,
    holdPageMs = 3000,
    loadWaitMs = 8000,
    transitionPauseMs = 2000,
  } = options;

  fs.mkdirSync(outputDir, { recursive: true });
  const videoDir = path.join(outputDir, '_raw_video');
  fs.mkdirSync(videoDir, { recursive: true });

  const sid = getSid();
  console.log(`SID obtained (${sid.substring(0, 12)}...)`);

  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1440, height: 900 },
    recordVideo: { dir: videoDir, size: { width: 1440, height: 900 } },
  });

  const page = await context.newPage();
  await page.route('**/*', (route, request) => {
    const url = request.url();
    if (url.includes('.domo.com') || url.includes('domoapps.')) {
      route.continue({ headers: { ...request.headers(), 'X-Domo-Authentication': sid } });
    } else {
      route.continue();
    }
  });

  const entries = Object.entries(pageIds);
  console.log(`Recording walkthrough: ${entries.length} pages`);

  for (let i = 0; i < entries.length; i++) {
    const [pageName, pageId] = entries[i];
    const url = `https://${INSTANCE}.domo.com/app-studio/${appId}/pages/${pageId}`;
    console.log(`  Page ${i + 1}/${entries.length}: ${pageName}`);

    await page.goto(url, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(i === 0 ? loadWaitMs : loadWaitMs / 2);

    // Hold at top
    await page.waitForTimeout(holdPageMs);

    // Smooth scroll
    const scrollSteps = Math.ceil(scrollDistance / scrollStepPx);
    for (let s = 0; s < scrollSteps; s++) {
      await page.evaluate((px) => window.scrollBy(0, px), scrollStepPx);
      await page.waitForTimeout(scrollIntervalMs);
    }

    // Hold at scroll position
    await page.waitForTimeout(holdPageMs / 2);

    // Scroll back to top before navigating to next page
    await page.evaluate(() => window.scrollTo({ top: 0, behavior: 'instant' }));
    await page.waitForTimeout(transitionPauseMs);
  }

  const videoPath = await page.video().path();
  await context.close();
  await browser.close();

  // Move raw video to output
  const rawPath = path.join(outputDir, 'walkthrough_raw.webm');
  fs.renameSync(videoPath, rawPath);
  console.log(`Raw walkthrough: ${rawPath}`);

  return rawPath;
}

// CLI
const args = process.argv.slice(2);
if (args.length < 2) {
  console.log('Usage: node demo-walkthrough.js <appId> <json-pageIds> [outputDir]');
  process.exit(1);
}

recordWalkthrough(args[0], JSON.parse(args[1]), args[2] || `./demo-output/app-${args[0]}`)
  .catch(err => { console.error('Fatal:', err); process.exit(1); });
```

### Usage

```bash
node demo-walkthrough.js 396231467 \
  '{"Overview":"1942764543","Sales":"1942764544","Inventory":"1942764545","Performance":"1942764546"}' \
  ./demo-output
```

---

## Post-Processing with ffmpeg

### Convert WebM to MP4

Playwright records in WebM (VP8). Convert to MP4 (H.264) for universal compatibility:

```bash
ffmpeg -i walkthrough_raw.webm -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -movflags +faststart walkthrough.mp4
```

### Stitch per-page videos into one

If using Mode 2 (per-page videos), concatenate them:

```bash
# Create concat list
echo "file 'Overview.webm'" > concat.txt
echo "file 'Sales.webm'" >> concat.txt
echo "file 'Inventory.webm'" >> concat.txt
echo "file 'Performance.webm'" >> concat.txt

# Concatenate and convert
ffmpeg -f concat -safe 0 -i concat.txt -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p demo.mp4
```

### Add crossfade transitions between pages

For a polished result with 0.5s crossfades between page clips:

```bash
ffmpeg \
  -i Overview.webm -i Sales.webm -i Inventory.webm -i Performance.webm \
  -filter_complex "\
    [0:v]setpts=PTS-STARTPTS[v0]; \
    [1:v]setpts=PTS-STARTPTS[v1]; \
    [2:v]setpts=PTS-STARTPTS[v2]; \
    [3:v]setpts=PTS-STARTPTS[v3]; \
    [v0][v1]xfade=transition=fade:duration=0.5:offset=4[x01]; \
    [x01][v2]xfade=transition=fade:duration=0.5:offset=8[x02]; \
    [x02][v3]xfade=transition=fade:duration=0.5:offset=12[out]" \
  -map "[out]" -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p demo.mp4
```

Adjust `offset` values based on each clip's duration. The offset is the timestamp (in seconds) where the crossfade begins.

### Trim to exact duration

```bash
ffmpeg -i demo.mp4 -t 30 -c copy demo_30s.mp4
```

### Add intro/outro title cards

Create a 2-second title card from a PNG:

```bash
# Generate title card video from image
ffmpeg -loop 1 -i title.png -c:v libx264 -t 2 -pix_fmt yuv420p -vf "scale=1440:900" title.mp4

# Prepend to walkthrough
ffmpeg -f concat -safe 0 -i <(echo -e "file 'title.mp4'\nfile 'walkthrough.mp4'") -c copy final.mp4
```

### Generate animated GIF (for Slack/docs)

```bash
ffmpeg -i walkthrough.mp4 -vf "fps=12,scale=720:-1:flags=lanczos" -loop 0 demo.gif
```

---

## Timing Recommendations

| Page content | `holdPageMs` | `scrollDistance` | `loadWaitMs` |
|-------------|-------------|-----------------|-------------|
| KPI row + chart (typical) | 3000 | 400 | 8000 |
| Dense dashboard (many cards) | 4000 | 800 | 10000 |
| Single chart (pro-code) | 2500 | 200 | 8000 |
| Data table | 3000 | 600 | 6000 |
| First page (cold load) | 3000 | 600 | 10000 |

### Total video duration estimates

| Pages | Per-page hold | Scroll time | Transitions | Total |
|-------|-------------|-------------|-------------|-------|
| 4 | ~5s each | ~3s each | ~2s each | ~38s |
| 4 (trimmed) | ~4s each | ~2s each | ~1s each | ~28s |
| 6 | ~4s each | ~2s each | ~1s each | ~42s |

Target **25-35 seconds** for a polished demo. Under 20s feels rushed; over 45s loses attention.

---

## Integration with Build Pipeline

After `build_app.py` completes (Steps 1-8 from app-build-process-summary), add a capture step:

```python
import subprocess, json

# Step 9: Capture demo
page_ids = {
    "Overview": str(overview_page_id),
    "Sales": str(sales_page_id),
    "Inventory": str(inventory_page_id),
    "Performance": str(performance_page_id),
}

# Screenshots (always — for eval and deck slides)
subprocess.run([
    "node", "screenshot.js", "app", str(app_id),
    json.dumps(page_ids), f"./{app_name}/screenshots"
], check=True)

# Animated walkthrough video
subprocess.run([
    "node", "demo-walkthrough.js", str(app_id),
    json.dumps(page_ids), f"./{app_name}/demo"
], check=True)

# Post-process to MP4
subprocess.run([
    "ffmpeg", "-i", f"./{app_name}/demo/walkthrough_raw.webm",
    "-c:v", "libx264", "-preset", "slow", "-crf", "18",
    "-pix_fmt", "yuv420p", "-movflags", "+faststart",
    f"./{app_name}/demo/walkthrough.mp4"
], check=True)
```

---

## Comparison with demo-ready-build

| Aspect | app-studio-demo-capture (this skill) | demo-ready-build |
|--------|--------------------------------------|------------------|
| Captures | Real deployed App Studio app in browser | React components in Remotion |
| Data | Live Domo data | Synthetic TypeScript arrays |
| Chrome | Full App Studio (nav, layout, cards, theme) | Component only (no nav/layout) |
| Auth | Domo session ID required | No auth needed |
| Tooling | Playwright + ffmpeg | Remotion + @remotion/cli |
| Code changes | None — captures any deployed app | Requires Remotion-safe styling constraints |
| Cursor animation | Not included (real browser cursor) | AnimatedCursor component |
| Best for | App Studio apps, eval screenshots, stakeholder demos | Standalone custom apps, product marketing |

**Use both together**: `demo-ready-build` for the component-level hero shots with animated cursor, `app-studio-demo-capture` for the full-chrome production walkthrough. Stitch both into a final video with ffmpeg.

---

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| Pro-code cards show blank/white | iframes haven't loaded yet | Increase `loadWaitMs` to 10000-12000 |
| Charts missing data | Data query still in flight | Increase `loadWaitMs`; add `page.waitForSelector('.recharts-wrapper')` |
| Left-nav collapsed/hidden | Viewport too narrow | Ensure viewport width >= 1280 |
| Auth redirect to login page | Expired SID | Re-run `domo login`; re-obtain SID |
| Video is choppy/laggy | Headless rendering under load | Use `--disable-gpu` flag; reduce `scrollStepPx` to 1 |
| WebM won't play | Player doesn't support VP8 | Convert to MP4 with ffmpeg |
| Screenshots too large | `deviceScaleFactor: 2` + `fullPage: true` | Use `deviceScaleFactor: 1` for video; keep 2x for screenshots |

---

## Output Checklist

After running the pipeline, verify:

- [ ] Screenshots exist for every page (no `_error.png` files)
- [ ] Pro-code banners and charts are visible (not blank)
- [ ] Theme is applied (correct colors, fonts, nav styling)
- [ ] Video is smooth (no frame drops or loading spinners captured)
- [ ] Video duration is 25-35s
- [ ] MP4 plays in QuickTime/VLC (H.264 baseline profile)
- [ ] Left-nav is visible and shows correct page names/icons
- [ ] Data is populated (charts have lines/bars, KPIs have values)
