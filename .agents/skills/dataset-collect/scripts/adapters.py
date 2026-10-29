"""Fetch adapters for dataset-collect. Stdlib only.

An adapter turns one *input* (a company name, a URL, a query string) into a
list of record dicts. Adding a provider means adding one function here and
naming it in a spec's `adapter:` field -- the collector, the store, and the
query path never learn a provider's name.

Three ship by default:

  file  -- reads a local JSON/JSONL fixture. No network, no key. This is what
           `--dry-run` and the test suite run against, and it is the reason
           the skill can be verified on a machine with no data vendor at all.
  http  -- generic JSON HTTP GET/POST. Covers any REST provider, including
           the one in the source video, without naming it.
  exa   -- Exa search (EXA_API_KEY), because this repo already has that key.

Credentials are never read from the spec. `${ENV:NAME}` in a header or param
value is resolved from the process environment at call time, so a spec is
safe to commit.
"""

from __future__ import annotations

import json
import os
import re
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

__all__ = ["AdapterError", "get_adapter", "expand_env", "ADAPTERS"]

_ENV_RE = re.compile(r"\$\{ENV:([A-Za-z_][A-Za-z0-9_]*)\}")


class AdapterError(RuntimeError):
    pass


def expand_env(value):
    """Resolve `${ENV:NAME}` recursively. Missing var is an error, not ''."""
    if isinstance(value, str):
        def sub(m):
            name = m.group(1)
            got = os.environ.get(name)
            if got is None:
                raise AdapterError(
                    f"environment variable {name} is referenced by the spec but "
                    f"is not set in this process"
                )
            return got
        return _ENV_RE.sub(sub, value)
    if isinstance(value, dict):
        return {k: expand_env(v) for k, v in value.items()}
    if isinstance(value, list):
        return [expand_env(v) for v in value]
    return value


def _as_records(payload, source_id: str) -> list[dict]:
    """Normalise any JSON shape into a list of dicts."""
    if payload is None:
        return []
    if isinstance(payload, dict):
        for key in ("results", "data", "items", "records"):
            inner = payload.get(key)
            if isinstance(inner, list):
                return [r for r in inner if isinstance(r, dict)]
        return [payload]
    if isinstance(payload, list):
        return [r for r in payload if isinstance(r, dict)]
    raise AdapterError(f"{source_id}: cannot read records out of {type(payload).__name__}")


def _http_json(url: str, *, method="GET", headers=None, body=None, timeout=60):
    data = json.dumps(body).encode() if body is not None else None
    hdrs = {"Accept": "application/json"}
    if data is not None:
        hdrs["Content-Type"] = "application/json"
    hdrs.update(headers or {})
    req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")[:400]
        raise AdapterError(f"HTTP {e.code} from {url}: {detail}") from None
    except urllib.error.URLError as e:
        raise AdapterError(f"cannot reach {url}: {e.reason}") from None
    if not raw.strip():
        return None
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        raise AdapterError(f"{url} returned non-JSON: {raw[:200]}") from None


# --------------------------------------------------------------------------
# adapters
# --------------------------------------------------------------------------

def adapter_file(source: dict, value: str, spec_dir: Path) -> list[dict]:
    """Read records from a local fixture, optionally filtered to one input.

    `fixture:` is resolved relative to the spec file, never the cwd -- a spec
    run from another directory must collect the same data.
    """
    fixture = source.get("fixture")
    if not fixture:
        raise AdapterError(f"{source['id']}: adapter 'file' needs a 'fixture' path")
    fp = Path(fixture)
    if not fp.is_absolute():
        fp = spec_dir / fp
    if not fp.is_file():
        raise AdapterError(f"{source['id']}: fixture not found: {fp}")
    text = fp.read_text(encoding="utf-8")
    if fp.suffix == ".jsonl":
        rows = [json.loads(ln) for ln in text.splitlines() if ln.strip()]
    else:
        rows = _as_records(json.loads(text), source["id"])
    key = source.get("input_key")
    if key and value is not None:
        match = [r for r in rows if str(r.get(key, "")).lower() == str(value).lower()]
        return match
    return rows


def adapter_http(source: dict, value: str, spec_dir: Path) -> list[dict]:
    """Generic JSON REST call. One input -> one request."""
    base = expand_env(source.get("base_url", "")).rstrip("/")
    endpoint = expand_env(source.get("endpoint", ""))
    if not base and not endpoint.startswith("http"):
        raise AdapterError(f"{source['id']}: needs 'base_url' or an absolute 'endpoint'")
    url = endpoint if endpoint.startswith("http") else f"{base}/{endpoint.lstrip('/')}"
    method = str(source.get("method", "GET")).upper()
    headers = expand_env(source.get("headers", {}) or {})
    params = expand_env(source.get("params", {}) or {})
    key = source.get("input_key")
    if key and value is not None:
        params = {**params, key: value}
    if method == "GET":
        if params:
            url = f"{url}?{urllib.parse.urlencode(params)}"
        payload = _http_json(url, method="GET", headers=headers,
                             timeout=int(source.get("timeout", 60)))
    else:
        payload = _http_json(url, method=method, headers=headers, body=params,
                             timeout=int(source.get("timeout", 60)))
    return _as_records(payload, source["id"])


def adapter_exa(source: dict, value: str, spec_dir: Path) -> list[dict]:
    """Exa search. Uses EXA_API_KEY from the environment, never the spec."""
    api_key = os.environ.get("EXA_API_KEY")
    if not api_key:
        raise AdapterError(
            f"{source['id']}: EXA_API_KEY is not set. This is a credential "
            f"binding, not a bug -- resolve it before running."
        )
    query = value if value is not None else source.get("query")
    if not query:
        raise AdapterError(f"{source['id']}: adapter 'exa' needs an input or 'query'")
    body = {
        "query": query,
        "numResults": int(source.get("num_results", 10)),
        "type": source.get("search_type", "auto"),
    }
    if source.get("include_text"):
        body["contents"] = {"text": {"maxCharacters": int(source.get("max_chars", 2000))}}
    payload = _http_json("https://api.exa.ai/search", method="POST",
                         headers={"x-api-key": api_key}, body=body,
                         timeout=int(source.get("timeout", 60)))
    return _as_records(payload, source["id"])


ADAPTERS = {
    "file": adapter_file,
    "http": adapter_http,
    "exa": adapter_exa,
}


def get_adapter(name: str):
    try:
        return ADAPTERS[name]
    except KeyError:
        raise AdapterError(
            f"unknown adapter {name!r}; available: {', '.join(sorted(ADAPTERS))}"
        ) from None
