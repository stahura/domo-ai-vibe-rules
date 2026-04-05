---

## name: pb-apps-initial-build

description: Orchestrates a new Domo custom app build or existing-app takeover from scratch. Loads rules, sequences capability skills, and tracks progress through manifest, data, UI, and publish phases. Use when starting a new Domo app project, taking over an existing app, or normalizing an app to platform best practices.

# Domo App Initial Build Playbook

## When to use

- Use at project kickoff for a brand-new Domo custom app.
- Use when taking over an existing app and normalizing it to platform best practices.

## Progress checklist

Copy this checklist and update it as you work:

```
Build Progress:
- [ ] Phase 0: Rules loaded
- [ ] Phase 1: Manifest & contracts
- [ ] Phase 2: App shell (domo.js)
- [ ] Phase 2b: App Studio integration (if embedded in App Studio)
- [ ] Phase 3: Data access
- [ ] Phase 4: App storage (if needed)
- [ ] Phase 5: Toolkit clients (if needed)
- [ ] Phase 6: Feature skills (AI / Code Engine / Workflow — as needed)
- [ ] Phase 7: Performance review
- [ ] Phase 8: Build & publish
- [ ] Phase 9: Verification
```

## Phase 0 — Load rules (always-on)

Apply before writing any code:

- `rules/core-custom-apps-rule.md`
- `rules/custom-app-gotchas.md`

## Phase 1 — Manifest & contracts

Use `cap-apps-manifest`.

Define all external resource mappings first — datasets, collections, workflows, Code Engine packages. Everything else depends on this.

In addition to creation of the manifest.json, check root folder for an existing thumbnail.png to copy into the public folder of the new app.

**Existing-app takeover?** Audit the current `manifest.json` against actual code usage before changing anything.

## Phase 2 — App shell

Use `cap-apps-domo-js`.

Set up the baseline: `ryuu.js` import, navigation via `domo.navigate()`, event listeners, environment info.

**Advanced users using DA CLI?** Ask the agent to also use `cap-apps-da-cli` for scaffolding and manifest instance workflows.Should not be used unless user explicitly asks agent to use it.

## Phase 2b — App Studio integration (if embedded in App Studio)

Use `app-studio-pro-code`.

**Skip this phase** if the app is a standalone full-page app. Use this phase when the custom app will be placed as a card inside an App Studio page.

### Step 0: Create the App Studio app and pages

Before any cards or pro-code apps, create the container:

