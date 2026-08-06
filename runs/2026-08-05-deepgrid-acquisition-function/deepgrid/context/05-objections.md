# Objections

Status: draft — responses drafted from verified evidence; **replace with real
call-sourced wording after the first 10 conversations.**

Every response concedes the true part first. A seller who concedes an accurate criticism is
believed on the next sentence; one who deflects is not.

## 1. "A ₹30,000 box passes the same inspection."
Correct today, while enforcement is transitional. It cannot do certified AEBS — radar, brake
actuation, proving-ground homologation — or driver monitoring. Move to capability. **Never
argue price here; you lose on their terms.**

> **If the product is AD0, the "move to capability" answer above does not work** — AD0 has no
> AEBS. Use the AD0 Tower content instead: 4D 77GHz radar (works in dust, fog and night; no
> camera box has it) and driver monitoring. Ask them what happens at night in dust, and
> whether their box watches the driver. See 01-offer.md, "AD0 Tower vs a ₹35,000 camera box".

## 2. "Are you actually AIS certified?"
No. Certification is a path via NATRAX, not held. Say it plainly and give the timeline **— BLOCKED: no NATRAX timeline exists in any source. Do not improvise a date. Say certification is **"a path via NATRAX, not held"** — never "in progress", which claims a stronger evidence state than 01-offer.md allows — and offer to come back with the schedule.**
**Never say "mandate-ready".** An evaluator can check and will.


> **Searched:** `sources/*.txt` for "NATRAX" — 2026-08-05. One occurrence, in
> `June-2026-IM-SUPERSEDED.txt` only, carrying no date. Every superseding document dropped
> it. No certification timeline exists anywhere. Blocker confirmed real — do not improvise
> a date.

## 3. "The mandate is 2027 — why am I talking to you now?"
Because AEBS binds new models 1 Jan 2027 and homologation cycles run longer than that. If
you want influence over what gets certified for your fleet, that decision is being made now.
Design partner, not vendor.

## 4. "Why not Mobileye? Mahindra chose them."
True, and for passenger-vehicle line-fit they have the relationships. That was an SUV
programme, not N2/N3 trucks. Our ground is indigenous supply, sovereign data, and price —
strongest where foreign silicon is excluded by procurement rule.

## 5. "What premium reduction will my insurer give?"
We do not have an actuarial partner or a measured baseline, so we will not quote a number.
What we will do is instrument the fleet, measure the delta, and bring your insurer the data.

## 6. "What if you don't tape out?"
The FPGA build runs today and can be demonstrated — it is a working module, not a shipping
product line. Defence and private-land work does not depend on the tapeout; the ASIC changes
cost, not capability. **Do not claim yard revenue — there is none.**

## 7. "What's your power draw?"
Not yet published. Honest answer, and flag it internally — this is the most common gap.

## 8. "You're a startup. What happens if you disappear?"
Fair. Point to the GeM record, the delivered contract, and escrow terms. Do not oversell
runway.

## 9. "Netrasemi are also Indian and better funded."
True — ₹107 Cr and production-ready declared May 2026. Their A2000 is a 12 TOPS edge-AI SoC
on 12nm for video analytics, with no AEC-Q100 and no ISO 26262 claim.
In a sovereign-data conversation it is not a substitute.

> ⚠ **Do not attack them on certification.** We hold no AIS certification either, and our
> ISO 26262 pre-audit is on the stop-doing list. That knock fires backwards the moment the
> evaluator asks us the same question. Compete on sovereign data rights and the truck-specific
> architecture, not on a credential neither party holds.

## 10. "Show me a fleet running this today."
We cannot, at fleet scale. We can show a delivered defence contract, a GeM record, and
silicon running at measured 40 fps. That is the honest position — say it rather than
stretching a pilot into a deployment.


---

## GAP REGISTER — the driverless/AGV objection set does not exist

All ten objections above are road-fleet or defence objections. The port and yard segment has
**zero objection coverage**, and it is the segment the plan leans on for AD4.

These objections are not written here because this file may only contain responses taken from
real conversations. **Inventing them would make this file lie.** They must be gathered from
the first two design-partner conversations and written up verbatim.

What the cold gate test proved a port buyer asks immediately, and we cannot yet answer:

| # | The objection | Why we have no answer |
|---|---|---|
| A1 | "What stops it killing someone?" | No functional-safety line item is funded. ISO 26262 pre-audit is on the stop-doing list. ASIL-D is banned as a present-tense claim. **This is the single biggest gap in the port proposition.** |
| A2 | "How does it localise under the quay cranes?" | GPS is unreliable between container stacks. No file addresses localisation. |
| A3 | "Does it talk to our terminal operating system?" | No TOS or crane-scheduling integration described anywhere. |
| A4 | "What happens around straddle carriers, reach stackers and people on foot?" | No mixed-traffic behaviour defined. A yard tractor is not a truck with the driver removed. |
| A5 | "Salt air, dust, 24/7 duty cycle — what's the environmental rating?" | Not specified. Power and thermal envelope also unpublished. |
| A6 | "What do the unions say?" | No labour/displacement position exists. |
| A7 | "Who insures a driverless vehicle in my yard?" | Unresolved for driven vehicles, let alone driverless. |

Until A1 has an answer, do not pitch AD4 as a product to anyone.
