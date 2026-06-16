# Business Proposal
## AI Engineering Team for Dental Practices
**Prepared for:** [Practice Name]
**Prepared by:** [Your Name / Company]
**Date:** June 2026
**Vertical Score:** 26/35 — CONDITIONAL (HIPAA compliance required)

---

## Executive Summary

The average dental practice loses $50,000–$200,000 per year in unscheduled recall
patients and insurance verification delays — revenue that is already earned, already
on the schedule, and already lost before the patient ever sits in the chair. We
propose deploying a HIPAA-compliant AI engineering team that recovers this revenue
automatically, eliminates insurance hold-time from your front desk's day, and reduces
patient no-shows by 60–80% — with a measurable return in the first billing cycle.

**Proposed engagement:** $2,500/month · 2 core workflows live in 14 days

---

## 1. The Business Problem

### What Is Happening Today

**Unscheduled Recall Patients:**
Your practice management software (Dentrix, Eaglesoft, Curve) shows exactly which
patients are 6, 12, or 24 months overdue for hygiene. Your front desk knows this list
exists. They also have 50 other things to do before noon. Manual outreach reaches
15–20% of overdue patients. The other 80% drift. At $200–$300 per hygiene appointment,
a practice with 400 overdue patients is leaving **$64,000–$96,000 per year unrealized**.

**Insurance Verification:**
The industry standard is to verify insurance benefits 24–48 hours before each
appointment. For a practice running 20–30 appointments per day, that is 1–3 staff
hours daily on hold with insurance companies — often for benefits that could be
queried through an electronic portal in 90 seconds. That is **350–500 staff hours
per year** spent on hold music.

**Patient No-Shows:**
Industry average no-show rate: 12–15%. At $250 average production value per
appointment, 2 no-shows per day in a busy practice represents **$120,000–$150,000
per year in empty chair time**. Automated reminders — 72 hours, 24 hours, and
morning-of — reduce no-show rates to 3–5% in practices that implement them consistently.

### The Cost of Inaction

| Problem | Annual Revenue Impact |
|---|---|
| Unscheduled recall patients (400 overdue × 40% recovery × $250/appt) | $40,000 recovered |
| Insurance hold time (400 hrs/yr × $25/hr staff cost) | $10,000 in staff time |
| No-show reduction (12% → 4% × $250/appt × 5 days/wk × 50 wks) | $37,500 recovered |
| **Total addressable improvement** | **$87,500/year** |

---

## 2. The Proposed Solution

We deploy a HIPAA-compliant AI engineering team for your practice — built on your
infrastructure, connected to your practice management system, operating under a
Business Associate Agreement (BAA) that satisfies your compliance requirements.

All patient data stays within HIPAA-compliant infrastructure (your VPS, your
encrypted database). No PHI is transmitted to third-party AI services without
explicit BAA coverage.

### What Gets Built (Initial Engagement)

**Workflow 1 — Patient Recall Automation**
Your AI team pulls the overdue recall list from Dentrix/Eaglesoft nightly. It
sends personalized SMS and email sequences — not blast messages, but sequenced
outreach that mirrors how a skilled front desk coordinator would communicate:
"We noticed it's been a while since your last cleaning, and we have openings next
Tuesday." Includes an online scheduling link. Auto-confirms bookings, sends
48-hour and morning-of reminders, and flags no-shows for immediate rebooking
while the patient's chair time can still be filled.

*Recovers: 15–40 additional hygiene appointments per month = $3,000–$8,000 in production*

**Workflow 2 — Insurance Pre-Authorization + Verification**
Before every appointment, your AI team queries insurance portals through the
Change Healthcare or Availity clearinghouse API, retrieves benefit breakdowns,
calculates patient responsibility, and sends the patient a cost estimate before
they arrive. Your front desk receives a pre-populated verification form — no hold
time, no manual data entry.

*Recovers: 1–3 staff hours per day · Reduces patient billing surprises at checkout*

