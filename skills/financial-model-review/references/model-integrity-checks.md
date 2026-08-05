# Model Integrity Checks

The standard identity set, plausibility bands, and the questions that separate an
aggressive plan from an incoherent one.

## Tier 1 — Identities that must hold exactly

Encode every one of these that the model exposes. Each is arithmetic, not
opinion, so a failure is `Verified` at the strongest grade.

| Identity | Terms |
|---|---|
| Revenue − COGS = Gross Profit | `Revenue: 1, COGS: -1, Gross Profit: -1` |
| Opex components = Total Overheads | `sums.of: [Payroll, R&D, S&M, G&A]` |
| Gross Profit − Overheads = EBITDA | `Gross Profit: 1, Total Overheads: -1, EBITDA: -1` |
| EBITDA − D&A = EBIT | `EBITDA: 1, D&A: -1, EBIT: -1` |
| EBIT − Interest = EBT | `EBIT: 1, Interest: -1, EBT: -1` |
| EBT − Tax = Net Income | `EBT: 1, Tax: -1, Net Income: -1` |
| Segment revenues = total revenue | `sums.of: [<each segment>]` |
| Segment gross profits = total gross profit | `sums.of: [<each segment GP>]` |
| Units × ASP = line revenue | check per product, per period |
| Closing cash = opening + net flows | where a cash statement exists |
| Balance sheet balances | assets = liabilities + equity |

Set `tolerance` to the model's own rounding unit. Anything inside it is noise;
anything outside is a break that must be explained before interpretation.

### The tell to watch for

When a break's magnitude equals another figure in the model — a prior-year loss,
a single segment, one quarter — the cause is usually a **cumulative value sitting
in a periodic row**, or a carryforward applied at the wrong line. Check that
before concluding "typo". A loss carried forward belongs in *taxable income*, not
subtracted from net income; done wrong it makes a profitable year print a loss.

## Tier 2 — Cross-document reconciliation

Where the model is accompanied by a pitch deck, information memorandum, board
paper, or an earlier model version, reconcile every headline figure across all of
them. Build a table: figure, value in each document, which one this review uses,
and why.

Two failure modes matter more than the rest:

- **A figure circulated to third parties that the current model contradicts.**
  This is a disclosure issue, not a modelling issue, and it is almost always
  Blocking regardless of size.
- **Documents that disagree in *opposite directions* on linked figures** — e.g. a
  memorandum showing lower revenue *and* higher margin than the model. That
  combination cannot come from a single consistent build, so at least one
  document contains a figure nobody re-derived.

If the workbook itself contains a reconciliation tab, it is a claim under review,
not a source of truth. Test its assertions literally — including prose ones like
"totals reconcile exactly".

## Tier 3 — Plausibility bands

These do not fail arithmetically. They fail against the world, so they are
`Benchmarked` when a source is cited and `Judgement` otherwise.

**Gross margin trajectory.** A rising gross margin is a claim about learning
curve, mix shift, or pricing power. The model must say which, and the driver
sheet must show it. Hardware selling physical BOM does not reach software-like
margins by assertion — if a kit business shows 55% → 89%, locate the mix shift
that does the work, or mark it unsupported.

**ASP over time.** Flat ASPs across five-plus years in a market with real price
erosion is a claim. Semiconductor and sensor ASPs typically decline; a model
holding them flat *and* expanding margin is making two aggressive claims that
compound.

**Opex ratios at scale.** R&D or S&M staying at a constant percentage of revenue
while revenue grows 100× implies headcount and spend scaling perfectly linearly
for years. Check the implied headcount against the payroll line.

**Financing coherence.** Constant interest across all periods implies no
incremental borrowing despite growth. For a hardware business, working capital —
inventory and receivables — consumes cash roughly in proportion to revenue. A
model that scales revenue enormously on a fixed raise, with no cash-flow
statement, has not demonstrated it is funded. Say that as a **gap**, not as a
computed shortfall: without a cash statement the review cannot quantify it.

