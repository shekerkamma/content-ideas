#!/usr/bin/env node
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function argValue(name) {
  const idx = process.argv.indexOf(name);
  return idx >= 0 ? process.argv[idx + 1] : undefined;
}

const input = process.argv[2];
if (!input || input === '--help' || input === '-h') {
  console.error('Usage: validate_tabbed_html.js <html-file-or-url> [--expected a,b,c] [--screenshot out.png]');
  process.exit(input ? 0 : 2);
}

const expectedArg = argValue('--expected');
const screenshotPath = argValue('--screenshot');
const expected = expectedArg ? expectedArg.split(',').map((s) => s.trim()).filter(Boolean) : null;

function toUrl(value) {
  if (/^https?:\/\//.test(value) || value.startsWith('file://')) return value;
  return `file://${path.resolve(value)}`;
}

(async () => {
  if (!/^https?:\/\//.test(input) && !input.startsWith('file://') && !fs.existsSync(input)) {
    throw new Error(`HTML file not found: ${input}`);
  }

  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 } });
  await page.goto(toUrl(input));

  const tabs = await page.$$eval('button[data-tab]', (els) => els.map((e) => e.dataset.tab));
  const sections = await page.$$eval('main section[id]', (els) => els.map((e) => e.id));
  const contract = expected || tabs;
  const missingTabs = contract.filter((id) => !tabs.includes(id));
  const missingSections = contract.filter((id) => !sections.includes(id));
  const extraSections = sections.filter((id) => !contract.includes(id));
  const duplicateTabs = tabs.filter((id, idx) => tabs.indexOf(id) !== idx);

  if (!tabs.length) throw new Error('No button[data-tab] navigation found.');
  if (!sections.length) throw new Error('No main section[id] report sections found.');
  if (missingTabs.length || missingSections.length || extraSections.length || duplicateTabs.length) {
    throw new Error(JSON.stringify({ tabs, sections, missingTabs, missingSections, extraSections, duplicateTabs }, null, 2));
  }

  for (const id of contract) {
    await page.click(`button[data-tab="${id}"]`);
    const active = await page.$eval('main section.active', (el) => el.id);
    if (active !== id) throw new Error(`Tab ${id} activated ${active}`);
  }

  if (screenshotPath) {
    await page.screenshot({ path: path.resolve(screenshotPath), fullPage: true });
  }
  await browser.close();

  console.log(JSON.stringify({ status: 'passed', tabs: tabs.length, sections: sections.length, checked: contract.length }));
})().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