**Workflow 3 (Month 2 expansion) — New Patient Intake Automation**
Prospective patients complete a structured intake form online. Your AI team
processes the submission, runs an insurance pre-check, creates the patient record
in your PMS, and sends a confirmation with appointment details, intake forms,
and parking instructions — before any staff member touches the file.

*Reduces: new patient administrative time by 70% per patient*

---

## 3. Business Case

### Return on Investment — Month 1

| Revenue/Cost Item | Current | After AI Team |
|---|---|---|
| Recovered recall appointments (20 additional/mo × $250) | $0 | +$5,000/mo |
| No-show reduction (12% → 4% × 2 appts/day × $250) | $0 | +$3,125/mo |
| Insurance hold time eliminated (2 hrs/day × $25 × 22 days) | $1,100/mo cost | $0 |
| **Monthly impact** | **-$1,100 (cost)** | **+$8,125 (value)** |
| **AI Engineering Team fee** | — | **$2,500/mo** |
| **Net monthly improvement** | — | **$6,725/mo** |

**Payback period:** 11 days (recovered recall appointments alone cover the fee)
**Annual net value:** $80,700 (conservative; does not include new patient intake improvement)

### 3-Year ROI Projection

| Year | Revenue Recovered | AI Team Cost | Net Benefit |
|---|---|---|---|
| Year 1 | $97,500 | $30,500 (incl. setup) | $67,000 |
| Year 2 | $97,500 | $30,000 | $67,500 |
| Year 3 | $120,000 (expanded workflows) | $30,000 | $90,000 |
| **Cumulative 3-Year** | **$315,000** | **$90,500** | **$224,500** |

---

## 4. Compliance Architecture

HIPAA compliance is a prerequisite, not an afterthought.

| Requirement | How We Address It |
|---|---|
| Business Associate Agreement | BAA executed before any PHI is processed |
| Data residency | All PHI stored on encrypted VPS in US data center |
| Access controls | Role-based access; patient data accessible only to configured systems |
| Audit trail | Every patient communication logged with timestamp and outcome |
| Breach notification | Automated alert to practice owner within 1 hour of any anomaly |
| Right to erasure | Patient data deletion workflow included on request |

---

## 5. Commercial Terms

| Tier | Monthly Fee | Included |
|---|---|---|
| Starter | $1,500/mo | 1 workflow (recall only) · HIPAA-compliant setup |
| **Growth ★** | **$2,500/mo** | **2 workflows · Full clearinghouse integration · BAA** |
| Scale | $4,500/mo | 3 workflows + new patient intake · Weekly strategy call |

**One-time setup fee:** $750 (includes BAA execution, HIPAA compliance architecture, integration testing)
**Contract:** Month-to-month · 30 days notice · No lock-in

---

## 6. Implementation Timeline

| Week | Milestone |
|---|---|
| Week 1 | BAA executed · PMS API connected · HIPAA infrastructure configured |
| Week 2 | Recall list imported · First outreach sequence tested (5 patients) |
| Week 3 | Insurance verification live for 1 week of appointments · Staff review |
| Week 4 | Full operations · Practice confirms recall booking rate improvement |
| Month 2 | New patient intake portal live · Expanded recall sequences |

---

## 7. Why Act Now

**Every month of delay is a quantifiable number.** With 400 overdue patients,
you are leaving $5,000–$8,000 per month in hygiene production on the table.
That is $60,000–$96,000 per year that is already in your patient database,
already earned, and already being lost to manual outreach that reaches 20% of the list.

**The practice that automates recall first builds the data moat.** A recall
automation system that has been running for 12 months has behavioral data on
which message sequences convert which patient segments. That data trains better
models. The longer you wait, the further behind that learning curve your practice sits.

---

## 8. Next Step

A 30-minute discovery call to review your current recall process, confirm your
PMS and insurance clearinghouse setup, and establish a compliance baseline before
any data is touched.

**Book here:** [Calendly link]
**Contact:** [Name · Email · Phone]
