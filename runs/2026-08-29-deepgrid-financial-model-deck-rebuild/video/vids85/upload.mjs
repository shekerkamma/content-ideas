import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const FILE = process.argv[2];
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
let page = ctx.pages().find(p => p.url().includes('drive.google.com/drive'));
if (!page) { page = await ctx.newPage();
  await page.goto('https://drive.google.com/drive/my-drive', {waitUntil:'domcontentloaded',timeout:60000}); }
await page.bringToFront(); await page.waitForTimeout(5000); await kill(page);
// Escape first: a native chooser left open by a failed run blocks every shortcut.
await page.keyboard.press('Escape'); await page.waitForTimeout(1000);
await page.mouse.click(900, 600); await page.waitForTimeout(900);
const [chooser] = await Promise.all([
  page.waitForEvent('filechooser', {timeout: 45000}),
  (async()=>{ await page.keyboard.press('Alt+c'); await page.waitForTimeout(700);
              await page.keyboard.press('u'); })(),
]);
await chooser.setFiles(FILE, {timeout: 120000});
console.log('handed to chooser:', FILE.split('/').pop());
for (let i=0;i<24;i++){
  await page.waitForTimeout(5000);
  const t = await page.evaluate(()=>document.body.innerText.slice(0,3000)).catch(()=> '');
  if (/upload complete/i.test(t)) { console.log('upload complete at', (i+1)*5, 's'); break; }
  if (i%3===0) console.log('  ', (i+1)*5, 's');
}
await b.close();
