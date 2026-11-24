# `folio` v1 完整架构设计与受管集成规划

> 状态：Phase 1（Claude Code & Codex 核心包体）定稿实施；Phase 2（Antigravity 受管接入）规划中  
> 目标：构建一套独立维护、零冗余、长期稳定、严格融入 `claudespace` + `claude-config` 受管体系的前端开发、UI 设计与数据可视化工作流插件。

---

## 1. 定位与设计原则

- **纯净上游源码仓**：位于 `/Users/lkcy/folio`（远端 `LKCY23/folio`），只维护插件本体、Skills、Rules、本地静态/验收脚本及各宿主原生包清单，不耦合任何业务项目或本机运行态。
- **零预装假设（Clean-slate）**：不假定目标环境预装了第三方设计插件、付费服务或重型外部工具；内置核保持自包含，同时对三宿主官方能力做到“存在即协同、缺失可兜底”。
- **遵循单一部署者（Single Deployer）架构**：严格对齐 `claudespace/docs/deployment-ownership.md` 与 `claude-config` 的管理边界：
  - **`folio` 仓库**：负责资源正文、跨宿主原生包清单、静态门禁与单元验证；**不内置**直接写 `~/.claude/`、`~/.agents/` 或 `~/.gemini/config/` 的全局安装脚本，也不在本仓库手填重复的 marketplace 清单。
  - **`claudespace`**：负责登记 `folio` 的固定提交基线，并通过 `scripts/sync_marketplaces.py` 统一生成与校验宿主市场清单。
  - **`claude-config`**：作为唯一部署者，负责 Profile 选择、Machine 绑定、`plan / apply / plugin` 事务写入与回滚恢复。
- **最小化与最高性价比（80/20 原则）**：用 **4 个正交核心 Skills + 1 个轻量免费免 Key MCP（`folio-shadcn`）+ 2 个本地离线/按需脚本 + 双轨官方协同（Figma / 宿主原生浏览器）** 解决 90%+ 的真实前端与可视化痛点。
- **零干扰边界**：插件规则明确限定只作用于前端开发、UI 设计、页面重构与数据可视化任务，不污染算法、后端、运维或配置工程任务。

---

## 2. 现代前端 5 类核心场景分析（资深前端工程师视角）

AI 写前端之所以每次结果“看运气”，根本原因在于把不同交互目标与信息密度的界面混成了同一种模板。`folio` 首先按**用户任务模式（Mode）+ 信息密度 + 交付形态**将现代前端项目划分为 5 类标准场景：

| 场景类型 | 典型代表 | 核心模式（Mode） | 常见 AI 翻车点 | 工业级标准解法 |
| :--- | :--- | :--- | :--- | :--- |
| **1. 数据工作台与仿真控制台** | 策略回测/交易监控、政策仿真演示台、实验指标看板、BI 面板 | **Operate（操作与决策）**——高信噪比、扫描快、对比准 | 手搓简陋 30 行 Canvas 2D 折线图；数字列不对齐；无对比 Tooltip；参数区与图表区互抢空间 | 严禁手写 Canvas 2D 画统计图；统一 **ECharts 5**（渐变面积、双轴、基准/策略/差值对比 Tooltip、MarkLine/MarkArea 阈值警戒带、情景区间、ResizeObserver）；强制 `tabular-nums` 等宽数字与克制语义色；支持**零构建单文件 HTML** 与 **SPA 工程**双形态 |
| **2. B 端业务应用 / SaaS 后台** | 配置管理、工作流控制台、复杂筛选列表、多步骤表单、设置中心 | **Operate（稳定完成任务）**——一致性与容错率高于炫技 | 用原生 `<div>` 乱拼下拉/弹窗/滑块；漏掉 Loading / Empty / Error / Disabled 状态；键盘焦点与表单校验缺失 | **Vite / Next.js + Tailwind + shadcn/ui（Radix 无头组件）**；通过 `DESIGN.md` 收敛令牌，重点落齐完整交互状态机、表单校验与可访问性 |
| **3. 营销着陆页 / 产品官网 / 作品集** | 开源项目主页、发布页、定价页、交互展示 | **Persuade / Experience（建立信任与转化）** | “AI 塑料感”重灾区：千篇一律的紫蓝渐变、居中三列等大图标卡片、无意义毛玻璃、所有区块同款淡入动画 | 先定视觉世界观（字号对比、留白节奏、单一主视觉锚点），克制且有目的的动效，禁用模板化卡片堆砌与装饰性渐变 |
| **4. 文档站 / 研究报告 / 阅读界面** | 技术文档、交互式论文解读、实验评审报告、Changelog | **Read（深度理解）**——阅读舒适度第一 | 正文铺满超宽屏（>75ch 难以扫读）；标题层级弱；长表格/代码块/公式在窄屏直接撑爆容器 | 控制 65–75ch 正文行宽、清晰目录与锚点导航、高对比度浅/深色方案、表格/代码块/公式自适应滚动与排版 |
| **5. 存量 UI 诊断、精修与设计稿还原** | “这页不好看帮我改”、Figma 稿转代码、上线前视觉体检 | **Audit / Refine / Redesign**——先看渲染真相再动手 | “盲写”不看真实渲染；把“精修”和“重构”混为一谈；改样式顺手改坏原有交互逻辑 | **先验真再落刀**：先真实渲染截图并收集 Console/溢出/对比度问题 → 明确“保留身份精修”还是“替换世界观重构” → 批量修复并复验截图 |

