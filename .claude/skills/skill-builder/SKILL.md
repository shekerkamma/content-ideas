---
name: skill-builder
description: Use when creating a new project skill, auditing or improving an existing skill, retrofitting skill relationship patterns, or checking Claude/Codex/OpenHands host compatibility. Auto-detects whether to build, audit, or fix based on whether a SKILL.md already exists. Also triggers on "help me build a skill", "audit this skill", "fix skill relationships", "skill doesn't trigger", "split this skill", "make this skill cross-host", and "will this work in Codex and Claude".
argument-hint: [skill-name or path]
---

## What This Skill Does

Builds, audits, and improves project skills following Anthropic's official best practices and this repo's Claude/Codex/OpenHands compatibility rules.
One unified workflow -- no mode selection needed. Auto-detects the situation and adapts.

For the complete technical reference (frontmatter fields, advanced patterns, hooks, permissions),
see [reference.md](reference.md).

---

## Step 0 — Auto-Detect

Check whether a skill already exists at the path or name given in `$ARGUMENTS`:

```bash
ls .claude/skills/$ARGUMENTS/SKILL.md 2>/dev/null || \
ls .agents/skills/$ARGUMENTS/SKILL.md 2>/dev/null || \
ls skills/$ARGUMENTS/SKILL.md 2>/dev/null || \
ls ~/.claude/skills/$ARGUMENTS/SKILL.md 2>/dev/null || \
find . -path "*skills/$ARGUMENTS/SKILL.md" 2>/dev/null | head -1 || \
echo "NOT_FOUND"
```

Route based on result:

| State | What to do |
|---|---|
| File found, complete | Audit + Fix — jump to Audit Framework |
| File found, incomplete | Continue Build — jump to Step 3 of Discovery |
| NOT_FOUND | New Build — run full Discovery Interview |
| No `$ARGUMENTS` | Ask: "Building a new skill or auditing an existing one? If existing, what's the name or path?" |

---

## New Build — Discovery Interview

Ask one round at a time via AskUserQuestion. Move forward only after the user answers.
Skip any round already answered by their initial message.

**Round 1 — Goal & Name**
- What does this skill do? What problem does it solve?
- What should we call it? (suggest: lowercase, hyphens, max 64 chars)

**Round 2 — Trigger**
- What would someone say to trigger this? (2–3 natural phrases)
- User-only `/slash`, Claude-auto-invocable, or both?
- Does it accept arguments? If so, what?
- Which host(s) must discover it: Claude Code, Codex/OpenAI, OpenHands, or shared?
- What is the canonical location: `.claude/skills/`, `.agents/skills/`, `skills/`, or a mirrored pair?

**Round 3 — Process**
- Walk me through exactly what happens, step by step, from trigger to output.
- For each step: does Claude do it directly, or delegate to a subagent/script?
- Conversational (back-and-forth) or fire-and-forget?

**Round 4 — Inputs, Outputs & Dependencies**
- What inputs does it need? (files, API responses, user args, live data)
- What does it produce? Where do outputs go?
- External APIs, scripts, or tools required?
- Does it depend on other skills being run first?
- Which host-specific tools or MCP servers does it rely on, and what is the fallback in the other host?

**Round 5 — Guardrails & Edge Cases**
- What could go wrong? Common failure modes?
- What should this skill NOT do? Any hard limits?
- Cost concerns? (API calls, AI generation)
- Ordering constraints?
- Host compatibility risks? (Claude-only frontmatter, Codex tool-name mapping, OpenHands path conventions, generic web fallback)

**Round 6 — Relationship Scan**
Before writing, ask about each pattern:
- Does any other skill produce output this skill consumes? → Sequential upstream
- Does this skill's output feed another skill? → Sequential downstream
- Are there alternative skills that do the same job differently? → Peer
- Does this skill call other skills as sub-tasks? → Orchestrator
- Does it modify HOW another skill runs? → Behavioral overlay
- Should its output be improvable by another skill? → Amplifier
- Must another skill run first as a gate? → Prerequisite
- Does it activate when another skill fails? → Fallback
- Are there sibling skills in the same domain? → Domain cluster

**Round 7 — Confirm**
Summarize in the format below and ask "Does this capture it?". Only build after confirmation.

```
## Skill Summary: [name]
Goal: [one sentence]
Trigger: `/name` + [natural language phrases]
Arguments: [what it accepts, or "none"]
Process: [numbered steps]
Inputs: [what it reads]
Outputs: [what it produces + where]
Dependencies: [APIs, scripts, other skills]
Guardrails: [what can go wrong, hard limits]
Relationships: [patterns found in Round 6]
Host compatibility: [Claude/Codex/OpenHands target + discovery path + fallback rules]
```

