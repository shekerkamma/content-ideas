import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
await page.mouse.click(1453,723);
console.log('clicked Select');
for(let i=0;i<18;i++){
  await page.waitForTimeout(10000); await kill(page);
  const m=await page.evaluate(()=>{const x=document.body.innerText.match(/Scene (\d+) \/ (\d+)/);return x?x[0]:null;});
  const dur=await page.evaluate(()=>{const x=document.body.innerText.match(/\/\s*(\d\d:\d\d\.\d)/);return x?x[1]:null;});
  console.log('  t+'+((i+1)*10)+'s scenes='+(m||'-')+' dur='+(dur||'-'));
  if(dur && dur!=='00:05.0') break;
}
await page.screenshot({path:'imported.png'});
console.log('TITLE:',await page.title());
await b.close();
