# SaaS Replacement Audit

**Stack audited:** Early-stage SaaS startup (15 tools, $2,774/mo)
**Date:** 2026-06-19

## Classification

| Tool | Monthly | Annual | Bucket | Reason |
|------|---------|--------|--------|--------|
| Retool | $600 | $7,200 | REPLACE | Custom Next.js admin panel replaces this; zero recurring cost |
| Airtable | $240 | $2,880 | REPLACE | CRM schema in Supabase covers all use cases |
| Zapier | $199 | $2,388 | REPLACE | n8n self-hosted on $5/mo VPS; 10 zaps = 3-day migration |
| Segment | $120 | $1,440 | REPLACE | Event pipeline is 200 lines of code + Supabase insert |
| Intercom | $299 | $3,588 | NEGOTIATE | Build math doesn't support replacement; push for 20% cut |
| Datadog | $410 | $4,920 | NEGOTIATE | Vercel + Supabase covers 80% of needs; push for SMB tier |
| Mixpanel | $89 | $1,068 | CONSOLIDATE | Overlaps with Segment; drop once event pipeline ships |
| Postman | $49 | $588 | AUDIT USAGE | Free tier likely sufficient; confirm active paid features |
| Loom | $16 | $192 | KEEP | $16/mo, no practical build alternative |
| Notion | $32 | $384 | KEEP | Replacing docs infra is distraction |
| Linear | $48 | $576 | KEEP | Best-in-class, $48/mo, strategic tool |
| Calendly | $24 | $288 | KEEP | $24/mo; Cal.com is valid replace but not worth migration |
| Algolia | $500 | $6,000 | KEEP | Core product feature; Supabase FTS has scale limitations |
| SendGrid | $89 | $1,068 | NEGOTIATE | Resend/SES 5× cheaper at same volume |
| Typeform | $59 | $708 | REPLACE | 50 lines React + Supabase insert; no unique capability |

## 3-Year Cost Math (REPLACE candidates)

### #1 Retool → Custom Next.js Admin Panel
- 3-yr SaaS cost: $23,832 | Build cost: $8,700 | Break-even: 16.6 months
- **Net 3-year savings: $15,132**

### #2 Zapier → n8n Self-Hosted
- 3-yr SaaS cost: $7,904 | Build cost: $1,380 | Break-even: 7.1 months
- **Net 3-year savings: $6,524**

### #3 Airtable → Supabase CRM
- 3-yr SaaS cost: $9,533 | Build cost: $4,350 | Break-even: 21.4 months
- **Net 3-year savings: $5,183**

## Annual Spend Summary

| | Amount |
|--|--------|
| Current annual spend | $33,288 |
| After quick wins (months 1-3) | $29,438 |
| After Top 3 builds (month 10) | ~$16,970 |
| **3-year total savings** | **~$29,500** |

## 12-Month Action Plan

| Month | Action | Tool | Savings |
|-------|--------|------|---------|
| 1 | Downgrade to free tier | Postman | $588/yr |
| 1 | Drop (consolidate into Segment) | Mixpanel | $1,068/yr |
| 2 | Negotiate -20% | Intercom | $718/yr |
| 2 | Negotiate -30% or migrate | Datadog | $1,476/yr |
| 3-4 | Migrate to n8n self-hosted | Zapier | $2,388/yr |
| 4-7 | Build custom admin panel | Retool | $7,200/yr |
| 5-8 | Build Supabase CRM (with admin panel) | Airtable | $2,880/yr |
| 9-12 | Build event pipeline | Segment | $1,440/yr |
