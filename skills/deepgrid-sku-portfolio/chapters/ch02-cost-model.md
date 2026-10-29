# Chapter 2: The 10x cost model, line by line
*Whitepaper Part Two, §2–2.1*

## Core Idea
An older process, a free design kit and an automated open flow cut the cost of a finished, tested, low-volume chip about ten times. The claim is deliberately small: four bills that a normal chip company pays are simply absent, which changes which order sizes make money.

## Frameworks Introduced
- **"Cannot", not "cleverer"**: the argument is structural. Deepgrid is not claiming better engineers than Texas Instruments; it is claiming a different cost base.
  - When to use: every competitive or investor cost conversation.
  - How: list the four invoices that become staff time (layout, tool licences, design months, full mask set), then show the order sizes that become profitable.
- **The per-chip cost ledger**: normal company versus Deepgrid, line by line (table below). Approval is listed separately, never hidden in overheads.
- **Supplier-quoted prices over estimates**: three numbers are now taken from supplier price pages, and one showed the earlier estimate was wrong in both directions.
  - How: sky130 shared run priced lower than assumed (overcharging nine chips); IHP priced by area, higher than assumed for the radar (undercharging the tenth).
- **Protected low-end entry**: a known strategy with a known failure mode (ch13). The entry is cheap small-volume programmes in a market the law protects.

## Key Concepts
- **MPW / shared factory run**: several designs share one mask set and wafer; ~100 packaged chips per design.
- **sky130 MPW price**: $14,950 (~₹14.3 L at ₹95.39/$), ~15 mm² of die area, 100 packaged chips.
- **IHP pricing**: €5,110–7,300 per mm²; a 6–10 mm² radar front end costs ₹34–80 L. An open-source option at €2,800/mm² requires publishing the design, which a defence radar cannot do.
- **Open flow**: Yosys (synthesis), OpenROAD (layout), TritonCTS (clock tree), TritonRoute (routing), OpenRCX (extraction), Magic and KLayout (final checks), all on Deepgrid's own computers.
- **Approval line**: ₹40–80 L per chip, listed separately (what it buys: ch12).
- **All-in per chip**: ₹0.6–1.2 Cr including approval; the two-die radar ₹1.4–1.8 Cr.
- **Gross margin at low volume**: 60–75% on protected 10,000-unit programmes.

## Mental Models
- Think of **one more design attempt as almost free**: when layout and tools are staff time, iteration cost collapses, and that is what lets a small company build a range instead of one chip.
- Use **"the volume at which each company wins"**: at 10 M units the incumbent has amortised its setup and buys wafers cheaper; at 10,000 units only the no-invoice cost base is profitable.
- Treat **a price estimate proven wrong at both ends** as a credibility asset when disclosed.

## Anti-patterns
- **Claiming to beat a mass-market chip at 10 M units**: "the fastest way to lose your trust"; the incumbent wins there.
- **Using one price range for two different factories**: sky130 and IHP price differently (per run versus per mm²).
- **Rolling approval cost into overhead**: hides the ₹40–80 L that every chip must spend.

## Reference Tables

| Cost item | Normal chip company | Deepgrid |
|---|---|---|
| Physical layout | $1–2 M outsourced per chip | in-house on free kits, staff time |
| Design tool licences | $0.5–1 M every year | free tools, near zero |
| Design time | 12–18 months per chip | design files in ≤30 days; chips every cycle |
| Prototype masks | $0.5–1 M full set | shared run: ₹14.3 L sky130; ₹34–80 L IHP |
| Testing and approval | rolled into project cost | ₹40–80 L per chip, listed separately |
| **Total per chip** | **$2–5 M** | **₹0.6–1.2 Cr including approval** |

## Worked Example
**Re-pricing the prototype line from supplier price pages (the correction the whitepaper makes):**
1. Old claim: "₹15–40 L per chip" for prototypes on any factory.
2. sky130: shared run $14,950 × ₹95.39 ≈ ₹14.26 L → ₹14.3 L for 100 packaged chips. Nine of ten chips were being over-costed.
3. IHP radar: €5,110–7,300/mm² × 6–10 mm² ≈ €30.7k–73k ≈ ₹34–80 L. The tenth chip was under-costed.
4. Rejected option: IHP's €2,800/mm² open-publication tier; a defence radar cannot be published.
5. Result: one range for two factories was wrong at both ends; the figures now show each factory's real price.

## Key Takeaways
1. The 10x claim rests on removed invoices, not superior engineering.
2. It is a low-volume advantage; concede the high-volume market explicitly.
3. Quote supplier prices where they exist, and disclose corrections in both directions.
4. Keep approval as a visible per-chip line.
5. Cheap iteration is the real enabler of a product range.

## Connects To
- **ch01**: the fixed-cost barrier this model removes.
- **ch05**: why one mistake still costs a full 168-day silicon cycle.
- **ch12**: what the ₹40–80 L approval budget actually buys.
- **ch14**: action 1, publishing the real all-in cost of the 130 nm test chip.