**Growth rate.** Compute the CAGR and state it plainly. Very high CAGRs are not
automatically wrong — they are the point of an early-stage plan — but they must
be attributed to specific, checkable drivers rather than to a curve.

## Tier 3b — Projection-stage models (fundraising)

When the workbook is a forward plan supporting a raise, every figure is an
assumption. That changes what counts as a defect.

**Aggressive is not a defect. Incoherent is.** A venture plan is *supposed* to
show a hockey stick — that is the asset being sold. Critiquing a high CAGR as
"implausible" is naive and will be dismissed. The real question is whether the
growth is decomposed into drivers an investor can check. A model built on
units × ASP per product is already better than most; say so.

**Arithmetic breaks cost more here, not less.** An analyst re-derives the P&L in
ten minutes. A broken identity in a document asking for money reads as
carelessness about the one thing the founder controls completely, and it taints
figures that are actually fine. These are the cheapest fixes with the highest
credibility return — rank them first even when small.

**Test whether a segment build is genuinely bottom-up.** Lay every segment's
margin (or growth, or conversion) side by side across all periods. If different
businesses land on *identical* rates — 80.0 / 83.0 / 86.0 / 89.0 across a kit
business, a robotics line, and a defence line — that is one global assumption
applied top-down while wearing a segment costume. Segmentation then adds
presentation, not evidence, and the model cannot answer "which line drives the
outcome" no matter how many tabs it has.

**Run the margin bridge before the investor does.** Decompose a margin change
into *mix* (revenue shifting toward higher-margin lines) and *rate*
(within-segment improvement):

- hold each segment's early-period rate constant, apply the terminal-period
  revenue mix → the difference from the early blended rate is the **mix effect**
- the remainder to the actual terminal blended rate is the **rate effect**

This matters because "we shift toward software and silicon" is the natural
narrative defense, and it is often quantitatively false. If mix explains a small
share of the expansion, the story rests entirely on within-segment cost-down and
must be defended on that basis instead.

**Convert every rate assumption into a physical unit.** This is where projections
become falsifiable:

- a gross margin plus an ASP implies a **BOM per unit** — check it against what
  the bill of materials actually contains
- a payroll line implies **headcount**
- an S&M ratio implies **revenue per salesperson**
- a unit forecast implies **production capacity and lead times**

A margin assumption is arguable. "This kit contains compute, software, and a
sensor suite, and the model requires its BOM to fall to ₹27,500" is checkable by
anyone who has built hardware — and that is the form the objection will take in
the meeting.

**Fundraise-specific gaps that outrank accounting nits:**

- **Uses of funds.** Sources stated without a uses waterfall answers half the
  question being asked.
- **Runway and cash flow.** The investor is buying "how long does this money
  last." A plan with no cash statement cannot answer it, and for hardware,
  working capital consumes cash roughly in proportion to revenue.
- **Sensitivity-ability.** A hardcoded workbook cannot be flexed in a live
  meeting. When an investor asks "halve the truck-kit volume", the answer must
  take seconds, not a rebuild. Treat "the model cannot be sensitized" as a
  fundraising defect in its own right.
- **Contradiction with already-circulated documents.** Highest severity. An
  information memorandum in investors' hands that disagrees with the current
  model is discoverable by anyone holding both, and no explanation of the
  discrepancy is as good as not having it.

## Tier 4 — Structural findings

- **No formulas anywhere.** The workbook is a values dump, so no calculation
  chain can be audited from the file. Every identity must be re-derived
  externally, and the "source model" that produced it is the real artifact under
  review. Report prominently.
- **Concentration.** Report the share of the terminal year carried by the largest
  segment or product. When one line carries most of the outcome, the review is
  really a review of that line.
- **Missing statements.** No cash flow, no balance sheet, no headcount build, no
  working-capital assumptions. State what is absent and what conclusions are
  therefore unavailable — never infer them.
- **Author prose.** Notes in the sheets are claims. Test each one.
