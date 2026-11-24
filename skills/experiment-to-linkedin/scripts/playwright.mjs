// Resolve the playwright package: $PLAYWRIGHT_ROOT, then the cwd, then the repo root
// (this file lives at <repo>/skills/experiment-to-linkedin/scripts/).
import { createRequire } from 'module';
import path from 'path';
import { fileURLToPath } from 'url';

export function loadPlaywright() {
  const here = path.dirname(fileURLToPath(import.meta.url));
  const roots = [process.env.PLAYWRIGHT_ROOT, process.cwd(), path.resolve(here, '../../..')].filter(Boolean);
  for (const root of roots) {
    try { return createRequire(path.join(root, 'package.json'))('playwright'); } catch { /* try next */ }
  }
  console.error(`Cannot find module 'playwright' under: ${roots.join(', ')}. Set PLAYWRIGHT_ROOT to a folder whose node_modules has it.`);
  process.exit(4);
}
