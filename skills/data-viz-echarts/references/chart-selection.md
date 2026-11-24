# Data Structure -> Chart Selection Matrix

Choose charts by analytical task, not visual novelty.

| Analytical Question / Data Shape | Best Chart Type | ECharts 5 Implementation | Avoid |
|---|---|---|---|
| Continuous trend over time (1–4 series) | **Line + subtle gradient area** | `type: 'line'`, `showSymbol: false`, soft `areaStyle` | 3D lines; raw Canvas 2D |
| Policy / Strategy vs Baseline over time | **Dual-line + delta tooltip + shaded diff** | Baseline dashed neutral + Policy solid accent; custom `tooltip.formatter` computing `Δ` | Separate disconnected charts when axes match |
| Two metrics with different units (e.g. MW & 元/MWh) | **Dual Y-Axis (bar + line or 2 lines)** | `yAxis: [{ name: 'MW' }, { name: '元/MWh' }]` with color-coded axis names | Normalizing without telling the user units |
| Scenario range / confidence band (P10–P90, 30%/40%/30%) | **Envelope band + median line** | Stacked transparent `lower` series + shaded `band` `areaStyle` + solid median line | Hiding uncertainty in plain text tables only |
| Component contribution to total (e.g. NPV by stakeholder) | **Stacked bar** (or **Waterfall** when +/- offsets) | `type: 'bar'`, `stack: 'total'`, clear positive/negative sign handling | Pie charts with >4 slices or negative values |
| Attribution from start to end (`Baseline -> +A -> -B -> Policy`) | **Waterfall chart** | Transparent base series + positive (`emerald`) / negative (`rose`) bar series | Plain table when visual flow tells the story |
| Ranked comparison across categories (>5 items) | **Horizontal bar chart** (sorted) | `yAxis: { type: 'category', inverse: true }` with right-end value labels | Slanted X-axis labels; radar/spider charts |
| Part-to-whole (<=4 clean positive shares) | **Donut (thin ring)** or **100% stacked bar** | `radius: ['58%', '78%']` with center total KPI | Multi-slice 3D pie charts |
| Distribution / outliers / quantile spread | **Boxplot** or **Histogram bar** | `type: 'boxplot'` or binned bar with mean `markLine` | Hiding skew inside a single mean bar |
| Correlation across 2–3 variables | **Scatter / Bubble** | `type: 'scatter'`, subtle opacity (`0.72`), quadrant `markLine` | Over-plotted solid dots with zero alpha |
| Flow / allocation across stages (e.g. energy or cash flow) | **Sankey diagram** | `type: 'sankey'`, ordered depth columns | Complex spaghetti network graphs |
| Time × category intensity matrix (e.g. 24h × 30d load/price) | **Heatmap** | `type: 'heatmap'` + sequential `visualMap` | 24-line overlapping spaghetti chart |
| Multi-KPI summary table with micro trends | **HTML table + inline ECharts sparklines / data bars** | Crisp `tabular-nums` HTML table with tiny `grid: { inset: 0 }` sparklines | Unformatted raw text tables |

## Golden Rule for Dense Workbenches
- Limit each chart card to **1 primary question**. If >6 series are needed, split into **small multiples** (synchronized `echarts.connect([...])`) or provide an interactive group filter.
