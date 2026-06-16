# Top 5 Use Cases — Real Estate Brokerages
**Source:** `runs/2026-06-16-openhands-smb-use-cases/top-25-use-cases.md`
**Filter:** Real estate only · Wave 1 priority

---

## #1 — Transaction Coordinator Bot
**Urgency:** 9/10 · **Wave:** 1 · **Combined Score:** 10/10

**The Pain:** Agents pay $300-$500 per transaction to a human TC who manually tracks
deadlines, chases documents, and emails all parties — and still miss contingency dates.

**The Build:** OpenHands ships a TC automation app: ingests the purchase agreement,
auto-extracts all deadline dates into Notion/Google Calendar, sends daily status emails
to all parties (buyer, seller, title, lender), flags missing documents, and closes the
deal file when all docs are collected.

**MCP Servers:** GitHub · Google Calendar · Gmail · Stripe (invoicing) · Notion · Twilio

**Subagent Type:** document-automation + crm-specialist

**Monthly Value to Client:** $1,500–$4,000 saved (3-8 transactions × $300-$500 TC fee eliminated)

**Buyer Line:** "I'm paying my TC $2,000 a month and half the time I still have to chase people myself."

**ROI Math:** Agent closing 5 transactions/month pays $1,500-$2,500 in TC fees.
Bot at $2,500/mo replaces that entirely and handles unlimited transactions.
Break-even = 5-6 transactions. Above that, pure margin.

**Reference pitch:** `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/01-transaction-coordinator-bot.md`

---

## #2 — Listing Description + MLS Auto-Post System
**Urgency:** 9/10 · **Wave:** 1 · **Combined Score:** 9/10

**The Pain:** Agents spend 45-90 minutes per listing writing property descriptions,
reformatting for MLS character limits, and manually uploading to Zillow, Realtor.com,
and the brokerage site.

**The Build:** Agent inputs address + bullet points + photos → system writes full MLS
description + social captions + email announcement → auto-posts to MLS API, syndicates
to Zillow/Realtor.com, queues social posts in Buffer.

**MCP Servers:** GitHub · Zillow API · Realtor.com API · Buffer · Google Drive (photos)

**Subagent Type:** content-writer + mls-integration-specialist

**Monthly Value to Client:** 8-15 hours/month saved; better listing copy = faster sales

**Buyer Line:** "Writing listing descriptions takes me forever and they all sound the same."

**Reference pitch:** `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/02-listing-description-mls-autopost.md`

---

## #3 — Lead Scoring + CRM Drip System
**Urgency:** 9/10 · **Wave:** 1 · **Combined Score:** 9/10

**The Pain:** Agents have 200-500 contacts with no scoring — so they call everyone
randomly and miss the 5% who are actually ready to transact.

**The Build:** Lead scoring engine on top of existing CRM (Follow Up Boss, KVCore,
or custom): scores leads by engagement (email opens, site visits, inquiry type),
auto-assigns to nurture sequences, surfaces "hot leads" daily via SMS to the agent.

**MCP Servers:** GitHub · Twilio · Mailchimp/ActiveCampaign · Postgres · Zapier

**Subagent Type:** crm-specialist + lead-scoring-agent

**Monthly Value to Client:** 1-3 additional closed transactions/year = $6K-$18K in commission

**Buyer Line:** "I know the deal is in my database somewhere. I just don't know which one to call today."

**Reference pitch:** `runs/2026-06-16-openhands-smb-use-cases/re-triplet-pitch/03-lead-scoring-crm-drip.md`

---

## #4 — CMA Generator
**Urgency:** 8/10 · **Wave:** 1 · **Combined Score:** 9/10

**The Pain:** Agents spend 2-3 hours building a CMA manually — pulling comps,
formatting in PowerPoint, adjusting for differences — before every listing appointment.

**The Build:** Input address + property details → pulls MLS comps via RESO/RETS API,
adjusts for square footage/beds/upgrades, generates a branded PDF presentation with
market trend charts and suggested list price range. Ready before the appointment.

**MCP Servers:** GitHub · MLS API (RETS/RESO) · Google Slides API · Stripe

**Subagent Type:** data-analyst + document-automation

**Monthly Value to Client:** 10-20 hours/month saved; faster listing appointments = more listings won

**Buyer Line:** "I spend half my Sunday doing CMAs. By the time I'm done I don't even want the listing."

---

## #5 — Commission Tracking Dashboard
**Urgency:** 6/10 · **Wave:** 2 · **Combined Score:** 8/10

**The Pain:** Agents track commissions in spreadsheets — no real-time view of which
transactions are pending, what's been paid, what's expected this month, or how close
they are to cap.

**The Build:** Real-time commission dashboard: reads pending transaction data from
their TC system or CRM → calculates gross commission, splits, brokerage fees, taxes →
shows month/year projections → triggers alerts when payments clear or deals fall through.

**MCP Servers:** GitHub · Postgres · Stripe (if collecting fees) · Google Sheets · Slack

**Subagent Type:** data-analyst + crm-specialist

**Monthly Value to Client:** Better cash flow visibility; avoid tax surprises; 3-5 hrs/month

**Buyer Line:** "I genuinely don't know how much money I'm making until I look at my bank account."

---

## Wave 1 Deployment Order

Start with Use Cases #1 and #2 for the first client. They have the cleanest ROI
conversation and the fastest build time (both deliverable in 1-2 weeks with OpenHands).

Add Use Case #3 at Month 2 to deepen stickiness — once your lead scoring is live
inside their CRM, they cannot leave without migrating all their data.

Use Case #4 (CMA) is the upsell conversation at Month 3: "Want to stop spending
Sunday on CMAs?" — same client, +$500-$1,000/mo added to the retainer.
