# Business Proposal
## AI Engineering Team for Medical Spas
**Prepared for:** [Med Spa Name]
**Prepared by:** [Your Name / Company]
**Date:** June 2026
**Vertical Score:** 26/35 — CONDITIONAL

---

## Executive Summary

The average medical spa loses $15,000–$40,000 per year in unfilled appointment slots,
incomplete follow-up sequences after treatments, and unrealized membership upsells —
revenue that sits in the patient database but never gets activated because the front desk
is managing check-ins, phones, and paperwork simultaneously. We propose deploying an AI
operations team that fills your cancellations automatically, runs post-treatment follow-up
sequences that generate rebookings on autopilot, and identifies your highest-LTV patients
for membership conversion — all while your front desk focuses on in-person hospitality.

**Proposed engagement:** $2,500/month · 2 core workflows live in 14 days

---

## 1. The Business Problem

### What Is Happening Today

**Unfilled Cancellations:**
Medical spas operate on appointment-based revenue with high fixed overhead (equipment,
licensed staff, facility). A cancellation at 2pm for a 3pm Botox appointment is not
just lost revenue — it is overhead that still runs with zero return. The industry average
cancellation rate is 10–15%. For a spa doing 40 appointments per day at $250 average
treatment value, that is **$250,000–$375,000 per year in cancellation-gap revenue**,
most of which goes unfilled because calling the waitlist manually takes time the front
desk does not have at 2pm.

**Post-Treatment Follow-Up:**
Every Botox patient should receive a 2-week check-in. Every filler patient should
receive a 4-week photo review prompt. Every skin treatment patient should receive a
product recommendation 72 hours post-treatment. These sequences exist in every spa's
protocol binder and almost nowhere in practice — because remembering which patient
had which treatment 2 weeks ago is a coordination problem that always loses to the
immediate demands of the front desk.

**Membership Upsell Identification:**
Most med spas have membership programs that patients never hear about at the right moment.
The right moment is after a patient's third visit, when their spend pattern shows they
would save money on a membership. Finding those patients manually — cross-referencing
visit frequency with spend history — never happens at scale. **The typical spa converts
fewer than 5% of eligible patients to memberships**, leaving a recurring revenue base
that could represent $50,000–$150,000/year in ARR on the table.

---

## 2. The Proposed Solution

We deploy an AI operations team connected to your practice management system (Jane App,
Mindbody, Zenoti, or Aesthetic Record), your SMS/email platform, and your patient records.
All communications are in your spa's brand voice. All patient data stays in your systems.

**HIPAA Note:** This proposal is scoped to scheduling, follow-up, and membership data
only — administrative use of protected health information. We operate under a Business
Associate Agreement and process no PHI outside your HIPAA-compliant infrastructure.

### What Gets Built (Initial Engagement)

**Workflow 1 — Cancellation Fill Automation**
When a cancellation occurs, your AI team immediately contacts your waitlist — in priority
order, based on treatment type, last visit, and expressed interest — via SMS: "A slot
just opened for [Treatment] this afternoon at [Time]. Reply YES to confirm." First
confirmation takes the slot, automated confirmation sent, schedule updated. If no
waitlist match exists, the slot is marked open and your front desk receives a heads-up.

*Fills: 40–60% of same-day cancellation slots that would otherwise go empty*
*Recovers: $2,500–$5,000/month on 10 cancelled appointments/month at $250 avg*

**Workflow 2 — Post-Treatment Follow-Up Sequences**
After every appointment, your AI team triggers a treatment-specific follow-up:
Botox → 2-week check-in SMS + rebooking prompt. Filler → 4-week photo review request.
HydraFacial → 72-hour skincare recommendation + product link. Each message is
pre-approved by your clinical director. The system tracks responses and flags patients
who don't rebook within the expected window for a personal front-desk call.

