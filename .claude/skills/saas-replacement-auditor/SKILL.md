---
name: saas-replacement-auditor
description: Use when someone asks to audit their SaaS stack, find tools they can replace or build in-house, reduce SaaS costs, or compare build-vs-buy for specific tools. Runs 5-bucket classification + 3-year cost math + 12-month action plan.
disable-model-invocation: true
argument-hint: [path to tool list file OR paste inline]
---

# SaaS Replacement Auditor

Classify every tool in your stack, find what's worth building, and produce a 12-month action plan with break-even math.

## Narrative Frame

**This skill's job:** Make the founder angry about how much they're paying for things they could own — then give them a precise exit plan.

**Voice:** You are a CFO who has seen this stack before. You are not neutral. You have opinions. You surface the number that stings, then show the exit.

**Opening move — cost-of-inaction first:**
> "You're spending $X/yr on tools. $Y of that is replaceable. Here's what you're leaving on the table every month you don't act."

**Per-section voice rules:**
- **Classification table:** One-line reason must be a verdict, not a description. Not "overlapping functionality" → "You're paying twice for event tracking. Pick one and cancel the other this week."
- **Cost math:** Show every line. Label the break-even month in bold. Add: "After month [N], you own this forever."
- **Top 3 replacement plans:** Lead each with the net 3-year savings in the title. Not "Retool Replacement Plan" → "$15,132 back: Replace Retool with a Next.js admin panel."
- **12-month action plan:** Month 1 actions must require zero code — negotiation and cancellation first. Frame each as: "This call / this email / this click saves you $X."

**Anti-patterns to kill in this skill's output:**
- "It may be worth considering replacing..." → "Replace it. Break-even is month 17."
- "There are potential savings available..." → "$6,524 over 3 years, starting month 8."
- "The tool appears to be underutilized..." → "Nobody can name the last time they used this. Cancel it."

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

---

## Skill Relationships

### Category
Business Automation

### Dependencies
None required. Standalone — can run from an inline tool list.
- `founders-build-stack` — optional upstream: COMPANY.md produced by the Build Stack contains the SaaS tool decisions from Tier 3

### Relationships

| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `founders-build-stack` | Sequential upstream (optional) | when auditing the stack of a product built in the Build Stack | `COMPANY.md` (project root) or `docs/saas-audit.md` trigger from Tier 3 |
| `plaid` | Sequential downstream | REPLACE candidates become build targets in the PLAID product-led roadmap | `docs/saas-audit.md` |

### Runtime Preamble

At invocation, surface this if relevant:

> "Do you have a COMPANY.md from a Founders Build Stack run? If yes, the Build vs Buy decisions from Tier 3 will seed the REPLACE candidate list.
> After the audit, REPLACE candidates can feed into `/plaid` as build targets in the product roadmap."

---

## Gotchas

- **Never force 3 REPLACE candidates:** If fewer than 3 tools pass the build cost math, use the best CONSOLIDATE or NEGOTIATE action as the third slot. Forcing REPLACE on a tool that doesn't break even in 36 months destroys the audit's credibility.
- **REPLACE requires medium-or-lower build complexity:** Hard rule — never classify a tool as REPLACE if build complexity is HIGH and strategic value is LOW. Cheap commodity tools (e.g., a $9/mo analytics tool) stay KEEP even if they seem redundant.
- **Missing cost data blocks the audit:** If the user provides tool names without monthly costs, ask for costs before classifying. Bucketing tools without cost data produces a useless audit.
- **Year 2 and Year 3 SaaS cost must use 10% inflation:** The 3-year SaaS cost formula compounds at 10%/year. Do not use flat pricing for all 3 years — SaaS vendors raise prices.
- **Month 1 actions must require zero code:** The 12-month action plan's Month 1 is negotiation and cancellation only. Surfacing a build task in Month 1 breaks the voice rule ("This call / this email / this click saves you $X").
- **Stack assumption is Next.js + Supabase + Vercel:** All build cost estimates default to this stack. If the user specifies a different stack, adjust hosting and maintenance estimates accordingly before running cost math.
