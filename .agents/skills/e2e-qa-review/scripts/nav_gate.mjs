#!/usr/bin/env node
// Navigation gate: every menu driven the way a person drives it, and every page reached by the URLs people type.
// usage (from the target project's directory): node <skill>/scripts/nav_gate.mjs qa/nav.json
// exit 0 clean · 2 findings · 1 BLOCKED. Config: references/config.md.
// Assumes the disclosure pattern: each dropdown button has aria-controls naming its panel's id.
// 1. desktop: hover each dropdown, move the pointer in a straight line at human speed to EVERY link, click, land
// 2. desktop keyboard: Enter opens, Tab reaches a link inside, Escape closes and returns focus to the button
// 3. 1024 px: every open panel stays inside the viewport
// 4. phone: open the sheet, expand each group, tap every same-site link
// 5. typed URLs: /Title, /UPPER, /x/, /x.html and configured extras reach the real page
import { createRequire } from 'module';
import { readFileSync, existsSync } from 'fs';
import { resolve } from 'path';

const blocked = (m) => { console.error('BLOCKED: ' + m); process.exit(1); };
const cfgPath = process.argv[2] || 'qa/nav.json';
if (!existsSync(cfgPath)) blocked(`config ${cfgPath} not found (see references/config.md)`);
const cfg = JSON.parse(readFileSync(cfgPath, 'utf8'));
// Resolve a dependency from the site first, then $E2E_QA_NODE_MODULES, then the skill's own repo, and say which
// one served the run: a site without axe-core or playwright installed should still be measurable.
const anchors = [resolve(process.cwd(), 'package.json'), ...(process.env.E2E_QA_NODE_MODULES ? [resolve(process.env.E2E_QA_NODE_MODULES, '..', 'package.json')] : []), import.meta.url];
const served = {};
function need(id, how = 'require') {
  for (const a of anchors) {
    try { const r = createRequire(a); const v = how === 'resolve' ? r.resolve(id) : r(id); served[id] = (how === 'resolve' ? v : r.resolve(id)).replace(/\/node_modules\/.*/, ''); return v; } catch {}
  }
  return null;
}
const pw = need('playwright');
if (!pw) blocked('playwright not found in the site, $E2E_QA_NODE_MODULES, or the skill repo (npm i -D playwright)');
const { chromium } = pw;
console.log(`deps: playwright from ${served.playwright}`);

const BASE = cfg.base.replace(/\/?$/, '/');
const MENU = cfg.menu || 'nav.mega-nav', TRIGGER = cfg.trigger || '.mega-trigger';
const TOP = cfg.topLinks || `${MENU} > a`, PHONE = cfg.phoneOpen || '[aria-label="Open navigation"]';
const SHEET = cfg.sheet || '.mobile-sheet', NF = cfg.notFound || '.nf-page';
const START = cfg.start || '', ALLOW = cfg.externalAllow ? new RegExp(cfg.externalAllow) : null;
try { await fetch(BASE); } catch { blocked(`${BASE} is not reachable (start scripts/serve_pages.py)`); }

const fails = [];
const fail = (m) => { fails.push(m); console.log('  FAIL ' + m); };
const path = (u) => new URL(u, BASE).pathname.replace(/\/$/, '');
const same = (u) => new URL(u).origin === new URL(BASE).origin;
const b = await chromium.launch();

async function landed(p, want, via) {
  await p.waitForURL((u) => path(u.toString()) === want, { timeout: 15000 }).catch(() => {});
  const got = path(p.url()).replace(/\.html$/, ''); // Pages serves /x.html as the same page as /x
  let h = { h1: '', nf: false };
  for (let t = 0; t < 4; t++) {
    await p.waitForLoadState('networkidle').catch(() => {});
    try { h = await p.evaluate((nf) => ({ h1: document.querySelector('h1')?.textContent.trim() || '', nf: !!document.querySelector(nf) }), NF); break; }
    catch { await p.waitForTimeout(500); } // a redirect was still in flight
  }
  if (got !== want || !h.h1 || h.nf) fail(`${via}: wanted ${want}, got ${got} (h1 "${h.h1}"${h.nf ? ', not-found page' : ''})`);
}

