import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=1600,900','--autoplay-policy=no-user-gesture-required','--enable-speech-dispatcher']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
page.on('console',m=>{ const t=m.text(); if(t.startsWith('SPY')) console.log(' ',t); });
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2000);
await page.mouse.click(800,450); await page.waitForTimeout(800);
// Record every utterance the page attempts, without changing behaviour.
await page.evaluate(()=>{
  const orig=speechSynthesis.speak.bind(speechSynthesis);
  speechSynthesis.speak=u=>{ console.log('SPY speak:', JSON.stringify(u.text)); return orig(u); };
});
await page.evaluate(()=>{const e=document.querySelector('button[data-t='+ (window.__p||'peak') +']'); if(e) e.click();});
await page.waitForTimeout(3000);
let prev=null, placed=0;
for(let i=0;i<55;i++){
  await page.waitForTimeout(1000);
  const s=await page.evaluate(()=>({x:+ego.position.x.toFixed(2),z:+ego.position.z.toFixed(2),
    a:Object.fromEntries(Object.entries(alerts).map(([k,v])=>[k,typeof v==='object'?!!v:v])),
    gain:AUDIO.hornGain?+AUDIO.hornGain.gain.value.toFixed(3):null})).catch(()=>({}));
  if(i%10===0) console.log(`  t+${i+1}s`, JSON.stringify(s).slice(0,190));
  if(prev && i%5===4 && placed<8){
    const dx=s.x-prev.x, dz=s.z-prev.z, m=Math.hypot(dx,dz);
    // place ON the truck's nose when it is barely moving, else ahead of it
    const d = m>0.05 ? 3.0 : 1.6;
    const hx = m>0.05 ? s.x+dx/m*d : s.x, hz = m>0.05 ? s.z+dz/m*d : s.z+d;
    await page.evaluate(([a,b])=>worker(true,[a,b]),[hx,hz]).catch(()=>{});
    placed++;
  }
  if(s.x!==undefined) prev=s;
}
console.log('workers placed:',placed);
await browser.close();
