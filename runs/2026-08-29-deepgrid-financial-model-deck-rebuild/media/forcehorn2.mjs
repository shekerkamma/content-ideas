import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=1600,900','--autoplay-policy=no-user-gesture-required']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
// trusted gesture: arms audioInit() via the page's once-only pointerdown hook
await page.mouse.click(800,450); await page.waitForTimeout(800);
await page.evaluate(()=>{const e=document.querySelector('button[data-t=putaway]'); if(e) e.click();});
await page.waitForTimeout(3500);

let fired=0, placements=0, prev=null;
for(let i=0;i<50;i++){
  await page.waitForTimeout(1000);
  const s=await page.evaluate(()=>({
    x:+ego.position.x.toFixed(2), z:+ego.position.z.toFixed(2), ry:+ego.rotation.y.toFixed(2),
    stop:!!alerts.stop, voice:!!alerts.voice, phase:AUDIO.hornPhase,
    gain: AUDIO.hornGain?+AUDIO.hornGain.gain.value.toFixed(3):null, actors:actors.length,
  })).catch(()=>({}));
  if(s.stop&&s.voice) fired++;
  if(i%6===0) console.log(`  t+${i+1}s`, JSON.stringify(s));
  // Derive "ahead" from measured motion, not from the heading convention --
  // the first attempt guessed the sign and dropped every worker behind the truck.
  if(prev && i%6===5 && placements<6){
    const dx=s.x-prev.x, dz=s.z-prev.z, m=Math.hypot(dx,dz);
    if(m>0.02){
      const d=3.5, hx=s.x+dx/m*d, hz=s.z+dz/m*d;
      await page.evaluate(([hx,hz])=>worker(true,[hx,hz]),[hx,hz]).catch(()=>{});
      placements++; console.log(`  worker #${placements} at (${hx.toFixed(1)},${hz.toFixed(1)}) ahead of truck (${s.x},${s.z})`);
    }
  }
  prev = s.x!==undefined ? s : prev;
}
console.log('\nplacements:',placements,'| seconds with HORN ACTIVE:',fired);
await browser.close();
