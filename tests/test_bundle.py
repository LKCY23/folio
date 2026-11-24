import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = Path(__file__).resolve().parent.parent


class FolioBundleTests(unittest.TestCase):
    def test_validate_bundle_passes(self) -> None:
        res = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "validate_bundle.py"), "--root", str(REPO_ROOT)],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(res.returncode, 0, msg=res.stderr + res.stdout)

    def test_static_checker_catches_bad_html(self) -> None:
        bad_html = """<!doctype html>
<html>
<head><title>Bad Workbench</title></head>
<body>
  <style>
    button { outline: none; }
  </style>
  <img src="logo.png">
  <button><svg width="16" height="16"></svg></button>
  <table><tr><td>123.45</td></tr></table>
  <canvas id="c"></canvas>
  <script>
    const ctx = document.getElementById('c').getContext('2d');
    ctx.beginPath();
    ctx.lineTo(10, 20);
    ctx.stroke();
  </script>
</body>
</html>
"""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "bad.html"
            target.write_text(bad_html, encoding="utf-8")
            res = subprocess.run(
                [sys.executable, str(REPO_ROOT / "tools" / "check_ui_static.py"), "--format", "json", str(target)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res.returncode, 1, msg=res.stdout + res.stderr)
            payload = json.loads(res.stdout)
            rules = {item["rule"] for item in payload["findings"]}
            self.assertIn("no-raw-canvas-chart", rules)
            self.assertIn("missing-viewport-meta", rules)
            self.assertIn("img-missing-alt", rules)
            self.assertIn("icon-button-missing-label", rules)
            self.assertIn("table-missing-tabular-nums", rules)
            self.assertIn("outline-none-without-focus", rules)

    def test_static_checker_passes_clean_html(self) -> None:
        clean_html = """<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Clean ECharts Workbench</title>
  <style>
    :root { --bg: #f8fafc; --ink: #0f172a; --accent: #0284c7; }
    button:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }
    table { font-variant-numeric: tabular-nums; }
  </style>
</head>
<body>
  <img src="banner.png" alt="Simulation Overview">
  <button type="button" aria-label="Refresh charts"><svg width="16" height="16"></svg></button>
  <table><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody><tr><td>NPV</td><td>128.40</td></tr></tbody></table>
  <div id="chart" style="height: 320px;"></div>
  <script>
    const chart = echarts.init(document.getElementById('chart'), 'folio-light');
    chart.setOption({ series: [{ type: 'line', data: [1, 2, 3] }] });
  </script>
</body>
</html>
"""
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "clean.html"
            target.write_text(clean_html, encoding="utf-8")
            res = subprocess.run(
                [
                    sys.executable,
                    str(REPO_ROOT / "tools" / "check_ui_static.py"),
                    "--strict",
                    "--format",
                    "json",
                    str(target),
                ],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res.returncode, 0, msg=res.stdout + res.stderr)
            payload = json.loads(res.stdout)
            self.assertEqual(payload["errors"], 0)
            self.assertEqual(payload["warnings"], 0)

    def test_js_templates_and_scripts_syntax(self) -> None:
        for rel in (
            "skills/data-viz-echarts/templates/echarts-theme.js",
            "skills/ui-visual-verify/scripts/verify_page.mjs",
        ):
            res = subprocess.run(
                ["node", "--check", str(REPO_ROOT / rel)],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(res.returncode, 0, msg=f"{rel}: {res.stderr}")

        help_res = subprocess.run(
            ["node", str(REPO_ROOT / "skills/ui-visual-verify/scripts/verify_page.mjs"), "--help"],
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(help_res.returncode, 0, msg=help_res.stderr)
        self.assertIn("--url", help_res.stdout)
        self.assertIn("--viewports", help_res.stdout)


if __name__ == "__main__":
    unittest.main()
