# Deck image routing gate

Use this gate before promising a raster asset for a presentation. Provider catalogs and prior
successful renders are not proof that a route is healthy now.

| Route | Appropriate content | Health proof required |
| --- | --- | --- |
| Deterministic HTML/SVG | diagrams, cards, text-bearing graphics, charts | local render and exact-size screenshot |
| Host-native image generation | organic illustration or photographic imagery | one real render in the current host session |
| OmniRoute image adapter | organic imagery when explicitly selected | `omniroute doctor`, reachable image route, then one real render |
| CLIProxyAPI Gemini adapter | explicit Gemini request or disclosed fallback | adapter probe plus one real render |

## Decision rules

1. Prefer deterministic HTML/SVG whenever code can own the structure and every glyph.
2. Use generated imagery only for organic, text-free regions that cannot be represented cleanly
   with native PowerPoint or deterministic code.
3. Treat preflight as transport validation only. It does not prove quota, model entitlement, or
   that a particular model identifier is routable.
4. Confirm the chosen generated-image path with one real render before committing it to the deck.
5. Record the chosen route and output artifact in `visual-spec.json` and the skill-application
   manifest. Do not silently substitute another provider.
6. If every generated route fails, disclose the failure and use a deterministic or native visual
   treatment; never insert an unverified placeholder image.

## Cross-host notes

- Claude Code and Antigravity may expose a host-native image tool; use it when available.
- Codex uses its signed-in image-generation tool when available.
- Hermes may require the configured Windows image router. From WSL, diagnose the Windows route
  with an explicit Windows working directory and gateway address rather than assuming localhost.
- A green status on one host does not establish health on another host.
