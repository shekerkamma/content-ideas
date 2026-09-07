import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const [,,SRC,OUT,MODE,ARG,SECS]=process.argv;
const W=1600,H=900;
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:[`--window-size=${W},${H}`,'--autoplay-policy=no-user-gesture-required']});
const ctx=await browser.newContext({viewport:{width:W,height:H},
  reducedMotion:'no-preference', recordVideo:{dir:OUT,size:{width:W,height:H}}});
const page=await ctx.newPage();
await page.goto('file://'+SRC,{waitUntil:'load'});
await page.waitForTimeout(2500);

if(MODE==='deck'){
  // trusted click for focus, rewind to slide 1, then step to the target
  await page.mouse.click(800,450); await page.waitForTimeout(300);
  for(let k=0;k<24;k++){ await page.keyboard.press('ArrowLeft'); await page.waitForTimeout(45); }
  for(let k=0;k<+ARG;k++){ await page.keyboard.press('ArrowRight'); await page.waitForTimeout(300); }
  await page.waitForTimeout(1500);
  const n=await page.evaluate(()=>(document.getElementById('cur')||{}).textContent);
  const run=await page.evaluate(()=>[...document.querySelectorAll('.slide.active *')]
    .filter(e=>e.getAnimations&&e.getAnimations().length>0).length);
  console.log(`landed on slide ${n} with ${run} running animations`);
}else{
  await page.evaluate(y=>scrollTo(0,y), +ARG);
  await page.waitForTimeout(800);
  const hit=await page.evaluate(()=>{const b=document.getElementById('btnPlay'); if(b){b.click();return true;} return false;});
  console.log('play clicked:', hit);
}
await page.waitForTimeout((+SECS)*1000);
await ctx.close(); await browser.close();
console.log('captured ->', OUT);