1. **Create the app**: `POST /content/v1/dataapps` with `{"title": "...", "description": "..."}` — see `app-studio` skill § "13. Create App". The response gives you `dataAppId` and `landingViewId` (the first page's ID).
2. **Create additional pages**: `POST /content/v1/dataapps/:dataAppId/views` for each subpage — see `app-studio` skill § "2b. Create a New View". Each returns a `viewId` which is also the `pageId` for card/layout operations.
3. **Discover dataset schemas**: Before creating any cards, query each dataset's schema so you know the exact column names and types. Use `GET /api/query/v1/datasources/{dataSourceGuid}/schema/indexed` — returns `tables[0].columns[]` with `name` and `type`. Store the column list for each dataset.

Execute the following sub-steps **in order**:

### Step 1: Custom color palette (FIRST — before any cards or pro-code)

Select a curated palette from `domo-app-theme/color-palettes.md` (50 OKLCH palettes across 9 harmony types). Pick the palette that best suits the use case and data domain. This palette drives everything below — App Studio theme, pro-code charts, and native card series overrides. Use OKLCH values in pro-code CSS; convert to hex for native card `series_N_color` overrides and App Studio theme slots. NEVER use Domo default colors.

### Step 2: Custom app icon

Every App Studio app must have a custom icon (never leave the default placeholder). Generate a 256×256 PNG using the custom palette (see `app-studio` skill § "Custom App Icon") and upload it via the Data File Service (`POST /api/data/v1/data-files`, `Content-Type: image/png`). Then set both `iconDataFileId` and `navIconDataFileId` on the app via the standard full-object PUT.

### Step 3: Page-specific banners

Create one banner pro-code app per page (e.g., `mfg-banner-overview/`, `mfg-banner-production/`). Each banner is a separate Domo custom app with hardcoded page title and subtitle — iframe cards cannot receive params from the host page.

**CRITICAL: Banners must be visually distinct across pages AND across different app builds.** Do NOT reuse the same CSS gradient pattern for all pages. Vary the following:

- **Gradient direction**: Use different angles per page (e.g., `135deg` for Overview, `to right` for Production, `160deg` for Quality, `to bottom right` for Supply Chain)
- **Color stops**: Use different shades from the palette for each page (e.g., darker stops for one page, lighter for another, or different hue combinations within the palette family)
- **Accent elements**: Add subtle CSS decorative elements that differ per page — e.g., a thin accent line at the top, a subtle radial highlight in one corner, or an angled divider. These make each banner feel unique without requiring images.

Each banner includes:
- Brand line (e.g., "MODOCORP MANUFACTURING") in accent color
- Page title (e.g., "Overview") in white, bold
- Subheader describing the page's focus in muted light color

Publish each as a separate design, create one card instance per design, place at y=0, width=60, height=14, style ca8, with `hideTitle`, `hideBorder`, `hideMargins`, `fitToFrame` all true.

### Step 4: Hero metric cards (3-4 per page, SINGLE ROW, NATIVE — never pro-code)

NEVER build pro-code apps for hero/summary metrics. Always use native `badge_pop_multi_value` (Period over Period Multi-Value) cards. They automatically provide big number, percent change, direction indicator, and additional text.

**CRITICAL: Use exactly 3 or 4 heroes per page in a SINGLE ROW. Never 5-6 (too crowded) and never 2 rows.** If you have 3 heroes, each is width 20. If you have 4, each is width 15. All sit at y=14 in the same row.

**Full recipe** (see `app-studio/SKILL.md` § "Hero Metric Card Design" and `card-creation/SKILL.md` § Gotchas for format details):

1. Create via `PUT /content/v3/cards/kpi?pageId=:pageId` with `chartType: "badge_pop_multi_value"`
2. Include **three subscriptions**: `big_number`, `main`, and `time_period`
3. In `main.columns`: add the date column with `mapping: "ITEM"`, `aggregation: "MAX"` as the first column, then the metric VALUE column
4. Add `dateRangeFilter` to the `main` subscription — **ALWAYS use YEAR interval** (not MONTH). MONTH causes blank heroes when current month has no data yet. Use: `dateTimeRange.interval: "YEAR"`, `periods.combined[0]: {interval: "YEAR", type: "OVER", count: 1}`. Without `dateRangeFilter`, PoP comparison shows "0".
5. Set overrides: `gauge_layout: "Center Vertical"`, `comp_val_displayed: "Percent Change"`, `addl_text: "Prior Year"`, `title_text: "<metric name>"`
6. In the layout content entry: set `hideTitle: true`, `hideSummary: true`, `hideDescription: true`, `hideFooter: true`
7. In the layout template: use height **14** (not 10 — height 10 makes metric values hard to read)

If a `dateGrain` field exists on the subscription, remove it before adding `dateRangeFilter.periods` (they conflict: "Cannot save dategrain with periods").

### Step 5: Primary visualization

**DEFAULT BEHAVIOR: Use NATIVE Domo charts** (bar, line, area, donut) for the primary visualization on each page. Pro-code custom apps are ONLY used when the user explicitly requests them (e.g., "pro-code charts", "custom Recharts", "custom D3 visualization"). If the prompt does not mention pro-code or custom apps, use native Domo cards for all visualizations.

Each page gets one full-width (width=60) chart relevant to that page's domain. Place below the HEADER that follows heroes.

#### Step 5a: Native chart primary visualization (DEFAULT)

Create 1 full-width native Domo card (vertical bar, line, area) per page as the primary chart. Use different chart types per page when possible (e.g., bar for one page, line for another) and apply palette colors via `series_N_color` overrides. This is the default behavior and requires no pro-code publishing.

#### Step 5b: Pro-code primary visualization (ONLY when explicitly requested)

Skip this section entirely unless the user's prompt explicitly asks for pro-code, custom charts, Recharts, D3, or custom apps. When requested, use one of the proven patterns from `app-studio-pro-code/SKILL.md`.

**CRITICAL RULE: Every page's chart MUST be visually distinct.** This means:
1. **Different datasets per page** — each chart queries a DIFFERENT dataset (not just a different column from the same dataset). Map datasets to pages based on domain relevance.
2. **Different chart types per page** — do NOT repeat the same chart type (e.g., area chart) on every page. Mix area charts, bar charts, multi-line charts, and combo charts. If you have 4 pages, use at least 3 different Recharts component combinations.
3. **Different visual patterns** — the line/bar shapes must look different. Using the same dataset for all pages produces identical line shapes even with different column names. This is a critical failure.

**Dataset-to-page mapping** — assign each dataset to the page that matches its domain:

| Page | Primary Dataset | Metric Focus | Suggested Chart Type |
|------|----------------|--------------|---------------------|
| Overview | Work Orders | Production volume over time (OrderQuantity, daily) | Multi-line (Actual + Plan) or area chart |
| Production | Work Orders | Cycle time, efficiency, or output by plant/product | Bar chart (by category) or grouped bar |
| Quality | Quality Inspections | Defect rate, inspection pass/fail, scrap rate | Multi-line (defect rate + scrap rate) or combo |
| Supply Chain | Material Consumption | Material cost, quantity used, waste by supplier | Horizontal bar (by supplier/material) or area |

If two pages must share a dataset, they MUST aggregate DIFFERENT columns that produce visually different shapes. Never aggregate the same column twice.

**CRITICAL: Use the React + Recharts + import-map pattern below. Vanilla SVG charts have failed repeatedly in production — they don't load data because `ryuu.js` is never injected. The pattern below is proven to work.**

This is a **static HTML app** (no `npm run build` step needed). Publish directly with `domo publish` from the app directory, just like banners.

**Chart type templates** — pick the best type for each page. All share the same `index.html` and `app.css` below. Only `app.js` changes per chart type.

**Shared `index.html`** (same for ALL chart types):

```html
<!-- index.html — MUST load ryuu.js explicitly -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Primary Chart</title>
  <link rel="stylesheet" href="app.css" />
</head>
<body>
  <div id="app"></div>
  <script src="https://unpkg.com/ryuu.js"></script>
  <script type="importmap">
  {
    "imports": {
      "react": "https://esm.sh/react@18.2.0",
      "react-dom/client": "https://esm.sh/react-dom@18.2.0/client",
      "recharts": "https://esm.sh/recharts@2.12.7?deps=react@18.2.0,react-dom@18.2.0"
    }
  }
  </script>
  <script type="module" src="app.js"></script>
</body>
</html>
```

```css
/* app.css — production-grade chart styling */
*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 100%; height: 100%; overflow: hidden; background: transparent;
  font-family: "Open Sans", "Helvetica Neue", Arial, sans-serif; }
#app { width: 100%; height: 100%; display: flex; flex-direction: column; padding: 20px 24px 16px; }
.chart-container { display: flex; flex-direction: column; flex: 1; min-height: 0; }
.chart-header { margin-bottom: 8px; }
.chart-header h1 { font-size: 15px; font-weight: 600; margin: 0; }
.chart-header p { font-size: 12px; margin: 2px 0 0; }
.chart-wrapper { flex: 1; min-height: 0; }

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}
```

```javascript
/* app.js — Template A: PRODUCTION-GRADE Area/Line time series (ES module)
   Matches quality of proven reference apps (mfg-production-chart, forecast-line-recharts).
   Features: aggregation controls, custom tooltip, today line, loading animation, footer legend,
   filter listener with try/catch. */
import React, { useState, useEffect, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ComposedChart, Area, Line, XAxis, YAxis,
  CartesianGrid, Tooltip, ResponsiveContainer, ReferenceLine
} from 'recharts';

/* ── CUSTOMIZE PER PAGE — palette hex, alias, columns, title ── */
const COLORS = {
  primary:  '#BRAND_500',   /* primary line — replace with palette hex */
  accent:   '#BRAND_300',   /* secondary/area fill */
  grid:     '#D5DAE2',
  text:     '#23272E',
  textSec:  '#64748B',
  today:    '#64748B',
};
const ALIAS    = 'DATASET_ALIAS';
const DATE_COL = 'DATE_COLUMN_NAME';
const VAL_COL  = 'VALUE_COLUMN_NAME';
const TITLE    = 'Chart Title';
const SUBTITLE = 'Subtitle';
const Y_LABEL  = 'Units';

/* ── Data parsing ── */
const parseData = (raw) => {
  if (!raw?.length) return [];
  let headers, rows;
  if (Array.isArray(raw[0])) {
    headers = raw[0].map(h => String(h).toUpperCase().replace(/\./g, '_'));
    rows = raw.slice(1);
  } else {
    headers = Object.keys(raw[0]).map(h => String(h).toUpperCase().replace(/\./g, '_'));
    rows = raw.map(r => Object.keys(r).map(k => r[k]));
  }
  const find = (n) => headers.findIndex(h => h === n.toUpperCase() || h.includes(n.toUpperCase()));
  const di = find(DATE_COL), vi = find(VAL_COL);
  if (di === -1) { console.error('Date col not found. Headers:', headers); return []; }
  return rows.map(r => ({ date: new Date(r[di]), value: parseFloat(r[vi]) || 0 }))
    .filter(d => !isNaN(d.date.getTime()));
};

/* ── Aggregation (D/W/M) ── */
const aggregateData = (data, period) => {
  const grouped = {};
  data.forEach(({ date, value }) => {
    let key;
    switch (period) {
      case 'week': { const s = new Date(date); s.setDate(date.getDate()-date.getDay()); key = s.toISOString().split('T')[0]; break; }
      case 'month': key = `${date.getFullYear()}-${String(date.getMonth()+1).padStart(2,'0')}-01`; break;
      default: key = date.toISOString().split('T')[0];
    }
    if (!grouped[key]) grouped[key] = { date: key, value: 0, count: 0 };
    grouped[key].value += value; grouped[key].count++;
  });
  return Object.values(grouped).map(g => ({ date: g.date, value: g.value }))
    .sort((a,b) => new Date(a.date) - new Date(b.date));
};

const fmtNum = v => v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':String(Math.round(v));
const fmtDate = (s, period) => {
  const d = new Date(s);
  if (period === 'month') return d.toLocaleDateString('en-US',{ month:'short', year:'numeric' });
  return d.toLocaleDateString('en-US',{ month:'short', day:'numeric' });
};
const calcTickInterval = (len) => { if (len<=30) return 0; if (len<=90) return 6; if (len<=180) return 13; return Math.ceil(len/18)-1; };

/* ── Custom tooltip ── */
const ChartTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  const d = new Date(label);
  return React.createElement('div', {
    style: { background:'#fff', border:'1px solid #E5E7EB', borderRadius:0, padding:'8px 12px', fontSize:12 }
  },
    React.createElement('p', { style:{ fontWeight:600, marginBottom:4 } },
      d.toLocaleDateString('en-US',{ weekday:'short', month:'short', day:'numeric', year:'numeric' })),
    payload[0]?.value != null && React.createElement('p', { style:{ color:COLORS.primary, margin:0 } },
      `${VAL_COL}: ${fmtNum(payload[0].value)}`)
  );
};

/* ── Main component ── */
const Chart = () => {
  const [rawData, setRawData] = useState([]);
  const [aggregation, setAggregation] = useState('month');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const now = new Date();
  const today = `${now.getFullYear()}-${String(now.getMonth()+1).padStart(2,'0')}-${String(now.getDate()).padStart(2,'0')}`;

  const fetchAndParse = async () => {
    try { setLoading(true); setRawData(parseData(await domo.get('/data/v1/'+ALIAS))); setError(null); }
    catch (e) { setError(e.message||String(e)); } finally { setLoading(false); }
  };

  useEffect(() => { fetchAndParse(); }, []);
  useEffect(() => {
    try { if (typeof domo !== 'undefined' && domo.onFiltersUpdate) domo.onFiltersUpdate(() => fetchAndParse()); }
    catch (_) {}
  }, []);

  const chartData = useMemo(() => aggregateData(rawData, aggregation), [rawData, aggregation]);
  const todayInRange = chartData.length > 0 && new Date(chartData[0].date) <= new Date(today) && new Date(chartData[chartData.length-1].date) >= new Date(today);

  if (loading) return React.createElement('div', {
    style: { display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height:'100%', gap:12 }
  },
    React.createElement('div', { style:{ display:'grid', gridTemplateColumns:'repeat(3,16px)', gap:4 } },
      ...[0,1,2,3,4,5,6,7,8].map(i => React.createElement('div', { key:i, style:{ width:16, height:16, background:COLORS.grid, animation:'pulse 1.2s ease-in-out infinite', animationDelay:`${(i%3)*0.1}s` } }))
    ), React.createElement('p', { style:{ color:COLORS.textSec, fontSize:13 } }, 'Loading…'));
  if (error) return React.createElement('div', { style:{ display:'flex', alignItems:'center', justifyContent:'center', height:'100%', color:'#B44', fontSize:14 } }, 'Error: '+error);

  const dateRange = chartData.length > 0
    ? `${new Date(chartData[0].date).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})} – ${new Date(chartData[chartData.length-1].date).toLocaleDateString('en-US',{month:'short',day:'numeric',year:'numeric'})}`
    : '';

  return React.createElement('div', { className:'chart-container' },
    React.createElement('div', { className:'chart-header', style:{ display:'flex', justifyContent:'space-between', alignItems:'flex-start' } },
      React.createElement('div', null,
        React.createElement('h1', { style:{ fontSize:15, fontWeight:600, color:COLORS.text, margin:0 } }, TITLE),
        React.createElement('p', { style:{ fontSize:12, color:COLORS.textSec, margin:'2px 0 0' } },
          `${dateRange}, by ${aggregation==='day'?'Day':aggregation==='week'?'Week':'Month'}`)
      ),
      React.createElement('select', {
        value:aggregation, onChange:e=>setAggregation(e.target.value),
        style:{ fontSize:12, padding:'4px 8px', border:`1px solid ${COLORS.grid}`, borderRadius:0, background:'#fff', cursor:'pointer' }
      },
        React.createElement('option',{value:'day'},'Daily'),
        React.createElement('option',{value:'week'},'Weekly'),
        React.createElement('option',{value:'month'},'Monthly'))
    ),
    React.createElement('div', { className:'chart-wrapper', key:`w-${aggregation}` },
      React.createElement(ResponsiveContainer, { width:'100%', height:'100%' },
        React.createElement(ComposedChart, { data:chartData, margin:{ top:10, right:20, left:10, bottom:20 } },
          React.createElement(CartesianGrid, { strokeDasharray:'3 3', stroke:COLORS.grid, vertical:false }),
          React.createElement(XAxis, { dataKey:'date', tickFormatter:d=>fmtDate(d,aggregation), stroke:COLORS.textSec, fontSize:11, tickLine:false, axisLine:{ stroke:COLORS.grid }, interval:aggregation==='day'?calcTickInterval(chartData.length):'preserveStartEnd' }),
          React.createElement(YAxis, { tickFormatter:fmtNum, stroke:COLORS.textSec, fontSize:12, tickLine:false, axisLine:false, label:{ value:Y_LABEL, angle:-90, position:'insideLeft', style:{ textAnchor:'middle', fill:COLORS.textSec, fontSize:12 } } }),
          React.createElement(Tooltip, { content:React.createElement(ChartTooltip) }),
          todayInRange && React.createElement(ReferenceLine, { x:today, stroke:COLORS.today, strokeDasharray:'4 4', label:{ value:'Today', position:'top', fill:COLORS.today, fontSize:11 } }),
          React.createElement(Area, { type:'monotone', dataKey:'value', stroke:'none', fill:COLORS.primary, fillOpacity:0.12 }),
          React.createElement(Line, { type:'monotone', dataKey:'value', stroke:COLORS.primary, strokeWidth:2.5, dot:false, activeDot:{ r:4 } })
        )
      )
    ),
    React.createElement('div', { style:{ display:'flex', gap:16, paddingTop:8, fontSize:12, color:COLORS.textSec } },
      React.createElement('div', { style:{ display:'flex', alignItems:'center', gap:6 } },
        React.createElement('span', { style:{ display:'inline-block', width:16, height:2, background:COLORS.primary } }),
        React.createElement('span', null, VAL_COL))
    )
  );
};
createRoot(document.getElementById('app')).render(React.createElement(Chart));
```

