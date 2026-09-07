import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const DL  = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/export';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront();

// route downloads to our staging dir
const cdp = await ctx.newCDPSession(page);
await cdp.send('Browser.setDownloadBehavior', { behavior: 'allow', downloadPath: DL, eventsEnabled: true })
  .catch(async () => cdp.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: DL }));
console.log('download dir set ->', DL);

await page.keyboard.press('Escape'); await page.waitForTimeout(700); await kill(page);
await page.locator('#docs-file-menu').click({ timeout: 15000 });
await page.waitForTimeout(1800);
await page.getByRole('menuitem', { name: /^Download/ }).first().hover({ timeout: 10000 });
await page.waitForTimeout(2500); await kill(page);
await page.screenshot({ path: out + '/dl-submenu.png' });
const items = await page.evaluate(() =>
  [...document.querySelectorAll('[role=menuitem]')]
    .map(e => (e.innerText || '').trim().replace(/\s+/g,' '))
    .filter(s => /mp4|video|gif|download|720|1080|480/i.test(s)).slice(0, 12));
console.log('submenu options:', items.join(' | ') || '(none captured)');
await b.close();
