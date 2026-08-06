# Proof

> **Internal-only registry.** These numbers exist and are permitted *internally* but may
> never be said to a buyer: kit gross margin 72% (ASIC phase), 45%→25% (FPGA phase with
> dealer cut), die cost $3.876 at 1M units. Recorded here so the ceiling rule stays true —
> the offer file is not asserting a number this file has never seen.

Status: draft — **requires founder approval before outbound use**

**This file is the ceiling on every claim the system may make.** If a number, name or
outcome is not here, it may not be asserted anywhere — outbound, proposal, deck or call.

## May be claimed

| Claim | Evidence state | Source | Caveat that must travel with it |
|---|---|---|---|
| GeM procurement record held | CONTRACTED | GeM GEMC-511687794620175 | Real, and the strongest Track A asset |
| ₹23.01L (delivered) delivered — Robot Training | CONTRACTED | GeM, BP-1A §9 | **Sits in Deepgrid Datacentre Pvt Ltd, not Deepgrid Semi. IP is MCEME-owned (Clause 27). It is not ADAS revenue** |
| YOLOv11n measured at 40 fps on FPGA | MEASURED | July deck | On Artix-7 class hardware. Say measured, not derived |
| Attention head at 24.25 ms | MEASURED | July deck | The honest perception-latency datapoint |
| DGS001 module running on FPGA | SILICON | Live demo | Artix-7 class. Do not imply ASIC performance |
| 15 provisional patents filed Mar 2026 | FILED | July deck | **Filed, not granted.** Say filed |
| Carla-validated D-Drive loop | SIMULATION | IM | Simulation, not road. Say so |
| TSMC 28nm, 39.3 TOPS INT8 design target | DERIVED | IM p.5 | A **derivation** (MACs × clock), not a measurement |
| Price below imported kits | PLAN | BP-1A §7 | **Say "materially below imported kits" and stop.** Do not quote a multiple: 2.8–6.5× compares list prices, ~2.3× compares loaded cost. Until one comparison is chosen and evidenced, any multiple is the same category error that retired 12.9× |

## Must never be claimed — retired by verification

| Retired claim | Why |
|---|---|
| "39.3 TOPS measured on FPGA" | Artix-7 ceilings ~1.8 TOPS. 22× short. It is a derivation |
| "84% ASIC gross margin" | Retracted by the company's own July Corrections Ledger |
| "88% blended systems margin" | Requires 120% margin on all non-kit revenue. Arithmetically impossible |
| "12.9× cheaper than Mobileye" | Compares their ASP to our die cost. Loaded, it is ~2.3× |
| "₹1 Cr defence revenue" | ₹23.01L delivered; ₹78.39L is L1 — lowest bidder, not an award |
| "Transformer VLA runs on-chip" | Bandwidth-bound: ~68 ms to stream weights vs a 33.3 ms budget |
| "Mandate live since April 2026" | GSR 184(E) was a draft. Real rule G.S.R. 834(E), Nov 2025 |
| "ASIL-D path" | No functional-safety line item; ISO 26262 pre-audit is on the stop-doing list |
| Any insurance-premium or accident-reduction % | No actuarial partner, no measured baseline |

## Known gaps a buyer will probe

- **Power and thermal envelope appears in no document.** First question any serious
  integrator asks about an M.2 module in a truck cabin. Answer: not yet published.
- **AIS-162/188 certification is not held.** A path via NATRAX. Never imply otherwise.
- **Die area is stated as both 57.1 mm² and ~20 mm²** across documents. Unreconciled.


---

## CORRECTION — the defence figure was over-retired

An earlier pass retired "₹1 Cr defence revenue" and instructed the system to say ₹23.01L
instead. That over-corrected. BP-1A shows **two** GeM records, not one:

| Record | Value | State |
|---|---|---|
| GeM GEMC-511687794620175 · Robot Training | ₹23.01L | Delivered, CONTRACTED |
| GeM RA GEM/2026/R/672471 · Robotics Assistant | ₹78.39L | L1, under execution, CONTRACTED |
| **Total defence engagement** | **₹1.01 Cr** | Contracted |

**What may now be said:** "₹1.01 Cr contracted across two GeM records, one delivered and one
under execution." **What still may not:** calling it *revenue*, calling it *ADAS*, or
attributing it to Deepgrid Semi — it sits in **Deepgrid Datacentre Pvt Ltd**, and the Robot
Training IP is MCEME-owned.

The original claim was wrong about the *kind* of number, not the magnitude. Retiring the
magnitude threw away the strongest verifiable asset in this file.

## OPEN — blocks the government/PSU segment

**Does Deepgrid Semi Pvt Ltd hold its own GeM seller registration?** `02-icp.md` uses "GeM
access already demonstrated" to qualify the target-now segment, but both records sit in
Deepgrid Datacentre. If Semi is not registered, the segment's core qualifier does not apply
to the entity that would supply. Nothing in any source answers this. **Ask before the next
PSU approach.**