The above is **Template A: Area/Line time series** — use for Overview or any page needing a trend line. Features aggregation controls, custom tooltip, today reference line, loading animation, and footer legend.

**Template B: Bar chart (categorical)** — use for Production (by plant, by product, by status) or Supply Chain (by supplier). Replace the `Chart` component in `app.js`:

```javascript
/* app.js — Template B: Bar chart (ES module) */
import React, { useState, useEffect, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';

const COLORS = { bar: 'BRAND_500', grid: 'NEUTRAL_200', textSec: 'NEUTRAL_500' };
const ALIAS = 'DATASET_ALIAS', CAT_COL = 'CATEGORY_COLUMN', VAL_COL = 'VALUE_COLUMN';
const TITLE = 'Bar Chart Title', SUBTITLE = 'description';

const parseData = (raw) => {
  if (!raw?.length) return [];
  let headers, rows;
  if (Array.isArray(raw[0])) { headers = raw[0].map(h => String(h).toUpperCase()); rows = raw.slice(1); }
  else { headers = Object.keys(raw[0]).map(h => h.toUpperCase()); rows = raw.map(r => Object.values(r)); }
  const find = (n) => headers.findIndex(h => h === n.toUpperCase() || h.includes(n.toUpperCase()));
  const ci = find(CAT_COL), vi = find(VAL_COL);
  if (ci === -1) return [];
  const acc = {};
  rows.forEach(r => { const k = String(r[ci]); acc[k] = (acc[k] || 0) + (parseFloat(r[vi]) || 0); });
  return Object.entries(acc).sort((a, b) => b[1] - a[1]).slice(0, 15).map(([k, v]) => ({ name: k, value: v }));
};
const fmtNum = v => v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':String(Math.round(v));

const Chart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const fetchAndParse = async () => {
    try { setLoading(true); setData(parseData(await domo.get('/data/v1/'+ALIAS))); setError(null); }
    catch(e){ setError(e.message||String(e)); } finally { setLoading(false); }
  };
  useEffect(() => { fetchAndParse(); }, []);
  useEffect(() => {
    try { if (typeof domo !== 'undefined' && domo.onFiltersUpdate) domo.onFiltersUpdate(() => fetchAndParse()); }
    catch (_) {}
  }, []);

  if (loading) return React.createElement('div', {
    style: { display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height:'100%', gap:12 }
  }, React.createElement('div', { style:{ display:'grid', gridTemplateColumns:'repeat(3,16px)', gap:4 } },
    ...[0,1,2,3,4,5,6,7,8].map(i => React.createElement('div', { key:i, style:{ width:16, height:16, background:'#D5DAE2', animation:'pulse 1.2s ease-in-out infinite', animationDelay:`${(i%3)*0.1}s` } }))
  ), React.createElement('p', { style:{ color:COLORS.textSec, fontSize:13 } }, 'Loading…'));
  if (error) return React.createElement('div', { style:{ display:'flex', alignItems:'center', justifyContent:'center', height:'100%', color:'#B44', fontSize:14 } }, 'Error: '+error);
  return React.createElement('div', {className:'chart-container'},
    React.createElement('div', {className:'chart-header'},
      React.createElement('h1', { style:{ fontSize:15, fontWeight:600, margin:0 } }, TITLE),
      React.createElement('p', { style:{ fontSize:12, color:COLORS.textSec, margin:'2px 0 0' } }, SUBTITLE)),
    React.createElement('div', {className:'chart-wrapper'},
      React.createElement(ResponsiveContainer, {width:'100%', height:'100%'},
        React.createElement(BarChart, {data, layout:'vertical', margin:{top:5,right:30,left:80,bottom:5}},
          React.createElement(CartesianGrid, {strokeDasharray:'3 3', stroke:COLORS.grid, horizontal:false}),
          React.createElement(XAxis, {type:'number', tickFormatter:fmtNum, stroke:COLORS.textSec, fontSize:11}),
          React.createElement(YAxis, {type:'category', dataKey:'name', stroke:COLORS.textSec, fontSize:11, width:75}),
          React.createElement(Tooltip, {formatter:v=>fmtNum(v)}),
          React.createElement(Bar, {dataKey:'value', fill:COLORS.bar, radius:[0,0,0,0]})))));
};
createRoot(document.getElementById('app')).render(React.createElement(Chart));
```

