import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID='152QXh5JxQiJ9jqNR0HKMx8SydcG-6laY';
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=await ctx.newPage();
await page.goto(`https://docs.google.com/presentation/d/${ID}/edit`,{waitUntil:'domcontentloaded',timeout:90000});
await page.waitForTimeout(12000);
console.log('URL  :', page.url());
console.log('TITLE:', await page.title());
await page.screenshot({ path:`${out}/slides-open.png` });
const hints = await page.evaluate(() => {
  const t=[];
  document.querySelectorAll('[aria-label],[role=menuitem],button').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<6||r.height<6) return;
    const s=(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\s+/g,' ');
    if(/office|save as google|slides|compat/i.test(s)) t.push(s.slice(0,70));
  });
  return [...new Set(t)].slice(0,12);
});
console.log('hints:', hints.join(' | '));
await b.close();
