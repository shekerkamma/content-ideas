# Top 25 Use Cases — OpenHands × SMB "Done-For-You AI Engineering Team"
**Run:** 2026-06-16  
**Method:** last30days signals + vertical-scorer (33→24/35) + ai-use-case-prioritiser (Value × Feasibility)  
**Operator model:** Self-host OpenHands on $20/mo VPS + specialist subagents per niche + MCP integrations  
**Price point:** $2,000–$5,000/month per client

---

## Use Case Prioritiser Matrix

| # | Use Case | Vertical | Value (1-5) | Feasibility (1-5) | Combined | Urgency | Wave |
|---|---|---|---|---|---|---|---|
| 1 | Transaction Coordinator Bot | Real Estate | 5 | 5 | 10 | 9 | Wave 1 |
| 2 | Listing Description + MLS Auto-Post | Real Estate | 4 | 5 | 9 | 9 | Wave 1 |
| 3 | Lead Scoring + CRM Drip System | Real Estate | 5 | 4 | 9 | 9 | Wave 1 |
| 4 | CMA Generator | Real Estate | 5 | 4 | 9 | 8 | Wave 1 |
| 5 | Patient Recall + Appointment System | Dental | 5 | 5 | 10 | 10 | Wave 1 |
| 6 | Insurance Pre-Auth + Verification Bot | Dental | 5 | 4 | 9 | 10 | Wave 1 |
| 7 | Contract Generation + E-Sign | Law | 5 | 5 | 10 | 9 | Wave 1 |
| 8 | Client Intake Portal + Conflict Check | Law | 4 | 5 | 9 | 8 | Wave 1 |
| 9 | Monthly Close + Client Reporting | Accounting | 5 | 4 | 9 | 8 | Wave 1 |
| 10 | Product Description Factory | E-Commerce | 4 | 5 | 9 | 8 | Wave 1 |
| 11 | Abandoned Cart Recovery System | E-Commerce | 5 | 4 | 9 | 9 | Wave 1 |
| 12 | New Patient Intake Automation | Dental | 4 | 5 | 9 | 8 | Wave 1 |
| 13 | Buyer/Seller Matching + Tour Scheduler | Real Estate | 4 | 4 | 8 | 8 | Wave 2 |
| 14 | Review Generation + Reputation Bot | Dental | 4 | 5 | 9 | 7 | Wave 1 |
| 15 | Discovery Document Review + Summary | Law | 5 | 3 | 8 | 8 | Wave 2 |
| 16 | Billing Narrative Automation | Law | 4 | 5 | 9 | 8 | Wave 1 |
| 17 | AP Processing + Vendor Management | Accounting | 4 | 4 | 8 | 7 | Wave 2 |
| 18 | Tax Document Collection + Organizer | Accounting | 5 | 4 | 9 | 9 | Wave 1 |
| 19 | CS Response Automation | E-Commerce | 4 | 5 | 9 | 8 | Wave 1 |
| 20 | Inventory Reorder Trigger System | E-Commerce | 4 | 4 | 8 | 7 | Wave 2 |
| 21 | Commission Tracking Dashboard | Real Estate | 3 | 5 | 8 | 6 | Wave 2 |
| 22 | Client Advisory Digest | Accounting | 4 | 4 | 8 | 7 | Wave 2 |
| 23 | Social Media Content Calendar | Real Estate | 3 | 5 | 8 | 6 | Wave 2 |
| 24 | Med Spa Upsell Automation | Med Spa | 4 | 4 | 8 | 7 | Wave 2 |
| 25 | HVAC Quote Follow-Up System | HVAC | 3 | 5 | 8 | 6 | Wave 2 |

---

## TOP 25 — FULL STRUCTURED USE CASES

---

