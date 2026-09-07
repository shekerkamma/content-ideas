import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID = '1RqX9_46Id1fGCqQpBno_4fPAFvK6jxcoQbzVLf6_1jo';
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids85';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(1000); await kill(page);

// 1. dismiss the confirm dialog so we can set the voice first
const cancel = page.getByRole('button', { name: /^Cancel$/ }).first();
if (await cancel.count() && await cancel.isVisible().catch(()=>false)) {
  await cancel.click({ timeout: 8000 }); console.log('cancelled dialog'); await page.waitForTimeout(2000);
}
await kill(page);

// 2. force the voice to Holt
await page.getByText('Change', { exact: true }).first().click({ timeout: 20000 });
await page.waitForTimeout(4500); await kill(page);
const hb = await page.getByText('Holt', { exact: true }).first().boundingBox();
await page.mouse.click(hb.x + 40, hb.y + 8);
await page.waitForTimeout(2000);
await page.getByRole('button', { name: /^Select$/ }).first().click({ timeout: 15000 });
await page.waitForTimeout(4000); await kill(page);
console.log('voice set to:', await page.evaluate(() => (document.body.innerText.match(/(Holt|Nyla)/)||['?'])[0]));

// 3. regenerate, and confirm through the dialog this time
const btn = page.getByRole('button', { name: /^Update all voiceovers$/i }).first();
const bb = await btn.boundingBox();
await page.mouse.click(bb.x + bb.width/2, bb.y + bb.height/2);
await page.waitForTimeout(2500);
const rep = page.getByRole('button', { name: /^Replace$/ }).first();
if (await rep.count() && await rep.isVisible().catch(()=>false)) {
  await rep.click({ timeout: 10000 }); console.log('confirmed Replace');
} else console.log('no Replace dialog appeared');
await page.waitForTimeout(240000); await kill(page);
await page.screenshot({ path: out + '/voiceB.png' });
const t = await page.evaluate(() => document.body.innerText);
console.log('outdated markers left:', (t.match(/Voiceover outdated/g)||[]).length);
console.log('voice :', (t.match(/(Holt|Nyla)/)||['?'])[0]);
console.log('music :', /Corporate Green Technology/.test(t) ? 'present' : 'MISSING');
await b.close();
