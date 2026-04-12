# Design-Aware Layout Reference

Detailed spacing examples and layout density presets for App Studio pages.

## Executive Layout (4–8 cards)

Generous whitespace, large card sizes, minimal visual noise. For leadership dashboards where each card should be immediately readable at a glance.

```
y=0:   SPACER (height 3)
y=3:   HEADER "Revenue Summary" (height 4)
y=7:   KPI | KPI | KPI (width 20 each, height 10)
y=17:  SPACER (height 5)
y=22:  HEADER "Quarterly Trend" (height 4)
y=26:  Chart (width 60, height 30)
y=56:  SPACER (height 5)
y=61:  HEADER "Regional Breakdown" (height 4)
y=65:  Chart | Chart (width 30 each, height 25)
```

Compact template: all cards at width 12, stacked. KPIs at height 6, charts at height 10.

Key traits:
- 3 KPIs across (width 20), never 4+
- Charts at width 30+ for readability
- Height-5 SPACERs between every section
- No tables — link to a Detailed page instead

## Operational Layout (8–16 cards)

Balanced density for daily monitoring. Filters at top, KPIs below, charts and tables for drill-down.

```
y=0:   SPACER (height 3)
y=3:   Filter | Filter | Filter | Filter | Filter | Filter (width 10 each, height 10)
y=13:  SEPARATOR (height 2)
y=15:  HEADER "Key Metrics" (height 4)
y=19:  KPI | KPI | KPI | KPI (width 15 each, height 10)
y=29:  SPACER (height 3)
y=32:  HEADER "Trends" (height 4)
y=36:  Chart | Chart (width 30 each, height 22)
y=58:  SPACER (height 3)
y=61:  HEADER "Detail" (height 4)
y=65:  Table (width 60, height 25)
```

Compact template: filters at height 6 stacked, KPIs at height 6, charts at height 8, tables at height 10.

Key traits:
- Filter row at the very top, followed by SEPARATOR
- 4 KPIs across (width 15) is the standard density
- Height-3 SPACERs between sections
- One table at full width for drill-down

## Detailed Layout (16+ cards)

High density for analysts. Maximizes information per viewport. Minimal spacing, smaller card sizes, multiple chart rows.

```
y=0:   SPACER (height 2)
y=2:   Filter | Filter | Filter | Filter | Filter | Filter (width 10 each, height 8)
y=10:  SEPARATOR (height 2)
y=12:  KPI | KPI | KPI | KPI | KPI | KPI (width 10 each, height 8)
y=20:  SPACER (height 2)
y=22:  HEADER "Analysis" (height 4)
y=26:  Chart | Chart | Chart (width 20 each, height 20)
y=46:  Chart | Chart (width 30 each, height 20)
y=66:  SPACER (height 2)
y=68:  HEADER "Records" (height 4)
y=72:  Table (width 60, height 25)
y=97:  Table (width 60, height 25)
```

Compact template: all cards at width 12 stacked. KPIs at height 5, charts at height 8, tables at height 10.

Key traits:
- 6 KPIs across (width 10) — maximum density
- Height-2 SPACERs — just enough to separate sections
- Filters use reduced height (8 instead of 10)
- Multiple chart rows and tables are expected

## Row Harmony Examples

Cards on the same row should share the same height to avoid ragged bottom edges.

```
GOOD — uniform heights per row:
y=0:  KPI(15×10) | KPI(15×10) | KPI(15×10) | KPI(15×10)
y=10: Chart(30×22) | Chart(30×22)

BAD — mixed heights on same row:
y=0:  KPI(15×10) | Chart(20×22) | KPI(15×10)
      ↑ ragged bottom: KPI ends at y=10, chart extends to y=22
```

If you must mix card types on the same row, set all cards to the height of the tallest card in that row. A KPI at height 22 will have empty space below the number, but the row reads as a single visual band.

## Visual Weight Hierarchy

The vertical order of content creates implicit hierarchy. Follow this order:

```
1. SPACER (breathing room)
2. Filters / controls (user sets context)
3. SEPARATOR (divides controls from content)
4. KPIs / summary numbers (headline answer)
5. Charts (trends, distributions, comparisons)
6. Tables (raw detail, drill-down)
```

Reversing this order (e.g., table above KPIs) forces the reader to process detail before understanding the summary.

## Spacing Between Sections

| Density | Between-section SPACER height | Before first content |
|---------|-------------------------------|----------------------|
| Executive | 5 | 3 |
| Operational | 3 | 3 |
| Detailed | 2 | 2 |

SPACERs are template-only elements (`type: "SPACER"`) that don't appear in the `content` array. They occupy grid space but render as empty whitespace.
