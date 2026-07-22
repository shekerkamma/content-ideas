# Genspark deck prompt routing

Use these prompts as acceptance examples for skill discovery and routing. Natural
variants with the same intent should follow the same route.

| User prompt | Entry skill | Compound route |
|---|---|---|
| "Create a first-pass deck in Genspark from this brief." | `genspark-slides` | Generate, retain project URL, recover only if requested |
| "Use Genspark to create this, then make it branded." | `genspark-slides` | Genspark → recovery → `genspark-branded-deck` |
| "Rebuild this Genspark URL in our brand." | `genspark-slides` | Recover URL → handoff JSON → `genspark-branded-deck` |
| "Turn this Genspark deck into an editable PowerPoint." | `genspark-slides` | Recover → branded reference → `branded-pptx-deck` |
| "Make this Genspark deck client-ready for presales." | `genspark-slides` | Recover → branded reference → `vault-presales-pptx-pipeline` → QA |
| "Modify, update, or contextualize this existing deck for Acme." | `genspark-branded-deck` | Rebuild from validated content; do not patch slide coordinates in place |
| "Reskin this deck and improve the visual assets." | `genspark-branded-deck` | Re-author HTML/CSS, replace weak visuals, render, and QA |
| "Make a fast branded deck without using Genspark credits." | `genspark-branded-deck` | Local owned HTML/CSS → image or hybrid PPTX |
| "Genspark is blocked; finish the deck locally." | `genspark-slides` | Record hosted failure → `genspark-branded-deck` fallback |
| "Diagnose why Genspark login works in Windows but not WSL." | `genspark-slides` | Browser-boundary diagnostics; no deck mutation unless requested |

## Routing rules

- Words such as **brand**, **reskin**, **visual refresh**, **modify**, **update**,
  or **contextualize** require a rebuild, not coordinate-level patching.
- **Editable** means the requester must choose or infer `hybrid` versus `native`.
  Use native when they need to re-layout shapes, edit charts, or deliver a
  client-owned deck.
- **Client-ready**, **presales**, or **fully native** always continues beyond
  `genspark-branded-deck` into the native branded pipeline and mandatory QA.
- A Genspark URL, project, viewer, or export starts at `genspark-slides` so the
  source and slide count are recovered before rebuilding.
