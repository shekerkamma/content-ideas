import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
let page=b.contexts()[0].pages().find(p=>p.url().includes(VID));
if(!page){ page=await b.contexts()[0].newPage();
  await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000});
  await page.waitForTimeout(12000); }
await page.bringToFront(); await page.keyboard.press('Escape');
await page.waitForTimeout(2000); await kill(page);

// Do not look for "music" or a provider name: Vids may seat ANY stock clip in
// this lane (here, a YouTube-sourced speech). Identify the bed structurally --
// a timeline track that is not a per-scene voiceover and not a scene tile.
const find = () => page.evaluate(()=>{
  for(const e of document.querySelectorAll('[aria-label]')){
    const l=e.getAttribute('aria-label')||''; const r=e.getBoundingClientRect();
    if(!/starting in scene/.test(l)) continue;
    if(/ - (Holt|Nyla|Rhea|Orion) starting in scene /.test(l)) continue;  // voiceover
    return {l:l.slice(0,80), x:Math.round(r.x), y:Math.round(r.y+r.height/2), w:Math.round(r.width)};
  }
  return null;
});
let t = await find();
console.log('bed track:', JSON.stringify(t));
if(false){
  const cx = Math.max(60, Math.min(1200, t.x + 40));   // the track starts off-screen left
  await page.mouse.click(cx, t.y);
  await page.waitForTimeout(1800);
  await page.keyboard.press('Delete');
  await page.waitForTimeout(4000); await kill(page);
}
t = await find();
console.log('bed after delete:', t ? JSON.stringify(t) : 'GONE');
const txt = await page.evaluate(()=>document.body.innerText);
console.log('duration:', (txt.match(/\d\d:\d\d\.\d\s*\/\s*\d\d:\d\d\.\d/)||['-'])[0].replace(/\s+/g,''));
console.log('any Kennedy ref left:', /Kennedy/i.test(txt));
await page.screenshot({path:'checkA.png'});
await b.close();
