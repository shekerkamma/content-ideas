# Use Case Realization Structure

Each use case maps directly to the branded PPTX slide layout. Full JSON schema:
`FILE-SCHEMAS.md` (`useCases` key).

1. **Kicker + Title** — category label (`USE CASE {N}  ·  {CATEGORY}`) and a
   short noun-phrase title. Categories: `HORIZONTAL OPS`, `REVENUE`,
   `KNOWLEDGE WORK`, `ENGINEERING`, `PLATFORM`, `VERTICAL`, `TRUST`,
   `PROFESSIONAL`.
2. **Challenge** — exactly 3 bullets: the pain points this use case addresses.
3. **Solution** — exactly 3 bullets: how AI addresses each challenge.
4. **How it works** — exactly 3 numbered steps: trigger → process → outcome.
5. **Stats** — exactly 3 metric tuples: `[number/metric, label]` (e.g.,
   `["100%", "data on-prem"]`).
6. **Solution stack** — exactly 4 layers: `EXPERIENCE`, `ORCHESTRATION`,
   `CONTEXT`, `ACTUATION` — each with a one-line detail.
7. **Systems + Users** — which systems the solution touches (3–5) and the
   buyer/user personas.
8. **Organizations** — 2–4 organizations already delivering this or suggested
   prospects. Each is `[name, one-line description]` — these also feed
   `/presales-deal-prep`.
9. **Signal provenance** — link the supporting posts/comments with `signalType`
   (`demand` / `thesis` / `gap` / `trend` / `competitive_move`) and a one-line
   evidence extract.
10. **Downstream pass-throughs** — `verticalName` (exact input for
    `/vertical-scorer`), `sourceUrls` (for `/research-to-strategy`),
    `confidence` (`high` / `medium` / `exploratory`).

If OpenHands is relevant to the use case, prefer verified stack entries such as
OpenHands SDK agents, skills/repository agents, MCP transports, CLI/headless
execution, and self-hosted deployment modes rather than generic labels like
"agent orchestrator" or "custom runtime".
