import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(3000); await kill(page);
const labs = await page.evaluate(()=>[...document.querySelectorAll('[aria-label^="Scene "]')]
  .map(e=>({l:e.getAttribute('aria-label'), t:(e.innerText||'').replace(/\n+/g,' ').trim().slice(0,60)})));
console.log('scenes:', labs.length);
labs.slice(0,6).forEach(x=>console.log('  ',x.l,'|',x.t));
console.log('  ...');
labs.slice(-5).forEach(x=>console.log('  ',x.l,'|',x.t));
await b.close();
