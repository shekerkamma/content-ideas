import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID='1bLfYm2pFV8JfhdMOMHOhvR2xgT1bwqRe';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
await page.getByText('Transform',{exact:true}).first().click({timeout:15000}).catch(()=>{});
await page.waitForTimeout(6000);
await page.screenshot({path:'panel.png'});
const t=await page.evaluate(()=>{
  const el=[...document.querySelectorAll('div,span,button')]
    .filter(e=>{const r=e.getBoundingClientRect();return r.x>1200&&r.width>40&&e.children.length<3;})
    .map(e=>(e.innerText||'').trim().replace(/\s+/g,' ')).filter(s=>s&&s.length<90);
  return [...new Set(el)].slice(0,20);
});
console.log(t.join('\n'));
await b.close();
