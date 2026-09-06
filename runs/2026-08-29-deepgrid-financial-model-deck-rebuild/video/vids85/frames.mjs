import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(2000);
for (const f of page.frames()) {
  const t = await f.evaluate(()=>document.body?document.body.innerText.slice(0,400):'').catch(()=> '');
  if (/slides selected|Select all|Deselect all|Next/i.test(t))
    console.log('HIT frame:', f.url().slice(0,70), '\n---\n', t.replace(/\n+/g,' | ').slice(0,300));
}
console.log('frames total:', page.frames().length);
await b.close();
