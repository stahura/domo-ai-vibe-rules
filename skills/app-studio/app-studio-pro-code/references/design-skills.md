# Design Skills Integration for Pro-Code Apps

When building pro-code custom apps for App Studio, apply these design principles from the `make-interfaces-feel-better` and `color-oklch` skills. Every principle below applies fully because the agent has complete CSS/JS control inside a custom app.

## Base Layer: domo-app-theme

Always load `domo-app-theme` first. It provides the OKLCH color palette, typography scale, shadow system, and component patterns that make the custom app feel Domo-native. All design skills build on top of this base.

## Typography Polish

From `make-interfaces-feel-better` > typography:

- **Font smoothing**: Already in `domo-app-theme` reset (`-webkit-font-smoothing: antialiased` on root).
- **Text wrapping**: Apply `text-wrap: balance` to all headings and card titles (6 lines or fewer). Apply `text-wrap: pretty` to body text and descriptions to prevent orphans.
- **Tabular numbers**: Apply `font-variant-numeric: tabular-nums` to every number that updates dynamically — KPI values, counters, table columns with numbers, timers. Prevents layout shift as digits change.

## Surface Quality

From `make-interfaces-feel-better` > surfaces:

- **Concentric border radius**: When nesting rounded elements, `outerRadius = innerRadius + padding`. The `domo-app-theme` documents this relationship for its card/button/badge radius values. Apply it to any custom nested containers.
- **Optical alignment**: Buttons with text + icon need less padding on the icon side (`icon-side = text-side - 2px`). Play icons need a 2px rightward shift. Asymmetric icons (stars, arrows) should be fixed in the SVG viewBox directly.
- **Shadows over borders**: Use the three-layer `--shadow` / `--shadow-hover` variables from `domo-app-theme` for card containers, buttons, and elevated elements (dropdowns, modals). Keep solid borders for dividers, table cells, and form input outlines.
- **Image outlines**: Apply `outline: 1px solid oklch(0.374 0.014 256 / 0.1); outline-offset: -1px` to images for consistent depth.
- **Hit areas**: Interactive elements need at least 40x40px hit area. Extend with a pseudo-element if the visible element is smaller. Never let hit areas of two elements overlap.

## Animation & Interaction

From `make-interfaces-feel-better` > animations:

- **Interruptible animations**: Use CSS transitions for interactive state changes (hover, toggle, open/close). Reserve CSS keyframes for staged sequences that run once (data loading entrance). Transitions can be interrupted mid-animation; keyframes restart from the beginning.
- **Enter animations**: Don't animate a single container. Split content into semantic chunks (title, description, data rows) and stagger each with ~100ms delay. Combine `opacity`, `translateY(12px)`, and `blur(4px)` for the enter effect.
- **Exit animations**: Use a small fixed `translateY(-12px)` instead of full container height. Keep exits shorter than enters (150ms vs 300ms). Don't fight for attention — the user's focus is moving to the next thing.
- **Icon animations**: Animate contextual icons (hover-reveal, state-change) with `opacity`, `scale(0.25 -> 1)`, and `blur(4px -> 0px)`. If the project uses `motion` or `framer-motion`, use `transition: { type: "spring", duration: 0.3, bounce: 0 }`. Otherwise, keep both icons in the DOM and cross-fade with CSS transitions using `cubic-bezier(0.2, 0, 0, 1)`.
- **Scale on press**: `scale(0.96)` on `:active` for buttons. Already in `domo-app-theme`. Never below `0.95`. Disable with a `data-static` attribute where motion would distract.
- **Skip page-load animation**: Use `initial={false}` on `AnimatePresence` (if using Framer Motion) to prevent enter animations on first render. Elements in their default state should not animate in on page load.

## Performance

From `make-interfaces-feel-better` > performance:

- **Transition specificity**: Never use `transition: all`. Always specify exact properties: `transition-property: scale, opacity, background-color`. Tailwind's `transition-transform` covers `transform, translate, scale, rotate`.
- **will-change**: Only for `transform`, `opacity`, `filter`. Only when you notice first-frame stutter. Never `will-change: all`. Each extra compositing layer costs memory.

## Color & Contrast

From `color-oklch`:

- **OKLCH everywhere**: All colors in the custom app should use `oklch()` syntax. The `domo-app-theme` already provides the full palette in OKLCH with hex fallback comments. Extend the palette using the same color space.
- **Chart color series**: Generate data-encoding colors using constant hue with the OKLCH palette algorithm (fixed lightness range 0.97–0.25, gamma 1.5, chroma clamped per step). Use the same chroma percentage across hues for consistent vividness.
- **Contrast checking**: Verify text contrast using APCA thresholds — Lc 60 for normal text, Lc 45 for large text, Lc 30 for UI components. Adjust oklch L channel to fix contrast, keep C and H constant.
- **Gamut safety**: Clamp chroma to the sRGB maximum for the given L/H pair. High-chroma values at certain hues will clip silently. Cyans have the lowest max chroma; purples have the highest.
- **Dark mode**: If the custom app supports dark mode, reverse the palette L mapping (lightest becomes darkest). OKLCH's perceptual uniformity makes this work cleanly. Simplify shadows to a single white ring: `0 0 0 1px oklch(1 0 0 / 0.08)`.

## Copy Quality

From `writing-better`:

Apply to all user-facing text in the custom app: labels, tooltips, error messages, empty states, help text, button text, section headers.

- Use active voice, positive form, definite language
- Omit needless words — if a label can lose a word without losing meaning, cut it
- Avoid AI writing tells: no "delve", no "let's break this down", no negative parallelism, no tricolon abuse
- Keep related words together — don't split subject from verb with long parentheticals
- Place emphatic words at end of sentence

## Checklist

Before publishing a pro-code app for App Studio:

- [ ] `domo-app-theme` loaded as base CSS
- [ ] Font smoothing applied to root
- [ ] Headings use `text-wrap: balance`
- [ ] Dynamic numbers use `tabular-nums`
- [ ] Nested rounded elements use concentric border radius
- [ ] Icons optically centered, not just geometrically
- [ ] Shadows used instead of borders for depth elements
- [ ] Enter animations split and staggered (~100ms)
- [ ] Exit animations subtle (small translateY, 150ms)
- [ ] No `transition: all` — only specific properties
- [ ] Interactive elements have 40x40px minimum hit area
- [ ] All colors in OKLCH
- [ ] Text contrast passes APCA Lc 60 for normal text
- [ ] Data-encoding colors use consistent chroma percentage across hues
- [ ] Body background set to `transparent` or `--bg` for canvas blending
- [ ] `acceptFilters: true` set on the content entry
- [ ] `domo.onFiltersUpdate` registered if page filters should propagate
- [ ] UI copy reviewed for clarity and concision
