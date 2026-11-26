#!/usr/bin/env node
// Render an animated web page to video, frame by frame, with exact timing.
// No packages to install: it drives the Chrome that is already on the machine and pipes frames to ffmpeg.

const HELP = `
Render an animated web page (HTML, canvas, three.js) to video, one exact frame at a time.

The page must be driven by time, not by a running clock. It exposes one object:

  window.ad = {
    duration: 16,                       // seconds
    width: 1920, height: 1080,          // the stage, in CSS pixels
    seek(t) { ... },                    // draw the frame for time t (may return a promise)
    events: { "logo.land": 12.7 },      // optional: named beats, for the sound
    ready: somePromise                  // optional: resolves when images, fonts and models are loaded
  }

Because every frame is drawn from t alone, the render is repeatable and never drops frames,
however slow a frame is to draw.

Usage:
  render_page.mjs <page.html> --video out.mp4 [--fps 30] [--scale 2] [--from 2 --to 8]
  render_page.mjs <page.html> --video overlay.mov --alpha      transparent ProRes 4444, to lay over footage
  render_page.mjs <page.html> --stills folder --at 1.0,4.9,12   single frames for review
  render_page.mjs <page.html> --events events.json              write the page's named beats

Options:
  --fps N        frames per second (default 30)
  --scale N      pixel density. 2 turns a 1920x1080 stage into a 3840x2160 video (default 1)
  --alpha        keep the page background transparent (use a .mov output)
  --gpu          use the real graphics card (faster for three.js; default is software rendering)
  --crf N        H.264 quality, lower is better (default 14)
  --query STR    added to the page address, e.g. "draft=1", so one page can have modes
  --chrome PATH  the browser to use (default: Chrome, Chromium or Edge, or the CHROME environment variable)

MP4 output is H.264, yuv420p, tagged BT.709, so editors show the right contrast.
Needs: Node 22 or newer, Chrome or Chromium, ffmpeg.
`;

