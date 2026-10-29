const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  
  console.log('Loading page...');
  await page.goto('http://localhost:3001', { waitUntil: 'networkidle', timeout: 30000 });
  
  // Wait for content to render
  await page.waitForTimeout(2000);
  
  // Take full page screenshot
  await page.screenshot({ path: 'full-page.png', fullPage: true });
  console.log('Full page screenshot saved');
  
  // Check for specific elements
  const hero = await page.$('header.hero');
  console.log('Hero element:', hero ? 'FOUND' : 'MISSING');
  
  const valueProp = await page.$('.value-prop-bar');
  console.log('Value Prop Bar:', valueProp ? 'FOUND' : 'MISSING');
  
  const pillars = await page.$('#pillars');
  console.log('Pillars section:', pillars ? 'FOUND' : 'MISSING');
  
  const verification = await page.$('#verification');
  console.log('Verification Ladder:', verification ? 'FOUND' : 'MISSING');
  
  const procurement = await page.$('#procurement');
  console.log('Procurement Scorecard:', procurement ? 'FOUND' : 'MISSING');
  
  const usecases = await page.$('#usecases');
  console.log('Use Cases:', usecases ? 'FOUND' : 'MISSING');
  
  const media = await page.$('#media');
  console.log('Media Proof:', media ? 'FOUND' : 'MISSING');
  
  const personas = await page.$('#personas');
  console.log('Persona Tabs:', personas ? 'FOUND' : 'MISSING');
  
  const portfolio = await page.$('#portfolio');
  console.log('Product Portfolio:', portfolio ? 'FOUND' : 'MISSING');
  
  const footer = await page.$('#footer');
  console.log('Footer:', footer ? 'FOUND' : 'MISSING');
  
  // Check for overlapping text
  const allText = await page.evaluate(() => {
    const elements = document.querySelectorAll('*');
    let overlaps = 0;
    elements.forEach(el => {
      const rect = el.getBoundingClientRect();
      if (rect.width === 0 || rect.height === 0) return;
      const style = window.getComputedStyle(el);
      if (style.position === 'absolute' || style.position === 'fixed') {
        // Check if text is readable
        const text = el.textContent?.trim();
        if (text && text.length > 5 && style.fontSize) {
          const fs = parseFloat(style.fontSize);
          if (fs < 10) console.log('TINY TEXT:', text.substring(0,50), 'at', rect.x, rect.y, 'size', fs);
        }
      }
    });
    return 'done';
  });
  
  // Check computed styles on key elements
  const styles = await page.evaluate(() => {
    const hero = document.querySelector('header.hero');
    if (hero) {
      const style = window.getComputedStyle(hero);
      return {
        heroHeight: style.height,
        heroDisplay: style.display,
        heroOverflow: style.overflow
      };
    }
    return {};
  });
  console.log('Hero styles:', styles);
  
  // Take viewport screenshot
  await page.screenshot({ path: 'viewport.png' });
  console.log('Viewport screenshot saved');
  
  await browser.close();
})();
