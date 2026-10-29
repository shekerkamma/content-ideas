import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
await page.bringToFront();
await page.waitForTimeout(1000);
const info = await page.evaluate(function () {
  const out = [];
  document.querySelectorAll('*').forEach(function (e) {
    const s = (e.textContent || '').trim();
    if (s !== 'Voiceover') return;
    const r = e.getBoundingClientRect();
    if (r.width < 4) return;
    out.push({
      tag: e.tagName, role: e.getAttribute('role'), aria: e.getAttribute('aria-label'),
      cls: (e.className || '').toString().slice(0, 40),
      x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height),
      parentRole: e.parentElement && e.parentElement.getAttribute('role'),
      parentAria: e.parentElement && e.parentElement.getAttribute('aria-label'),
    });
  });
  return out.slice(0, 8);
});
console.log(JSON.stringify(info, null, 1));
await b.close();
