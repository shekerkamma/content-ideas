import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes('/presentation/d/'));
await page.bringToFront(); await page.waitForTimeout(2000);
await page.mouse.click(551, 23);                    // the .PPTX compatibility chip
await page.waitForTimeout(2500);
await page.screenshot({ path:`${out}/pptx-chip.png` });
const items = await page.evaluate(() =>
  [...document.querySelectorAll('[role=menuitem],button,[role=button]')]
    .map(e=>(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\s+/g,' '))
    .filter(s=>/save as google|google slides|convert/i.test(s)).slice(0,6));
console.log('conversion affordances:', items.join(' || ') || 'none found');
if (items.length){
  await page.getByText(/Save as Google Slides/i).first().click({ timeout:15000 });
  await page.waitForTimeout(18000);
  console.log('URL  :', page.url());
  console.log('TITLE:', await page.title());
  await page.screenshot({ path:`${out}/converted.png` });
}
await b.close();