**Template C: Multi-line time series** — use for Quality (defect rate + scrap rate) or Overview (actual + plan). Shows 2-3 lines on one chart:

```javascript
/* app.js — Template C: Multi-line (ES module) */
import React, { useState, useEffect, useMemo } from 'react';
import { createRoot } from 'react-dom/client';
import {
  ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';

const COLORS = { line1: 'BRAND_500', line2: 'BRAND_300', line3: 'ACCENT_500', grid: 'NEUTRAL_200', textSec: 'NEUTRAL_500' };
const ALIAS = 'DATASET_ALIAS', DATE_COL = 'DATE_COLUMN';
const SERIES = [
  { col: 'METRIC_1_COL', name: 'Metric 1', color: 'line1' },
  { col: 'METRIC_2_COL', name: 'Metric 2', color: 'line2' },
];
const TITLE = 'Multi-Line Title', SUBTITLE = 'description';

const parseData = (raw) => {
  if (!raw?.length) return [];
  let headers, rows;
  if (Array.isArray(raw[0])) { headers = raw[0].map(h => String(h).toUpperCase()); rows = raw.slice(1); }
  else { headers = Object.keys(raw[0]).map(h => h.toUpperCase()); rows = raw.map(r => Object.values(r)); }
  const find = (n) => headers.findIndex(h => h === n.toUpperCase() || h.includes(n.toUpperCase()));
  const di = find(DATE_COL);
  if (di === -1) return [];
  const acc = {};
  rows.forEach(r => {
    const d = new Date(r[di]);
    if (isNaN(d.getTime())) return;
    const k = d.getFullYear()+'-'+String(d.getMonth()+1).padStart(2,'0');
    if (!acc[k]) acc[k] = { date: k };
    SERIES.forEach(s => {
      const si = find(s.col);
      if (si !== -1) acc[k][s.name] = (acc[k][s.name] || 0) + (parseFloat(r[si]) || 0);
    });
  });
  return Object.values(acc).sort((a, b) => a.date.localeCompare(b.date));
};
const fmtNum = v => v>=1e6?(v/1e6).toFixed(1)+'M':v>=1e3?(v/1e3).toFixed(0)+'K':String(Math.round(v));
const fmtDate = d => { const [y,m]=d.split('-'); return ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'][+m-1]+" '"+y.slice(2); };

const Chart = () => {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const fetchAndParse = async () => {
    try { setLoading(true); setData(parseData(await domo.get('/data/v1/'+ALIAS))); setError(null); }
    catch(e){ setError(e.message||String(e)); } finally { setLoading(false); }
  };
  useEffect(() => { fetchAndParse(); }, []);
  useEffect(() => {
    try { if (typeof domo !== 'undefined' && domo.onFiltersUpdate) domo.onFiltersUpdate(() => fetchAndParse()); }
    catch (_) {}
  }, []);

  if (loading) return React.createElement('div', {
    style: { display:'flex', flexDirection:'column', alignItems:'center', justifyContent:'center', height:'100%', gap:12 }
  }, React.createElement('div', { style:{ display:'grid', gridTemplateColumns:'repeat(3,16px)', gap:4 } },
    ...[0,1,2,3,4,5,6,7,8].map(i => React.createElement('div', { key:i, style:{ width:16, height:16, background:'#D5DAE2', animation:'pulse 1.2s ease-in-out infinite', animationDelay:`${(i%3)*0.1}s` } }))
  ), React.createElement('p', { style:{ color:COLORS.textSec, fontSize:13 } }, 'Loading…'));
  if (error) return React.createElement('div', { style:{ display:'flex', alignItems:'center', justifyContent:'center', height:'100%', color:'#B44', fontSize:14 } }, 'Error: '+error);
  return React.createElement('div', {className:'chart-container'},
    React.createElement('div', {className:'chart-header'},
      React.createElement('h1', { style:{ fontSize:15, fontWeight:600, margin:0 } }, TITLE),
      React.createElement('p', { style:{ fontSize:12, color:COLORS.textSec, margin:'2px 0 0' } }, SUBTITLE)),
    React.createElement('div', {className:'chart-wrapper'},
      React.createElement(ResponsiveContainer, {width:'100%', height:'100%'},
        React.createElement(ComposedChart, {data, margin:{top:10,right:20,left:10,bottom:20}},
          React.createElement(CartesianGrid, {strokeDasharray:'3 3', stroke:COLORS.grid, vertical:false}),
          React.createElement(XAxis, {dataKey:'date', tickFormatter:fmtDate, stroke:COLORS.textSec, fontSize:11}),
          React.createElement(YAxis, {tickFormatter:fmtNum, stroke:COLORS.textSec, fontSize:12, axisLine:false}),
          React.createElement(Tooltip, {formatter:v=>fmtNum(v), labelFormatter:fmtDate}),
          ...SERIES.map(s => React.createElement(Line, {key:s.name, type:'monotone', dataKey:s.name, stroke:COLORS[s.color], strokeWidth:2, dot:false, activeDot:{ r:4, fill:COLORS[s.color] }}))))),
    React.createElement('div', { style:{ display:'flex', gap:16, paddingTop:8, fontSize:12, color:COLORS.textSec } },
      ...SERIES.map(s => React.createElement('div', { key:s.name, style:{ display:'flex', alignItems:'center', gap:6 } },
        React.createElement('span', { style:{ display:'inline-block', width:16, height:2, background:COLORS[s.color] } }),
        React.createElement('span', null, s.name))))
  );
};
createRoot(document.getElementById('app')).render(React.createElement(Chart));
```

