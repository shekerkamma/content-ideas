# Domain Workflow Reference Implementations

Date: 2026-06-20

## Tooling Used

- GBrain recall: unavailable in this host (`list_mcp_resources` returned no resources).
- Exa/Firecrawl: not available on PATH and no related API keys were exported.
- Printing Press: installed at `/home/shekerk/go/bin/printing-press`; local library has `yc-companies`, `youtube`, and `tally`. The catalog contains a `github` API entry, but it is not installed as a local printed CLI.
- Primary-source discovery: GitHub connector and `gh api` against official repositories.

## Maintained Reference Repositories

### Anthropic Financial Services

Repository: https://github.com/anthropics/financial-services

Maintenance metadata from GitHub API:

- Default branch: `main`
- Last pushed: 2026-06-05T20:53:09Z
- Last updated: 2026-06-20T02:51:19Z
- License: Apache-2.0
- Open issues: 167
- Stars/forks at check time: 31,948 / 4,591

Implementation pattern:

- Marketplace manifest: `.claude-plugin/marketplace.json`
- Vertical plugins: reusable source-of-truth domain skills under `plugins/vertical-plugins/*/skills/*`
- Agent plugins: composed workflow agents under `plugins/agent-plugins/*`
- Managed-agent cookbooks: optional headless deployment configs under `managed-agent-cookbooks/*`
- Partner-built connectors: LSEG and S&P Global under `plugins/partner-built/*`
- Maintenance scripts:
  - `scripts/check.py` validates manifests, frontmatter, cross-file references, bundled-skill drift, and cookbook required files.
  - `scripts/sync-agent-skills.py` copies source-of-truth vertical skills into agent bundles.

Representative implemented workflows:

- Financial analysis: DCF, comps, LBO, 3-statement model, deck QC.
- Investment banking: client and market insights, pitch deck creation, transaction workflows.
- Equity research: earnings review, initiating coverage, research workflows.
- Private equity: deal sourcing, CRM integration, founder outreach.
- Wealth management: client reviews, financial planning, portfolio analysis, reporting.
- Fund administration: GL reconciliation, break tracing, accruals, roll-forwards, NAV tie-out.
- Operations: KYC document parsing and KYC/AML rules-grid evaluation.

Concrete examples:

- `plugins/agent-plugins/pitch-agent/agents/pitch-agent.md`: composes sector overview, comps, LBO, DCF, 3-statement modeling, audit, pitch deck, and deck QC into an investment banking pitch workflow.
- `plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md`: institutional DCF workflow with live Excel formulas, WACC, sensitivity tables, source comments, and recalculation requirements.
- `plugins/vertical-plugins/operations/skills/kyc-rules/SKILL.md`: KYC/AML rules-grid scoring with explicit trusted/untrusted data separation and human-review routing.
- `managed-agent-cookbooks/pitch-agent/agent.yaml`: optional managed/headless config with CapIQ and Daloopa MCP servers, skill bundle, and callable subagents.

### Anthropic Life Sciences

Repository: https://github.com/anthropics/life-sciences

Maintenance metadata from GitHub API:

- Default branch: `main`
- Last pushed: 2026-05-08T16:54:54Z
- Last updated: 2026-06-19T20:56:13Z
- Repo-level license metadata: null
- Open issues: 18
- Stars/forks at check time: 466 / 90

Implementation pattern:

- Marketplace manifest: `.claude-plugin/marketplace.json`
- Remote MCP connectors: PubMed, BioRender, Synapse, Wiley Scholar Gateway, Consensus, Cortellis, AdisInsight, bioRxiv/medRxiv, ClinicalTrials.gov, ChEMBL, Open Targets, Owkin, Medidata.
- Local MCPB connectors: 10x Genomics Cloud, ToolUniverse.
- Skills: domain workflow folders with `SKILL.md`, references, scripts, assets, and per-skill licenses.

Representative implemented workflows:

- `single-cell-rna-qc`: scRNA-seq QC for `.h5ad` and 10x `.h5`, with MAD-based filtering and visualization scripts.
- `clinical-trial-protocol-skill`: waypoint-based clinical trial protocol workflow with research-only and full-protocol modes, ClinicalTrials.gov MCP requirement, FDA database routing, template assets, and sample-size script.
- `nextflow-development`: nf-core pipeline workflow for RNA-seq, Sarek, and ATAC-seq, including environment checks, GEO/SRA acquisition, samplesheet generation, test profile, run, and output verification.
- `instrument-data-to-allotrope`: lab instrument data conversion to Allotrope ASM JSON/CSV with native Allotropy-first parsing, fallback parsing, parser export, and ASM validation.
- `scvi-tools`: model-selection and execution workflows for scVI, scANVI, totalVI, PeakVI, MultiVI, DestVI, veloVI, sysVI, with reusable scripts.
- `scientific-problem-selection`: research strategy/problem-selection framework.

Important caveat:

- Repo-level license metadata is null. Several skill folders include `LICENSE.txt`, but reuse should check the specific folder license before copying content.

## OpenHands Findings

Repositories checked:

- https://github.com/OpenHands/OpenHands
- https://github.com/OpenHands/software-agent-sdk
- https://github.com/OpenHands/agent-canvas
- https://github.com/OpenHands/automation
- https://github.com/OpenHands/extensions

