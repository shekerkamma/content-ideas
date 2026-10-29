import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=1600,900','--autoplay-policy=no-user-gesture-required']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
await page.mouse.click(800,450); await page.waitForTimeout(800);
await page.evaluate(()=>{const e=document.querySelector('button[data-t=putaway]'); if(e) e.click();});
await page.waitForTimeout(4000);
// Which lexical globals look like the vehicle, and can we call worker()?
const g = await page.evaluate(()=>{
  const probe={};
  for(const n of ['truck','rig','bot','car','me','ego','unit','agent','amrState','state','sim','WORLD','world','pose','nav','waypoints','WP','wps'])
    { try{ const v=eval(n); probe[n]= (typeof v==='function')?'fn':(v&&typeof v==='object')?Object.keys(v).slice(0,10):typeof v; }catch(e){ probe[n]='undef'; } }
  return probe;
});
console.log('named globals:', JSON.stringify(g));
// find the ego vehicle by shape: an object carrying x, z and a heading
const ego = await page.evaluate(()=>{
  const out=[];
  for(const k of Object.getOwnPropertyNames(globalThis)){
    try{ const v=globalThis[k];
      if(v&&typeof v==='object'&&'x' in v&&'z' in v&&!Array.isArray(v)) out.push([k,Object.keys(v).slice(0,12)]);
    }catch(e){}
  }
  return out.slice(0,8);
});
console.log('window objects with x/z:', JSON.stringify(ego));
console.log('actors[0]:', JSON.stringify(await page.evaluate(()=>Object.keys(actors[0]||{}).slice(0,16))));
await browser.close();