---

## Audit Framework

**Read the skill file completely before running any check.**
Never audit a skill you haven't read in full.

### A — Frontmatter

- [ ] `name` matches the directory name
- [ ] `description` is trigger-focused — written for the model, not humans ("Use when someone asks to X")
- [ ] `description` keywords match what users naturally say
- [ ] `disable-model-invocation: true` set if skill has side effects or costs money
- [ ] `argument-hint` set if skill accepts arguments
- [ ] `allowed-tools` set if skill needs restricted access
- [ ] `context: fork` used only for self-contained tasks that don't need conversation history
- [ ] `permissions.env` declared if skill requires API keys or env vars (enables pre-flight check; fails fast with a clear message instead of a mid-run 401)
- [ ] `permissions.network` declared if skill calls external APIs or localhost services (enables sandbox enforcement and user transparency)
- [ ] `permissions.file_read` / `permissions.file_write` declared if skill reads or writes outside the skill directory (scope declaration for cross-host safety)
- [ ] No unnecessary fields added

### B — Category Fit (Anthropic's 9 categories)

Identify which single category this skill belongs to.
Flag if it straddles multiple — that means it should be split.

| Category | Signs it belongs here |
|---|---|
| Library / API Reference | Documents a CLI, SDK, or API with edge cases and gotchas |
| Product Verification | Testing, validation, QA workflows |
| Data & Analysis | Connects to data stacks, produces structured analysis |
| Business Automation | Workflow automation with dependencies on other skills |
| Scaffolding & Templates | Boilerplate generation, project setup, framework starters |
| Code Quality & Review | Review, lint, style enforcement |
| CI/CD & Deployment | Build, test, deploy pipelines |
| Runbook | Multi-tool investigation → structured report |
| Infrastructure Ops | Routine maintenance, safety guardrails |

- [ ] Skill fits ONE category cleanly
- [ ] If straddling 2+: flagged for split into separate skills

### C — Content Quality

- [ ] SKILL.md is under 500 lines (detailed reference moved to supporting files)
- [ ] Numbered step-by-step workflow — no vague or abstract instructions
- [ ] Output format specified with templates or file path examples
- [ ] All file paths documented (inputs, outputs, scripts)
- [ ] `## Gotchas` section present — what NOT to do, common failure points
- [ ] Supporting files referenced from SKILL.md (not orphaned)
- [ ] Avoids railroading — gives Claude information + flexibility, not over-prescribed steps
- [ ] `$ARGUMENTS` / `$N` used where the skill takes dynamic input

### D — Relationship Patterns

Scan the skill body for each pattern. Document what's found.

| Pattern | Detection Question |
|---|---|
| **Sequential** | Does it consume another skill's output file? Does it produce a file another skill reads? |
| **Parallel / Complement** | Could it run alongside another skill on the same input for different outputs? |
| **Orchestrator** | Does it invoke other skills as sub-tasks? |
| **Behavioral Overlay** | Does it modify HOW another skill runs, not what it produces? |
| **Alternative / Peer** | Is there another skill doing the same job with a different approach? |
| **Fallback** | Does it activate when another skill fails or is unavailable? |
| **Prerequisite / Gate** | Must another skill run before this one? |
| **Amplifier** | Does it take another skill's output and improve it? |
| **Domain Cluster** | Are there sibling skills in the same vertical or domain? |

- [ ] All found relationships documented in `## Skill Relationships` section
- [ ] Each relationship names the handoff artifact (file path + format)
- [ ] Runtime preamble surfaces relationships to user at invocation
- [ ] "None" stated explicitly if no relationships exist (not just omitted)

### E — Progressive Disclosure

- [ ] Long reference content lives in supporting files, not SKILL.md
- [ ] Stuck/error scenarios have their own files (e.g., `troubleshoot.md`, `stuck-jobs.md`)
- [ ] SKILL.md tells Claude what supporting files exist and when to read them

### F — Host Compatibility

Decide whether the skill is Claude-only or shared. Do not assume a `.claude/skills/` skill is automatically visible to Codex/OpenHands.

- [ ] Target host(s) declared: Claude Code, Codex/OpenAI, OpenHands, or shared
- [ ] Discovery path documented: `.claude/skills/<name>/`, `.agents/skills/<name>/`, `skills/<name>/`, or mirrored paths
- [ ] Canonical source of truth named if the skill is mirrored across host roots
- [ ] Claude-only frontmatter (`argument-hint`, `allowed-tools`, `context`, `hooks`, `disable-model-invocation`) treated as an enhancement, not the only safety mechanism
- [ ] Claude tool names mapped or written in host-neutral language (`Read`, `Edit`, `Bash`, `AskUserQuestion`, `Task`)
- [ ] Source/tool order is explicit for strategy, research, deck, or pipeline skills: local references, GBrain/memory, preferred research plugins, official sources, generic web fallback last
- [ ] Required MCP/tool fallbacks are documented when one host lacks the preferred tool
- [ ] Output paths and write-back rules use repo-relative paths or env vars, not one-host assumptions

