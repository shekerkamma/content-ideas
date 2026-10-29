# Patterns

## Bottom-up market funnel
**When to use**: stating any market size to a skeptical reader.
**How**: start from the one external figure, cut step by step (process class, product kinds, sellable scenario), end at signed orders; invite argument with the bottom number. Check each step's factor.
**Trade-offs**: the headline looks smaller; credibility rises. A wrong factor (the source's "×35" that is really ×347) undermines the whole funnel. (Ch 1)

## Claim labelling
**When to use**: every figure in a document, deck or pitch.
**How**: tag DONE, DESIGNED, PLANNED or ESTIMATED at the point of use; default volumes, prices and curves to ESTIMATED; pair proofs with what they do not prove.
**Trade-offs**: less rhetorical punch; far fewer diligence surprises. (Ch 3)

## Remove invoices, not effort
**When to use**: explaining a cost advantage against incumbents.
**How**: list the incumbent's per-chip invoices that become staff time for you; show which order sizes flip from unprofitable to profitable; concede high volume.
**Trade-offs**: wins only where volume is low and demand protected. (Ch 2)

## Three-level validation ladder
**When to use**: deciding where to prove a block or chip.
**How**: digital blocks on a shared die ($100–500) → full chip on a shared run (₹14.3 L / ₹34–80 L) → dedicated mask set (₹1 Cr+). Analog and HV blocks start at level 2.
**Trade-offs**: shared dies cannot prove analog, many pins or datasheet limits. (Ch 6)

## Commercial first, simplest-through-qualification first
**When to use**: sequencing a multi-chip portfolio.
**How**: ship mostly-digital commercial chips first for early revenue; send the simplest die through military screening first as a process probe; follow with defence versions on the same approved silicon.
**Trade-offs**: defence margins arrive later; screening risk is learned cheaply. (Ch 8, 9)

## Partition at the ADC
**When to use**: mixed RF/digital parts needing a specialist RF process.
**How**: RF chain on the specialist die (SiGe HBT); ADC onward on mature CMOS; FPGA-validate the digital half; budget a separate RF test chip.
**Trade-offs**: two dies and higher NRE (₹1.4–1.8 Cr); each die on its cheapest adequate process. (Ch 10)

## Deterministic control processor
**When to use**: control, power sequencing and safety silicon.
**How**: omit caches, branch prediction, FPU and compressed instructions; use fixed-point and PMP; move heavy work to dedicated hardware sized by lanes.
**Trade-offs**: lower average speed; guaranteed worst case and identical results across grades. (Ch 7)

## Prove shared safety blocks on cheap silicon first
**When to use**: a block that must ship on an expensive node.
**How**: build and validate it at 130 nm inside mature-node chips before committing a 28 nm mask set.
**Trade-offs**: extra integration work; avoids an unproven block on the costliest mask set. (Ch 11)

## No buyer, no build (with a public scoreboard)
**When to use**: allocating build money across a pipeline.
**How**: spend only when a buyer is named (own product, government list, defence filing, tender, signed letter); publish which chips may spend, which wait on one signature, which are on hold.
**Trade-offs**: slower starts; spend tracks real demand; holds read as discipline. (Ch 12)

## Three buyer clocks
**When to use**: placing revenue in forecast years.
**How**: list entry = permission, 2–4 yr trickle, not counted; defence filing = ~15–18 months to assured order, counted; tender = fast, plus 6–12 months vendor registration.
**Trade-offs**: smaller near-term forecast; no permission counted as orders. (Ch 12)

## Supply the silicon inside the listed box
**When to use**: selling into indigenisation lists that name assemblies.
**How**: map listed LRUs to the chips inside them; open with the box owner's technical team; offer trial silicon, not a box build.
**Trade-offs**: a different first meeting; matches how chip suppliers actually enter defence. (Ch 12)

## Crash case beside the plan
**When to use**: any forecast shown externally.
**How**: re-price each row under a named adverse scenario; mark rows the scenario cannot reach; show the surviving total.
**Trade-offs**: exposes fragile rows (meters, motors); builds trust. (Ch 13)

## Dated stop rules
**When to use**: decisions likely to be bent under enthusiasm.
**How**: write trigger, date and consequence now (S1 meter letter, S2 screening failures, S3 price floor, S4 factory delay); no exceptions later.
**Trade-offs**: removes flexibility deliberately. (Ch 13)

## Self-audit for wishful thinking
**When to use**: before a document goes to investors.
**How**: run a bias checklist (borrowed glory, permission as orders, protecting your number, one skill for another); change the document for each hit; distrust unanimous forces.
**Trade-offs**: time; catches the errors a friendly reader will not. (Ch 13)

## Split the headline number, then check the split
**When to use**: a top-line scenario like FY31 ₹1,000 Cr.
**How**: divide per product; divide each by price to get units and share; cap shares (e.g. 30%) to test the total; rebalance concentration.
**Trade-offs**: may reveal the split does not hold even when the total does. (Ch 14)