**Chart type selection per page (MANDATORY — do NOT use the same type on every page):**

| Page | Use Template | Why |
|------|-------------|-----|
| Overview | A (area) or C (multi-line if Plan data exists) | Time-series trend fits overview narrative |
| Production | B (bar chart by Plant/Product/Status) | Categorical comparison fits production domain |
| Quality | C (multi-line: defect rate + scrap rate over time) | Dual metrics show quality trends |
| Supply Chain | B (horizontal bar by Supplier/Material) | Categorical spend breakdown fits supply chain |

**Per-page customization**: Create a separate app directory per page (e.g., `chart-overview/`, `chart-production/`). Each page's `app.js` should use a DIFFERENT template (A, B, or C) and point to the DATASET and COLUMNS relevant to that page's domain. Using the same template type on all pages is a critical failure.

**CRITICAL: Each chart app needs its OWN manifest.json with the CORRECT dataset.** Do NOT copy the same manifest to all chart directories. The manifest's `datasetsMapping[].dataSetId` MUST match the dataset that page's chart queries, and the `alias` MUST match the `ALIAS` constant in that chart's `app.js`. Example:

```
chart-overview/manifest.json  → dataSetId: Work Orders GUID,  alias: "wo"
chart-overview/app.js         → const ALIAS = 'wo';

chart-production/manifest.json → dataSetId: Work Orders GUID,  alias: "wo"
chart-production/app.js        → const ALIAS = 'wo';

chart-quality/manifest.json   → dataSetId: Quality GUID,       alias: "qi"
chart-quality/app.js           → const ALIAS = 'qi';

chart-supply/manifest.json    → dataSetId: Material GUID,      alias: "mc"
chart-supply/app.js            → const ALIAS = 'mc';
```

