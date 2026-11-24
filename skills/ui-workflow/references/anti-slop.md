# Anti-Slop Craft Principles (Mode-Calibrated)

Distilled from Anthropic's `frontend-design` aesthetic discipline and refined for production engineering across both expressive websites and high-density data interfaces.

## 1. Commit Before Coding
Default LLM outputs look generic ("AI slop") because they average across safe templates. Before writing CSS or JSX:
1. **Pick a deliberate visual stance** anchored to the domain (e.g., *editorial financial terminal*, *clean clinical lab console*, *warm tactile publication*, *industrial control room*).
2. **Establish clear dominance**: One primary accent (<=10% surface area) + disciplined neutral scale. Never let 4 saturated colors fight equally on screen.
3. **Create obvious typographic hierarchy**: Distinct size, weight, and spacing jumps between page title, section heading, body, and metadata. Pair Latin + CJK cleanly (`"Inter", "PingFang SC", "Microsoft YaHei"`).

## 2. Mode Calibration (Avoid Over-Designing Workbenches)
- **On `Persuade` / `Experience` (landing pages, showcases)**: Push contrast, asymmetric composition, expressive display type, and one memorable focal centerpiece.
- **On `Operate` / `Read` (dashboards, simulation consoles, SaaS, docs)**: Ambition means **precision, restraint, and zero visual friction**. Keep backgrounds quiet so data, charts, and controls carry the visual weight.

## 3. Hard Refusal Checklist (Block These Habits)
- **Banned Page Scaffolds**:
  - Repetitive 3-column equal-size `[icon + bold title + 2-line blurb]` card grids as the default layout.
  - Nested cards inside cards inside cards (use crisp dividers, subtle background shifts, or spacing instead).
  - Mandatory eyebrow/kicker labels (`01 // OVERVIEW`) above every single heading.
  - Giant hero metric templates when the user actually needs comparison or trend context.
- **Banned Surface Habits**:
  - Unmotivated purple/indigo-to-cyan gradients, rainbow borders, or zero-offset glowing box-shadows.
  - Decorative `backdrop-filter: blur()` glassmorphism on non-floating panels.
  - One-sided colored accent bars (`border-left: 4px solid ...`) on every rounded card.
  - Gradient text on headings or KPI numbers (reduces legibility).
  - Monospace font used as a "techy costume" on prose labels instead of actual code, IDs, or aligned data.
  - Emoji or raw Unicode arrows/stars (`🚀`, `📊`, `✨`) replacing a consistent SVG icon set (e.g. Lucide).
  - Unstyled browser defaults on custom UIs (broken text selection contrast, jarring default scrollbars on dark consoles, misaligned table numerals).
- **Motion Discipline**:
  - One purposeful focal transition or chart reveal rather than slapping identical fade-up animations onto every block.
  - Always respect `@media (prefers-reduced-motion: reduce)`.
