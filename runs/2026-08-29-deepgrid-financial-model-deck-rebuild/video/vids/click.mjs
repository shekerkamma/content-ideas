import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const label = process.argv[2];
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes('docs.google.com')) || ctx.pages()[0];
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const el = page.locator(`[aria-label*="${label}" i]`).or(page.getByText(label, { exact:false })).first();
await el.waitFor({ state:'visible', timeout:20000 });
await el.click();
await page.waitForTimeout(5000);
await page.screenshot({ path:`${out}/after-click.png` });
console.log('URL:', page.url());
const els = await page.evaluate(() => {
  const seen=[];
  document.querySelectorAll('button,[role=button],a[href],[aria-label],input').forEach(e=>{
    const r=e.getBoundingClientRect(); if(r.width<8||r.height<8) return;
    const t=(e.getAttribute('aria-label')||e.innerText||e.placeholder||'').trim().replace(/\s+/g,' ').slice(0,64);
    if(t) seen.push(t);
  });
  return [...new Set(seen)].slice(0,40);
});
console.log(els.join('\n'));
await b.close();
