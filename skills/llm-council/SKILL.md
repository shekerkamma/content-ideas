---
name: llm-council
description: 'Run any question, idea, or decision through a council of 5 AI advisors who independently analyze it, peer-review each other anonymously, and synthesize a final verdict. Based on Karpathy''s LLM Council methodology. MANDATORY TRIGGERS: ''council this'', ''run the council'', ''war room this'', ''pressure-test this'', ''stress-test this'', ''debate this''. STRONG TRIGGERS (use when combined with a real decision or tradeoff): ''should I X or Y'', ''which option'', ''what would you do'', ''is this the right move'', ''validate this'', ''get multiple perspectives'', ''I can''t decide'', ''I''m torn between''. Do NOT trigger on simple yes/no questions, factual lookups, or casual ''should I'' without a meaningful tradeoff. DO trigger when the user presents a genuine decision with stakes, multiple options, and context suggesting they want it pressure-tested from multiple angles.'
---

# LLM Council

You ask one AI a question, you get one answer. That answer might be right. It might be confidently wrong. You have no way to tell because you only saw one perspective.

The council fixes this. Your question runs through 5 independent advisors, each attacking it from a fundamentally different angle. They then anonymously review each other's work. A chairman synthesizes where they agree, where they clash, and what you should actually do.

Adapted from Andrej Karpathy's LLM Council: dispatch to multiple perspectives, peer-review anonymously, chairman produces the final answer.

---

## When to Run the Council

The council is for decisions where being wrong is expensive.

**Good council questions:**
- "Should we build this POC on Azure OpenAI or AWS Bedrock for this client?"
- "I'm thinking of pivoting from per-project billing to a retainer model. Am I crazy?"
- "Which of these 3 architecture approaches should we pitch to the TMNA team?"
- "Should I hire a contractor or automate this with n8n first?"

**Not council questions:**
- Factual lookups (one right answer, no tradeoffs)
- Writing tasks (creation, not judgment)
- Summaries and processing tasks
- Simple yes/no with no real stakes

If the question is too vague ("council this: my business"), ask one clarifying question. Just one. Then proceed.

---

## The Five Advisors

These are thinking styles, not job titles. They create deliberate tension.

**The Killer** — Hunts for the fatal flaw. Assumes the idea is broken and tries to prove it. If everything looks solid, digs deeper. Not a pessimist—the friend who saves you from a bad deal by asking questions you're avoiding.

**The Rebuilder** — Ignores the surface question and asks "what are we actually trying to solve here?" Strips assumptions, rebuilds from the ground up. Sometimes the most valuable output is "you're asking the wrong question entirely."

**The Maximizer** — Looks for upside everyone else misses. What could be bigger? What adjacent opportunity is hiding? What's being undervalued? Doesn't care about risk—that's the Killer's job.

**The Stranger** — Has zero context about you, your field, or your history. Responds purely to what's in front of them. Catches the curse of knowledge: things that are obvious to you but opaque to everyone else. Most underrated advisor.

**The Operator** — One job: can this actually be done, and what's the fastest path? Ignores theory and big-picture thinking. Every idea gets filtered through "OK but what do you do Monday morning?"

**Natural tensions:** Killer vs Maximizer (downside vs upside). Rebuilder vs Operator (rethink everything vs just ship it). The Stranger sits in the middle keeping everyone honest.

---

## How a Council Session Works

### Step 1: Frame the Question

When triggered, do two things before framing:

**A. Scan for workspace context.** Quick-scan for relevant files:
- `CLAUDE.md` / `.claude/` memory files (business context, constraints, preferences)
- Files the user referenced or attached
- Prior council transcripts on the same topic

Use Glob and quick Read calls. Spend no more than 30 seconds. You're looking for the 2-3 files that give advisors enough to give specific, grounded advice instead of generic takes.

**B. Frame the question.** Rewrite the raw question as a clear, neutral prompt all five advisors will receive. Include:
1. The core decision
2. Key context from the user's message
3. Relevant context from workspace files (business stage, constraints, numbers, past results)
4. What's at stake

Don't add your opinion. Don't steer. But make sure each advisor has enough context to give specific advice.

---

### Step 2: Convene the Council (5 sub-agents, all at once)

Spawn all 5 advisors simultaneously. Each gets their identity, the framed question, and this instruction: respond independently, don't hedge, lean fully into your assigned perspective. The synthesis comes later.

**Sub-agent prompt template:**