---

## 3. 4 阶段闭环工作流（Skills × 工具链端到端融合）

无论目标页面是单个静态 `index.html` 还是大型 React 工程，均严格按以下 4 阶段推进：

```text
[Phase 1: 定型与契约]             [Phase 2: 架构与构建]              [Phase 3: 静态门禁]            [Phase 4: 自适应视觉闭环]
ui-workflow                      ui-components + data-viz-echarts   tools/check_ui_static.py       ui-visual-verify
───────────────────────          ───────────────────────────────    ────────────────────────       ─────────────────────────
• 判定 5 类前端场景               • 路径 A: 零构建单文件 HTML 工作台  • 拦截原生 getContext("2d")      • 优先: 调用宿主原生浏览器
• 有 Figma 稿 → 调 Figma MCP      • 路径 B: Vite/Next + Tailwind     • 检查 viewport / 横向溢出风险    (Claude /chrome / Codex App
  读取节点/变量/截图                + 调 shadcn MCP 拉取真实组件      • 检查表格 tabular-nums          / AGY browser)
• 无设计稿 → 按场景应用吸收自     • 数据图表统一 ECharts 5 + 内置    • 检查基础 a11y 与反塑料感红线    • 兜底/批量: 运行内置脚本
  Anthropic 的反塑料感原则          亮/暗双模式主题模板               • 输出 error / warn JSON 报告     verify_page.mjs 抓三视口图
• 生成或锁定项目 DESIGN.md        • 补齐完整状态机与交互底线                                         + Console 报错 + 横向溢出
  (Tokens/字阶/间距/禁令)          (Loading/Empty/Error/Focus)                                      → 批量修复后复验交付
```

### 各阶段详细规程

1. **Phase 1 — 定型与契约（`ui-workflow`）**
   - 识别当前任务属于 5 类场景中的哪一类，锁定 Mode（`Operate` / `Persuade` / `Experience` / `Read` / `Audit & Refine`）。
   - 若用户提供 Figma 链接或节点：按 `figma-handoff.md` 规程先读取变量（Variables）、组件结构与截图，将真实设计令牌映射入项目契约。
   - 若无设计稿：依据吸收自 Anthropic `frontend-design` 的反塑料感原则（先定视觉方向、明确主次色彩比例、字号对比、空间节奏与单一视觉焦点，并结合场景控制工作台的克制密度），为项目生成或复用精简的 **`DESIGN.md`**（主色/辅助色/语义色、字阶、8px 间距体系、圆角阴影与明确禁用清单）。

