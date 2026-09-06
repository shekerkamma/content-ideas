import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.keyboard.press('Escape'); await page.waitForTimeout(800); await kill(page);

const has = () => page.evaluate(() => /Corporate Green Technology/.test(document.body.innerText));
console.log('music present before:', await has());

// click the music track itself (the aria-labelled container)
const track = page.locator('[aria-label^="Corporate Green Technology"]').first();
await track.click({ timeout: 15000 });
await page.waitForTimeout(1500);
await page.screenshot({ path: out + '/music-selected.png' });
await page.keyboard.press('Delete');
await page.waitForTimeout(3000); await kill(page);
console.log('music present after Delete:', await has());
await page.screenshot({ path: out + '/music-deleted.png' });
const t = await page.evaluate(() => document.body.innerText);
console.log('runtime:', (t.match(/\d\d:\d\d\.\d\s*\/\s*(\d\d:\d\d\.\d)/) || ['?'])[0]);
await b.close();