If ANY manifest has the wrong dataset or alias, `domo.get()` will silently fail and the chart renders blank. This is the #1 cause of blank charts.

**CRITICAL: `onFiltersUpdated` must be wrapped in try-catch.** If you add a `domo.onFiltersUpdated()` or `domo.onFiltersUpdate()` listener, ALWAYS wrap the call in `try { ... } catch (_) {}`. The ryuu.js internal `listeners` property may not be initialized in all contexts, causing a crash that unmounts the entire React component and leaves the chart blank. This is the #2 cause of blank charts.

**CRITICAL manifest and publish requirements:**

1. **Include a `thumbnail.png`** (at least 300×300) in every pro-code app directory before running `domo publish`. Without it, Domo returns DA0087 and card instances cannot be created. Generate one programmatically (e.g., solid color square using Pillow or a static PNG).
2. **Use empty `fields: []`** in the manifest — do NOT restrict fields, which causes column-name mismatches:
   ```json
   "datasetsMapping": [{"dataSetId": "GUID", "alias": "wo", "fields": []}]
   ```
3. **Alias consistency**: The alias must match exactly between manifest `datasetsMapping[].alias`, the context `mapping[].alias` in `POST https://{instance}.domo.com/domoapps/apps/v2/contexts` (NOT `/api/domoapps/...`), and `domo.get('/data/v1/{alias}')`. The context/card endpoints use the **root domain**, not the `/api/` prefix.
4. **No build step**: This is a static HTML app. Run `domo publish` directly from the app directory (same as banners).