2. **Phase 2 — 架构与构建（`ui-components` + `data-viz-echarts`）**
   - **双交付形态路由**：
     - **模式 A（零构建单文件工作台）**：用于独立仿真控制台、单文件 Demo 与轻量报告，CSS Custom Properties 承载 `DESIGN.md` Token + 引入 ECharts 5 + 内置 `echarts-theme.js` 亮/暗主题模板。
     - **模式 B（工程化前端应用）**：用于 Vite / Next.js + Tailwind 项目，优先通过 **`folio-shadcn` MCP** 检索并安装真实成熟组件，严禁手写无障碍残缺的自定义弹窗/下拉/滑块。
   - **工程底线（内化 Vercel `web-design-guidelines` Top 35 条铁律）**：落齐 `Hover / Focus-visible / Active / Disabled / Loading / Empty / Error` 状态机、表单校验与错误恢复、URL 状态/防抖、CLS 防抖动与键盘导航。
   - **数据可视化（`data-viz-echarts`）**：彻底禁止手搓 Canvas 2D 统计图；依据数据结构选型矩阵，配置富信息悬浮对比 Tooltip（如“基准 vs 政策 vs 差值”）、`MarkLine`/`MarkArea` 阈值警戒带、情景区间带、`tabular-nums` 等宽数字与 `ResizeObserver` 自适应重绘。

3. **Phase 3 — 静态门禁（`tools/check_ui_static.py`）**
   - 每次修改前端文件后、进入浏览器验收前，用纯 Python 标准库静态体检器 1 秒扫描：
     - 拦截手写原生 `canvas.getContext("2d")` 绘图代码；
     - 检查 `<meta name="viewport">`、潜在固定超宽风险；
     - 检查数据表格与 KPI 区域是否缺失 `tabular-nums`；
     - 检查图片 `alt`、纯图标按钮 `aria-label`、丢失 `:focus-visible` 的 `outline: none` 以及硬编码杂色泛滥；
     - 输出带分级（`error` / `warn`）的 JSON 与摘要报告，先消灭机械低级错误。

4. **Phase 4 — 自适应视觉验收闭环（`ui-visual-verify`）**
   - **第一优先（宿主原生浏览器）**：在 Claude Code 中使用 `/chrome`（或 Desktop 预览），在 Codex Desktop App 中使用内置浏览器预览（后续在 Antigravity 中调度内置 `browser` 子代理），真实打开页面检查布局、交互、Tooltip 与视觉层级。
   - **第二兜底与批量巡检（`verify_page.mjs`）**：当处于纯 CLI、第三方 API 中转、无头环境，或需要一次性对多断点做结构化巡检时，运行内置脚本 `skills/ui-visual-verify/scripts/verify_page.mjs`：
     - 按需调用本地 Playwright（用完即退，平时零进程、零上下文开销）；
     - 抓取 **1440×900（桌面）/ 768×1024（平板）/ 390×844（手机）** 三视口截图；
     - 采集 `console.error`、`pageerror`、横向溢出（`document.documentElement.scrollWidth > clientWidth`）与破损图片（`naturalWidth === 0`），输出结构化 JSON 报告。
   - **批量修复原则**：把一轮验收发现的问题一次性打包修复，再复验截图。

---

## 4. 工具、MCP 与社区生态选取与集成矩阵（L1–L4 分层）

### L1：插件内置本地工具（100% 离线/零账号，跨宿主一致）

| 组件 | 路径 | 作用 | 成本与依赖 |
| :--- | :--- | :--- | :--- |
| **静态 UI 体检器** | `tools/check_ui_static.py` | 自动拦截手写 Canvas 2D、缺 viewport、表格缺失 `tabular-nums`、基础 a11y 与杂色泛滥 | 纯 Python 3 标准库 |
| **多视口验收脚本** | `skills/ui-visual-verify/scripts/verify_page.mjs` | 抓 1440 / 768 / 390 三视口截图 + Console 报错 + 横向溢出 + 破损图 JSON 体检 | Node.js + Playwright（按需调用，不常驻） |
| **ECharts 主题模板** | `skills/data-viz-echarts/templates/echarts-theme.js` | 开箱即用的亮/暗双模式 ECharts 5 主题注册代码（兼容全局 `<script>` 与 ESM/CJS） | 零依赖 JS |
| **插件包自检器** | `scripts/validate_bundle.py` | 校验多宿主清单、版本号一致、SKILL frontmatter、Markdown 相对引用与 MCP JSON 合法性 | 纯 Python 3 标准库 |

### L2：默认内置 MCP（仅 1 个，免费免 API Key）

