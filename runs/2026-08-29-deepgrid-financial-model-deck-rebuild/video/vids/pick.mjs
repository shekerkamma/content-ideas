import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1500); await kill(page);
await page.mouse.click(516,385);            // the "Product Lines" card
await page.waitForTimeout(2500);
await page.screenshot({path:'picked.png'});
for(const nm of [/^Select$/,/^Insert$/,/^Import$/,/^Open$/,/^Continue$/]){
  const btn=page.getByRole('button',{name:nm}).first();
  if(await btn.count() && await btn.isVisible().catch(()=>false)){
    await btn.click({timeout:8000}); console.log('confirmed with',nm); break; }
}
await page.waitForTimeout(15000); await kill(page);
await page.screenshot({path:'picked2.png'});
console.log('URL:',page.url().split('?')[0]);
console.log('TITLE:',await page.title());
const t=await page.evaluate(()=>document.body.innerText.match(/Scene \d+ \/ \d+|\d\d:\d\d\.\d/g)||[]);
console.log('markers:',[...new Set(t)].slice(0,6).join(' | '));
await b.close();
