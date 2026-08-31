import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID='19OkYdwlxjrSaV7UED1IQ5ABP48HgmUiNtofc_ZR9Fbs';
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(2000);
// pause playback so the UI settles
try { await page.getByRole('button',{name:/Pause/i}).first().click({timeout:4000}); } catch {}
await page.waitForTimeout(1500);
// open the Voiceover side panel
await page.getByText('Voiceover',{exact:true}).first().click({ timeout:20000 });
await page.waitForTimeout(5000);
await page.screenshot({ path:`${out}/voiceover-panel.png` });
const txt = await page.evaluate(() => {
  const grab=[];
  document.querySelectorAll('textarea,[contenteditable=true],[role=textbox]').forEach(e=>{
    const v=(e.value||e.innerText||'').trim();
    if(v && v.length>25) grab.push(v.replace(/\s+/g,' ').slice(0,300));
  });
  return grab.slice(0,6);
});
console.log('--- narration text found ---');
console.log(txt.length ? txt.join('\n\n') : '(none exposed in DOM)');
await b.close();
