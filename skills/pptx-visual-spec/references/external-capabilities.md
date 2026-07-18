# External presentation capabilities

Connector code, service accounts, OAuth grants, credit balances, and organization policy are
host state. They must not be copied into this repository. Portability therefore means the
workflow remains executable without them, not that credentials are silently transferred.

At runtime, discover the requested connector before story or rendering work begins:

1. If the capability is exposed and authorized, use it as an upstream creation/reference
   surface and apply `pptx-visual-spec` when packaging or rebuilding the final deck.
2. If it is exposed but unauthenticated, ask the user to authorize it on that host. Never copy
   tokens, browser profiles, cookies, or OAuth files from another machine.
3. If it is unavailable, continue through the declared local fallback unless the user
   explicitly required that hosted product.

| Capability | Portable local fallback |
|---|---|
| Canva presentation | `branded-pptx-deck` |
| Google Slides | `branded-pptx-deck`, then import the reviewed PPTX |
| Gamma | `presentation` |
| Genspark AI Slides | `genspark-branded-deck` |

Use `scripts/check_external_capabilities.py` for installation diagnostics. Agent hosts should
also use their native tool discovery because a local process cannot enumerate every MCP/app
tool exposed only inside the active session.
