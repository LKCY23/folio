---
name: data-viz-echarts
description: >-
  Engineer interactive charts and analytical visualizations using Apache ECharts
  5. Bans raw Canvas 2D statistical drawing and guides chart selection,
  baseline-vs-policy comparison tooltips, dual axes, markLine/markArea bands,
  domain palettes, tabular typography, and ResizeObserver lifecycles. Use
  whenever building dashboards, simulation outputs, reports, or metrics UIs.
---

# Data Visualization Engineering (Apache ECharts 5)

Never draw statistical charts with hand-rolled `canvas.getContext("2d")` loops. Ship interactive, accessible, responsive **Apache ECharts 5** charts that align visually with the page's `DESIGN.md` tokens.

## Workflow

1. **Select Chart Type**: Match the analytical question and data shape using [chart-selection.md](./references/chart-selection.md). Replace low-precision pie charts with horizontal bars, stacked bars, or waterfalls whenever values need accurate comparison.
2. **Apply Domain Palette & Typography**: Load [palettes-and-typo.md](./references/palettes-and-typo.md) to pick semantic colors (baseline vs policy vs delta), cap categorical series cleanly, and enforce `tabular-nums` in HTML tooltips and legends.
3. **Register Light/Dark Theme**: Use [echarts-theme.js](./templates/echarts-theme.js) (`registerFolioEChartsThemes(echarts)`) to initialize charts with `folio-light` or `folio-dark`.
4. **Implement Production ECharts Patterns**: Use [echarts-patterns.md](./references/echarts-patterns.md) for:
   - Rich `trigger: 'axis'` comparison tooltips (showing Baseline, Policy, and signed Delta)
   - Gradient area fills and crisp line series
   - Dual Y-axis scaling with clear unit headers
   - `markLine` thresholds and `markArea` scenario/win-win bands
   - Confidence / scenario interval bands (30% / 40% / 30% or min-max envelopes)
   - Clean `ResizeObserver` + `chart.dispose()` lifecycle
