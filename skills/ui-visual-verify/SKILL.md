---
name: ui-visual-verify
description: >-
  Close the frontend visual verification loop without blind coding. Uses host
  native browser tooling first when available, or falls back to the bundled
  Playwright script (verify_page.mjs) for multi-viewport screenshots, console
  error checks, horizontal overflow detection, and broken image audits. Use
  after building or editing any UI page, chart, or stylesheet.
---

# Adaptive Visual Verification

Never treat code edits as complete until the rendered UI is inspected at shipping viewports.

## Tier 1: Host Native Browser (First Choice)

When the active host provides a native browser capability, use it first (zero extra MCP overhead):
- **Claude Code**: `/chrome` extension or Claude Desktop built-in preview
- **Codex**: Codex Desktop App built-in browser tool
- **Antigravity**: Built-in `browser` subagent

Verify:
1. Initial above-the-fold hierarchy, typography contrast, and alignment.
2. Interactive flows (tab switches, slider updates, ECharts hover tooltips, modals, empty/error states).
3. Zero console/page errors and zero horizontal overflow on desktop and mobile widths.

## Tier 2: Bundled Headless Audit (`verify_page.mjs`)

Use [verify_page.mjs](./scripts/verify_page.mjs) whenever running in headless CLI / third-party API environments without native browser UI, or when you want reproducible multi-viewport screenshots + JSON diagnostics:

```sh
node <folio-root>/skills/ui-visual-verify/scripts/verify_page.mjs \
  --url http://localhost:3000 \
  --out .folio-verify
```

Or pass a local HTML file directly (`--url ./demo/index.html`).

What it checks per viewport (`1440x900`, `768x1024`, `390x844` by default):
- Full-viewport PNG screenshots (`<out>/shot-<WxH>.png`)
- `console.error` and uncaught `pageerror` events
- Horizontal overflow (`document.documentElement.scrollWidth > document.documentElement.clientWidth`)
- Broken `<img>` elements (`complete && naturalWidth === 0`)

## Batch-Fix Discipline

Inspect **all** screenshots and JSON findings together, list every visual or runtime defect, fix them in **one** batched edit pass, and re-verify once before concluding.
