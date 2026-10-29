import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const ID='1bLfYm2pFV8JfhdMOMHOhvR2xgT1bwqRe';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const before=new Set(ctx.pages().map(p=>p.url()).filter(u=>u.includes('/videos/d/')));
const page=await ctx.newPage();
await page.goto(`https://docs.google.com/presentation/d/${ID}/edit`,{waitUntil:'domcontentloaded',timeout:90000});
await page.waitForTimeout(14000); await kill(page);
console.log('slides open:', (await page.title()).slice(0,60));
await page.getByText('Transform',{exact:true}).first().click({timeout:20000});
await page.waitForTimeout(4500); await kill(page);
await page.getByRole('button',{name:/Turn into video/i}).first().click({timeout:20000});
console.log('clicked Turn into video');
for(let i=0;i<12;i++){
  await page.waitForTimeout(8000); await kill(page);
  const now=ctx.pages().map(p=>p.url()).filter(u=>u.includes('/videos/d/'));
  const fresh=now.find(u=>![...before].some(o=>o.split('?')[0]===u.split('?')[0]));
  if(fresh){ console.log('NEW VIDS DOC:', fresh.split('?')[0]); break; }
  console.log('  waiting…');
}
await b.close();
