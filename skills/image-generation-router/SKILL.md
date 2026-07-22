---
name: image-generation-router
description: Use when an existing skill needs to generate raster imagery and must choose between built-in OpenAI imagegen and an explicitly requested or fallback Gemini/Nano Banana model through local CLIProxyAPI. Also triggers on "use Gemini for this image", "use Nano Banana", "choose an image model", and "generate through CLIProxyAPI".
argument-hint: "<image request or prompt-file> [provider]"
permissions:
  network:
    - http://127.0.0.1:8317
    - https://api.kimi.com
  file_read:
    - ~/cliproxyapi/config.yaml
    - ~/.config/kimi/.env
  file_write:
    - /tmp/
    - output/imagegen/
    - runs/
  shell:
    allowed_scripts:
      - scripts/generate_gemini.py
      - scripts/kimi_adapter.py
      - scripts/validate_contract.py
---

# Image Generation Router

Shared provider-selection overlay for image-producing skills. It does not replace the
system `imagegen` skill: that skill still owns prompt shaping, input-image semantics,
transparent-background handling, visual inspection, and project save-path rules.

Normative source: [contracts/image-generation-routing-contract.json](contracts/image-generation-routing-contract.json).
Its schema is [contracts/image-generation-routing-contract.schema.json](contracts/image-generation-routing-contract.schema.json).
When prose and the JSON contract disagree, stop and fix the drift before generating.

## Runtime Preamble

State the selected path before generation:

> "Image route: built-in OpenAI imagegen by default. Gemini through CLIProxyAPI is used
> only when you explicitly request it or the built-in route is unavailable. I will report
> the provider/model used and will not switch providers silently."

## Routing Contract

The words **MUST**, **MUST NOT**, **SHOULD**, and **MAY** below are normative.

Apply these rules in order:

1. **Respect an explicit provider request.** `OpenAI`, `imagegen`, or `image_gen` selects
   the built-in tool. `Gemini`, `Nano Banana`, or `CLIProxyAPI` selects the local Gemini
   adapter. Never translate "Nano Banana Pro" into a different Flash model.
2. **Otherwise use built-in OpenAI imagegen first.** Follow the installed `imagegen`
   skill and invoke the host-native built-in image tool. A successful tool call is its
   availability check; no API key is required.
3. **Fallback to Gemini only after built-in unavailability.** Tell the user what failed,
   probe CLIProxyAPI, and continue only when the live catalog contains an image model.
   This fallback is unavailable when the local service, client key, or provider OAuth is
   missing.
4. **Never infer availability from a model name or old status table.** Runtime
   `GET /v1/models` is authoritative for CLIProxyAPI.
5. **Do not silently substitute models.** If the requested model is absent, stop and name
   the available image models. A user may then choose one.

### Operator commands

Run from the repository root:

```bash
# Discover every currently routable Gemini image model (authoritative command)
python3 skills/image-generation-router/scripts/generate_gemini.py --list-models

# Verify service/auth readiness and show the selected live model
python3 skills/image-generation-router/scripts/generate_gemini.py --probe

# Validate the routing contract and consumer wiring without generating
python3 skills/image-generation-router/scripts/validate_contract.py
```

- Consumers **MUST** use `--list-models` or `--probe` before promising Gemini capability.
- Consumers **MUST NOT** treat `preferred_models` as an availability list; it is selection
  order applied only after live discovery.
- Consumers **MUST NOT** call the raw endpoint with a key printed in shell history when the
  safe discovery command is available.

## Shared Intake

Before either route, use the installed `imagegen` prompt schema to capture the request,
asset type, subject, composition, style, exact text, constraints, and avoid list. Keep the
same prompt intent across providers; provider selection must not change the creative brief.

For decks, documents, and evidence-bearing work, the `pptx-visual-spec` contract takes
precedence: image models are text-free, non-evidentiary, and limited to organic/editorial
regions. Structured meaning remains native or deterministically authored.

## OpenAI Route

1. Read and follow the installed system `imagegen` skill completely.
2. Invoke the built-in `image_gen` tool.
3. Inspect the result, iterate at most twice for paid/quota-bound generations, and persist
   the accepted asset according to the system skill's save-path policy.
4. Record `execution_path=built-in-image_gen`, the reported engine when available, and
   `resolved_engine=null` when the tool exposes none.

