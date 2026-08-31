import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const ID = process.argv[2];
const DL = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/export90';
const OUT= '/tmp/claude-1000/-home-sheke-content-ideas/68302287-f1a5-41fe-8500-4181db882526/scratchpad';
const kill = p => p.evaluate(() => document.querySelector('#google-hats-survey')?.remove()).catch(()=>{});
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes(ID));
if(!page){ console.log('NO TAB for', ID); await b.close(); process.exit(1); }
await page.bringToFront();
const cdp = await ctx.newCDPSession(page);
// Documented to silently no-op on an externally launched browser -- the file is
// located by searching afterwards, never by trusting this path.
await cdp.send('Browser.setDownloadBehavior',
  { behavior:'allow', downloadPath:DL, eventsEnabled:true }).catch(()=>{});
cdp.on('Browser.downloadWillBegin', e => console.log('  will begin:', e.suggestedFilename));
cdp.on('Browser.downloadProgress', e => { if(e.state!=='inProgress') console.log('  progress:', e.state); });

await page.keyboard.press('Escape'); await page.waitForTimeout(700); await kill(page);
await page.locator('#docs-file-menu').click({ timeout: 20000 });
await page.waitForTimeout(1800);
await page.getByRole('menuitem', { name: /^Download/ }).first().hover({ timeout: 12000 });
await page.waitForTimeout(2000);
await page.getByRole('menuitem', { name: /MP4 video/i }).first().click({ timeout: 15000 });
console.log('clicked: MP4 video (.mp4)');
await page.waitForTimeout(10000); await kill(page);
await page.screenshot({ path: `${OUT}/export88-started.png` });
const t = await page.evaluate(()=>document.body.innerText);
console.log('status:', t.split('\n').filter(l=>/prepar|export|download|render|ready|%|minute/i.test(l)&&l.length<80).slice(0,6).join(' | '));
await b.close();
