import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const page=await (await browser.newContext({viewport:{width:1600,height:900},reducedMotion:'no-preference'})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
const svgs=await page.evaluate(()=>[...document.querySelectorAll('svg')].map((s,i)=>{
  const r=s.getBoundingClientRect();
  return {i, y:Math.round(r.y+scrollY), h:Math.round(r.height), w:Math.round(r.width),
          id:s.id||s.parentElement?.id||''};}));
console.log('svgs:', JSON.stringify(svgs));
const heads=await page.evaluate(()=>[...document.querySelectorAll('h1,h2,h3')]
  .map(e=>({y:Math.round(e.getBoundingClientRect().y+scrollY), t:e.innerText.replace(/\s+/g,' ').slice(0,48)})));
console.log('headings:', JSON.stringify(heads.slice(0,8)));
await page.screenshot({path:`/tmp/claude-1000/-home-sheke-content-ideas/877343a8-f961-422a-be31-61d6af046921/scratchpad/sa_full.png`, fullPage:true});
await browser.close();