## Gemini / CLIProxyAPI Route

Write the structured prompt to a UTF-8 file, then run:

```bash
python3 skills/image-generation-router/scripts/generate_gemini.py \
  --prompt-file <prompt.txt> \
  --out <durable-output.png> \
  [--model <exact-live-model-id>]
```

Useful non-generating checks:

```bash
python3 skills/image-generation-router/scripts/generate_gemini.py --list-models
python3 skills/image-generation-router/scripts/generate_gemini.py --probe
```

Configuration precedence:

1. `CLIPROXYAPI_KEY` when explicitly set;
2. the first client key in `CLIPROXYAPI_CONFIG`;
3. `~/cliproxyapi/config.yaml`.

The base URL defaults to `http://127.0.0.1:8317` and may be overridden with
`CLIPROXYAPI_BASE_URL`. The script never prints the client key or provider credential. It
writes `<output>.provenance.json` beside the image.

## Kimi K3 Helper (Not A Provider)

Kimi K3 (OpenAI-compatible endpoint, default `https://api.kimi.com/coding/v1`) is a
vision-language model with **no raster image generation**. It **MUST NOT** appear in any
execution path, provider contract entry, or availability claim. The bundled
`scripts/kimi_adapter.py` supports exactly two optional helper roles around the real routes:

```bash
# Refine a text-free image spec before the OpenAI or Gemini route renders it
python3 skills/image-generation-router/scripts/kimi_adapter.py \
  --refine-prompt --prompt-file <spec.txt> --out <refined.txt>

# Vision second-opinion on an existing image (reference screenshot, generated-asset QA)
python3 skills/image-generation-router/scripts/kimi_adapter.py \
  --describe-image --image <asset.png> --prompt-file <question.txt> --out <review.txt>

# Non-generating checks
python3 skills/image-generation-router/scripts/kimi_adapter.py --probe
python3 skills/image-generation-router/scripts/kimi_adapter.py --list-models
```

Rules:

- The helper is optional. A missing `KIMI_API_KEY` never blocks either image route —
  skip the refinement step and continue.
- Refined prompts keep the same creative brief and the text-free constraint; record the
  refinement in run notes as `prompt_refined_by: <resolved model>` using the adapter's
  `.kimi.json` sidecar, never as an execution path.
- Vision review supplements the host model's own read; it never becomes the source of
  truth for EXTRACT/recreate decisions or QA sign-off.
- Default model order prefers the free tier: `moonshotai/kimi-k3-free`, then
  `kimi-k3-free`, then `k3`, then whatever the live catalog returns first. Override with
  `--model` or `KIMI_MODEL`.