// 1-2. desktop pointer and keyboard
{
  const p = await b.newPage({ viewport: { width: 1440, height: 900 } });
  await p.goto(BASE + START, { waitUntil: 'networkidle' });
  const menus = await p.$$eval(`${MENU} ${TRIGGER}`, (xs) => [...new Set(xs.map((x) => x.getAttribute('aria-controls')).filter(Boolean))]);
  if (!menus.length) fail(`no dropdowns found with "${MENU} ${TRIGGER}[aria-controls]": check the config before trusting a green`);
  let followed = 0;
  for (const id of menus) {
    await p.goto(BASE + START, { waitUntil: 'networkidle' });
    const links = await p.$$eval(`#${id} a`, (as) => as.map((a) => [a.href, a.target]));
    for (const [href, target] of links) if (!same(href) && (!(ALLOW && ALLOW.test(href)) || target !== '_blank')) fail(`menu ${id}: external link ${href} (target ${target || 'self'})`);
    for (let i = 0; i < links.length; i++) {
      if (!same(links[i][0])) continue; // external: checked above, never followed
      if (i) await p.goto(BASE + START, { waitUntil: 'networkidle' });
      const bb = await p.locator(`[aria-controls="${id}"]`).first().boundingBox();
      await p.mouse.move(bb.x + bb.width / 2, bb.y + bb.height / 2);
      await p.waitForTimeout(150);
      const link = p.locator(`#${id} a`).nth(i);
      if (!(await link.isVisible())) { fail(`hover ${id}: panel did not open`); break; }
      const lb = await link.boundingBox();
      const [x0, y0, x1, y1] = [bb.x + bb.width / 2, bb.y + bb.height / 2, lb.x + Math.min(24, lb.width / 2), lb.y + lb.height / 2];
      for (let k = 1; k <= 24; k++) { await p.mouse.move(x0 + (x1 - x0) * k / 24, y0 + (y1 - y0) * k / 24); await p.waitForTimeout(20); } // ~500 ms, human speed
      if (!(await link.isVisible())) { fail(`hover ${id}: panel closed before the pointer reached "${(await link.textContent()).trim().slice(0, 40)}"`); continue; }
      await p.mouse.down(); await p.mouse.up();
      await landed(p, path(links[i][0]), `menu ${id} -> link ${i + 1}`);
      followed++;
    }
    await p.goto(BASE + START, { waitUntil: 'networkidle' });
    await p.mouse.move(5, 890);
    const btn = p.locator(`[aria-controls="${id}"]`).first();
    await btn.focus(); await p.keyboard.press('Enter');
    if (!(await p.locator(`#${id}`).isVisible())) fail(`keyboard ${id}: Enter did not open the panel`);
    await p.keyboard.press('Tab');
    if (!(await p.evaluate((i) => !!document.activeElement?.closest('#' + i), id))) fail(`keyboard ${id}: Tab from the open button did not reach its first link`);
    await p.keyboard.press('Escape');
    const st = await p.evaluate((i) => ({ open: !document.getElementById(i).hidden, focus: document.activeElement?.getAttribute('aria-controls') }), id);
    if (st.open || st.focus !== id) fail(`keyboard ${id}: Escape left it ${st.open ? 'open' : 'closed'}, focus on ${st.focus}`);
  }
  const tops = await p.$$eval(TOP, (as) => as.map((x) => x.href)); // resolved hrefs; the attribute may be relative
  for (let i = 0; i < tops.length; i++) {
    if (!same(tops[i])) continue;
    await p.goto(BASE + START, { waitUntil: 'networkidle' });
    try { await p.locator(TOP).nth(i).click({ timeout: 5000 }); } catch { fail(`top link ${path(tops[i])}: not clickable`); continue; }
    await landed(p, path(tops[i]), 'top link ' + path(tops[i]));
  }
  console.log(`desktop: ${menus.length} dropdowns, ${followed} links followed by pointer at human speed, keyboard open/close on each`);
  await p.close();
}

