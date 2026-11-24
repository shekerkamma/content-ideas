// Render each .slide of a carousel HTML to slide-NN.png at 2x (2160x2700).
// Refuses to render while a [[placeholder]] from the template is left in the page.
// The PDF is built separately from these PNGs by build_pdf.mjs.
// Usage: node render.mjs <carousel.html> <outdir>
import fs from 'fs';
import path from 'path';
import { loadPlaywright } from './playwright.mjs';

const [html, out] = process.argv.slice(2);
if (!html || !out) { console.error('usage: node render.mjs <carousel.html> <outdir>'); process.exit(2); }
const src = fs.readFileSync(html, 'utf8');
const left = src.match(/\[\[[^\]]*\]\]/g);
if (left) { console.error(`unfilled placeholders (${left.length}): ${[...new Set(left)].slice(0, 5).join(' ')}`); process.exit(3); }

const { chromium } = loadPlaywright();
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1350 }, deviceScaleFactor: 2 });
await page.goto('file://' + path.resolve(html));
await page.evaluate(() => document.fonts.ready);
const slides = await page.$$('.slide');
for (const f of fs.readdirSync(out).filter(f => /^slide-\d+\.png$/.test(f))) fs.unlinkSync(path.join(out, f));
for (let i = 0; i < slides.length; i++) {
  await slides[i].screenshot({ path: path.join(out, `slide-${String(i + 1).padStart(2, '0')}.png`) });
}
console.log(`rendered ${slides.length} slides to ${out}`);
await browser.close();
