# `DESIGN.md` Lean Contract Template

Create or update `DESIGN.md` in the project root (or UI workspace folder) during Phase 1 so every subsequent component, chart, and fix shares one source of truth. Keep it concise (under 60 lines).

```markdown
# DESIGN.md

## 1. Surface & Mode
- **Scenario**: <1. Workbench | 2. SaaS App | 3. Landing/Showcase | 4. Docs/Report | 5. Redesign>
- **Mode**: <Operate | Persuade | Experience | Read>
- **Delivery Stack**: <Mode A: Single-file HTML + ECharts 5 | Mode B: React + Tailwind + shadcn/ui>
- **Visual Direction**: <1-2 sentences describing tone, contrast, and primary focal hierarchy>

## 2. Color Tokens (Semantic First)
- `--bg-canvas`: <#hex> (page background)
- `--bg-surface`: <#hex> (panels, cards, tables)
- `--bg-subtle`: <#hex> (hover states, recessed inputs, table stripes)
- `--border-default`: <#hex> (1px crisp hairlines)
- `--ink-primary`: <#hex> (>= 4.5:1 contrast on surface)
- `--ink-secondary`: <#hex> (tinted from surface/ink hue, >= 4.5:1 for body)
- `--accent-primary`: <#hex> (primary actions, active tab, primary series)
- `--status-positive` / `--status-warning` / `--status-danger`: <#hex> / <#hex> / <#hex>

## 3. Typography & Rhythm
- **UI Sans**: `"Inter", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif`
- **Data / Mono**: `"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace`
- **Scale**: `12px (meta) / 14px (body) / 16px (card title) / 20px (section) / 28px+ (page/KPI)`
- **Numeric Rule**: `font-variant-numeric: tabular-nums;` on all KPIs, tables, badges, and chart axes
- **Spacing Base**: `4px / 8px / 12px / 16px / 24px / 32px` (more space above headings than below)
- **Radius & Depth**: `6px` inputs/buttons, `10px` panels; crisp 1px borders + subtle offset shadow (no neon halos)

## 4. Hard Bans for This Project
- No raw `canvas.getContext("2d")` statistical charts (use ECharts 5).
- No emoji/unicode icons standing in for SVG UI icons.
- <Add 1-2 project-specific bans, e.g. no purple gradients, no nested cards>
```
