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
const dohTemplate = arg("doh-template") || process.env.GENSPARK_DOH_TEMPLATE;
const hostResolverRules = arg("host-resolver-rules") || process.env.GENSPARK_HOST_RESOLVER_RULES;
const headed = hasFlag("headed");
const waitMs = Number(arg("wait-ms", "25000"));
const authWaitMs = Number(arg("auth-wait-ms", "0"));
const minSlides = Number(arg("min-slides", "0"));
const scrollPasses = Number(arg("scroll-passes", "8"));

function classifyViewerText(text) {
  const body = String(text || "");
  const explicitCreditError = /(?:insufficient|not enough|out of|exceeded|exhausted).{0,40}(?:credit|quota)|(?:credit|quota).{0,40}(?:limit|exceeded|exhausted)|upgrade.{0,40}(?:credit|plan)/i.test(body);
  const generating = /tasks? remaining|in progress|continue building|continue creating|editing (?:slide|page)|blank placeholders?|queued|generating/i.test(body);
  const completed = /all tasks? (?:are )?complete|presentation (?:is )?ready|finished building|completed presentation/i.test(body);
  const declaredSlides = body.match(/(?:you have|created|presentation (?:has|contains))\s+(\d+)\s+slides?/i);
  return {
    hostedStatus: explicitCreditError ? "blocked_credit_limit" : generating && !completed ? "generating" : completed ? "completed" : "unknown",
    explicitCreditError,
    declaredSlideCount: declaredSlides ? Number(declaredSlides[1]) : null,
  };
}

if (!url || !out) {
  console.error("Usage: node capture_genspark_slides.mjs --url <genspark-url> --out <output-dir> [--chrome <path>] [--headed] [--doh-template <url>] [--host-resolver-rules <rules>]");
  process.exit(2);
}

const htmlDir = path.join(out, "html");
await fs.mkdir(htmlDir, { recursive: true });

const { chromium } = require("playwright");
const launchOptions = { headless: !headed };
if (chrome) launchOptions.executablePath = chrome;
const browserArgs = [];
if (dohTemplate) {
  browserArgs.push(
    "--dns-over-https-mode=secure",
    `--dns-over-https-templates=${dohTemplate}`,
  );
}
if (hostResolverRules) browserArgs.push(`--host-resolver-rules=${hostResolverRules}`);
if (browserArgs.length) launchOptions.args = browserArgs;

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
const networkUrls = new Set();
const responses = [];
const consoleMessages = [];
const pageErrors = [];

function collect(rawUrl) {
  if (networkUrls.size < 1000) networkUrls.add(rawUrl);
  if (!rawUrl.includes("/api/files/s/")) return;
  const u = new URL(rawUrl);
  const match = u.pathname.match(/\/api\/files\/s\/([^/]+)/);
  const pageIndex = Number(u.searchParams.get("pageIndex"));
  if (!match || !Number.isFinite(pageIndex)) return;
  u.searchParams.set("scale", "1");
  seen.set(pageIndex, { id: match[1], url: u.toString() });
}

page.on("request", req => collect(req.url()));
page.on("response", res => {
  collect(res.url());
  if (responses.length < 1000) responses.push({ url: res.url(), status: res.status() });
});
page.on("console", msg => {
  if (consoleMessages.length < 200) consoleMessages.push({ type: msg.type(), text: msg.text() });
});
page.on("pageerror", err => {
  if (pageErrors.length < 100) pageErrors.push(String(err?.stack || err));
});

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
  const bodyText = await page.locator("body").innerText().catch(() => "");
  const classification = classifyViewerText(bodyText);
  const diagnostic = {
    url: page.url(),
    title: await page.title().catch(() => ""),
    text: bodyText,
    classification,
    networkUrls: [...networkUrls],
    responses,
    consoleMessages,
    pageErrors,
  };
  await fs.writeFile(path.join(out, "capture-diagnostic.json"), JSON.stringify(diagnostic, null, 2), "utf8");
  await fs.writeFile(path.join(out, "capture-state.json"), JSON.stringify({
    ...classification,
    viewerUrl: page.url(),
    observedEndpointCount: 0,
    minimumSlides: minSlides,
    recoveryStatus: classification.hostedStatus === "generating" ? "generating" : "not_captured",
  }, null, 2), "utf8");
  await page.screenshot({ path: path.join(out, "capture-diagnostic.png"), fullPage: true }).catch(() => {});
  if (context) await context.close();
  if (browser) await browser.close();
  const reason = classification.hostedStatus === "generating"
    ? "The viewer still reports generation activity; wait and retry this same project."
    : classification.explicitCreditError
      ? "The viewer explicitly reports a credit/quota blocker."
      : "No explicit generation or credit state was proven.";
  throw new Error(`No /api/files/s slide endpoints were observed. ${reason} Inspect ${path.join(out, "capture-diagnostic.json")} and capture-diagnostic.png.`);
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
const viewerText = await page.locator("body").innerText().catch(() => "");
const classification = classifyViewerText(viewerText);
const viewerState = {
  url: page.url(),
  title: await page.title().catch(() => ""),
  text: viewerText,
  classification,
};
await fs.writeFile(path.join(out, "viewer-state.json"), JSON.stringify(viewerState, null, 2), "utf8");
await fs.writeFile(path.join(out, "capture-state.json"), JSON.stringify({
  ...classification,
  viewerUrl: page.url(),
  observedEndpointCount: manifest.length,
  capturedSlideCount: manifest.filter(item => item.saved).length,
  minimumSlides: minSlides,
  recoveryStatus: manifest.every(item => item.saved) ? "captured" : "partial",
}, null, 2), "utf8");
await page.screenshot({ path: path.join(out, "viewer-state.png"), fullPage: true }).catch(() => {});
if (context) await context.close();
if (browser) await browser.close();

const saved = manifest.filter(x => x.saved).length;
console.log(`Captured ${saved}/${manifest.length} Genspark slides into ${htmlDir}`);
console.log(path.join(out, "manifest.json"));

if (Number.isFinite(minSlides) && minSlides > 0 && saved < minSlides) {
  throw new Error(`Captured ${saved} slides, below evidence-derived minimum ${minSlides}. Update the same Genspark project and expand until the coverage matrix is complete.`);
}
