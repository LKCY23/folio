#!/usr/bin/env node
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

function printHelp() {
  console.log(`Usage: verify_page.mjs --url <url-or-file> [options]

Options:
  --url <target>          Target HTTP(S) URL or local HTML file path (required)
  --out <dir>             Output directory for screenshots and report.json (default: .folio-verify)
  --viewports <list>      Comma-separated WxH list (default: 1440x900,768x1024,390x844)
  --wait-ms <ms>          Wait duration after networkidle in ms (default: 500)
  --full-page             Capture full scrollable page instead of viewport only
  --help                  Show this help message
`);
}

function parseArgs(argv) {
  const opts = {
    url: '',
    out: '.folio-verify',
    viewports: '1440x900,768x1024,390x844',
    waitMs: 500,
    fullPage: false,
    help: false
  };
  for (let i = 0; i < argv.length; i += 1) {
    const arg = argv[i];
    if (arg === '--help' || arg === '-h') {
      opts.help = true;
    } else if (arg === '--full-page') {
      opts.fullPage = true;
    } else if (arg === '--url' && i + 1 < argv.length) {
      opts.url = argv[++i];
    } else if (arg === '--out' && i + 1 < argv.length) {
      opts.out = argv[++i];
    } else if (arg === '--viewports' && i + 1 < argv.length) {
      opts.viewports = argv[++i];
    } else if (arg === '--wait-ms' && i + 1 < argv.length) {
      opts.waitMs = Number(argv[++i]) || 500;
    } else {
      throw new Error(`Unknown or incomplete argument: ${arg}`);
    }
  }
  return opts;
}

function parseViewports(spec) {
  return spec.split(',').map((token) => {
    const match = /^(\d+)x(\d+)$/i.exec(token.trim());
    if (!match) {
      throw new Error(`Invalid viewport "${token}". Expected WxH like 1440x900.`);
    }
    return { width: Number(match[1]), height: Number(match[2]), label: `${match[1]}x${match[2]}` };
  });
}

function resolveTargetUrl(raw) {
  if (/^(https?|file):\/\//i.test(raw)) {
    return raw;
  }
  const abs = path.resolve(raw);
  if (!fs.existsSync(abs)) {
    throw new Error(`Target file not found: ${abs}`);
  }
  return pathToFileURL(abs).href;
}

async function loadPlaywright() {
  for (const pkg of ['playwright', 'playwright-core']) {
    try {
      const mod = await import(pkg);
      if (mod && mod.chromium) return mod;
    } catch {
      // try next package
    }
  }
  return null;
}

async function main() {
  let opts;
  try {
    opts = parseArgs(process.argv.slice(2));
  } catch (err) {
    console.error(JSON.stringify({ ok: false, error: err.message }));
    process.exit(1);
  }

  if (opts.help) {
    printHelp();
    process.exit(0);
  }

  if (!opts.url) {
    console.error(JSON.stringify({ ok: false, error: 'Missing required --url argument. Run with --help.' }));
    process.exit(1);
  }

  let viewports;
  let targetUrl;
  try {
    viewports = parseViewports(opts.viewports);
    targetUrl = resolveTargetUrl(opts.url);
  } catch (err) {
    console.error(JSON.stringify({ ok: false, error: err.message }));
    process.exit(1);
  }

  const pw = await loadPlaywright();
  if (!pw) {
    const payload = {
      ok: false,
      error: 'Playwright is not installed in the current environment.',
      remediation: 'Install locally with `npm install -D playwright && npx playwright install chromium`, or use the host native browser.'
    };
    console.error(JSON.stringify(payload, null, 2));
    process.exit(2);
  }

  fs.mkdirSync(opts.out, { recursive: true });
  const browser = await pw.chromium.launch({ headless: true });
  const results = [];

  try {
    for (const vp of viewports) {
      const context = await browser.newContext({ viewport: { width: vp.width, height: vp.height } });
      const page = await context.newPage();
      const consoleErrors = [];
      const pageErrors = [];

      page.on('console', (msg) => {
        if (msg.type() === 'error') {
          consoleErrors.push(msg.text());
        }
      });
      page.on('pageerror', (err) => {
        pageErrors.push(err.message || String(err));
      });

      await page.goto(targetUrl, { waitUntil: 'networkidle', timeout: 30000 });
      if (opts.waitMs > 0) {
        await page.waitForTimeout(opts.waitMs);
      }

      const metrics = await page.evaluate(() => {
        const doc = document.documentElement;
        const brokenImages = Array.from(document.querySelectorAll('img'))
          .filter((img) => img.complete && img.naturalWidth === 0)
          .map((img) => img.getAttribute('src') || '(no src)');
        return {
          title: document.title || '',
          scrollWidth: doc.scrollWidth,
          clientWidth: doc.clientWidth,
          horizontalOverflow: doc.scrollWidth > doc.clientWidth,
          brokenImages
        };
      });

      const shotPath = path.join(opts.out, `shot-${vp.label}.png`);
      await page.screenshot({ path: shotPath, fullPage: opts.fullPage });

      results.push({
        viewport: vp.label,
        screenshot: shotPath,
        horizontalOverflow: metrics.horizontalOverflow,
        scrollWidth: metrics.scrollWidth,
        clientWidth: metrics.clientWidth,
        brokenImages: metrics.brokenImages,
        consoleErrors,
        pageErrors
      });
      await context.close();
    }
  } finally {
    await browser.close();
  }

  const hasIssues = results.some(
    (r) => r.horizontalOverflow || r.brokenImages.length > 0 || r.consoleErrors.length > 0 || r.pageErrors.length > 0
  );
  const report = {
    ok: !hasIssues,
    target: targetUrl,
    viewports: results
  };
  const reportPath = path.join(opts.out, 'report.json');
  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n', 'utf8');
  console.log(JSON.stringify({ ...report, reportPath }, null, 2));
  process.exit(hasIssues ? 1 : 0);
}

main().catch((err) => {
  console.error(JSON.stringify({ ok: false, error: err && err.message ? err.message : String(err) }));
  process.exit(1);
});
