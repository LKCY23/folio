# Folio Frontend & UI Guardrails

> **Scope Guard**: Apply these rules **ONLY** when creating, redesigning, auditing, or modifying frontend UI, web pages, dashboards, HTML demos, or data visualizations. Ignore completely for backend, algorithm, CLI, infra, or configuration-only tasks.

1. **Route & Lock Contract First**: Before styling or editing layout, classify the surface into one of the 5 scenarios (Data Workbench, B2B SaaS, Marketing/Showcase, Editorial/Docs, or Audit/Redesign) via `ui-workflow` and establish or follow `DESIGN.md` tokens (palette, type scale, 8px spacing rhythm, bans).
2. **Never Hand-Roll Statistical Charts**: Do not draw line, bar, area, scatter, or dashboard charts using raw `canvas.getContext("2d")` primitives. Use **Apache ECharts 5** (or the repository's existing professional charting engine) following `data-viz-echarts`.
3. **Reuse Accessible Component Primitives**: In React/Tailwind codebases, prefer mature primitives (`shadcn/ui` / Radix via `folio-shadcn` MCP) over ad-hoc `<div>` controls. Implement complete interactive states (`hover`, `focus-visible`, `disabled`, `loading`, `empty`, `error`).
4. **Tabular Numerals Everywhere Data Lives**: Apply `font-variant-numeric: tabular-nums` to KPIs, financial/simulation tables, badges with metrics, and chart axes/tooltips.
5. **Run Static UI Gate Before Delivery**: After UI edits, run `tools/check_ui_static.py` on the modified frontend files to catch raw Canvas 2D charts, missing viewport tags, missing `tabular-nums`, and basic accessibility defects.
6. **Close the Visual Loop**: Verify rendered output in a real browser (host native browser first; `skills/ui-visual-verify/scripts/verify_page.mjs` fallback in headless/CLI runs), inspect console errors and overflow across desktop and mobile viewports, and batch-fix issues before reporting done.
