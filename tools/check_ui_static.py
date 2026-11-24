#!/usr/bin/env python3
"""Zero-dependency static UI quality checker for folio workflows."""

from __future__ import annotations

import argparse
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
from typing import Any

UI_EXTENSIONS = {".html", ".htm", ".css", ".jsx", ".tsx", ".vue", ".svelte"}
SKIP_DIRS = {"node_modules", ".git", "dist", "build", ".venv", "__pycache__", ".folio-verify"}

RAW_CANVAS_RE = re.compile(r"""getContext\(\s*['"]2d['"]\s*\)""")
CANVAS_DRAW_RE = re.compile(r"""\.(?:lineTo|stroke|fillRect|arc|beginPath)\s*\(""")
CHART_LIB_RE = re.compile(r"""\b(?:echarts|Chart|ApexCharts|Plotly|vegaEmbed)\b""")
VIEWPORT_META_RE = re.compile(
    r"""<meta\b[^>]*\bname\s*=\s*['"]viewport['"][^>]*>""",
    re.IGNORECASE,
)
HEAD_TAG_RE = re.compile(r"""<head\b""", re.IGNORECASE)
TABLE_TAG_RE = re.compile(r"""<table\b""", re.IGNORECASE)
TABULAR_NUMS_RE = re.compile(r"""tabular-nums""", re.IGNORECASE)
OUTLINE_NONE_RE = re.compile(r"""outline\s*:\s*(?:none|0)\b""", re.IGNORECASE)
FOCUS_VISIBLE_RE = re.compile(r""":focus-visible\b""", re.IGNORECASE)
HEX_COLOR_RE = re.compile(r"""#[0-9a-fA-F]{3,8}\b""")
CSS_VAR_DEF_RE = re.compile(r"""--[a-zA-Z0-9_-]+\s*:""")
IMG_TAG_RE = re.compile(r"""<img\b([^>]*)>""", re.IGNORECASE | re.DOTALL)
ALT_ATTR_RE = re.compile(r"""\balt\s*=""", re.IGNORECASE)
BUTTON_BLOCK_RE = re.compile(r"""<button\b([^>]*)>(.*?)</button>""", re.IGNORECASE | re.DOTALL)
SVG_OR_ICON_RE = re.compile(r"""<(?:svg|i|span[^>]*icon)""", re.IGNORECASE)
LABEL_ATTR_RE = re.compile(r"""\b(?:aria-label|aria-labelledby|title)\s*=""", re.IGNORECASE)
HTML_TAG_STRIP_RE = re.compile(r"""<[^>]+>""")


