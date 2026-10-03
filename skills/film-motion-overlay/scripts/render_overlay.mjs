#!/usr/bin/env node
// Render attention motion for a narrated deck film from its plan: per matched cue, a short camera move
// toward the region the sentence is about (a push of at most MAX_ZOOM), the rest of the slide dimmed a
// little, the region outlined in the deck's own accent. Unmatched cues keep the previous framing.
//
// Rendered from the clean deck frame (frames/slide-NN.png), not from decoded video, so no generation
// loss. Writes <run>/frames/<slide>/... and <run>/timeline.json: per segment, an ordered list of
// {file, dur} that build_overlay.py concatenates with the original fades.
//
// Usage: node render_overlay.mjs <run-dir> --plan plan.json --slides <frames-dir> [--accent #0077A3]
import fs from 'node:fs';
import path from 'node:path';
import {createRequire} from 'node:module';

const args = process.argv.slice(2), run = path.resolve(args[0]);
const opt = (k, d) => { const i = args.indexOf(k); return i > 0 ? args[i + 1] : d; };
const plan = JSON.parse(fs.readFileSync(opt('--plan'), 'utf8')), slides = opt('--slides'), accent = opt('--accent', '#0077A3');
const FPS = 30, MOVE_S = 0.8, FADE = Number(opt('--fade', '0.25')), MAX_ZOOM = 1.12, PAD = 18, W = 1920, H = 1080;
const k = W / plan.stage[0];   // stage units -> pixels

let chromium;
for (const base of [process.cwd(), path.resolve(path.dirname(new URL(import.meta.url).pathname), '../../..')]) {
  try { ({chromium} = createRequire(path.join(base, 'x.js'))('playwright')); break; } catch {}
}
if (!chromium) { console.error('BLOCKED: playwright not resolvable'); process.exit(1); }

// Framing for a target: zoom so the region reads larger but never past MAX_ZOOM, then centre on it as far
// as the slide edges allow (the window never shows past the slide).
// The slide's headline band (plan "keep") stays whole: a push that would cut the title gives up zoom first,
// then pans only as far as the title allows (a 1.12x push toward a right-hand card cropped "Same pins" to
// "e pins" on the 2DOM datasheet, 2026-10-03).
function frame(t, keep) {
  if (!t) return {s: 1, cx: W / 2, cy: H / 2, box: null};
  const [x, y, w, h] = t.bbox.map(v => v * k), bx = [x - PAD, y - PAD, w + 2 * PAD, h + 2 * PAD];
  let s = Math.min(MAX_ZOOM, Math.max(1, Math.min(W * 0.9 / bx[2], H * 0.9 / bx[3])));
  const kp = keep ? keep.map(v => v * k) : null, M = 24;
  if (kp) s = Math.max(1, Math.min(s, W / (kp[2] + 2 * M)));
  const vw = W / s, vh = H / s, clamp = (v, lo, hi) => Math.min(hi, Math.max(lo, v));
  let cx = clamp(x + w / 2, vw / 2, W - vw / 2), cy = clamp(y + h / 2, vh / 2, H - vh / 2);
  if (kp) { cx = clamp(cx, kp[0] + kp[2] + M - vw / 2, kp[0] - M + vw / 2); cy = Math.min(cy, kp[1] - M + vh / 2); }
  return {s, cx: clamp(cx, vw / 2, W - vw / 2), cy: clamp(cy, vh / 2, H - vh / 2), box: bx};
}
const ease = t => t < .5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;

const browser = await chromium.launch();
const page = await browser.newPage({viewport: {width: W, height: H}});
const timeline = {fps: FPS, fade: FADE, segments: []};
for (const seg of plan.segments) {
  const png = path.join(slides, `slide-${String(seg.slide).padStart(2, '0')}.png`);
  if (!fs.existsSync(png)) { console.error(`BLOCKED: no deck frame ${png}`); process.exit(1); }
  const dir = path.join(run, 'frames', String(seg.slide).padStart(2, '0')); fs.mkdirSync(dir, {recursive: true});
  await page.setContent(`<html><body style="margin:0;width:${W}px;height:${H}px;overflow:hidden;background:#000">
    <div id="cam" style="position:absolute;left:0;top:0;width:${W}px;height:${H}px;transform-origin:0 0">
    <img src="data:image/png;base64,${fs.readFileSync(png).toString('base64')}" style="position:absolute;left:0;top:0;width:${W}px;height:${H}px">
    <svg id="ov" viewBox="0 0 ${W} ${H}" style="position:absolute;left:0;top:0;width:${W}px;height:${H}px"></svg></div></body></html>`);
  const draw = (a, b, t, o) => page.evaluate(({a, b, t, o, W, H, accent}) => {
    const L = (p, q) => p + (q - p) * t, s = L(a.s, b.s), cx = L(a.cx, b.cx), cy = L(a.cy, b.cy);
    document.getElementById('cam').style.transform = `scale(${s}) translate(${W / 2 / s - cx}px, ${H / 2 / s - cy}px)`;
    const box = b.box || a.box, op = b.box ? (a.box && a.box === b.box ? 1 : o) : (a.box ? 1 - o : 0);
    document.getElementById('ov').innerHTML = box ? `<path d="M-50,-50H${W + 50}V${H + 50}H-50z M${box[0]},${box[1]}h${box[2]}v${box[3]}h${-box[2]}z"
      fill-rule="evenodd" fill="#101212" opacity="${.22 * op}"/><rect x="${box[0]}" y="${box[1]}" width="${box[2]}" height="${box[3]}" rx="6"
      fill="none" stroke="${accent}" stroke-width="${3 / s}" opacity="${op}"/>` : '';
  }, {a, b, t, o, W, H, accent});
  const items = []; let cur = frame(null), clock = 0, n = 0, prevKey = null;
  const hold = async (until) => { if (until - clock < 1 / FPS) return; await draw(cur, cur, 1, 1);
    const f = path.join(dir, `h${n}.png`); await page.screenshot({path: f}); items.push({file: f, dur: +(until - clock).toFixed(4)}); clock = until; };
  for (const m of seg.moves) {
    const key = m.target ? m.target.bbox.join(',') : null;
    if (!m.target || key === prevKey) continue;                     // nothing new to look at: stay
    const start = Math.max(m.t - seg.start - 0.15, FADE + 0.25);   // never move during the fade-in
    if (start + MOVE_S > seg.duration - FADE - 0.2) continue;       // too close to the cut to move and settle
    await hold(start);
    const nxt = frame(m.target, seg.keep), steps = Math.round(MOVE_S * FPS);
    for (let i = 1; i <= steps; i++) {
      const e = ease(i / steps); await draw(cur, nxt, e, Math.min(1, i / steps * 1.4));
      const f = path.join(dir, `m${n}-${String(i).padStart(2, '0')}.png`); await page.screenshot({path: f}); items.push({file: f, dur: +(1 / FPS).toFixed(4)});
    }
    clock = start + MOVE_S; cur = {...nxt, box: nxt.box}; prevKey = key; n++;
  }
  await hold(seg.duration);
  timeline.segments.push({slide: seg.slide, start: seg.start, duration: seg.duration, moves: n, items});
  console.log(`slide ${seg.slide}: ${n} moves, ${items.length} frames`);
}
fs.writeFileSync(path.join(run, 'timeline.json'), JSON.stringify(timeline, null, 1));
await browser.close();
