# Session Handoff: KYC Workflow Prototype

Date: 2026-06-20
Repository: `/home/shekerk/content-ideas`
Branch: `main`
Latest pushed commit: `c87bd33 Add KYC workflow and Playwright e2e`

## Current State

Implemented and pushed a concrete, validated financial-services KYC workflow prototype.

The committed work includes:

- Domain workflow skill: `domain-workflows/financial-services/kyc-screening/SKILL.md`
- Workflow contract: `domain-workflows/financial-services/kyc-screening/workflow.json`
- Trusted rules grid: `domain-workflows/financial-services/kyc-screening/references/rules-grid.json`
- Deterministic Python runner: `domain-workflows/financial-services/kyc-screening/scripts/run_kyc_screening.py`
- Validator/eval gate: `domain-workflows/financial-services/kyc-screening/scripts/validate_kyc_disposition.py`
- Sample eval fixture: `domain-workflows/financial-services/kyc-screening/evals/sample-pep-escalation/`
- Next.js API hook: `app/api/domain-workflows/kyc-screening/route.ts`
- Frontend workflow screen: `app/domain-workflows/kyc-screening/page.tsx`
- UI component contract: `lib/domain-workflows/kyc-ui.ts`
- Dashboard link: `app/dashboard/page.tsx`
- Playwright config and KYC e2e test:
  - `playwright.config.ts`
  - `tests/e2e/kyc-screening.spec.ts`
  - `docs/playwright.md`
- Project instructions updated:
  - `AGENTS.md`
  - `.gitignore`

## What The Workflow Tests

The test proves this chain works end to end:

```text
KYC page
-> Run workflow button
-> Next.js API route
-> Python KYC runner
-> trusted rules grid
-> validator
-> generated UI component payload
-> React-rendered result
```

The sample applicant is `Northstar Family Holdings Ltd.`

Input facts:

- confirmed PEP exposure
- possible adverse media hit
- missing source of funds document
- no sanctions hit

Expected business output:

- risk: `high`
- disposition: `escalate-EDD`
- human review required: `true`
- validation: `pass - 0 errors`
- rule evidence includes `R-PEP-001`, `R-AM-001`, `R-DOC-001`, `R-SOF-001`

## Validation Already Run

These passed before the commit:

```bash
npm run test:e2e:kyc
npm run typecheck
npm run lint
```

The KYC e2e test output was:

```text
1 passed
```

The Playwright test opens `/domain-workflows/kyc-screening`, clicks `Run workflow`, waits for the API `200`, then checks that the generated UI renders:

- `escalate-EDD`
- `high risk`
- `pass - 0 errors`
- `source of funds`
- `R-PEP-001`

## Manual Test

Start the app:

```bash
npm run dev
```

Open:

```text
http://localhost:3000/domain-workflows/kyc-screening
```

Expected initial screen:

- `KYC workflow`
- applicant form
- `Run workflow`
- `No disposition yet`

Click `Run workflow`.

Expected generated UI:

- applicant: `Northstar Family Holdings Ltd.`
- risk badge: `high risk`
- disposition badge: `escalate-EDD`
- review badge: `human review`
- missing document: `source of funds`
- validation: `pass - 0 errors`
- rule outcomes table includes `R-PEP-001`

## Playwright Notes

Installed dev dependency:

```text
@playwright/test
```

Useful commands:

```bash
npm run test:e2e
npm run test:e2e:kyc
npm run test:e2e:headed
npm run test:e2e:install
```

Important gotcha:

If `npm run build` was run while `npm run dev` was already active, restart `npm run dev` before Playwright testing. A stale dev server can serve HTML that points to missing `.next` chunks such as `main-app.js`, which prevents React hydration and makes clicks no-op.

## Git State At Handoff

Pushed:

```text
c87bd33 Add KYC workflow and Playwright e2e
```

Remote push target:

```text
origin/main -> github.com:shekerkamma/content-ideas.git
```

The working tree still contains many pre-existing untracked directories and run artifacts unrelated to this KYC workflow. They were intentionally not committed.

This handoff file itself was created after the push and may be uncommitted unless separately staged and committed.

## Suggested Next Steps

1. Promote the workflow into a reusable/global skill only after deciding the install location and trigger phrases.
2. Add a second eval case for a sanctions-confirmed applicant to validate `decline-recommend`.
3. Add a clean applicant case to validate `clear`.
4. Consider extracting the frontend "generated UI renderer" into a reusable pattern for future domain workflow skills.
5. If committing this handoff, stage only this file and avoid sweeping unrelated untracked directories.
