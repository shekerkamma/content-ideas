// deck-grid.mjs — LAYOUT AS SPECIFICATION.
//
// The problem this solves: hand-typing left/top/width for every object means layout is
// hard-coded, not specified — one label grows and every coordinate downstream is wrong.
//
// The mechanism: a 12-column grid + named vertical bands. You say "columns 1–4, band BODY"
// and the coordinates are DERIVED. Slides compose from templates, never from raw pixels.
// Coordinates are computed in JS (reliable, editable) on top of the proven absolute
// primitives — so native objects stay fully editable in PowerPoint.
//
// Canvas 1280×720 · margin 48 · 12 columns · gutter 20.

export const GRID = {
  W: 1280, H: 720, M: 48, COLS: 12, GUT: 20,
  get inner() { return this.W - 2 * this.M; },                 // 1184
  get colW() { return (this.inner - (this.COLS - 1) * this.GUT) / this.COLS; }, // ~78.7
  // vertical bands (top, height) — the spec's rows
  bands: {
    KICKER: [26, 18],
    TITLE:  [50, 46],
    SUB:    [100, 28],
    RULE:   [140, 2],
    BODY:   [168, 468],        // main content region
    FOOTER: [683, 34],
  },
};

// column-x: left edge of column i (1-based)
export function cx(i) { return GRID.M + (i - 1) * (GRID.colW + GRID.GUT); }
// span width: columns a..b inclusive (1-based)
export function span(a, b) { return (b - a + 1) * GRID.colW + (b - a) * GRID.GUT; }
// band accessors
export function bandTop(name) { return GRID.bands[name][0]; }
export function bandH(name) { return GRID.bands[name][1]; }

// EQUAL COLUMNS: return N boxes {x,w} that fill the body width with gutters.
// This is the flexbox "fr(1) fr(1) …" behaviour, computed. No coordinates typed.
export function cols(n, { left = GRID.M, right = GRID.W - GRID.M, gutter = GRID.GUT } = {}) {
  const total = right - left;
  const w = (total - (n - 1) * gutter) / n;
  return Array.from({ length: n }, (_, i) => ({ x: left + i * (w + gutter), w }));
}

// ROWS within a region: N stacked boxes {y,h} with gutter.
export function rows(n, { top, height, gutter = GRID.GUT } = {}) {
  const h = (height - (n - 1) * gutter) / n;
  return Array.from({ length: n }, (_, i) => ({ y: top + i * (h + gutter), h }));
}

// A 2-D CELL GRID: r rows × c cols inside a region -> array of {x,y,w,h}.
export function cellGrid(r, c, region) {
  const { top, height, left = GRID.M, right = GRID.W - GRID.M, gutter = GRID.GUT } = region;
  const C = cols(c, { left, right, gutter });
  const R = rows(r, { top, height, gutter });
  const out = [];
  for (const row of R) for (const col of C) out.push({ x: col.x, y: row.y, w: col.w, h: row.h });
  return out;
}
