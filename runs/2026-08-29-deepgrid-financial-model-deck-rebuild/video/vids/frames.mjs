import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID = '19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
const kill = () => page.evaluate(() => document.querySelectorAll('#google-hats-survey').forEach(e => e.remove())).catch(()=>{});
await page.bringToFront(); await page.waitForTimeout(1000); await kill();
try { await page.getByText('Current scene', { exact:true }).first().click({ timeout: 10000 }); } catch(e){}
await page.waitForTimeout(3500); await kill();

for (const f of page.frames()) {
  let info;
  try {
    info = await f.evaluate(function () {
      const ce = document.querySelectorAll('[contenteditable]').length;
      const ta = document.querySelectorAll('textarea').length;
      const tb = document.querySelectorAll('[role=textbox]').length;
      const txt = (document.body ? document.body.innerText : '').trim().slice(0, 70);
      return { ce, ta, tb, txt };
    });
  } catch (e) { info = { err: String(e.message).slice(0, 40) }; }
  console.log((f.url() || '(blank)').slice(0, 60), '=>', JSON.stringify(info));
}
await b.close();
