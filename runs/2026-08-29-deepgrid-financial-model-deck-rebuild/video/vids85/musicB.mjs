import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1RqX9_46Id1fGCqQpBno_4fPAFvK6jxcoQbzVLf6_1jo';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const page=b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.keyboard.press('Escape');
await page.waitForTimeout(1500); await kill(page);
const has=()=>page.evaluate(()=>/Provided by Shutterstock|background music/i.test(document.body.innerText));
console.log('music before:', await has());
// The track's aria-label wording varies; find any timeline element that names a
// music bed rather than assuming the Shutterstock string.
const box = await page.evaluate(()=>{
  const e=[...document.querySelectorAll('[aria-label]')]
    .find(x=>/background music|Provided by Shutterstock/i.test(x.getAttribute('aria-label')||''));
  if(!e) return null;
  const r=e.getBoundingClientRect();
  return {x:Math.round(r.x+Math.min(60,r.width/2)), y:Math.round(r.y+r.height/2),
          label:(e.getAttribute('aria-label')||'').slice(0,60)};
});
console.log('track:', JSON.stringify(box));
if(box){
  await page.mouse.click(box.x, box.y);
  await page.waitForTimeout(1800);
  await page.keyboard.press('Delete');
  await page.waitForTimeout(4000); await kill(page);
}
console.log('music after :', await has());
const t=await page.evaluate(()=>document.body.innerText);
console.log('duration    :',(t.match(/\d\d:\d\d\.\d\s*\/\s*\d\d:\d\d\.\d/)||['-'])[0].replace(/\s+/g,''));
await page.screenshot({path:'nomusicB.png'});
await b.close();
