import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const FILE = process.argv[2];
if (!FILE) { console.error('usage: upload_deck.mjs <abs path>'); process.exit(1); }

const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
const ctx = b.contexts()[0];
// A stale Drive tab makes Alt+C,U fire no filechooser at all -- always a fresh one.
const page = await ctx.newPage();
await page.goto('https://drive.google.com/drive/my-drive', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(6000);
// A Google survey iframe intercepts every click.
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
// Hand over a PATH via raw CDP -- playwright's setFiles ships bytes and refuses >50Mb.
const client = await ctx.newCDPSession(page);
await client.send('DOM.enable');
const doc = await client.send('DOM.getDocument', { depth: -1, pierce: true });
const { nodeId } = await client.send('DOM.querySelector', {
  nodeId: doc.root.nodeId, selector: 'input[type=file]' });
if (!nodeId) throw new Error('no input[type=file]');
await client.send('DOM.setFileInputFiles', { files: [FILE], nodeId });
console.log('handed to Drive:', FILE.split('/').pop());
await page.waitForTimeout(180000);   // verified externally, not from the toast
await page.close();
await b.close();
