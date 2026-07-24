const { chromium } = require('playwright');
const path = require('path');

const expected = [
  'take',
  'method',
  'map',
  'scoring',
  'evidence',
  'datapoints',
  'matrix',
  'pressure',
  'buyers',
  'battlecards',
  'consulting',
  'war-game',
  'proof',
  'roadmap',
  'sources',
  'recommendations',
];

(async () => {
  const file = `file://${path.resolve(__dirname, '../site/index.html')}`;
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(file);

  const tabs = await page.$$eval('button[data-tab]', (els) => els.map((e) => e.dataset.tab));
  const sections = await page.$$eval('main section', (els) => els.map((e) => e.id));
  const missingTabs = expected.filter((id) => !tabs.includes(id));
  const extraSections = sections.filter((id) => !expected.includes(id));

  for (const id of expected) {
    await page.click(`button[data-tab="${id}"]`);
    const active = await page.$eval('section.active', (e) => e.id);
    if (active !== id) {
      throw new Error(`Tab ${id} activated ${active}`);
    }
  }

  await page.screenshot({ path: path.resolve(__dirname, 'html-story-final.png'), fullPage: true });
  await browser.close();

  if (missingTabs.length || extraSections.length || sections.length !== expected.length) {
    throw new Error(JSON.stringify({ sections, tabs, missingTabs, extraSections }, null, 2));
  }

  console.log(JSON.stringify({ sections: sections.length, tabs: tabs.length, expected: expected.length }));
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