Maintenance metadata from GitHub API:

- `OpenHands/OpenHands`: pushed 2026-06-19, updated 2026-06-20, license `NOASSERTION`
- `OpenHands/software-agent-sdk`: pushed 2026-06-20, updated 2026-06-20, MIT
- `OpenHands/agent-canvas`: pushed 2026-06-20, updated 2026-06-20, MIT
- `OpenHands/extensions`: pushed 2026-06-19, updated 2026-06-19, MIT

What OpenHands provides:

- Agent Canvas: self-hosted control center for coding agents and automations.
- Software Agent SDK: Python/REST APIs for agents that work with code, local or ephemeral workspaces.
- Automation service: scheduled and event-driven automations with run history.
- Skills/microagents: markdown instructions loaded from public skills or repository-specific `.openhands/skills` / `.openhands/microagents`.
  - Conceptually, these are the OpenHands equivalent of domain/task expertise packs: specialized prompts that encode domain-specific knowledge, repository-specific context, and task-specific workflows.
  - They can absolutely be industry-specific when a team writes finance, healthcare, legal, scientific, or operations microagents.
- MCP routing/proxying: example includes Tavily MCP proxy and Git provider MCP tools.
- Extensions marketplace: public registry with 58 extensions at check time.

OpenHands domain-workflow result:

- Searches across OpenHands repos and the extensions registry found no maintained public finance, healthcare, life-sciences, legal, or banking microagent packs comparable to Anthropic's financial-services/life-sciences repositories.
- OpenHands should be treated as a runtime, SDK, automation layer, and microagent/skill substrate. It can host industry microagents, but the public OpenHands org does not currently appear to be the best source of finance/life-sciences vertical content.
- One exception adjacent to domain modernization is `cobol-modernization` under `OpenHands/extensions` large-codebase marketplace, which is enterprise modernization rather than finance/life-sciences domain workflow.

## Implication For `launch-domain-specific-workflow`

The skill should not generate domain workflows from scratch as its first move.

Recommended design:

1. Discover maintained reference packs first:
   - Anthropic vertical marketplaces: `financial-services`, `life-sciences`
   - OpenHands extensions/runtime repos for reusable microagents, execution substrate, and generic automations
   - Project-specific OpenHands `.openhands/microagents` / `.openhands/skills` folders when a target repo already encodes its own domain workflow
   - Other official domain repositories as discovered
2. Verify maintenance and license:
   - GitHub API metadata
   - repo-level and folder-level licenses
   - CI/check scripts
   - current issue/activity state
3. Select reusable assets:
   - `SKILL.md`
   - `references/`
   - `scripts/`
   - `assets/`
   - MCP connector manifests
   - validation/eval scripts
4. Adapt only the wrapper:
   - runtime: Codex, Claude Code, OpenHands, local CLI, GitHub Actions, cron, service worker
   - connectors: local MCP URLs, CLI auth, env vars
   - memory/logs: repo run folders, GBrain if available, local DB if needed
5. Preserve provenance:
   - source repo, commit/date checked, license, copied/adapted files, validation commands
6. Validate before declaring usable:
   - static manifest checks
   - script smoke tests
   - domain-specific QA script if available
   - explicit missing-tool report

The right framing is: launch a domain-specific workflow pack by adapting proven skills, connectors, scripts, and validations to the local runtime. Managed agents are optional deployment packaging, not the core idea.

## Key Source Links

- Anthropic financial-services: https://github.com/anthropics/financial-services
- Financial marketplace manifest: https://github.com/anthropics/financial-services/blob/main/.claude-plugin/marketplace.json
- Pitch agent: https://github.com/anthropics/financial-services/blob/main/plugins/agent-plugins/pitch-agent/agents/pitch-agent.md
- DCF skill: https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/financial-analysis/skills/dcf-model/SKILL.md
- KYC rules skill: https://github.com/anthropics/financial-services/blob/main/plugins/vertical-plugins/operations/skills/kyc-rules/SKILL.md
- Financial check script: https://github.com/anthropics/financial-services/blob/main/scripts/check.py
- Anthropic life-sciences: https://github.com/anthropics/life-sciences
- Life-sciences marketplace manifest: https://github.com/anthropics/life-sciences/blob/main/.claude-plugin/marketplace.json
- Single-cell RNA QC skill: https://github.com/anthropics/life-sciences/blob/main/single-cell-rna-qc/SKILL.md
- Clinical trial protocol skill: https://github.com/anthropics/life-sciences/blob/main/clinical-trial-protocol-skill/SKILL.md
- Nextflow skill: https://github.com/anthropics/life-sciences/blob/main/nextflow-development/SKILL.md
- Instrument data to Allotrope skill: https://github.com/anthropics/life-sciences/blob/main/instrument-data-to-allotrope/SKILL.md
- scvi-tools skill: https://github.com/anthropics/life-sciences/blob/main/scvi-tools/SKILL.md
- OpenHands: https://github.com/OpenHands/OpenHands
- OpenHands extensions: https://github.com/OpenHands/extensions
- OpenHands software-agent-sdk: https://github.com/OpenHands/software-agent-sdk
- OpenHands agent-canvas: https://github.com/OpenHands/agent-canvas
- OpenHands automation: https://github.com/OpenHands/automation
