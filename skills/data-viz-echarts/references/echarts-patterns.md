# Production ECharts 5 Patterns

## 1. Baseline vs Policy Rich Comparison Tooltip (`tabular-nums`)

```js
tooltip: {
  trigger: 'axis',
  axisPointer: { type: 'cross', lineStyle: { type: 'dashed' } },
  renderMode: 'html',
  formatter(params) {
    if (!params || !params.length) return '';
    const title = params[0].axisValueLabel;
    const base = params.find((p) => p.seriesName.includes('基准') || p.seriesName === 'Baseline');
    const policy = params.find((p) => p.seriesName.includes('政策') || p.seriesName === 'Policy');
    const rows = params.map((p) => (
      `<div style="display:flex;justify-content:space-between;gap:16px;font-variant-numeric:tabular-nums;">` +
      `<span>${p.marker}${p.seriesName}</span>` +
      `<strong>${Number(p.value).toLocaleString('zh-CN', { maximumFractionDigits: 2 })}</strong>` +
      `</div>`
    ));
    if (base && policy && Number.isFinite(base.value) && Number.isFinite(policy.value)) {
      const diff = policy.value - base.value;
      const pct = base.value !== 0 ? (diff / Math.abs(base.value)) * 100 : 0;
      const sign = diff >= 0 ? '+' : '';
      const color = diff >= 0 ? '#059669' : '#dc2626';
      rows.push(
        `<div style="margin-top:6px;padding-top:6px;border-top:1px solid rgba(148,163,184,0.3);display:flex;justify-content:space-between;gap:16px;font-variant-numeric:tabular-nums;color:${color};">` +
        `<span>差值 (Δ)</span><strong>${sign}${diff.toFixed(2)} (${sign}${pct.toFixed(1)}%)</strong></div>`
      );
    }
    return `<div style="min-width:190px;"><div style="font-weight:600;margin-bottom:6px;">${title}</div>${rows.join('')}</div>`;
  }
}
```

## 2. Gradient Area + Crisp Baseline Comparison

```js
series: [
  {
    name: '基准情景 (Baseline)',
    type: 'line',
    showSymbol: false,
    lineStyle: { width: 2, type: 'dashed', color: '#64748b' },
    data: baselineData
  },
  {
    name: '政策情景 (Policy)',
    type: 'line',
    smooth: 0.2,
    showSymbol: false,
    lineStyle: { width: 2.5, color: '#0284c7' },
    areaStyle: {
      color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
        { offset: 0, color: 'rgba(2, 132, 199, 0.26)' },
        { offset: 1, color: 'rgba(2, 132, 199, 0.02)' }
      ])
    },
    data: policyData
  }
]
```

## 3. Threshold `markLine` & Win-Win / Alert `markArea`

```js
markLine: {
  symbol: ['none', 'none'],
  label: { formatter: '{b}: {c}', position: 'insideEndTop' },
  lineStyle: { type: 'dashed', width: 1.5, color: '#d97706' },
  data: [{ name: '盈亏平衡线', yAxis: 0 }]
},
markArea: {
  silent: true,
  itemStyle: { color: 'rgba(16, 185, 129, 0.08)' },
  data: [[{ name: '双赢区间', yAxis: 0 }, { yAxis: 120 }]]
}
```

## 4. Scenario / Confidence Envelope Band

Keep `lower` invisible and stack `bandWidth = upper - lower` above it:

```js
series: [
  { name: 'Lower', type: 'line', stack: 'band', showSymbol: false, lineStyle: { opacity: 0 }, areaStyle: { opacity: 0 }, silent: true, data: lowArr },
  { name: '区间 (P30–P70)', type: 'line', stack: 'band', showSymbol: false, lineStyle: { opacity: 0 }, areaStyle: { color: 'rgba(2, 132, 199, 0.16)' }, data: highArr.map((h, i) => h - lowArr[i]) },
  { name: '基准预期', type: 'line', showSymbol: false, lineStyle: { width: 2.5, color: '#0284c7' }, data: midArr }
]
```

## 5. Responsive `ResizeObserver` & Clean Lifecycle

```js
function mountChart(el, themeName, getOption) {
  const chart = echarts.init(el, themeName);
  chart.setOption(getOption());
  const ro = new ResizeObserver(() => chart.resize());
  ro.observe(el);
  return {
    update(nextOption) { chart.setOption(nextOption, { notMerge: false }); },
    dispose() { ro.disconnect(); chart.dispose(); }
  };
}
```

- Always set explicit `min-height` (e.g. `280px–380px`) on `.chart-box` and `containLabel: true` in `grid` so long Chinese/numeric axis labels never clip.
- Place legends at top-left or top-right (`top: 0`), leaving `grid.top >= 44` so legends never collide with Y-axis unit labels.
