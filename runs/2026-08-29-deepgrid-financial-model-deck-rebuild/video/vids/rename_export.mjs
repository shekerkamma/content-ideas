import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
// rename
try{
  await page.locator('input[aria-label*="Rename"], [aria-label="Rename"]').first().click({timeout:15000});
  await page.waitForTimeout(1000);
  await page.keyboard.press('Control+a');
  await page.keyboard.type('DeepGrid Semi — Product Lines (15 SKUs, Investor Video)',{delay:20});
  await page.keyboard.press('Enter');
  await page.waitForTimeout(5000);
  console.log('renamed:',await page.title());
}catch(e){ console.log('rename skipped:',String(e.message).slice(0,60)); }
await kill(page);
// export MP4
await page.keyboard.press('Escape'); await page.waitForTimeout(800);
await page.locator('#docs-file-menu').click({timeout:15000});
await page.waitForTimeout(1800);
await page.getByRole('menuitem',{name:/^Download/}).first().hover({timeout:10000});
await page.waitForTimeout(1800);
await page.getByRole('menuitem',{name:/MP4 video/i}).first().click({timeout:12000});
console.log('MP4 export triggered');
await page.waitForTimeout(8000);
await b.close();
