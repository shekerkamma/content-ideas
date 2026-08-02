# Genspark video-to-deck contract

This is the canonical cross-host contract for the compound chain:

```text
watch / transcript + scene-complete hyperframes
→ evidence and context packet
→ Genspark AI Slides generation or same-project expansion
→ headed-browser recovery
→ branded rebuild
→ native or accurately labelled hybrid PowerPoint
→ content, visual, editability, and Office QA
```

`video-to-deck`, `genspark-slides`, and `genspark-branded-deck` must follow this
contract. Resolve it from the installed sibling skill at
`../pptx-visual-spec/references/genspark-video-deck-contract.md`; in the source
repository use `skills/pptx-visual-spec/references/genspark-video-deck-contract.md`.

## 1. Source and evidence contract

For a video source, do not build the story from a capped keyframe sample.

1. Capture with `watch --detail scene-complete --resolution 1280` or a host
   equivalent that samples densely and deduplicates screens without a fixed cap.
2. Preserve the full transcript with timestamps. Empty or unavailable transcript
   blocks generation because visual states alone cannot establish the argument.
3. Write a screen manifest with one record per retained state: timestamp, frame,
   screen group, observed state, evidence role, and disposition.
4. Record `distinct_screen_count` and `max_gap_seconds`. Inspect large gaps; they
   are acceptable for presenter-only stretches but suspicious in active demos.
5. Map every meaningful transcript beat and screen group to a slide, a grouped
   duplicate, an authored visual, or an explicit skip reason.

Hyperframes and transcript have different jobs:

- Transcript establishes what was said, why it matters, caveats, and sequence.
- Hyperframes establish which screens actually appeared, their exact state, and
  whether the deck covers the demonstrated workflow.
- The coverage matrix joins both. Neither replaces the other.

## 2. Rich-context gate

Before calling a remote slide generator, write `<run>/genspark-context-packet.md`.
It must contain:

- audience, decision, BLUF, tension, narrative arc, and desired action;
- timestamped transcript sections and claim status;
- screen groups, representative timestamps, observed UI states, and disposition;
- a slide-to-evidence matrix with assertion title, content, visual state, caveat,
  implication, transcript evidence, and frame evidence;
- allowed numbers and named entities, plus unsupported or sensitive values that
  must not appear;
- brand/design direction and requested editability route;
- the evidence-driven slide-count policy below.

Paste the substantive packet into the connector requirements. A local path is not
remote context. A short outline, transcript summary, or list of chapter names does
not pass this gate.

## 3. Slide-count contract

Slide count is an output of evidence coverage and legibility, not a production
constraint.

- Treat a requested or generated count as a minimum or planning estimate unless
  the user explicitly states a hard maximum.
- Split distinct UI states, setup steps, proofs, caveats, or decisions when one
  slide would become crowded.
- One slide per meaningful captured state is acceptable.
- Complete only when every coverage row has a slide/disposition and the rendered
  slide is legible. Endpoint count alone is not completion.
- If Genspark compresses or omits coverage, update the same project with a precise
  expansion request. Do not create a new project unless the user requests a new
  concept or the existing project is irrecoverably corrupt.

## 4. Hosted-generation contract

Use Genspark as an upstream storyline and visual-concept surface, not the system
of record for facts or the final guarantee of editability.

- Keep the project ID and viewer URL in `genspark-handoff.json`.
- Do not infer a credit failure from slow generation, generic quota CSS/assets,
  anonymous-viewer console noise, or an incomplete first capture.
- Classify `blocked_credit_limit` only when the UI/API explicitly reports credit,
  quota, billing, or upgrade exhaustion.
- If the viewer says it is building/editing slides or has tasks remaining, classify
  `generating`, wait, and retry recovery from the same viewer.
- A connector failure does not stop local delivery when validated source content
  exists. Record the hosted status and continue through the local branded builder.

## 5. Playwright and browser contract

### Browser lanes

| Need | Preferred lane |
|---|---|
| Remote Genspark generation | Host connector/app when available |
| Public or connector-returned viewer | Headed Playwright Chromium first |
| Viewer requiring existing sign-in | Windows-native authenticated Chrome/DevTools or host-native headed browser |
| Recovered local HTML rendering | Headless Playwright/Chromium |

Headed recovery is mandatory before declaring a Genspark viewer unreachable.
Shell DNS and the browser can use different resolver paths.

### Recovery sequence

1. Open the exact returned viewer URL in headed Chromium.
2. Click `View` or the presentation artifact when the conversation wrapper is shown.
3. Observe `/api/files/s/<id>?pageIndex=<n>` requests and recover them at `scale=1`.
4. Use arrow navigation and controlled scrolling to force lazy slide requests.
5. Save `manifest.json`, `viewer-state.json`, a screenshot, and diagnostics.
6. Require the evidence-derived minimum with `--min-slides`; retry the same project
   when generation is still progressing.

