import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(2000); await kill(page);
const count = () => page.evaluate(()=>(document.body.innerText.match(/(\d+) out of (\d+) slides selected/)||[])[0]||'?');
const link  = () => page.evaluate(()=>{
  const e=[...document.querySelectorAll('span,div,button,a')].find(x=>/^(Select all|Deselect all)$/.test(x.innerText.trim()));
  return e ? e.innerText.trim() : null; });
console.log('start:', await count(), '| link:', await link());
// toggle off, which should flip the affordance to "Select all"
await page.evaluate(()=>{ const e=[...document.querySelectorAll('span,div,button,a')]
  .find(x=>x.innerText.trim()==='Deselect all'); if(e) e.click(); });
await page.waitForTimeout(2500);
console.log('after deselect:', await count(), '| link:', await link());
await page.evaluate(()=>{ const e=[...document.querySelectorAll('span,div,button,a')]
  .find(x=>x.innerText.trim()==='Select all'); if(e) e.click(); });
await page.waitForTimeout(3500);
console.log('after select all:', await count(), '| link:', await link());
await page.screenshot({path:'selectall.png'});
await b.close();