```
You are [Advisor Name] on an LLM Council.

Your thinking style: [advisor description from above]

A user has brought this question to the council:
---
[framed question]
---

Respond from your perspective only. Be direct and specific. Don't hedge or try to be balanced. Lean fully into your assigned angle—the other advisors will cover what you're not covering.

Keep your response between 150-300 words. No preamble. Go straight into your analysis.
```

Run all 5 in parallel. Do not let earlier responses influence later ones.

---

### Step 3: Peer Review (5 more sub-agents, all at once)

This is what separates the council from "ask 5 times." It's Karpathy's core insight.

Collect all 5 advisor responses. Anonymize them as Response A through E (randomize which advisor maps to which letter—no positional bias). Spawn 5 new sub-agents, one per reviewer. Each sees all 5 anonymized responses and answers three questions.

**Reviewer prompt template:**

```
You are reviewing the outputs of an LLM Council. Five advisors independently answered this question:
---
[framed question]
---

Here are their anonymized responses:

**Response A:** [response]
**Response B:** [response]
**Response C:** [response]
**Response D:** [response]
**Response E:** [response]

Answer these three questions. Be specific. Reference responses by letter.

1. Which response is the strongest? Why?
2. Which response has the biggest blind spot? What is it missing?
3. What did ALL five responses miss that the council should consider?

Keep your review under 200 words. Be direct.
```

Run all 5 reviewers in parallel.

---

### Step 4: Chairman Synthesis

One agent gets everything: the framed question, all 5 advisor responses (de-anonymized—label them by advisor name), and all 5 peer reviews. The chairman produces the final verdict.

**Chairman prompt template:**

```
You are the Chairman of an LLM Council. Synthesize the work of 5 advisors and their peer reviews into a final verdict.

The question brought to the council:
---
[framed question]
---

ADVISOR RESPONSES:
**The Killer:** [response]
**The Rebuilder:** [response]
**The Maximizer:** [response]
**The Stranger:** [response]
**The Operator:** [response]

PEER REVIEWS:
[all 5 peer reviews]

Produce the council verdict using this exact structure:

## Where the Council Agrees
[Points multiple advisors converged on independently. These are high-confidence signals.]

## Where the Council Clashes
[Genuine disagreements. Present both sides. Explain why reasonable advisors disagree here.]

## Blind Spots the Council Caught
[Things that only emerged through peer review. What individual advisors missed that others flagged.]

## The Recommendation
[A clear, direct recommendation. Not "it depends." A real answer with reasoning. The chairman can disagree with the majority if one dissenter's reasoning is strongest—explain why.]

## The One Thing to Do First
[A single concrete next step. Not a list. One thing.]

Be direct. Don't hedge. The whole point of the council is clarity you couldn't get from one perspective.
```

---

### Step 5: Deliver the Output

After the chairman synthesis completes:

**Generate an HTML report.** A single self-contained file. Structure:
- The framed question at the top
- The chairman's verdict as the main content (this is what most people read)
- Collapsible sections for each advisor's full response (collapsed by default, labeled by advisor name)
- Collapsible section for peer review highlights
- Timestamp at the bottom

Design: dark background (`#0A0A0A`), primary text (`#F5F4EE`), secondary text (`#D6D4CB`), red accent (`#D93025`) for section labels and dividers, surface cards (`#141413`). No emoji. System-sans body font. Cards with subtle borders (`rgba(245,244,238,0.06)`). Readable at a glance.

**Save both files** to `D:\AppliedAICourse\Claude Cowork\OUTPUTS\llm-council\`:
- `council-report-[YYYY-MM-DD-HHmm].html`
- `council-transcript-[YYYY-MM-DD-HHmm].md`

The transcript includes: original question, framed question, all 5 advisor responses, all 5 peer reviews with anonymization mapping revealed, and the chairman's full synthesis.

Provide a `computer://` link to the HTML report so the user can open it directly.

---

## Critical Rules

**Spawn all 5 advisors in parallel.** Sequential spawning lets earlier responses bleed into later ones. Never do this.

**Anonymize for peer review.** If reviewers know which advisor said what, they'll defer to thinking styles they prefer instead of evaluating on merit.

**The chairman can overrule the majority.** If 4 of 5 say "do it" but the dissenter's logic is tighter, the chairman sides with the dissenter and explains why.

**The recommendation must be concrete.** "It depends" is not a recommendation. Pick a side and defend it.

**Don't council trivial questions.** If someone asks something with one right answer, just answer it. The council is for genuine uncertainty with real stakes.
