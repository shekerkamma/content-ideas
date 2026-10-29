import { readFileSync } from 'node:fs';
export function blocks() {
  const raw = readFileSync('/home/sheke/content-ideas/runs/2026-08-29-deepgrid-financial-model-deck-rebuild/narration-script.md', 'utf8');
  const re = /\*\*(\d{2}) · [^*]+\*\*\n(.+?)(?=\n\*\*\d{2} ·|$)/gs;
  const out = {}; let m;
  while ((m = re.exec(raw)) !== null) out[parseInt(m[1], 10)] = m[2].replace(/\s+/g, ' ').trim();
  return out;
}
export const kill = (page) => page.evaluate(
  () => document.querySelectorAll('#google-hats-survey').forEach(e => e.remove())).catch(() => {});