Canonical command:

```bash
node scripts/capture_genspark_slides.mjs \
  --url "<viewer-url>" \
  --out "<run>/genspark-source" \
  --headed \
  --min-slides "<evidence-derived-minimum>"
```

### WSL and sandbox failures

- `ERR_NAME_NOT_RESOLVED`: verify current public DNS, then rerun the same headed
  command with `--doh-template "https://dns.google/dns-query{?dns}"`.
- If Chromium still fails, use a current DoH A record with a process-scoped
  `--host-resolver-rules`; never store a transient IP in the repository.
- Browser launch errors mentioning Linux sandbox host, `Operation not permitted`,
  GUI denial, or cache access: rerun through the host's approved GUI/unsandboxed
  execution path. Do not weaken the browser or rewrite system networking as a fix.
- Windows Chrome listening on `127.0.0.1:9222` is not necessarily reachable from
  WSL loopback. Run the DevTools client on Windows or expose a deliberate bridge.
- Do not copy Windows browser profiles or cookies into Linux. Keep the browser and
  encrypted cookie store on the same OS.
- Do not automate around Google/Genspark bot or sign-in controls. Ask the user to
  authenticate in a normal headed browser when required.

Read `genspark-slides/references/wsl-execution-blockers.md` for diagnostics.

## 6. Factual-integrity contract

Genspark output is untrusted draft content until checked against the packet.

If `slide-plan.json` has claims with `evidence_ids`, run `pptx-design-quality`'s
`check_claim_evidence.py` first as a fast mechanical pre-pass for the first bullet
below (unsourced numbers) — it does not replace the full manual scan that follows,
which also covers URLs, provider/model names, and simulated-UI states this
deterministic script cannot check.

- Scan every visible number, URL, provider/model name, version, price, hardware
  specification, performance metric, completion percentage, and status.
- Remove or source generated specifics such as example domains, invented API
  endpoints, latency, throughput, model inventories, or monthly cost ranges.
- Do not treat a polished simulated UI as evidence that the source product exposes
  that exact state.
- Keep interpretation in notes or label it explicitly; visible claims require
  transcript, frame, user-provided, or verified external evidence.

## 7. Editability and output contract

Use these labels exactly:

| Artifact | Accurate label |
|---|---|
| Genspark project/viewer | hosted editable reference |
| PNG-per-slide PPTX | image-based reference/draft |
| Native text over rendered background | hybrid/editable-text PPTX |
| Native PowerPoint text, shapes, diagrams, tables, and charts | fully native editable PPTX |

Do not call a hybrid deck fully native. A client-ready request defaults to a fully
native branded rebuild through `branded-pptx-deck` or
`vault-presales-pptx-pipeline`. Genspark contributes storyline, semantic roles,
and useful archetypes; the downstream builder owns brand tokens, grid, object
model, layout, and final QA.

## 8. QA and status contract

Use only `draft`, `reviewed`, or `blocked` for deliverables.

`reviewed` requires all of the following:

- coverage matrix complete;
- unsupported-generated-specific scan clean;
- source/claim validation complete;
- slide count and ordering verified;
- visual render inspected slide by slide for clipping, overlap, footer collision,
  contrast, alignment, and density;
- editability accurately declared and verified;
- PPTX schema validation and Office issue scan passed;
- final rendered PowerPoint, not just source HTML, inspected.

If any gate is unavailable or fails, retain `draft` or `blocked` and state the
specific reason. Never promote status because the filename already says reviewed.

## 9. Handoff contract

Write `<run>/genspark-handoff.json` using
`references/genspark-handoff-template.json`. Validate it with:

```bash
python3 skills/pptx-visual-spec/scripts/validate_genspark_handoff.py \
  <run>/genspark-handoff.json
```

The handoff is the source of truth for project identity, evidence inputs, slide
coverage, browser recovery, editability, builder routing, blockers, and QA status.

## 10. Cross-host adapter contract

- **Codex Desktop:** discover/use the Genspark app for generation; use headed
  Playwright for recovery; request the host's GUI permission when required.
- **Codex CLI:** use an exposed MCP/connector if present; otherwise recover an
  existing viewer with Playwright and continue locally.
- **Claude Code:** use its connector/browser tools when available; otherwise run
  the same repository scripts and preserve the same handoff.
- **OpenHands/generic agents:** execute stages sequentially with equivalent shell,
  browser, and file tools; do not omit gates because named skills are unavailable.
- **Antigravity/Gemini on Windows:** prefer Windows-native headed Chrome/Playwright
  for authentication; use managed skill copies installed by the registry.

Host capability changes execution mechanics, not evidence, count, truthfulness,
editability, or QA requirements.
