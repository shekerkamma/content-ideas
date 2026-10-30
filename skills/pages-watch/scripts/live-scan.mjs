// Live leak scan: fetch one page on each site, crawl every JS chunk it loads (and the chunks those import),
// then count internal phrases (must be 0) and shipped-code controls (must be > 0).
// Usage: node live-scan.mjs <config.json> <site-url>...
import { readFileSync } from 'node:fs';

const [configPath, ...sites] = process.argv.slice(2);
if (!configPath || !sites.length) {
  console.error('usage: node live-scan.mjs <config.json> <site-url>...');
  process.exit(2);
}
const { page, must_be_zero: MUST_BE_ZERO, must_hit: MUST_HIT } = JSON.parse(readFileSync(configPath, 'utf8'));
let bad = 0;
for (const raw of sites) {
  const base = raw.endsWith('/') ? raw : raw + '/';
  const origin = new URL(base).origin;
  const res = await fetch(base + page);
  const html = await res.text();
  if (!res.ok) bad++;
  const seen = new Map([[page, html]]);
  const queue = [...html.matchAll(/(?:src|href)="([^"]+\.js)"/g)].map(m => new URL(m[1], base).href);
  while (queue.length) {
    const u = queue.shift();
    if (seen.has(u) || !u.startsWith(origin)) continue;
    const r = await fetch(u);
    const t = r.ok ? await r.text() : '';
    seen.set(u, t);
    for (const m of t.matchAll(/["'`(]((?:\.{1,2}\/|\/)[^"'`()\s]+?\.js)["'`)]/g)) queue.push(new URL(m[1], u).href);
  }
  const all = [...seen.values()].join('\n');
  console.log(`== ${base}${page} HTTP ${res.status}, last-modified ${res.headers.get('last-modified')}, ${seen.size - 1} JS files`);
  for (const p of MUST_BE_ZERO) { const n = all.split(p).length - 1; if (n) bad++; console.log(`  ${n === 0 ? 'ok  ' : 'LEAK'} ${n} × "${p}"`); }
  for (const p of MUST_HIT) { const n = all.split(p).length - 1; if (!n) bad++; console.log(`  ${n > 0 ? 'ok  ' : 'MISS'} ${n} × control "${p}"`); }
}
console.log(bad ? `live-scan: ${bad} problem(s)` : 'live-scan: clean, controls present');
process.exit(bad ? 1 : 0);
