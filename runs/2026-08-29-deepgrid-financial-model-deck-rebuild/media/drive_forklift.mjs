import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const ctx = await chromium.launchPersistentContext('/home/sheke/.cache/sim-capture-profile', {
  executablePath: EXEC, headless:false, viewport:null,
  args:[`--app=file://${process.argv[2]}`,'--window-position=0,0','--window-size=1600,900',
        '--autoplay-policy=no-user-gesture-required','--enable-speech-dispatcher'],
});
const page = ctx.pages()[0];
page.on('console',m=>{const t=m.text(); if(t.startsWith('SPY')) console.log('  '+Math.round(process.uptime())+'s '+t);});
await page.waitForTimeout(2500);
// trusted pointerdown arms audioInit(); an in-page click() would not
await page.mouse.click(800,450);
await page.waitForTimeout(600);
await page.evaluate(()=>{ const o=speechSynthesis.speak.bind(speechSynthesis);
  speechSynthesis.speak=u=>{console.log('SPY speak: '+JSON.stringify(u.text)); return o(u);}; });
const preset=p=>page.evaluate(x=>{const e=document.querySelector(`button[data-t=${x}]`); if(e) e.click();},p);
const ahead=async(d=3.0)=>{ await page.evaluate(async D=>{
    const a={x:ego.position.x,z:ego.position.z};
    await new Promise(r=>setTimeout(r,900));
    let dx=ego.position.x-a.x, dz=ego.position.z-a.z, m=Math.hypot(dx,dz);
    if(m<0.03){dx=0;dz=1;m=1;}
    worker(true,[ego.position.x+dx/m*D, ego.position.z+dz/m*D]);
  },d); };
const wait=ms=>page.waitForTimeout(ms);
await preset('peak');   await wait(13000);
await ahead(2.6);       await wait(11000);
await ahead(2.2);       await wait(9000);
await preset('pick');   await wait(12000);
await ahead(2.4);       await wait(10000);
await preset('putaway');await wait(8000);
console.log('drive complete at', Math.round(process.uptime()),'s');
await ctx.close();