// 3. panels fit a narrow desktop
{
  const p = await b.newPage({ viewport: { width: 1024, height: 800 } });
  await p.goto(BASE + START, { waitUntil: 'networkidle' });
  for (const id of await p.$$eval(`${MENU} ${TRIGGER}`, (xs) => xs.map((x) => x.getAttribute('aria-controls')).filter(Boolean))) {
    if (!(await p.locator(`[aria-controls="${id}"]`).first().isVisible())) continue;
    await p.click(`[aria-controls="${id}"]`);
    const r = await p.locator('#' + id).boundingBox();
    if (!r) fail(`1024px: panel ${id} is not open after a click on its button (hover-open then click-toggle closes it)`);
    else if (r.x < 0 || r.x + r.width > 1025) fail(`1024px: panel ${id} spans ${Math.round(r.x)}..${Math.round(r.x + r.width)}`);
    await p.keyboard.press('Escape');
  }
  await p.close();
}

// 4. phone sheet
if (!cfg.noPhoneSheet) {
  const p = await b.newPage({ viewport: { width: 390, height: 844 }, hasTouch: true, isMobile: true });
  await p.goto(BASE + START, { waitUntil: 'networkidle' });
  const open = async () => { await p.locator(PHONE).first().click(); await p.waitForTimeout(200); };
  await open().catch(() => fail(`phone: no "${PHONE}" button`));
  const items = (await p.$$eval(`${SHEET} a`, (as) => as.map((a) => a.href)).catch(() => [])).filter(same);
  let n = 0;
  for (const href of [...new Set(items)]) {
    await p.goto(BASE + START, { waitUntil: 'networkidle' });
    await open();
    const a = p.locator(`${SHEET} a[href="${new URL(href).pathname}${new URL(href).hash}"], ${SHEET} a[href="${href}"]`).first();
    if (!(await a.isVisible().catch(() => false))) {
      const panel = await a.evaluate((el) => el.closest('[id]')?.id).catch(() => null);
      if (panel) await p.locator(`${SHEET} [aria-controls="${panel}"]`).first().tap().catch(() => {});
    }
    if (!(await a.isVisible().catch(() => false))) { fail(`phone: "${path(href)}" not reachable in the sheet`); continue; }
    try { await a.tap({ timeout: 5000 }); } catch { fail(`phone: "${path(href)}" is in the sheet but cannot be scrolled to or tapped`); continue; }
    await landed(p, path(href), 'phone ' + path(href));
    n++;
  }
  console.log(`phone: ${n}/${new Set(items).size} same-site sheet links tapped`);
  await p.close();
}

// 5. URLs as people type them
{
  const cap = (r) => r.split('/').map((s) => (s ? s[0].toUpperCase() + s.slice(1) : s)).join('/');
  const variants = (cfg.typed || []).flatMap((r) => [[cap(r), r], [r + '/', r], [r + '.html', r], [r.toUpperCase(), r]]).concat(cfg.extraVariants || [])
    .filter(([t], i, all) => all.findIndex(([u]) => u === t) === i); // /A is both the Title and UPPER form of /a
  const p = await b.newPage({ viewport: { width: 1280, height: 800 } });
  const base = path(BASE);
  for (const [typed, want] of variants) {
    await p.goto(BASE + typed, { waitUntil: 'networkidle' }).catch(() => {});
    await landed(p, base + '/' + want, `typed /${typed}`);
  }
  console.log(`typed URLs: ${variants.length} variants checked`);
  await p.close();
}

await b.close();
console.log(fails.length ? `\n${fails.length} navigation finding(s)` : '\nall navigation checks passed');
process.exit(fails.length ? 2 : 0);
