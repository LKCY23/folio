# Delivery Stack Modes: Single-File Workbench vs Modern App

## Mode A: Zero-Build Single-File HTML Workbench

**Best for**: Simulation demos, research/policy consoles, single-page calculators, portable reports where zero `npm install` overhead is a feature.

### Required Architecture
1. **Viewport & Reset**:
   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0" />
   ```
2. **Tokenized CSS Variables**: Define `:root` (and optional `[data-theme="dark"]`) matching `DESIGN.md` (`--bg-canvas`, `--bg-surface`, `--border-default`, `--ink-primary`, `--ink-secondary`, `--accent-primary`, semantic colors).
3. **Structured Workbench Grid**:
   - Header bar: Title, concise subtitle/scenario badge, global controls (run/reset/theme/export).
   - Main layout: Collapsible/sticky parameter sidebar (`280px–340px`) + fluid `1fr` results canvas (`minmax(0, 1fr)` to prevent CSS Grid chart overflow!).
   - Mobile (`< 900px`): Stack parameter panel cleanly above or behind a toggleable drawer; zero horizontal page scroll.
4. **Data & Charts**:
   - Load ECharts 5 (`echarts.min.js`) cleanly and register `FOLIO_ECHARTS_THEMES` from `data-viz-echarts`.
   - Separate pure calculation/state logic from DOM/chart rendering functions so updates are deterministic and debounced on slider `input`.

---

## Mode B: Vite / Next.js + Tailwind + `shadcn/ui`

**Best for**: Multi-page SaaS products, complex CRUD/forms, persistent apps, team codebases.

### Required Architecture
1. **Token Mapping**: Map `DESIGN.md` semantic tokens into Tailwind CSS variables (`--background`, `--foreground`, `--card`, `--border`, `--primary`, `--muted`, `--destructive`) so `shadcn/ui` components inherit your design automatically.
2. **`folio-shadcn` MCP Workflow**:
   - Query available components (`button`, `card`, `tabs`, `select`, `slider`, `dialog`, `sheet`, `table`, `badge`, `tooltip`, `skeleton`).
   - Install/scaffold via CLI or registry instead of rewriting Radix primitives by hand.
3. **Layout Guardrails**:
   - Always put `min-w-0` on flex/grid children that contain charts or data tables.
   - Keep client state clean (URL search params for filters/tabs where shareability matters; debounced inputs for live sliders/search).
