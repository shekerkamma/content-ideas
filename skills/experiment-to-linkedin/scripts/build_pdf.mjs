// Build carousel.pdf from the reviewed slide-NN.png files, one image per 1080x1350 page.
// Image-only, so the PDF shows exactly what was reviewed (never page.pdf() the HTML:
// its text becomes Type 3 glyphs that render badly in Windows viewers).
// Usage: node build_pdf.mjs <dir> [out.pdf]
import fs from 'fs';
import path from 'path';
import { loadPlaywright } from './playwright.mjs';

const dir = path.resolve(process.argv[2] || '.');
const outPdf = path.resolve(process.argv[3] || path.join(dir, 'carousel.pdf'));
const files = fs.readdirSync(dir).filter(f => /^slide-\d+\.png$/.test(f)).sort();
if (!files.length) { console.error(`no slide-NN.png in ${dir}; run render.mjs first`); process.exit(2); }

const html = `<!DOCTYPE html><html><head><style>
@page{size:1080px 1350px;margin:0}html,body{margin:0;padding:0}
img{display:block;width:1080px;height:1350px;break-after:page}
img:last-child{break-after:auto}</style></head><body>
${files.map(f => `<img src="file://${path.join(dir, f)}">`).join('\n')}</body></html>`;
const tmp = path.join(dir, '.pdf-build.html');
fs.writeFileSync(tmp, html);
const { chromium } = loadPlaywright();
const browser = await chromium.launch();
try {
  const page = await browser.newPage();
  await page.goto('file://' + tmp);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode())));
  await page.pdf({ path: outPdf, width: '1080px', height: '1350px', printBackground: true });
} finally {
  await browser.close();
  fs.unlinkSync(tmp);
}
console.log(`pdf: ${files.length} pages -> ${outPdf}`);
