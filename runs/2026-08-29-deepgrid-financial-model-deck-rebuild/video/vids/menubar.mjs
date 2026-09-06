import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront(); await page.keyboard.press('Escape'); await page.waitForTimeout(800); await kill(page);
const m = await page.evaluate(function () {
  const out = [];
  document.querySelectorAll('*').forEach(function (e) {
    if ((e.textContent || '').trim() !== 'File') return;
    const r = e.getBoundingClientRect();
    if (r.width < 4 || r.y > 80) return;
    out.push({ tag: e.tagName, id: e.id || '-', role: e.getAttribute('role') || '-',
      cls: (e.className || '').toString().slice(0, 40),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) });
  });
  return out;
});
console.log(JSON.stringify(m, null, 1));
await b.close();
