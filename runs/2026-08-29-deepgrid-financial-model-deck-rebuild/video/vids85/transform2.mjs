import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID='1nJxO6IoIMg5qC-Uagh1bWgf9-Z4coALQ';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(2000); await kill(page);

// The panel header is ALSO called "Turn into video", so a name-based role query
// can land on it and do nothing. Pick the element that is actually the CTA:
// a button whose own text is exactly that and which sits lowest in the panel.
const clicked = await page.evaluate(() => {
  const cands = [...document.querySelectorAll('div[role="button"],button')]
    .filter(e => e.innerText.trim().toLowerCase() === 'turn into video')
    .map(e => ({ e, r: e.getBoundingClientRect() }))
    .filter(o => o.r.width > 120 && o.r.height > 24)
    .sort((a, b) => b.r.top - a.r.top);
  if (!cands.length) return null;
  cands[0].e.click();
  return { top: Math.round(cands[0].r.top), w: Math.round(cands[0].r.width) };
});
console.log('clicked CTA:', JSON.stringify(clicked));

const before = new Set(ctx.pages().map(p=>p.url().split('?')[0]).filter(u=>u.includes('/videos/d/')));
for (let i=0;i<50;i++){
  await page.waitForTimeout(10000);
  const fresh = ctx.pages().map(p=>p.url().split('?')[0]).find(u=>u.includes('/videos/d/') && !before.has(u));
  if (fresh) { console.log('NEW VIDS DOC:', fresh); break; }
  if (i%3===0) console.log('  t+'+((i+1)*10)+'s');
}
await b.close();
