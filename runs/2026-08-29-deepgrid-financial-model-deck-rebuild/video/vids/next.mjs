import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
for(let step=0; step<4; step++){
  const nx=page.getByRole('button',{name:/^(Next|Create|Generate|Done|Finish)$/i}).first();
  if(!(await nx.count()) || !(await nx.isVisible().catch(()=>false))) { console.log('no more step buttons'); break; }
  const label=(await nx.innerText()).trim();
  await nx.click({timeout:15000});
  console.log('clicked:',label);
  await page.waitForTimeout(9000); await kill(page);
  await page.screenshot({path:`step${step}.png`});
}
for(let i=0;i<24;i++){
  await page.waitForTimeout(10000); await kill(page);
  const t=await page.evaluate(()=>document.body.innerText);
  const dur=(t.match(/\/\s*(\d\d:\d\d\.\d)/)||[])[1];
  const sc=(t.match(/Scene \d+ \/ \d+/)||['-'])[0];
  console.log('  t+'+((i+1)*10)+'s dur='+(dur||'-')+' '+sc);
  if(dur && dur!=='00:05.0'){ console.log('IMPORT COMPLETE'); break; }
}
await page.screenshot({path:'imported.png'});
await b.close();
