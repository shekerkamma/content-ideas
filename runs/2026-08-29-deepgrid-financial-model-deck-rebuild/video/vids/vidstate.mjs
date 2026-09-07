import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const ID='19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
let page=ctx.pages().find(p=>p.url().includes(ID));
if(!page){ page=await ctx.newPage(); await page.goto(`https://docs.google.com/videos/d/${ID}/edit`,{waitUntil:'domcontentloaded',timeout:90000}); }
await page.bringToFront(); await page.waitForTimeout(8000);
console.log('URL  :', page.url());
console.log('TITLE:', await page.title());
await page.screenshot({ path:`${out}/vids-state.png` });
const els = await page.evaluate(() =>
  [...document.querySelectorAll('button,[role=button],[role=option],h1,h2,[aria-label]')]
    .map(e=>(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\s+/g,' '))
    .filter(s=>s && s.length<70).slice(0,45));
console.log([...new Set(els)].join('\n'));
await b.close();
