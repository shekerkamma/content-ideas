import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
const target=+process.argv[3];
// the deck paginates with arrow keys; step and read the counter
for(let i=0;i<target-1;i++){ await page.keyboard.press('ArrowRight'); await page.waitForTimeout(700); }
await page.waitForTimeout(2500);
const info=await page.evaluate(()=>{
  const t=document.body.innerText;
  const m=t.match(/(\d+)\s*\/\s*(\d+)/);
  const h=[...document.querySelectorAll('h1,h2')].map(e=>e.innerText.replace(/\s+/g,' ').trim()).filter(Boolean);
  return {counter:m?m[0]:'?', heads:h.slice(0,3)};
});
console.log(JSON.stringify(info));
await page.screenshot({path:process.argv[4]});
await browser.close();
