import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const FILE = process.argv[2];
const OUT='/tmp/claude-1000/-home-sheke-content-ideas/68302287-f1a5-41fe-8500-4181db882526/scratchpad';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = await ctx.newPage();
await page.goto('https://drive.google.com/drive/my-drive', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(8000);
await page.evaluate(() => document.querySelector('#google-hats-survey')?.remove());
await page.keyboard.press('Escape');
await page.waitForTimeout(1000);
await page.mouse.click(900, 600);
await page.waitForTimeout(900);
await Promise.all([
  page.waitForEvent('filechooser', { timeout: 30000 }).catch(() => null),
  (async () => { await page.keyboard.press('Alt+c'); await page.waitForTimeout(600);
                 await page.keyboard.press('u'); })(),
]);
const client = await ctx.newCDPSession(page);
await client.send('DOM.enable');
const doc = await client.send('DOM.getDocument', { depth: -1, pierce: true });
const { nodeId } = await client.send('DOM.querySelector', { nodeId: doc.root.nodeId, selector: 'input[type=file]' });
if (!nodeId) throw new Error('no file input');
await client.send('DOM.setFileInputFiles', { files: [FILE], nodeId });
console.log('handed:', FILE.split('/').pop());

// A same-name file can raise an "upload as separate file / replace" prompt that
// blocks the transfer silently. Report state rather than blind-waiting.
for (let i = 0; i < 24; i++) {
  await page.waitForTimeout(15000);
  const st = await page.evaluate(() => {
    const body = document.body.innerText || '';
    const dlg = [...document.querySelectorAll('[role=dialog],[role=alertdialog]')]
      .map(d => (d.innerText || '').replace(/\n/g, ' | ').slice(0, 160));
    const lines = body.split('\n').filter(l => /upload|version|replace|separate|complete|error|fail/i.test(l) && l.length < 80);
    return { dlg, lines: [...new Set(lines)].slice(0, 5) };
  }).catch(() => null);
  if (st) console.log(`[${(i+1)*15}s]`, JSON.stringify(st));
}
await page.screenshot({ path: `${OUT}/upload2.png` });
await b.close();
