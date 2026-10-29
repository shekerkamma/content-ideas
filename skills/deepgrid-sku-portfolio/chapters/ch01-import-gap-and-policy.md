# Chapter 1: The import gap, and the law that created a buyer
*Whitepaper Part One, §1–1.3*

## Core Idea
India imports about $9 bn a year of simple, older-process chips that nobody in India makes. The cause is a fixed-cost barrier, not a skills gap, and recent procurement law now requires Indian parts, creating a buyer that imports can no longer serve.

## Frameworks Introduced
- **The import funnel (Figure 1)**: a sizing argument that walks down from the only external number to what is already sold, each step smaller and more believable.
  - When to use: any time a market size is stated to an investor or customer.
  - How: $23.4 bn total chip imports (UN COMTRADE HS 8542, ~70% from China and Taiwan) → $9 bn on ≥130 nm processes (÷2.6) → $0.46 bn in the nine chip kinds Deepgrid builds (÷19, the biggest cut) → ₹1,000 Cr sellable by FY31 (scenario) → ₹2.88 Cr already sold. Close with: "We would rather you argue with the bottom number than believe the top one."
- **Why the gap persists (the fixed-cost barrier)**: a normal chip costs $2–5 M before one unit sells, mostly non-design spend.
  - How: outsourced physical layout $1–2 M per chip; tool licences $0.5–1 M per year; a full mask set $0.5–1 M. A 10,000-unit/yr avionics power chip with a unique spec and military screening cannot pay that back, so global suppliers offer a catalogue part with the wrong spec or one near discontinuation.
- **Stacked procurement law**: four rules that together remove the import rather than merely disadvantage it.
  - DAP-2020 Buy (Indian-IDDM): Indian-designed products ranked first, before price comparison.
  - Positive Indigenisation Lists (PILs): named items may not be imported after a stated date. The foreign supplier is removed from bidding.
  - SRIJAN: a government portal where defence companies publish imported items they want replaced.
  - Make-II: a successful trial earns a guaranteed order. The buyer risks time; the supplier risks development money.
- **The IDDM caveat (Deepgrid raises it itself)**: IDDM depends on Indian value content, not design location. First wafers come from SkyWater (Wisconsin) and IHP (Germany), so strictly Deepgrid is Buy(Indian), not Buy(Indian-IDDM), until SCL Mohali makes the chips.
  - Consequence 1: Buy(Indian) still beats a straight import, and a PIL removes the import in either category.
  - Consequence 2: SCL Mohali is a business need, kept in the plan although it is the least proven factory.
- **Why now (four simultaneous changes)**: free PDKs became real (sky130 in 2020, IHP in 2023) and open tools now produce files real factories accept; RISC-V became good enough to ship without licence or royalty; PIL deadlines fall in 2025–2028; the national smart-meter programme peaks this decade.

## Key Concepts
- **Mature-node chips**: chips on 130 nm and larger processes: power management, small MCUs, motor gate drivers, transceivers, supervisors, meter front ends. Most chips in any product.
- **HS 8542**: the customs code behind the $23.4 bn import figure, the only externally sourced number in the section.
- **PIL**: Positive Indigenisation List; an import ban on named items after a date.
- **SRIJAN**: portal of imported defence items wanted for indigenisation (37,696 items quoted here; §11.3 says "over 33,000").
- **Make-II**: trial-to-guaranteed-order procurement route.
- **Buy(Indian-IDDM)**: the top DAP-2020 category, dependent on Indian value content.
- **Switching cost after AVL**: once Deepgrid is on an approved-vendor list, moving away is expensive for the customer.

## Mental Models
- Think of the gap as **arithmetic, not capability**: "Not because it is hard. Because the sums do not work."
- Use **"required, not preferred"** to explain why the market is unusual: in a normal market a cheap entrant meets a price cut; after a PIL date the foreign part cannot be chosen at any price.
- Use **"all four had to change"** when asked why this was not done five years ago.

## Anti-patterns
- **Leading with $23.4 bn or $9 bn**: invites disbelief; the credible number is the bottom of the funnel.
- **Claiming IDDM priority before SCL production**: overstates the legal advantage by one category.
- **Treating the gap as a talent problem**: misdiagnoses the barrier and suggests the wrong fix.

## Reference Tables

| Funnel step | Value | Cut |
|---|---|---|
| All chip imports (UN COMTRADE HS 8542) | $23.4 bn | external source |
| Made on ≥130 nm | $9 bn | ÷2.6 (analyst estimate) |
| The nine chip kinds Deepgrid builds | $0.46 bn | ÷19 |
| Sellable by FY31 | ₹1,000 Cr | scenario |
| Sold today | ₹2.88 Cr | DONE |

Note: the source calls the last step "a factor of 35"; ₹1,000 Cr ÷ ₹2.88 Cr ≈ 347. Correct it before reuse.

## Worked Example
**Answering "why hasn't anyone in India done this?" in the whitepaper's own logic:**
1. Name the cost: $2–5 M per chip, of which layout, licences and masks are invoices, not design work.
2. Name the demand shape: an avionics PMIC at ~10,000 units/yr with a unique spec and MIL screening.
3. Show the sums fail: the setup cost cannot be recovered at that volume, so global firms sell the wrong or ageing part.
4. Name what changed: PILs now ban the import after a date; free PDKs and open tools remove three of the invoices; RISC-V removes the processor licence.
5. State the caveat before being asked: foreign wafers mean Buy(Indian) until SCL Mohali, which is why SCL stays in the plan.

## Key Takeaways
1. The barrier is fixed cost; remove the fixed cost and small defence programmes become products.
2. The law turns a price competition into an eligibility rule after each PIL date.
3. Size markets bottom-up from signed orders; present the top-line import bill only as context.
4. State the Buy(Indian) versus IDDM caveat proactively; it strengthens trust and justifies SCL.
5. Timing is justified by four concurrent changes, none sufficient alone.

## Connects To
- **ch02**: the cost model that removes the barrier.
- **ch07**: SCL Mohali as the third factory.
- **ch12**: how PIL and SRIJAN entries actually convert (lists name boxes, not chips).
- **ch13**: why a large competitor cannot answer with a price cut.
