#!/usr/bin/env node
// Render every frame a part explainer needs, in Chromium, from the real draw.io SVG.
//
// Per scene: a camera move from the previous scene's view to this one (FPS x MOVE_S frames), then one
// hold frame that build_film.py loops for the rest of the narration. The active zones keep full
// strength while the rest of the diagram dims under the ink ground, a copper frame rings them, and the
// beat's reading-path marker gets a copper ring found in the SVG text itself. Motion rules: one move
// per scene, nothing idles, labels never sit on the diagram.
//
// Usage: node render_frames.mjs <run-dir> --svg <diagram.svg> --ds <design-system-dir> [--wordmark <png>]
// Reads <run>/scenes.json and <run>/zones.json; writes <run>/frames/<scene>/m###.png + hold.png and
// <run>/frames/frames.json. Resolves playwright from the cwd, then this repo's node_modules.
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const args = process.argv.slice(2);
const run = path.resolve(args[0]);
const opt = k => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : undefined; };
const svgPath = opt('--svg'), dsDir = opt('--ds'), wordmark = opt('--wordmark');
if (!svgPath || !dsDir) { console.error('BLOCKED: --svg and --ds are required'); process.exit(1); }
const FPS = 30, MOVE_S = 0.9, W = 1920, H = 1080;
const VIEW = {x: 96, y: 232, w: 1728, h: 768};   // the diagram's window; labels live above it, never on it

