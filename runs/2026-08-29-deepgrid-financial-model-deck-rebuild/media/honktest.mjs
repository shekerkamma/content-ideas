import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser = await chromium.launch({ executablePath: EXEC, headless:false,
  args:['--window-size=1280,720','--autoplay-policy=no-user-gesture-required'] });
const page = await (await browser.newContext({viewport:{width:1280,height:720}})).newPage();
await page.goto('file://'+process.argv[2],{waitUntil:'load'});
await page.waitForTimeout(2500);
// what does the page think it can do?
console.log('capabilities:', JSON.stringify(await page.evaluate(()=>({
  speechSynthesis: typeof speechSynthesis!=='undefined',
  voices: (typeof speechSynthesis!=='undefined' ? speechSynthesis.getVoices().length : -1),
  audioCtx: typeof (window.AudioContext||window.webkitAudioContext)!=='undefined',
}))));
await page.evaluate(()=>{ const e=document.querySelector('button[data-t=peak]'); if(e) e.click(); });
await page.waitForTimeout(22000);
await browser.close();
