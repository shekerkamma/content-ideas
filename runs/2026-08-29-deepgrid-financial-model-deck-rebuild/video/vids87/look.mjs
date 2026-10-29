import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID=process.argv[2];
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
let page=ctx.pages().find(p=>p.url().includes(VID));
if(!page){ page=await ctx.newPage(); await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000}); await page.waitForTimeout(12000);}
await page.bringToFront(); await page.waitForTimeout(3000); await kill(page);
const t=await page.evaluate(()=>document.body.innerText.replace(/\n+/g,' | '));
console.log('TEXT:', t.slice(0,700));
const btns=await page.evaluate(()=>[...document.querySelectorAll('button,[role=button]')]
  .map(e=>({t:((e.innerText||'').trim()).slice(0,22), w:Math.round(e.getBoundingClientRect().width)}))
  .filter(x=>x.t && x.w>60).slice(0,14));
console.log('BUTTONS:', JSON.stringify(btns));
await page.screenshot({path:'lookA.png'});
await b.close();