Configuration precedence (mirrors the Gemini route's pattern):

1. `KIMI_API_KEY` env var when set; otherwise a `KIMI_API_KEY=...` line in `KIMI_CONFIG`
   (default `~/.config/kimi/.env`, mode `0600`).
2. Base URL: `--base-url` flag, then `KIMI_BASE_URL` env var, then a `KIMI_BASE_URL=...`
   line in the same config file, then the default `https://api.kimi.com/coding/v1`.

**Gotcha — "Kimi K3 API key" often means a ZenMux key, not a native Kimi key.** Verified
2026-07-21: a key sourced as "the Kimi K3 API key" 401'd against `api.kimi.com` and
`api.moonshot.ai`/`api.moonshot.cn` on every route (models, chat/completions, and the
Anthropic-style `/messages` shape) — it authenticated only against the ZenMux aggregator,
`https://zenmux.ai/api/v1`, serving `moonshotai/kimi-k3-free` at the free tier. If `--probe`
401s against the default base URL, try `--base-url https://zenmux.ai/api/v1` (or set
`KIMI_BASE_URL` in the config file) before concluding the key is invalid. Never assume a
green preflight/probe on one base URL means the key is bad elsewhere, or vice versa.
- `KIMI_API_KEY` comes from the environment or `~/.config/kimi/.env`
  (override with `KIMI_CONFIG`); it is never printed or logged.

## Contract Validation

Run after changing this skill, its adapter, its contract, or any governed consumer:

```bash
python3 skills/image-generation-router/scripts/validate_contract.py
pytest -q skills/image-generation-router/tests skills/pptx-visual-spec/tests
python3 skills/pptx-visual-spec/scripts/audit_portability.py --host project-agents
```

The validator checks JSON Schema conformance, required consumer references, and the PPTX
execution-path enum. It never calls an image model.

## QA And Delivery

1. Inspect the actual output at full resolution.
2. Check subject, composition, required/forbidden text, accidental glyphs, logos,
   watermarks, and evidence separation.
3. Use at most two model generations per deliverable; after that, switch to deterministic
   authoring or ask the user how to proceed.
4. Save project assets inside the workspace; never leave a consumed asset only in `/tmp`.
5. Report the provider, exact resolved model, output path, and QA status.

## Skill Relationships

### Category
Business Automation

### Dependencies
- `imagegen` — prompt shaping, built-in OpenAI execution, edit semantics, and asset QA.
- `CLIProxyAPI` — optional local Gemini route; required only for explicit Gemini or fallback.
- `ai-graphics` — the default HTML/SVG-to-screenshot raster route for anything with text;
  image models here only handle the narrow text-free/organic gate. `ai-graphics` has no
  copy in this repo (WSL-global at `~/.claude/skills/ai-graphics`) and is not installed by
  `install_cross_host.py` — see `skills/pptx-visual-spec/references/externally-ported-skills.md`
  for its cross-host copies and manual refresh command.

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `imagegen` | Behavioral overlay | every generated raster | structured prompt + generated image |
| `ai-graphics` | Behavioral overlay | Track B organic raster execution | prompt file + image + provenance JSON |
| `pptx-visual-spec` | Prerequisite / Gate | any deck or document visual | `<run>/visual-spec.json` image-model record |
| `branded-pptx-deck` | Sequential downstream | generated deck slot selected | generated image + provenance JSON |
| `video-to-deck` | Sequential downstream | optional illustrative slot selected | generated image + provenance JSON |

## Host Compatibility

### Target Hosts
- Codex/OpenAI: yes — built-in OpenAI route plus local CLIProxyAPI adapter.
- Claude Code: conditional — use its installed host-native image route when available;
  otherwise the local CLIProxyAPI adapter may execute through the script.
- Antigravity IDE: yes — install a managed Windows-native copy; use its native image route
  when available or execute the local CLIProxyAPI adapter through the script.
- OpenHands: conditional — Gemini works only when the host can reach the declared local
  service and config; there is no assumption of a built-in OpenAI image tool.

### Cross-host installation

Run from the repository root:

```bash
# Claude Code (relative symlink to the canonical repo skill)
python3 skills/pptx-visual-spec/scripts/install_cross_host.py \
  --host claude --skill image-generation-router

# Antigravity IDE plus its Gemini-config discovery root (managed Windows copies)
python3 skills/pptx-visual-spec/scripts/install_cross_host.py \
  --host antigravity --host gemini-config \
  --windows-home /mnt/c/Users/<name> \
  --skill image-generation-router
```

Audit the installed copies with the same host and `--skill` arguments using
`scripts/audit_portability.py`. Antigravity copies include a managed-install marker and must
be refreshed with the installer after the canonical repo skill changes.

### Canonical Source
`skills/image-generation-router/` is canonical. Discovery wrappers under `.claude/skills/`
and `.agents/skills/` must point back to this directory rather than duplicating the policy.

### Tool Mapping
- Built-in image tool names are host-specific; use the host-native image tool only when
  present.
- Shell execution uses `python3 scripts/generate_gemini.py` from this skill directory.
- Visual inspection uses the host's image-read/view tool.

## Gotchas

- **System skill ownership:** Never edit Codex's system `imagegen` skill or its bundled
  scripts to add Gemini. System updates can replace those files.
- **Model-name substitution:** `gemini-3.1-flash-image` is not Nano Banana Pro. If Pro is
  requested and absent from `/v1/models`, report unavailable instead of substituting.
- **Authentication layers:** The CLIProxyAPI client key authenticates the local request;
  provider OAuth files authenticate upstream. Do not print either.
- **Sandboxed localhost:** A managed sandbox may block `127.0.0.1`; rerun the same bounded
  probe with approved host access rather than weakening the bind address.
- **No evidence fabrication:** Generated assets never replace real product screens,
  people, facilities, logos, certifications, or proof.
