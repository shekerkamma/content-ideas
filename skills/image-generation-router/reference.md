# Image Generation Router Reference

## Provider Matrix

| Route | Default condition | Authentication | Availability truth |
|---|---|---|---|
| Built-in OpenAI `image_gen` | Default | Signed-in host subscription | Successful built-in tool call |
| Gemini through CLIProxyAPI | Explicit request or disclosed fallback | Local client key plus provider OAuth | Authenticated `GET /v1/models` |

The router intentionally does not merge provider catalogs. Built-in tool metadata and
CLIProxyAPI model IDs come from different runtimes.

**Kimi K3 is not in this matrix and never will be.** Kimi is a vision-language model with
no image generation; `scripts/kimi_adapter.py` offers optional prompt refinement and
vision review only (see SKILL.md "Kimi K3 Helper"). Its sidecar is `<out>.kimi.json` with
`"is_image_generation": false`; it has no `execution_path` field by design.

## Normative Contract

- Policy: `contracts/image-generation-routing-contract.json`
- Schema: `contracts/image-generation-routing-contract.schema.json`
- Validator: `scripts/validate_contract.py`

`preferred_models` is a deterministic ordering hint, not a capability promise. The adapter
intersects that order with the authenticated live catalog before selecting anything.

## Operator Commands

| Purpose | Command | Generates? |
|---|---|---|
| Discover live Gemini image models | `python3 skills/image-generation-router/scripts/generate_gemini.py --list-models` | No |
| Check readiness and selected model | `python3 skills/image-generation-router/scripts/generate_gemini.py --probe` | No |
| Validate rules and consumers | `python3 skills/image-generation-router/scripts/validate_contract.py` | No |
| Generate with live default | `python3 skills/image-generation-router/scripts/generate_gemini.py --prompt-file <prompt.txt> --out <output.png>` | Yes |
| Require an exact model | add `--model <exact-live-model-id>` | Yes |

## Environment

- `CLIPROXYAPI_BASE_URL` — optional; default `http://127.0.0.1:8317`.
- `CLIPROXYAPI_CONFIG` — optional config path; default `~/cliproxyapi/config.yaml`.
- `CLIPROXYAPI_KEY` — optional local client key override. Never log it.
- `CLIPROXYAPI_IMAGE_MODEL` — optional exact image-model ID.
- `KIMI_API_KEY` — optional; helper only (see SKILL.md "Kimi K3 Helper"). Never log it.
- `KIMI_CONFIG` — optional config path; default `~/.config/kimi/.env` (mode `0600`),
  may also carry a `KIMI_BASE_URL=...` line.
- `KIMI_BASE_URL` — optional; default `https://api.kimi.com/coding/v1`. Set this to
  `https://zenmux.ai/api/v1` if the supplied key is a ZenMux aggregator key rather than
  a native Kimi key — 401 against the native endpoint does not by itself mean the key
  is invalid; see the SKILL.md gotcha before reporting a key as bad.
- `KIMI_MODEL` — optional exact model ID override for the helper.

## Output Contract

The Gemini adapter writes the requested image plus an adjacent provenance sidecar:

```json
{
  "execution_path": "cliproxyapi-gemini",
  "provider": "gemini",
  "requested_model": null,
  "resolved_model": "gemini-3.1-flash-image",
  "auth_mode": "local-client-key-plus-provider-oauth",
  "prompt_sha256": "...",
  "output_path": "...",
  "source_media_type": "image/jpeg",
  "output_media_type": "image/png",
  "generated_at": "..."
}
```

No key, OAuth token, account identifier, or full response payload belongs in the sidecar.

## Failure Semantics

- Service unreachable: report CLIProxyAPI unavailable; do not start or reconfigure it
  unless the user asked for installation/repair.
- HTTP 401: local client key missing or wrong.
- Empty image-model list: provider authentication/catalog unavailable.
- Explicit model absent: list available image-model IDs and stop.
- `unknown provider for model`: the proxy cannot route that model; do not alias it.
- Successful response without a data image: preserve no partial artifact; report the
  response shape as unsupported.
