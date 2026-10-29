import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID='1wzKEruiXeRF6SebbIdnsGNADVuOm3twn';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.keyboard.press('Escape');
await page.waitForTimeout(1500); await kill(page);
await page.getByText('Transform',{exact:true}).first().click({timeout:25000});
console.log('Transform panel opened');
await page.waitForTimeout(6000); await kill(page);
// The panel HEADER is also "Turn into video"; pick the lowest wide button.
const clicked = await page.evaluate(()=>{
  const c=[...document.querySelectorAll('div[role="button"],button')]
    .filter(e=>e.innerText.trim().toLowerCase()==='turn into video')
    .map(e=>({e,r:e.getBoundingClientRect()}))
    .filter(o=>o.r.width>120&&o.r.height>24)
    .sort((a,b)=>b.r.top-a.r.top);
  if(!c.length) return null; c[0].e.click(); return Math.round(c[0].r.top);
});
console.log('clicked CTA at y =', clicked);
const before=new Set(ctx.pages().map(p=>p.url().split('?')[0]).filter(u=>u.includes('/videos/d/')));
for(let i=0;i<50;i++){
  await page.waitForTimeout(10000);
  const fresh=ctx.pages().map(p=>p.url().split('?')[0]).find(u=>u.includes('/videos/d/')&&!before.has(u));
  if(fresh){ console.log('NEW VIDS DOC:',fresh); break; }
  if(i%4===0) console.log('  t+'+((i+1)*10)+'s');
}
await b.close();
