# Grill-Me Review: Gold-Standard Blueprint Drafts

Date: 2026-06-26

Reviewed files:

- `gold-standard/Conversational_Support_Master_Blueprint.md`
- `gold-standard/HR_Onboarding_Agent_Master_Blueprint.md`
- `gold-standard/KYC_AML_Onboarding_Agent_Master_Blueprint.md`
- `gold-standard/Prior_Authorization_Agent_Master_Blueprint.md`
- `gold-standard/AI_code_assistant_Master_Blueprint.md`

## Bottom Line

The five drafts are a strong upgrade from the imported Antigravity sketches.
They are structurally complete and usable as internal strategic drafts.

They are not yet `reviewed` deliverables. The biggest gap is not section
coverage; it is buyer-grade business-case specificity. The ROI sections still
read like directional strategy in four of five files. Before deck conversion,
each should include explicit formulas, buyer baselines, pilot price ranges,
run-cost assumptions, and sensitivity cases.

## Findings

### High: ROI Sections Are Not Yet True Business Cases

Affected:

- `HR_Onboarding_Agent_Master_Blueprint.md`
- `KYC_AML_Onboarding_Agent_Master_Blueprint.md`
- `Prior_Authorization_Agent_Master_Blueprint.md`
- `AI_code_assistant_Master_Blueprint.md`

The reconstructed Skill #5 requires current-state cost, agentic MVP cost,
pricing options, ROI cases, breakeven, and assumptions. The drafts contain
scenario tables, but most lack concrete formulas.

Required fix:

- Add current monthly cost formula.
- Add pilot price assumption.
- Add monthly run/maintenance assumption.
- Add base/upside/downside calculations.
- State which numbers are sourced versus assumptions.

Example shape:

```text
Current monthly cost = volume * minutes per case / 60 * loaded hourly cost
Agentic monthly cost = platform minimum + usage + review minutes
Monthly value = current cost avoided - agentic monthly cost
Payback = pilot/build cost / monthly value
```

### High: Scores Look Overconfident Without Interview-Proven Evidence

Affected: all five.

The diagnostic scores are useful, but they are inferred from scorecard +
research, not from the original six-question founder/user interview flow. A
skeptical reader could challenge scores like 28/30 for Prior Authorization or
27/30 for Conversational Support.

Required fix:

- Label the score as `research-inferred`, not interview-validated.
- Add a sentence: "This score should be confirmed with 3 buyer interviews."
- Keep the score, but lower certainty unless buyer interviews exist.

### Medium: Competitive Tables Omit Some Important Named Incumbents

Affected:

- HR: Rippling, Workday, HiBob, SAP SuccessFactors are mentioned but not in the
  teardown table.
- KYC/AML: Fenergo, NICE Actimize, Unit21, Middesk, and Dow Jones/LSEG are
  relevant but not tabled.
- Prior Authorization: CoverMyMeds, Availity, Waystar, Surescripts, Experian
  Health are mentioned but not tabled.
- AI Code Assistant: Anthropic Claude Code and OpenAI Codex are mentioned but
  not tabled.

Required fix:

- Expand tables or split into `direct competitors` and `adjacent incumbents`.
- Keep each table tight enough for deck conversion.

### Medium: ICP Is Still Too Broad In Some Drafts

Affected:

- Conversational Support: targets ecommerce, travel, marketplace, fintech,
  insurance, subscription. The MVP should pick one for concrete positioning.
- AI Code Assistant: "100-2,000 engineer companies" is broad. Strongest wedge
  is regulated/legacy/proprietary monorepo teams.
- HR Onboarding: 100-1,000 employee range is reasonable, but hiring-volume
  threshold should be a gating criterion earlier.

Required fix:

- Add `Initial ICP` and `Later ICPs` distinction.
- Use one concrete wedge per MVP.

### Medium: Source Notes Need Consistent Access Dates And Claim Mapping

Affected:

- AI Code Assistant
- HR Onboarding
- KYC/AML
- Prior Authorization

Conversational Support is best here: most sources include accessed date and
claim supported. The others mostly list sources without exact claim mapping.

Required fix:

- Normalize source notes as: `Source - URL - accessed YYYY-MM-DD - claim`.

### Medium: Source Confidence Should Be More Nuanced

Affected:

- HR Onboarding
- Prior Authorization
- KYC/AML

`source_confidence: high` is fair for problem evidence, but not for pricing in
opaque enterprise categories. Source confidence should be split:

