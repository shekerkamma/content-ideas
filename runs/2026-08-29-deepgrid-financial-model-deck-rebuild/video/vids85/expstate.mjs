import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(2000);
const t = await page.evaluate(()=>document.body.innerText);
console.log('pct/status:', [...new Set((t.match(/\d+(\.\d+)?%|Preparing|Downloading|ready|failed|error/gi)||[]))].slice(0,8).join(' | '));
await page.screenshot({path:'expstate.png'});
await b.close();
