import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID="1nJxO6IoIMg5qC-Uagh1bWgf9-Z4coALQ";
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.keyboard.press('Escape'); await page.waitForTimeout(1000); await kill(page);
await page.getByText('Transform',{exact:true}).first().click({timeout:20000});
console.log('Transform panel opened');
const btn=page.getByRole('button',{name:/Turn into video/i}).first();
await btn.waitFor({state:'visible',timeout:30000});
console.log('button visible; clicking');
await btn.click();
const before=new Set(ctx.pages().map(p=>p.url().split('?')[0]).filter(u=>u.includes('/videos/d/')));
for(let i=0;i<40;i++){
  await page.waitForTimeout(10000);
  const fresh=ctx.pages().map(p=>p.url().split('?')[0]).find(u=>u.includes('/videos/d/')&&!before.has(u));
  if(fresh){ console.log('NEW VIDS DOC:',fresh); break; }
  console.log('  t+'+((i+1)*10)+'s');
}
await b.close();
