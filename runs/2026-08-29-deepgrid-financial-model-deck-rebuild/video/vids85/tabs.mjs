import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
const b = await chromium.connectOverCDP('http://127.0.0.1:9222');
for (const ctx of b.contexts())
  for (const p of ctx.pages())
    console.log(' •', p.url().slice(0,95), '|', (await p.title().catch(()=>'?')).slice(0,60));
await b.close();
