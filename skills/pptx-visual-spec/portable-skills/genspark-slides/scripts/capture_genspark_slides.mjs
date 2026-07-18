#!/usr/bin/env node
import fs from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import Module from "node:module";

Module.Module?._initPaths?.();
const require = createRequire(import.meta.url);

function arg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`);
  return idx >= 0 ? process.argv[idx + 1] : fallback;
}

function hasFlag(name) {
  return process.argv.includes(`--${name}`);
}

const url = arg("url");
const out = arg("out");
const chrome = arg("chrome") || process.env.CHROME_PATH;
const userDataDir = arg("user-data-dir") || process.env.GENSPARK_USER_DATA_DIR;
const headed = hasFlag("headed");
const waitMs = Number(arg("wait-ms", "25000"));
const authWaitMs = Number(arg("auth-wait-ms", "0"));
const minSlides = Number(arg("min-slides", "0"));
const scrollPasses = Number(arg("scroll-passes", "8"));

if (!url || !out) {
  console.error("Usage: node capture_genspark_slides.mjs --url <genspark-url> --out <output-dir> [--chrome <path>] [--headed]");
  process.exit(2);
}

const htmlDir = path.join(out, "html");
await fs.mkdir(htmlDir, { recursive: true });

const { chromium } = require("playwright");
const launchOptions = { headless: !headed };
if (chrome) launchOptions.executablePath = chrome;

let browser;
let context;
let page;
if (userDataDir) {
  await fs.mkdir(userDataDir, { recursive: true });
  context = await chromium.launchPersistentContext(userDataDir, {
    ...launchOptions,
    viewport: { width: 1440, height: 1000 },
  });
  page = context.pages()[0] || await context.newPage();
  await page.setViewportSize({ width: 1440, height: 1000 });
} else {
  browser = await chromium.launch(launchOptions);
  page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
}
const seen = new Map();

function collect(rawUrl) {
  if (!rawUrl.includes("/api/files/s/")) return;
  const u = new URL(rawUrl);
  const match = u.pathname.match(/\/api\/files\/s\/([^/]+)/);
  const pageIndex = Number(u.searchParams.get("pageIndex"));
  if (!match || !Number.isFinite(pageIndex)) return;
  u.searchParams.set("scale", "1");
  seen.set(pageIndex, { id: match[1], url: u.toString() });
}

page.on("request", req => collect(req.url()));
page.on("response", res => collect(res.url()));

await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
await page.waitForTimeout(5000);

if (/accounts\.google\.com|login\.genspark\.ai/i.test(page.url())) {
  if (authWaitMs > 0) {
    console.error(`Authentication required. Complete sign-in in the opened browser window within ${Math.round(authWaitMs / 1000)} seconds...`);
    const deadline = Date.now() + authWaitMs;
    while (Date.now() < deadline && /accounts\.google\.com|login\.genspark\.ai/i.test(page.url())) {
      await page.waitForTimeout(3000);
    }
  }
  if (/accounts\.google\.com|login\.genspark\.ai/i.test(page.url())) {
    if (context) await context.close();
    if (browser) await browser.close();
    throw new Error("Genspark viewer requires sign-in. Re-run with --headed --user-data-dir <profile-dir> --auth-wait-ms 300000, complete sign-in once, then rerun capture with the same profile.");
  }
}

const view = page.getByRole("button", { name: "View" });
if ((await view.count().catch(() => 0)) === 1) {
  await view.click();
}

await page.waitForTimeout(waitMs);

if (seen.size === 0) {
  const openArtifact = page.getByText("Click to open", { exact: true });
  if ((await openArtifact.count().catch(() => 0)) >= 1) {
    await openArtifact.first().click();
    await page.waitForTimeout(5000);
  }
}

if (minSlides > 1 && seen.size < minSlides) {
  for (let i = 0; i < minSlides + 4; i += 1) {
    await page.keyboard.press("ArrowRight").catch(() => {});
    await page.waitForTimeout(900);
  }
}

for (let i = 0; i < scrollPasses; i += 1) {
  try {
    await page.evaluate(() => {
      window.scrollBy(0, Math.max(400, window.innerHeight * 0.8));
      for (const el of document.querySelectorAll("*")) {
        const element = /** @type {HTMLElement} */ (el);
        if (element.scrollHeight > element.clientHeight + 20) {
          element.scrollTop = Math.min(element.scrollTop + Math.max(400, element.clientHeight * 0.8), element.scrollHeight);
        }
        if (element.scrollWidth > element.clientWidth + 20) {
          element.scrollLeft = Math.min(element.scrollLeft + Math.max(400, element.clientWidth * 0.8), element.scrollWidth);
        }
      }
    });
  } catch (err) {
    if (!String(err?.message || err).includes("Execution context was destroyed")) throw err;
    await page.waitForLoadState("domcontentloaded", { timeout: 30000 }).catch(() => {});
  }
  await page.waitForTimeout(1500);
}

if (seen.size === 0) {
  if (context) await context.close();
  if (browser) await browser.close();
  throw new Error("No /api/files/s slide endpoints were observed. Open the viewer manually or confirm the deck is public.");
}

const manifest = [];
for (const [pageIndex, item] of [...seen.entries()].sort((a, b) => a[0] - b[0])) {
  const response = await page.request.get(item.url, { timeout: 30000, maxRedirects: 5 });
  if (!response.ok()) {
    manifest.push({ pageIndex, id: item.id, url: item.url, status: response.status(), saved: false });
    continue;
  }
  const text = await response.text();
  const slideNo = String(pageIndex + 1).padStart(2, "0");
  const file = path.join(htmlDir, `slide-${slideNo}.html`);
  await fs.writeFile(file, text, "utf8");
  manifest.push({ pageIndex, id: item.id, url: item.url, status: response.status(), file, saved: true, bytes: Buffer.byteLength(text) });
}

await fs.writeFile(path.join(out, "manifest.json"), JSON.stringify(manifest, null, 2), "utf8");
if (context) await context.close();
if (browser) await browser.close();

const saved = manifest.filter(x => x.saved).length;
console.log(`Captured ${saved}/${manifest.length} Genspark slides into ${htmlDir}`);
console.log(path.join(out, "manifest.json"));

if (Number.isFinite(minSlides) && minSlides > 0 && saved < minSlides) {
  throw new Error(`Captured ${saved} slides, below requested minimum ${minSlides}. Retry Genspark expansion or use Presentations for full-count rebuild.`);
}
