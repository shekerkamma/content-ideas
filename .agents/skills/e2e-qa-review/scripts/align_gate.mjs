// Heading-alignment gate: one axis per page. Every visible h1/h2 in the page body (not nav, footer or
// related-links blocks), on every route, at every width. A page FAILS when its headings use mixed axes: some
// centred (text-align: center) while others start at the left. A consistently centred page passes, so this
// encodes consistency, not taste. Left-aligned headings whose text starts well right of the page's content
// edge are listed as info (on DeepGrid v10 all 29 were headings inside cards or the text column of an
// image-and-text row, which is where they belong).
//
// Written after a user saw section titles jump between centred and left on every page (v10, 2026-10-04):
// two reviewers had flagged it and the orchestrator graded it contradicted, because a rule existed that only
// the author could see. Measured on that site: 258 of 594 headings centred or off the edge before the fix, 0
// centred after.
//
// Usage: node align_gate.mjs <config.json>   config: { base, routes, widths?: [[w,h,label]], out? }
//   exit 0 clean, 2 findings, 1 blocked. Reuses sweep.json (base, routes, widths).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';

const blocked = (m) => { console.error('BLOCKED: ' + m); process.exit(1); };
const cfgPath = process.argv[2]; if (!cfgPath || !fs.existsSync(cfgPath)) blocked('usage: node align_gate.mjs <config.json>');
const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
if (!cfg.base || !Array.isArray(cfg.routes) || !cfg.routes.length) blocked('config needs base and a non-empty routes list');
const BASE = cfg.base.endsWith('/') ? cfg.base : cfg.base + '/';
const widths = (cfg.widths || [[1440, 900, 'desktop'], [390, 844, 'phone']]).map((w) => Array.isArray(w) ? w : [w.width, w.height, w.label]);

// playwright from the project first, then $E2E_QA_NODE_MODULES, then this skill's repo (as sweep.mjs does).
let chromium;
for (const base of [process.cwd(), process.env.E2E_QA_NODE_MODULES, path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..')].filter(Boolean)) {
  try { ({ chromium } = createRequire(path.join(base, 'noop.js'))('playwright')); break; } catch {}
}
if (!chromium) blocked('playwright not found in the project, $E2E_QA_NODE_MODULES or the skill repo');

const browser = await chromium.launch();
const failures = [], info = []; let headings = 0, pages = 0;
for (const [w, h, label] of widths) {
  const pg = await browser.newPage({ viewport: { width: w, height: h }, reducedMotion: 'reduce' });
  for (const route of cfg.routes) {
    const res = await pg.goto(BASE + route, { waitUntil: 'networkidle' }).catch(() => null);
    if (!res || res.status() >= 400) continue;          // the sweep owns status; a 404 route has nothing to align
    pages++;
    const rows = await pg.evaluate(() => {
      const root = document.querySelector('main') || document.body;
      const hs = [...root.querySelectorAll('h1, h2')].filter((e) => {
        const b = e.getBoundingClientRect();
        return b.width > 0 && b.height > 0 && getComputedStyle(e).visibility !== 'hidden' && !e.closest('nav, footer, [class*="related"], .sr-only');
      });
      const edge = hs.length ? Math.min(...hs.map((e) => e.getBoundingClientRect().left)) : 0;
      return hs.map((e) => {
        const r = document.createRange(); r.selectNodeContents(e); const t = r.getBoundingClientRect();
        return { tag: e.tagName, text: e.innerText.replace(/\s+/g, ' ').slice(0, 60), align: getComputedStyle(e).textAlign, off: Math.round(t.left - edge) };
      });
    });
    headings += rows.length;
    const centred = rows.filter((x) => x.align === 'center'), left = rows.filter((x) => x.align !== 'center' && x.align !== 'right');
    if (centred.length && left.length)
      failures.push({ width: label, route: '/' + route, centred: centred.map((x) => `${x.tag} "${x.text}"`), left: left.length });
    for (const x of left) if (x.off > 40) info.push(`${label} /${route} ${x.tag} "${x.text}" starts ${x.off}px right of the content edge`);
  }
  await pg.close();
}
await browser.close();
if (!pages) blocked(`no route at ${BASE} answered below 400`);

const out = { base: BASE, pages, headings, failures, info };
if (cfg.out) fs.writeFileSync(cfg.out, JSON.stringify(out, null, 1));
console.log(`align gate: ${headings} headings on ${pages} page loads; ${failures.length} page(s) mix centred and left headings; ${info.length} off-edge (info)`);
for (const f of failures) console.log(`  FAIL ${f.width} ${f.route}: centred ${f.centred.join('; ')} beside ${f.left} left-aligned`);
process.exit(failures.length ? 2 : 0);
