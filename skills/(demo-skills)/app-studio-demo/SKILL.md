---

## description: Create an App Studio app with pages, theme, heroes, native cards, and layout. Triggers on "app studio", "create app", "dashboard", "add pages".
alwaysApply: false

# Micro-Demo: App Studio App

## Skills

Read and follow in order:

1. `~/.agents/skills/advanced-app-studio/SKILL.md` — 
2. `~/.agents/skills/domo-app-theme/SKILL.md` 

## Demo Pack

Read `demo-packs/{vertical}.md` for page definitions, icons, metrics, theme, and chart types.

## Input Requirements

Needs dataset id's to power cards. Sources:

1. Conversation context may have id's
2. Ask the user for dataset ids

## Procedure

1. **Create app**: 
2. **Create pages**: 
3. **Apply theme**: GET theme → from domo-app-theme/themes
4. **Hero metrics**: 3–4 `badge_pop_multi_value` cards per page in ONE ROW at y=20, height 14, YEAR interval
5. **Native charts**: 1 full-width (width 60) per page + 2–6 detail cards, different chart types per page
6. **Filter cards**: low-profile (height 6, style null, hideBorder, hideTitle, hideMargins, fitToFrame)
7. **Assemble layout** per vertical structure: banner y=0 → filters y=14 → heroes y=20 → header y=34 → primary viz y=38 → header y=68 → detail cards y=72
8. **Navigation**: LEFT orientation, custom icon on EVERY page, HOME first, showTitle false

## Adding Pages Only

If user asks to "add pages" to an existing app:

1. Get appId from context or ask
2. Create views, heroes, native cards, filters for each new page
3. Assemble layout for new pages
4. Update navigation with new page icons

## Output Contract

After completion, tell the user:

- App URL: `https://modocorp.domo.com/app-studio/{appId}`
- appId and all pageIds
- Card count per page

## Mandatory UI/UX Standards 

- All `borderRadius: 0` everywhere (cards, tables, notebooks, components, buttons, tabs, forms, pills)
- All cards: `borderWidth: 0`, `dropShadow: 'NONE'`, `padding: 0`
- Fixed-width layout: `isDynamic: false`, `density: {compact: 8, standard: 8}`
- Controls color c8: `#2563BE`
- Filter cards: height 6, style null, hideTitle true
- Heroes: SINGLE ROW, height 14, never 5+ heroes, never 2 rows
- Never create duplicate apps — reuse existing appId on retry

## CRITICAL: Navigation Icon Names

**Google Material icon names DO NOT WORK in Domo.** Names like `inventory_2`, `assignment_return`, `monetization_on`, `trending_up`, `electric_bolt`, `precision_manufacturing`, `verified_user` will render as BLANK SPACE with no icon visible.

**Use ONLY these Domo-native icon names** (verified from 100+ live apps):


| Page type                | Use these icon names                                                             |
| ------------------------ | -------------------------------------------------------------------------------- |
| Home                     | `home`                                                                           |
| Overview / Dashboard     | `analytics`, `pop-chart`, `chart-bar-vertical`, `select-chart`, `badge-layout-8` |
| Production / Operations  | `gauge`, `dataflow`, `cube-filled`, `completed-submissions`                      |
| Quality / Compliance     | `certified`, `checkbox-marked-outline`, `check-in-icon`, `approval-center`       |
| Supply Chain / Logistics | `globe`, `data-app`, `local_shipping`, `warehouse`, `shopping_cart`              |
| Retail / Store           | `store`, `cube-filled`, `numbers`, `toolbox`                                     |
| Financial                | `money-universal`, `money`, `benchmark`, `books`, `calculator`                   |
| People / HR              | `people`, `person`, `person-card`, `person-plus`                                 |
| Time / Scheduling        | `clock`, `calendar-simple`, `calendar-time`, `alarm`                             |
| AI / Intelligence        | `ai-chat`, `magic`, `wand`, `lightbulb`, `lightning-bolt`                        |
| Settings / Admin         | `controls`, `pages-gear`, `code-tags`, `pencil-box`                              |


**Manufacturing app example**: Home → `home`, Overview → `analytics`, Production → `gauge`, Quality → `certified`, Supply Chain → `globe`