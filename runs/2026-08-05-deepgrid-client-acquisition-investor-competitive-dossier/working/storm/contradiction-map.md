# Contradiction map

Five independent lenses + one citation verifier. Contradictions are between DeepGrid's own
documents unless marked EXTERNAL.

| # | Contradiction | Sources in conflict | Lens | Severity |
|---|---|---|---|---|
| C-1 | **Mandate dates.** Strategy built on GSR 184(E) as a live mandate (Apr/Oct 2026). It is a **draft**; the notified rule is G.S.R. 834(E) 11-Nov-2025 → AEBS 1-Jan-2027 new / 1-Oct-2027 all; LDWS+ 1-Oct-2027 new / 1-Jan-2028 existing | vendor blogs vs Gazette | verifier | **CRITICAL — invalidates the demand clock** |
| C-2 | **39.3 TOPS "measured on FPGA"** (July sl.02/04/37) vs Artix-7 XC7A200T ceiling ~1.8 TOPS. June IM correctly calls it a *derivation* | July deck vs BP-1A vs physics | academic | **CRITICAL — provably false as stated** |
| C-3 | **Die area 57.1 mm² (IM) vs ~20 mm² (July sl.31)** — 2.85×. The $3.876 die cost derives from the 20 mm² figure; at 57.1 mm² it is ~$8–10 | IM vs July deck | academic | **HIGH — the corrected cost rests on an uncorrected input** |
| C-4 | **72% kit vs 88.4% blended.** Cannot coexist: 88.4% needs 120% margin on all non-kit revenue. At 72% kit the honest blend is 77.2% | BP-1A §5 vs model vs July sl.18 | skeptic | **HIGH — the approved substitute fails too** |
| C-5 | **₹1 Cr defence revenue.** Actually ₹23.01L delivered + ₹78.39L at L1 (not awarded), in **Deepgrid Datacentre** not Semi, IP MCEME-owned. BP-1A: "none of it is trucking/ADAS revenue" | July deck vs BP-1A §9 | skeptic + practitioner | **HIGH — the headline proof asset** |
| C-6 | **Transformer VLA on-chip** vs bandwidth: ridge point 384 ops/byte, attention ~2. OpenVLA-7B INT8 needs ~68 ms to stream weights alone vs a 33.3 ms budget. And DeepGrid's own shipping model is YOLO-class | IM/July claim vs BP-1B SKU vs BP-1A risk #3 | academic | **HIGH — self-refuting** |
| C-7 | **Memory spec.** IM: LPDDR5 102.4 GB/s. July sl.05: "unified LPDDR4 controller" (~68 GB/s) | IM vs July deck | academic | MEDIUM |
| C-8 | **Insurers as channel.** July sl.13/19 exclude insurers as a sales channel; BP-1A §6 makes insurer co-funding a primary near-term engine | July deck vs BP-1A | practitioner | MEDIUM |
| C-9 | **Break-even.** 174,908 chips (July sl.06) vs net-income-positive FY2029 at ~9,600 cumulative chips — 18× apart, six slides apart. BP-1A's live figure is 400–600 kits/yr | July deck internal | skeptic | MEDIUM |
| C-10 | **OEM posture.** BP-1A §6 "opportunistic OEM engagement from month one" vs July deck's Tier-1-gated posture. EXTERNAL: history (Horizon–Changan, Intellic–ZF) favours the July deck | BP-1A vs July deck | historian | MEDIUM |
| C-11 | **ASIL-D path** claimed while July's stop-doing list bans ISO 26262 pre-audit and AEC-Q100 spend; MPW silicon cannot be AEC-Q100 qualified | IM claim vs July budget | academic | MEDIUM |
| C-12 | **Netrasemi head-start.** July deck: "₹125 Cr, ships mid-2027, a year behind us". Evidence: **₹107 Cr, production-ready May 2026, 3 live OEM trials** — wrong by ~12 months and in the wrong direction | July deck vs verified evidence | economist + verifier | **HIGH** |
| C-13 | **Dealer margin is unaffordable pre-tapeout.** A 20% dealer cut collapses FPGA-phase GM 45%→25%, raising the opex-covering volume from 400–600 kits to ~690–1,030 against an FY27 plan of 130 | BP-1A §5 vs §6 channel model | economist | **HIGH** |
| C-14 | **Insurer subsidy is mis-sized.** Works at ~20–30%, not 50% → ₹40,000–70,000, taking the kit to ₹1.6–1.9L. A margin instrument, **not** a bridge to the ₹30k anchor as BP-1A assumes. Unflagged IRDAI expense-of-management issue | BP-1A §6 assumption | economist | MEDIUM |

## Cross-lens agreement (independent convergence)
- **C-5** found separately by skeptic and practitioner from different starting points.
- **C-1** (verifier) and the historian's AIS-140 finding both point the same way: enforcement in
  India runs years later than notification implies.
- **C-12** found independently by the economist and the citation verifier.
- **C-2 / C-6** (academic) and the skeptic's margin work both show the July deck *regressing* on
  evidence quality while presenting itself as a correction.
