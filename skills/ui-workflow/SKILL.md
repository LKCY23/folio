---
name: ui-workflow
description: >-
  Orchestrate modern frontend development, UI design, redesign, and data
  visualization through a 4-phase workflow: scenario routing and DESIGN.md
  contract, component/ECharts architecture, static quality gate, and adaptive
  visual verification. Use when building, redesigning, auditing, or polishing
  any web UI, dashboard, simulation workbench, SaaS app, landing page, or
  interactive report.
---

# UI Workflow Orchestrator

Run every frontend or UI task through four deterministic phases so visual quality, usability, and code structure stay consistent across single-file HTML demos and full SPA applications.

## Phase 1: Route Scenario & Lock Contract

1. **Inspect existing context first**: Check whether the project already has `DESIGN.md`, CSS variables, Tailwind config, component primitives, or an existing page to refine vs replace.
   - **Refinement** preserves the incumbent identity, layout structure, and copy outside scope.
   - **Redesign** keeps product truth and functionality while replacing the visual world and `DESIGN.md`.
2. **Classify into one of the 5 frontend scenarios** using [scenarios.md](./references/scenarios.md) (`Operate` Workbench, `Operate` SaaS, `Persuade/Experience` Showcase, `Read` Editorial/Docs, or `Audit/Refine/Redesign`).
3. **If a Figma URL or node is provided**: Follow [figma-handoff.md](./references/figma-handoff.md) using the host's Figma MCP/plugin to inspect variables, layout, and screenshot reference before writing code.
4. **Lock `DESIGN.md` tokens & anti-slop direction**:
   - Read [anti-slop.md](./references/anti-slop.md) and commit to a clear, mode-appropriate aesthetic direction (high-SNR restraint for `Operate`/`Read`; intentional editorial/expressive contrast for `Persuade`/`Experience`).
   - Create or update a concise `DESIGN.md` using [design-tokens.md](./references/design-tokens.md) before authoring styles.
   - *Optional synergy*: If the host environment also has upstream `impeccable` installed and the user requests a deep visual critique or multi-comp exploration, coordinate with it rather than duplicating heavy design-director loops.

## Phase 2: Compose Components & Data Visualizations

1. **Components & Layout**: Load `ui-components` to pick Mode A (zero-build single-file HTML workbench) vs Mode B (Vite/Next.js + Tailwind + `shadcn/ui` via `folio-shadcn` MCP) and enforce full interactive states and accessibility.
2. **Charts & Analytics**: Whenever the interface displays metrics over time, comparisons, distributions, or simulation outputs, load `data-viz-echarts`. Never hand-code statistical charts with raw `canvas.getContext("2d")`.

## Phase 3: Static Quality Gate

Run the bundled static checker against edited HTML/CSS/TSX/JSX/Vue/Svelte targets before visual review:

```sh
python3 <folio-root>/tools/check_ui_static.py <target-path>
```

Fix every `error` (and high-signal `warn` such as missing `tabular-nums` on data tables or missing `:focus-visible` after `outline: none`) before proceeding.

## Phase 4: Adaptive Visual Verification

Load `ui-visual-verify` to inspect the live rendered result in the host's native browser (or fallback `verify_page.mjs` across `1440x900`, `768x1024`, and `390x844`). Batch all visual/layout/console findings into a single fix pass, re-verify once, then deliver.
