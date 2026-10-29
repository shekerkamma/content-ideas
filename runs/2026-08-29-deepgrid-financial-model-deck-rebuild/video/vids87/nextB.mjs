import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='19opB7Nr2HiXGwJG9sAAC0pgc0-I6v9LUqxfC4fV_v3I';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
let page = ctx.pages().find(p=>p.url().includes(VID));
if(!page){ page=await ctx.newPage(); await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000}); }
await page.bringToFront(); await page.waitForTimeout(9000); await kill(page);
const state = () => page.evaluate(()=>{
  const t = document.body ? document.body.innerText : '';
  const nextBtn = [...document.querySelectorAll('button,[role="button"]')]
    .some(x => (x.innerText||'').trim() === 'Next' && x.getBoundingClientRect().width > 60);
  return { next: nextBtn, busy: /Setting the scene|Generating/i.test(t),
           scenes: document.querySelectorAll('[aria-label^="Scene "]').length };
});
console.log('state:', JSON.stringify(await state()));
// Walk the dialog: click Next until it is gone.
for(let i=0;i<4;i++){
  const hit = await page.evaluate(()=>{
    const e=[...document.querySelectorAll('button,[role="button"]')]
      .find(x=>(x.innerText||'').trim()==='Next' && x.getBoundingClientRect().width>60);
    if(e){ e.click(); return true; } return false;
  });
  console.log('  Next click', i+1, hit?'hit':'no button');
  if(!hit) break;
  await page.waitForTimeout(6000); await kill(page);
}
console.log('state after:', JSON.stringify(await state()));
await page.screenshot({path:'nextB.png'});
await b.close();
