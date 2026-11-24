# folio

面向现代前端开发、UI 设计与数据可视化的跨宿主工作流插件，一套源码同时服务 **Claude Code**、**Codex** 与 **Antigravity**。

## 当前状态

- **阶段**：`v0.2.0`（Phase 2：新增 Antigravity 原生清单 `plugin.json` 与 `mcp_config.json`，与 Claude Code & Codex 共享 4 个核心 Skills、Rules 与静态/视觉门禁工具）。
- **分发原则**：严格遵循 [`claudespace`](https://github.com/LKCY23/claudespace) + [`claude-config`](https://github.com/LKCY23/claude-config) 的**单一部署者（Single Deployer）**规范——本仓库只作为纯净上游源码仓，不内置越权的全局安装脚本，也不在根目录手工维护重复的 marketplace 清单。
- **Antigravity 适配**：已提供根目录 `plugin.json`、`mcp_config.json`、`rules/AGENTS.md` 与 `skills/`，支持由 `claude-config`（Phase B）受管部署至 `~/.gemini/config/plugins/`。

## 核心工作流与工具链

1. **`ui-workflow`**：5 类现代前端场景路由（数据工作台、B 端 SaaS、营销着陆页、文档/报告页、存量 UI 重构）+ `DESIGN.md` 契约 + 反塑料感原则 + Figma/Impeccable 协同。
2. **`ui-components`**：模式 A（零构建单文件 HTML 工作台）vs 模式 B（Vite/Next + Tailwind + `shadcn` MCP），内化表单/表格/状态机/无障碍工程底线。
3. **`data-viz-echarts`**：禁用手搓 Canvas 2D 统计图，提供 ECharts 5 选型矩阵、交互对比 Tooltip/阈值线/情景区间模式与亮/暗主题模板（`skills/data-viz-echarts/templates/echarts-theme.js`）。
4. **`ui-visual-verify`** + **`tools/check_ui_static.py`**：静态体检拦截低级缺陷 + 自适应视觉闭环（宿主原生浏览器优先，`skills/ui-visual-verify/scripts/verify_page.mjs` 兜底三视口截图与 Console/溢出巡检）。

## 本地校验与检查命令

```sh
python3 scripts/validate_bundle.py
python3 -m unittest discover -s tests -v
python3 tools/check_ui_static.py <html-or-frontend-dir>
```

## 文档

- [v1 完整架构设计与受管集成规划](docs/architecture-and-plan.md)

## 许可

[MIT](LICENSE)
