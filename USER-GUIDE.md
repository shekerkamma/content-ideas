# DealForge User Guide

## 1. End-to-End Test Guide

Use this when you want to verify that the PLAID and `/goal` workflow still produces the right product scaffold.

### Purpose
Prove that the roadmap, prompt, and output stay aligned from intake to verification.

### Test Inputs
- One real test account
- One use case
- One bounded `/goal` or `/plaid build` prompt

### Recommended Test Accounts
- Rich-data enterprise account
- Mid-market vertical account
- Thin-data private company
- Compliance-heavy account
- Fast-moving SaaS account

See `docs/test-accounts.md` for the current Phase 2 matrix and the primary exploratory account.

### Run Pattern
1. Read `docs/product-vision.md`, `docs/prd.md`, and `docs/product-roadmap.md`.
2. Start from Phase 1 only.
3. Use a prompt that explicitly limits scope to `TASK-001` through `TASK-005`.
4. Verify that the agent updates only the expected files.
5. Confirm build, lint, and typecheck pass.
6. Check that roadmap checkboxes match verified work.

### Pass Criteria
- Correct phase selected
- Only expected files changed
- Verification commands pass
- No drift into later phases
- Output matches the stated use case

### Failure Signals
- Generic or unfocused output
- Wrong phase selected
- Scope creep into later roadmap tasks
- Missing or skipped verification
- Checkbox updates that do not match actual work

## 2. `/goal` Usage Guide

Use this when running long-lived work in Codex or Claude Code.

### What It Is
`/goal` sets a bounded objective that the agent keeps working toward until the goal is complete, paused, cleared, or blocked.

### Good Goal Shape
- Objective
- Scope
- Acceptance criteria
- Verification commands
- Constraints
- Stop conditions

### Example Prompt
```text
/goal Build DealForge Phase 1 from docs/product-roadmap.md using the repo-local PLAID artifacts.
Scope: complete TASK-001 through TASK-005 only.
Read docs/prd.md, docs/product-vision.md, vision.json, and docs/product-roadmap.md as the product contract.
Implement the Phase 1 scaffold.
Mark tasks complete only after implementation and verification.
Verify with build, lint, and typecheck.
Stop if required credentials or missing product/design decisions prevent meaningful progress.
```

### Best Practices
- Read the roadmap before starting
- Keep goals phase-specific
- Put the acceptance criteria in writing
- Stop at the boundary you actually want
- Verify the result before marking tasks done

### Anti-Patterns
- Vague goals like “build the app”
- Mixed-scope asks that cross multiple phases
- No verification step
- No stop rule
- Letting the agent mark work complete without validation

## 3. DealForge App User Guide

Use this when explaining how the app itself works.

### Local Setup
1. Run `npm run dev`.
2. Open `http://localhost:3000`.
3. Use the dashboard to create a deal and follow the pipeline.

### What DealForge Does
DealForge turns a prospect name into a deal-prep package:
- account brief
- strategy brief
- branded deck
- objection script
- downloadable package

### User Flow
1. Enter a prospect name.
2. Optionally add industry and use case.
3. Wait for research and generation.
4. Review the outputs.
5. Edit or rerun if needed.
6. Download the package.

### Routes To Test
- `/` landing page
- `/dashboard` deal intake and dashboard shell
- `/deal/[id]` pipeline progress and downloads
- `/api/deals/[id]/download?artifact=brief`
- `/api/deals/[id]/download?artifact=deck`
- `/api/deals/[id]/download?artifact=objections`
- `/api/deals/[id]/download?artifact=zip`

### What the User Sees
- Dashboard
- Empty state
- Deal cards
- Progress indicator
- Review queue
- Download actions
- Thin-data warnings when public data is limited

### What Good Output Looks Like
- Specific to the account
- Grounded in the stated industry
- Honest when data is thin
- Editable, not locked
- Useful in a real client meeting

### How To Review Outputs
- Check the brief for account-specific facts
- Check the deck for structure and clear use-case framing
- Check objections for real pushback, not generic filler
- Check warnings where data is thin
- Re-run with better context if the output is too generic

### What To Do When Data Is Thin
- Accept the warning
- Add your own context
- Supply a more specific use case
- Rerun the package

### Manual Test Checklist
- Start the dev server and confirm the homepage loads.
- Open the dashboard and create a new deal.
- Confirm the browser routes to the deal detail page.
- Check that the pipeline shows five stages.
- Click each download button and verify a file opens or downloads.
- Open the zip endpoint directly and confirm it returns a ZIP file.
- Confirm the app still builds with `npm run build`.

### Brand Rules
- Keep the output consultant-grade
- Avoid generic AI language
- Prefer specific numbers, risks, and implications
- Follow the brand guidance in `docs/product-vision.md`
