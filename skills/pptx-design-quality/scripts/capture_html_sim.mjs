import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';

// AUDIO: Playwright's recordVideo captures VIDEO ONLY -- the .webm it writes has
// no audio stream at all. A page that beeps, speaks or plays a tone records
// silent, and muxing an anullsrc track afterwards makes that look deliberate.
// To capture a page's audio, record the PulseAudio *monitor* source alongside
// (on WSLg: `-f pulse -i RDPSink.monitor`; the default `RDPSource` is the
// MICROPHONE and will hand you room noise that reads as success).
// Web Audio also needs a TRUSTED gesture: page.mouse.click() dispatches
// pointerdown through CDP and unlocks it; an in-page el.click() does not.

const SRC  = process.argv[2];
const OUT  = process.argv[3];
const PLAN = JSON.parse(process.argv[4]);   // [[selector|null, holdMs, label], ...]

// Do NOT hardcode build numbers: Playwright's expected build moves with every
// upgrade and a stale list makes this exit BLOCKED on a machine that has a
// perfectly good browser. Scan the cache and take the newest build present.
import { readdirSync } from 'node:fs';
const ROOT = '/home/sheke/.cache/ms-playwright';
const EXEC = (() => {
  let builds = [];
  try {
    builds = readdirSync(ROOT)
      .filter(d => /^chromium-\d+$/.test(d))
      .sort((a, b) => Number(b.split('-')[1]) - Number(a.split('-')[1]));
  } catch { return undefined; }
  return builds.map(b => `${ROOT}/${b}/chrome-linux64/chrome`).find(existsSync);
})();
if (!EXEC) { console.error('BLOCKED: no cached chromium build'); process.exit(1); }

const W = 1600, H = 900;
const browser = await chromium.launch({
  executablePath: EXEC, headless: false,
  args: [`--window-size=${W},${H}`, '--autoplay-policy=no-user-gesture-required',
         '--force-device-scale-factor=1'],
});
const ctx = await browser.newContext({
  viewport: { width: W, height: H },
  recordVideo: { dir: OUT, size: { width: W, height: H } },
});
const page = await ctx.newPage();
await page.goto('file://' + SRC, { waitUntil: 'load' });
await page.waitForTimeout(2500);

for (const [sel, hold, label] of PLAN) {
  if (sel) {
    // A direct DOM click, not page.click(): these consoles paint overlays
    // (confidentiality watermarks, intro panels) that intercept pointer events,
    // and Playwright's actionability wait then times out on a button that is
    // perfectly clickable from script.
    const hit = await page.evaluate((s) => {
      const el = document.querySelector(s);
      if (!el) return false;
      el.click();
      return true;
    }, sel);
    if (!hit) console.log(`  MISS ${sel}`);
  }
  console.log(`  ${label} (${hold}ms)`);
  await page.waitForTimeout(hold);
}

await ctx.close();          // finalises the .webm
await browser.close();
console.log('captured ->', OUT);