## #1 — Transaction Coordinator Bot
**Vertical:** Real estate brokerages  
**The Pain:** Agents pay $300-$500 per transaction to a human TC who manually tracks deadlines, chases documents, and emails all parties — and still miss contingency dates.  
**The Build:** OpenHands ships a TC automation app: ingests the purchase agreement, auto-extracts all deadline dates into a Notion/Google Calendar, sends daily status emails to all parties (buyer, seller, title, lender), flags missing documents, and closes the deal file when all docs are collected.  
**MCP Servers Used:** GitHub (codebase), Google Calendar, Gmail, Stripe (invoicing), Notion, Twilio (SMS alerts)  
**Subagent Type:** document-automation, crm-specialist  
**Monthly Value to Client:** $1,500-$4,000 saved per month (3-8 transactions × $300-$500 TC fee eliminated)  
**Buyer Line:** "I'm paying my TC $2,000 a month and half the time I still have to chase people myself."  
**Urgency Score:** 9/10 — TC fees are an obvious line item; ROI conversation is a 30-second math problem.

---

## #2 — Listing Description + MLS Auto-Post System
**Vertical:** Real estate brokerages  
**The Pain:** Agents spend 45-90 minutes per listing writing property descriptions, reformatting for MLS character limits, and manually uploading to Zillow, Realtor.com, and the brokerage site.  
**The Build:** OpenHands builds a listing pipeline: agent inputs address + bullet points + photos → agent writes full MLS description + social captions + email announcement → auto-posts to MLS API, syndicates to Zillow/Realtor.com via API, queues social posts in Buffer.  
**MCP Servers Used:** GitHub, Zillow API, Realtor.com API, Buffer/Hootsuite, Google Drive (photos)  
**Subagent Type:** content-writer, mls-integration-specialist  
**Monthly Value to Client:** 8-15 hours/month saved; better listing copy = faster sales = higher commissions  
**Buyer Line:** "Writing listing descriptions takes me forever and they all sound the same."  
**Urgency Score:** 9/10 — every agent has this exact pain; same build works for all 106K brokerages.

---

## #3 — Lead Scoring + CRM Drip System
**Vertical:** Real estate brokerages  
**The Pain:** Agents have 200-500 contacts in a spreadsheet or basic CRM with no scoring — so they call everyone randomly and miss the 5% who are actually ready to transact.  
**The Build:** OpenHands builds a lead scoring engine on top of their existing CRM (Follow Up Boss, KVCore, or custom): scores leads by engagement (email opens, site visits, inquiry type), auto-assigns to nurture sequences, and surfaces "hot leads" daily via SMS to the agent.  
**MCP Servers Used:** GitHub, Twilio, Mailchimp/ActiveCampaign, Postgres, Zapier (CRM integration)  
**Subagent Type:** crm-specialist, lead-scoring-agent  
**Monthly Value to Client:** 1-3 additional closed transactions per year = $6K-$18K in commission  
**Buyer Line:** "I know the deal is in my database somewhere. I just don't know which one to call today."  
**Urgency Score:** 9/10 — universal pain across all 1.5M active realtors; clear revenue impact.

---

## #4 — Comparative Market Analysis (CMA) Generator
**Vertical:** Real estate brokerages  
**The Pain:** Agents spend 2-3 hours building a CMA manually — pulling comps, formatting in PowerPoint, adjusting for differences — before every listing appointment.  
**The Build:** OpenHands builds a CMA generator: input address + property details → agent pulls MLS comps via API, adjusts for square footage/beds/upgrades, generates a branded PDF presentation with market trend charts and suggested list price range.  
**MCP Servers Used:** GitHub, MLS API (RETS/RESO), Google Slides API, Stripe  
**Subagent Type:** data-analyst, document-automation  
**Monthly Value to Client:** 10-20 hours/month saved; faster listing appointments = more listings won  
**Buyer Line:** "I spend half my Sunday doing CMAs. By the time I'm done I don't even want the listing."  
**Urgency Score:** 8/10 — high frequency pain (every listing appointment); strong willingness to pay.

---

