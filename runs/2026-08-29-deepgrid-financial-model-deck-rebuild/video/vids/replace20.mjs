import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { readFileSync } from 'node:fs';
import { kill } from './lib.mjs';
const VID='174Q-q4Zu7vTYoBppSvvsEBxr2gT46pV21pF0MWzwimA';
const raw=readFileSync('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/narration-product-lines.md','utf8');
const B={}; let m;
const re=/\*\*(\d{2}) · [^*]+\*\*\n(.+?)(?=\n\*\*\d{2} ·|$)/gs;
while((m=re.exec(raw))!==null) B[parseInt(m[1],10)]=m[2].replace(/\s+/g,' ').trim();
console.log('blocks parsed:',Object.keys(B).length);
if(Object.keys(B).length!==20) process.exit(1);
const norm=s=>s.replace(/\s+/g,' ').replace(/[—–]/g,'-').replace(/['']/g,"'").trim();

const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1200); await kill(page);
// open the AI voiceover panel on Current scene
if(!(await page.getByText('AI voiceover').first().isVisible().catch(()=>false))){
  await page.locator('[role=button][aria-label="Generate a voiceover"]').last().click({timeout:20000});
  await page.waitForTimeout(5000); await kill(page);
}
await page.getByText('Current scene',{exact:true}).first().click({timeout:12000}).catch(()=>{});
await page.waitForTimeout(2500); await kill(page);

const header=()=>page.evaluate(()=>{const x=document.body.innerText.match(/Scene (\d+) \/ 20/);return x?+x[1]:null;});
const PREV=[1737,210], NEXT=[1771,210];
async function goto(n){for(let i=0;i<40;i++){const c=await header();if(c===n)return true;if(c===null)return false;
  await page.mouse.click(...(c>n?PREV:NEXT));await page.waitForTimeout(850);}return false;}
const shown=()=>page.evaluate(()=>{const el=[...document.querySelectorAll('div,span,p')].filter(e=>{
  const r=e.getBoundingClientRect();return e.children.length<=1&&r.x>1500&&r.width>150&&r.y>225&&r.y<560&&(e.innerText||'').trim().length>40;});
  return el.map(e=>e.innerText).join(' ');});

const ok=[],bad=[];
for(let n=1;n<=20;n++){
  await kill(page);
  if(!(await goto(n))){bad.push(n+':nav');continue;}
  await page.mouse.click(1560,270); await page.waitForTimeout(900);
  await page.keyboard.press('Control+a'); await page.waitForTimeout(300);
  await page.keyboard.type(B[n],{delay:4});
  await page.waitForTimeout(1800);
  const hit=norm(await shown()).includes(norm(B[n]).slice(0,55));
  (hit?ok:bad).push(n);
  console.log('scene',n,hit?'OK':'CHECK','| on',await header());
}
console.log('\nOK:',ok.join(','));
console.log('CHECK:',bad.join(',')||'none');
await b.close();
