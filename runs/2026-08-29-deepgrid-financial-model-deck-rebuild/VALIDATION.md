# Deck validation — 90-slide Product Lines explainer

Validated 2026-08-31 against the sources that govern it. Method: every claim
rebuilt **from the source**, never from the slide that asserts it. A ledger
built from slide headlines passes by construction; this repo has been burned by
that before.

## Governing sources

| layer | source | location |
|---|---|---|
| financial | `Deepgrid_Semi_Financial_Model_Corrected_v3-sept.xlsx` | `~/Downloads`; ingested to `data/*.csv` |
| technical | `DeepGrid_Semi_-Aravind.pdf` (33 pp business plan) | `~/Downloads` |
| narrative / sims | `Deepgrid_Speciale_Deck.html`, `Deepgrid_DataMovement.html` | `refs/` |

`runs/2026-08-30-deepgrid-demand-tam-analysis/data/financial_model.xlsx` is
**byte-identical** to the v3-sept workbook (md5 `722e424ffa8a5f5713d43603793ab193`),
so the CSVs in that run and the ones in `data/` describe the same model.

## What reconciles exactly

- **All 15 SKUs.** FY2032 revenue rebuilt as `ASP x units` from `Revenue Build`
  rows 44-58 matches every "How it fits" slide at **delta 0.00** (one 0.05
  rounding on Seaport AGV). Shares within 0.05pp.
- **Total.** Reconstruction sums to **1128.45 Cr**, equal to the model's own P&L
  cell — delta +0.00. Segment totals sum to 100.0%.
- **Silicon spec.** The business plan's derivation is self-checking:
  `64 x 512 x 600 MHz x 2 / 1e12 = 39.3 TOPS` exactly. 32,768 MACs, 102.4 GB/s,
  ~57.1 mm2 TSMC 28nm HPC+ all present.
- **Demand and tapeout.** 1.0M trucks in scope / 0.5M new / 0.5M retrofit
  (Demand & TAM r10-r12), 18,000 FY32 AD2 units (r15), $3.17M programme NRE
  (Tapeout r14), $3.88 per die (r26, $3.876), 175k breakeven (r34, 174,908).
- **The weakest line is disclosed.** T100 AI licence (50 Cr, 4.4%) is flagged
  `ABSENT from Demand & TAM` in the reconciliation, and its slide already says
  the pool is not separately sized and to treat it as optionality.

## Where the two governing sources disagree

| # | item | financial model | business plan | deck follows | status |
|---|---|---|---|---|---|
| 1 | product lines / FY32 revenue | 15 lines, 1128.45 Cr | 26 lines, 1387.95 Cr | model | **open** |
| 2 | what 8.6 ms is measured on | — | **6 cameras** | "eleven channels" | **defect** |
| 3 | NRE | $3.17M | $2.42M | model | resolved by rule |

**#2 is a defect.** The business plan states *"6 Cameras. One Chip. 8.6ms of
33.3ms Budget"* and its spec table row *"AD2 frame budget 8.6ms / 33.3ms (74%
free)"*. It never says eleven channels, nor nine-cameras-plus-two-radar — that
framing traces only to `Deepgrid_Speciale_Deck.html`, a pitch artifact. Slides 6
and 7 should read **six cameras**. The eleven-channel sensor list is correct as
the AD2 kit's complement; it is not what was measured at 8.6 ms.

**#1 is a disclosure question, not an error.** The eleven business-plan lines the
deck omits (259.5 Cr: AD4 Heavy Transport AGV 105, AD4 Autonomous AUGV L4 37.5,
Agricultural 30, Defence 18, Intl Delivery Robovan 15, S100 die 13.5, AMR 12,
Utility 9, R100 die 7.5, Airport Patrol 6, Food Delivery 6) are **all** flagged
`ABSENT from Demand & TAM`. Excluding them is the conservative and correct
choice. Open question is whether the deck should say so, since an investor
holding both documents sees 26 lines and 1388 Cr in one and 15 and 1128 Cr in
the other.

**#3** — the xlsx governs financial data, so the deck's $3.17M is right. DeepGrid
should still know their own documents differ by $750k.

## Rerunning this

```bash
# ingest the governing workbook (never guesses between sheets)
~/.venvs/data/bin/python skills/ai-analyst/excel-ingest/scripts/excel_ingest.py \
  <model>.xlsx --all-sheets --out-dir runs/<run>/data
# then rebuild each claim from Revenue Build rows 44-58 and compare to the deck
```

Seven sheets, all `header_confidence: high`, **no merged ranges** — a
system-generated model, so the ingest needs no header override and nothing is
repaired.
