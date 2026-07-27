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
await fs.mkdir(bgDir, { recursive: true }); await fs.mkdir(posDir, { recursive: true });

const browser = await chromium.launch({ headless: true, executablePath: chrome });
const ctx = await browser.newContext({ viewport: { width: 1280, height: 720 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();
await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 30000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 15000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });
const total = await page.evaluate(() => window.__deck.total);

// capture-runs helper injected into page context
const CAPTURE = () => {
  const slide = Array.from(document.querySelectorAll(".slide")).find(s => s.style.display !== "none") || document.querySelector(".slide");
  const INLINE = new Set(["SPAN", "STRONG", "B", "EM", "I", "A", "SMALL", "MARK"]);
  const boxes = [];
  const hasDirectText = (el) => [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  // lines = array of runs-arrays; a <br> starts a new line
  const walkLines = (el, lines) => {
    for (const n of el.childNodes) {
      if (n.nodeType === 3) {
        const t = n.textContent.replace(/\s+/g, " ");
        if (t.trim() || t === " ") {
          const cs = getComputedStyle(el);
          lines[lines.length - 1].push({ text: t, color: cs.color, bold: parseInt(cs.fontWeight) >= 600 });
        }
      } else if (n.nodeType === 1) {
        if (n.tagName === "BR") lines.push([]);
        else if (INLINE.has(n.tagName)) walkLines(n, lines);
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
    if (!hasDirectText(el)) continue;
    const r = el.getBoundingClientRect();
    if (r.width < 2 || r.height < 2) continue;
    const lines = [[]];
    walkLines(el, lines);
    const clean = lines.filter(ln => ln.length);
    if (!clean.length) continue;
    if (cs.textTransform === "uppercase") clean.forEach(ln => ln.forEach(x => x.text = x.text.toUpperCase()));
    const gutter = el.tagName === "LI" ? 22 : 0;
    boxes.push({
      x: r.left + gutter, y: r.top, w: Math.max(2, r.width - gutter), h: r.height,
      fontPx: parseFloat(cs.fontSize),
      lh: (parseFloat(cs.lineHeight) / parseFloat(cs.fontSize)) || 1.2,
      align: cs.textAlign === "center" ? "center" : cs.textAlign === "right" ? "right" : "left",
      mono: /mono|consol|menlo|courier|sf mono|jetbrains|cascadia|roboto mono/i.test(cs.fontFamily),
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
console.log(`DONE: ${total} slides -> bg/ + pos/`);