## #5 — Patient Recall + Appointment Reminder System
**Vertical:** Dental practices  
**The Pain:** Dental offices lose $50K-$200K/year in unscheduled recall patients who fell off the hygiene schedule — staff manually calls patients from a list and reaches maybe 20% of them.  
**The Build:** OpenHands builds a HIPAA-compliant recall automation: pulls overdue recall patients from Dentrix/Eaglesoft via API, sends personalized SMS + email sequences with online scheduling link, auto-confirms and sends 48h + day-of reminders, flags no-shows for rebooking.  
**MCP Servers Used:** GitHub, Twilio, Calendly/Acuity, Postgres (HIPAA-compliant), SendGrid  
**Subagent Type:** hipaa-auditor, patient-communication-specialist  
**Monthly Value to Client:** 15-40 additional hygiene appointments/month = $3,000-$8,000 in production  
**Buyer Line:** "I have 400 patients who are 6 months overdue and my front desk doesn't have time to call all of them."  
**Urgency Score:** 10/10 — direct revenue impact, dentist can calculate ROI themselves in 60 seconds.

---

## #6 — Insurance Pre-Authorization + Verification Bot
**Vertical:** Dental practices  
**The Pain:** Front desk staff spend 2-4 hours per day on hold with insurance companies verifying benefits and getting pre-auths — a task that frequently delays treatment and causes patient friction.  
**The Build:** OpenHands builds an insurance automation layer: reads upcoming appointment list from PMS → queries insurance portals (via scraping or clearinghouse APIs) → returns benefit breakdown → auto-populates treatment plan estimates → sends patient a cost breakdown before their appointment.  
**MCP Servers Used:** GitHub, Availity API, Change Healthcare API, Twilio, Postgres  
**Subagent Type:** hipaa-auditor, insurance-verification-specialist  
**Monthly Value to Client:** 8-15 staff hours/month recovered; fewer insurance claim denials = $2,000-$5,000 recovered  
**Buyer Line:** "My front desk spends half their day on hold with insurance. I'm basically paying them to listen to hold music."  
**Urgency Score:** 10/10 — every dental office has this exact problem; existing clearinghouse APIs make the build straightforward.

---

## #7 — Contract Generation + E-Signature Automation
**Vertical:** Law firms (solo + small)  
**The Pain:** Attorneys spend 30-90 minutes per client drafting standard engagement letters, NDAs, and boilerplate contracts from scratch in Word — and then chase clients for wet signatures via email.  
**The Build:** OpenHands builds a contract factory: attorney inputs client details + matter type → agent selects the right template from the firm's library → customizes with client/matter specifics → generates PDF → sends DocuSign/HelloSign link → logs signed version to Clio/case file.  
**MCP Servers Used:** GitHub, DocuSign API, Clio API, Google Drive, Stripe  
**Subagent Type:** document-automation, legal-workflow-specialist  
**Monthly Value to Client:** 10-20 hours/month recovered at $300-$500/hr billable rate = $3,000-$10,000 in recovered time  
**Buyer Line:** "I spend an hour drafting an NDA I've drafted 200 times before. That's an hour I'm not billing."  
**Urgency Score:** 9/10 — universal law firm pain; same build works across practice areas.

---

## #8 — Client Intake Portal + Conflict Check System
**Vertical:** Law firms (solo + small)  
**The Pain:** New client intake is done over phone or email with a legal pad — no structured data collection, no conflict check, and potential clients fall through when the attorney doesn't follow up within 24 hours.  
**The Build:** OpenHands builds a branded intake portal: custom intake form captures matter type, parties, facts → auto-runs conflict check against existing client database → routes to attorney with a summary + recommended next steps → sends automated "received your inquiry" response to prospect.  
**MCP Servers Used:** GitHub, Clio API, Notion, Twilio, Stripe (retainer payment)  
**Subagent Type:** document-automation, client-intake-specialist  
**Monthly Value to Client:** 2-5 additional retained clients/month who would have fallen off; $500-$2,000 retainer each  
**Buyer Line:** "I lose clients because someone called, left a voicemail, and I didn't get back to them for two days."  
**Urgency Score:** 8/10 — lost client pain is visceral; portal is fast to build and easy to demo.

---

