# Claude Code Director and PLAID build loop

<!-- Moved out of CLAUDE.md so it only loads when needed. Read on demand. -->

## Claude Code Director Skill
- `.claude/skills/claude-code-director/SKILL.md` — Director Framework (Cole Medin):
  Plan First → Manage Context → Verify The Work → Build The System. Generates
  PLAN.md, context budget, verification harness, and system evolution notes.
- Trigger: `/claude-code-director` or "director mode", "plan this properly",
  "stop vibe coding", "apply the director framework"


## PLAID build loop

For long-running app builds, use PLAID as the product source of truth and
Codex/Claude `/goal` as the execution loop:
1. Read `vision.json`, `docs/product-vision.md`, `docs/prd.md`, and
   `docs/product-roadmap.md`.
2. If `docs/design.md` is present, follow it for UI. If it is missing, use the
   brand guidance in `docs/product-vision.md` and keep the UI restrained.
3. Execute roadmap tasks in order, one phase at a time.
4. Mark roadmap checkboxes complete only after implementation and verification.
5. Run available build, lint, test, and manual verification before reporting a
   goal achieved.

