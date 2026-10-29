# DeepGrid Interactive Site

A modern, animated, componentized web presentation of the DeepGrid Semi India
ADAS competitor dossier — built as a real React app instead of a static deck
render.

## Stack
- Vite 8 + React 19 + TypeScript
- Framer Motion 13 (scroll-driven, staggered, spring, AnimatePresence)
- Plain CSS with the deck's design tokens (dark navy `#081525` + cyan `#04B3C7`
  + status ramp)

## Data
Single source of truth: `src/data/*.json` are the run's JSON artifacts
(`company-profiles.json`, `scoring.json`, `strategy-sections.json`,
`narrative.json`) imported and typed in `src/data.ts`. Nothing is re-typed.

## Commands
```bash
npm install            # deps (uses a local npm cache)
npm run dev            # local dev server
npm run build          # tsc + vite build -> single-file dist/index.html
npm run preview        # serve dist/
```

## WebMCP

The page registers nine imperative, read-only tools for in-browser agents:

- `navigate_dossier_section`
- `show_competitor`
- `show_hostile_question`
- `get_competitor_ranking`
- `compare_competitors`
- `find_evidence`
- `build_executive_brief`
- `recommend_competitive_response`
- `export_analysis`

`@mcp-b/webmcp-polyfill` initializes `document.modelContext` before React
mounts. Browsers without WebMCP support keep the normal human UI.

The build uses `vite-plugin-singlefile`, so `dist/index.html` is a single
self-contained file (~436 KB) that opens directly by double-click (no server).

## Structure
- `src/App.tsx` — shell, scroll-spy nav, scroll progress
- `src/components/` — Hero, ScaleChart, RelationshipMap, RankingChart,
  Timelines, Tables, CompanyExplorer, Posture, ExecAction, HostileAccordion
- `src/data.ts` — typed re-exports + the log-scale exhibit constants

The build output (`dist/`) is fully static — deployable to any static host or
GitHub Pages.
