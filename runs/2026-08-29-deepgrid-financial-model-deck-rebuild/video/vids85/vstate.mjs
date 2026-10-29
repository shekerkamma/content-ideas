import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
let page = ctx.pages().find(p=>p.url().includes(VID));
if(!page){ page=await ctx.newPage(); await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000}); }
await page.bringToFront(); await page.waitForTimeout(8000); await kill(page);
const info = await page.evaluate(()=>{
  const scenes=[...document.querySelectorAll('[aria-label^="Scene "]')].map(e=>e.getAttribute('aria-label'));
  const t=document.body.innerText;
  const dur=(t.match(/\d{2}:\d{2}\.\d/)||[])[0]||'-';
  const outdated=(t.match(/Voiceover outdated/g)||[]).length;
  return {scenes:scenes.length, first:scenes[0]||'-', last:scenes[scenes.length-1]||'-', dur, outdated};
});
console.log(JSON.stringify(info));
console.log('title:', await page.title());
await page.screenshot({path:'vids-state.png'});
await b.close();
