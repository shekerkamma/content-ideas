# DeepGrid Semi — Pre-Series A Investor & GTM Deck

**Artifact:** `DeepGrid-Semi-PreSeriesA-v2-reviewed.pptx` — 43 slides, 2.3 MB
**Delivered to:** `C:\Users\sheke\OneDrive\Desktop\` (fonts alongside in `DeepGrid-fonts\`)
**Status:** `reviewed` — contact-sheet QA + OfficeCLI QA (0 issues) + per-slide render comparison
**Editability:** hybrid-editable — 776 native PowerPoint text boxes over a rendered, text-free design background

## Design template

The palette, type roles and type scale were **extracted from the reference deck's own
`chrome.css`** (fetched from the Genspark project) and re-authored as an owned template:

| Token | Value |
|---|---|
| Grounds | `--bg-0 #05090F` · `--bg-1 #0A1220` · `--bg-2 #0F1A2E` · `--bg-3 #16243D` |
| Rules | `--line #1E3253` · `--line-soft #172642` |
| Ink | `#E8F1FF` / `#B7C7DE` / `#7A8CA6` / `#4E617D` |
| Accents | `--cyan #22D3EE` (wedge) · `--amber #F59E0B` (correction) · `--red #EF4444` (kill) · `--green #22C55E` (pass) |
| Type | Space Grotesk (headers) · IBM Plex Sans (body) · JetBrains Mono (rails/figures) |

Layout system, also taken from the reference: **1920×1080 stage**, 120 px margins,
1680 px content width, mono chrome rail + hairline at the top, mono footer rail with
slide number and disclaimer, panel cards on `--bg-2` with `--line` borders at 6 px radius,
and an 80 px wafer grid on the cover.

Files:
- `theme.css` — identity tokens only. **Swap this one file to reskin the whole deck.**
- `template.css` — structure: chrome rails, `.cbody` centred content column, and nine archetypes
  (cover, kpi band, card bands 2–5 up, chain, rows, split, callout, bars, sources).
- `build_deck.py` — emits `deck.html` from the 43-slide spec. Re-run to regenerate.

## Pipeline actually executed

1. Recovered the reference design via Windows Chrome DevTools MCP (the WSL-blocked lane) —
   read `chrome.css` plus the cover and three content slides to learn the archetypes.
2. Authored `theme.css` + `template.css` + `build_deck.py`; generated 43 slides.
3. Sanitize scan — no tool names, paths or internal production language on any slide.
4. `render.mjs` → 43 × 2560×1440 PNG (WSL Playwright Chromium, 1920 stage @ dsf 4/3).
5. `contact_sheet.py` → 4 sheets, **every slide inspected visually**.
6. `render_hybrid.mjs` → text-free backgrounds + 776 captured text boxes with font roles.
7. `build_editable_pptx.py` → native text over the design background.
8. `officecli_qa.py` → validate / issues / html / screenshot, and **per-slide renders compared
   against the HTML source**.

Pipeline scripts were retargeted from the 1280×720 template to the 1920×1080 reference stage
(`IN_PER_PX = 13.333/1920`, `PT_PER_PX = 0.5`), and the PPTX builder now carries a captured
`role` (display / body / mono) so the real font families survive into PowerPoint instead of
the previous hardcoded Segoe UI / Consolas.

## Defects found and fixed during QA

| # | Defect | Caught by | Fix |
|---|---|---|---|
| 1 | Content sat top-aligned, leaving the bottom third of most slides empty | contact sheet | Replaced per-slide magic top/height numbers with a `.cbody` column that vertically centres every band; cards stretch and pin their body low |
| 2 | Cover KPI band ran ~2 cm off-canvas | OfficeCLI `issues` | `.kpi.abs` inherited `width:100%`, which resolves against the 1920 px slide, not the 1680 px content width — pinned explicitly |
| 3 | Cover die label rendered `DGRID` and `ALPHA / 28nm` overlapping | per-slide PPTX render | A `<span>` styled `display:block` is double-captured (its text lands in the parent's runs *and* it becomes its own box). Reverted to inline + `<br>`, as the reference deck does |
| 4 | Bar captions collided (`margin` over `first silicon,`) | per-slide PPTX render | Same trap on `.bcap b` — audited the whole stylesheet for inline tags styled `display:block`; these were the only two |

Defects 3 and 4 are invisible to OfficeCLI (`issues: 0` throughout) because the text stays
inside the slide bounds — they are wrap/overlap defects. Only the render-versus-HTML
comparison catches them, which is why that step is not optional.

## Canonical numbers

Verified against `.claude/skills/deepgrid-gtm/references/canonical-numbers.md`:
₹55 Cr blended (₹45 Cr CCPS + ₹10 Cr CGTMSE) · ₹1,387.95 Cr FY32 · $3.876 die at 1M chips ·
~$30 board BOM · 12.9× vs Mobileye $50 ASP · $3.17M NRE with $370K (11.7%) at risk pre-gate ·
174,908 chips to break even in FY2032 · 39.3 TOPS INT8 · 96.7% predicted yield ·
53→88% margin walk · ₹536.63 Cr FY32 EBITDA (39%) · profitable from FY2029 · ₹2.48 Cr raised to date.

The four banned figures (**₹1,128 Cr**, **774×**, **$8M NRE**, **3,636-unit break-even**) plus
"under $3 die" and "₹25 Cr ask" appear **only** inside their own labelled correction rows on
slides 7, 27, 35 and 37 — never asserted as fact. The unverified insurance-premium-reduction
claim is named on slide 20 as a claim to stop using, and insurers are scored as anti-ICP.

## Fonts

Space Grotesk, IBM Plex Sans and JetBrains Mono are shipped as variable TTFs in
`DeepGrid-fonts\`. They are installed on the build machine, so the renders and QA are accurate.
**Install them on any machine that will present or edit the deck** — otherwise PowerPoint
substitutes and the typographic register is lost.

## Not client-ready under the vault design system

This is the hybrid path: layouts are a design background with native text on top. The
`Client-Ready PPTX Design System` forbids flattened layouts. If fully native objects are
required, route to `/vault-presales-pptx-pipeline` using `deck.html` and `build/png/*` as the
design reference.