## #9 — Monthly Close + Client Reporting Automation
**Vertical:** Small accounting firms / bookkeepers  
**The Pain:** Bookkeepers spend 3-5 days per month per client doing manual reconciliation in QuickBooks, then another 2-3 hours building a client-facing P&L summary in Excel or PowerPoint.  
**The Build:** OpenHands builds a monthly close pipeline: pulls transactions from QuickBooks/Xero API → auto-categorizes → flags anomalies → generates a branded PDF client report with P&L, cash flow statement, key ratios, and a plain-English narrative → delivers via client portal.  
**MCP Servers Used:** GitHub, QuickBooks API, Xero API, Stripe, Google Drive  
**Subagent Type:** financial-analyst, document-automation  
**Monthly Value to Client:** 20-40 hours/month recovered per client → can serve 2x more clients at same staff level  
**Buyer Line:** "Close week is a nightmare. I'm manually pulling the same numbers from QuickBooks every month for every client."  
**Urgency Score:** 8/10 — recurring monthly pain; same build works for all 80K+ small bookkeeping firms.

---

## #10 — Product Description Factory
**Vertical:** E-commerce brands (DTC, Shopify)  
**The Pain:** Store owners manually write product descriptions for every SKU — for a 500-product catalog this is weeks of work, and descriptions go stale when products update.  
**The Build:** OpenHands builds a product description pipeline: ingests product catalog from Shopify API → generates SEO-optimized descriptions at scale (with tone/brand voice config) → bulk-uploads back to Shopify → flags products with thin content for review.  
**MCP Servers Used:** GitHub, Shopify API, OpenAI/Anthropic API (via MCP), Google Search Console API  
**Subagent Type:** content-writer, ecommerce-specialist  
**Monthly Value to Client:** 40-200 hours of copywriting saved; better SEO = organic traffic gains  
**Buyer Line:** "I have 300 products with three-word descriptions because I never had time to write them properly."  
**Urgency Score:** 8/10 — immediately quantifiable; same build serves thousands of Shopify stores.

---

## #11 — Abandoned Cart Recovery System
**Vertical:** E-commerce brands  
**The Pain:** 70% of shopping carts are abandoned — most stores use Klaviyo's basic 3-email sequence, but they're generic and untailored to what the customer was actually looking at.  
**The Build:** OpenHands builds a personalized recovery system: monitors cart abandonment via Shopify webhook → triggers a custom 5-step sequence (email + SMS) personalized to cart contents, customer history, and abandonment timing → A/B tests subject lines → reports recovered revenue weekly.  
**MCP Servers Used:** GitHub, Shopify API, Klaviyo API, Twilio, Stripe  
**Subagent Type:** ecommerce-specialist, email-campaign-agent  
**Monthly Value to Client:** 10-25% cart recovery rate on abandoned revenue → typically $2,000-$10,000/month in recovered sales  
**Buyer Line:** "I know people put things in their cart and leave. I just don't have a system to bring them back."  
**Urgency Score:** 9/10 — directly measurable revenue recovery; client can see ROI in week 1.

---

## #12 — New Patient Intake Automation
**Vertical:** Dental practices  
**The Pain:** New patients fill out paper forms in the waiting room or receive a 10-page PDF attachment that half of them don't complete — causing delays at check-in and incomplete medical histories.  
**The Build:** OpenHands builds a digital intake system: sends HIPAA-compliant online intake form 48h before appointment → patient completes on phone → data flows into Dentrix/Eaglesoft patient record → front desk sees completed intake flag before patient arrives.  
**MCP Servers Used:** GitHub, Twilio, Dentrix API (or Eaglesoft), Postgres (HIPAA-compliant), SendGrid  
**Subagent Type:** hipaa-auditor, patient-communication-specialist  
**Monthly Value to Client:** Front desk saves 5-10 minutes per new patient; better intake data improves case acceptance  
**Buyer Line:** "Patients show up for their appointment and we're still entering their insurance info while they're sitting in the chair."  
**Urgency Score:** 8/10 — patient experience problem that every dental office recognizes immediately.

---

