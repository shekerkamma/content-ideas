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
    const t = (e.textContent || '').trim();
    if (!/Corporate Green Technology/.test(t)) return;
    if (e.children.length > 1) return;
    const r = e.getBoundingClientRect();
    if (r.width < 10) return;
    let p = e, chain = [];
    for (let i = 0; i < 4 && p; i++) {
      chain.push(p.tagName + (p.getAttribute('role') ? '[' + p.getAttribute('role') + ']' : '') +
                 (p.getAttribute('aria-label') ? '{' + p.getAttribute('aria-label').slice(0,34) + '}' : ''));
      p = p.parentElement;
    }
    out.push({ x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height), chain: chain.join(' < ') });
  });
  return out.slice(0, 4);
});
console.log(JSON.stringify(m, null, 1));
await b.close();
