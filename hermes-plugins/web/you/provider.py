"""You.com web search provider for Hermes Agent."""

from __future__ import annotations

import logging
import os
from typing import Any, Dict, Iterable, List

from agent.web_search_provider import WebSearchProvider

logger = logging.getLogger(__name__)

_DEFAULT_BASE_URL = "https://ydc-index.io"


def _api_key() -> str:
    return os.getenv("YOU_API_KEY", "").strip()


def _base_url() -> str:
    return os.getenv("YOU_BASE_URL", _DEFAULT_BASE_URL).rstrip("/")


def _pick_first(mapping: Dict[str, Any], keys: Iterable[str]) -> str:
    for key in keys:
        value = mapping.get(key)
        if value is not None:
            if isinstance(value, list):
                value = " ".join(str(item).strip() for item in value if item)
            text = str(value).strip()
            if text:
                return text
    return ""


def _result_items(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Return the most likely result list from You.com response variants."""
    candidates: list[Any] = [
        payload.get("hits"),
        payload.get("results"),
        payload.get("web"),
        payload.get("data"),
    ]
    data = payload.get("data")
    if isinstance(data, dict):
        candidates.extend([data.get("hits"), data.get("results"), data.get("web")])
    results = payload.get("results")
    if isinstance(results, dict):
        candidates.extend(
            [results.get("hits"), results.get("results"), results.get("web")]
        )

    for candidate in candidates:
        if isinstance(candidate, list):
            return [item for item in candidate if isinstance(item, dict)]
    return []


class YouWebSearchProvider(WebSearchProvider):
    """You.com search provider using the You.com platform API."""

    @property
    def name(self) -> str:
        return "you"

    @property
    def display_name(self) -> str:
        return "You.com"

    def is_available(self) -> bool:
        return bool(_api_key())

    def supports_search(self) -> bool:
        return True

    def supports_extract(self) -> bool:
        return False

    def search(self, query: str, limit: int = 5) -> Dict[str, Any]:
        try:
            from tools.interrupt import is_interrupted

            if is_interrupted():
                return {"success": False, "error": "Interrupted"}

            key = _api_key()
            if not key:
                raise ValueError(
                    "YOU_API_KEY environment variable not set. "
                    "Get your API key at https://you.com/platform"
                )

            import httpx

            max_results = max(1, min(int(limit or 5), 20))
            response = httpx.get(
                f"{_base_url()}/v1/search",
                params={"query": query, "num_web_results": max_results},
                headers={"X-API-Key": key},
                timeout=30,
            )
            response.raise_for_status()
            payload = response.json()

            web_results = []
            for index, item in enumerate(_result_items(payload)):
                url = _pick_first(item, ("url", "link", "source_url"))
                title = _pick_first(item, ("title", "name"))
                description = _pick_first(
                    item,
                    ("description", "snippet", "content", "text", "summary"),
                )
                if not url and not title and not description:
                    continue
                web_results.append(
                    {
                        "title": title,
                        "url": url,
                        "description": description,
                        "position": index + 1,
                    }
                )

            return {"success": True, "data": {"web": web_results}}
        except ValueError as exc:
            return {"success": False, "error": str(exc)}
        except Exception as exc:  # noqa: BLE001
            logger.warning("You.com search error: %s", exc)
            return {"success": False, "error": f"You.com search failed: {exc}"}

    def get_setup_schema(self) -> Dict[str, Any]:
        return {
            "name": "You.com",
            "badge": "paid",
            "tag": "You.com platform web search.",
            "env_vars": [
                {
                    "key": "YOU_API_KEY",
                    "prompt": "You.com API key",
                    "url": "https://you.com/platform",
                },
            ],
        }