let chromium;
for (const base of [process.cwd(), path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..')]) {
  try { ({chromium} = createRequire(path.join(base, 'x.js'))('playwright')); console.log('playwright from', base); break; } catch {}
}
if (!chromium) { console.error('BLOCKED: playwright not resolvable from cwd or the repo'); process.exit(1); }

const scenes = JSON.parse(fs.readFileSync(path.join(run, 'scenes.json'), 'utf8'));
const zones = JSON.parse(fs.readFileSync(path.join(run, 'zones.json'), 'utf8'));
const tokens = JSON.parse(fs.readFileSync(path.join(dsDir, 'tokens.json'), 'utf8'));
const col = Object.fromEntries(tokens.color.tokens.map(t => [t.name, typeof t.value === 'string' ? t.value : t.value.ink]));
const font = f => `data:font/woff2;base64,${fs.readFileSync(path.join(dsDir, f)).toString('base64')}`;
const faces = tokens.type.fonts.map(f => `@font-face{font-family:'${f.family}';src:url(${font(f.file)}) format('woff2');font-weight:${f.weight};font-style:${f.style}}`).join('');
const svg = fs.readFileSync(svgPath, 'utf8').replace(/^[\s\S]*?(<svg)/, '$1');
const mark = wordmark ? `data:image/png;base64,${fs.readFileSync(wordmark).toString('base64')}` : '';

// The camera rectangle for a scene, in SVG units, fitted to the window's aspect with padding.
const ZW = zones.width, ZH = zones.height, aspect = VIEW.w / VIEW.h;
function camera(sc) {
  if (!sc.zones.length) { const w = Math.max(ZW, ZH * aspect) * 1.02; return {x: ZW / 2 - w / 2, y: ZH / 2 - w / aspect / 2, w, h: w / aspect}; }
  const b = sc.zones.map(n => zones.zones[n]);
  let x0 = Math.min(...b.map(z => z.x)), y0 = Math.min(...b.map(z => z.y)), x1 = Math.max(...b.map(z => z.x + z.w)), y1 = Math.max(...b.map(z => z.y + z.h));
  const pad = 48; x0 -= pad; y0 -= pad; x1 += pad; y1 += pad;
  let w = x1 - x0, h = y1 - y0, cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
  if (w / h > aspect) h = w / aspect; else w = h * aspect;
  const minW = ZW * 0.42; if (w < minW) { w = minW; h = w / aspect; }   // never zoom past legibility of context
  return {x: cx - w / 2, y: cy - h / 2, w, h};
}

const page_html = `<!doctype html><html><head><meta charset="utf-8"><style>${faces}
html,body{margin:0;width:${W}px;height:${H}px;background:${col.ink};overflow:hidden}
#k{position:absolute;left:96px;top:64px;font:500 22px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;text-transform:uppercase;color:${col['muted-foreground']};display:flex;gap:16px;align-items:center}
.disc{display:inline-grid;place-items:center;min-width:44px;height:44px;border-radius:22px;background:${col.copper};color:${col.ink};font:600 24px/1 'JetBrains Mono Variable',monospace;letter-spacing:0}
#l{position:absolute;left:96px;top:118px;font:400 72px/1.02 'Newsreader Variable',serif;letter-spacing:-.025em;color:${col.paper};white-space:nowrap}
#v{position:absolute;left:${VIEW.x}px;top:${VIEW.y}px;width:${VIEW.w}px;height:${VIEW.h}px;overflow:hidden;border-radius:6px;background:${col['paper-bright']};outline:1px solid ${col.border}}
#stage{position:absolute;left:0;top:0;width:${ZW}px;height:${ZH}px;transform-origin:0 0}
#stage>svg{position:absolute;left:0;top:0;width:${ZW}px;height:${ZH}px}
#ov{position:absolute;left:0;top:0;width:${ZW}px;height:${ZH}px;overflow:visible}
#bar{position:absolute;left:96px;top:1036px;height:2px;background:${col.copper}}
#bart{position:absolute;left:96px;top:1036px;width:1728px;height:1px;background:${col.rule}}
#close{position:absolute;inset:0;display:none;background:${col.ink}}
#ck{position:absolute;left:96px;top:300px;font:500 24px/1 'JetBrains Mono Variable',monospace;letter-spacing:.08em;text-transform:uppercase;color:${col.copper}}
#ct{position:absolute;left:96px;top:352px;width:1300px;font:400 96px/1.02 'Newsreader Variable',serif;letter-spacing:-.025em;color:${col.paper}}
#cs{position:absolute;left:96px;top:500px;width:1100px;font:400 30px/1.5 'Inter Variable',sans-serif;color:${col['ink-2']}}
#cr{position:absolute;left:96px;top:276px;width:1728px;height:1px;background:${col.rule}}
#wm{position:absolute;right:96px;bottom:88px;height:48px}
</style></head><body>
<div id="k"></div><div id="l"></div>
<div id="v"><div id="stage">${svg}<svg id="ov" viewBox="0 0 ${ZW} ${ZH}"></svg></div></div>
<div id="bart"></div><div id="bar"></div>
<div id="close"><div id="cr"></div><div id="ck"></div><div id="ct"></div><div id="cs"></div>${mark ? `<img id="wm" src="${mark}">` : ''}</div>
</body></html>`;

const browser = await chromium.launch();
const page = await browser.newPage({viewport: {width: W, height: H}});
await page.setContent(page_html, {waitUntil: 'load'});
// Load each face explicitly: document.fonts.ready only waits for faces the DOM has used, and an unused face
// falls back to the default font, which differs in width from sans-serif and monospace and so passes a naive check.
const loaded = await page.evaluate(async () => Promise.all(["72px 'Newsreader Variable'", "30px 'Inter Variable'", "22px 'JetBrains Mono Variable'"]
  .map(async f => (await document.fonts.load(f)).length)));
if (loaded.includes(0)) { console.error('BLOCKED: font face failed to load', loaded); process.exit(1); }
// The typeface must be the design system's, not a fallback that looks fine: measure against a serif control.
const fontOk = await page.evaluate(() => { const m = (f) => { const c = document.createElement('canvas').getContext('2d'); c.font = `72px ${f}`; return c.measureText('Surges stop at the door').width; };
  return [m("'Newsreader Variable'") !== m('serif'), m("'Inter Variable'") !== m('sans-serif'), m("'JetBrains Mono Variable'") !== m('monospace')]; });
if (fontOk.includes(false)) { console.error('BLOCKED: a design-system font did not load', fontOk); process.exit(1); }
// Reading-path markers: draw.io puts them in the SVG as label text. Their boxes, in SVG units.
const marks = await page.evaluate(() => { const out = {}; const st = document.querySelector('#stage>svg'); const r0 = st.getBoundingClientRect(); const s = st.viewBox.baseVal.width / r0.width;
  for (const el of st.querySelectorAll('div, text')) { const t = (el.textContent || '').trim(); if (t.length === 1 && '①②③④⑤⑥⑦⑧⑨⑩'.includes(t) && !el.querySelector('div')) { const r = el.getBoundingClientRect(); if (r.width) out[t] = {x: (r.x - r0.x + r.width / 2) * s, y: (r.y - r0.y + r.height / 2) * s}; } }
  return out; });
console.log('markers found in SVG:', Object.keys(marks).join(' ') || 'none');

const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
const lerp = (a, b, t) => ({x: a.x + (b.x - a.x) * t, y: a.y + (b.y - a.y) * t, w: a.w + (b.w - a.w) * t, h: a.h + (b.h - a.h) * t});
const all = scenes.scenes, beats = all.filter(s => s.kind !== 'open' && s.kind !== 'close').length;
const out = {fps: FPS, move_s: MOVE_S, width: W, height: H, scenes: []};
// The film enters by settling from a wider view into the whole diagram, so the first scene moves like the rest.
const full = camera({zones: []}), wide = 1.18;
let prevCam = {x: full.x - full.w * (wide - 1) / 2, y: full.y - full.h * (wide - 1) / 2, w: full.w * wide, h: full.h * wide}, prevLabel = '';
for (const [i, sc] of all.entries()) {
  const dir = path.join(run, 'frames', sc.id); fs.mkdirSync(dir, {recursive: true});
  const cam = sc.kind === 'close' ? prevCam : camera(sc);
  const zs = sc.zones.map(n => zones.zones[n]), mk = sc.marks.map(m => marks[m]).filter(Boolean);
  const n = Math.round(FPS * MOVE_S);
  const state = (t) => ({cam: lerp(prevCam, cam, ease(t)), fade: Math.min(1, Math.max(0, (t - .35) / .5)), labelIn: sc.kind === 'close' ? 0 : Math.min(1, Math.max(0, (t - .3) / .5)),   // the close card carries its own title
    kicker: scenes.kicker, marks: sc.marks, label: sc.label, prevLabel, labelOut: Math.max(0, 1 - t / .3), zs, mk, close: sc.kind === 'close',
    closeIn: ease(Math.min(1, t / .8)), progress: Math.max(0, Math.min(1, (i) / (all.length - 1))), title: sc.title || '', cta: sc.cta || ''});
  for (let f = 0; f <= n; f++) {
    const st = state(f / n);
    await page.evaluate(({st, VIEW, ZW, ZH, ink, copper}) => {
      const s = VIEW.w / st.cam.w;
      document.getElementById('stage').style.transform = `scale(${s}) translate(${-st.cam.x}px, ${-st.cam.y}px)`;
      const k = document.getElementById('k'); k.innerHTML = st.marks.map(m => `<span class="disc">${m}</span>`).join('') + `<span>${st.kicker}</span>`;
      const l = document.getElementById('l'); const lab = st.labelIn > 0 ? st.label : st.prevLabel; l.textContent = lab;
      l.style.opacity = st.labelIn > 0 ? st.labelIn : st.labelOut; l.style.transform = `translateY(${(1 - (st.labelIn > 0 ? st.labelIn : 1)) * 12}px)`;
      const ov = document.getElementById('ov'); const sw = 4 / s;
      if (!st.zs.length) ov.innerHTML = '';
      else {
        const holes = st.zs.map(z => `M${z.x},${z.y}h${z.w}v${z.h}h${-z.w}z`).join('');
        ov.innerHTML = `<path d="M-4000,-4000H${ZW + 4000}V${ZH + 4000}H-4000z${holes}" fill-rule="evenodd" fill="${ink}" opacity="${.55 * st.fade}"/>` +
          st.zs.map(z => `<rect x="${z.x}" y="${z.y}" width="${z.w}" height="${z.h}" rx="${6 / s}" fill="none" stroke="${copper}" stroke-width="${sw}" opacity="${st.fade}"/>`).join('') +
          st.mk.map(m => `<circle cx="${m.x}" cy="${m.y}" r="${20 / s}" fill="none" stroke="${copper}" stroke-width="${sw}" opacity="${st.fade}"/>`).join('');
      }
      document.getElementById('bar').style.width = `${1728 * st.progress}px`;
      const c = document.getElementById('close'); c.style.display = st.close ? 'block' : 'none';
      if (st.close) { c.style.opacity = Math.min(1, st.closeIn * 1.8);   // ground first, words after: never text over the diagram
        for (const id of ['ck', 'ct', 'cs', 'wm', 'cr']) { const e = document.getElementById(id); if (e) e.style.opacity = Math.max(0, (st.closeIn - .55) / .45); }
        document.getElementById('ck').textContent = 'What is still unproven';
        document.getElementById('ct').textContent = st.label; document.getElementById('cs').textContent = st.title; }
    }, {st, VIEW, ZW, ZH, ink: col.ink, copper: col.copper});
    if (f < n) await page.screenshot({path: path.join(dir, `m${String(f).padStart(3, '0')}.png`)});
    else await page.screenshot({path: path.join(dir, 'hold.png')});
  }
  out.scenes.push({scene: sc.id, move_frames: n, camera: cam});
  console.log(`${sc.id}: ${n} move frames + hold`);
  prevCam = cam; prevLabel = sc.label;
}
fs.writeFileSync(path.join(run, 'frames', 'frames.json'), JSON.stringify(out, null, 1));
await browser.close();
