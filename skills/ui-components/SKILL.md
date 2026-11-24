---
name: ui-components
description: >-
  Architect and implement clean frontend components and layouts for either
  zero-build single-file HTML workbenches (Mode A) or modern Vite/Next.js +
  Tailwind + shadcn/ui apps (Mode B). Enforces complete interactive states,
  form/table hygiene, and accessibility. Use when building UI layouts,
  dashboards, forms, tables, or refactoring frontend components.
---

# UI Components & Engineering Discipline

Choose the lightest stack that fits the product, reuse mature accessible primitives instead of hand-coding broken widgets, and ship complete interaction states.

## Step 1: Select Delivery Stack Mode

Consult [stack-modes.md](./references/stack-modes.md):
- **Mode A — Zero-Build Single-File Workbench**: Use for standalone simulation consoles, algorithm demos, policy workbenches, and self-contained HTML reports. Uses semantic HTML + CSS Custom Properties (`DESIGN.md` tokens) + ECharts 5.
- **Mode B — Modern Frontend App**: Use for Vite, Next.js, or multi-route SaaS/web apps. Uses Tailwind CSS + CSS token variables + **`shadcn/ui`**.

## Step 2: Reuse Components via `folio-shadcn` MCP (Mode B)

When working in a React/Tailwind codebase with `folio-shadcn` MCP available:
1. Search the registry before hand-writing dialogs, popovers, dropdowns, sliders, tabs, or data tables.
2. Inspect the component dependencies and install/adapt it to match the project's `DESIGN.md` tokens.
3. Never build custom `<div>` dropdowns, modals, or switches without Radix/shadcn keyboard & ARIA semantics.

## Step 3: Enforce States, Tables & Accessibility

Read [states-and-a11y.md](./references/states-and-a11y.md) before finalizing markup/CSS:
- Implement all applicable states (`hover`, `focus-visible`, `active`, `disabled`, `loading`, `empty`, `error`).
- Enforce `tabular-nums`, sticky/scannable headers, and overflow wrappers on tables.
- Maintain contrast (`>=4.5:1` body, `>=3:1` large/UI), semantic elements, and responsive breakpoints down to `390px`.
