# Process

Status: draft

## Lead states

```text
new -> researched -> contacted -> replied -> booked -> proposed -> won | lost | dead
```

One record per lead, one state, one store. Two people disagreeing about a lead's state means
the store is broken.

## One intake path

Every lead enters the same way regardless of source — referral, inbound, event, cold, GeM
tender alert. Same record shape, same first step. Multiple intake paths is the most common
reason these systems collapse.

## Stages

| # | Stage | Owner | Duration | Exit criterion |
|---|---|---|---|---|
| 1 | Source | Commercial lead | — | Named organisation, named segment from `02-icp.md` |
| 2 | Qualify | Commercial lead | 1 day | Passes ICP check; disqualifiers explicitly cleared |
| 3 | Research | Commercial lead | 2 days | Buying trigger identified, or "none found" recorded |
| 4 | First contact | Commercial lead | — | Response or 3-touch sequence exhausted |
| 5 | Discovery call | Commercial lead | 45 min | Requirement, timeline and decision unit captured |
| 6 | Technical review | CTO | 1–2 weeks | Their evaluator has seen the demo and the proof kit |
| 7 | Proposal | Commercial + founder | 3 days | Priced by function; founder approved |
| 8 | Close | Founder | — | Signed, with data-rights clause |
| 9 | Deploy | Engineering | 15–35 min/vehicle | Installed, baseline measurement started |

## Human approval required — not negotiable

Anything sent to a client · any price · any contract · any claim not in `04-proof.md` ·
any lead scoring above 9.

## Lead score — the model the approval rule refers to

Score out of 10. **Corrected:** the first version summed to 12 on a stated scale of 10, and
gave +2 for "owns its own vehicles (no homologation gate in the way)" — which is false for a
bus or truck fleet that owns its vehicles and runs them on public roads. Ownership is not
regulatory exposure. Fixed below.

| Signal | Points |
|---|---|
| Government / PSU / defence buyer (eligibility, not certification, is the gate) | +4 |
| Fleet of 50+ vehicles under one decision-maker | +2 |
| **Operates on private land only** — no homologation gate applies to the vehicle | +2 |
| A named buying trigger — tender, incident, safety programme, throughput target | +1 |
| Budget cycle identified | +1 |
| **Any disqualifier from 02-icp.md fires** | **score = 0, stop** |

Maximum 10. A public-road PSU fleet scores 8 — high, and correctly below a private-land
government buyer, because the road fleet still needs certification we do not hold.

9+ means it is large or unusual enough that a human confirms before anything is sent.
A score is not a forecast — AD3/AD4 interest never becomes pipeline regardless of score.

## Known gaps in the current process

- **No defence programme or SI partner is named.** Track A has a proposition and no
  pipeline; a real UGV cycle runs QR → RFI → RFP → seasonal field trials → CNC, which is
  multi-year.
- **No CRM or shared store exists.** Stage 1 has nowhere to write to. This blocks Level 6
  and above.
- **Channel is unaffordable pre-tapeout.** A 20% dealer cut collapses FPGA-phase gross
  margin from 45% to 25%. Sell direct through 2026–27.
- **Insurer role is contradictory across documents** — BP-1A makes it a primary engine, the
  July deck excludes insurer selling. Founder decision required.
