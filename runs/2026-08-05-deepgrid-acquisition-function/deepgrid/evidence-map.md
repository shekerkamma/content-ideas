# Evidence map

Every rule in `context/` traces to a source here. Where two sources conflict, the
verification column records which survived and why.

| ID | Claim or rule | Lands in | Source | Verdict |
|---|---|---|---|---|
| E-01 | Price by function: AEBS + DMS carry, warnings ride free | 01-offer | STORM economist lens | Analyst recommendation, not company doctrine |
| E-02 | Kit gross margin 72% at ASIC phase | 01-offer | BP-1A §5 | SURVIVES — company-corrected |
| E-03 | 88% blended margin | — retired | July deck sl.18 | FAILS — needs 120% on non-kit revenue |
| E-04 | 84% ASIC gross margin | — retired | June IM | FAILS — retracted by company's own ledger |
| E-05 | Segments and disqualifiers | 02-icp | July deck sl.08–14; BP-1A §3 | SURVIVES |
| E-06 | Sub-5-truck operators not addressable (~3.5M) | 02-icp | BP-1A §3 | SURVIVES — SOURCED |
| E-07 | AEBS binds 1 Jan 2027 new / 1 Oct 2027 all | 02-icp | G.S.R. 834(E), gazette | SURVIVES — replaces "April 2026" |
| E-08 | "Mandate live since April 2026" | — retired | June IM; BP-1A §2 | FAILS — GSR 184(E) was a draft |
| E-09 | GeM record held | 04-proof | GeM GEMC-511687794620175 | SURVIVES — CONTRACTED |
| E-10 | ₹23.01L delivered, Robot Training | 04-proof | BP-1A §9 line 278 | SURVIVES — with entity and IP caveat |
| E-11 | "₹1 Cr defence revenue" | — retired | June IM; July deck | FAILS — ₹78.39L is L1, not awarded |
| E-12 | YOLOv11n 40 fps; attention head 24.25 ms | 04-proof | July deck | SURVIVES — MEASURED |
| E-13 | "39.3 TOPS measured on FPGA" | — retired | July deck sl.02/04/37 | FAILS — Artix-7 ceilings ~1.8 TOPS |
| E-14 | 39.3 TOPS as a design derivation | 04-proof | June IM p.5 | SURVIVES — as derivation only |
| E-15 | Transformer VLA on-chip | — retired | June IM | FAILS — bandwidth-bound (~68 ms vs 33.3 ms) |
| E-16 | Ten objections and responses | 05-objections | Drafted from E-01…E-15 | **WEAK — not from real calls; replace after 10** |
| E-17 | Banned-words list | 03-voice | July deck sl.18 + retired claims | SURVIVES |
| E-18 | Voice samples | 03-voice | — none exist | **MISSING — blocks the file** |
| E-19 | Lead states and stages | 06-process | Framework L10; BP-1A §6 | SURVIVES |
| E-20 | Channel unaffordable pre-tapeout | 06-process | STORM economist lens | Analyst finding |
| E-21 | Ten-level ladder and gates | control/ | Claude For Client Acquisition (22pp) | Framework |

## Conflicts resolved
Four company documents disagreed on margin, defence revenue, mandate date, compute
performance and price advantage. In every case the later-and-verified figure was taken and
the earlier one written into `03-voice.md` as a banned claim rather than silently dropped.
