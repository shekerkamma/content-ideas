import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const out = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(1200);
await page.getByText('Change', { exact: true }).first().click({ timeout: 20000 });
await page.waitForTimeout(4500);
await page.screenshot({ path: out + '/voice-picker.png' });
const v = await page.evaluate(function () {
  const seen = [];
  document.querySelectorAll('[role=option],[role=radio],[role=listitem],[role=menuitem],li').forEach(function (e) {
    const r = e.getBoundingClientRect();
    if (r.width < 8 || r.height < 8) return;
    const s = (e.innerText || '').trim().replace(/\s+/g, ' ');
    if (s && s.length < 60) seen.push(s);
  });
  return Array.from(new Set(seen)).slice(0, 40);
});
console.log(v.join('\n'));
await b.close();
