# Figma Handoff Contract (Design-to-Code & Code-to-Figma)

Use this contract whenever a Figma URL, file key, node ID, or design sync task is involved.

## Integration Rule (Zero-Conflict Dual Track)
- **Default**: Use the host's official Figma plugin / authenticated MCP session (available across Claude Code, Codex, and Antigravity).
- **Blank CLI fallback**: Only configure `mcp/optional/figma.json` (`https://mcp.figma.com/mcp`) if no Figma MCP tools are present in the environment.

## Design -> Code Workflow
1. **Inspect Visual & Token Truth First**:
   - Read design context, variable definitions (`get_variable_defs` / design context), and a rendered screenshot (`get_screenshot`) for the target Figma node before writing CSS/JSX.
2. **Map Tokens to `DESIGN.md`**:
   - Translate Figma variables (colors, typography, spacing, radii) into CSS Custom Properties / Tailwind tokens in `DESIGN.md` rather than hardcoding raw hex values per element.
3. **Reuse Before Inventing**:
   - Check Code Connect mappings or existing project components (`shadcn/ui` / local UI primitives) first.
4. **Adapt Responsively**:
   - Treat Figma frames as north-star specs at their designed breakpoint, then ensure fluid behavior at `1440px`, `768px`, and `390px` during Phase 4 visual verification.
5. **Visual Diff**:
   - Compare your rendered browser screenshot against the Figma screenshot to catch spacing drift, wrong weights, clipped labels, or missing states.

## Code -> Figma Workflow
- When pushing a live page or component system back to Figma, extract the finalized `DESIGN.md` tokens and component states cleanly first so Figma receives structured styles/variables rather than ungrouped flat rectangles.
