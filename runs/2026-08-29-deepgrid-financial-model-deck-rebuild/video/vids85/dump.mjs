import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const VID='1KUDU8gjS5Lu8FX08a4PdclPdubwx1YeFWII2XEQilLA';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const page = b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.waitForTimeout(2500);
const r = await page.evaluate(()=>{
  const walk=(root,out)=>{ for(const e of root.querySelectorAll('*')){
    if(e.shadowRoot) walk(e.shadowRoot,out);
    const t=(e.textContent||'').trim();
    if(t && t.length<60 && e.children.length===0) out.add(t);
  } return out; };
  return { body: document.body.innerText.replace(/\n+/g,' | ').slice(0,600),
           leaves: [...walk(document, new Set())].slice(0,50) };
});
console.log('BODY:', r.body);
console.log('LEAVES:', r.leaves.join(' · ').slice(0,900));
await page.screenshot({path:'dump.png'});
await b.close();
