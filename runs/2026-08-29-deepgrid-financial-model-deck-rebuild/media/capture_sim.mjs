import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';

const SRC  = process.argv[2];
const OUT  = process.argv[3];
const PLAN = JSON.parse(process.argv[4]);   // [[selector|null, holdMs, label], ...]

const EXEC = ['chromium-1234', 'chromium-1208']
  .map(b => `/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`)
  .find(existsSync);
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
