// render_hybrid.mjs — for EDITABLE output.
// Per slide: (a) capture every text block's bbox + runs (color/bold) + font/align,
// (b) render a text-free background PNG (design kept, glyphs hidden).
// build_editable_pptx.py then overlays native PPT text boxes at those coords.
//
//   node render_hybrid.mjs --deck <deck.html> --out <dir>
//     -> <dir>/bg/slide-XX.png   (text-free background, 2560x1440)
//     -> <dir>/pos/slide-XX.json  (text boxes for that slide)
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs/promises";

function arg(n, d) { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; }
const deck = path.resolve(arg("deck", "deck.html"));
const out = path.resolve(arg("out", path.join(path.dirname(deck), "build")));
const chrome = arg("chrome", process.env.CHROME_PATH || "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe");
const bgDir = path.join(out, "bg"), posDir = path.join(out, "pos");
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

await fs.mkdir(bgDir, { recursive: true }); await fs.mkdir(posDir, { recursive: true });

const browser = await chromium.launch({ headless: true, executablePath: chrome });
const stage = await detectStage(browser, pathToFileURL(deck).href, arg("stage", null));
const ctx = await browser.newContext({ viewport: { width: stage.w, height: stage.h },
  deviceScaleFactor: 2560 / stage.w });   // always exports 2560x1440
const page = await ctx.newPage();
await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 30000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 15000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });
const total = await page.evaluate(() => window.__deck.total);

// capture-runs helper injected into page context
const CAPTURE = () => {
  const slide = document.querySelector(".slide.render-static");
  const INLINE = new Set(["SPAN", "STRONG", "B", "EM", "I", "A", "SMALL", "MARK"]);
  const boxes = [];
  // lines = array of runs-arrays; a <br> starts a new line.
  //
  // `pre` = the box is preformatted (white-space: pre/pre-wrap/pre-line, i.e. a
  // <pre> code block, file tree or ASCII diagram). There, newlines ARE line
  // breaks and runs of spaces ARE alignment. Collapsing them — the default for
  // prose — turns a directory tree into one wrapped paragraph in the PPTX while
  // the PNG still looks perfect.
  const walkLines = (el, lines, pre) => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3) {
        const cs = getComputedStyle(el);
        const run = (text) => lines[lines.length - 1].push(
          { text, color: cs.color, bold: parseInt(cs.fontWeight) >= 600 });
        if (pre) {
          const parts = n.textContent.split("\n");   // real newlines = real lines
          parts.forEach((part, i) => {
            if (i > 0) lines.push([]);
            if (part.length) run(part);               // keep every space: it is alignment
          });
        } else {
          const t = n.textContent.replace(/\s+/g, " ");
          if (t.trim() || t === " ") run(t);
        }
      } else if (n.nodeType === 1) {
        if (n.tagName === "BR") lines.push([]);
        else if (INLINE.has(n.tagName)) walkLines(n, lines, pre);
        // block child: skip — it's its own box
      }
    }
  };
  const all = slide.querySelectorAll("*");
  for (const el of all) {
    if (el.classList && el.classList.contains("num")) continue;
    if (["STRONG", "B", "EM", "I", "A", "SMALL", "MARK"].includes(el.tagName)) continue;
    const cs = getComputedStyle(el);
    if (cs.display === "inline") continue;   // pure-inline nodes are runs of their block, not boxes
    // A text box is any element that HOLDS text but contains no block-level
    // child that itself holds text ("text leaf block").
    //
    // This deliberately does NOT require a direct text node. Requiring one
    // silently dropped every box whose text lives entirely inside inline tags,
    // e.g. <div><b>Label</b><br><span>caption</span></div> — a very common
    // authoring pattern. Whole table columns disappeared from the exported
    // PPTX while rendering perfectly in the PNG, and OfficeCLI could not see
    // it because the surviving shapes were all in-bounds. Verify with
    // check_export_coverage.mjs, never by eye alone.
    if (!el.textContent.trim()) continue;
    const hasBlockKid = [...el.children].some(c => {
      const d = getComputedStyle(c).display;
      return d !== "inline" && d !== "none" && c.textContent.trim();
    });
    if (hasBlockKid) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const isPre = /^pre/.test(cs.whiteSpace);
    const lines = [[]];
    walkLines(el, lines, isPre);
    // a blank line inside a <pre> is meaningful vertical space; elsewhere it is noise
    const clean = isPre ? lines.slice(0, lines.length - (lines[lines.length-1].length ? 0 : 1))
                        : lines.filter(ln => ln.length);
    if (!clean.length) continue;
    if (cs.textTransform === "uppercase") clean.forEach(ln => ln.forEach(x => x.text = x.text.toUpperCase()));
    const gutter = el.tagName === "LI" ? 22 : 0;
    boxes.push({
      x: r.left + gutter, y: r.top, w: Math.max(2, r.width - gutter), h: r.height,
      fontPx: parseFloat(cs.fontSize),
      lh: (parseFloat(cs.lineHeight) / parseFloat(cs.fontSize)) || 1.2,
      // absolute line box in px. CSS line-height is a multiple of FONT SIZE;
      // PowerPoint's float line_spacing is a multiple of SINGLE LINE SPACING
      // (~1.2x font size). Passing the CSS ratio through over-spaces every
      // paragraph by ~20% and pushes long blocks out of their box.
      lhPx: parseFloat(cs.lineHeight) || (parseFloat(cs.fontSize) * 1.2),
      align: cs.textAlign === "center" ? "center" : cs.textAlign === "right" ? "right" : "left",
      pre: isPre,
      mono: /mono|consol|menlo|courier|sf mono|jetbrains|cascadia|roboto mono/i.test(cs.fontFamily),
      // Carry the deck's ACTUAL typography into the PPTX. Without this the
      // builder falls back to Segoe UI / Consolas and the source's type
      // identity is silently lost. `family` is the first declared family with
      // quotes stripped; `role` is a coarse fallback if that name is unusable.
      family: (cs.fontFamily || "").split(",")[0].replace(/["']/g, "").trim(),
      role: /mono|consol|menlo|courier/i.test(cs.fontFamily) ? "mono"
          : parseInt(cs.fontWeight) >= 600 ? "display" : "body",
      lines: clean,
    });
  }
  return boxes;
};

for (let i = 0; i < total; i++) {
  await page.evaluate((k) => window.__deck.show(k), i);
  await page.waitForTimeout(300);
  const boxes = await page.evaluate(CAPTURE);
  await fs.writeFile(path.join(posDir, `slide-${String(i + 1).padStart(2, "0")}.json`), JSON.stringify(boxes));
  // text-free background
  await page.evaluate(() => document.body.classList.add("export-bg"));
  await page.waitForTimeout(120);
  await page.screenshot({ path: path.join(bgDir, `slide-${String(i + 1).padStart(2, "0")}.png`) });
  await page.evaluate(() => document.body.classList.remove("export-bg"));
  console.log(`slide ${i + 1}: ${boxes.length} text boxes`);
}
await browser.close();
console.log(`DONE: ${total} slides @ ${stage.w}x${stage.h} stage -> bg/ + pos/`);
