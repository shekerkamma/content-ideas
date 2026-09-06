import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1500); await kill(page);
// find any element whose text is exactly Next / Create / Generate, anywhere
const info=await page.evaluate(()=>{
  const out=[];
  document.querySelectorAll('*').forEach(e=>{
    const t=(e.textContent||'').trim();
    if(!/^(Next|Create|Generate|Done)$/i.test(t)) return;
    if(e.children.length>1) return;
    const r=e.getBoundingClientRect(); if(r.width<20) return;
    out.push({t,x:Math.round(r.x+r.width/2),y:Math.round(r.y+r.height/2),tag:e.tagName});
  });
  return out;
});
console.log('candidates:',JSON.stringify(info));
if(info.length){
  await page.mouse.click(info[0].x,info[0].y);
  console.log('clicked',info[0].t,'at',info[0].x,info[0].y);
  await page.waitForTimeout(10000); await kill(page);
  await page.screenshot({path:'afternext.png'});
  const t=await page.evaluate(()=>document.body.innerText);
  console.log('dur:',(t.match(/\/\s*(\d\d:\d\d\.\d)/)||['-'])[1]||'-');
  console.log('dialog still open:', /Select slides|Generating|Creating/i.test(t));
}
await b.close();
