import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='19opB7Nr2HiXGwJG9sAAC0pgc0-I6v9LUqxfC4fV_v3I';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront();
let last=-1, stable=0;
for (let i=0;i<75;i++){
  await page.waitForTimeout(20000); await kill(page);
  const r = await page.evaluate(()=>({
    n: document.querySelectorAll('[aria-label^="Scene "]').length,
    busy: /Setting the scene|Generating|Creating your video/i.test(document.body.innerText),
    dur: (document.body.innerText.match(/\d{2}:\d{2}\.\d/g)||['-']).pop(),
  })).catch(()=>({n:-1,busy:true,dur:'-'}));
  console.log(`  t+${(i+1)*20}s scenes=${r.n} busy=${r.busy} dur=${r.dur}`);
  if (!r.busy && r.n>1 && r.n===last) { if(++stable>=3){ console.log('GEN DONE scenes='+r.n); break; } }
  else stable=0;
  last=r.n;
}
await page.screenshot({path:'genA87.png'});
await b.close();
