import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { blocks, kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const B = blocks();
const norm = s => s.replace(/\s+/g, ' ').replace(/[—–]/g, '-').replace(/[’']/g, "'").trim();
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(800); await kill(page);
const header = () => page.evaluate(() => { const m = document.body.innerText.match(/Scene (\d+) \/ 30/); return m ? +m[1] : null; });
const PREV = [1737, 210], NEXT = [1771, 210];
async function goto(n) {
  for (let i = 0; i < 40; i++) {
    const c = await header(); if (c === n) return true; if (c === null) return false;
    await page.mouse.click(...(c > n ? PREV : NEXT)); await page.waitForTimeout(700);
  } return false;
}
const shown = () => page.evaluate(() => {
  const el = [...document.querySelectorAll('div,span,p')].filter(e => {
    const r = e.getBoundingClientRect();
    return e.children.length <= 1 && r.x > 1500 && r.width > 150 && r.y > 225 && r.y < 560
           && (e.innerText || '').trim().length > 40; });
  return el.map(e => e.innerText).join(' ');
});
const bad = [];
for (let n = 1; n <= 30; n++) {
  await goto(n); await page.waitForTimeout(500);
  const t = norm(await shown());
  const ok = t.includes(norm(B[n]).slice(0, 50));
  if (!ok) bad.push({ n, got: t.slice(0, 60) });
  process.stdout.write(ok ? '.' : 'X');
}
console.log('\nmismatches:', bad.length);
bad.forEach(x => console.log('  scene', x.n, '=>', x.got));
await b.close();
