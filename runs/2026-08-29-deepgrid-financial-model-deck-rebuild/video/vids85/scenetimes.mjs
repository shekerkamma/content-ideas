import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID=process.argv[2];
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
let page=ctx.pages().find(p=>p.url().includes(VID));
if(!page){ page=await ctx.newPage();
  await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000});
  await page.waitForTimeout(14000); }
await page.bringToFront(); await page.waitForTimeout(3000); await kill(page);
const rows = await page.evaluate(()=>{
  const out=[];
  for(const e of document.querySelectorAll('[aria-label]')){
    const l=e.getAttribute('aria-label')||'';
    const m=l.match(/ - (?:Holt|Nyla|Rhea|Orion) starting in scene (\d+) at (?:(\d+) minutes? )?(\d+) seconds? with duration (\d+) seconds?/);
    if(m) out.push({scene:+m[1], start:(+(m[2]||0))*60+(+m[3]), dur:+m[4]});
  }
  return out.sort((a,b)=>a.scene-b.scene);
});
console.log(JSON.stringify(rows));
await b.close();