```yaml
source_confidence:
  problem: high
  competitor: medium-high
  pricing: low-medium
  implementation: medium
```

### Low: Deck-Ready Summaries May Inherit Draft Weaknesses

Affected:

- `deck/gold-standard-opportunity-summaries.md`

The summaries are clean, but they should not be used as final slides until the
ROI and source-note fixes land. Otherwise the deck will look sharper than the
evidence underneath.

## Per-Blueprint Verdict

| Blueprint | Verdict | Reason |
|---|---|---|
| Conversational Support | Strongest; near reviewed | Best positioning, strongest ROI structure, strongest source notes. Needs final ROI formula and interview-validation caveat. |
| Prior Authorization | Strategically strong, needs source/ROI polish | Excellent pain/regulatory wedge. Needs fuller competitor table and explicit ROI math. |
| KYC/AML | Strong but high-risk | Good regulatory boundary. Needs stronger model-risk language, expanded incumbents, and ROI calculations. |
| AI Code Assistant | Good but crowded | Wedge is credible if narrowed to governed repo operations. Needs sharper ICP and ROI math. |
| HR Onboarding | Useful but weakest wedge | Real pain, but less urgent than others. Needs stronger buyer pain quantification and source confidence nuance. |

## Recommended Fix Order

1. Upgrade ROI formulas across all five.
2. Add research-inferred score caveat to all diagnostics.
3. Normalize source notes with access dates and claim mapping.
4. Expand competitor tables where direct threats are missing.
5. Narrow initial ICP per blueprint.
6. Only then change status from `draft-needs-operator-review` to `reviewed`.

## Deck Gate

Do not produce the final branded deck yet. Generate it only after at least:

- Conversational Support and Prior Authorization pass the fixes above.
- The other three are either fixed or clearly marked as secondary examples.

## Fix Pass: 2026-06-26

Applied fixes to:

- `gold-standard/Conversational_Support_Master_Blueprint.md`
- `gold-standard/Prior_Authorization_Agent_Master_Blueprint.md`

Changes made:

- Marked diagnostic scores as `research-inferred`.
- Added initial ICP and later ICP distinction.
- Split source confidence into problem, competitor, pricing, and implementation.
- Added ROI formulas, assumptions, and numeric scenario examples.
- Expanded competitor tables where important adjacent incumbents were missing.
- Updated status to `reviewed` for those two files only.

Remaining drafts:

- None in the five-file gold-standard batch.

## Fix Pass: Remaining Three

Applied the same fix pattern to:

- `gold-standard/HR_Onboarding_Agent_Master_Blueprint.md`
- `gold-standard/KYC_AML_Onboarding_Agent_Master_Blueprint.md`
- `gold-standard/AI_code_assistant_Master_Blueprint.md`

Changes made:

- Marked diagnostic scores as `research-inferred`.
- Added initial ICP and later ICP distinction.
- Split source confidence into problem, competitor, pricing, and implementation.
- Added ROI formulas, assumptions, and numeric scenario examples.
- Expanded competitor tables where important direct or adjacent incumbents were
  missing.
- Updated status to `reviewed`.

Current gold-standard strategy audit:

- 5 reviewed
- 0 draft-needs-operator-review

## Implementation-Depth Reclassification

After the user's clarification, the bar for "implementation blueprint" is
higher than the prior strategy-review gate. This does not mean we are building
the use cases. It means the blueprint artifact must include exact implementation
planning details: schema/data model, API surface, integrations, folder/module
structure, environment variables, deployment checks, and observability.

`qa/implementation-depth-audit.tsv` shows the current five reviewed files still
need an implementation-depth pass:

- `Conversational_Support_Master_Blueprint.md`: missing folder/module structure
  and env vars.
- `AI_code_assistant_Master_Blueprint.md`: missing API surface, folder/module
  structure, and env vars.
- `HR_Onboarding_Agent_Master_Blueprint.md`: missing API surface, folder/module
  structure, and env vars.
- `KYC_AML_Onboarding_Agent_Master_Blueprint.md`: missing API surface,
  folder/module structure, and env vars.
- `Prior_Authorization_Agent_Master_Blueprint.md`: missing API surface,
  folder/module structure, and env vars.

Recommendation: upgrade the five reviewed strategy blueprints into complete
implementation-ready capability blueprints before deck conversion, starting with
Conversational Support because it is closest to passing.