| MCP 服务 | 启动命令 | 在插件中的配置位置 | 设计原因 |
| :--- | :--- | :--- | :--- |
| **`folio-shadcn`** | `npx shadcn@latest mcp` | `.mcp.json`（Claude Code 插件级 MCP；Codex 可通过受管 Profile/配置按需映射；`mcp/optional/` 保持独立） | 免费免 Key、高杠杆，彻底解决 React/Tailwind 工程组件“手搓简陋控件”痛点；命名为 `folio-shadcn` 以防与其他全局 MCP 冲突 |

### L3：官方能力一等协同（双轨制：优先复用、空白兜底、绝不重复冲突）

| 外部能力 | 默认轨道（推荐） | 空白环境兜底轨道 | 这样设计的工程理由 |
| :--- | :--- | :--- | :--- |
| **Figma 双向工作流** | 直接协同 Claude Code / Codex / Antigravity 三家官方提供的 Figma 插件与官方认证会话；`folio` 在 `ui-workflow/references/figma-handoff.md` 内置标准 **Design-to-Code / Code-to-Figma** 交接规范 | 仓库内置 `mcp/optional/figma.json`（官方 Streamable HTTP 端点 `https://mcp.figma.com/mcp`），供完全空白 CLI 环境按需引用 | 避免在已装官方 Figma 插件的宿主里重复注册第二份 Figma MCP，防止工具名冲突与额外上万 Token 膨胀 |
| **浏览器视觉验收** | 优先调度宿主自带浏览器（Claude `/chrome`、Codex App 浏览器、Antigravity `browser`） | ① 内置 `verify_page.mjs` 跑完即退<br>② 纯 CLI 深度交互可按需引用 `mcp/optional/playwright.json`（`npx @playwright/mcp@latest`） | 不默认常驻 `playwright` MCP，既省启动时间也省每轮工具清单上下文 |

### L4：社区 4 大明星 Skills 的取舍与深度整合

| 社区生态项目 | 在 `folio` 中的集成方式 | 工程取舍理由 |
| :--- | :--- | :--- |
| **Anthropic `frontend-design`** | **核心美学原则完整吸收，并按 5 类场景分流升级** → 融入 `ui-workflow/references/anti-slop.md` 与 `scenarios.md` | 保留其全部反“AI 塑料感”核心原则，同时补齐原版未覆盖的“高密度数据工作台 / B 端后台克制模式”分流，防止工作台过度装饰 |
| **Vercel `web-design-guidelines`** | **提炼 Top 35 条最高性价比工程铁律** → 融入 `ui-components/references/states-and-a11y.md` + 固化进 `tools/check_ui_static.py` | 避免每次把 100+ 条规则全量塞入上下文浪费 Token，同时把可机检规则直接变成静态门禁 |
| **`Impeccable`（`pbakaus/impeccable`）** | **轻量审查内化 + 上游可选协同** | 上游包含 48 份参考文档与独立二进制且迭代极快，硬拷贝进自有仓库极易过时且臃肿；`folio` 内置自包含的轻量诊断与精修流程，若宿主已安装上游 `impeccable`，`ui-workflow` 自动约定深度 Critique/Polish 协同上游 |
| **`UI/UX Pro Max`** | **仅吸收 `DESIGN.md` 契约机制与图表选型思路** | 不搬运其庞大的 97 套静态 CSV 风格/配色表，防止强模型退化成“机械套模板”；数据可视化部分升级为可落地的 ECharts 5 工程技能 `data-viz-echarts` |
| **`antv/mcp-server-chart`** | **v1 刻意不纳入** | 该服务主要返回远程静态图片 URL，适合聊天/文档插图，不适合需要悬浮对比 Tooltip、缩放、动态图例与主题联动的现代交互式前端 |

---

## 5. 仓库完整目录结构与模块职责（Phase 1）