## #13 — Buyer/Seller Matching + Tour Scheduler
**Vertical:** Real estate brokerages  
**The Pain:** Agents with both buyer and seller clients manually cross-reference active listings against buyer criteria — a time-consuming process done in their head or on a spreadsheet.  
**The Build:** OpenHands builds a matching engine: ingests buyer preference profiles from CRM + active listing inventory from MLS → auto-scores every listing against every buyer criteria profile → generates daily "new matches" alert to agent + buyer → auto-schedules showings via Calendly integration.  
**MCP Servers Used:** GitHub, MLS API, Follow Up Boss/KVCore API, Calendly, Twilio  
**Subagent Type:** crm-specialist, matching-algorithm-agent  
**Monthly Value to Client:** Agents close deals faster; buyers stay engaged; fewer lost buyers to competing agents  
**Buyer Line:** "My buyer wants 3/2 under $400K near good schools. I know I have sellers who'd be perfect but I can never remember to cross-reference."  
**Urgency Score:** 8/10 — clear time saver; highly replicable across any brokerage.

---

## #14 — Review Generation + Reputation Management Bot
**Vertical:** Dental practices  
**The Pain:** Dental offices get 3-5 Google reviews per month while competitors get 20-30 — because no one asks at the right moment (post-appointment, while the experience is fresh).  
**The Build:** OpenHands builds a review pipeline: detects completed appointments in PMS → sends a personalized text 2 hours post-visit → includes direct Google review link → monitors for new reviews and alerts the office → routes negative feedback to a private response channel before it becomes public.  
**MCP Servers Used:** GitHub, Twilio, Google Business Profile API, Postgres  
**Subagent Type:** reputation-management-specialist  
**Monthly Value to Client:** 15-30 additional reviews/month → better Google ranking → more new patients ($200-$500 value each)  
**Buyer Line:** "My competitor down the street has 400 reviews and I have 40. I don't know what they're doing differently."  
**Urgency Score:** 7/10 — strong business impact but not daily pain; good upsell to existing clients.

---

## #15 — Discovery Document Review + Summarization
**Vertical:** Law firms (litigation + transactional)  
**The Pain:** Associates spend 40-80 hours reviewing and summarizing document productions in discovery — work that bills at $200-$400/hr but adds no strategic value and could be 10x faster with AI.  
**The Build:** OpenHands builds a document review pipeline: ingests document production (PDFs) → OCR + chunking → categorizes by document type → flags privileged documents → generates per-document summary + issue tag → produces a master review spreadsheet with hot docs highlighted.  
**MCP Servers Used:** GitHub, Google Drive, Postgres, DocuSign (for privilege log)  
**Subagent Type:** document-automation, legal-review-specialist  
**Monthly Value to Client:** $5,000-$20,000 in associate time saved per discovery production; client billing efficiency  
**Buyer Line:** "I'm paying a junior associate $300/hour to read emails we already know are junk. There has to be a better way."  
**Urgency Score:** 8/10 — massive value per engagement; higher complexity build but defensible moat.

---

## #16 — Billing Narrative Automation
**Vertical:** Law firms  
**The Pain:** Attorneys lose 10-20% of billable time to poor time entry — either they forget to enter time, write vague entries ("research"), or reduce bills out of embarrassment at narrative quality, costing thousands per month.  
**The Build:** OpenHands builds a billing narrative system: integrates with Toggl/Harvest or Clio timer → at end of day, drafts complete billing narratives from time entries with context → attorney reviews and approves → syncs to Clio billing system → generates monthly billing reports.  
**MCP Servers Used:** GitHub, Clio API, Toggl API, Stripe  
**Subagent Type:** legal-workflow-specialist, document-automation  
**Monthly Value to Client:** $2,000-$8,000/month in recovered billable time and reduced write-downs  
**Buyer Line:** "I spent 6 hours on a brief this week and billed 4 because I forgot to run my timer. I do that every single week."  
**Urgency Score:** 8/10 — every attorney feels this pain; clear dollar amount they can calculate themselves.

---

## #17 — Accounts Payable Processing + Vendor Management
**Vertical:** Small accounting firms / SMBs  
**The Pain:** AP staff manually enter vendor invoices from email attachments into QuickBooks — a tedious, error-prone process that often results in double payments or missed discounts.  
**The Build:** OpenHands builds an AP automation pipeline: monitors AP email inbox → OCR extracts invoice data → matches to PO if applicable → routes for approval based on dollar threshold → posts to QuickBooks → schedules ACH payment → archives to vendor folder.  
**MCP Servers Used:** GitHub, QuickBooks API, Gmail, Stripe (for payment), Google Drive  
**Subagent Type:** financial-analyst, document-automation  
**Monthly Value to Client:** 5-15 hours/month per AP person saved; fewer errors and duplicate payments  
**Buyer Line:** "My bookkeeper spends two days a week just typing in invoices. That's not what I'm paying her for."  
**Urgency Score:** 7/10 — strong pain; multiple SMB verticals can use the same build.

