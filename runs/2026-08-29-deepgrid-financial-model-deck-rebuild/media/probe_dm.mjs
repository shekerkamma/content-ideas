import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,args:['--window-size=1600,900']});
const page=await (await browser.newContext({viewport:{width:1600,height:900},reducedMotion:'no-preference'})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(3000);
const id=process.argv[3];
await page.evaluate(i=>document.getElementById(i).scrollIntoView({block:'center'}), id);
await page.waitForTimeout(4000);
const fr=page.frames().find(f=>f!==page.mainFrame() && f.name()===id) || page.frameLocator(`#${id}`);
const el=await page.$(`#${id}`);
const box=await el.boundingBox();
console.log('frame box:', JSON.stringify(box));
// count running animations inside the iframe document
const frames=page.frames();
for(const f of frames){
  const r=await f.evaluate(()=>({url:location.href.slice(0,24),
    running:[...document.querySelectorAll('*')].filter(e=>e.getAnimations&&e.getAnimations().length>0).length,
    raf: typeof requestAnimationFrame==='function',
    canvas: document.querySelectorAll('canvas').length,
    svg: document.querySelectorAll('svg').length})).catch(()=>null);
  if(r && (r.running>0||r.canvas>0||r.svg>0)) console.log('  frame:',JSON.stringify(r));
}
for(let i=0;i<3;i++){ await page.screenshot({path:`/tmp/claude-1000/-home-sheke-content-ideas/877343a8-f961-422a-be31-61d6af046921/scratchpad/dm_${i}.png`}); await page.waitForTimeout(1500); }
await browser.close();
