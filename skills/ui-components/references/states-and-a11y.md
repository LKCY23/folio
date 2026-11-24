# Production UI Engineering Rules (Top 35 Distilled)

Distilled from Vercel's `web-design-guidelines` and production accessibility standards into high-ROI rules.

## A. Interactive State Machine
1. Every clickable control has visible `hover`, `active`, `focus-visible`, and `disabled` states.
2. Never remove focus outlines (`outline: none`) without supplying a high-contrast `:focus-visible` ring.
3. Async actions show an immediate loading indicator, preserve button width (prevent layout jump), and disable duplicate submission.
4. Every list, search, and chart container handles **Empty** (clear explanation + recovery action) and **Error** (cause + retry) states.
5. Destructive actions require confirmation or undo—never trigger irreversibly on a single accidental click.

## B. Semantics & Accessibility
6. Use `<button type="button|submit">` for actions and `<a href>` for navigation—never `<div onClick>`.
7. Every icon-only button has an explicit `aria-label` (and optional tooltip).
8. Every `<img>` carries meaningful `alt` text (or `alt=""` for purely decorative assets).
9. Associate every form `<input>` / `<select>` with a `<label for>` or `aria-labelledby`; avoid placeholder-only labels for complex forms.
10. Maintain text contrast `>= 4.5:1` for body/captions and `>= 3:1` for large headings, borders, and active chart marks.
11. Support keyboard navigation (`Tab`, `Enter`/`Space`, `Escape` to close modals/drawers, arrow keys in tablists/menus).
12. Respect `@media (prefers-reduced-motion: reduce)` by disabling non-essential transitions.

## C. Forms, Inputs & Parameters
13. Put units (`%`, `MW`, `元/kWh`, `ms`) explicitly in labels or input suffixes—never force users to guess units.
14. Validate on blur or submit (not angrily on the first keystroke); place error text inline next to the offending field.
15. Numeric sliders in simulation consoles must show live current value in `tabular-nums`, support direct numeric input or fine stepping, and provide a quick "Reset to Baseline" control.
16. Persist meaningful view filters/tabs in URL params or clean local state so refreshes/back buttons feel predictable.

## D. Data Tables & Numerical Display
17. Apply `font-variant-numeric: tabular-nums;` to **every** `<table>`, KPI card, financial column, and numeric badge.
18. Right-align numeric columns (`text-align: right`) and left-align text labels; keep units in column headers (`NPV (万元)`) rather than repeating them in every cell.
19. Wrap wide tables in `overflow-x: auto` with `min-width` only on the inner table so narrow viewports never break page width.
20. Sticky table headers (`position: sticky; top: 0`) for long scrollable datasets; subtle hover row highlight.
21. Truncate overflowing identifiers with `text-overflow: ellipsis` + full value on hover/title—never clip silently without recourse.

## E. Layout, Responsive & Performance
22. Include `<meta name="viewport" content="width=device-width, initial-scale=1.0" />` on every HTML entry.
23. Prevent CSS Grid/Flexbox blowout: always add `min-width: 0` on grid/flex columns housing charts, code blocks, or tables.
24. Give images/media explicit `width`/`height` or `aspect-ratio` to eliminate Cumulative Layout Shift (CLS).
25. Keep readable prose measure between `65ch` and `75ch`.
26. Keep click/touch targets at least `36px` tall on desktop (`44px` on touch/mobile controls).
27. Separate sections cleanly with spacing (`16px–32px`) and subtle `1px` borders rather than piling drop shadows everywhere.
28. Ensure dark/light theme toggles update both CSS tokens and ECharts instances cleanly without stale axis colors.
29. Lazy-render or virtualize very large lists (>200 rows) instead of freezing main thread DOM updates.
30. Debounce expensive simulation recalculations (`50ms–120ms`) during continuous slider drag.

## F. Copy & Polish
31. Write concrete action labels ("Run Simulation", "Export CSV") instead of vague "Submit" or "OK".
32. Format numbers consistently (fixed decimals per metric type, explicit `+`/`-` sign on deltas, thousands separators where helpful).
33. Eliminate horizontal scrollbars at `1440px`, `768px`, and `390px` viewports.
34. Style browser surfaces (`::selection`, scrollbars, `accent-color`) from the `DESIGN.md` palette.
35. Verify zero console errors and zero broken asset requests before shipping.