### Step 6: Supporting native cards

Add 2-6 additional native Domo cards per page (bar charts, line charts, donut charts, tables) for detail sections. Apply custom series colors via `series_N_color` overrides on each card.

**CRITICAL: Use HEADER content items** to separate card groups into named sections (e.g., "Production Output", "Quality & Waste", "Operations Overview"). Every group of related cards MUST be preceded by a HEADER. Pages without section headers look flat and unorganized.

### Step 7: Layout assembly

Arrange ALL content on the canvas using the `app-studio` skill layout API. **Every card, banner, and header MUST be moved from the appendix to the canvas** — cards left in the appendix are invisible to users.

Follow the vertical structure:
```
y=0:   BANNER — width 60, height 14
y=14:  FILTER CARDS — 2-3 dropdown selectors, width 20 each, height 6 (low-profile, see below)
y=20:  HERO METRICS — 3-4 cards in ONE ROW, width 20 (3 cards) or 15 (4 cards), height 14
y=34:  HEADER — section title (e.g., "Production Output"), height 4
y=38:  PRIMARY VIZ — width 60, height 30 (native chart by default, pro-code only if requested)
y=68:  HEADER — section title (e.g., "Quality & Waste"), height 4
y=72:  DETAIL CARDS — 2-3 per row, width 20 or 30, height 22
```

**Filter cards MUST be extremely low-profile.** They are controls, not content:
- `hideBorder: true`, `hideMargins: true`, `fitToFrame: true`, `hideSummary: true`
- `style: null` — NO colored style. No `ca3`, no green, no blue. Transparent background only.
- Height **6** — minimal. They should blend into the page, not compete with heroes or charts.
- See `app-studio` skill § "Filter Card Content Entry" for the full property list.

**CRITICAL: Heroes occupy a SINGLE ROW at y=20 (below filters). Never use 2 rows of heroes.** If the page needs more than 4 key metrics, put the extras in the detail section below the primary viz.
Ensure all unused content items are placed in the appendix (`virtualAppendix: true`).

### Step 7b: Navigation setup

After layout assembly, configure the left-hand navigation:
1. **GET** the navigation via `GET /content/v1/dataapps/:dataAppId/navigation` — this returns the full array including system items (HOME, AI_ASSISTANT, CONTROLS, DISTRIBUTE, MORE)
2. **Preserve ALL system nav items** — never drop them. Missing system items makes the app uneditable from the UI.
3. **Add HOME if missing**: New apps may not include a HOME nav item. Add: `{"entity": "HOME", "title": "Home", "icon": {"value": "home", "size": "DEFAULT"}, "visible": true}`.
4. **Set custom icons on EVERY VIEW item** — ALL pages must have an icon. Use `icon: {"value": "icon_name", "size": "DEFAULT"}`. Proven icon names: `dashboard`, `store`, `inventory_2`, `assignment_return`, `local_shipping`, `shopping_cart`, `warehouse`, `account_balance`, `monetization_on`, `trending_up`, `school`, `real_estate_agent`, `electric_bolt`.
5. **Fix "App Page 1" labels**: New views are created with title "App Page 1" in the navigations array. Change to "Overview" (or appropriate name) in the nav item's `title` field.
6. **PUT via the reorder endpoint**: `PUT /content/v1/dataapps/:dataAppId/navigation/reorder` with the full modified array. **Do NOT try to update navigation via the app PUT** — changes to `navigations[]` in the app PUT body are silently ignored.
7. Set `navOrientation: "LEFT"`, `showTitle: false`, `showLogo: false`, `showDomoNavigation: false` on the app via PUT

### Step 8: Event listeners (pro-code apps)

Wire up event listeners so pro-code apps react to the surrounding App Studio environment:

- **Page filters**: Register `domo.onFiltersUpdated` at the top level. Filter objects use `operand` (not `operator`) with values like `BETWEEN`, `IN`, `GREATER_THAN_EQUAL`. Map column names to internal state, then refetch data immediately.
- **Variables**: Register `domo.onVariablesUpdated` at the top level. Variables arrive keyed by numeric function ID strings (e.g., `"858"`) with values at `parsedExpression.value`. Use a pending/commit pattern — stage changes, commit on Apply, then refetch.
- **Variable write-back**: Use `domo.requestVariablesUpdate([{ functionId, value }], onAck, onReply)` for dependent dropdowns. Guard with an `isUpdatingVariable` flag to prevent infinite loops.
- **Theme alignment**: Set body background to `transparent` to blend with the App Studio canvas. All chart series, text, and UI colors must use hex values from the custom palette.

See `app-studio-pro-code` for the full filter/variable integration reference, including production-tested code patterns.

## Phase 3 — Data access (if domo datasets need to be queried)