class _HtmlInspector(HTMLParser):
    """Lightweight HTML parser to check img alt and icon-only buttons accurately."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.img_missing_alt_lines: list[int] = []
        self.icon_button_lines: list[int] = []
        self._btn_depth = 0
        self._btn_line = 0
        self._btn_has_label = False
        self._btn_has_svg_or_icon = False
        self._btn_text_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag_l = tag.lower()
        attr_map = {k.lower(): (v or "") for k, v in attrs}
        line, _ = self.getpos()

        if tag_l == "img" and "alt" not in attr_map:
            self.img_missing_alt_lines.append(line)

        if tag_l == "button":
            if self._btn_depth == 0:
                self._btn_line = line
                self._btn_has_label = any(k in attr_map for k in ("aria-label", "aria-labelledby", "title"))
                self._btn_has_svg_or_icon = False
                self._btn_text_parts = []
            self._btn_depth += 1
        elif self._btn_depth > 0 and tag_l in {"svg", "i"}:
            self._btn_has_svg_or_icon = True

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() == "button":
            self.handle_endtag(tag)

    def handle_data(self, data: str) -> None:
        if self._btn_depth > 0:
            self._btn_text_parts.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "button" and self._btn_depth > 0:
            self._btn_depth -= 1
            if self._btn_depth == 0:
                text = "".join(self._btn_text_parts).strip()
                if self._btn_has_svg_or_icon and not text and not self._btn_has_label:
                    self.icon_button_lines.append(self._btn_line)


def collect_files(targets: list[Path]) -> tuple[list[Path], list[Path]]:
    files: list[Path] = []
    missing: list[Path] = []
    seen: set[Path] = set()

    for target in targets:
        if not target.exists():
            missing.append(target)
            continue
        if target.is_file():
            resolved = target.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(resolved)
            continue
        for item in sorted(target.rglob("*")):
            if any(part in SKIP_DIRS for part in item.parts):
                continue
            if item.is_file() and item.suffix.lower() in UI_EXTENSIONS:
                resolved = item.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    files.append(resolved)

    return files, missing


def finding(file_path: Path, rule: str, severity: str, message: str, line: int | None = None) -> dict[str, Any]:
    item: dict[str, Any] = {
        "file": str(file_path),
        "rule": rule,
        "severity": severity,
        "message": message,
    }
    if line is not None:
        item["line"] = line
    return item


def scan_file(
    file_path: Path,
    content: str,
    suite_has_tabular_nums: bool,
    suite_has_focus_visible: bool,
) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    suffix = file_path.suffix.lower()
    is_html = suffix in {".html", ".htm"}

    if RAW_CANVAS_RE.search(content) and CANVAS_DRAW_RE.search(content):
        if not CHART_LIB_RE.search(content):
            match = RAW_CANVAS_RE.search(content)
            line = content[: match.start()].count("\n") + 1 if match else None
            issues.append(
                finding(
                    file_path,
                    "no-raw-canvas-chart",
                    "error",
                    "Hand-rolled Canvas 2D drawing detected without ECharts/chart library; replace statistical charts with Apache ECharts 5.",
                    line,
                )
            )

    if is_html and HEAD_TAG_RE.search(content) and not VIEWPORT_META_RE.search(content):
        issues.append(
            finding(
                file_path,
                "missing-viewport-meta",
                "error",
                'HTML <head> is missing <meta name="viewport" content="width=device-width, initial-scale=1.0">.',
            )
        )

    if is_html:
        parser = _HtmlInspector()
        parser.feed(content)
        parser.close()
        for line in parser.img_missing_alt_lines:
            issues.append(
                finding(file_path, "img-missing-alt", "warn", "<img> element is missing an alt attribute.", line)
            )
        for line in parser.icon_button_lines:
            issues.append(
                finding(
                    file_path,
                    "icon-button-missing-label",
                    "warn",
                    "Icon-only <button> lacks aria-label, aria-labelledby, or title.",
                    line,
                )
            )
    elif suffix in {".jsx", ".tsx", ".vue", ".svelte"}:
        for m in IMG_TAG_RE.finditer(content):
            if not ALT_ATTR_RE.search(m.group(1)):
                line = content[: m.start()].count("\n") + 1
                issues.append(
                    finding(file_path, "img-missing-alt", "warn", "<img> element is missing an alt attribute.", line)
                )
        for m in BUTTON_BLOCK_RE.finditer(content):
            attrs, body = m.group(1), m.group(2)
            visible_text = HTML_TAG_STRIP_RE.sub("", body).strip()
            if SVG_OR_ICON_RE.search(body) and not visible_text and not LABEL_ATTR_RE.search(attrs):
                line = content[: m.start()].count("\n") + 1
                issues.append(
                    finding(
                        file_path,
                        "icon-button-missing-label",
                        "warn",
                        "Icon-only <button> lacks aria-label, aria-labelledby, or title.",
                        line,
                    )
                )

    if TABLE_TAG_RE.search(content) and not (TABULAR_NUMS_RE.search(content) or suite_has_tabular_nums):
        issues.append(
            finding(
                file_path,
                "table-missing-tabular-nums",
                "warn",
                "Data <table> found without font-variant-numeric: tabular-nums in file or companion CSS.",
            )
        )

    if OUTLINE_NONE_RE.search(content) and not (FOCUS_VISIBLE_RE.search(content) or suite_has_focus_visible):
        match = OUTLINE_NONE_RE.search(content)
        line = content[: match.start()].count("\n") + 1 if match else None
        issues.append(
            finding(
                file_path,
                "outline-none-without-focus",
                "warn",
                "outline: none/0 used without a :focus-visible replacement rule.",
                line,
            )
        )

    distinct_hex = {m.group(0).lower() for m in HEX_COLOR_RE.finditer(content)}
    if len(distinct_hex) > 12 and not CSS_VAR_DEF_RE.search(content):
        issues.append(
            finding(
                file_path,
                "inline-color-sprawl",
                "warn",
                f"Found {len(distinct_hex)} distinct hex color literals without CSS custom property (--*) definitions.",
            )
        )

    return issues


def main() -> int:
    parser = argparse.ArgumentParser(description="Static UI quality checker for folio frontend deliverables.")
    parser.add_argument("paths", nargs="+", help="HTML, CSS, or frontend component files/directories to inspect.")
    parser.add_argument("--format", choices=("text", "json"), default="text", help="Output format (default: text).")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings as well as errors.")
    args = parser.parse_args()

    targets = [Path(p) for p in args.paths]
    files, missing = collect_files(targets)
    if missing:
        msg = f"Target path(s) not found: {', '.join(str(m) for m in missing)}"
        if args.format == "json":
            print(json.dumps({"ok": False, "error": msg, "findings": []}, ensure_ascii=False, indent=2))
        else:
            print(msg, file=sys.stderr)
        return 2

    contents: dict[Path, str] = {}
    for fp in files:
        contents[fp] = fp.read_text(encoding="utf-8", errors="replace")

    css_text = "\n".join(text for fp, text in contents.items() if fp.suffix.lower() == ".css")
    suite_has_tabular_nums = bool(TABULAR_NUMS_RE.search(css_text))
    suite_has_focus_visible = bool(FOCUS_VISIBLE_RE.search(css_text))

    all_findings: list[dict[str, Any]] = []
    for fp in files:
        all_findings.extend(scan_file(fp, contents[fp], suite_has_tabular_nums, suite_has_focus_visible))

    error_count = sum(1 for item in all_findings if item["severity"] == "error")
    warn_count = sum(1 for item in all_findings if item["severity"] == "warn")
    passed = error_count == 0 and (not args.strict or warn_count == 0)

    if args.format == "json":
        print(
            json.dumps(
                {
                    "ok": passed,
                    "files_scanned": len(files),
                    "errors": error_count,
                    "warnings": warn_count,
                    "findings": all_findings,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
    else:
        print(f"Scanned {len(files)} file(s): {error_count} error(s), {warn_count} warning(s)")
        for item in all_findings:
            loc = f"{item['file']}:{item['line']}" if "line" in item else item["file"]
            print(f"[{item['severity'].upper()}] {item['rule']} ({loc}): {item['message']}")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
