#!/usr/bin/env node
// Screenshot a local HTML file OR a live URL at exact pixel dimensions using
// Playwright chromium. Also used as the reference-capture engine (see
// capture_reference.py): pointing this at a real product's live page grabs
// a genuine design reference with no gallery, signup, or paywall involved.
// Usage: node html_to_png.mjs <file.html-or-url> <out.png> <WIDTHxHEIGHT> [--full]
// --full: capture the full scrollable page height, not just the viewport
//   (use for reference capture; omit for fixed-canvas Track A renders).
// Works around version-mismatched Playwright caches by falling back to any
// cached chromium build, then system chromium.
import { existsSync, readdirSync } from "fs";
import { createRequire } from "module";

// playwright isn't installed globally — resolve it from a repo that has it
// (override with PLAYWRIGHT_ROOT=/path/to/repo)
const pwRoot = process.env.PLAYWRIGHT_ROOT ?? `${process.env.HOME}/content-ideas`;
const { chromium } = createRequire(`${pwRoot}/package.json`)("playwright");

const rawArgs = process.argv.slice(2);
const fullPage = rawArgs.includes("--full");
const settleIdx = rawArgs.indexOf("--settle");
const settleMs = settleIdx >= 0 ? Number(rawArgs[settleIdx + 1]) : 0;
const args = rawArgs.filter((a, i) => a !== "--full" && !(settleIdx >= 0 && (i === settleIdx || i === settleIdx + 1)));
const [html, out, size] = args;
if (!html || !out || !/^\d+x\d+$/.test(size ?? "")) {
  console.error("usage: node html_to_png.mjs <file.html-or-url> <out.png> <WIDTHxHEIGHT> [--full]");
  process.exit(2);
}
const [width, height] = size.split("x").map(Number);

function findExecutable() {
  const cache = `${process.env.HOME}/.cache/ms-playwright`;
  if (existsSync(cache)) {
    for (const d of readdirSync(cache).filter(d => d.startsWith("chromium-")).sort().reverse()) {
      for (const sub of ["chrome-linux64/chrome", "chrome-linux/chrome"]) {
        const p = `${cache}/${d}/${sub}`;
        if (existsSync(p)) return p;
      }
    }
  }
  for (const p of ["/usr/bin/chromium-browser", "/usr/bin/chromium", "/snap/bin/chromium"]) {
    if (existsSync(p)) return p;
  }
  return undefined; // let playwright try its default
}

const browser = await chromium.launch({ executablePath: findExecutable() });
const page = await browser.newPage({
  viewport: { width, height },
  userAgent: "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
});
const url = html.startsWith("http") ? html : `file://${html.startsWith("/") ? html : process.cwd() + "/" + html}`;
await page.goto(url, { waitUntil: "networkidle", timeout: 45000 });
if (settleMs > 0) await page.waitForTimeout(settleMs);
await page.screenshot({ path: out, fullPage });
await browser.close();
console.log(`saved: ${out} ${width}x${height}${fullPage ? " (full page)" : ""}${settleMs ? ` (settled ${settleMs}ms)` : ""}`);
