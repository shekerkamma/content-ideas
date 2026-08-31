import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';

const FILE = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/export85/DeepGrid-Semi-Product-Lines-87-Slide-Explainer.mp4';
const out  = '/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/video/vids';

const b   = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
const page = ctx.pages().find(p => p.url().includes('drive.google.com'));
if (!page) throw new Error('no Drive tab');

await page.bringToFront();
// A native chooser left over from a failed run blocks every shortcut.
await page.keyboard.press('Escape');
await page.waitForTimeout(1200);
// Click the file list, not a menu, so the shortcut has focus.
await page.mouse.click(900, 600);
await page.waitForTimeout(800);

const [chooser] = await Promise.all([
  page.waitForEvent('filechooser', { timeout: 30000 }),
  (async () => {
    await page.keyboard.press('Alt+c');
    await page.waitForTimeout(600);
    await page.keyboard.press('u');
  })(),
]);
// playwright's setFiles refuses >50Mb over CDP ("browser not co-located").
// The browser IS co-located here, so hand the DOM a path via raw CDP instead --
// DOM.setFileInputFiles transfers no bytes, the browser opens the path itself.
const client = await ctx.newCDPSession(page);
await client.send('DOM.enable');
const doc = await client.send('DOM.getDocument', { depth: -1, pierce: true });
const { nodeId } = await client.send('DOM.querySelector', {
  nodeId: doc.root.nodeId, selector: 'input[type=file]',
});
if (!nodeId) throw new Error('no input[type=file] in DOM');
await client.send('DOM.setFileInputFiles', { files: [FILE], nodeId });
console.log('path handed to input via CDP:', FILE.split('/').pop());

// Completion detection: Drive's upload toast text did NOT match any /upload/i
// scan on the run that worked -- the transfer finished while this loop was still
// polling, so do NOT treat a missing toast as a failed upload. Watch the
// progress row's aria-label, and verify externally (Drive search on file size)
// rather than trusting anything read off this page.
const deadline = Date.now() + 20 * 60 * 1000;
let last = '';
while (Date.now() < deadline) {
  const st = await page.evaluate(() => {
    const n = [...document.querySelectorAll('[aria-label],[role=progressbar]')]
      .map(x => x.getAttribute('aria-label') || '')
      .filter(t => /%|complete|uploading|remaining/i.test(t));
    return n.length ? n[n.length - 1] : '';
  }).catch(() => '');
  if (st && st !== last) { last = st; console.log('[progress]', st); }
  if (/complete/i.test(st)) { console.log('UPLOAD_COMPLETE'); break; }
  await page.waitForTimeout(5000);
}
await page.screenshot({ path: `${out}/drive-uploaded-87.png` });
console.log('screenshot written');
await b.close();
