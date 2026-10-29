#!/usr/bin/env node
// Every route at every width: status, errors, structure, design defaults and axe-core WCAG 2.2 A/AA.
// usage (from the target project's directory): node <skill>/scripts/sweep.mjs qa/sweep.json
// exit 0 clean · 2 findings · 1 BLOCKED (no playwright / axe-core / base unreachable): never a silent skip.
// Design-default items (em dashes, counters, pills...) are reported; they fail the run only with
// "strictDesign": true, because a look the user pinned may legitimately carry them.
// Every same-site link on every page is also requested once: the nav gate covers menus, and a dead link
// inside page content (a CTA to a route that was never built) is otherwise invisible to every other gate.
import { createRequire } from 'module';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'fs';
import { resolve } from 'path';

const blocked = (m) => { console.error('BLOCKED: ' + m); process.exit(1); };
const cfgPath = process.argv[2] || 'qa/sweep.json';
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
let AXE;
try { AXE = readFileSync(cfg.axe ? resolve(cfg.axe) : need('axe-core/axe.min.js', 'resolve'), 'utf8'); } catch { blocked('axe-core not found in the site, $E2E_QA_NODE_MODULES, or the skill repo (npm i -D axe-core, or set "axe")'); }
console.log(`deps: playwright from ${served.playwright}, axe-core from ${cfg.axe || served['axe-core/axe.min.js']}`);

const BASE = cfg.base.replace(/\/?$/, '/');
const widths = cfg.widths || [[1440, 900, 'desktop'], [390, 844, 'phone']];
const out = cfg.out || 'qa/sweep-results.json';
const shots = cfg.shots || 'qa/shots';
mkdirSync(shots, { recursive: true });
try { const r = await fetch(BASE); if (!r.ok && r.status !== 404) blocked(`${BASE} answered ${r.status}`); } catch { blocked(`${BASE} is not reachable (start scripts/serve_pages.py)`); }

