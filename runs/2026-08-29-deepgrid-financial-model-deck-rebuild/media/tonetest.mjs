import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=900,600','--autoplay-policy=no-user-gesture-required']});
const page=await (await browser.newContext({viewport:{width:900,height:600}})).newPage();
await page.goto('about:blank');
const r = await page.evaluate(async ()=>{
  const C=window.AudioContext||window.webkitAudioContext; const c=new C();
  if(c.state==='suspended') await c.resume().catch(()=>{});
  const o=c.createOscillator(), g=c.createGain();
  o.frequency.value=440; g.gain.value=0.8; o.connect(g); g.connect(c.destination); o.start();
  await new Promise(r=>setTimeout(r,6000));
  return {state:c.state, sampleRate:c.sampleRate};
});
console.log('AudioContext:', JSON.stringify(r));
await browser.close();
