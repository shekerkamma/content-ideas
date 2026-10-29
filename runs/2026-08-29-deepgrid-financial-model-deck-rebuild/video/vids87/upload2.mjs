import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const FILE = process.argv[2];
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
// Always a fresh tab: a Drive tab left over from an earlier step can be in a
// state where the upload shortcut never fires, which reads as a dead shortcut.
const page = await ctx.newPage();
await page.goto('https://drive.google.com/drive/my-drive',{waitUntil:'domcontentloaded',timeout:90000});
await page.bringToFront(); await page.waitForTimeout(9000); await kill(page);
await page.keyboard.press('Escape'); await page.waitForTimeout(1200);
await page.mouse.click(900, 600); await page.waitForTimeout(1500); await kill(page);
const [chooser] = await Promise.all([
  page.waitForEvent('filechooser', {timeout: 60000}),
  (async()=>{ await page.keyboard.press('Alt+c'); await page.waitForTimeout(900);
              await page.keyboard.press('u'); })(),
]);
await chooser.setFiles(FILE, {timeout: 180000});
console.log('handed to chooser:', FILE.split('/').pop());
for (let i=0;i<30;i++){
  await page.waitForTimeout(5000);
  const t = await page.evaluate(()=>document.body.innerText.slice(0,3000)).catch(()=> '');
  if (/upload complete/i.test(t)) { console.log('upload complete at', (i+1)*5, 's'); break; }
  if (i%4===0) console.log('  ', (i+1)*5, 's');
}
await b.close();
