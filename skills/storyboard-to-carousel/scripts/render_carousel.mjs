#!/usr/bin/env node
// Render an authored carousel at 1080x1350 in the DeepGrid Semi design system: PNG per slide plus one PDF
// (LinkedIn takes a carousel as a document). Beat slides show the real draw.io SVG cropped to the beat's
// zones, the rest dimmed, a copper frame on the zones. Blocks on a font that did not load and on any
// text box whose content overflows it: a clipped line passes every visual skim at thumbnail size.
//
// Usage: node render_carousel.mjs <run-dir> --svg <diagram.svg> --ds <design-system-dir> [--wordmark <png>]
// Reads <run>/carousel.json and <run>/zones.json; writes <run>/out/<part>-NN.png and <run>/out/<part>-carousel.pdf
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const args = process.argv.slice(2), run = path.resolve(args[0]);
const opt = k => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : undefined; };
const W = 1080, H = 1350, M = 80;
let chromium;
for (const base of [process.cwd(), path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..')]) {
  try { ({chromium} = createRequire(path.join(base, 'x.js'))('playwright')); break; } catch {}
}
if (!chromium) { console.error('BLOCKED: playwright not resolvable'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(path.join(run, 'carousel.json'), 'utf8'));
const zones = JSON.parse(fs.readFileSync(path.join(run, 'zones.json'), 'utf8'));
const ds = opt('--ds'), tokens = JSON.parse(fs.readFileSync(path.join(ds, 'tokens.json'), 'utf8'));
const col = Object.fromEntries(tokens.color.tokens.map(t => [t.name, typeof t.value === 'string' ? t.value : t.value.ink]));
const faces = tokens.type.fonts.map(f => `@font-face{font-family:'${f.family}';src:url(data:font/woff2;base64,${fs.readFileSync(path.join(ds, f.file)).toString('base64')}) format('woff2');font-weight:${f.weight};font-style:${f.style}}`).join('');
const svg = fs.readFileSync(opt('--svg'), 'utf8').replace(/^[\s\S]*?(<svg)/, '$1').replace(/<svg /, '<svg class="d" ');
const mark = opt('--wordmark') ? `data:image/png;base64,${fs.readFileSync(opt('--wordmark')).toString('base64')}` : '';
const curly = t => t.replace(/(^|[\s(])"/g, '$1“').replace(/"/g, '”').replace(/(\w)'(\w)/g, '$1’$2').replace(/'/g, '’');
const esc = t => curly(t).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const ZW = zones.width, ZH = zones.height, DW = W - 2 * M, DH = 660;   // 560 left ~250 px empty under the body and shrank two-zone beats

function crop(sl) {   // camera rect in SVG units with the card's aspect, as in the explainer film
  const a = DW / DH;
  if (!sl.zones.length) { const w = Math.max(ZW, ZH * a) * 1.02; return {x: ZW / 2 - w / 2, y: ZH / 2 - w / a / 2, w, h: w / a}; }
  const b = sl.zones.map(n => zones.zones[n]);
  let x0 = Math.min(...b.map(z => z.x)) - 36, y0 = Math.min(...b.map(z => z.y)) - 36, x1 = Math.max(...b.map(z => z.x + z.w)) + 36, y1 = Math.max(...b.map(z => z.y + z.h)) + 36;
  let w = x1 - x0, h = y1 - y0; if (w / h > a) h = w / a; else w = h * a;
  // keep the crop inside the diagram where it fits, so no blank paper shows past its edge
  const fit = (p, len, max) => len >= max ? (max - len) / 2 : Math.min(Math.max(p, 0), max - len);
  return {x: fit((x0 + x1) / 2 - w / 2, w, ZW), y: fit((y0 + y1) / 2 - h / 2, h, ZH), w, h};
}
function diagram(sl) {
  const k = crop(sl), s = DW / k.w, zs = sl.zones.map(n => zones.zones[n]);
  const ov = zs.length ? `<path d="M-4000,-4000H${ZW + 4000}V${ZH + 4000}H-4000z${zs.map(z => `M${z.x},${z.y}h${z.w}v${z.h}h${-z.w}z`).join('')}" fill-rule="evenodd" fill="${col.ink}" opacity=".5"/>` +
    zs.map(z => `<rect x="${z.x}" y="${z.y}" width="${z.w}" height="${z.h}" rx="${6 / s}" fill="none" stroke="${col.copper}" stroke-width="${5 / s}"/>`).join('') : '';
  return `<div class="dg"><div class="st" style="transform:scale(${s}) translate(${-k.x}px,${-k.y}px)">${svg}<svg class="ov" viewBox="0 0 ${ZW} ${ZH}">${ov}</svg></div></div>`;
}
const N = c.slides.length;
const page = (sl, i) => {
  const kick = `<div class="k">${sl.marks.map(m => `<span class="disc">${m}</span>`).join('')}<span>${sl.kind === 'close' ? 'What is still unproven' : c.kicker}</span></div>`;
  const foot = `<div class="f"><span>${String(i + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')}</span>${sl.kind === 'cta' ? '' : '<span>Pre-silicon · design targets</span>'}</div>`;
  if (sl.kind === 'cover') return `<section class="p cover">${kick}<h1 class="t xl fit">${esc(sl.title)}</h1><p class="b fit">${esc(sl.body)}</p>${diagram(sl)}${foot}</section>`;
  if (sl.kind === 'beat') return `<section class="p">${kick}<h2 class="t fit">${esc(sl.title)}</h2>${diagram(sl)}<p class="b fit">${esc(sl.body)}</p>${foot}</section>`;
  if (sl.kind === 'close') return `<section class="p close">${kick}<h2 class="t lg fit">${esc(sl.title)}</h2><p class="b lg fit">${esc(sl.body)}</p>${foot}</section>`;
  return `<section class="p cta">${kick}<h2 class="t xl fit">${esc(sl.title)}</h2><p class="b lg fit">${esc(sl.body)}</p><p class="u">${esc(c.url)}</p>${mark ? `<img class="wm" src="${mark}">` : ''}${foot}</section>`;
};
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${faces}
@page{size:${W}px ${H}px;margin:0}
*{box-sizing:border-box}html,body{margin:0;background:${col.ink}}
.p{position:relative;width:${W}px;height:${H}px;padding:${M}px;background:${col.ink};color:${col.paper};overflow:hidden;page-break-after:always;display:flex;flex-direction:column;gap:36px}
.k{display:flex;gap:16px;align-items:center;font:500 24px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;text-transform:uppercase;color:${col['muted-foreground']}}
.close .k span:last-child{color:${col.copper}}
.disc{display:inline-grid;place-items:center;min-width:48px;height:48px;border-radius:24px;background:${col.copper};color:${col.ink};font:600 26px/1 'JetBrains Mono Variable',monospace;letter-spacing:0}
.t{margin:0;font:400 64px/1.08 'Newsreader Variable',serif;letter-spacing:-.025em;color:${col.paper};max-height:212px;text-wrap:balance}
.t.lg{font-size:76px;max-height:340px}.t.xl{font-size:88px;line-height:1.02;max-height:370px}
.b{margin:0;font:400 34px/1.45 'Inter Variable',sans-serif;color:${col['ink-2']};max-height:200px;max-width:880px}
.b.lg{font-size:40px;max-height:300px}
.dg{position:relative;width:${DW}px;height:${DH}px;flex:none;overflow:hidden;border-radius:6px;background:${col['paper-bright']};outline:1px solid ${col.border}}
.cover .dg{height:${DH - 80}px}
.st{position:absolute;left:0;top:0;width:${ZW}px;height:${ZH}px;transform-origin:0 0}.st>svg{position:absolute;left:0;top:0;width:${ZW}px;height:${ZH}px}
.f{margin-top:auto;display:flex;justify-content:space-between;padding-top:20px;border-top:1px solid ${col.rule};font:500 22px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;text-transform:uppercase;color:${col['muted-foreground']}}
.close .t{margin-top:120px}
.u{margin:0;font:500 28px/1.3 'JetBrains Mono Variable',monospace;color:${col.copper};word-break:break-all}
.wm{height:64px;width:auto;align-self:flex-start;margin-top:40px}
</style></head><body>${c.slides.map(page).join('')}</body></html>`;

const out = path.join(run, 'out'); fs.mkdirSync(out, {recursive: true});
const browser = await chromium.launch(); const pg = await browser.newPage({viewport: {width: W, height: H}});
await pg.setContent(html, {waitUntil: 'load'});
const loaded = await pg.evaluate(async () => Promise.all(["64px 'Newsreader Variable'", "34px 'Inter Variable'", "24px 'JetBrains Mono Variable'"].map(async f => (await document.fonts.load(f)).length)));
if (loaded.includes(0)) { console.error('BLOCKED: a design-system font did not load', loaded); process.exit(1); }
const over = await pg.evaluate(() => [...document.querySelectorAll('.fit, .u')].map((e, i) => ({i, cls: e.className, sec: [...document.querySelectorAll('section')].indexOf(e.closest('section')) + 1,
  over: e.scrollHeight - e.clientHeight, past: e.getBoundingClientRect().bottom > e.closest('section').querySelector('.f').getBoundingClientRect().top - 8})).filter(x => x.over > 1 || x.past));
if (over.length) { console.error('BLOCKED: text overflows its box or runs into the footer', JSON.stringify(over)); process.exit(1); }
const secs = await pg.$$('section');
for (const [i, s] of secs.entries()) await s.screenshot({path: path.join(out, `${c.part}-${String(i + 1).padStart(2, '0')}.png`)});
await pg.pdf({path: path.join(out, `${c.part}-carousel.pdf`), width: `${W}px`, height: `${H}px`, printBackground: true, pageRanges: `1-${N}`});
console.log(`${secs.length} slides -> ${out}`);
await browser.close();
