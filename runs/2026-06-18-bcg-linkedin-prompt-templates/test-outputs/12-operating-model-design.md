# Operating Model Design — Apex HR (Post-Payroll)

## Capability Model
Must-Win Capabilities to deliver Payroll + HR bundle to 150–500 employee segment:
1. Payroll compliance engine (state + federal tax, garnishments, direct deposit)
2. HR + Payroll integration (single data model, no re-entry)
3. Implementation and onboarding (faster than Rippling; <30 days to first payroll)
4. Customer success (proactive expansion; upsell motion from HR → Payroll)
5. Compliance monitoring (reg change alerts, audit trails)

## Operating Structure Options
| Option | Description | Pros | Cons |
|---|---|---|---|
| A — Separate Payroll BU | Dedicated team: PM, Eng, CS, Compliance | Fast; clear ownership | Duplication; integration risk between BUs |
| B — Platform model | Shared platform team; Payroll = product line | No duplication; single data model | Slower; competing priorities |
| C — Acquisition integration | Acquire team + fold in | Fastest talent acquisition | Integration overhead; culture risk |

**Recommendation: Option B (Platform)** — HR + Payroll must share a data model or customers face the same re-entry problem they're trying to escape.

## Decision Rights (RACI for Critical Decisions)
| Decision | Responsible | Accountable | Consulted | Informed |
|---|---|---|---|---|
| Payroll compliance rule changes | Compliance Lead | CPO | Legal, Engineering | All |
| Partner vs Build for payroll | CTO | CEO | CPO, CFO | Board |
| Customer pricing exceptions | VP Sales | CFO | CPO | CS |
| APAC launch go/no-go | Head of Revenue | CEO | CFO, CPO | Board |

## Ways-of-Working Changes
- Add Compliance function reporting to CPO (currently no dedicated compliance role)
- Institute weekly Payroll Readiness stand-up (Eng + CS + Compliance + Sales)
- Create Customer Advisory Board for payroll beta (10 existing customers, 150–300 employees)
