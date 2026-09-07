import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
const browser=await chromium.launch({executablePath:EXEC,headless:false,
  args:['--window-size=900,600','--autoplay-policy=no-user-gesture-required','--enable-speech-dispatcher']});
const page=await (await browser.newContext({viewport:{width:900,height:600}})).newPage();
await page.goto('about:blank');
await page.mouse.click(400,300); await page.waitForTimeout(500);
const v = await page.evaluate(async ()=>{
  await new Promise(r=>{ if(speechSynthesis.getVoices().length) return r();
    speechSynthesis.onvoiceschanged=r; setTimeout(r,3000); });
  const list=speechSynthesis.getVoices().map(x=>x.name+' ['+x.lang+']');
  await new Promise(r=>setTimeout(r,5000));
  return {count:list.length, sample:list.slice(0,5)};
});
console.log('voices:', JSON.stringify(v));
await browser.close();