const b = await chromium.launch({ args: cfg.webgl === false ? [] : ['--use-gl=angle', '--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const rows = [];
for (const [w, h, tag] of widths) for (const route of cfg.routes) {
  const p = await b.newPage({ viewport: { width: w, height: h }, ...(w < 700 ? { isMobile: true, hasTouch: true } : {}) });
  const errs = [], failed = [];
  p.on('pageerror', (e) => errs.push(e.message.slice(0, 160)));
  const expect404 = /no-such|missing|404/.test(route);
  // the 404 route's own document 404 is the expected answer, not an error; anything else it loads still counts
  p.on('console', (m) => m.type() === 'error' && !(expect404 && m.location().url === BASE + route) && errs.push(m.text().slice(0, 160)));
  p.on('response', (x) => { if (x.status() >= 400 && !x.url().endsWith('/' + route)) failed.push(x.status() + ' ' + x.url().replace(BASE, '')); });
  const res = await p.goto(BASE + route, { waitUntil: 'networkidle', timeout: 60000 }).catch(() => null);
  await p.waitForTimeout(400);
  await p.screenshot({ path: `${shots}/${tag}-${(route || 'home').replace(/[/?#]/g, '_')}.png` });
  const H = await p.evaluate(() => document.body.scrollHeight);
  for (let y = 0; y < H; y += Math.round(h * 0.8)) { await p.evaluate((v) => scrollTo({ top: v, behavior: 'instant' }), y); await p.waitForTimeout(60); }
  await p.waitForTimeout(600);
  await p.evaluate(() => scrollTo({ top: 0, behavior: 'instant' }));
  await p.waitForTimeout(250);
  const m = await p.evaluate(([reveal, fonts, minTarget, base, vw]) => {
    const vis = (e) => { const r = e.getBoundingClientRect(); const c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && !e.closest('[hidden],[aria-hidden="true"]'); };
    const text = document.body.innerText;
    const around = (re) => { const o = []; let x; const g = new RegExp(re.source, 'g'); while ((x = g.exec(text)) && o.length < 3) o.push(text.slice(Math.max(0, x.index - 35), x.index + 35).replace(/\s+/g, ' ')); return o; };
    const heads = [...document.querySelectorAll('h1,h2,h3,h4,h5,h6')].filter(vis);
    const skips = []; let prev = 0;
    for (const x of heads) { const l = +x.tagName[1]; if (prev && l > prev + 1) skips.push(`h${prev}->h${l} "${x.textContent.trim().slice(0, 40)}"`); prev = l; }
    const inter = [...document.querySelectorAll('a[href],button,input,select,textarea,[role=button],[role=tab]')].filter(vis);
    const small = inter.filter((e) => { const r = e.getBoundingClientRect(); return (r.width < minTarget || r.height < minTarget) && !(e.tagName === 'A' && getComputedStyle(e).display === 'inline') && !['checkbox', 'radio'].includes(e.type); });
    const pills = inter.filter((e) => { const r = e.getBoundingClientRect(); return r.height > 20 && parseFloat(getComputedStyle(e).borderTopLeftRadius) >= r.height / 2 - 1 && r.width > r.height * 1.4; });
    const leaves = [...document.querySelectorAll('body *')].filter((e) => e.children.length === 0 && vis(e));
    const noBox = [...document.images].filter((i) => vis(i) && !(i.getAttribute('width') && i.getAttribute('height')) && getComputedStyle(i).aspectRatio === 'auto');
    const kickers = [...document.querySelectorAll('.kicker, .eyebrow, [class*="kicker"]')].filter(vis).length;
    return {
      // same-site hrefs, hash and query dropped; checked once each after the sweep
      links: [...new Set([...document.querySelectorAll('a[href]')].map((a) => { try { const u = new URL(a.href); u.hash = ''; u.search = ''; return u.href; } catch { return ''; } })
        .filter((h) => h.startsWith(base)))],
      title: document.title, h1: heads.filter((x) => x.tagName === 'H1').length, skips,
      // Against the configured width, not innerWidth: with isMobile (phone rows) the layout viewport grows to
      // fit wide content, so scrollWidth - innerWidth reads 0 on a page that scrolls sideways. A product bar
      // 31 px too wide passed this sweep at 390 and failed CI's clientWidth check (2026-10-01).
      overflowX: Math.max(document.documentElement.scrollWidth, document.body.scrollWidth) - vw,
      broken: [...document.images].filter((i) => i.complete && i.naturalWidth === 0 && i.getAttribute('src')).map((i) => i.getAttribute('src').slice(-60)),
      noBox: noBox.map((i) => (i.getAttribute('src') || '').slice(-60)).slice(0, 4), noBoxN: noBox.length,
      small: small.length, smallSample: [...new Set(small.map((e) => `${String(e.className).split(' ')[0] || e.tagName}:${Math.round(e.getBoundingClientRect().width)}x${Math.round(e.getBoundingClientRect().height)}`))].slice(0, 5),
      // A disclosure whose only content is its summary opens onto nothing: v6's evaluation guide shipped
      // empty on eleven routes because its body component returned null for routes without a brief.
      emptyDisclosures: [...document.querySelectorAll('details')].filter((d) => vis(d) && ![...d.children].some((c) => c.tagName !== 'SUMMARY' && (c.textContent.trim() || c.querySelector('img,svg,canvas,video,iframe')))).map((d) => (d.querySelector('summary')?.textContent || '').trim().slice(0, 40)),
      unrevealed: reveal ? [...document.querySelectorAll(reveal)].filter((e) => e.getClientRects().length && parseFloat(getComputedStyle(e).opacity) < 0.99).length : 0,
      // text whose rendered first family is outside the declared type system (runtime proof, not a CSS grep)
      offFont: (() => {
        if (!fonts.length) return [];
        const seen = new Map();
        for (const e of leaves) {
          if (!e.textContent.trim()) continue;
          const fam = getComputedStyle(e).fontFamily.split(',')[0].trim().replace(/^["']|["']$/g, '');
          if (fonts.some((f) => fam.toLowerCase() === f.toLowerCase())) continue;
          const key = fam + ' @ ' + (String(e.className).split(' ')[0] || e.tagName.toLowerCase());
          seen.set(key, (seen.get(key) || 0) + 1);
        }
        return [...seen].map(([k, n]) => `${k} x${n}`).slice(0, 8);
      })(),
      // Lordicon's free licence requires a visible credit; an animated icon with no link back is a breach
      lordiconNoCredit: (document.querySelector('lord-icon, [src*="cdn.lordicon.com"], script[src*="lordicon"]')
        && ![...document.querySelectorAll('a[href]')].some((a) => /lordicon\.com/i.test(a.href))) || false,
      design: {
        emDash: (text.match(/—/g) || []).length, emDashAt: around(/—/),
        // typewriter quotes in running text: an apostrophe between letters, or a straight double quote
        straightQuotes: (text.match(/[A-Za-z]'[A-Za-z]|"/g) || []).length, straightQuotesAt: around(/[A-Za-z]'[A-Za-z]|"/),
        counters: leaves.filter((e) => /^(0\d|\d{2}\s*\/\s*\d{2})$/.test(e.textContent.trim())).length,
        italicHeads: heads.filter((x) => x.querySelector('em,i') || getComputedStyle(x).fontStyle === 'italic').map((x) => x.textContent.trim().slice(0, 50)),
        monoLabels: leaves.filter((e) => /mono|courier/i.test(getComputedStyle(e).fontFamily) && e.textContent.trim().length > 1 && e.textContent.trim().length < 40).length,
        pills: pills.length,
        // icons must be SVG: a small raster image blurs at 2x and cannot take a token colour
        rasterIcons: [...document.images].filter((i) => { const r = i.getBoundingClientRect(); const src = i.currentSrc || i.src || '';
          return vis(i) && r.width > 0 && r.width <= 48 && r.height <= 48 && !/\.svg(\?|#|$)|^data:image\/svg/i.test(src); })
          .map((i) => (i.getAttribute('src') || '').slice(-50)).slice(0, 5),
        eyebrowsPerH2: +(kickers / Math.max(1, heads.filter((x) => x.tagName === 'H2').length)).toFixed(2),
      },
    };
  }, [cfg.reveal || '', cfg.allowedFonts || [], cfg.minTarget || 24, BASE, w]);
  await p.addScriptTag({ content: AXE });
  const axe = await p.evaluate(async () => (await window.axe.run(document, { runOnly: ['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa'] })).violations
    .map((v) => ({ id: v.id, impact: v.impact, n: v.nodes.length, sample: v.nodes.slice(0, 2).map((x) => x.target.join(' ') + ' | ' + ((x.failureSummary || '').split('\n')[1] || '').trim()) })));
  const status = res ? res.status() : 0;
  rows.push({ width: tag, route: route || '/', status, statusOk: expect404 ? status === 404 : status < 400, errs: [...new Set(errs)], failed: [...new Set(failed)], ...m, axe });
  await p.close();
}
await b.close();

// One request per distinct link across the whole run; a link is dead when it ends in 4xx/5xx or never answers.
const linkStatus = new Map();
// node:http(s), not fetch: undici's parser asserted (`assert(!this.paused)`) on a socket the server closed,
// and the throw lands outside any try, killing the run after every page had loaded (v10 QA, 2026-10-04).
// Reading the body did not prevent it. Follows up to five redirects; no answer in 15 s counts as dead.
const { default: http } = await import('node:http'); const { default: https } = await import('node:https');
const probe = (href, hops = 5) => new Promise((resolve) => {
  let u; try { u = new URL(href); } catch { return resolve(0); }
  const req = (u.protocol === 'https:' ? https : http).get(u, { agent: false, headers: { 'user-agent': 'e2e-qa-review' } }, (res) => {
    res.resume();
    const loc = res.headers.location;
    if (res.statusCode >= 300 && res.statusCode < 400 && loc && hops > 0) return resolve(probe(new URL(loc, u).href, hops - 1));
    resolve(res.statusCode || 0);
  });
  req.setTimeout(15000, () => { req.destroy(); resolve(0); });
  req.on('error', () => resolve(0));
});
for (const href of new Set(rows.flatMap((r) => r.links))) linkStatus.set(href, await probe(href));
for (const r of rows) {
  r.deadLinks = r.links.filter((h) => { const s = linkStatus.get(h); return !s || s >= 400; }).map((h) => `${linkStatus.get(h) || 'no answer'} ${h.replace(BASE, '/')}`);
  r.linksN = r.links.length; delete r.links;
}

const titles = rows.filter((r) => r.width === widths[0][2] && r.statusOk && !/no-such|missing|404/.test(r.route)).map((r) => r.title);
const dupTitles = [...new Set(titles.filter((t, i) => titles.indexOf(t) !== i))];
const hard = (r) => !r.statusOk || r.errs.length || r.failed.length || r.h1 !== 1 || r.skips.length || r.overflowX > 0 || r.broken.length || r.noBoxN || r.small || r.unrevealed || r.offFont.length || r.lordiconNoCredit || r.deadLinks.length || r.emptyDisclosures.length || r.axe.length;
const soft = (r) => r.design.emDash || r.design.straightQuotes || r.design.counters || r.design.italicHeads.length || r.design.pills || r.design.rasterIcons.length;
const hardN = rows.filter(hard).length, softN = rows.filter(soft).length;
writeFileSync(out, JSON.stringify({ base: BASE, loads: rows.length, dupTitles, rows }, null, 1));
console.log(`sweep: ${rows.length} loads, ${hardN} with findings, ${softN} with design-default items, ${dupTitles.length} duplicate titles -> ${out}`);
process.exit(hardN || dupTitles.length || (cfg.strictDesign && softN) ? 2 : 0);
