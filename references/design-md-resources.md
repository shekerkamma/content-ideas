# DESIGN.md Resources & Workflow

How to stop AI coding agents from producing the "generic AI startup" look —
same-cards, random gradients, inconsistent buttons, weak spacing. The fix is
**design context**: a `DESIGN.md` the agent reads before it writes UI code.

Captured 2026-06-22.

---

## What DESIGN.md is

`DESIGN.md` is a plain-markdown design system introduced by **Google Stitch**.
Coding agents read `AGENTS.md` for *how to build*; design agents read `DESIGN.md`
for *how it should look and feel*. No Figma exports, no JSON, no tooling — markdown
is what LLMs read best. Drop it in the project root and point the agent at it.

- Stitch spec: https://stitch.withgoogle.com/docs/design-md/specification/
- Standard 9 sections: visual theme · color palette & roles · typography ·
  component stylings · layout principles · depth & elevation · do's/don'ts ·
  responsive behavior · agent prompt guide.

## Two kinds of DESIGN.md — keep them separate

| Kind | Purpose | Use when | Caveat |
|---|---|---|---|
| **Borrowed** (library) | Make UI feel like Linear / Stripe / Notion | Inspiration, internal demos | Extracted from public sites — inspiration, **not a clone license** for client work |
| **Owned** (ours) | Enforce *our* consistent identity | Client deliverables, anything shipped | Original tokens — safe |

Our owned one: [`../DESIGN.md`](../DESIGN.md) — **Aurora Glass**, derived from the
`neon` Marp theme so slides + app UI share one identity.

## Resources

### getdesign.md — https://getdesign.md
- ~75 ready-to-use DESIGN.md files (Claude, Linear, Stripe, Vercel, Notion, Cursor…).
- Built on the MIT repo **`VoltAgent/awesome-design-md`** (90k★) — public catalog is free.
- Each entry: `DESIGN.md` + `preview.html` + `preview-dark.html`.
- Freemium: free public templates; paid "private DESIGN.md" crafting + LaunchKit.
- Repo: https://github.com/VoltAgent/awesome-design-md

### Refero Styles / Refero MCP — https://styles.refero.design · https://refero.design/mcp
- Bigger and deeper: **2,000+** DESIGN.md style examples; the MCP exposes
  **132,000+ real product screens + 10,000+ user flows** (web + iOS).
- **Refero MCP** = the standout: agent searches/studies real screens *at build time*
  instead of copying a static file. Works with Claude Code, Cursor, Codex, Lovable,
  Antigravity, Manus.
- **Status: requires Refero Pro (paid).** Config is gated behind sign-in; first call
  opens a browser to authorize. Cannot be wired up without a Pro account.
- **Refero Skill (free, open):** a research→extract→craft design methodology skill —
  `npx skills add https://github.com/referodesign/refero_skill`
- Also has a Figma plugin and "research mode."

## The workflow

1. **Research** — use Refero MCP (if Pro) or browse getdesign.md / Refero Styles to
   study real products that solved the same UI problem.
2. **Distill** — extract the patterns into our **own** `DESIGN.md` (Aurora Glass, or a
   client-specific token set). Never ship a borrowed brand's identity as client work.
3. **Build** — point the agent at `DESIGN.md`: *"Build the UI using DESIGN.md."*
4. **Sync** — keep app tokens and the `neon` Marp theme (`~/.claude/skills/marp/SKILL.md`)
   in step so decks and product UI share one system.

## Design QA gate — Impeccable detector

The one piece DESIGN.md + refero don't give us: a **deterministic slop linter**. Adopted
from [Impeccable](https://github.com/pbakaus/impeccable) (Apache-2.0) — the CLI only, **not
the skill** (the skill would collide with `refero-design`'s vocabulary, and refero is our
design authority for client work).

**What it is:** 44 deterministic rules, **no LLM, no API key**, JSON output, exit codes for
CI. Catches exactly our stated enemies — purple/violet gradients, Inter/overused fonts,
bounce easing, cramped padding, dark glows, low contrast, side-tab borders.

**Run it (needs Node 24+ — use nvm; system node is 22):**
```bash
nvm use 24
npx -y impeccable@latest detect <dir|file|URL>     # human-readable
npx -y impeccable@latest detect --json <path>       # CI: parse + exit code
```

**Detection power varies by target — point it at rendered output for the real check:**
- **URLs** → full Puppeteer render (strongest; run against a live dev server / built HTML).
- **HTML files** → full static HTML/CSS analysis (catches linked CSS).
- **JSX/TSX/CSS** → regex matching only (weaker; clean source can still ship slop once rendered).

**Notes:** loads local `DESIGN.md` by default and suppresses findings that match our system
(use `--no-config` to see raw hits); waive false positives with inline
`<!-- impeccable-disable <rule> -->` comments. Verified working 2026-06-28: positive-control
HTML flagged all 6 expected anti-patterns; RE dashboard `src/` came back clean.

**Canonical wrapper:** `scripts/design-qa-detect.sh <file|dir|URL>` — handles the
Node-24 guard (via nvm) and propagates Impeccable's exit code (0 clean / 2 findings /
1 blocked). Use it instead of calling `npx` directly.

**Wired into (run automatically before delivery):**
- `marp` — Stage 2.5 design-QA gate on the exported HTML.
- `openkb-deck-neon` / `openkb-deck-editorial` — gate on `output/decks/<slug>/index.html`,
  ahead of the LLM `openkb-html-critic`.
- `openkb-html-critic` — Step 0 deterministic pre-pass before its structural checklist.

Same delivery-gate discipline as PPTX QA: a deck with unresolved findings is not `reviewed`.
Per-theme caveats (waive intentional Aurora Glass `dark-glow`, editorial `overused-font`
Fraunces) are documented in each skill.

## Where this pays off in our stack

- Generative-UI ADK demos (`~/awesome-llm-apps/generative_ui_agents/`, RE dashboard fork)
  — stop them looking like default CopilotKit templates.
- `founders-build-stack` (Next.js/Supabase/Vercel) — drop `DESIGN.md` next to `COMPANY.md`.
- `marp` decks — already token-aligned with Aurora Glass.

## Related local files
- `../DESIGN.md` — our Aurora Glass design system (owned, client-safe)
- `~/.claude/skills/marp/SKILL.md` — `neon` theme, same tokens (`:root` block)