```text
folio/
├── README.md                                  # 架构总览、受管分发原则与本地校验命令
├── LICENSE                                    # MIT 协议
├── .gitignore                                 # 忽略系统临时文件、缓存、虚拟环境与验证截图目录
├── docs/
│   └── architecture-and-plan.md               # 本文档：v1 完整架构设计与受管集成规划
├── .claude-plugin/
│   └── plugin.json                            # Claude Code 原生插件清单 (name: "folio")
├── .codex-plugin/
│   └── plugin.json                            # Codex 原生插件清单 (name: "folio")
├── .mcp.json                                  # Claude Code 插件级 MCP (默认仅 folio-shadcn)
├── mcp/
│   └── optional/
│       ├── figma.json                         # 官方 Figma 远程 MCP 可选片段 (https://mcp.figma.com/mcp)
│       └── playwright.json                    # 官方 Playwright MCP 可选片段 (npx @playwright/mcp@latest)
├── rules/
│   └── AGENTS.md                              # 6 条极简前端守卫铁律（明确仅作用于前端/UI 任务）
├── skills/                                    # 4 个正交核心 Skills（跨宿主 100% 共享，渐进式披露）
│   ├── ui-workflow/
│   │   ├── SKILL.md                           # 总控：需求分级 → 5场景路由 → Figma/Impeccable协同 → DESIGN.md → 4阶段交付
│   │   └── references/
│   │       ├── scenarios.md                   # 5 类场景的模式、密度、排版与布局决策矩阵
│   │       ├── design-tokens.md               # 精简 DESIGN.md 模板（8px 间距、字阶、语义色、圆角/阴影）
│   │       ├── anti-slop.md                   # 吸收自 Anthropic frontend-design 的反塑料感禁令与精修清单
│   │       └── figma-handoff.md               # Figma Design-to-Code 与 Code-to-Figma 标准交接规程
│   ├── ui-components/
│   │   ├── SKILL.md                           # 组件工程：单文件工作台 vs React/Tailwind/shadcn 工程选型与实现
│   │   └── references/
│   │       ├── stack-modes.md                 # 模式 A（零构建单文件工作台）与模式 B（Vite/Next + shadcn）规范
│   │       └── states-and-a11y.md             # 吸收自 Vercel 工程审计 Top 35 条：状态机、表单/表格、焦点与无障碍
│   ├── data-viz-echarts/
│   │   ├── SKILL.md                           # 数据可视化工程：禁用手搓 Canvas 2D → 图表选型 → ECharts 5 落地
│   │   ├── references/
│   │   │   ├── chart-selection.md             # 20+ 数据结构 → 最优图表选型矩阵
│   │   │   ├── echarts-patterns.md            # 渐变面积、双轴、基准/策略/差值 Tooltip、MarkLine/Area、情景区间、ResizeObserver
│   │   │   └── palettes-and-typo.md           # 能源/金融/科研/政企语义色板、色盲友好、tabular-nums、中英混排
│   │   └── templates/
│   │       └── echarts-theme.js               # 亮/暗双模式轻量 ECharts 5 主题注册模板
│   └── ui-visual-verify/
│       ├── SKILL.md                           # 自适应两级视觉验收：宿主原生浏览器优先 → verify_page.mjs 兜底 → 批量修复
│       └── scripts/
│           └── verify_page.mjs                # 三视口截图 + Console/溢出/破损图结构化体检脚本
├── tools/
│   └── check_ui_static.py                     # 零依赖 Python 静态 UI 体检器
├── scripts/
│   └── validate_bundle.py                     # 多宿主清单、SKILL frontmatter、引用路径与 MCP JSON 校验器
└── tests/
    └── test_bundle.py                         # 单元测试（清单校验、静态体检正反例、JS 模板与脚本检查）
```

> 注：**Antigravity 清单（`plugin.json`、`mcp_config.json`）将在 Phase 2** 待 `claude-config` 完成 Antigravity（App + `agy` CLI）受管适配方案与规范后同步补齐。

---

## 6. `claudespace` + `claude-config` 受管集成与分发架构

遵循 `claudespace` 与 `claude-config` 的**单一部署者**契约：`folio` 不自带全局安装/卸载脚本，也不在仓库根生成静态 `marketplace.json`，由 `claudespace` 登记固定提交并由 `claude-config` 统一受管部署。

### Phase 1（当前实施）：Claude Code & Codex 优先落地