---

## #18 — Tax Document Collection + Organizer
**Vertical:** Small accounting firms  
**The Pain:** Each January-March, accountants spend 40% of their time chasing clients for W-2s, 1099s, and supporting documents via email — each client follows up 3-5 times and documents arrive in different formats.  
**The Build:** OpenHands builds a tax document portal: sends each client a secure upload link in December → accepts documents in any format → OCR extracts key fields → organizes into a standardized folder structure → alerts accountant when a client's package is complete vs. still missing documents.  
**MCP Servers Used:** GitHub, Google Drive, SendGrid, Twilio, Stripe  
**Subagent Type:** document-automation, financial-analyst  
**Monthly Value to Client:** 20-40 hours/month recovered during tax season; can take on 30% more clients  
**Buyer Line:** "Tax season is just three months of emailing the same clients asking for the same documents they forgot to send last year too."  
**Urgency Score:** 9/10 — seasonal but acute pain; high willingness to pay to make tax season survivable.

---

## #19 — Customer Service Response Automation
**Vertical:** E-commerce brands  
**The Pain:** Shopify stores with 500+ monthly orders receive 50-100 CS emails per day (order status, return requests, product questions) — a founder doing CS themselves loses 3-4 hours daily.  
**The Build:** OpenHands builds a CS automation layer: ingests support emails from Gorgias/Zendesk → classifies request type → generates response from order data + policy docs → routes high-complexity tickets to human → sends approved responses automatically for WISMO/return requests.  
**MCP Servers Used:** GitHub, Shopify API, Gorgias/Zendesk API, Gmail, Stripe (refunds)  
**Subagent Type:** customer-service-specialist, ecommerce-specialist  
**Monthly Value to Client:** 3-4 hours/day recovered; founder can focus on growth; 90% of CS volume automated  
**Buyer Line:** "I'm a one-person store doing $50K a month and I spend every morning answering 'where is my order' emails."  
**Urgency Score:** 8/10 — founder-time problem with clear before/after; same build across all Shopify stores.

---

## #20 — Inventory Reorder Trigger System
**Vertical:** E-commerce brands  
**The Pain:** Store owners stockout on bestsellers because they're monitoring inventory manually in a spreadsheet and reorder 2 weeks too late — losing $5,000-$20,000 in sales per stockout event.  
**The Build:** OpenHands builds an inventory intelligence system: monitors SKU-level stock from Shopify → calculates reorder points based on sales velocity + lead time → generates purchase orders automatically → emails supplier → creates Shopify "low stock" alerts → logs forecast vs. actual.  
**MCP Servers Used:** GitHub, Shopify API, Gmail, Slack, Postgres  
**Subagent Type:** ecommerce-specialist, inventory-management-agent  
**Monthly Value to Client:** Eliminates 2-4 stockout events/year → $10,000-$80,000 in recovered sales  
**Buyer Line:** "I run out of my bestseller every quarter and by the time I reorder it takes three weeks to get here from my supplier."  
**Urgency Score:** 7/10 — seasonal acute pain; strong ROI story but less frequent than CS or descriptions.

---

## #21 — Commission Tracking + Agent Performance Dashboard
**Vertical:** Real estate brokerages  
**The Pain:** Brokerage owners track agent commissions in a spreadsheet — calculating splits, tracking caps, and paying out is a manual process that takes 5-8 hours at month-end and creates disputes.  
**The Build:** OpenHands builds a commission management system: ingests closed transactions from CRM → calculates splits per agent contract → tracks commission caps → generates agent pay statements → exports to QuickBooks for payroll → gives agents a self-service portal to see their YTD production.  
**MCP Servers Used:** GitHub, QuickBooks API, Stripe, Notion, Follow Up Boss API  
**Subagent Type:** financial-analyst, crm-specialist  
**Monthly Value to Client:** 5-8 hours/month recovered for broker; fewer commission disputes; agent satisfaction  
**Buyer Line:** "Every month close I spend a whole day in Excel making sure I'm paying everyone the right split."  
**Urgency Score:** 6/10 — clear operational pain but not revenue-generating; better as an upsell to existing RE clients.

