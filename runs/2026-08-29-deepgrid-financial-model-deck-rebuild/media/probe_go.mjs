import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2000);
for (const idx of process.argv[3].split(',').map(Number)) {
  // `go` lives inside a closure, so drive the deck the way a viewer does and
  // read #cur to confirm the landing rather than assuming the step count.
  await page.mouse.click(800,450); await page.waitForTimeout(400);
  await page.keyboard.press('Home').catch(()=>{});
  for(let k=0;k<24;k++){ await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(60); }
  for(let k=0;k<idx;k++){ await page.keyboard.press('ArrowRight'); await page.waitForTimeout(320); }
  await page.waitForTimeout(2500);
  const info=await page.evaluate(()=>({
    cur:(document.getElementById('cur')||{}).textContent,
    head:(document.querySelector('.slide.active h2, .slide.active h1')||{}).innerText?.replace(/\s+/g,' ').slice(0,70),
    kicker:(document.querySelector('.slide.active .kicker, .slide.active .eyebrow')||{}).innerText?.replace(/\s+/g,' ').slice(0,60),
  }));
  console.log(`go(${idx}) -> cur=${info.cur} | ${info.kicker||''} | ${info.head||''}`);
  await page.screenshot({path:`${process.argv[4]}/spec_go${idx}_a.png`});
  await page.waitForTimeout(3000);
  await page.screenshot({path:`${process.argv[4]}/spec_go${idx}_b.png`});
}
await browser.close();