---

## Build / Fix Phase

After Discovery (new) or Audit (existing), apply changes.

**For new skills:** Write full SKILL.md using Standard Templates below.

**For existing skills:** Surgical edits only — fix what the audit flagged, don't rewrite what works.

**Always apply if missing:**
1. `## Skill Relationships` section
2. `## Gotchas` section
3. Category label in `## Skill Relationships`
4. Fix `description` if it's a human-readable summary instead of trigger-focused
5. Runtime preamble if relationships exist but aren't surfaced at invocation
6. `## Host Compatibility` section for any skill expected to work outside one host
7. Flag for split if category straddle found
8. `permissions:` frontmatter block if skill calls any external API, requires env vars, or writes outside its own directory (see Permissions Frontmatter Block template)

---

## Standard Templates

### Skill Relationships Block

```markdown
## Skill Relationships

### Category
[One of the 9 Anthropic categories]

### Dependencies
Skills that must be installed for this skill to work (none if standalone):
- `skill-name` — [why required]

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `skill-a` | Sequential upstream | always | path/to/file.json |
| `skill-b` | Alternative / Peer | if output format is markdown | — |
| `skill-c` | Behavioral overlay | always-on | — |
| `skill-d` | Fallback | if primary tool unavailable | — |
| `skill-e` | Amplifier | optional post-processing | output/*.html |

### Runtime Preamble
[What this skill says to user at invocation about relevant relationships]
Example: "Have you run /skill-a first? It produces X that I'll use as input.
Alternatives for this job: /skill-b (markdown output), /skill-c (PDF output)."
```

### Permissions Frontmatter Block

Use when a skill calls external APIs, requires credentials, or writes outside its own directory.
Declare only what applies — omit the block entirely for skills that are purely read/local.

```yaml
---
name: skill-name
description: Use when...
permissions:
  env:
    - REQUIRED_API_KEY        # fails fast if missing; user sees what's needed before first run
    - OPTIONAL_KEY            # document optional vars here too
  network:
    - https://api.example.com # declared endpoints; sandbox-enforced on hosts that support it
    - http://localhost:8000   # local services need explicit declaration too
  file_read:
    - path/to/input/          # paths outside skill dir that this skill reads
  file_write:
    - path/to/output/         # paths this skill writes; "/tmp/" is always safe to declare
    - /tmp/
  shell:
    allowed_scripts:
      - scripts/helper.py     # only declare scripts this skill explicitly runs
---
```

**Which skills need this:** any skill with `SCRAPECREATORS_API_KEY`, `EXA_API_KEY`, GBrain MCP,
Higgsfield, Firecrawl, or any `http://localhost:*` dependency. Purely local/read-only skills can omit.

---

### Gotchas Block

```markdown
## Gotchas

- **[Common failure mode]:** [What goes wrong and how to avoid it]
- **Never:** [Hard constraint — what not to do and why]
- **Watch out for:** [Edge case — when normal instructions break]
```

### Host Compatibility Block

```markdown
## Host Compatibility

### Target Hosts
- Claude Code: [yes/no] — discovery path: `.claude/skills/<skill-name>/SKILL.md`
- Codex/OpenAI: [yes/no] — discovery path: `.agents/skills/<skill-name>/SKILL.md` or `skills/<skill-name>/SKILL.md`
- OpenHands: [yes/no] — discovery path: `.agents/skills/<skill-name>/SKILL.md`

### Canonical Source
[Name the source of truth if mirrored; e.g., `.claude/skills/<skill-name>/` mirrors to `.agents/skills/<skill-name>/`.]

### Tool Mapping
- Claude `Read` / `Grep` / `Glob` -> Codex shell reads / `rg`
- Claude `Edit` / `MultiEdit` -> Codex `apply_patch`
- Claude `Bash` -> Codex shell command
- Claude `AskUserQuestion` -> Codex concise chat question or repo AGENTS numbered choices
- Claude `Task` / subagent -> Codex main-thread execution or available multi-agent tools

### Source / Tool Order
1. Read this `SKILL.md` and required references first.
2. Use local repo artifacts and prior run files before external research.
3. Use GBrain or durable memory when available for recurring entities, verticals, and prior strategy work.
4. Use preferred research plugins / MCPs / official docs before generic web search.
5. Use generic web search only as fallback or official-source verification.
6. Write durable findings back only when the skill's workflow calls for it.
```

