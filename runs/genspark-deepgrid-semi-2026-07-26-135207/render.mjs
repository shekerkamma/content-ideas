// render.mjs — deck HTML -> one 2560x1440 PNG per slide (Genspark export res)
// Run with Windows node (Playwright + system Chrome). No Genspark, no auth, no credits.
//
//   node render.mjs --deck <deck.html> --out <png-dir> [--chrome <chrome.exe>]
//
// The deck HTML must link theme.css + deck.css and expose window.__deck
// ({ total, fitOne(), show(i) }). See assets/deck.example.html.
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";

function arg(n, d) { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; }

const deck = path.resolve(arg("deck", "deck.html"));
const out = path.resolve(arg("out", path.join(path.dirname(deck), "build", "png")));
const chrome = arg("chrome", process.env.CHROME_PATH || "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe");

await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless: false, executablePath: chrome, args: ['--no-sandbox'] });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 30000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 15000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });

const total = await page.evaluate(() => window.__deck.total);
for (let i = 0; i < total; i++) {
  await page.evaluate((k) => window.__deck.show(k), i);
  await page.waitForTimeout(350);
  const file = path.join(out, `slide-${String(i + 1).padStart(2, "0")}.png`);
  await page.screenshot({ path: file });   // 1280x720 * dsf2 = 2560x1440
  console.log("rendered " + path.basename(file));
}
await browser.close();
console.log(`DONE: ${total} slides -> ${out}`);
