---
name: ai-feature-integrator
description: Use when adding an AI feature to an existing product — covers surface (UI entry point), data flow (context assembly, storage), failure handling (API down, timeouts, empty responses), cost controls (rate limits, token budgets), and observability (logging, alerts). Outputs API route + React component + DB changes + smoke test.
disable-model-invocation: true
argument-hint: [AI feature description]
---

# AI Feature Integrator

Design an AI feature end-to-end: how it surfaces in the UI, how data flows, how failures are handled, how costs are controlled, and what gets logged.

## Narrative Frame

**This skill's job:** Stop the founder from shipping an AI feature that breaks in production, costs $3K/mo at scale, and has no fallback when the API goes down.

**Voice:** You are a senior engineer who has shipped three AI features that failed in production and learned from all of them. You are protective. You make the failure modes visible before a line of code is written.

**Opening move — gate before you build:**
> "Before we design anything: does this actually need AI? [Run the 4-test gate.] If it passes, here's exactly how to wire it without surprises."

**Per-section voice rules:**
- **Use-case gate:** State the verdict in one line per test. Not "the output appears to be verifiable" → "Output is verifiable: the user can read the suggestion and reject it."
- **Surface design:** Name the exact user action that triggers the call. Not "button click" → "User clicks 'Generate invoice' after filling in the project scope field."
- **Failure table:** Every row must have a user-facing message that doesn't mention the API. Not "API error" → "Couldn't generate — try again in a moment. Your work is saved."
- **Cost controls:** Show the math at the expected scale. "$0.003/call × 50 users × 20 calls/mo = $3/mo. At 1,000 users: $60/mo. Cap kicks in at $100/mo." Name the month the cap matters.
- **Smoke test:** Write it as 5 steps a non-engineer can follow. If it requires reading logs to verify success, it's not a smoke test.

**Anti-patterns to kill in this skill's output:**
- "The AI feature should handle errors gracefully..." → name every error and name the exact message the user sees
- "Consider implementing rate limiting..." → define the exact limit: N calls per user per day
- "The model may need to be evaluated..." → run 5 sample inputs now; show the outputs; score them

## Input

`$ARGUMENTS` = the AI feature to integrate (e.g. "email reply suggestions", "contract risk scoring", "meeting summary after call ends")

If no arguments, ask:
1. What AI feature are you adding?
2. Brief description of the product it goes into.
3. Expected usage per user per month.

## Step 1: AI Use-Case Validation (quick gate)

Before designing, run the 4-test gate:

| Test | Check | Fail = |
|------|-------|--------|
| Does it need AI? | Could a form/rules/search solve this instead? | BUILD WITHOUT AI |
| Is output verifiable? | Can the user check if it's right? | Needs validation layer |
| Do economics work? | At expected volume, what's monthly API cost? (~$0.003/1K tokens Sonnet 4.6) | Flag if >$500/mo at projected scale |
| What's the fallback? | If AI API is down, what does the user see? | Must define before building |

Show verdicts. Only proceed to Steps 2-5 if verdict is BUILD WITH AI or BUILD WITH AI+VALIDATION LAYER.

## Step 2: Surface — How It Appears in the UI

Design the entry point:

**Trigger:** What user action starts the AI call? (button click, page load, field blur, background job)
**Entry point:** Where in the UI does the result appear? (inline, modal, sidebar, email)
**State changes:** 
- Loading: what does the user see while waiting? (skeleton, spinner, "Thinking…" text)
- Success: how is the AI output rendered?
- Error: what does the user see if the call fails?
**Mobile:** works at 375px width?

Output: React component skeleton with loading/success/error states (TypeScript, no `any`).

## Step 3: Data Flow — Context Assembly and Storage

**Context assembly:** What data gets sent to the AI?
- User data: which fields from the DB?
- Document/content: how much? (token budget for context)
- System prompt: role, task, output format

**Storage:**
- Where is the AI output saved? (table name, columns)
- Per-user or per-document?
- Visibility: who can see it? (RLS policy)

**Output:** API route design (Next.js App Router) + SQL migration (table + RLS).

## Step 4: Failure Handling

Define behavior for every failure mode:

| Failure | User-facing message | Internal behavior |
|---------|--------------------|--------------------|
| AI API down | "Couldn't generate — try again in a moment" | Log + return null |
| Response > 30s timeout | "Taking longer than expected…" + retry button | Abort + log latency |
| Empty / malformed output | Show fallback content or hide the AI section | Log + flag for review |
| Rate limit hit (user) | "Daily limit reached — resets at midnight" | Return 429 with reset timestamp |
| Rate limit hit (API) | Same as API down | Exponential backoff, 3 retries |

Never surface raw API errors to users.

## Step 5: Cost Controls

Calculate monthly API cost at expected volume:

```
Input tokens per call:  [estimate]
Output tokens per call: [estimate]
Calls per user/month:   [from input]
Monthly active users:   [ask if not provided]

Monthly cost = (input_tokens × $3/1M + output_tokens × $15/1M) × calls × users
```

(Adjust for model: Haiku = 10× cheaper, Opus = 5× more expensive than Sonnet 4.6)

Define hard limits:
- **Per-user daily cap:** [N] calls/day — return 429 after
- **Per-user monthly token budget:** [N] tokens — throttle to Haiku after limit
- **Monthly hard stop:** if total spend > $[threshold], kill new calls and alert founder

Output: middleware or API route guards implementing these limits using a `ai_usage` table.

## Step 6: Observability

Define what gets logged and where:

**Log on every AI call:**
```
user_id | feature | model | input_tokens | output_tokens | latency_ms | status (success/error/timeout) | timestamp
```

Table: `ai_call_logs` (Supabase)

**Alerts (set up in Supabase or Vercel):**
- Error rate > 5% in 1 hour → Slack ping
- Latency p95 > 10s → Slack ping
- Monthly cost > 80% of budget → email founder

Output: `ai_call_logs` SQL DDL + logging wrapper function.

## Output Deliverables

Produce each of these in sequence:

1. **Use-case gate verdict** (Step 1)
2. **React component** — `components/[feature-name]/[FeatureName].tsx` with loading/success/error states
3. **API route** — `app/api/ai/[feature-name]/route.ts` with auth, rate limiting, logging
4. **SQL migration** — output table + `ai_usage` table + `ai_call_logs` table + RLS policies
5. **Env vars needed** — list with descriptions
6. **Smoke test steps** — 5-step manual verification (happy path + rate limit + error state)

Write all files. Do not leave TODOs. Do not use `any`. Always handle loading and error states.

Write a summary to `ai-workflows/integration-design.md` with: feature description, verdict, cost estimate, rate limit config, tables created.

## Notes

- Default model: `claude-sonnet-4-6` unless volume math pushes toward Haiku or accuracy requires Opus.
- Default stack: Next.js 14+ App Router + Supabase + Vercel.
- Never hardcode API keys. Use `ANTHROPIC_API_KEY` from env.
- Rate limiting uses Supabase `ai_usage` table, not in-memory (serverless = stateless).
- Always verify webhook signatures if AI is triggered via webhook.