### Skill File Structure

```
skill-name/
  SKILL.md              ← Main instructions (<500 lines)
  reference.md          ← Detailed docs, full field reference
  examples/
    good.md             ← Positive examples Claude should match
    avoid.md            ← Anti-patterns Claude must never produce
  troubleshoot.md       ← What to do when stuck
  scripts/
    helper.py           ← Utility scripts
    test_host_compatibility.py
```

---

## After Fixing

1. Update CLAUDE.md entry if skill name, trigger phrases, or output location changed
2. Test natural language trigger AND `/skill-name` direct invocation
3. If split into two skills: write CLAUDE.md entries for both, remove the old entry
4. If relationships added: verify every named handoff artifact exists at its documented path
5. If `description` changed: confirm the new wording triggers in at least 2 different phrasings
6. If cross-host: verify the skill is discoverable from each intended host root or document the missing mirror

---

## Notes

- Read before you write. Always read an existing skill before auditing or modifying it.
- Category straddle = two skills sharing one file. Split it, don't patch it.
- Gotchas is the highest-signal section per Anthropic. Never skip it.
- Descriptions are for the model, not humans — trigger conditions, not summaries.
- Don't railroad. Provide information + flexibility. Over-prescribed steps break on edge cases.
- Progressive disclosure: SKILL.md is the hub. Detail lives in supporting files loaded on demand.
- "None" in Relationships is valid — state it explicitly so future audits know it was checked.
- `skill-builder` and Codex's system `skill-creator` are peers, not replacements. Use `skill-builder` for project-local Claude/OpenHands/Codex portability audits; use `skill-creator` for Codex-native skill authoring.

---

## Host Compatibility

### Target Hosts
- Claude Code: yes -- primary project-local discovery path is `.claude/skills/skill-builder/SKILL.md`.
- Codex/OpenAI: yes -- compatible guidance, but Codex auto-discovery requires a mirror or wrapper under `.agents/skills/skill-builder/` or explicit AGENTS routing.
- OpenHands: yes -- compatible guidance for OpenHands-style `.agents/skills/<name>/SKILL.md` project skills.

### Canonical Source
The canonical source for this project skill is `.claude/skills/skill-builder/`. If mirrored into `.agents/skills/skill-builder/`, keep this file as the source of truth and copy only reviewed updates.

### Tool Mapping
- Claude `Read` / `Grep` / `Glob` -> Codex shell reads / `rg`
- Claude `Edit` / `MultiEdit` -> Codex `apply_patch`
- Claude `Bash` -> Codex shell command
- Claude `AskUserQuestion` -> Codex concise chat question, or numbered choices when repo AGENTS requires it
- Claude `Task` / subagent -> Codex main-thread execution, unless a multi-agent tool is explicitly available

### Source / Tool Order
1. Read the target skill and its references before auditing.
2. Use repo-local artifacts and prior run files before external research.
3. Use GBrain or durable memory when available for recurring entities, verticals, prospects, or prior strategy work.
4. Use preferred research plugins / MCPs / official docs before generic web search.
5. Use generic web search only as fallback or official-source verification.
6. Keep `skill-creator` separate: do not rewrite Codex-native skill authoring rules to match this Claude-first project skill.

---

## Skill Relationships

### Category
Scaffolding & Templates

### Dependencies
Skills that must be installed for this skill to work (none if standalone):
- None — standalone auditor/builder for skill files.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `skill-creator` | Alternative / Peer | use for Codex-native system skill authoring instead of project-local skill-builder audits | — |
| `skill-starter-template` | Sequential downstream | use when creating a new project-specific skill after manual workflow validation | `.agents/skills/<skill-name>/SKILL.md` |
| `karpathy-guidelines` | Behavioral overlay | during implementation edits to keep changes surgical and verified | — |

### Runtime Preamble
I'm using `skill-builder` for project-local skill build/audit work, including Claude/Codex/OpenHands compatibility. Codex's `skill-creator` is a separate peer workflow for Codex-native skills, not a replacement for this project-local audit path.

---

## Gotchas

- **Wrong root:** `.claude/skills/<name>/` is not automatically discoverable by Codex/OpenHands. Cross-host skills need a mirror, wrapper, or explicit AGENTS routing.
- **Frontmatter false safety:** Claude-specific fields such as `allowed-tools`, `hooks`, and `disable-model-invocation` may not be enforced by other hosts. Put essential safety rules in the skill body too.
- **Tool-name drift:** Claude tool names are not portable by themselves. Include host-neutral wording or a tool mapping when a skill must run in Codex/OpenHands.
- **Generic search fallback:** Strategy/research skills must name source/tool order. Generic web search belongs last unless the user explicitly asks for it or official current verification is required.
