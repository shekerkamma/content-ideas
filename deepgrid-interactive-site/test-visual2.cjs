const { chromium } = require('playwright');
const fs = require('fs');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  
  console.log('Loading page...');
  const response = await page.goto('http://localhost:3001', { waitUntil: 'networkidle', timeout: 30000 });
  console.log('Response status:', response.status());
  
  // Wait for content to render
  await page.waitForTimeout(3000);
  
  // Take full page screenshot
  await page.screenshot({ path: '/home/sheke/content-ideas/deepgrid-interactive-site/test-full.png', fullPage: true });
  console.log('Full page screenshot saved');
  
  // Take viewport screenshot
  await page.screenshot({ path: '/home/sheke/content-ideas/deepgrid-interactive-site/test-viewport.png' });
  console.log('Viewport screenshot saved');
  
  // Get detailed layout info
  const layout = await page.evaluate(() => {
    const results = {};
    
    // Check hero
    const hero = document.querySelector('header.hero');
    if (hero) {
      const style = window.getComputedStyle(hero);
      results.hero = {
        height: style.height,
        minHeight: style.minHeight,
        display: style.display,
        position: style.position,
        overflow: style.overflow,
        innerHTML: hero.innerHTML.substring(0, 500)
      };
    }
    
    // Check all sections
    const sections = document.querySelectorAll('section[id]');
    results.sections = [];
    sections.forEach(s => {
      const style = window.getComputedStyle(s);
      results.sections.push({
        id: s.id,
        height: style.height,
        display: style.display,
        visibility: style.visibility,
        rect: s.getBoundingClientRect().toJSON()
      });
    });
    
    // Check for text overlapping
    const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
    let overlapCount = 0;
    while (walker.nextNode()) {
      const textNode = walker.currentNode;
      const parent = textNode.parentElement;
      if (parent) {
        const style = window.getComputedStyle(parent);
        if (style.position === 'absolute' || style.position === 'fixed') {
          const rect = parent.getBoundingClientRect();
          if (rect.width > 0 && rect.height > 0) {
            overlapCount++;
            if (overlapCount <= 5) {
              console.log('Absolute positioned text:', textNode.textContent?.substring(0, 100), 'at', rect.x, rect.y);
            }
          }
        }
      }
    results.absoluteTextCount = overlapCount;
    
    // Check for z-index issues
    const allElements = document.querySelectorAll('*');
    let zIndexIssues = 0;
    allElements.forEach(el => {
      const style = window.getComputedStyle(el);
      const z = parseInt(style.zIndex) || 0;
      if (z > 100) {
        zIndexIssues++;
      }
    });
    results.highZIndexCount = zIndexIssues;
    
    return results;
  });
  
  console.log('Layout analysis:', JSON.stringify(layout, null, 2));
  
  // Check CSS variables
  const cssVars = await page.evaluate(() => {
    const root = document.documentElement;
    const style = window.getComputedStyle(root);
    const vars = {};
    ['--color-bg', '--color-accent', '--color-text', '--space-12', '--section-padding-y-lg'].forEach(v => {
      vars[v] = style.getPropertyValue(v).trim();
    });
    return vars;
  });
  console.log('CSS Variables:', cssVars);
  
  await browser.close();
})();
