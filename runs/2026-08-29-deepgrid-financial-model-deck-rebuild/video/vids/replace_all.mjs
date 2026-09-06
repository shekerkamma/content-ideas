import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { blocks, kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const B = blocks();
const norm = s => s.replace(/\s+/g, ' ').replace(/[—–]/g, '-').trim();

const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(800); await kill(page);

const header = () => page.evaluate(() => {
  const m = document.body.innerText.match(/Scene (\d+) \/ 30/); return m ? +m[1] : null; });

// panel prev/next arrows sit just right of the "Scene n / 30" header
const PREV = [1737, 210], NEXT = [1771, 210];
async function gotoScene(n) {
  for (let i = 0; i < 40; i++) {
    const cur = await header();
    if (cur === n) return true;
    if (cur === null) return false;
    await page.mouse.click(...(cur > n ? PREV : NEXT));
    await page.waitForTimeout(900);
  }
  return false;
}

const done = [], failed = [];
for (let n = 1; n <= 30; n++) {
  await kill(page);
  if (!(await gotoScene(n))) { failed.push(n + ':nav'); continue; }
  await page.mouse.click(1560, 270);          // inside the narration paragraph
  await page.waitForTimeout(900);
  await page.keyboard.press('Control+a');
  await page.waitForTimeout(300);
  await page.keyboard.type(B[n], { delay: 4 });
  await page.waitForTimeout(1800);
  const shown = await page.evaluate(() => {
    const el = [...document.querySelectorAll('div,span,p')].filter(e => {
      const r = e.getBoundingClientRect();
      return e.children.length <= 1 && r.x > 1500 && r.width > 150 && r.y > 225 && r.y < 560
             && (e.innerText || '').trim().length > 40;
    });
    return el.length ? el.map(e => e.innerText).join(' ') : '';
  });
  const hit = norm(shown).includes(norm(B[n]).slice(0, 55));
  (hit ? done : failed).push(n + (hit ? '' : ':text'));
  console.log('scene', n, hit ? 'OK' : 'MISMATCH', '| still on', await header());
}
console.log('\nDONE  :', done.join(','));
console.log('FAILED:', failed.join(',') || 'none');
await b.close();
