import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync, writeFileSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const SRC=process.argv[2], OUT=process.argv[3];
const W=1600,H=900;
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:[`--window-size=${W},${H}`,'--autoplay-policy=no-user-gesture-required','--enable-speech-dispatcher']});
const ctx=await browser.newContext({viewport:{width:W,height:H},recordVideo:{dir:OUT,size:{width:W,height:H}}});
const page=await ctx.newPage();
page.on('console',m=>{const t=m.text(); if(t.startsWith('SPY')) console.log('  SPY '+t.slice(4));});
await page.goto('file://'+SRC,{waitUntil:'load'});
await page.waitForTimeout(2000);
await page.mouse.click(800,450);            // trusted gesture arms audioInit()
await page.waitForTimeout(600);
await page.evaluate(()=>{ const o=speechSynthesis.speak.bind(speechSynthesis);
  speechSynthesis.speak=u=>{console.log('SPY speak '+JSON.stringify(u.text)); return o(u);}; });

// SYNC MARKER: a white full-screen flash and a 1 kHz beep fired in the same
// tick. Post-processing aligns the flash frame with the beep, so the audio is
// muxed at a MEASURED offset instead of an assumed one.
const t0 = Date.now();
await page.evaluate(()=>{
  const d=document.createElement('div');
  d.style.cssText='position:fixed;inset:0;background:#fff;z-index:2147483647';
  document.body.appendChild(d);
  const C=window.AudioContext||window.webkitAudioContext; const c=new C();
  const o=c.createOscillator(), g=c.createGain();
  o.frequency.value=1000; g.gain.value=0.7; o.connect(g); g.connect(c.destination); o.start();
  setTimeout(()=>{o.stop(); d.remove();},250);
});
console.log('marker fired at +'+((Date.now()-t0)/1000).toFixed(2)+'s');
await page.waitForTimeout(1500);

const preset=p=>page.evaluate(x=>{const e=document.querySelector(`button[data-t=${x}]`); if(e) e.click();},p);
const ahead=async(D)=>page.evaluate(async d=>{
  const a={x:ego.position.x,z:ego.position.z};
  await new Promise(r=>setTimeout(r,900));
  let dx=ego.position.x-a.x, dz=ego.position.z-a.z, m=Math.hypot(dx,dz);
  if(m<0.03){dx=0;dz=1;m=1;}
  worker(true,[ego.position.x+dx/m*d, ego.position.z+dz/m*d]);
},D);
const wait=ms=>page.waitForTimeout(ms);
await preset('peak');    await wait(12000);
await ahead(2.6);        await wait(11000);
await ahead(2.2);        await wait(9000);
await preset('pick');    await wait(11000);
await ahead(2.4);        await wait(10000);
await preset('putaway'); await wait(8000);
console.log('drive done');
await ctx.close(); await browser.close();
