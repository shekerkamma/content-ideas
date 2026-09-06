import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
let page = ctx.pages().find(p=>p.url().includes('drive.google.com')) || await ctx.newPage();
await page.bringToFront();
await page.goto('https://drive.google.com/drive/recent',{waitUntil:'domcontentloaded',timeout:60000});
await page.waitForTimeout(7000); await kill(page);
const rows = await page.evaluate(()=>[...document.querySelectorAll('[role="row"],[data-id]')]
  .map(e=>e.innerText.replace(/\n/g,' | ').slice(0,110)).filter(t=>t.trim()).slice(0,14));
rows.forEach(r=>console.log(' •',r));
await b.close();
