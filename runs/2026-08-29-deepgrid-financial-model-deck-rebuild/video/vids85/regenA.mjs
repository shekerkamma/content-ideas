import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const ID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(ID));
await page.bringToFront(); await page.waitForTimeout(1500); await kill(page);

const voice = () => page.evaluate(()=>(document.body.innerText.match(/(Holt|Nyla|Rhea|Orion)/)||['?'])[0]);
const outdated = () => page.evaluate(()=>(document.body.innerText.match(/Voiceover outdated/g)||[]).length);
console.log('voice before:', await voice());

// "Update all voiceovers" only exists on the All scenes tab; Current scene
// offers the singular "Update voiceover", which regenerates one.
await page.getByText('All scenes',{exact:true}).first().click({timeout:20000});
await page.waitForTimeout(3500); await kill(page);
console.log('voice on All scenes:', await voice());

const btn = page.getByRole('button',{name:/Update all voiceovers/i}).first();
await btn.waitFor({state:'visible',timeout:30000});
const bb = await btn.boundingBox();
await page.mouse.click(bb.x+bb.width/2, bb.y+bb.height/2);
await page.waitForTimeout(3000);

// "Replace all existing voiceovers?" -- an unconfirmed click looks like a
// completed regeneration and silently does nothing.
const rep = page.getByRole('button',{name:/^(Replace|Replace all)$/i}).first();
if (await rep.count() && await rep.isVisible().catch(()=>false)) {
  await rep.click({timeout:12000}); console.log('confirmed Replace');
} else console.log('WARNING: no Replace dialog appeared');

// The outdated-badge count is the honest progress signal, not the duration.
let last=-1, stable=0;
for(let i=0;i<60;i++){
  await page.waitForTimeout(20000); await kill(page);
  const n=await outdated().catch(()=>-1);
  console.log(`  t+${(i+1)*20}s outdated=${n}`);
  if(n===0){ if(++stable>=2){ console.log('REGEN COMPLETE'); break; } } else stable=0;
  last=n;
}
console.log('voice after:', await voice(), '| outdated:', await outdated());
await page.screenshot({path:'regenA.png'});
await b.close();
