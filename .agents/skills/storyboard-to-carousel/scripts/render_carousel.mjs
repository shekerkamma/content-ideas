#!/usr/bin/env node
// Render an authored carousel at 1080x1350 in the DeepGrid Semi design system: PNG per slide plus one PDF
// (LinkedIn takes a carousel as a document).
//
// Design (v2, after the first version was rejected as unprofessional: a pasted draw.io screenshot with
// 5-px labels on a phone, no focal point, half-empty closing slides, one template on every slide):
//   - Signature element: the SIGNAL-CHAIN RAIL. The part's real zones, drawn natively along the base of
//     every slide; the active zone fills copper, so the rail is both the diagram and the progress bar.
//   - One risk: an oversized hero figure per beat in Newsreader copper, the slide's focal point.
//   - No screenshots: a beat redraws its zone's blocks (zone_blocks.py) as large native tiles.
//   - Four archetypes: cover (hook + zone map + swipe cue), beat, close (numbered open questions),
//     call to action (what to bring + link card).
// Blocks on a font that did not load and on any text that overflows its box.
//
// Usage: node render_carousel.mjs <run-dir> --ds <design-system-dir> [--wordmark <png>]
// Reads <run>/carousel.json and <run>/zones.json (with blocks); writes <run>/out/<part>-NN.png + -carousel.pdf
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const args = process.argv.slice(2), run = path.resolve(args[0]);
const opt = k => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : undefined; };
const W = 1080, H = 1350, M = 84;
let chromium;
for (const base of [process.cwd(), path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..')]) {
  try { ({chromium} = createRequire(path.join(base, 'x.js'))('playwright')); break; } catch {}
}
if (!chromium) { console.error('BLOCKED: playwright not resolvable'); process.exit(1); }
const c = JSON.parse(fs.readFileSync(path.join(run, 'carousel.json'), 'utf8'));
const zones = JSON.parse(fs.readFileSync(path.join(run, 'zones.json'), 'utf8')).zones;
const ds = opt('--ds'), tokens = JSON.parse(fs.readFileSync(path.join(ds, 'tokens.json'), 'utf8'));
const col = Object.fromEntries(tokens.color.tokens.map(t => [t.name, typeof t.value === 'string' ? t.value : t.value.ink]));
const faces = tokens.type.fonts.map(f => `@font-face{font-family:'${f.family}';src:url(data:font/woff2;base64,${fs.readFileSync(path.join(ds, f.file)).toString('base64')}) format('woff2');font-weight:${f.weight};font-style:${f.style}}`).join('');
const mark = opt('--wordmark') ? `data:image/png;base64,${fs.readFileSync(opt('--wordmark')).toString('base64')}` : '';
const curly = t => String(t ?? '').replace(/(^|[\s(])"/g, '$1“').replace(/"/g, '”').replace(/(\w)'(\w)/g, '$1’$2').replace(/'/g, '’');
const esc = t => curly(t).replace(/&/g, '&amp;').replace(/</g, '&lt;');
const short = n => n.split('·')[0].trim();
const N = c.slides.length, beats = c.slides.filter(s => s.kind === 'beat');

// Rail order: zones in the order the story visits them, then any zone with blocks it never visits.
// A zone that contains other zones is the package frame, not a stage of the signal path: keep it off the rail.
const inside = (a, b) => b !== a && zones[b].x >= zones[a].x && zones[b].y >= zones[a].y && zones[b].x + zones[b].w <= zones[a].x + zones[a].w && zones[b].y + zones[b].h <= zones[a].y + zones[a].h;
const frame = k => Object.keys(zones).some(b => inside(k, b));
const order = [];
for (const s of beats) for (const z of s.zones) if (!order.includes(z) && !frame(z)) order.push(z);
for (const [k, v] of Object.entries(zones)) if (!order.includes(k) && !frame(k) && (v.blocks || []).length) order.push(k);
const rail = (active = []) => `<div class="rail${order.length >= 7 ? ' dense' : ''}">${order.map((z, i) => `${i ? '<i></i>' : ''}<span class="${active.includes(z) ? 'on' : ''}">${esc(short(z))}</span>`).join('')}</div>`;
const head = (sl, i, label) => `<header><span class="kick">${sl.marks?.length ? sl.marks.map(m => `<b class="disc">${m}</b>`).join('') : ''}${esc(label ?? c.kicker)}</span><span class="pg">${String(i + 1).padStart(2, '0')} / ${String(N).padStart(2, '0')}</span></header>`;
const foot = (txt = 'Pre-silicon · every figure a design target') => `<footer><span>${esc(txt)}</span>${mark ? `<img src="${mark}" alt="">` : '<span>DeepGrid Semi</span>'}</footer>`;
const tiles = sl => {
  const said = (sl.source + ' ' + sl.title + ' ' + sl.body).toLowerCase();   // blocks the beat names come first
  const all = sl.zones.flatMap(z => (zones[z].blocks || []).map((b, k) => ({...b, z, k})));
  const named = b => said.includes(b.name.toLowerCase()) || said.includes(b.name.split(/[ ·(]/)[0].toLowerCase());
  const seen = new Set(), uniq = [...all.filter(named), ...all.filter(b => !named(b))].filter(b => !seen.has(b.name) && seen.add(b.name));
  const bl = uniq.slice(0, 4);   // four rails share block names: show each name once
  const more = uniq.length - bl.length;
  return `<section class="zone"><div class="zh">${esc(sl.zones.map(short).join('  +  '))}</div><div class="tiles n${bl.length}">${bl.map(b =>
    `<div class="tile"><strong>${esc(b.name)}</strong>${b.sub ? `<small>${esc(b.sub)}</small>` : ''}</div>`).join('')}</div>${more > 0 ? `<div class="more">+ ${more} more block${more > 1 ? 's' : ''} in this zone</div>` : ''}</section>`;
};
const page = (sl, i) => {
  if (sl.kind === 'cover') return `<article class="p cover">${head(sl, i)}
    <h1 class="fit">${esc(sl.title)}</h1><p class="lead fit">${esc(sl.body)}</p>
    <div class="map"><div class="mh">Inside the part · ${order.length} zones of the architecture</div>${order.map((z, k) => `<div class="mr"><span class="mn">${String(k + 1).padStart(2, '0')}</span><span class="mz">${esc(short(z))}</span><span class="mc">${(zones[z].blocks || []).length} blocks</span></div>`).join('')}</div>
    <div class="swipe">Swipe to follow the signal <svg viewBox="0 0 40 16" width="40" height="16"><path d="M0 8h36M29 2l7 6-7 6" fill="none" stroke="currentColor" stroke-width="2"/></svg></div>${foot()}</article>`;
  if (sl.kind === 'beat') return `<article class="p beat${sl.stat ? '' : ' nostat'}">${head(sl, i)}
    ${sl.stat ? `<div class="stat"><div class="sv">${esc(sl.stat.value)}</div><div class="sl">${esc(sl.stat.label)}</div></div>` : ''}
    <h2 class="fit">${esc(sl.title)}</h2><p class="body fit">${esc(sl.body)}</p>${tiles(sl)}${rail(sl.zones)}${foot()}</article>`;
  if (sl.kind === 'close') return `<article class="p close">${head(sl, i, 'What is still unproven')}
    <h2 class="fit">${esc(sl.title)}</h2>${(sl.items || []).length ? '' : `<p class="body fit">${esc(sl.body)}</p>`}
    <ol class="qs">${(sl.items || []).map((q, k) => `<li><span>${String(k + 1).padStart(2, '0')}</span><p class="fit">${esc(q)}</p></li>`).join('')}</ol>${rail([])}${foot('Evaluation, not a datasheet, settles these')}</article>`;
  return `<article class="p cta">${head(sl, i)}<h2 class="big fit">${esc(sl.title)}</h2>
    <div class="bring">Bring us</div><ul class="items">${(sl.items || []).map(t => `<li><svg viewBox="0 0 20 20" width="22" height="22"><path d="M3 10.5l4.5 4.5L17 5" fill="none" stroke="currentColor" stroke-width="2.4"/></svg><p class="fit">${esc(t)}</p></li>`).join('')}</ul>
    <div class="link"><span>Read the full architecture</span><b>${esc(c.url)}</b></div>${rail([])}${foot()}</article>`;
};
const css = `${faces}
@page{size:${W}px ${H}px;margin:0}*{box-sizing:border-box}html,body{margin:0;background:${col.ink}}
.p{position:relative;width:${W}px;height:${H}px;padding:${M}px ${M}px 0;background:${col.ink};color:${col.paper};overflow:hidden;page-break-after:always;display:flex;flex-direction:column}
header{display:flex;justify-content:space-between;align-items:center;font:500 22px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col['muted-foreground']};padding-bottom:22px;border-bottom:1px solid ${col.rule}}
.kick{display:flex;gap:14px;align-items:center}.close .kick{color:${col.copper}}
.disc{display:inline-grid;place-items:center;min-width:44px;height:44px;border-radius:22px;background:${col.copper};color:${col.ink};font:600 24px/1 'JetBrains Mono Variable',monospace;letter-spacing:0}
footer{height:96px;display:flex;justify-content:space-between;align-items:center;border-top:1px solid ${col.rule};font:500 18px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col['muted-foreground']}}
footer img{height:34px;width:auto}
h1{margin:56px 0 0;font:400 92px/1.0 'Newsreader Variable',serif;letter-spacing:-.03em;max-height:380px;text-wrap:balance}
h2{margin:0;font:400 58px/1.08 'Newsreader Variable',serif;letter-spacing:-.022em;max-height:192px;text-wrap:balance}
.lead{margin:30px 0 0;font:400 34px/1.42 'Inter Variable',sans-serif;color:${col['ink-2']};max-height:150px;max-width:880px}
.body{margin:22px 0 0;font:400 30px/1.45 'Inter Variable',sans-serif;color:${col['ink-2']};max-height:132px;max-width:900px}
.stat{margin:48px 0 30px;display:grid;gap:16px}
.sv{font:400 168px/.86 'Newsreader Variable',serif;letter-spacing:-.04em;color:${col.copper};white-space:nowrap}
.sl{font:500 22px/1.35 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col['muted-foreground']}}
.nostat h2{margin-top:72px;font-size:72px;max-height:240px}
.zone{margin-top:36px;padding:26px 28px 24px;background:${col.surface};border:1px solid ${col.border};border-radius:6px}
.zh{font:500 20px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col.copper};margin-bottom:20px}
.tiles{display:grid;grid-template-columns:1fr 1fr;gap:14px}.tiles.n1,.tiles.n3 .tile:first-child{grid-column:1/-1}
.tile{padding:18px 20px;border:1px solid ${col['portfolio-frame']};border-radius:4px;background:${col.ink};min-height:96px}
.tile strong{display:block;font:600 28px/1.2 'Inter Variable',sans-serif;color:${col.paper}}
.tile small{display:block;margin-top:8px;font:400 20px/1.35 'Inter Variable',sans-serif;color:${col['muted-foreground']};max-height:54px;overflow:hidden}
.more{margin-top:14px;font:500 18px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;color:${col['muted-foreground']}}
.rail{margin-top:auto;margin-bottom:34px;flex:none;display:flex;align-items:center;gap:0}
.rail span{flex:1 1 0;min-width:0;text-align:center;padding:12px 6px;border:1px solid ${col.border};border-radius:4px;font:500 15px/1.2 'JetBrains Mono Variable',monospace;letter-spacing:.04em;text-transform:uppercase;color:${col['muted-foreground']};overflow:hidden;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;height:62px}
.rail.dense span{font-size:12.5px;letter-spacing:.01em;padding:12px 3px}.rail.dense i{flex-basis:10px}
.rail span.on{background:${col.copper};border-color:${col.copper};color:${col.ink};font-weight:600}
.rail i{flex:0 0 18px;height:1px;background:${col['portfolio-frame']}}
.map{margin-top:48px;border-top:1px solid ${col.rule}}
.mh{font:500 20px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col.copper};padding:22px 0 8px}
.mr{display:grid;grid-template-columns:64px 1fr auto;align-items:baseline;padding:16px 0;border-bottom:1px solid ${col.rule}}
.mn{font:500 22px/1 'JetBrains Mono Variable',monospace;color:${col.copper}}.mz{font:400 34px/1.15 'Newsreader Variable',serif;color:${col.paper}}
.mc{font:500 18px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;text-transform:uppercase;color:${col['muted-foreground']}}
.swipe{margin-top:28px;align-self:flex-end;display:flex;gap:14px;align-items:center;font:500 22px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col.copper}}
.close h2{margin-top:72px;font-size:72px;max-height:240px}.cover footer{margin-top:auto}
.qs{list-style:none;margin:44px 0 40px;padding:0;border-top:1px solid ${col.rule};flex:1;display:flex;flex-direction:column;justify-content:space-evenly}
.qs li{display:grid;grid-template-columns:96px 1fr;padding:40px 0;border-bottom:1px solid ${col.rule}}
.qs span{font:400 60px/1 'Newsreader Variable',serif;color:${col.copper}}.qs p{margin:0;font:400 38px/1.32 'Inter Variable',sans-serif;color:${col.paper};max-height:152px}
.cta .big{margin-top:64px;font-size:84px;line-height:1.02;max-height:270px}
.bring{margin-top:52px;font:500 20px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col.copper}}
.items{list-style:none;margin:16px 0 0;padding:0;flex:1;display:flex;flex-direction:column;justify-content:space-evenly}
.items li{display:grid;grid-template-columns:44px 1fr;align-items:start;padding:22px 0;border-bottom:1px solid ${col.rule};color:${col.copper}}
.items p{margin:0;font:400 32px/1.35 'Inter Variable',sans-serif;color:${col.paper};max-height:132px}
.cta .body{margin-top:30px}
.link{margin:34px 0 40px;padding:24px 28px;border:1px solid ${col.copper};border-radius:6px;display:grid;gap:10px}
.link span{font:500 18px/1 'JetBrains Mono Variable',monospace;letter-spacing:.1em;text-transform:uppercase;color:${col['muted-foreground']}}
.link b{font:500 24px/1.3 'JetBrains Mono Variable',monospace;color:${col.copper};word-break:break-all}`;
const html = `<!doctype html><html><head><meta charset="utf-8"><style>${css}</style></head><body>${c.slides.map(page).join('')}</body></html>`;
const out = path.join(run, 'out'); fs.mkdirSync(out, {recursive: true});
fs.writeFileSync(path.join(out, `${c.part}-carousel.html`), html);   // the editable design artifact
const browser = await chromium.launch(); const pg = await browser.newPage({viewport: {width: W, height: H}});
await pg.setContent(html, {waitUntil: 'load'});
const loaded = await pg.evaluate(async () => Promise.all(["64px 'Newsreader Variable'", "34px 'Inter Variable'", "24px 'JetBrains Mono Variable'"].map(async f => (await document.fonts.load(f)).length)));
if (loaded.includes(0)) { console.error('BLOCKED: a design-system font did not load', loaded); process.exit(1); }
const over = await pg.evaluate(() => [...document.querySelectorAll('.fit, .tile, .zone, .map, .qs, .items, .link')].map(e => {
  const art = e.closest('article'), f = art.querySelector('footer').getBoundingClientRect();
  return {slide: [...document.querySelectorAll('article')].indexOf(art) + 1, cls: e.className, text: (e.textContent || '').slice(0, 40),
    over: e.scrollHeight - e.clientHeight, past: e.getBoundingClientRect().bottom > f.top + 1};
}).filter(x => x.over > 1 || x.past));
if (over.length) { console.error('BLOCKED: content overflows its box or runs into the footer\n' + over.map(o => JSON.stringify(o)).join('\n')); process.exit(1); }
const arts = await pg.$$('article');
for (const [i, s] of arts.entries()) await s.screenshot({path: path.join(out, `${c.part}-${String(i + 1).padStart(2, '0')}.png`)});
await pg.pdf({path: path.join(out, `${c.part}-carousel.pdf`), width: `${W}px`, height: `${H}px`, printBackground: true, pageRanges: `1-${N}`});
console.log(`${arts.length} slides -> ${out}`);
await browser.close();
