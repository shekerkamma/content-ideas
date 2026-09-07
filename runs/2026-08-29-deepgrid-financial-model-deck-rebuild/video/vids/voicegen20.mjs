import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
const voice=()=>page.evaluate(()=>(document.body.innerText.match(/(Holt|Nyla|Elio|Knox|Jett|Zeno)/)||['?'])[0]);
console.log('voice before:',await voice());
// pick Holt
await page.getByText('Change',{exact:true}).first().click({timeout:20000});
await page.waitForTimeout(5000); await kill(page);
const hb=await page.getByText('Holt',{exact:true}).first().boundingBox();
await page.mouse.click(hb.x+40,hb.y+8); await page.waitForTimeout(2200);
await page.getByRole('button',{name:/^Select$/}).first().click({timeout:15000});
await page.waitForTimeout(4500); await kill(page);
console.log('voice after :',await voice());
// regenerate every scene
await page.getByText('All scenes',{exact:true}).first().click({timeout:15000});
await page.waitForTimeout(3000); await kill(page);
const btn=page.getByRole('button',{name:/^Update all voiceovers$/i}).first();
const bb=await btn.boundingBox();
await page.mouse.click(bb.x+bb.width/2,bb.y+bb.height/2);
await page.waitForTimeout(2500);
const rep=page.getByRole('button',{name:/^Replace$/}).first();
if(await rep.count() && await rep.isVisible().catch(()=>false)){ await rep.click({timeout:10000}); console.log('confirmed Replace'); }
else console.log('no Replace dialog');
for(let i=0;i<16;i++){
  await page.waitForTimeout(15000); await kill(page);
  const n=await page.evaluate(()=>(document.body.innerText.match(/Voiceover outdated/g)||[]).length);
  console.log('  t+'+((i+1)*15)+'s outdated='+n);
  if(n===0 && i>=2) break;
}
const t=await page.evaluate(()=>document.body.innerText);
console.log('voice :',(t.match(/(Holt|Nyla)/)||['?'])[0]);
console.log('music :',/Provided by Shutterstock/i.test(t)?'PRESENT':'none');
console.log('dur   :',(t.match(/\d\d:\d\d\.\d\s*\/\s*\d\d:\d\d\.\d/)||['-'])[0].replace(/\s+/g,''));
await page.screenshot({path:'final20.png'});
await b.close();
