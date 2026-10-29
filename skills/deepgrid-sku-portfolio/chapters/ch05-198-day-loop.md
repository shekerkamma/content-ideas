# Chapter 5: One loop every 198 days
*Whitepaper §5–5.3*

## Core Idea
Progress is measured in factory runs. One cycle is up to 30 days of design plus 168 days of silicon; the design half scales with engineers and money, the silicon half cannot be repeated, and working silicon is still 6–21 months from a sellable product.

## Frameworks Introduced
- **The design/silicon split**:
  - **Design (≤30 days)**: specification → circuit code → verification (iterates with circuit code, nothing else does) → layout → final checks. Limited by engineer count, which money buys.
  - **Manufacturing gate**: enough verification coverage, no timing failures, clean layout check. These are targets today, not history.
  - **Silicon (168 days)**: masks, wafers, packaging, testing. Cannot be repeated; one mistake costs a whole cycle, so enforce the design-complete gate before the factory window.
- **Two speeds, not one**:
  - Mostly digital (chips 1, 2, 4, 8, 9): verification on a computer; realistic time to a tested chip is one 198-day cycle plus 6–9 months.
  - Mostly analog (chips 3, 5, 6, 7): references and protection rings need silicon in hand; usually 2–3 silicon attempts, so two to three cycles plus approval.
  - This is why chips 1 and 2 (mostly digital, commercial) go first and carry early revenue.
- **Who makes the production batch (state it, do not assume it)**: the prototype service's published FAQ says prototype volumes of 100 units per design, with production "based on market demand". A verbal willingness to support production is real progress but is not a contract, quote or schedule. Next step: a written price for a production mask set and first wafer batch (action 3).
  - Uncomfortable consequence: one supplier covering prototype and production deepens single-supplier dependence.
  - Backups: SkyWater direct (sky130 is its own production process); SCL Mohali in India.
- **Silicon is not a product (the boundary)**: commercial chips ship 6–9 months after silicon (characterisation, datasheet, test programme, approval batches, customer design work); screened defence chips add 9–12 months of MIL-883, JSS and CEMILAC that no money shortens.

## Key Concepts
- **Cycle arithmetic**: 30 + 168 = 198 days (the earlier "180 days" headline used a rounded "about 150 days" guess).
- **CI2609 run**: design sent 16 September 2026 → packaged chips 3 March 2027 (168 days).
- **CI2612 run**: 7 December 2026 → 25 May 2027.
- **Design-complete gate**: the enforced check before the factory window.
- **Parallel runs**: split designs across runs so one slip does not stop everything.
- **Approval line**: ₹40–80 L per chip, separate (ch12).

## Mental Models
- Think of **design as elastic and silicon as fixed**: money compresses the first half only.
- Use **"one chip per cycle"** to size what a single loop delivers; range growth comes from the block library (ch06).
- Treat **a supplier's verbal yes as a hope with a next action**, not a line item.

## Anti-patterns
- **Letting the 30-day digital figure stand for the whole range**.
- **Fixing design errors during the factory window**: a miss costs ~6 months.
- **Presenting 180 days as the end of the schedule**: it ends with silicon, not a product.
- **Assuming production volume exists because prototypes do**.

## Reference Tables

| | Mostly digital | Mostly analog |
|---|---|---|
| Chips | 1, 2, 4, 8, 9 | 3, 5, 6, 7 |
| Design loop | ≤30 days to design files | one factory run per silicon-checked attempt |
| Attempts | limited by verification on a computer | usually 2–3, each needing silicon |
| Realistic time to a tested chip | one 198-day cycle + 6–9 months | two to three cycles + approval |

| After silicon | Added time | Controllable? |
|---|---|---|
| Commercial release | 6–9 months | partly |
| Defence screening (MIL-883, JSS, CEMILAC) | 9–12 months more | no |

## Worked Example
**Correcting the loop headline from the published factory calendar:**
1. Old statement: "about 150 days" of silicon, "180-day loop".
2. Source of truth: the shuttle calendar. CI2609: 16 Sep 2026 → 3 Mar 2027 = 168 days.
3. Full cycle: 30 design days + 168 silicon days = 198 days.
4. Decision: keep the loop name because the design half is the controlled part, but publish 198.
5. Principle: "We would rather correct our own headline than have you find the factory's calendar and correct it for us."

## Key Takeaways
1. A cycle is 198 days: 30 elastic, 168 fixed.
2. Analog chips need two to three cycles; schedule them across cycles 2 and 3.
3. The production route needs a written quote; a verbal indication is not a plan.
4. Budget 6–9 months commercial and 9–12 more for screening after silicon.
5. Commercial, mostly-digital chips go first because they reach revenue fastest.

## Connects To
- **ch06**: how a range grows faster than one chip per cycle.
- **ch12**: what happens in the months after silicon.
- **ch14**: the tightest link (chips arriving March and May 2027 for September production) and action 3.
