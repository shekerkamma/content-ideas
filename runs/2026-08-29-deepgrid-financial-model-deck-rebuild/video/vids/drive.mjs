// Attach to the already-running Chromium over CDP and report/act on Google Vids.
import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const [,, cmd = 'status', arg] = process.argv;
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => !p.url().startsWith('devtools://')) || ctx.pages()[0];
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';

async function shot(name){ await page.screenshot({ path: `${out}/${name}.png`, fullPage:false }); }

if (cmd === 'status') {
  console.log('URL   :', page.url());
  console.log('TITLE :', await page.title());
  const signedIn = !/accounts\.google\.com/.test(page.url());
  console.log('SIGNED_IN:', signedIn);
  await shot('state');
} else if (cmd === 'goto') {
  await page.goto(arg, { waitUntil:'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(4000);
  console.log('URL   :', page.url());
  console.log('TITLE :', await page.title());
  await shot('state');
}
await b.close();
