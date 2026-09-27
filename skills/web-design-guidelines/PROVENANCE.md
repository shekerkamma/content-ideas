# Provenance

- `references/command.md` is the Vercel Labs Web Interface Guidelines ruleset, from
  [vercel-labs/web-interface-guidelines](https://github.com/vercel-labs/web-interface-guidelines)
  `command.md`, MIT (see `LICENSE-web-interface-guidelines`). Upstream main at the time of vendoring:
  e3d624b (2026-08-18).
- `SKILL.md` and `scripts/audit.mjs` are this repo's own: a condensed rulebook and a five-rule source
  audit. `audit.mjs` always exits 0; `e2e-qa-review`'s lanes runner turns its output into findings and
  treats a zero-file scan as BLOCKED.