1. **Claude Code**：
   - `folio` 提供完整的 `.claude-plugin/plugin.json`、`.mcp.json`（`folio-shadcn`）及 `skills/`。
   - 可在 `claudespace/catalog.json`（`claudespace-personal`）按 `kind: "plugin"`、`source: external`、`compatibility.claude-code.entry: ".claude-plugin/plugin.json"` 登记（与 `sanctuary-translate` 同范式），由 `claudespace` 自动生成根市场并经 `claude-config plugin install / upgrade` 受管部署与锁定版本。
2. **Codex**：
   - `folio` 提供 `.codex-plugin/plugin.json` 与标准 `skills/*/SKILL.md`（并附 `rules/AGENTS.md`）。
   - 适配 `claudespace` 现有约束（当前 `claudespace/docs/marketplace-generation.md` 规定 Codex 市场包仅直接支持本地包或 submodule，不直接支持 `external` 插件）：登记时可选择**以 submodule 纳入 `claudespace` Codex 包装**，或将 `skills/` 中的核心 skill 登记为独立 `skill` 入口，由 `claude-config` 部署到绑定的 `.agents/skills/`。

### Phase 2（待 Antigravity 集成研究与 `claude-config` 适配完成后接入）：Antigravity（App + `agy` CLI）

- **已核实的官方架构事实**：
  - Antigravity 在 **App、CLI（`agy`）、IDE 扩展** 之间共用统一认证层（含 Google Free / Pro / Ultra 个人订阅与企业账号），登录态保存在系统 Keychain，无需独立 API Key。
  - App 与 `agy` CLI 共享同一个全局定制根目录 `~/.gemini/config/`（`plugins/`、`skills/`、`mcp_config.json`、`config.json`），插件安装与启停在两端自动同步；同时 `agy` CLI 独立保存终端 TUI 设置 `~/.gemini/antigravity-cli/settings.json`。
  - `~/.gemini/config/config.json` 以 `0600` 原子写入并同时存储 `userSettings`、权限授予与插件启停，且被 Language Server 实时监听，不能由外部工具粗暴整文件覆写。
- **Phase 2 接入原则**：
  - 先由专门的 `claude-config` 会话完成 Antigravity（App + `agy` CLI）建模、只读 `doctor / plan` 与安全插件目录部署/回滚设计；
  - 适配器确定规范后，再为 `folio` 补充 Antigravity 原生 `plugin.json` 与 `mcp_config.json`，并在 `claudespace` 登记 `compatibility.antigravity`，接入同一套受管生命周期。

---

## 7. 实施路线图、验收标准与边界

### 阶段划分

- **Phase 1（当前交付）**：在 `/Users/lkcy/folio` 落地面向 Claude Code 与 Codex 的 `v0.1.0` 完整包体（原生清单、`.mcp.json`、4 个核心 Skills 与全部 `references/`、`echarts-theme.js`、`rules/AGENTS.md`、`tools/check_ui_static.py`、`verify_page.mjs`、`scripts/validate_bundle.py`、`tests/test_bundle.py`），通过全量自动化校验后提交推送至 `LKCY23/folio` `main`。
- **Phase 2（外部仓受管接入 — Claude Code & Codex）**：在 `claudespace` 登记 `folio` 固定 commit SHA 并同步市场清单，通过 `claude-config` 执行 `plan / apply` 或 `plugin install` 部署验收。
- **Phase 3（Antigravity 受管集成）**：根据 Antigravity 集成分析与 `claude-config` Antigravity 适配器实现结果，补全 `folio` 的 Antigravity 清单并纳入统一部署。

### Phase 1 仓库验收门禁

```sh
python3 scripts/validate_bundle.py
python3 -m unittest discover -s tests -v
node --check skills/ui-visual-verify/scripts/verify_page.mjs
node --check skills/data-viz-echarts/templates/echarts-theme.js
node skills/ui-visual-verify/scripts/verify_page.mjs --help
python3 tools/check_ui_static.py --help
```

### 明确不做的事项

- 不在 `folio` 仓库硬编码任何本机路径、凭据或绕过 `claude-config` 的全局覆盖安装脚本；
- 不硬拷贝外部高频迭代的大型二进制/词表（如 `Impeccable` 48 份参考与二进制、`UI/UX Pro Max` 97 套静态 CSV）；
- 在 `claude-config` 尚未实现 Antigravity 适配器前，不提前对本机 `~/.gemini/config/` 做任何写入操作。
