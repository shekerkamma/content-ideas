import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const NAME='DeepGrid-Semi-SKU-Explainer-PartB.pptx';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = await ctx.newPage();
await page.goto('https://drive.google.com/drive/recent',{waitUntil:'domcontentloaded',timeout:90000});
await page.bringToFront(); await page.waitForTimeout(9000); await kill(page);
await page.locator('[role="row"]',{hasText:NAME}).first().dblclick({timeout:25000});
await page.waitForTimeout(12000);
const sl = ctx.pages().find(p=>p.url().includes('docs.google.com/presentation') && !p.url().includes('1nJxO6'));
if(!sl){ console.log('BLOCKED: no new Slides tab'); process.exit(2); }
await sl.bringToFront(); await sl.waitForTimeout(10000); await kill(sl);
console.log('SLIDES URL:', sl.url().split('?')[0]);
console.log('title:', await sl.title());
await b.close();
