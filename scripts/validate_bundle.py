#!/usr/bin/env python3
"""Validate folio cross-host manifests, skills, relative links, and MCP configs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")
KEBAB_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
MD_LINK_RE = re.compile(r"\[[^\]]+\]\(([^)]+)\)")


def parse_frontmatter(text: str) -> dict[str, str]:
    lines = text.splitlines()
    if len(lines) < 3 or lines[0].strip() != "---":
        raise ValueError("SKILL.md must start with YAML frontmatter ('---').")
    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        raise ValueError("SKILL.md frontmatter is missing closing '---'.")

    data: dict[str, str] = {}
    i = 1
    while i < end_idx:
        line = lines[i]
        if not line.strip() or line.lstrip().startswith("#"):
            i += 1
            continue
        if ":" not in line:
            i += 1
            continue
        key, raw_val = line.split(":", 1)
        key = key.strip()
        val = raw_val.strip()
        if val in {">-", ">", "|-", "|"}:
            block_lines: list[str] = []
            i += 1
            while i < end_idx and (lines[i].startswith("  ") or not lines[i].strip()):
                block_lines.append(lines[i].strip())
                i += 1
            data[key] = " ".join(part for part in block_lines if part).strip()
            continue
        data[key] = val.strip("'\"")
        i += 1
    return data


def check_markdown_links(md_path: Path, repo_root: Path, errors: list[str]) -> None:
    text = md_path.read_text(encoding="utf-8")
    # Strip fenced code blocks before scanning links.
    stripped = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    for match in MD_LINK_RE.finditer(stripped):
        raw_target = match.group(1).strip().split()[0]
        if (
            raw_target.startswith("http://")
            or raw_target.startswith("https://")
            or raw_target.startswith("mailto:")
            or raw_target.startswith("#")
        ):
            continue
        rel_part = raw_target.split("#", 1)[0]
        if not rel_part:
            continue
        resolved = (md_path.parent / rel_part).resolve()
        if not resolved.exists():
            errors.append(f"Broken relative link in {md_path.relative_to(repo_root)}: {raw_target}")


def validate_repo(repo_root: Path) -> list[str]:
    errors: list[str] = []

    # Phase 1 hygiene: ensure Antigravity/global-installer files are not prematurely present.
    for forbidden in ("plugin.json", "mcp_config.json", "scripts/install.sh"):
        if (repo_root / forbidden).exists():
            errors.append(f"Phase 1 hygiene violation: unexpected file '{forbidden}' exists.")

    claude_manifest_path = repo_root / ".claude-plugin" / "plugin.json"
    codex_manifest_path = repo_root / ".codex-plugin" / "plugin.json"
    manifests: dict[str, dict] = {}
    for label, path in (("claude", claude_manifest_path), ("codex", codex_manifest_path)):
        if not path.is_file():
            errors.append(f"Missing manifest: {path.relative_to(repo_root)}")
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            manifests[label] = data
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {path.relative_to(repo_root)}: {exc}")
            continue

        if data.get("name") != "folio":
            errors.append(f"{path.relative_to(repo_root)}: name must be 'folio'")
        version = str(data.get("version", ""))
        if not SEMVER_RE.match(version):
            errors.append(f"{path.relative_to(repo_root)}: invalid SemVer version '{version}'")
        if not str(data.get("description", "")).strip():
            errors.append(f"{path.relative_to(repo_root)}: empty description")
        skills_rel = data.get("skills")
        if not isinstance(skills_rel, str) or not (path.parent.parent / skills_rel).is_dir():
            errors.append(f"{path.relative_to(repo_root)}: invalid skills directory '{skills_rel}'")

    if "claude" in manifests and "codex" in manifests:
        if manifests["claude"].get("version") != manifests["codex"].get("version"):
            errors.append("Version mismatch between .claude-plugin/plugin.json and .codex-plugin/plugin.json")

    for mcp_rel in (".mcp.json", "mcp/optional/figma.json", "mcp/optional/playwright.json"):
        mcp_path = repo_root / mcp_rel
        if not mcp_path.is_file():
            errors.append(f"Missing MCP config: {mcp_rel}")
            continue
        try:
            mcp_data = json.loads(mcp_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"Invalid JSON in {mcp_rel}: {exc}")
            continue
        if not isinstance(mcp_data.get("mcpServers"), dict) or not mcp_data["mcpServers"]:
            errors.append(f"{mcp_rel}: must declare non-empty mcpServers object")

    rules_path = repo_root / "rules" / "AGENTS.md"
    if not rules_path.is_file() or not rules_path.read_text(encoding="utf-8").strip():
        errors.append("Missing or empty rules/AGENTS.md")

    skills_dir = repo_root / "skills"
    if not skills_dir.is_dir():
        errors.append("Missing skills/ directory")
        return errors

    skill_dirs = sorted(p for p in skills_dir.iterdir() if p.is_dir())
    if not skill_dirs:
        errors.append("skills/ directory contains no skills")

    for sdir in skill_dirs:
        skill_md = sdir / "SKILL.md"
        if not skill_md.is_file():
            errors.append(f"Missing SKILL.md in {sdir.relative_to(repo_root)}")
            continue
        try:
            fm = parse_frontmatter(skill_md.read_text(encoding="utf-8"))
        except ValueError as exc:
            errors.append(f"{skill_md.relative_to(repo_root)}: {exc}")
            continue
        name = fm.get("name", "")
        if not KEBAB_RE.match(name) or name != sdir.name:
            errors.append(f"{skill_md.relative_to(repo_root)}: frontmatter name '{name}' must match directory '{sdir.name}'")
        if not fm.get("description", "").strip():
            errors.append(f"{skill_md.relative_to(repo_root)}: frontmatter description is required")
        check_markdown_links(skill_md, repo_root, errors)

    readme_path = repo_root / "README.md"
    if readme_path.is_file():
        check_markdown_links(readme_path, repo_root, errors)
    else:
        errors.append("Missing README.md")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate folio plugin bundle integrity.")
    parser.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="Repository root path")
    args = parser.parse_args()

    repo_root = Path(args.root).resolve()
    errors = validate_repo(repo_root)
    if errors:
        for err in errors:
            print(f"ERROR: {err}", file=sys.stderr)
        return 1

    print(f"Bundle validation passed for {repo_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
