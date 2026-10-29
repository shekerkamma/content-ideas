import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const page=await (await browser.newContext({viewport:{width:1600,height:900},reducedMotion:'no-preference'})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
const btns=await page.evaluate(()=>[...document.querySelectorAll('button')]
  .map(b=>({t:(b.innerText||'').trim().slice(0,18), id:b.id})).slice(0,8));
console.log('buttons:', JSON.stringify(btns));
console.log('doc size:', JSON.stringify(await page.evaluate(()=>({w:document.documentElement.scrollWidth,h:document.documentElement.scrollHeight}))));
// press whatever looks like play, then sample
await page.evaluate(()=>{const b=[...document.querySelectorAll('button')]
  .find(x=>/play|▶|start/i.test((x.innerText||'')+(x.id||''))); if(b) b.click();});
await page.waitForTimeout(1500);
for(let i=0;i<3;i++){ await page.screenshot({path:`/tmp/claude-1000/-home-sheke-content-ideas/877343a8-f961-422a-be31-61d6af046921/scratchpad/sa_${i}.png`}); await page.waitForTimeout(1500); }
await browser.close();
