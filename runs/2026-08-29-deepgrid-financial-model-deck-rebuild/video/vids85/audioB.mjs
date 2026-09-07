import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { kill } from '../vids/lib.mjs';
const VID='1RqX9_46Id1fGCqQpBno_4fPAFvK6jxcoQbzVLf6_1jo';
const b=await chromium.connectOverCDP('http://127.0.0.1:9222');
const page=b.contexts()[0].pages().find(p=>p.url().includes(VID));
await page.bringToFront(); await page.keyboard.press('Escape');
await page.waitForTimeout(2000); await kill(page);
// Enumerate every labelled timeline element in the audio lanes (below the
// scene strip), without assuming what the track is called.
const rows = await page.evaluate(()=>{
  const out=[];
  for(const e of document.querySelectorAll('[aria-label]')){
    const l=e.getAttribute('aria-label')||''; const r=e.getBoundingClientRect();
    if(r.width>20 && r.y>600 && l.length>3 && !/ - Holt starting in scene /.test(l))
      out.push({l:l.slice(0,95), x:Math.round(r.x), y:Math.round(r.y), w:Math.round(r.width), h:Math.round(r.height)});
  }
  return out;
});
rows.forEach(r=>console.log(`  y=${r.y} h=${r.h} x=${r.x} w=${r.w} :: ${r.l}`));
console.log('audio-lane elements:', rows.length);
await page.screenshot({path:'audioB.png'});
await b.close();