---

## #22 — Client Advisory Digest + Proactive Alert System
**Vertical:** Small accounting firms  
**The Pain:** Accountants only talk to clients during tax season — missing opportunities to flag cash flow issues, tax savings opportunities, or benchmark anomalies throughout the year that would deepen the relationship and justify higher fees.  
**The Build:** OpenHands builds a monthly advisory digest system: analyzes each client's books monthly → identifies anomalies (margin decline, cash burn, payroll spike) → drafts a 1-page advisory memo with specific observations and recommended actions → delivers via client portal or email.  
**MCP Servers Used:** GitHub, QuickBooks API, Xero API, Google Drive, SendGrid  
**Subagent Type:** financial-analyst, document-automation  
**Monthly Value to Client:** Accountant can upgrade clients to advisory engagements at $500-$2,000/month vs. $100/month bookkeeping  
**Buyer Line:** "I only talk to my clients when they call me in a panic. By then the problem has been sitting in the books for three months."  
**Urgency Score:** 7/10 — strategic upsell opportunity; works best for accountants ready to offer advisory services.

---

## #23 — Social Media Content Calendar for Listings
**Vertical:** Real estate brokerages  
**The Pain:** Agents know they should post consistently on Instagram and Facebook — most post 1-2 times per week inconsistently because creating content is time-consuming and they never know what to say.  
**The Build:** OpenHands builds a real estate content system: pulls new listings, price reductions, and closings from MLS API → generates a 30-day content calendar with captions, hashtags, and post formats → exports to Buffer/Hootsuite for auto-scheduling → generates monthly "market update" carousel content.  
**MCP Servers Used:** GitHub, MLS API, Buffer API, Canva API (for graphics), Instagram Graph API  
**Subagent Type:** content-writer, social-media-specialist  
**Monthly Value to Client:** 5-10 hours/month saved; consistent posting builds audience and drives inbound leads  
**Buyer Line:** "I know I need to post but every Sunday night I sit there staring at my phone and can't think of anything."  
**Urgency Score:** 6/10 — strong time saver but marketing ROI is longer-cycle; good bundled add-on.

---

## #24 — Med Spa Retail Upsell Automation
**Vertical:** Med spas / aesthetic clinics  
**The Pain:** Med spa owners know their clients should be buying retail skincare products between treatments but staff forget to recommend, and there's no follow-up system — leaving $500-$2,000/month in retail revenue per location on the table.  
**The Build:** OpenHands builds a retail automation layer: post-treatment, triggers a personalized email/text with recommended products based on treatment received → sends a 7-day follow-up with before/after education → integrates with Vagaro/Mindbody inventory → tracks which campaigns drive retail conversion.  
**MCP Servers Used:** GitHub, Vagaro API/Mindbody API, Twilio, Stripe, SendGrid  
**Subagent Type:** customer-retention-specialist, ecommerce-specialist  
**Monthly Value to Client:** $500-$2,000/month in incremental retail revenue; improved client retention  
**Buyer Line:** "I know my clients need SPF but my injectors forget to mention it and then they go buy it on Amazon."  
**Urgency Score:** 7/10 — clear revenue add; high-growth vertical (med spa market up 14%/year).

---

