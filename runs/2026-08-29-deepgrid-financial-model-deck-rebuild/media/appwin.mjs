import { chromium } from '/home/sheke/content-ideas/node_modules/playwright/index.mjs';
import { existsSync } from 'node:fs';
const EXEC=['chromium-1234','chromium-1208'].map(b=>`/home/sheke/.cache/ms-playwright/${b}/chrome-linux64/chrome`).find(existsSync);
// --app gives a chromeless window so an x11grab of the window rect is pure page.
const ctx = await chromium.launchPersistentContext('/home/sheke/.cache/sim-capture-profile', {
  executablePath: EXEC, headless:false, viewport:null,
  args:[`--app=file://${process.argv[2]}`,'--window-position=0,0','--window-size=1600,900',
        '--autoplay-policy=no-user-gesture-required','--enable-speech-dispatcher'],
});
await new Promise(r=>setTimeout(r,4000));
const page = ctx.pages()[0];
console.log('url:', page.url().slice(0,60));
console.log('inner size:', JSON.stringify(await page.evaluate(()=>({w:innerWidth,h:innerHeight,sx:screenX,sy:screenY}))));
await new Promise(r=>setTimeout(r,2000));
await ctx.close();
