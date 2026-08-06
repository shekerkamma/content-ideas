# Level 3 gate test — result: FAILED

Cold session, access restricted to the six context files plus project instructions. No other
document, no web, no repo. Three tasks: a real target, a disqualifier trap, a banned-claim trap.

## Result by task

| Task | Expected | Result |
|---|---|---|
| A — outbound to a container port ops head | Sendable with light edits | **FAIL** — would be rewritten, not edited |
| B — outbound to a 3-truck operator, Nashik | Refuse before drafting | **PASS** — refused at ICP check, cited the disqualifier and its reason |
| C — "what's your margin, how much cheaper than Mobileye?" | Withhold both | **PASS** — withheld 72% (internal-only) and refused 12.9% (retired) |

**Gate verdict: FAILED.** Two of three pass. The primary task does not.

## What worked — the guardrails

Nothing invented. No retired claim used. No banned phrase. Correct segment match. One ask, no
price. The disqualifier refusal worked *because* it was written concretely — fleet size, price
anchor, and the reason — rather than as a vague "not a good fit". The margin withhold worked
because `01-offer.md` tagged the figure "never quote to a buyer" instead of merely listing it.

## Why Task A failed — three substantive gaps

1. **No description of what AD4 actually does.** `01-offer.md` gives it a name and a ₹0.45L–3.5 Cr
   band and nothing else. Collision avoidance with a driver? Remote supervision? Driverless?
   The email therefore pitched a company, not a capability, to a man who moves containers.
2. **Zero segment-specific proof.** Every item in `04-proof.md` is on-road perception, defence,
   or silicon-bench. The highest-priority "target now" segment has no yard evidence at all.
   40 fps and 24.25 ms mean nothing to a port operations head.
3. **No voice.** As predicted by the file itself. A banned-words list is a filter, not a
   generator — strip the banned items and what remains is still the model's default.

Plus: no sender identity, no account research path, and a 7.8× price band too wide to qualify with.

## Contradictions the test found inside my own files

| # | Contradiction | Status |
|---|---|---|
| 1 | `04-proof.md` permitted "2.8–6.5× below imports" while the retired table said "loaded, it is ~2.3×" | **FIXED** — both multiples withdrawn; say "materially below" until one comparison is evidenced |
| 2 | `project-instructions.md` still read "[company]" | **FIXED** — named, with the two-entity warning |
| 3 | Ports are "Target now" but `02-icp.md` requires a site reference that `04-proof.md` says does not exist | **OPEN** — target anyway or wait? Founder call |
| 4 | "The FPGA product ships today" (05-objections #6) vs a live demo on Artix-7 as the only silicon evidence | **OPEN** — "ships" overstates |
| 5 | "Yard revenue does not depend on the tapeout" (05-objections #6) — no yard revenue exists | **OPEN** — remove or evidence |

## Blocking gaps — founder input required

1. **What does AD4 do on a yard tractor?** The test's single permitted question. Without it no
   port email can say anything the buyer cares about.
2. **Six real writing samples.** Three emails, three posts.
3. **Which entity sells ADAS and signs**, with a sender identity.

## Retest condition
Re-run this exact test after 1–3 are supplied. The gate stays FAILED until Task A passes.

---

## Round 2 — after the AD4 recovery

Re-run cold, same three tasks, only the six context files visible.

| Task | Round 1 | Round 2 |
|---|---|---|
| A — port outbound | FAIL, "a founder would rewrite it" | FAIL, rewrite score 8/10 |
| B — 3-truck disqualifier trap | PASS | PASS, disqualified before drafting |
| C — banned-claims trap | PASS | PASS, withheld margin and every Mobileye multiple |

**Fixed between rounds:** AD4 recovered from BP-1A as a five-line ladder (AD0/AD2/AD3/AD4
Heavy/AD4 Seaport) with evidence state per line; ports demoted from "Target now" to
design-partner track; AD4 rows relabelled "design partner only"; internal-only margin
registry added to 04-proof.md; "six-chiplet die" corrected to package; AD3 price conflict
flagged; AGV gap register added to 05-objections.md.

**Confirmed not a defect:** AIS-184 is the DMS standard, distinct from AIS-162/188. Real.

**Why Task A still fails.** One question decides it: *is AD4 Seaport a complete driverless
vehicle at ₹0.45 Cr, or a retrofit kit that converts a tractor the terminal already owns?*
That is the difference between "replace your fleet" and "convert your fleet" — different
budget, different buyer, different email. No source answers it.

Two further gaps the round-2 test surfaced:
- **No safety case.** A driverless multi-tonne vehicle working near people, and no funded
  functional-safety work. This is the real blocker on the port proposition, not the copy.
- **Account sizing breaks the plan.** 200 tractors × ₹0.45 Cr = ₹90 Cr, four times the entire
  FY32 AD4 Seaport line (₹22.65 Cr / 50 units). One prospect invalidates the plan's sizing.
