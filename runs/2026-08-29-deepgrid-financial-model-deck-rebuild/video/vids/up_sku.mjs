import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const FILE='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/build/DeepGrid-Semi-SKU-Pitch-reviewed.pptx';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
let page=ctx.pages().find(p=>p.url().includes('drive.google.com/drive'));
if(!page){ page=await ctx.newPage(); await page.goto('https://drive.google.com/drive/my-drive',{waitUntil:'domcontentloaded',timeout:60000}); }
await page.bringToFront(); await page.waitForTimeout(5000); await kill(page);
await page.keyboard.press('Escape'); await page.waitForTimeout(800);
await page.mouse.click(900,600); await page.waitForTimeout(800);
const [chooser]=await Promise.all([
  page.waitForEvent('filechooser',{timeout:30000}),
  (async()=>{await page.keyboard.press('Alt+c');await page.waitForTimeout(600);await page.keyboard.press('u');})(),
]);
await chooser.setFiles(FILE);
console.log('handed to chooser:',FILE.split('/').pop());
await page.waitForTimeout(35000);
console.log('upload window elapsed');
await b.close();
