import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const ctx=await browser.newContext({viewport:{width:1600,height:900},reducedMotion:'no-preference'});
const page=await ctx.newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2000);
await page.mouse.click(800,450); await page.waitForTimeout(300);
for(let k=0;k<24;k++){ await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(50); }
for(let k=0;k<+process.argv[3];k++){ await page.keyboard.press('ArrowRight'); await page.waitForTimeout(320); }
await page.waitForTimeout(3000);
const diag=await page.evaluate(()=>({
  reduced: matchMedia('(prefers-reduced-motion: reduce)').matches,
  // how many elements on the ACTIVE slide actually have a running animation?
  running: [...document.querySelectorAll('.slide.active *')]
    .filter(e=>e.getAnimations && e.getAnimations().length>0).length,
  names: [...new Set([...document.querySelectorAll('.slide.active *')]
    .flatMap(e=>e.getAnimations?e.getAnimations().map(a=>a.animationName||'?'):[]))].slice(0,10),
  cur:(document.getElementById('cur')||{}).textContent,
}));
console.log(JSON.stringify(diag));
for(let i=0;i<3;i++){ await page.screenshot({path:`${process.argv[4]}/m${process.argv[3]}_${i}.png`}); await page.waitForTimeout(1200); }
await browser.close();
