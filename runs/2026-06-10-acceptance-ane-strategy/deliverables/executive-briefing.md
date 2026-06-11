# AI-Native Engineering Strategy — Executive Briefing

**Prepared for:** 400-developer enterprise software organization (CIOS acceptance scenario)
**Date:** 2026-06-10 · **Status:** draft (pack v0.1 `draft`; freshness gate per CIOS-GOV-001)
**Domain pack:** ai-native-engineering v0.1 · **Sources:** cited inline per CIOS-GOV-002

## The question

What should our AI-native engineering strategy be?

## The answer in three sentences

Stop optimizing for which model or copilot to buy and start building the two
things that compound: **owned engineering context** (specs, skills, routing,
memory that any agent host can run) and **an earned-autonomy operating
model** (agents progress from assisted to gated-autonomous work only as
governance and evidence allow). Anchor the platform decision on an open,
MIT-licensed agent layer you can own — OpenHands runs from laptop CLI to
self-hosted Kubernetes in your VPC (source: github.com/OpenHands/OpenHands
README; docs.openhands.dev, 2026-06) — while keeping interactive work on
commercial harnesses. Run a 90-day gated pilot now; scale by maturity rung,
not by tool rollout.

## Where you are — and where this goes

The adoption ladder (pack §5): **1 Copilot → 2 Agent-assisted → 3
Agent-executed (gated) → 4 Agent-native delivery → 5 Compounding system.**
A 400-developer org with copilot seats sits at rung 1–2. The strategy below
targets rung 3 in 90 days and rung 4 within 12 months, with rung 5 as the
durable-IP end state: your specs, skills, and context as versioned
engineering assets.

## Strategy pillars

1. **Context over model choice.** Models are engine swaps; folders-and-files
   context is portable across Claude Code, Codex, and OpenHands — OpenHands
   even defines sub-agents as plain Markdown files (source:
   docs.openhands.dev/sdk/guides/agent-file-based.md, 2026-06).
2. **Spec-driven development.** Agents scale past toy tasks when an
   execution-grade spec removes architectural ambiguity (Constitution §16
   pattern). Specification discipline becomes the senior-engineer skill.
3. **Earned autonomy, keys not prompts.** Write actions live behind
   confirmation policies and sandboxes — OpenHands ships action-security
   analysis, Docker/Apptainer sandboxing, and org roles/permissions (source:
   docs.openhands.dev security + organizations docs, 2026-06).
4. **Own the platform layer.** MIT-licensed core (except `enterprise/`),
   multi-LLM, SDK/CLI/Cloud/Enterprise deployment modes — the buy-vs-build
   calculus favors owning your agent layer the way you own CI (source:
   github.com/OpenHands/OpenHands README, 2026-06).

## Reference architecture (pack §4A)

- **Execution:** OpenHands — SDK for codified agents, CLI for interactive,
  Enterprise Helm/K8s install in your VPC for unattended work (source:
  docs.openhands.dev/enterprise, 2026-06)
- **Context:** repo-based brain — routing files, skills, specs, memory
- **Integration:** MCP servers for live systems (documented: SDK MCP guide +
  CLI server management), scoped service accounts
- **Governance:** roles/permissions, sandbox isolation, confirmation
  policies, token/budget caps on unattended runs
- **Hybrid harness:** interactive on subscription tools; unattended on owned
  infra where audit and budget control live (pack §4B)

## 90-day pilot (rung 3, gated)

- **Select** 2–3 workstreams via the pilot rubric: scoped repo, objective
  done-definition, read-mostly risk, measurable cycle time, existing tests.
  PR review automation and TODO implementation are documented OpenHands
  GitHub-workflow patterns (source: docs.openhands.dev github-workflows,
  2026-06) — natural first candidates.
- **Gate:** agents propose, tests + humans dispose; least-privilege keys;
  sandboxed execution; caps on every unattended run.
- **Measure:** cycle time, review throughput, defect escape rate against a
  pre-pilot baseline (pack §7 value drivers; benchmark numbers
  [NEEDS ACQUISITION] — to be baselined in-house during the pilot).

## Risks we are explicitly managing

Ungoverned write access · cost runaway on unattended runs · context rot ·
vendor lock-in · safeguard friction on newest models (pin versions for
unattended jobs). Mitigations per pack §8.

## Decision requested

Approve the 90-day gated pilot and the context-infrastructure workstream
(the second brain your agents — and consultants — will run on). Platform
deployment-mode selection (Cloud vs self-hosted Enterprise) follows the
pilot's data-residency findings.

---
*Traceability (CIOS-MM-005): registry source (OpenHands) → inbox item
2026-06-10-openhands-docs-delta → domain ai-native-engineering → pack v0.1 →
asset reference-architecture-owned-agent-platform → this output.*
