import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p=>p.url().includes('1nJxO6IoIMg5qC-Uagh1bWgf9-Z4coALQ'));
await page.bringToFront(); await page.waitForTimeout(2500); await kill(page);
const txt = await page.evaluate(()=>document.body.innerText);
// print anything that looks like panel/dialog copy
const lines=[...new Set(txt.split('\n').map(s=>s.trim()).filter(s=>s.length>3&&s.length<120))];
console.log(lines.slice(0,60).join('\n'));
await page.screenshot({path:'slides-transform.png'});
await b.close();
