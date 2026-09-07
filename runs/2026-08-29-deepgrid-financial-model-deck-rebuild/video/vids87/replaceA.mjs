import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { readFileSync } from 'node:fs';
import { kill } from '../vids/lib.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const FROM=Number(process.env.FROM||1), TO=Number(process.env.TO||45), TOTAL=45;
const raw=readFileSync('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/narration-sku-explainer.md','utf8');
const B={}; let m;
const re=/\*\*(\d{2}) · [^*]+\*\*\n(.+?)(?=\n\*\*\d{2} ·|$)/gs;
while((m=re.exec(raw))!==null) B[parseInt(m[1],10)]=m[2].replace(/\s+/g,' ').trim();
console.log('blocks parsed:',Object.keys(B).length);
for(let i=FROM;i<=TO;i++) if(!B[i]){ console.error('missing block',i); process.exit(1); }
const norm=s=>s.replace(/\s+/g,' ').replace(/[—–]/g,'-').replace(/[\u2018\u2019\u02BC]/g,"'").trim();

const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(1500); await kill(page);
const header=()=>page.evaluate(total=>{
  const x=document.body.innerText.match(new RegExp('Scene (\\d+) / '+total));
  return x?+x[1]:null;
}, TOTAL);
if((await header())===null){
  await page.locator('[role=button][aria-label="Generate a voiceover"]').last().click({timeout:25000});
  await page.waitForTimeout(6000); await kill(page);
  await page.getByText('Current scene',{exact:true}).first().click({timeout:12000}).catch(()=>{});
  await page.waitForTimeout(2500); await kill(page);
}

// Build the regex INSIDE evaluate. Passing one in as `.source` from the node
// side double-escaped the \d into a literal backslash, so header() returned
// null forever and every goto() failed instantly -- which reads as a dead
// panel and is not.

const PREV=[1737,210], NEXT=[1771,210];
async function goto(n){for(let i=0;i<90;i++){const c=await header();if(c===n)return true;if(c===null)return false;
  await page.mouse.click(...(c>n?PREV:NEXT));await page.waitForTimeout(750);}return false;}
const shown=()=>page.evaluate(()=>{const el=[...document.querySelectorAll('div,span,p')].filter(e=>{
  const r=e.getBoundingClientRect();return e.children.length<=1&&r.x>1500&&r.width>150&&r.y>225&&r.y<560&&(e.innerText||'').trim().length>40;});
  return el.map(e=>e.innerText).join(' ');});

// The panel renders asynchronously; starting before the header exists makes
// every goto() fail instantly and reads as 45 nav failures.
let h=null;
for(let i=0;i<30;i++){ h=await header(); if(h!==null) break; await page.waitForTimeout(2000); await kill(page); }
if(h===null){ console.error('BLOCKED: voiceover panel header never appeared'); process.exit(2); }
console.log('header ready at scene', h);
const ok=[],bad=[];
for(let n=FROM;n<=TO;n++){
  await kill(page);
  if(!(await goto(n))){bad.push(n+':nav');console.log('scene',n,'NAV-FAIL');continue;}
  // click the paragraph BODY, never the "Scene n / N" header -- a click on the
  // header turns Ctrl+A and typing into scene navigation.
  await page.mouse.click(1560,270); await page.waitForTimeout(900);
  await page.keyboard.press('Control+a'); await page.waitForTimeout(300);
  await page.keyboard.type(B[n],{delay:3});
  await page.waitForTimeout(1600);
  const hit=norm(await shown()).includes(norm(B[n]).slice(0,55));
  (hit?ok:bad).push(n);
  console.log('scene',n,hit?'OK':'CHECK','| on',await header());
}
console.log('\nOK:',ok.length,'| CHECK:',bad.join(',')||'none');
await b.close();
