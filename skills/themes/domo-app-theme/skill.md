# Domo Custom App Theme

A clean, professional dashboard theme used across Domo custom apps. Designed to feel native to the Domo platform while being modern and readable. Corporate but not sterile — hierarchy comes from font weight and subtle shadows rather than color. Feels Domo-native / Salesforce-adjacent.

Author: David Johnson

## CSS Custom Properties

```css
:root {
  /* Typography */
  --font-stack: "Open Sans", "Helvetica Neue", Arial, Helvetica, sans-serif;

  /* Core Colors */
  --text-primary: #3F454D;
  --text-secondary: #68737F;
  --bg: #F1F6FA;
  --surface: #FFFFFF;
  --border: #B7C1CB;
  --border-light: #DCE4EA;
  --hover-bg: #DCE4EA;
  --subtle-hover: #F8FAFC;
  --accent-hover: #99CCEE;

  /* Status Colors */
  --on-track: #ADD4C1;
  --on-track-bg: #e8f3ec;
  --on-track-text: #4a7a5a;
  --at-risk: #FF9922;
  --at-risk-bg: #fff0dd;
  --at-risk-text: #c47a10;
  --behind: #776CB0;
  --behind-bg: #eae7f3;
  --behind-text: #5a5094;
  --complete: #99CCEE;
  --complete-bg: #e0f0fa;
  --complete-text: #5a9abe;

  /* Summary Card Values */
  --on-track-value: #6a9f7a;
  --at-risk-value: #FF9922;
  --behind-value: #776CB0;
  --complete-value: #99CCEE;
  --total-value: #3F454D;

  /* Accent / Highlight */
  --alert: #e45f5f;
  --avatar-bg: #3F454D;
  --avatar-text: #FFFFFF;

  /* Shadows */
  --shadow: 0 1px 3px rgba(63, 69, 77, 0.08);
  --shadow-hover: 0 4px 12px rgba(63, 69, 77, 0.14);

  /* Border Radius */
  --radius-card: 10px;
  --radius-btn: 6px;
  --radius-badge: 4px;
  --radius-bar: 4px;

  /* Spacing */
  --page-padding: 24px;
  --max-width: 1400px;
  --grid-gap: 16px;
  --card-padding: 20px;
}
```

## Reset

```css
* { box-sizing: border-box; margin: 0; padding: 0; }
```

## Typography


| Role                         | Size | Weight | Extra                           |
| ---------------------------- | ---- | ------ | ------------------------------- |
| Page title                   | 22px | 700    |                                 |
| Card / section titles        | 16px | 600    |                                 |
| Body text / descriptions     | 13px | 400    | line-height 1.4                 |
| Labels / captions            | 12px | 600    | uppercase, letter-spacing 0.5px |
| Small text (badges, charts)  | 11px | 600    |                                 |
| Micro text (avatar initials) | 9px  | 700    | letter-spacing 0.5px            |


- **Font stack**: `"Open Sans", "Helvetica Neue", Arial, Helvetica, sans-serif`
- Semibold (600) is used extensively for labels, table headers, filters, and buttons

## Color Palette

### Core Colors


| Role             | Hex       | Usage                                              |
| ---------------- | --------- | -------------------------------------------------- |
| Text primary     | `#3F454D` | Headings, card titles, meta labels, active buttons |
| Text secondary   | `#68737F` | Descriptions, captions, filter labels              |
| Background       | `#F1F6FA` | Page background                                    |
| Surface          | `#FFFFFF` | Cards, containers, inputs                          |
| Border           | `#B7C1CB` | Input borders, button borders                      |
| Border light     | `#DCE4EA` | Dividers, progress bar tracks, row borders         |
| Hover background | `#DCE4EA` | Button/row hover                                   |
| Subtle hover bg  | `#F8FAFC` | Table/list row hover                               |
| Accent hover     | `#99CCEE` | Border highlight on hover (inputs, buttons)        |


### Status Colors


| Status   | Primary   | Background | Text      | Usage                 |
| -------- | --------- | ---------- | --------- | --------------------- |
| On Track | `#ADD4C1` | `#e8f3ec`  | `#4a7a5a` | Bars, borders, badges |
| At Risk  | `#FF9922` | `#fff0dd`  | `#c47a10` | Bars, borders, badges |
| Behind   | `#776CB0` | `#eae7f3`  | `#5a5094` | Bars, borders, badges |
| Complete | `#99CCEE` | `#e0f0fa`  | `#5a9abe` | Bars, borders, badges |


