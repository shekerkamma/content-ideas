// check_layout_overflow.mjs — LAYOUT GATE. Measures what the eye misses.
//
//   node check_layout_overflow.mjs --deck <deck.html> [--chrome <path>] [--min 20]
//
// Reports, per slide:
//   overflow  — a text box whose content is taller than its declared height.
//               With absolutely positioned boxes the excess does not clip, it
//               prints ON TOP of whatever sits below (classically: a two-line
//               title over its own subtitle).
//   collide   — two text boxes whose rectangles intersect.
//
// Not every hit is a defect. Deliberately layered design (a label over a bar, a
// row label beside a right-aligned value) shows up as `collide` and is fine.
// `overflow` above ~20px is almost always real. Triage against the render;
// this tool tells you WHERE to look, it does not decide for you.
//
// Exit 0 always — this is a report, not a hard gate. The hard gates are
// check_export_coverage.mjs and OfficeCLI.
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";

function arg(n, d) { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; }
const deck = path.resolve(arg("deck", "deck.html"));
const chrome = arg("chrome", process.env.CHROME_PATH || undefined);
const MIN = parseInt(arg("min", "8"), 10);

const browser = await chromium.launch({ headless: true, ...(chrome ? { executablePath: chrome } : {}) });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 60000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 30000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });
const total = await page.evaluate(() => window.__deck.total);

let nOver = 0, nColl = 0;
const lines = [];

for (let i = 0; i < total; i++) {
  await page.evaluate(k => window.__deck.show(k), i);
  await page.waitForTimeout(100);
  const hits = await page.evaluate((MIN) => {
    const slide = [...document.querySelectorAll(".slide")].find(s => s.classList.contains("render-static"));
    if (!slide) return [];
    // absolutely positioned text nodes: the source deck's own object model,
    // falling back to any positioned element that holds text
    let els = [...slide.querySelectorAll('[data-object-type="textbox"]')];
    if (!els.length) {
      els = [...slide.querySelectorAll("*")].filter(e => {
        const cs = getComputedStyle(e);
        return cs.position === "absolute" && e.textContent.trim();
      });
    }
    const boxes = els.map(e => {
      const r = e.getBoundingClientRect();
      return { t: (e.innerText || "").trim().replace(/\s+/g, " ").slice(0, 48),
               x: r.left, y: r.top, w: r.width, h: r.height,
               sh: e.scrollHeight, ch: e.clientHeight };
    });
    const out = [];
    for (const b of boxes) if (b.sh > b.ch + 2) out.push({ kind: "overflow", a: b.t, by: b.sh - b.ch });
    for (let a = 0; a < boxes.length; a++) for (let b = a + 1; b < boxes.length; b++) {
      const A = boxes[a], B = boxes[b];
      const ox = Math.min(A.x + A.w, B.x + B.w) - Math.max(A.x, B.x);
      const oy = Math.min(A.y + A.h, B.y + B.h) - Math.max(A.y, B.y);
      if (ox > MIN && oy > MIN) out.push({ kind: "collide", a: A.t, b: B.t, ox: Math.round(ox), oy: Math.round(oy) });
    }
    return out;
  }, MIN);

  const ov = hits.filter(h => h.kind === "overflow");
  const co = hits.filter(h => h.kind === "collide");
  nOver += ov.length; nColl += co.length;
  if (hits.length) {
    lines.push(`  slide ${String(i + 1).padStart(2, "0")}: ${ov.length} overflow, ${co.length} collide`);
    for (const h of ov.slice(0, 3)) lines.push(`       overflow +${h.by}px  "${h.a}"`);
    for (const h of co.slice(0, 2)) lines.push(`       collide ${h.ox}x${h.oy}px  "${h.a}" <> "${h.b}"`);
  }
}
await browser.close();

console.log(`LAYOUT REPORT: ${total} slides — ${nOver} overflowing box(es), ${nColl} collision(s).`);
if (lines.length) console.log(lines.join("\n"));
else console.log("  clean.");
console.log("\nTriage: overflow >20px is almost always a real collision (fixed-height title");
console.log("boxes are the usual cause). Layered-by-design overlaps report as `collide`.");
