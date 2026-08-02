# You.com Search Plan For AI Analyst Competitor Analysis

Use this before external competitor research. The goal is repeatable source retrieval, not ad hoc search.

## API Key And Endpoint Rules

- Use `YOU_API_KEY` from the environment.
- In Hermes/Codex-on-WSL contexts, `skills/you-com-search/scripts/search.py` may also read `~/.hermes/.env`.
- Do not hardcode, print, commit, or paste the API key into run artifacts.
- Default endpoint base is `https://ydc-index.io`; override only with `YOU_BASE_URL` when intentionally testing another compatible endpoint.

## Livecrawl Naming Contract

This is the convention that prevents the known livecrawl failure:

| Layer | Correct Name |
|---|---|
| Human workflow label | `Level 2 livecrawl` |
| CLI flag | `--livecrawl` |
| Helper behavior | `--level 2` implies `--livecrawl` |
| You.com Search API query parameter | `live_crawl=true` |

Do not send these API parameter names:

- `livecrawl=true`
- `liveCrawl=true`
- `live-crawl=true`
- `live_crawl=1`

The CLI flag is intentionally `--livecrawl`, but the HTTP query parameter must be `live_crawl=true`. If a host uses an MCP/plugin instead of the local helper, choose the tool's official livecrawl option; if constructing HTTP requests directly, use `live_crawl`.

Known-safe command:

```bash
python3 skills/you-com-search/scripts/search.py \
  "<query>" \
  --level 2 \
  --out runs/<run>/working/you-com/<slug>.json
```

Before a high-stakes competitor run, or after changing `skills/you-com-search/scripts/search.py`, run the no-network regression check:

```bash
python3 skills/you-com-search/scripts/check_livecrawl_param.py
```

This must print `OK: Level 2 sends live_crawl=true`.

## Search Log

Write `outputs/search-log.md` with one row per query:

| Date | Level | Mode | Query | Output file | Purpose | Result | Follow-up |
|---|---|---|---|---|---|---|---|

Each row must state whether it was:

- Level 1 discovery seed
- Level 2 livecrawl evidence retrieval
- Level 3 research synthesis
- Level 3 finance/company synthesis
- fallback verification

If You.com fails, record the command, error class, and fallback route.

## Level Selection

- Use Level 2 by default when target, competitor, domain, or buyer arena is known.
- Use Level 1 only when discovering unknown competitors or arenas.
- Use Level 3 only for interpreted synthesis or finance/company research after source collection.
- Do not use generic web search until You.com or another approved research route has been attempted.

## Query Templates

Replace bracketed terms.

### Target Proof

```text
[target] case study onboarding implementation time ROI support productivity AI automation
[target] customers implementation proof points onboarding time support response
site:[target-domain] case study implementation onboarding ROI support automation
```

### Competitor Pricing / Packaging

```text
[competitor] pricing packaging enterprise plan implementation fee
site:[competitor-domain] pricing enterprise plan implementation professional services
[competitor] pricing user month annual contract minimum
```

### Time / Velocity

```text
[competitor] implementation time onboarding time time to value deployment duration
[competitor] case study reduced onboarding time go live faster
```

### ROI / Financial Proof

```text
[competitor] ROI payback cost savings revenue lift customer case study
[competitor] reduced cost implementation savings business impact
```

### Support Productivity

```text
[competitor] support tickets response time resolution time self service case study
[competitor] customer support productivity onboarding support volume
```

### Trust / Compliance

```text
site:[competitor-domain] SOC 2 ISO 27001 SSO audit logs security trust center
[competitor] security trust center SOC 2 ISO SAML SCIM RBAC
```

### AI / Automation

```text
[competitor] AI agent automation workflow copilot implementation orchestration
[competitor] browser automation workflow automation AI onboarding setup configuration
```

### Distribution / Market Presence

```text
[competitor] funding customers integrations partners marketplace reviews analyst
[competitor] G2 reviews integrations partner ecosystem acquisition funding
```

### Consulting / SI Benchmarks

```text
Accenture [arena] implementation automation AI transformation productivity benchmark
Deloitte [arena] implementation AI automation managed services productivity benchmark
BCG [arena] AI transformation implementation productivity benchmark
```

## Search-Again Mapping

When quality gates find a gap, run targeted Level 2 queries:

| Gap | Query Pattern |
|---|---|
| no pricing datapoints | `[competitor] pricing packaging enterprise plan implementation fee` |
| no implementation-time datapoints | `[competitor] implementation time onboarding time case study go live` |
| no trust/compliance datapoints | `site:[domain] security trust SOC 2 ISO SSO audit logs` |
| no support-productivity datapoints | `[competitor] support tickets response time resolution time self service case study` |
| weak target proof | `[target] customer case study ROI onboarding support automation` |
| consulting/SI gap | `[consulting firm] [arena] implementation AI automation productivity benchmark` |

If Level 2 returns weak/no evidence, record the gap in `outputs/data-quality-report.md` and `outputs/search-log.md`; do not invent a datapoint.

## Output Handling

- Save raw You.com JSON under `working/you-com/`.
- Convert claims into `outputs/evidence-ledger.csv`; do not paste raw JSON into client-facing decks.
- Follow important URLs into official pages, filings, docs, pricing pages, or source documents before treating a claim as high confidence.
