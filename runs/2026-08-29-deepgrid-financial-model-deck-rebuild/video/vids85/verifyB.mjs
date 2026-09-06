import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { readFileSync } from 'node:fs';
import { kill } from '../vids/lib.mjs';
const VID='1RqX9_46Id1fGCqQpBno_4fPAFvK6jxcoQbzVLf6_1jo';
const TOTAL=40, OFFSET=45;
const raw=readFileSync('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/narration-sku-explainer.md','utf8');
const B={}; let m; const re=/\*\*(\d{2}) · [^*]+\*\*\n(.+?)(?=\n\*\*\d{2} ·|$)/gs;
while((m=re.exec(raw))!==null) B[parseInt(m[1],10)]=m[2].replace(/\s+/g,' ').trim();
const norm=s=>s.replace(/\s+/g,' ').replace(/[—–]/g,'-').replace(/[\u2018\u2019\u02BC]/g,"'").toLowerCase().trim();
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const page=b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1500); await kill(page);
const header=()=>page.evaluate(total=>{const x=document.body.innerText.match(new RegExp('Scene (\\d+) / '+total));return x?+x[1]:null;},TOTAL);
const PREV=[1737,210], NEXT=[1771,210];
async function goto(n){for(let i=0;i<90;i++){const c=await header();if(c===n)return true;if(c===null)return false;
  await page.mouse.click(...(c>n?PREV:NEXT));await page.waitForTimeout(700);}return false;}
const shown=()=>page.evaluate(()=>{const el=[...document.querySelectorAll('div,span,p')].filter(e=>{
  const r=e.getBoundingClientRect();return e.children.length<=1&&r.x>1500&&r.width>150&&r.y>225&&r.y<560&&(e.innerText||'').trim().length>25;});
  return el.map(e=>e.innerText).join(' ');});
const targets = process.argv[2] ? process.argv[2].split(',').map(Number)
                                : Array.from({length:TOTAL},(_,i)=>i+1);
const bad=[];
for(const n of targets){
  await kill(page);
  if(!(await goto(n))){bad.push(n+':nav');continue;}
  await page.waitForTimeout(600);
  const got=norm(await shown()), want=norm(B[n+OFFSET]);
  const head=want.slice(0,60), tail=want.slice(-45);
  const ok = got.includes(head) && got.includes(tail);
  if(!ok){ bad.push(n); console.log('scene',n,'MISMATCH\n  want:',want.slice(0,90),'\n  got :',got.slice(0,140)); }
  else console.log('scene',n,'verified');
}
console.log('\nMISMATCHES:', bad.length? bad.join(',') : 'none');
await b.close();
