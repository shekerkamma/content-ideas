import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=1600,900','--autoplay-policy=no-user-gesture-required']});
const page=await (await browser.newContext({viewport:{width:1600,height:900}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
const preset = process.argv[3]||'peak';
await page.evaluate(p=>{const e=document.querySelector(`button[data-t=${p}]`); if(e) e.click();}, preset);
let sawCtx=false, sawHorn=false, sawStop=false, sawVoice=false, phases=new Set();
for(let i=0;i<44;i++){
  await page.waitForTimeout(1000);
  const s=await page.evaluate(()=>({
    ctx: !!(window.AUDIO&&AUDIO.ctx), state: (window.AUDIO&&AUDIO.ctx)?AUDIO.ctx.state:'-',
    phase: window.AUDIO?AUDIO.hornPhase:'-',
    stop: (typeof alerts!=='undefined')?!!alerts.stop:null,
    voice:(typeof alerts!=='undefined')?!!alerts.voice:null,
    mode: typeof HORN_MODE!=='undefined'?HORN_MODE:'-',
  })).catch(()=>({}));
  if(s.ctx) sawCtx=true;
  if(s.stop) sawStop=true;
  if(s.voice) sawVoice=true;
  if(s.phase) phases.add(s.phase);
  if(s.stop&&s.voice) sawHorn=true;
  if(i%8===0) console.log(`  t+${i+1}s`, JSON.stringify(s));
}
console.log('\nAudioContext created:',sawCtx,'| horn phases seen:',[...phases].join(','));
console.log('alerts.stop ever true:',sawStop,'| alerts.voice ever true:',sawVoice,'| HORN ACTIVE ever:',sawHorn);
await browser.close();
