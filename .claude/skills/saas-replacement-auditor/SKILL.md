---
name: saas-replacement-auditor
description: Use when someone asks to audit their SaaS stack, find tools they can replace or build in-house, reduce SaaS costs, or compare build-vs-buy for specific tools. Runs 5-bucket classification + 3-year cost math + 12-month action plan.
disable-model-invocation: true
argument-hint: [path to tool list file OR paste inline]
---

# SaaS Replacement Auditor

Classify every tool in your stack, find what's worth building, and produce a 12-month action plan with break-even math.

## Input Format

Expect a list in any of these forms (ask the user if missing cost data):

```
Tool Name | Monthly Cost | What It Does | Who Uses It
Intercom  | $299         | Customer chat + support inbox | CS team
Segment   | $120         | Event tracking pipeline | Engineering
```

If `$ARGUMENTS` is a file path, read the file. Otherwise treat `$ARGUMENTS` as inline content.
If no arguments provided, ask the user to paste their tool list.

## Step 1: Classify Every Tool

For each tool, assign exactly one bucket:

| Bucket | Criteria |
|--------|----------|
| **KEEP** | Strategic moat, hard to replicate, deeply integrated, OR cheaper than 3-year build cost |
| **REPLACE** | 3-year build cost < 3-year SaaS cost AND build complexity ≤ medium AND you own the core use case |
| **CONSOLIDATE** | Overlapping functionality with another tool in the stack — pick one, drop the other |
| **NEGOTIATE** | Clearly overpriced for usage, no switching cost reason — push for a better rate first |
| **AUDIT USAGE** | Unclear if actively used, no clear owner, or cost not justified by visible output |

**Hard rule:** Never classify a tool as REPLACE if build complexity is HIGH and strategic value is LOW — commodity tools that are cheap to buy stay KEEP.

Show each classification in a table:

```
| Tool | Monthly | Annual | Bucket | Reason (1 line) |
```

## Step 2: REPLACE Candidates — 3-Year Cost Math

For every tool classified as REPLACE, calculate:

**3-Year SaaS Cost:**
```
Year 1: monthly × 12
Year 2: Year 1 × 1.10
Year 3: Year 2 × 1.10
Total SaaS = Year 1 + Year 2 + Year 3
```

**3-Year Build Cost:**
```
One-time build cost (estimate dev hours × $150/hr)
+ Hosting/infra per year × 3
+ Maintenance (15% of build cost per year × 3)
Total Build = one-time + (hosting × 3) + (maintenance × 3)
```

**Break-even:**
```
Break-even months = Total Build / (Monthly SaaS - Monthly hosting - Monthly maintenance)
```

Show the math explicitly. Never assert without showing numbers.

Sort REPLACE candidates by: **Annual SaaS cost DESC → Build complexity ASC → Strategic value DESC**

## Step 3: Top 3 Replacement Plans

For the top 3 REPLACE candidates (sorted per Step 2), produce:

### [Tool Name] Replacement Plan

**Stack:** [specific tech: e.g., Next.js API routes + Supabase + Resend]
**Build time:** [X weeks with 1 engineer]
**First 30-day milestone:** [what ships in month 1]
**Migration plan:** [data export → shadow mode → cutover → decommission]
**3-year savings:** $[Total SaaS] - $[Total Build] = **$[net savings]**

## Step 4: Annual Spend Summary

```
Current annual SaaS spend:     $[sum of all monthly × 12]
After NEGOTIATE (est -20%):    -$[savings]
After CONSOLIDATE:             -$[savings]
After REPLACE (Top 3, Year 1): -$[Year 1 SaaS saved - build cost]
After REPLACE (Year 3):        -$[net savings by year 3]

Projected Year 3 annual spend: $[amount]
```

## Step 5: 12-Month Action Plan

Output a month-by-month roadmap:

| Month | Action | Tool | Expected Savings |
|-------|--------|------|-----------------|
| 1-2   | AUDIT USAGE — confirm active users, set kill deadline if unused | ... | ... |
| 2-3   | NEGOTIATE — benchmark competitors, push for 15-20% reduction | ... | ... |
| 3-4   | CONSOLIDATE — migrate from duplicate tool, cancel loser | ... | ... |
| 4-8   | BUILD replacement #1 | ... | $X/yr by month 8 |
| 6-10  | BUILD replacement #2 | ... | $X/yr by month 10 |
| 9-12  | BUILD replacement #3 | ... | $X/yr by month 12 |

## Output

Write the full audit to `docs/saas-audit.md` (create `docs/` if it doesn't exist).
Print a short summary to the terminal:
- Number of tools classified per bucket
- Total current annual spend
- Projected 3-year savings if Top 3 replacements ship

## Notes

- If the user's stack has fewer than 3 REPLACE candidates, include the best CONSOLIDATE or NEGOTIATE action in the "Top 3 Actions" instead — never force 3 replacements if math doesn't support it.
- Default dev rate for build cost estimates: $150/hr (senior freelancer). Adjust if user specifies their own rate.
- Default hosting estimate: $20-50/mo for simple CRUD services on Vercel + Supabase free tier.
- This skill assumes Next.js + Supabase + Vercel stack unless the user specifies otherwise.
