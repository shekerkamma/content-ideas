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

let fired=0, placements=0;
for(let i=0;i<50;i++){
  await page.waitForTimeout(1000);
  const s=await page.evaluate(()=>({
    x:+ego.position.x.toFixed(2), z:+ego.position.z.toFixed(2), ry:+ego.rotation.y.toFixed(2),
    stop:!!alerts.stop, voice:!!alerts.voice, phase:AUDIO.hornPhase,
    gain: AUDIO.hornGain?+AUDIO.hornGain.gain.value.toFixed(3):null, actors:actors.length,
  })).catch(()=>({}));
  if(s.stop&&s.voice) fired++;
  if(i%6===0) console.log(`  t+${i+1}s`, JSON.stringify(s));
  // drop a hi-vis worker ~4.5 m ahead along the heading, every 8 s
  if(i%8===5 && placements<5){
    await page.evaluate(()=>{
      const d=4.5, hx=ego.position.x - Math.sin(ego.rotation.y)*d, hz=ego.position.z - Math.cos(ego.rotation.y)*d;
      worker(true,[hx,hz]);
    }).catch(e=>console.log('  place failed',e.message));
    placements++; console.log(`  placed worker #${placements} ahead of the truck`);
  }
}
console.log('\nplacements:',placements,'| seconds with HORN ACTIVE:',fired);
await browser.close();