### Summary Card Values


| Category | Color     |
| -------- | --------- |
| On Track | `#6a9f7a` |
| At Risk  | `#FF9922` |
| Behind   | `#776CB0` |
| Complete | `#99CCEE` |
| Total    | `#3F454D` |


### Accent / Highlight


| Role        | Hex       | Usage                          |
| ----------- | --------- | ------------------------------ |
| Alert/today | `#e45f5f` | Today marker line, alert color |
| Avatar bg   | `#3F454D` | Initials fallback avatar       |
| Avatar text | `#FFFFFF` | Initials text                  |


## Spacing & Layout

- **Page padding**: 24px
- **Max width**: 1400px, centered
- **Grid gap**: 16px
- **Card grid**: `repeat(auto-fill, minmax(320px, 1fr))`
- **Section gap**: 16px–24px vertical between sections
- **Card padding**: 20px
- **Input/button padding**: 6px 12px (inputs), 6px 14px (filter buttons), 8px 20px (tab buttons)

## Shadows

- **Rest**: `0 1px 3px rgba(63, 69, 77, 0.08)`
- **Hover**: `0 4px 12px rgba(63, 69, 77, 0.14)`

Shadow color uses the primary text color `#3F454D` (rgb 63, 69, 77) at low opacity to stay cohesive. Opacity is kept very low (0.08–0.14) for a subtle, flat-but-lifted feel.

## Components

### Buttons (Filter / Tab)


| State   | Background | Border    | Text      |
| ------- | ---------- | --------- | --------- |
| Default | `#FFFFFF`  | `#B7C1CB` | `#68737F` |
| Hover   | `#DCE4EA`  | `#99CCEE` | `#3F454D` |
| Active  | `#3F454D`  | `#3F454D` | `#FFFFFF` |


- Ghost/outline style throughout — no fills on default buttons
- Border radius: 6px
- Transition: `all 0.15s ease`

### Cards

- White background, 10px radius, subtle shadow
- 4px left border colored by status
- Hover lifts shadow
- Padding: 20px

### Status Badges

- 11px uppercase text, weight 600, letter-spacing 0.5px
- Padding: 3px 8px, 4px radius
- Tinted background with darker matching text (see status colors table)

### Progress Bars

- Track: `#DCE4EA`, 8px height, 4px radius
- Fill: status-colored, `width` transition 0.3s ease

### Owner Avatars

- **Default size**: 22px circle (cards), 18px circle (compact/gantt contexts)
- Image: `border-radius: 50%`, `object-fit: cover`
- Fallback: `#3F454D` circle with white initials (9px default, 8px compact)
- Always `flex-shrink: 0` to prevent squishing
- Paired with name in a flex row with 6px gap

### Select Inputs

- White bg, `#B7C1CB` border, 6px radius
- 13px text, weight 600, `#3F454D` text color
- Hover: `#99CCEE` border

### Summary Cards

- White bg, 10px radius, subtle shadow
- `flex: 1`, min-width 140px
- Label: 12px uppercase secondary text
- Value: 28px weight 700, color per status (see summary card values table)

### Gantt Chart

- Container: white bg, 10px radius, subtle shadow
- Row height: 40px min
- Row dividers: 1px solid `#F1F6FA`
- Row hover: `#F8FAFC`
- Header divider: 2px solid `#DCE4EA`
- Bars: 24px height, 4px radius, status-colored with darker fill layer for progress
- Today line: 2px `#e45f5f` dashed, with 10px label above

## Transitions


| Element           | Transition                          |
| ----------------- | ----------------------------------- |
| Buttons/controls  | `all 0.15s ease`                    |
| Progress bars     | `width 0.3s ease`                   |
| Card hover shadow | `box-shadow 0.15s ease`             |
| Gantt bars        | `opacity 0.15s ease` (hover → 0.85) |


## Design Principles

- All colors are derived from a cool-gray palette anchored on `#3F454D`
- Status colors are intentionally muted/pastel for bars and borders, with saturated variants only in small text badges
- The theme avoids pure black (`#000`) and pure white borders — everything has a slight blue-gray tint
- No bold primary color — soft blue (`#99CCEE`) is used sparingly for accents
- Hierarchy comes from font weight and subtle shadows rather than color

