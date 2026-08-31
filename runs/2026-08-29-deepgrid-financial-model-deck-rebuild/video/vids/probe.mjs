import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes('docs.google.com')) || ctx.pages()[0];
await page.waitForTimeout(2500);
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
await page.screenshot({ path:`${out}/vids-home.png` });
const els = await page.evaluate(() => {
  const seen=[];
  document.querySelectorAll('button,[role=button],a[href],[aria-label]').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<8||r.height<8) return;
    const t=(e.getAttribute('aria-label')||e.innerText||'').trim().replace(/\s+/g,' ').slice(0,60);
    if(t) seen.push(`${t}  @${Math.round(r.x)},${Math.round(r.y)}`);
  });
  return [...new Set(seen)].slice(0,45);
});
console.log('URL:', page.url());
console.log(els.join('\n'));
await b.close();
