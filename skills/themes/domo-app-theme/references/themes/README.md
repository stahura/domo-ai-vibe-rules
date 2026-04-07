# DESIGN.md Theme System

## Overview

This directory contains pre-built `DESIGN.md` theme specifications for Domo App Studio apps. Each file is a complete, self-contained design document that an AI agent consumes to build a fully-themed App Studio app — including native Domo theme JSON, pro-code CSS variables, chart palettes, and navigation styling.

## Architecture

The system has three layers:

| Layer | Purpose | Artifact |
|-------|---------|----------|
| **1. DESIGN.md** | Single source of truth for a theme's visual identity | `*.DESIGN.md` files in this directory |
| **2. App Studio Theme JSON** | Native Domo schema (`c1`–`c60` color slots, `f1`–`f8` fonts, `ca1`–`ca8` card styles) | Embedded in each DESIGN.md under "Importable Theme JSON" |
| **3. Pro-Code CSS** | Custom properties for iframe-based chart/banner components | Derived from DESIGN.md color system at build time |

All three layers must stay synchronized. The DESIGN.md is the Rosetta Stone that maps between them.

## Theme Catalog

### Production Themes

| Theme | Mode | Accent | Best For |
|-------|------|--------|----------|
| `corporate-light` | Light | Cool blue-gray | Enterprise dashboards, financial reporting |
| `charcoal-ember-dark` | Dark | Warm orange/ember | Executive dashboards, operations monitoring |
| `emerald-dark` | Dark | Green/emerald | Environmental, sustainability, growth metrics |
| `neon-magenta-dark` | Dark | Hot pink/magenta | Healthcare, creative analytics, engagement |
| `cyberpunk` | Dark | Neon cyan | Technology, SaaS, developer tools |
| `solarpunk` | Light | Leaf green | Sustainability, agriculture, community |

### Subgenre Themes

| Theme | Mode | Accent | Feel |
|-------|------|--------|------|
| `steampunk` | Dark | Polished brass/copper | Vintage industrial, mechanical aesthetic |
| `dieselpunk` | Dark | Rust orange | Heavy industry, power, raw materials |
| `atompunk` | Light | Atomic orange | Retro-futurism, mid-century optimism |
| `biopunk` | Dark | Toxic green | Biotech, laboratory, experimental |
| `dreadpunk` | Dark | Deep crimson | Risk management, security, incident response |
| `dungeonpunk` | Dark | Arcane amber/gold | Fantasy-inspired, gamification |

### Palette Overlays

`palette-overlays.md` provides chart color palette swaps for the Corporate Light base theme. Use when the full DESIGN.md aesthetic is right but chart series colors need variety.

## How It Works

1. Agent reads the target `DESIGN.md` theme file
2. Extracts the color system (hex values mapped to `c1`–`c60` slots)
3. Applies the App Studio Theme JSON via `PUT /api/content/v1/dataapps/{appId}`
4. Builds pro-code components (banners, charts) using the same hex values from the DESIGN.md
5. Sets navigation icons from the verified icon catalog (133 names, documented in `app-studio/SKILL.md`)
6. Sets font family across both native theme slots and pro-code CSS

## Key Rules

- **Font family must match everywhere**: Theme `fonts[].family` and all pro-code `font-family` CSS must use the same family (Sans, Serif, or Slab)
- **Pro-code colors are NOT inherited**: iframe-based components must explicitly use the DESIGN.md hex values — they don't inherit the App Studio theme
- **`c60` AUTOMATIC_COLOR breaks dark mode**: On dark themes, replace all `c60` font color references with `c58`
- **`c55`/`c56` must be set explicitly**: Page background color slots are not auto-derived — always set them to the intended page background hex
- **Nav icons**: Only use names from the verified 133-icon catalog. Google Material names render as blank space

## Eval Results

Five live App Studio apps were built to validate the DESIGN.md system:

| Test | Use Case | Theme | Mode | First-Run Quality | Issues Found |
|------|----------|-------|------|-------------------|--------------|
| test-i | Retail | Charcoal Ember Dark | Dark | 3 fix iterations | Icons, page bg, nav order, c60 text |
| test-j | Healthcare | Corporate Light | Light | 2 fix iterations | Banner bg, nav hover colors |
| test-k | SaaS | Cyberpunk | Dark | 1 fix (theme PUT) | Unsupported theme properties |
| test-m | Retail | Warm Copper (custom) | Light | Clean build | Palette swap post-build |
| test-n | Healthcare | Neon Magenta Dark | Dark | Clean build, zero issues | None |

**Trend**: Each successive test produced fewer issues as lessons were codified into skills. Test-n achieved zero-defect first-run output.

## Palette Overlay Strategy

- **For themed requests** (user specifies a mood, aesthetic, or subgenre): Use the matching full `DESIGN.md` theme
- **For generic requests** (user just wants "a dashboard"): Use `corporate-light.DESIGN.md` as the base, optionally applying a chart palette overlay from `palette-overlays.md`
- **For new aesthetics**: Generate a new `DESIGN.md` following the established format — color system with slot mapping, typography, card styles, chart palette, and importable theme JSON
