# Domain Palettes & Data Typography

## 1. Domain-Tested Semantic Palettes

Pick **one** palette per project and encode its colors into `DESIGN.md`.

### A. Energy / Grid / Industrial Policy (High Clarity on Light Slate)
- **Primary / Policy**: `#0284c7` (Deep Sky Blue)
- **Baseline / Reference**: `#64748b` (Cool Slate, dashed line)
- **Positive / Surplus / Win**: `#059669` (Emerald)
- **Storage / Renewable / Secondary**: `#0d9488` (Teal)
- **Warning / Peak / Threshold**: `#d97706` (Amber)
- **Deficit / Curtailment / Risk**: `#dc2626` (Crimson)

### B. Finance / Quantitative Trading (Okabe-Ito Colorblind-Friendly Categorical)
- Series order (max 6 before small multiples): `['#1d4ed8', '#ea580c', '#0d9488', '#7c3aed', '#ca8a04', '#475569']`
- Note for Chinese financial/market UIs vs international UIs: clarify explicitly in legend/labels whether `+` is green or red if regional convention matters, and keep sign prefixes (`+` / `-`) visible.

### C. Dark Mode Console Pairings
- **Canvas**: `#0b1120` | **Panel**: `#111827` | **Gridline**: `rgba(148, 163, 184, 0.14)`
- **Primary Ink**: `#f1f5f9` | **Secondary Ink**: `#94a3b8`
- **Brightened Accents**: `#38bdf8` (Sky), `#34d399` (Emerald), `#fbbf24` (Amber), `#fb7185` (Rose)

## 2. Numerical & Bilingual Typography Rules
- **Font Family**: `"Inter", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif`
- **Tabular Figures**: Always set `font-variant-numeric: tabular-nums` on KPI cards, axis labels (`axisLabel`), HTML tooltips, and data tables so updating sliders never causes jittery column shifts.
- **Units & Precision**:
  - Put units once in the chart subtitle or Y-axis `name` (`净现值 / 万元`, `电价 / 元·MWh⁻¹`), not crammed onto every tick label.
  - Format large values cleanly (`12,480` or `1.25万`) rather than raw `12480.394812`.
