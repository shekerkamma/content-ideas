# COMPANY.md — Founder's Build Stack State Ledger

## Product Idea
A client portal for freelance designers. Clients upload briefs, give feedback on deliverables, and pay invoices. Currently all of this happens over email, Notion links, and Stripe payment links sent manually.

---

## Validation Score
**25/30 → VALIDATED** ✅
- Problem realness: 9/10
- Solution fit: 8/10
- Buying signal: 8/10

---

## ICP Rubric
**93/100** ✅

Solo freelance designer with 5–12 active clients doing $5K–$12K/mo who is drowning in email threads and manual payment chasing.

---

## Scope ✅

**TIER1-KEEP (v1):** Brief intake form, file upload + deliverable feedback, Stripe invoicing + payment, email notifications (Resend), designer dashboard, client magic-link access (no account).

**TIER2-DEFER:** Revision count tracking, project timeline view.

**TIER3-CUT:** In-app client messaging / chat.

---

## Build vs Buy Decisions ✅
- File storage: Supabase Storage (BUILD — free)
- Auth: Supabase Auth (BUILD — free)
- Email: Resend free tier (BUY at $0)
- Payments: Stripe Connect Express (BUY — no alternative)
- Forms: Custom React (BUILD — 4hr)

---

## Feature Sequence ✅
Week 1: Schema + auth + magic-link + brief intake
Week 2: File upload + feedback + designer dashboard
Week 3: Stripe invoicing + email notifications
Week 4: QA + mobile + onboarding + prod deploy

---

## Timeline ✅
30-day plan. Checkpoints: Day 5, 12, 19, 26, 30.

---

## Architecture ✅
**See:** docs/architecture.md

Stack: Next.js 14 App Router · Supabase · Vercel · Stripe Connect Express · Resend

Key decisions:
1. No client accounts — magic token per project
2. Stripe Connect Express — money directly to designer
3. Supabase Storage with signed URLs — private deliverable files
4. Service role key only in API routes
5. Append-only deliverable versioning

---

## MVP Build Progress
- [x] Architecture Designer — docs/architecture.md
- [x] Frontend Builder — BriefForm.tsx + brief/page.tsx
- [x] Backend Builder — /api/briefs/[projectId]/route.ts
- [x] Integration Specialist — /api/webhooks/stripe/route.ts
- [ ] Deployment Manager — pending
- [ ] Post-Launch Iterator — pending (Day 30+)

---

## Deployment Status
[ ] Pending — Day 27-29

---

## Internal Tools
[ ] Post-MVP — run /saas-replacement-auditor after $1K MRR

---

## AI Workflows
### Candidate AI Features (post-launch)
- Auto-generate invoice from brief answers (amount suggestion from scope + deadline)
- Feedback sentiment summary for designer ("client is happy / has concerns about X")

Run /ai-feature-integrator for either when ready.
