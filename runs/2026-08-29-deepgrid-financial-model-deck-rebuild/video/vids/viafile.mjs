import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';  // the empty "Untitled video"
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
let page=ctx.pages().find(p=>p.url().includes(VID));
if(!page){ page=await ctx.newPage(); await page.goto(`https://docs.google.com/videos/d/${VID}/edit`,{waitUntil:'domcontentloaded',timeout:90000}); }
await page.bringToFront(); await page.waitForTimeout(10000); await kill(page);
await page.keyboard.press('Escape'); await page.waitForTimeout(800);
await page.locator('#docs-file-menu').click({timeout:20000});
await page.waitForTimeout(2500); await kill(page);
const item=page.getByRole('menuitem',{name:/Slides to video/i}).first();
console.log('menu item found:', await item.count());
await item.click({timeout:15000});
await page.waitForTimeout(8000); await kill(page);
await page.screenshot({path:'slides2video.png'});
console.log('URL:',page.url().split('?')[0]);
const t=await page.evaluate(()=>[...document.querySelectorAll('div,span,button')]
  .map(e=>(e.innerText||'').trim().replace(/\s+/g,' ')).filter(s=>s&&s.length<70&&/slide|select|choose|import|deck|presentation/i.test(s)).slice(0,12));
console.log([...new Set(t)].join(' | '));
await b.close();
