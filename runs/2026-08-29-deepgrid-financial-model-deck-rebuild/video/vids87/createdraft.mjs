import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID=process.argv[2];
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx=b.contexts()[0];
const page=ctx.pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(2500); await kill(page);
// Step 3 of the wizard. "Voiceover only" is the default and is what we want --
// an avatar would put a talking head over the slides.
const mode=await page.evaluate(()=>{
  const r=[...document.querySelectorAll('[role=radio],input[type=radio]')]
    .map(e=>({t:(e.closest('label')?.innerText||e.getAttribute('aria-label')||'').trim().slice(0,28),
              on:e.getAttribute('aria-checked')==='true'||e.checked}));
  return r;
});
console.log('narration mode:', JSON.stringify(mode));
const hit=await page.evaluate(()=>{
  const b=[...document.querySelectorAll('button,[role=button]')]
    .find(e=>/create the draft video/i.test((e.innerText||'').trim()));
  if(b){ b.click(); return true; } return false;
});
console.log('clicked "Create the draft video":', hit);
await page.waitForTimeout(8000); await kill(page);
console.log('busy now:', await page.evaluate(()=>/Setting the scene|Generating|Creating/i.test(document.body.innerText)));
await b.close();
