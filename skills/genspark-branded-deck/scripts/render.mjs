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

// Stage size is READ FROM THE DECK, not assumed. This skill's own template is a
// 1280x720 stage; a recovered Genspark deck is 1920x1080. Hardcoding 1280 means a
// 1920 deck silently renders only its top-left 66.7% — every PNG looks plausible,
// the count and 2560x1440 dimensions are right, and whole columns are simply gone.
// Override with --stage <cssWidth> only if auto-detection fails.
async function detectStage(browser, deckUrl, override) {
  if (override) { const w = parseInt(override, 10); return { w, h: Math.round(w * 9 / 16) }; }
  const probeCtx = await browser.newContext({ viewport: { width: 1920, height: 1080 } });
  const probe = await probeCtx.newPage();
  try {
    await probe.goto(deckUrl, { waitUntil: "domcontentloaded", timeout: 30000 });
    await probe.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 20000 });
    const s = await probe.evaluate(() => {
      const el = document.getElementById("stage") || document.querySelector(".stage");
      if (!el) return null;
      const cs = getComputedStyle(el);
      return { w: Math.round(parseFloat(cs.width)), h: Math.round(parseFloat(cs.height)) };
    });
    if (s && s.w > 0) return s;
  } catch (e) { /* fall through to default */ }
  finally { await probeCtx.close(); }
  return { w: 1280, h: 720 };
}

await fs.mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless: true, executablePath: chrome });
const stage = await detectStage(browser, pathToFileURL(deck).href, arg("stage", null));
const ctx = await browser.newContext({ viewport: { width: stage.w, height: stage.h },
  deviceScaleFactor: 2560 / stage.w });   // always exports 2560x1440
const page = await ctx.newPage();

await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 30000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 15000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });

const total = await page.evaluate(() => window.__deck.total);
for (let i = 0; i < total; i++) {
  await page.evaluate((k) => window.__deck.show(k), i);
  await page.waitForTimeout(350);
  const file = path.join(out, `slide-${String(i + 1).padStart(2, "0")}.png`);
  await page.screenshot({ path: file });   // stage * dsf = 2560x1440
  console.log("rendered " + path.basename(file));
}
await browser.close();
console.log(`DONE: ${total} slides @ ${stage.w}x${stage.h} stage -> ${out}`);
