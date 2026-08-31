import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(1000); await kill(page);
await page.keyboard.press('Escape'); await page.waitForTimeout(500);
await page.getByRole('menuitem', { name: /^File$/ }).first().click({ timeout: 15000 }).catch(async () => {
  await page.getByText('File', { exact: true }).first().click({ timeout: 10000 });
});
await page.waitForTimeout(2500); await kill(page);
await page.screenshot({ path: out + '/filemenu.png' });
const items = await page.evaluate(() =>
  [...document.querySelectorAll('[role=menuitem]')]
    .map(e => (e.innerText || '').trim().replace(/\s+/g, ' '))
    .filter(Boolean).slice(0, 25));
console.log(items.join('\n'));
await b.close();
