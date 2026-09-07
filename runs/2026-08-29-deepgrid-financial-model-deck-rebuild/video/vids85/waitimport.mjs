import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront();
let last=-1, stable=0;
for (let i=0;i<60;i++){
  await page.waitForTimeout(20000); await kill(page);
  const n = await page.evaluate(()=>document.querySelectorAll('[aria-label^="Scene "]').length).catch(()=>-1);
  const dur = await page.evaluate(()=>(document.body.innerText.match(/\d{2}:\d{2}\.\d/)||['-'])[0]).catch(()=>'-');
  console.log(`  t+${(i+1)*20}s scenes=${n} dur=${dur}`);
  // Scene count is the honest signal; the duration readout lags and has lied before.
  if (n>1 && n===last) { if (++stable>=3){ console.log('IMPORT SETTLED scenes='+n); break; } }
  else stable=0;
  last=n;
}
await b.close();
