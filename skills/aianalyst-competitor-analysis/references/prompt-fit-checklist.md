# Prompt Fit Checklist For AI Analyst Competitor Analysis

Use this before turning a user prompt into a competitor-analysis run. The goal is to keep the run decision-led instead of letting a broad market, launch, or investor-report template produce a long but unfocused artifact.

## Principle

A competitor-analysis prompt should answer a competitive decision. It should not primarily optimize for report length, generic completeness, or investor polish.

Use the user's original prompt as:

- **Operating prompt** when it is already decision-led and competitor-specific.
- **QA checklist** when it is broad, launch-oriented, market-oriented, or asks for a giant report.

When the prompt is not fit, rewrite it into a shorter operating prompt and save that artifact before continuing.

## Fit Test

Ask these questions:

| Question | Good signal | Bad signal |
|---|---|---|
| What decision must the reader make? | Compete, partner, reposition, invest, de-risk, price, prioritize roadmap, brief sales. | "Write a complete report" without a decision. |
| Is the target company/product specific? | Named target, buyer, market, geography, and competitor arenas. | Generic placeholders or broad category only. |
| Are competitors grouped by buyer job? | Direct, adjacent, substitutes, incumbents, consulting/SI, internal build. | One flat vendor list. |
| Does it define evidence standards? | Source types, confidence labels, vendor-published vs independent proof. | "Use sources" only. |
| Does it avoid false precision? | Labels assumptions and missing data. | Demands market size, financial model, charts, and exact stats without evidence. |
| Is length appropriate? | Brief/report length matches the decision. | 12,000-18,000 words by default. |
| Are irrelevant launch sections removed? | Only sections that affect competitive strategy remain. | Supply chain, packaging design, broad launch tactics, or generic dashboards when irrelevant. |

## Hurt Signals

Rewrite the prompt before proceeding when it:

- Looks like a launch report rather than competitor analysis.
- Requests exhaustive volume before defining the competitive decision.
- Asks for market-size, financial-model, or unit-economics precision without available evidence.
- Encourages one section per competitor instead of arena-level synthesis.
- Treats vendor-published proof as validated proof.
- Compares the target only against the most obvious category while ignoring substitutes, consulting/SIs, internal build, or adjacent tools.
- Optimizes for deck polish before source quality and proof gaps are clear.

## Required Operating Prompt Shape

The rewritten operating prompt should use [effective-competitor-analysis-prompt.md](effective-competitor-analysis-prompt.md) as the default template. At minimum, it should include:

```yaml
objective: "<one decision-ready objective>"
core_question: "<the competitive question the report must answer>"
target: "<company/product>"
audience: "<decision audience>"
competitor_arenas:
  - "<arena by buyer job>"
required_outputs:
  - "executive answer"
  - "competitor arena map"
  - "threat matrix with confidence labels"
  - "proof gap analysis"
  - "positioning recommendation"
  - "next-step roadmap"
must_not_do:
  - "do not write a generic market report"
  - "do not invent pricing, market size, or proof"
evidence_standard: "<how claims should be sourced and labeled>"
final_answer_should_decide:
  - "<decision 1>"
  - "<decision 2>"
```

## Recommended Competitor-Analysis Prompt Pattern

For full runs, prefer the copy-ready prompt in [effective-competitor-analysis-prompt.md](effective-competitor-analysis-prompt.md). Use this shorter pattern only for quick briefs or when the run does not need full AI Analyst artifacts.

```yaml
objective: >
  Build a decision-ready competitor analysis for [target] that determines whether
  [target] can own [strategic position] and how it should defend that position
  against [arena 1], [arena 2], [arena 3], and [arena 4].

core_question: >
  Is [target]'s wedge strong enough to own a distinct category, or will buyers
  compress it into known alternatives?

required_outputs:
  - "Executive answer: where the target should compete, partner, attach, and avoid"
  - "Competitor arena map by buyer job"
  - "Threat matrix with confidence labels"
  - "Proof gap analysis"
  - "Positioning recommendation"
  - "Proof plan"
  - "30/60/90-day roadmap"

must_not_do:
  - "Do not write a generic market report"
  - "Do not organize the report as one competitor per section only"
  - "Do not treat vendor-published proof as independently validated"
  - "Do not invent pricing, market size, or customer outcomes"

final_answer_should_decide:
  - "What category the target should claim"
  - "Which competitors are most dangerous"
  - "What proof is missing"
  - "What the target should build, publish, or test next"
```

## Recommended Slide-Generation Prompt Pattern

Use this when handing the analysis to `genspark-slides` or any slide-generation tool. This is not a replacement for the operating prompt; it is the artifact-generation prompt after evidence and story QA exist.

```yaml
deck_objective: >
  Build a comprehensive editable competitor-analysis deck for [target] that
  answers [decision question] for [audience].

source_of_truth:
  - "Use the provided story-architect pack as the slide spine."
  - "Use only the provided evidence-backed datapoints and labeled assumptions."
  - "Do not invent market size, ROI, pricing, ARR, growth, implementation,
    customer-count, or competitor benchmark numbers."

slide_requirements:
  - "Use assertion titles, not topic labels."
  - "Organize by buyer job and competitive arena, not one vendor per section only."
  - "Promote supported datapoints into the main storyline."
  - "Label vendor-published numbers as vendor-published or to validate."
  - "Include proof gaps and confidence labels where evidence is thin."
  - "Treat the generated slides as upstream content/design reference; final client PPTX will be recreated through genspark-branded-deck."

allowed_numbers:
  - "<number>: <meaning>; <source/claim_id>; <required caveat>"

banned_numbers:
  - "Any number not listed in allowed_numbers unless it is a structural slide number,
    date, or roadmap day label."

qa_instruction: >
  After generation, recovered slide text will be scanned for unsupported numbers.
  Unsupported visible metrics must be removed or replaced with qualitative wording.
```

## Recommended Final Packaging Prompt Pattern

Use this after the hosted slide/reference stage and evidence cleanup.

```yaml
final_delivery:
  deck:
    tool: "genspark-branded-deck"
    source: "owned deck.html/theme.css/deck.css"
    output: "client-package/genspark-deck/build/<name>-draft.pptx"
    editability: "hybrid_editable or native_powerpoint"
    required_qa:
      - "contact-sheet review"
      - "visible unsupported-number scan"
      - "OfficeCLI or documented equivalent"
  html:
    source: "self-contained static index.html"
    local_path: "client-package/site/index.html"
    publish_path: "client-package/pages/<slug>/index.html"
    required_qa:
      - "browser/Playwright navigation check"
      - "desktop/mobile readability"
      - "GitHub Pages URL verification when requested"
  manifest:
    required: true
    must_record:
      - "hosted Genspark project URL if used"
      - "branded deck source path"
      - "PPTX path and editability"
      - "HTML local and public URL"
      - "evidence-clean scan status"
      - "sync status across hosted, PPTX, and HTML artifacts"
```

## Output Requirement

When this checklist changes the prompt, write one of:

- `inputs/operating-prompt.yaml`
- `outputs/operating-prompt.md`
- `outputs/prompt-fit-review.md`

Include:

- what was kept from the original prompt
- what was demoted to QA checklist
- what was removed as irrelevant
- the final operating prompt
