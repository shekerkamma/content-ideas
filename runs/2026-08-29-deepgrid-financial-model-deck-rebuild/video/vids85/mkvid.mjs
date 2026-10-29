import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = await ctx.newPage();
await page.bringToFront();
await page.goto('https://drive.google.com/drive/recent',{waitUntil:'domcontentloaded',timeout:60000});
await page.waitForTimeout(7000); await kill(page);

// open the deck (double-click the first matching row)
const row = page.locator('[role="row"]', { hasText: 'DeepGrid-Semi-SKU-Explainer-Sims-reviewed.pptx' }).first();
await row.dblclick({ timeout: 20000 });
await page.waitForTimeout(9000); await kill(page);
console.log('after open:', page.url().slice(0, 78));

// a new tab may have taken over
const pages = ctx.pages();
const slides = pages.find(p => p.url().includes('docs.google.com/presentation')) || page;
await slides.bringToFront(); await slides.waitForTimeout(9000); await kill(slides);
console.log('slides url:', slides.url().slice(0, 78));
console.log('title:', await slides.title());
await slides.screenshot({ path: 'slides-open.png' });