import { spawn } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, rmSync, writeFileSync } from 'node:fs';
import { homedir, tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';

const argv = process.argv.slice(2);
if (!argv.length || argv.includes('--help') || argv.includes('-h')) { console.log(HELP.trim()); process.exit(0); }
const opt = { fps: 30, scale: 1, crf: 14 };
const SWITCHES = new Set(['alpha', 'gpu']);
let page = null;
for (let i = 0; i < argv.length; i++) {
  const a = argv[i];
  if (!a.startsWith('--')) { page = a; continue; }
  const key = a.slice(2);
  opt[key] = SWITCHES.has(key) ? true : argv[++i];
}
const fail = (msg) => { console.error(msg); process.exit(1); };
if (!page || !existsSync(page)) fail(`Page not found: ${page}`);
if (!opt.video && !opt.stills && !opt.events) fail('Say what to write: --video, --stills or --events. See --help.');
if (typeof WebSocket === 'undefined') fail('This needs Node 22 or newer.');

function findChrome() {
  const fromCache = (dir, bin) => {
    const root = join(homedir(), '.cache', 'puppeteer', dir);
    if (!existsSync(root)) return [];
    return readdirSync(root).sort().reverse().flatMap((v) => readdirSync(join(root, v)).map((sub) => join(root, v, sub, bin)));
  };
  const places = [
    opt.chrome, process.env.CHROME,
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    '/Applications/Chromium.app/Contents/MacOS/Chromium',
    '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
    '/usr/bin/google-chrome', '/usr/bin/google-chrome-stable', '/usr/bin/chromium', '/usr/bin/chromium-browser',
    'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe',
    ...fromCache('chrome', 'Google Chrome for Testing.app/Contents/MacOS/Google Chrome for Testing'),
    ...fromCache('chrome', 'chrome'),
  ];
  return places.find((p) => p && existsSync(p)) || fail('No Chrome or Chromium found. Install one, or pass --chrome PATH.');
}

const profile = mkdtempSync(join(tmpdir(), 'render-page-'));
const flags = [
  '--headless=new', '--remote-debugging-port=0', `--user-data-dir=${profile}`, '--no-first-run', '--no-default-browser-check',
  '--hide-scrollbars', '--mute-audio', '--allow-file-access-from-files', '--autoplay-policy=no-user-gesture-required',
  '--disable-background-timer-throttling', '--disable-renderer-backgrounding', '--force-color-profile=srgb',
  ...(opt.gpu ? ['--enable-gpu', '--ignore-gpu-blocklist', ...(process.platform === 'darwin' ? ['--use-angle=metal'] : [])]
              : ['--enable-unsafe-swiftshader']),
  'about:blank',
];
const chrome = spawn(findChrome(), flags, { stdio: ['ignore', 'ignore', 'pipe'] });
const cleanup = () => { try { chrome.kill(); } catch {} try { rmSync(profile, { recursive: true, force: true }); } catch {} };
process.on('exit', cleanup);
process.on('SIGINT', () => process.exit(130));

const port = await new Promise((done, bad) => {
  let text = '';
  const timer = setTimeout(() => bad(new Error('Chrome did not start within 30 s')), 30000);
  chrome.stderr.on('data', (chunk) => {
    text += chunk;
    const m = text.match(/DevTools listening on ws:\/\/[^:]+:(\d+)\//);
    if (m) { clearTimeout(timer); done(m[1]); }
  });
  chrome.on('exit', () => bad(new Error('Chrome closed before it was ready:\n' + text.slice(-800))));
}).catch((e) => fail(e.message));

const targets = await (await fetch(`http://127.0.0.1:${port}/json/list`)).json();
const socket = new WebSocket(targets.find((t) => t.type === 'page').webSocketDebuggerUrl);
await new Promise((done, bad) => { socket.onopen = done; socket.onerror = () => bad(new Error('Could not connect to Chrome')); });
let nextId = 0;
const waiting = new Map();
const listeners = new Map();
socket.onmessage = (msg) => {
  const data = JSON.parse(msg.data);
  if (data.id && waiting.has(data.id)) {
    const { done, bad } = waiting.get(data.id);
    waiting.delete(data.id);
    data.error ? bad(new Error(data.error.message)) : done(data.result);
  } else if (data.method && listeners.has(data.method)) listeners.get(data.method)(data.params);
};
const send = (method, params = {}) => new Promise((done, bad) => { const id = ++nextId; waiting.set(id, { done, bad }); socket.send(JSON.stringify({ id, method, params })); });
const run = async (expression) => {
  const r = await send('Runtime.evaluate', { expression, awaitPromise: true, returnByValue: true });
  if (r.exceptionDetails) throw new Error('The page threw: ' + (r.exceptionDetails.exception?.description || r.exceptionDetails.text));
  return r.result.value;
};

await send('Page.enable');
await send('Runtime.enable');
listeners.set('Runtime.exceptionThrown', (p) => console.error('page error:', p.exceptionDetails.exception?.description || p.exceptionDetails.text));
const loaded = new Promise((done) => listeners.set('Page.loadEventFired', done));
await send('Emulation.setDeviceMetricsOverride', { width: 1920, height: 1080, deviceScaleFactor: 1, mobile: false });
await send('Page.navigate', { url: pathToFileURL(resolve(page)).href + (opt.query ? `?${opt.query}` : '') });
await loaded;

let ad = null;
for (let tries = 0; tries < 300 && !ad; tries++) {
  ad = await run(`(async () => { const a = window.ad; if (!a || typeof a.seek !== 'function') return null; if (a.ready) await a.ready;
    return { duration: a.duration, width: a.width || 1920, height: a.height || 1080, events: a.events || {} }; })()`);
  if (!ad) await new Promise((r) => setTimeout(r, 100));
}
if (!ad) fail('The page never defined window.ad with a seek(t) function. See --help for the contract.');
if (!(ad.duration > 0)) fail('window.ad.duration must be a number of seconds.');

const scale = Number(opt.scale);
await send('Emulation.setDeviceMetricsOverride', { width: ad.width, height: ad.height, deviceScaleFactor: scale, mobile: false });
if (opt.alpha) await send('Emulation.setDefaultBackgroundColorOverride', { color: { r: 0, g: 0, b: 0, a: 0 } });

const frameAt = async (t) => {
  await run(`Promise.resolve(window.ad.seek(${t})).then(() => Promise.race([
    new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r))), new Promise((r) => setTimeout(r, 250))]))`);
  const shot = await send('Page.captureScreenshot', { format: 'png', captureBeyondViewport: false });
  return Buffer.from(shot.data, 'base64');
};

if (opt.events) {
  const events = { start: 0, ...ad.events, end: ad.duration };
  writeFileSync(opt.events, JSON.stringify(events, null, 1));
  console.log(`Wrote ${Object.keys(events).length} beats to ${opt.events}`);
}

if (opt.stills) {
  mkdirSync(opt.stills, { recursive: true });
  const times = String(opt.at ?? ad.duration / 2).split(',').map(Number);
  for (const t of times) {
    const file = join(opt.stills, `${t.toFixed(3).padStart(8, '0')}.png`);
    writeFileSync(file, await frameAt(t));
    console.log(`still ${file}`);
  }
}

if (opt.video) {
  const fps = Number(opt.fps);
  const from = Number(opt.from ?? 0), to = Math.min(Number(opt.to ?? ad.duration), ad.duration);
  const total = Math.round((to - from) * fps);
  const mov = opt.video.toLowerCase().endsWith('.mov');
  const codec = opt.alpha ? ['-c:v', 'prores_ks', '-profile:v', '4444', '-pix_fmt', 'yuva444p10le']
    : mov ? ['-c:v', 'prores_ks', '-profile:v', '3', '-pix_fmt', 'yuv422p10le']
      : ['-vf', 'scale=out_color_matrix=bt709:out_range=tv,format=yuv420p', '-c:v', 'libx264', '-preset', 'slow', '-crf', String(opt.crf),
        '-colorspace', 'bt709', '-color_primaries', 'bt709', '-color_trc', 'bt709', '-color_range', 'tv', '-movflags', '+faststart'];
  if (opt.alpha && !mov) fail('--alpha needs a .mov output (ProRes 4444).');
  const ffmpeg = spawn('ffmpeg', ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(fps), '-c:v', 'png', '-i', '-', ...codec, '-r', String(fps), opt.video],
    { stdio: ['pipe', 'inherit', 'inherit'] });
  const finished = new Promise((done) => ffmpeg.on('exit', done));
  const began = Date.now();
  for (let i = 0; i < total; i++) {
    const png = await frameAt(from + i / fps);
    if (!ffmpeg.stdin.write(png)) await new Promise((r) => ffmpeg.stdin.once('drain', r));
    if (i % fps === 0) process.stdout.write(`\rframe ${i}/${total}`);
  }
  ffmpeg.stdin.end();
  const code = await finished;
  if (code !== 0) fail(`\nffmpeg stopped with code ${code}`);
  console.log(`\rWrote ${opt.video}: ${total} frames, ${ad.width * scale}x${ad.height * scale}, ${fps} fps, ${((Date.now() - began) / 1000).toFixed(1)} s to render`);
}

socket.close();
process.exit(0);
