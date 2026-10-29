import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const FILE='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/build/DeepGrid-Semi-Financial-Model-Walkthrough-reviewed.pptx';
const out='/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes('drive.google.com'));
await page.bringToFront();
await page.keyboard.press('Escape'); await page.waitForTimeout(1200);
await page.mouse.click(900, 600);      // focus the file list, not a menu
await page.waitForTimeout(800);
const [chooser] = await Promise.all([
  page.waitForEvent('filechooser', { timeout:30000 }),
  (async () => { await page.keyboard.press('Alt+c'); await page.waitForTimeout(600); await page.keyboard.press('u'); })(),
]);
await chooser.setFiles(FILE);
console.log('file handed to chooser:', FILE.split('/').pop());
await page.waitForTimeout(40000);
await page.screenshot({ path:`${out}/drive-uploaded.png` });
await b.close();
