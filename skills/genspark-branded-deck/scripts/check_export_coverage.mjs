// check_export_coverage.mjs — EXPORT FIDELITY GATE for the hybrid path.
//
// Proves that every visible string in the deck survived into the captured text
// boxes. Run it after render_hybrid.mjs and before build_editable_pptx.py.
//
//   node check_export_coverage.mjs --deck <deck.html> --pos <build/pos> [--chrome <path>]
//
// Exit 0 = every visible string is present. Exit 1 = text was dropped.
//
// WHY THIS EXISTS
// The hybrid export decides what is a "text box" by walking the DOM. Any bug in
// that predicate silently deletes content: the PNG render still looks perfect
// (it is a real browser screenshot) and OfficeCLI still reports issues=0 (the
// surviving shapes are all in-bounds). The only way to catch it is to diff the
// DOM's visible text against the capture. A real instance dropped entire table
// columns across 36 of 37 slides and shipped, because both other gates passed.
//
// Comparison is case-insensitive: `text-transform:uppercase` legitimately makes
// the capture differ from the DOM, and treating that as a loss buries real ones.
import { chromium } from "playwright";
import { pathToFileURL } from "node:url";
import path from "node:path";
import fs from "node:fs";

function arg(n, d) { const i = process.argv.indexOf(`--${n}`); return i >= 0 ? process.argv[i + 1] : d; }
const deck = path.resolve(arg("deck", "deck.html"));
const posDir = path.resolve(arg("pos", path.join(path.dirname(deck), "build", "pos")));
const chrome = arg("chrome", process.env.CHROME_PATH || undefined);
const norm = s => s.replace(/\s+/g, " ").trim().toLowerCase();

const browser = await chromium.launch({ headless: true, ...(chrome ? { executablePath: chrome } : {}) });
const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 } })).newPage();
await page.goto(pathToFileURL(deck).href, { waitUntil: "networkidle", timeout: 60000 });
await page.waitForFunction(() => window.__deck && window.__deck.total > 0, { timeout: 30000 });
await page.evaluate(() => { document.body.classList.add("export-mode"); window.__deck.fitOne(); });
const total = await page.evaluate(() => window.__deck.total);

let missingTotal = 0;
const report = [];

for (let i = 0; i < total; i++) {
  await page.evaluate(k => window.__deck.show(k), i);
  await page.waitForTimeout(90);

  // every rendered, visible text node on the active slide
  const domTexts = await page.evaluate(() => {
    const slide = [...document.querySelectorAll(".slide")].find(s => s.classList.contains("render-static"));
    if (!slide) return [];
    const out = [];
    const walk = document.createTreeWalker(slide, NodeFilter.SHOW_TEXT, {
      acceptNode(n) {
        const el = n.parentElement;
        if (!el) return NodeFilter.FILTER_REJECT;
        const tag = el.tagName;
        if (tag === "STYLE" || tag === "SCRIPT" || tag === "TITLE" || tag === "HEAD")
          return NodeFilter.FILTER_REJECT;
        const r = el.getBoundingClientRect();
        if (r.width < 1 || r.height < 1) return NodeFilter.FILTER_REJECT;
        const cs = getComputedStyle(el);
        if (cs.visibility === "hidden" || cs.display === "none") return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      },
    });
    let n;
    while ((n = walk.nextNode())) { const t = n.textContent.replace(/\s+/g, " ").trim(); if (t) out.push(t); }
    return out;
  });

  const posFile = path.join(posDir, `slide-${String(i + 1).padStart(2, "0")}.json`);
  if (!fs.existsSync(posFile)) {
    report.push({ slide: i + 1, error: "no pos/ file — run render_hybrid.mjs first" });
    missingTotal += domTexts.length;
    continue;
  }
  const boxes = JSON.parse(fs.readFileSync(posFile, "utf8"));
  const captured = norm(boxes.map(b => b.lines.map(l => l.map(r => r.text).join("")).join(" ")).join(" "));

  const missing = domTexts.filter(t => t.length > 2 && !captured.includes(norm(t)));
  if (missing.length) { missingTotal += missing.length; report.push({ slide: i + 1, missing }); }
}

await browser.close();

if (missingTotal === 0) {
  console.log(`EXPORT COVERAGE OK: ${total} slides, every visible string captured.`);
  process.exit(0);
}
console.error(`EXPORT COVERAGE FAILED: ${missingTotal} visible strings dropped across ${report.length} slide(s).`);
for (const r of report) {
  if (r.error) { console.error(`  slide ${String(r.slide).padStart(2, "0")}: ${r.error}`); continue; }
  console.error(`  slide ${String(r.slide).padStart(2, "0")}: ${r.missing.length} missing`);
  for (const m of r.missing.slice(0, 4)) console.error(`       - ${m.slice(0, 100)}`);
}
console.error("\nUsually a capture-predicate bug in render_hybrid.mjs. Do not ship: the PNG will");
console.error("look correct and OfficeCLI will report 0 issues while the PPTX is missing content.");
process.exit(1);
