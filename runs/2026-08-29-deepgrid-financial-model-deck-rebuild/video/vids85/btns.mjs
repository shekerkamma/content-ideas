import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(2000); await kill(page);
const r = await page.evaluate(()=>{
  const out=[];
  for(const e of document.querySelectorAll('button,[role="button"]')){
    const t=(e.innerText||e.getAttribute('aria-label')||'').trim();
    const b=e.getBoundingClientRect();
    if(t && b.width>0 && b.x>1400) out.push(`${t.slice(0,42)} @${Math.round(b.x)},${Math.round(b.y)}`);
  }
  return {btns:[...new Set(out)].slice(0,30), voice:(document.body.innerText.match(/(Holt|Nyla)/)||['?'])[0]};
});
console.log('voice:', r.voice);
r.btns.forEach(x=>console.log('  •',x));
await page.screenshot({path:'voice-panel.png'});
await b.close();
