# DealForge Test Accounts

Use these accounts to exercise the Phase 2 pipeline in a controlled way.

## Primary Account

**Acme Manufacturing**
- Industry: Manufacturing
- Segment: Mid-market
- Test angle: predictive quality
- Why: gives the pipeline a concrete operational use case with enough specificity to test research quality, brief framing, deck depth, and objection handling.

## Test Matrix

### 1. Rich-Data Enterprise
- Account: Thompson Manufacturing Group
- Industry: Manufacturing
- Test angle: broad account research and deck specificity
- Expectation: the brief should be detailed and grounded in public signals.

### 2. Thin-Data Private Company
- Account: Northstar Fabrication
- Industry: Manufacturing
- Test angle: graceful fallback and honest uncertainty
- Expectation: the pipeline should flag weak public data instead of fabricating confidence.

### 3. Compliance-Heavy Vertical
- Account: Meridian Health Services
- Industry: Healthcare
- Test angle: conservative messaging and risk-aware positioning
- Expectation: objections should reflect compliance and data sensitivity concerns.

### 4. Fast-Moving SaaS
- Account: SignalStack
- Industry: SaaS
- Test angle: speed, ROI, and concise deck flow
- Expectation: the package should move quickly from pain to value to next steps.

### 5. Operational Use Case
- Account: Harbor Logistics
- Industry: Logistics
- Test angle: operational AI and measurable ROI
- Expectation: the output should center on workflow efficiency and process visibility.

## Prompt Shape

Use the same prompt structure for each account:

```text
Build a DealForge package for <account name>.
Industry: <industry>
Focus: <test angle / use case>
Flag thin-data sections clearly.
Generate the brief, deck, objections, and package outputs as described in docs/product-roadmap.md.
```

