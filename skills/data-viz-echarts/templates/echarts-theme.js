(function (root, factory) {
  if (typeof module === 'object' && module.exports) {
    module.exports = factory();
  } else {
    var exported = factory();
    root.FOLIO_ECHARTS_THEMES = exported.FOLIO_ECHARTS_THEMES;
    root.registerFolioEChartsThemes = exported.registerFolioEChartsThemes;
  }
}(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  var FONT_FAMILY = '"Inter", "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", system-ui, sans-serif';

  var FOLIO_ECHARTS_THEMES = {
    'folio-light': {
      color: ['#0284c7', '#059669', '#d97706', '#7c3aed', '#e11d48', '#0d9488'],
      backgroundColor: 'transparent',
      textStyle: {
        fontFamily: FONT_FAMILY,
        color: '#0f172a'
      },
      title: {
        textStyle: { color: '#0f172a', fontWeight: 600, fontSize: 15 },
        subtextStyle: { color: '#475569', fontSize: 12 }
      },
      legend: {
        textStyle: { color: '#334155', fontSize: 12 },
        itemWidth: 14,
        itemHeight: 8
      },
      tooltip: {
        backgroundColor: 'rgba(255, 255, 255, 0.96)',
        borderColor: '#cbd5e1',
        borderWidth: 1,
        padding: [10, 12],
        textStyle: { color: '#0f172a', fontSize: 12, fontFamily: FONT_FAMILY }
      },
      grid: {
        top: 48,
        right: 20,
        bottom: 28,
        left: 16,
        containLabel: true
      },
      categoryAxis: {
        axisLine: { lineStyle: { color: '#cbd5e1' } },
        axisTick: { show: false },
        axisLabel: { color: '#475569', fontSize: 11 },
        splitLine: { show: false }
      },
      valueAxis: {
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#475569', fontSize: 11 },
        splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.22)', type: 'dashed' } }
      }
    },
    'folio-dark': {
      color: ['#38bdf8', '#34d399', '#fbbf24', '#a78bfa', '#fb7185', '#2dd4bf'],
      backgroundColor: 'transparent',
      textStyle: {
        fontFamily: FONT_FAMILY,
        color: '#f1f5f9'
      },
      title: {
        textStyle: { color: '#f1f5f9', fontWeight: 600, fontSize: 15 },
        subtextStyle: { color: '#94a3b8', fontSize: 12 }
      },
      legend: {
        textStyle: { color: '#cbd5e1', fontSize: 12 },
        itemWidth: 14,
        itemHeight: 8
      },
      tooltip: {
        backgroundColor: 'rgba(15, 23, 42, 0.96)',
        borderColor: '#334155',
        borderWidth: 1,
        padding: [10, 12],
        textStyle: { color: '#f1f5f9', fontSize: 12, fontFamily: FONT_FAMILY }
      },
      grid: {
        top: 48,
        right: 20,
        bottom: 28,
        left: 16,
        containLabel: true
      },
      categoryAxis: {
        axisLine: { lineStyle: { color: '#334155' } },
        axisTick: { show: false },
        axisLabel: { color: '#94a3b8', fontSize: 11 },
        splitLine: { show: false }
      },
      valueAxis: {
        axisLine: { show: false },
        axisTick: { show: false },
        axisLabel: { color: '#94a3b8', fontSize: 11 },
        splitLine: { lineStyle: { color: 'rgba(148, 163, 184, 0.16)', type: 'dashed' } }
      }
    }
  };

  function registerFolioEChartsThemes(echartsInstance) {
    if (!echartsInstance || typeof echartsInstance.registerTheme !== 'function') {
      return false;
    }
    Object.keys(FOLIO_ECHARTS_THEMES).forEach(function (name) {
      echartsInstance.registerTheme(name, FOLIO_ECHARTS_THEMES[name]);
    });
    return true;
  }

  return {
    FOLIO_ECHARTS_THEMES: FOLIO_ECHARTS_THEMES,
    registerFolioEChartsThemes: registerFolioEChartsThemes
  };
}));