Use `cap-apps-dataset-query` (primary) and `cap-apps-data-api` (routing overview).

Build queries with `@domoinc/query`. Use the Query API for all dataset reads — it respects page filters and does server-side aggregation.

**Need raw SQL?** Use `cap-apps-sql-query`, but know that SQL ignores page filters.

**Explicit filter handling for non-Query data access**: If the app uses Code Engine calls, stored procedures, or raw SQL instead of `@domoinc/query`, page filters will NOT be applied automatically. You must register `domo.onFiltersUpdated` (see Phase 2b) and pass filter values as parameters to your data source manually.

## Phase 4 — App storage (if appdb , or any user data entry is needed)

Use `cap-apps-appdb`.

Skip if the app only reads datasets. Use AppDB when you need to persist app-specific state, user preferences, or document-style data.

## Phase 5 — Toolkit clients (if appdb, domo workflows, or domo sql query is needed)

Use `cap-apps-toolkit`.

Move to typed `@domoinc/toolkit` clients where they add value (structured responses, type safety). Not required for simple apps.

## Phase 6 — Feature skills (as needed)

Only load the skills your app actually requires (3 examples are listed here but you have access to many more skills):


| Feature needed                                 | Skill                       |
| ---------------------------------------------- | --------------------------- |
| AI text generation or text-to-SQL              | `cap-apps-ai-service-layer` |
| Server-side functions (secrets, external APIs) | `cap-apps-code-engine`      |
| Triggering automation workflows                | `cap-apps-workflow`         |


**Decision guide:** If the user hasn't mentioned AI, Code Engine, or Workflows, skip this phase entirely. Don't add complexity the app doesn't need.

## Phase 7 — Performance review

Use `cap-apps-performance`.

Review all queries before finalizing. Check for full-dataset fetches, missing aggregations, and unnecessary columns.

## Phase 8 — Build & publish

Use `cap-apps-publish`.

`npm run build` → `cd dist` → `domo publish`. On first publish, copy the generated `id` back to your source manifest.

## Phase 9 — Verification

After publishing, confirm:

- App loads without console errors in Domo
- All dataset aliases resolve (no 404s on data calls)
- AppDB collections are wired in the card UI (if used)
- Page filters propagate correctly (if app is embedded in a dashboard)
- Navigation uses `domo.navigate()`, not `<a href>`
- Thumbnail has been copied into public folder
- App Studio app has a custom icon set (`iconDataFileId` and `navIconDataFileId` are non-null)

## Global UI/UX Standards (MANDATORY for every build)

These standards MUST be applied to every App Studio app. They are non-negotiable:

### 1. Zero Border-Radius (STRICT)
**All border-radius values MUST be 0.** No rounded corners anywhere — cards, tables, notebooks, components, buttons, tabs, forms, pills, inputs, or filters. Apply via theme update:
```python
for card in theme.get('cards', []):
    card['borderRadius'] = 0
    if 'itemBorderRadius' in card: card['itemBorderRadius'] = 0
for t in theme.get('tables', []): t['borderRadius'] = 0
for n in theme.get('notebooks', []): n['borderRadius'] = 0
for c in theme.get('components', []):
    c['borderRadius'] = 0
    if 'itemBorderRadius' in c: c['itemBorderRadius'] = 0
for b in theme.get('buttons', []): b['borderRadius'] = 0
for t in theme.get('tabs', []): t['borderRadius'] = 0
for f in theme.get('forms', []): f['borderRadius'] = 0
for p in theme.get('pills', []):
    p['borderRadius'] = 0
    if 'radius' in p: p['radius'] = 0
```

### 2. Card Styling Reference
Apply to ALL card styles (ca1–ca8):
```python
for card in theme.get('cards', []):
    card['borderRadius'] = 0
    card['borderWidth'] = 0
    card['dropShadow'] = 'NONE'
    card['dropShadowColor'] = None
    card['padding'] = {'left': 0, 'right': 0, 'top': 0, 'bottom': 0}
    card['contentSpacing'] = None
    card['headerBottomSpacing'] = 0
```

### 3. Controls Color
```python
for c in theme.get('colors', []):
    if c['id'] == 'c8':
        c['value'] = {'value': '#2563BE', 'type': 'RGB_HEX'}
```

### 4. Fixed-Width Layout (MANDATORY)
All apps MUST use fixed-width. Auto-width is never acceptable:
```python
for page in theme.get('pages', []):
    page['isDynamic'] = False
    page['density'] = {'compact': 8, 'standard': 8}
```

### 5. Page Icons
ALL VIEW items in navigation MUST have a custom icon. Verify after setting. See `app-studio` skill § "Navigation Icons" for proven icon names.

### 6. Filter Cards — Low-Profile
Filter cards MUST use: `hideBorder: true`, `style: null`, `hideMargins: true`, `fitToFrame: true`, `hideSummary: true`, `hideTitle: true`, height 6. The dropdown renders its own field label — hiding the card title avoids redundant or coded text. See `app-studio` skill § "Filter Card Content Entry" for the full spec.

## Build-time guardrails

- Client-side only: no SSR/server routes/server components.
- Use Vite `base: './'`.
- Prefer `HashRouter` unless rewrites are intentionally handled.
- Treat `domo.env.`* as convenience only; use verified identity for trust decisions.
- **NEVER create duplicate apps.** If a deploy step fails partway through, fix the issue and retry on the SAME app ID — do NOT create a new app. If retrying is impossible, delete the failed app before creating a replacement. The user should see exactly ONE app per build, not 2-3 partially completed copies.