## #25 — HVAC Quote Follow-Up + Review Automation
**Vertical:** HVAC / plumbing contractors  
**The Pain:** Contractors send 30-50 quotes per month and follow up on maybe 20% of them — the other 80% sit in email and go cold, and they never know which jobs they lost or why.  
**The Build:** OpenHands builds a quote lifecycle system: when a quote is sent from ServiceTitan/Housecall Pro → auto-triggers a follow-up sequence (day 2 email, day 5 text, day 10 call reminder) → marks quote as won/lost → triggers review request 24h after completed jobs → logs win/loss data for pricing analysis.  
**MCP Servers Used:** GitHub, ServiceTitan API, Twilio, Gmail, Google Business Profile API  
**Subagent Type:** crm-specialist, customer-communication-agent  
**Monthly Value to Client:** 10-20% more quotes converted → 2-4 additional jobs/month at $500-$2,000 each  
**Buyer Line:** "I sent out 40 quotes last month and I have no idea what happened to half of them. I probably lost jobs and don't even know it."  
**Urgency Score:** 6/10 — strong pain but lower business scale than top verticals; good for secondary expansion.

---

## AI Use Case Portfolio — Wave Mapping

### Wave 1 — Quick Wins (Ship in 0-4 weeks, show ROI in 30 days)
| # | Use Case | Vertical | Why It's Wave 1 |
|---|---|---|---|
| 1 | Transaction Coordinator Bot | Real Estate | Replaces an existing line item; instant ROI |
| 2 | Listing Description + MLS Auto-Post | Real Estate | Replaces daily manual work; fast demo |
| 3 | Lead Scoring + CRM Drip | Real Estate | Revenue-generating; clear before/after |
| 4 | CMA Generator | Real Estate | Replaces 2-3 hours per listing appt |
| 5 | Patient Recall System | Dental | Directly books appointments = same-day revenue |
| 6 | Insurance Pre-Auth Bot | Dental | Replaces hold-music hours; same-day relief |
| 7 | Contract Generation + E-Sign | Law | Replaces repetitive attorney time; fast build |
| 8 | Client Intake Portal | Law | Lost-client pain; fast to demo |
| 9 | Monthly Close + Reporting | Accounting | Recurring monthly pain; same build all clients |
| 10 | Product Description Factory | E-Commerce | Catalog-wide impact; same day visible results |
| 11 | Abandoned Cart Recovery | E-Commerce | Measurable revenue recovery in week 1 |
| 12 | New Patient Intake | Dental | Removes front desk chaos; fast build |
| 14 | Review Generation Bot | Dental | Google ranking impact; fast build |
| 16 | Billing Narrative | Law | Attorney time recovery; clear dollar value |
| 18 | Tax Doc Collection | Accounting | Acute seasonal pain; high willingness to pay |
| 19 | CS Response Automation | E-Commerce | Founder time recovery; 3-4 hours/day back |

### Wave 2 — Strategic Bets (4-12 weeks, higher complexity, deeper moat)
| # | Use Case | Vertical | Dependency |
|---|---|---|---|
| 13 | Buyer/Seller Matching | Real Estate | MLS API access |
| 15 | Discovery Doc Review | Law | OCR + vector search infrastructure |
| 17 | AP Processing | Accounting | QuickBooks API + OCR pipeline |
| 20 | Inventory Reorder | E-Commerce | Shopify webhook + supplier API |
| 21 | Commission Dashboard | Real Estate | CRM API + QuickBooks |
| 22 | Client Advisory Digest | Accounting | Monthly cadence; advisory positioning |
| 23 | Social Media Calendar | Real Estate | MLS + social APIs + design layer |
| 24 | Med Spa Upsell | Med Spa | Vagaro/Mindbody API access |
| 25 | HVAC Quote Follow-Up | HVAC | ServiceTitan/Housecall Pro API |

---

## Recommended Execution Sequence

```
Month 1:  Launch with Real Estate vertical (#1, #2, #3 as the core triplet)
Month 2:  Add Dental vertical (#5, #6, #12 — HIPAA-ready infrastructure)
Month 3:  Add Law vertical (#7, #8, #16 — document automation layer)
Month 4:  Add E-Commerce (#10, #11, #19 — Shopify integration layer)
Month 5:  Add Accounting (#9, #18 — QuickBooks integration layer)
Month 6+: Wave 2 builds for each vertical (deeper moat, higher LTV)
```

---

*Generated by: last30days + vertical-scorer + ai-use-case-prioritiser + PLAID Idea framework*  
*Based on: OpenHands 77K stars (All-Hands-AI/OpenHands), SMB market signals June 2026*
