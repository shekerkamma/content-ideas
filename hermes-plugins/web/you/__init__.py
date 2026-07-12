"""You.com web search provider plugin for Hermes."""

from __future__ import annotations

from .provider import YouWebSearchProvider


def register(ctx) -> None:
    """Register the You.com provider with the plugin context."""
    ctx.register_web_search_provider(YouWebSearchProvider())
