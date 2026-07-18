# Image Generation Router Reference

## Provider Matrix

| Route | Default condition | Authentication | Availability truth |
|---|---|---|---|
| Built-in OpenAI `image_gen` | Default | Signed-in host subscription | Successful built-in tool call |
| Gemini through CLIProxyAPI | Explicit request or disclosed fallback | Local client key plus provider OAuth | Authenticated `GET /v1/models` |

The router intentionally does not merge provider catalogs. Built-in tool metadata and
CLIProxyAPI model IDs come from different runtimes.

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
