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

## Where this pays off in our stack

- Generative-UI ADK demos (`~/awesome-llm-apps/generative_ui_agents/`, RE dashboard fork)
  — stop them looking like default CopilotKit templates.
- `founders-build-stack` (Next.js/Supabase/Vercel) — drop `DESIGN.md` next to `COMPANY.md`.
- `marp` decks — already token-aligned with Aurora Glass.

## Related local files
- `../DESIGN.md` — our Aurora Glass design system (owned, client-safe)
- `~/.claude/skills/marp/SKILL.md` — `neon` theme, same tokens (`:root` block)
