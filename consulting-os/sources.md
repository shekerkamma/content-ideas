# CIOS Source Registry

Canonical knowledge-layer sources per `governance/decisions/CIOS-SRC-001.md`.
Pack §7 watchlists draw ONLY from this registry (plus engagement-specific
client sources). Status: **draft — slots 2–10 are proposed, awaiting owner
confirmation.**

## Tier 1 — Top-10 GitHub resources (ground truth)

| # | Resource | Status | Feeds domains | Why |
|---|----------|--------|---------------|-----|
| 1 | `OpenHands/OpenHands` + docs.openhands.dev | **CONFIRMED — PRIMARY, ALL DOMAINS** | all 9, including sap-ai-transformation | Owner decision: OpenHands is the cross-domain ground truth. Check it FIRST for every domain; other Tier-1 sources supplement it. Coverage gaps → printing-press fallback (see Acquisition tooling) |
| 2 | `google/adk-python` (Google ADK) | proposed | enterprise-agent-platforms, sap-ai-transformation | The reference agent stack (Gemini + ADK) |
| 3 | `modelcontextprotocol/*` (spec + servers) | proposed | all — integration layer | MCP is the connection standard in every reference architecture |
| 4 | `anthropics/claude-code` (+ skills repos) | proposed | ai-native-engineering, platform-engineering | Harness patterns, skills, agent-native workflows |
| 5 | `CopilotKit/CopilotKit` (AG-UI) | proposed | enterprise-agent-platforms | Generative UI layer; proven in the RE dashboard PoC |
| 6 | `Shubhamsaboo/awesome-llm-apps` | proposed | cross-domain patterns | Already cloned locally; working demo seedbed |
| 7 | `microsoft/graphrag` | proposed | enterprise-rag-knowledge | Enterprise knowledge-graph RAG reference |
| 8 | `run-llama/llama_index` | proposed | enterprise-rag-knowledge | Broadest enterprise RAG framework surface |
| 9 | `backstage/backstage` | proposed | platform-engineering, cloud-modernization | Platform engineering de-facto standard |
| 10 | `keephq/keep` | proposed | sre-aiops-transformation | Open-source AIOps/alert management reference |

## Acquisition tooling — printing-press fallback (owner decision, 2026-06-10)

When Tier-1 coverage is missing or insufficient for a needed claim, the
authorized mechanism is the **printing-press CLI pattern**: generate a
ship-ready CLI against the relevant API (printing-press skill: research →
generate → build → shipcheck) and acquire through it. Existing pp-CLI fleet
already covers firecrawl, scrape-creators (LinkedIn), hackernews, wikipedia,
substack, podscan, and more; new APIs (e.g., `api.sap.com` for OData surface,
GitHub API for repo mining) get a pp-CLI on first need. This keeps acquisition
on CLIs/APIs rather than ad-hoc scraping — consistent with the OS-wide
CLIs-over-MCP preference and CIOS-ACQ-005 (read-only, never authenticate to
client systems).

Resolution order per claim: OpenHands repo/docs → other Tier-1 registry
repos → printing-press CLI against the authoritative API → else the claim
stays **[NEEDS ACQUISITION]**.

## Tier 2 — practitioner & vendor-engineering signal

### 2a. LinkedIn posts
- **What it's for:** proof points (§4), objection material (§6), market
  sentiment (§3), adoption evidence. NOT authoritative for technical claims —
  a technical claim sourced from LinkedIn MUST be re-grounded in a Tier-1
  source before pack curation.
- **Acquisition mechanism:** existing tooling — ScrapeCreators API via the
  content-ideas scraper, `content-research` skill for individual post URLs.

### 2b. Curated YouTube channels (owner decision, 2026-06-10)
- **What it's for:** vendor-engineering deep dives — reference architectures,
  deployment patterns, capability walkthroughs straight from hyperscaler/
  vendor engineering teams. Richer technical signal than LinkedIn.
- **Role: general gap-fill.** For ANY domain, when Tier-1 repos don't cover a
  pattern, curated channels are the first gap-fill mechanism in the
  CIOS-ACQ-007 resolution order (alongside pp-CLIs for structured data).
  Expect every domain to accumulate channels here over time.
- **Confirmed channels:**

| Channel | Feeds domains |
|---------|---------------|
| SAP on Azure | sap-ai-transformation, cloud-modernization |
| SAP on AWS | sap-ai-transformation, cloud-modernization |

- **Citation rule:** video claims cite as
  `(source: <video url> @<timestamp>, <YYYY-MM>)`. Re-ground in a Tier-1
  repo/doc when one exists; where the video is the best available source for
  an architecture pattern (common for SAP-on-hyperscaler), the video citation
  MAY stand in §2/§3 with the timestamp — never for capability claims a repo
  could verify.
- **Acquisition mechanism:** `/watch` skill (frames + transcript) and
  `content-research` for full-channel ingestion. Per-video transcripts land in
  the domain inbox like any acquisition item.
- **Watchlist growth:** new channels per domain are added here first
  (registry, not per-pack drift), same rule as the GitHub set.

### 2c. Operator engineering blogs (clarification, 2026-06-10)
- **What it's for:** first-party operator metrics and delivery experience —
  the strongest proof-point class (e.g., Intercom, Atlassian, Shopify
  engineering blogs publishing their own agent-adoption numbers).
- **Rule:** citable as proof points (§4/§7) and PoV evidence with URL + date.
  Technical capability claims still re-ground in Tier 1.
- **Why added:** discovered during the first ANE backlog pass — operator
  blogs with hard revert-rate/cycle-time data are stronger evidence than
  LinkedIn posts but were unclassified. Logged in CIOS-SRC-001 amendments.

## Tier 3 — context only

Vendor marketing, analyst reports, news. May color §3 narrative; can never be
the sole citation for an `active`-pack claim.
