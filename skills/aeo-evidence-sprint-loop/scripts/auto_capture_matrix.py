#!/usr/bin/env python3
"""Fill an AEO AI-answer capture matrix from official model APIs.

This does not scrape logged-in consumer AI products. It calls provider APIs
when credentials are available and writes the same template consumed by
ingest_capture_matrix.py.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_MODELS = {
    "ChatGPT": os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
    "Claude": os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5"),
    "Perplexity": os.environ.get("PERPLEXITY_MODEL", "sonar-pro"),
    "Google AI Mode": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    "Gemini": os.environ.get("GEMINI_MODEL", "gemini-2.5-flash"),
    "Gemini Deep Research": os.environ.get("GEMINI_RESEARCH_MODEL", os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")),
    "Groq": os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile"),
    "Grok": os.environ.get("XAI_MODEL", "grok-3-mini"),
}


def env_value(name: str) -> str | None:
    value = os.environ.get(name)
    if value:
        return value
    claude_settings_candidates = [
        Path.home() / ".claude" / "settings.local.json",
        Path("/home/shekerk/.claude/settings.local.json"),
    ]
    for claude_settings in claude_settings_candidates:
        if not claude_settings.exists():
            continue
        try:
            data = json.loads(claude_settings.read_text(encoding="utf-8"))
            value = (data.get("env") or {}).get(name)
            if value:
                return str(value)
            if name == "ANTHROPIC_API_KEY" and data.get("apiKey"):
                return str(data["apiKey"])
            if name == "ANTHROPIC_BASE_URL" and data.get("baseURL"):
                return str(data["baseURL"])
        except (OSError, json.JSONDecodeError):
            continue
    watch_env = Path.home() / ".config" / "watch" / ".env"
    if watch_env.exists():
        try:
            for line in watch_env.read_text(encoding="utf-8").splitlines():
                if "=" not in line or line.lstrip().startswith("#"):
                    continue
                key, raw_value = line.split("=", 1)
                key = key.strip().removeprefix("export ").strip()
                if key == name:
                    value = raw_value.strip().strip('"').strip("'")
                    if value:
                        return value
        except OSError:
            return None
    return None


def now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def post_json(url: str, payload: dict, headers: dict[str, str], timeout: int) -> dict:
    body = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", **headers},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {detail[:1200]}") from exc


def research_prompt(prompt: str) -> str:
    return (
        "Answer as a concise web-grounded research analyst. "
        "Give 5-8 bullet points, cite source URLs when available, and separate supported facts from uncertainty.\n\n"
        f"Question: {prompt}"
    )


def openai_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = env_value("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY missing")
    model = DEFAULT_MODELS["ChatGPT"]
    data = post_json(
        "https://api.openai.com/v1/responses",
        {
            "model": model,
            "input": prompt,
        },
        {"Authorization": f"Bearer {api_key}"},
        timeout,
    )
    text = data.get("output_text") or ""
    if not text:
        parts = []
        for item in data.get("output", []) or []:
            for content in item.get("content", []) or []:
                if content.get("type") in {"output_text", "text"} and content.get("text"):
                    parts.append(content["text"])
        text = "\n".join(parts).strip()
    return text, extract_urls(data), model


def anthropic_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = env_value("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY missing")
    model = DEFAULT_MODELS["Claude"]
    base_url = (env_value("ANTHROPIC_BASE_URL") or "https://api.anthropic.com").rstrip("/")
    data = post_json(
        f"{base_url}/v1/messages",
        {
            "model": model,
            "max_tokens": 1800,
            "messages": [{"role": "user", "content": prompt}],
        },
        {"x-api-key": api_key, "anthropic-version": "2023-06-01"},
        timeout,
    )
    text = "\n".join(part.get("text", "") for part in data.get("content", []) if part.get("type") == "text").strip()
    return text, extract_urls(data), model


def perplexity_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = env_value("PERPLEXITY_API_KEY") or env_value("PPLX_API_KEY")
    if not api_key:
        raise RuntimeError("PERPLEXITY_API_KEY or PPLX_API_KEY missing")
    model = DEFAULT_MODELS["Perplexity"]
    data = post_json(
        "https://api.perplexity.ai/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        {"Authorization": f"Bearer {api_key}"},
        timeout,
    )
    choices = data.get("choices") or []
    text = choices[0].get("message", {}).get("content", "").strip() if choices else ""
    citations = data.get("citations") or []
    return text, sorted(set(citations + extract_urls(data))), model


def groq_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = env_value("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY missing")
    model = DEFAULT_MODELS["Groq"]
    data = post_json(
        "https://api.groq.com/openai/v1/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        {"Authorization": f"Bearer {api_key}"},
        timeout,
    )
    choices = data.get("choices") or []
    text = choices[0].get("message", {}).get("content", "").strip() if choices else ""
    return text, extract_urls(data), model


def grok_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = env_value("XAI_API_KEY") or env_value("GROK_API_KEY")
    if not api_key:
        raise RuntimeError("XAI_API_KEY or GROK_API_KEY missing")
    model = DEFAULT_MODELS["Grok"]
    data = post_json(
        "https://api.x.ai/v1/chat/completions",
        {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
        },
        {"Authorization": f"Bearer {api_key}"},
        timeout,
    )
    choices = data.get("choices") or []
    text = choices[0].get("message", {}).get("content", "").strip() if choices else ""
    return text, extract_urls(data), model


def gemini_capture(prompt: str, timeout: int) -> tuple[str, list[str], str]:
    api_key = (
        env_value("GOOGLE_GENERATIVE_AI_API_KEY")
        or env_value("GEMINI_API_KEY")
        or env_value("GOOGLE_API_KEY")
    )
    if not api_key:
        raise RuntimeError("GOOGLE_GENERATIVE_AI_API_KEY, GEMINI_API_KEY, or GOOGLE_API_KEY missing")
    model = DEFAULT_MODELS["Gemini"]
    data = post_json(
        f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}",
        {"contents": [{"parts": [{"text": research_prompt(prompt) if "research" in prompt.lower() else prompt}]}]},
        {},
        timeout,
    )
    parts = []
    for candidate in data.get("candidates", []) or []:
        for part in candidate.get("content", {}).get("parts", []) or []:
            if part.get("text"):
                parts.append(part["text"])
    return "\n".join(parts).strip(), extract_urls(data), model


def extract_urls(obj: Any) -> list[str]:
    urls: set[str] = set()
    if isinstance(obj, dict):
        for value in obj.values():
            urls.update(extract_urls(value))
    elif isinstance(obj, list):
        for item in obj:
            urls.update(extract_urls(item))
    elif isinstance(obj, str):
        for match in re.findall(r"https?://[^\s\]\)>\"']+", obj):
            urls.add(match.rstrip(".,;:"))
        for token in obj.replace(")", " ").replace("]", " ").replace('"', " ").split():
            if token.startswith(("http://", "https://")):
                urls.add(token.rstrip(".,;:"))
    return sorted(urls)


def provider_for(engine: str):
    normalized = engine.strip().lower()
    if normalized == "chatgpt":
        return openai_capture
    if normalized == "claude":
        return anthropic_capture
    if normalized == "perplexity":
        return perplexity_capture
    if normalized in {"google ai mode", "gemini", "gemini deep research"}:
        return gemini_capture
    if normalized == "groq":
        return groq_capture
    if normalized == "grok":
        return grok_capture
    raise RuntimeError(f"No API provider configured for engine: {engine}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run_dir", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--engines", help="Comma-separated engine allowlist")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--timeout", type=int, default=120)
    parser.add_argument("--sleep", type=float, default=0.5)
    parser.add_argument("--overwrite", action="store_true")
    args = parser.parse_args()

    template = args.template or args.run_dir / "stage_outputs" / "ai_live_capture_ingest_template.json"
    out = args.out or template
    rows = read_json(template)
    if not isinstance(rows, list):
        raise SystemExit("Template must be a JSON list")
    allow = {item.strip() for item in args.engines.split(",")} if args.engines else None
    captured = 0
    attempted = 0
    errors = []
    for row in rows:
        if args.limit is not None and attempted >= args.limit:
            break
        if allow and row.get("engine") not in allow:
            continue
        if row.get("answer") and not args.overwrite:
            continue
        attempted += 1
        try:
            provider = provider_for(row.get("engine", ""))
            answer, citation_urls, model = provider(row["prompt"], args.timeout)
            if not answer:
                raise RuntimeError("empty provider answer")
            row["answer"] = answer
            row["citation_urls"] = citation_urls
            row["captured_at"] = now_iso()
            row["capture_status"] = "captured_api"
            row["api_model"] = model
            row["api_capture_note"] = "Captured via official provider API, not consumer UI scraping."
            captured += 1
            write_json(out, rows)
            time.sleep(args.sleep)
        except (RuntimeError, urllib.error.URLError, TimeoutError) as exc:
            row["capture_status"] = "api_error"
            row["api_error"] = f"{type(exc).__name__}: {exc}"
            errors.append({"task_id": row.get("task_id"), "engine": row.get("engine"), "error": row["api_error"]})
            write_json(out, rows)
    write_json(out, rows)
    report = {
        "attempted": attempted,
        "captured": captured,
        "errors": errors,
        "output": str(out),
        "note": "Run ingest_capture_matrix.py after enough rows are captured.",
    }
    report_path = args.run_dir / "qa" / "auto_capture_matrix_report.json"
    write_json(report_path, report)
    print(report_path)
    return 0 if captured else 1


if __name__ == "__main__":
    raise SystemExit(main())