*Increases: rebooking rate by 15–25% vs no follow-up*
*Generates: $3,000–$6,000/month in incremental rebookings at 40 appointments/day volume*

**Workflow 3 (Month 2 expansion) — Membership Conversion Engine**
Your AI team identifies patients with 3+ visits in the last 90 days whose total spend
exceeds membership breakeven, and triggers a personalized membership offer:
"Based on your visits, you would have saved $[X] this quarter on a [Membership Name]
membership." The message is sent at the right moment — day 3 after their most recent
visit — not during checkout. Membership conversion handled in-spa by your front desk.

*Converts: 2–5% more eligible patients to memberships*
*Generates: $200–$500/month per converted member in recurring revenue*

---

## 3. Business Case

### Return on Investment — Month 1

| Revenue/Cost Item | Current | After AI Team |
|---|---|---|
| Cancellation fills (60% × 10 cancellations/mo × $250) | $0 | +$1,500/mo |
| Post-treatment rebooking increase (20% more × 40 appts/mo × $250) | $0 | +$2,000/mo |
| Front desk time saved on follow-up (5 hrs/wk × $18/hr) | $360/mo cost | $0 |
| **Monthly value** | **-$360 (cost)** | **+$3,500 (revenue)** |
| **AI Engineering Team fee** | — | **$2,500/mo** |
| **Net monthly improvement** | — | **$3,140/mo** |

**Payback period:** 21 days (cancellation fills + rebooking improvement)
**Annual net value:** $37,680 (before membership ARR compounds)

**Membership upsell (Month 2+):** 10 new memberships/month at $200/mo average =
**$2,000/month in additional recurring revenue** by Month 3.

---

## 4. Compliance Architecture

| Requirement | How We Address It |
|---|---|
| Business Associate Agreement | BAA executed before any patient data is processed |
| PHI scope | Only scheduling, visit history, and membership eligibility — no clinical notes or diagnoses |
| Communication consent | Only contacts patients who have opted in to SMS/email marketing under your existing consent |
| Data residency | All patient data in your existing practice management system; no PHI copied externally |
| Opt-out | Instant opt-out from any automated sequence via keyword reply; front desk notified |

---

## 5. Commercial Terms

| Tier | Monthly Fee | Included |
|---|---|---|
| Starter | $1,500/mo | Cancellation fill automation only · Jane App / Mindbody integration |
| **Growth ★** | **$2,500/mo** | **Cancellation fills + Post-treatment follow-up · BAA + HIPAA setup** |
| Scale | $4,500/mo | All 3 workflows + Membership engine · Weekly call |

**One-time setup fee:** $750 (BAA execution, PMS API integration, follow-up sequence approval with clinical director)
**Contract:** Month-to-month · 30 days notice · No lock-in

---

## 6. Implementation Timeline

| Week | Milestone |
|---|---|
| Week 1 | BAA signed · Jane App / Mindbody API connected · Waitlist data imported |
| Week 2 | Cancellation fill automation live (first 3 test fills) · Front desk reviews |
| Week 3 | Post-treatment sequences live for 3 treatment types · Clinical director approves messaging |
| Week 4 | Full operations · First month cancellation recovery tracked |
| Month 2 | Membership engine live · First eligible patient batch identified |

---

## 7. Why Act Now

**Your cancellation revenue is perishable.** An unfilled 3pm slot today is gone at
3:01pm. Every week without an automated waitlist system is a week of permanent
revenue loss. A spa that installs this system in June recovers June through December
within the same year.

**Your rebooking window is short.** The highest rebooking probability is within 7 days
of a treatment. A patient who does not hear from you in that window loses momentum.
The spa that follows up wins the next appointment; the spa that doesn't loses it to
the one that does.

---

## 8. Next Step

A 30-minute call to review your cancellation rate, confirm your practice management
platform, and walk through your current follow-up process for your two highest-volume
treatments.

**Book here:** [Calendly link]
**Contact:** [Name · Email · Phone]
