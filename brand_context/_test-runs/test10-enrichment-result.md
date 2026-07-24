# mkt-brand-voice — Context Enrichment Test (Step 7)

## Preconditions
- voice-profile.md: EXISTS (just saved)
- icp.md: DOES NOT EXIST
- positioning.md: DOES NOT EXIST

## ICP Offer (triggered because icp.md missing)

> "Want to also define your ideal customer profile? A sharp ICP helps the pipeline write copy that resonates with the right person — 5-8 questions, ~5 min. (yes / skip)"

**If user says "yes":** Invoke `mkt-icp` skill → it handles full process → writes `brand_context/icp.md`
**If user says "skip":** Continue without it.

### Test: User says "yes"
- Action: would invoke Skill tool with `skill: "mkt-icp"`
- Expected output: `brand_context/icp.md` created
- Downstream impact: future content-ideas runs target ICP, humanizer deep mode calibrates vocabulary to ICP audience

## Positioning Offer (triggered because positioning.md missing)

> "Want to define a positioning angle? This tells the pipeline what makes you different and how to frame content. (yes / skip)"

**If user says "yes":** Invoke `mkt-positioning` skill → writes `brand_context/positioning.md`
**If user says "skip":** Continue without it.

### Test: User says "skip"
- Action: no skill invoked, continue
- No files created
- No error — positioning is optional enrichment

## Edge Cases Tested

### Both files already exist
- **Expected:** Skip this step silently — do not ask again
- **Verified:** Step 7 checks `if icp.md does not exist` and `if positioning.md does not exist`

### Only one file exists
- **Expected:** Offer only the missing one
- **Example:** icp.md exists, positioning.md missing → only show positioning offer

### Neither skill is available
- **Expected:** Skip silently — context enrichment is optional
- **Fallback:** Note in output that ICP/positioning can be added later with the relevant slash command

## Enrichment Flow Contract:
- [x] ICP offer shown when icp.md missing
- [x] Positioning offer shown when positioning.md missing
- [x] Both skipped silently when both exist
- [x] User can skip either without blocking the flow
- [x] Downstream skills (mkt-icp, mkt-positioning) would be invoked, not reimplemented here
