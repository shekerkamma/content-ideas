/**
 * Hard preflight for every render gate in this skill.
 *
 * Upstream (plugin87/ux-ui-agent-skills) each gate opened with:
 *
 *     try { ({ chromium } = await import('playwright')); }
 *     catch { console.log('<gate>: playwright not installed — SKIPPED'); process.exit(0); }
 *
 * Exit 0 on a missing browser means the gate reports success while measuring
 * nothing. Upstream CI installs Chromium in a dedicated job so it never bites
 * there, but anyone running the gates locally — or wiring them into another
 * repo's test command — gets a green light over an unmeasured page. A check
 * that goes green because the thing it measures went away is worse than no
 * check: it now certifies the defect.
 *
 * Here a missing browser is BLOCKED (exit 1) on stderr, and axe-core must be
 * resolved from a local install — never a CDN, so two runs of one gate cannot
 * disagree because a remote build moved.
 *
 * Exit codes used by every gate that imports this:
 *   0  clean
 *   1  blocked (no playwright, no browser binary, no local axe-core, nothing to measure)
 *   2  findings (the gate ran and the page failed)
 *
 * DESIGN_TOKENS_CHROMIUM overrides which binary is used:
 *   <path>  an explicit Chromium/Chrome executable — checked for existence first,
 *           because setting executablePath never verifies the file is there and a
 *           wrong path launches nothing while looking configured.
 *   auto    use any Chromium build present in the Playwright cache when the build
 *           this Playwright expects is absent. The chosen path and browser version
 *           are always printed — the substitution is never silent.
 */
import { existsSync, readdirSync } from 'node:fs';
import { homedir } from 'node:os';
import { join } from 'node:path';
import { createRequire } from 'node:module';

export const BLOCKED = 1;
export const FINDINGS = 2;

const CACHE = process.env.PLAYWRIGHT_BROWSERS_PATH || join(homedir(), '.cache', 'ms-playwright');

export function blocked(what, how) {
  console.error(`BLOCKED: ${what}`);
  for (const line of [].concat(how)) console.error(`  ${line}`);
  console.error('  This gate did not run. Nothing was measured — do not read this as a pass.');
  process.exit(BLOCKED);
}

/** Chromium executables actually present in the Playwright cache, newest build first. */
function cachedChromium() {
  let entries;
  try { entries = readdirSync(CACHE); } catch { return []; }
  const found = [];
  for (const dir of entries) {
    const m = dir.match(/^chromium(?:_headless_shell)?-(\d+)$/);
    if (!m) continue;
    for (const rel of ['chrome-linux64/chrome', 'chrome-linux/chrome',
                       'chrome-headless-shell-linux64/chrome-headless-shell',
                       'chrome-mac/Chromium.app/Contents/MacOS/Chromium',
                       'chrome-win/chrome.exe']) {
      const p = join(CACHE, dir, rel);
      if (existsSync(p)) { found.push({ build: Number(m[1]), path: p }); break; }
    }
  }
  const seen = new Set();
  return found.sort((a, b) => b.build - a.build)
              .filter(c => !seen.has(c.build) && seen.add(c.build));
}

/**
 * Import Playwright and launch a browser, or exit 1. Never returns a stub.
 */
export async function openBrowser(opts = {}) {
  let chromium;
  try {
    ({ chromium } = await import('playwright'));
  } catch {
    blocked('playwright is not installed, so no page can be rendered.',
            'npm i -D playwright && npx playwright install --with-deps chromium');
  }

  const pin = process.env.DESIGN_TOKENS_CHROMIUM;
  if (pin && pin !== 'auto') {
    if (!existsSync(pin)) {
      blocked(`DESIGN_TOKENS_CHROMIUM points at ${pin}, which does not exist.`,
              'executablePath is accepted without being checked — a path that is set is not a path that resolves.');
    }
    const browser = await chromium.launch({ executablePath: pin, ...opts })
      .catch(e => blocked(`the pinned browser at ${pin} failed to launch: ${String(e.message || e).split('\n')[0]}`,
                          'Check it is a Chromium/Chrome build for this platform.'));
    console.error(`# browser: pinned ${pin} (${await browser.version()})`);
    return browser;
  }

  const failures = [];
  for (const attempt of [{ label: 'system Chrome', args: { channel: 'chrome', ...opts } },
                         { label: 'bundled Chromium', args: { ...opts } }]) {
    try { return await chromium.launch(attempt.args); }
    catch (e) { failures.push(`${attempt.label}: ${String(e.message || e).split('\n')[0]}`); }
  }

  const cached = cachedChromium();
  if (pin === 'auto' && cached.length) {
    const pick = cached[0];
    const browser = await chromium.launch({ executablePath: pick.path, ...opts })
      .catch(e => blocked(`cached Chromium build ${pick.build} failed to launch: ${String(e.message || e).split('\n')[0]}`,
                          `Builds present: ${cached.map(c => c.build).join(', ')}`));
    console.error(`# browser: cached build ${pick.build} (${await browser.version()}) — DESIGN_TOKENS_CHROMIUM=auto`);
    return browser;
  }

  blocked(
    `playwright is installed but no browser launched (${failures.join(' | ')}).`,
    cached.length
      ? [`Builds present in ${CACHE}: ${cached.map(c => c.build).join(', ')} — this Playwright wants a different one.`,
         'Fix: npx playwright install --with-deps chromium',
         'Or:  DESIGN_TOKENS_CHROMIUM=auto (use the newest cached build) / =<path> (pin one).']
      : ['npx playwright install --with-deps chromium'],
  );
}

/**
 * Inject axe-core from the local install only. A CDN fallback would make the
 * gate depend on the network and let the rule set drift between runs.
 */
export async function injectAxe(page) {
  const require = createRequire(import.meta.url);
  let axePath;
  try { axePath = require.resolve('axe-core/axe.min.js'); }
  catch {
    for (const p of ['node_modules/axe-core/axe.min.js', join(process.cwd(), 'node_modules/axe-core/axe.min.js')]) {
      if (existsSync(p)) { axePath = p; break; }
    }
  }
  if (!axePath) {
    blocked('axe-core is not installed locally.',
            'npm i -D axe-core   # local on purpose: no CDN fallback, so the rule set cannot drift between runs');
  }
  await page.addScriptTag({ path: axePath });
  const version = await page.evaluate(() => (window.axe && window.axe.version) || 'unknown');
  return { path: axePath, version };
}
