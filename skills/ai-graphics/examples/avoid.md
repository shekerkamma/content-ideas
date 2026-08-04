# ai-graphics — anti-patterns (each one actually failed on 2026-07-13)

## 1. Raw prose prompt with text through FLUX
"Whiteboard infographic ... title: '3 REASONS SMBs SHOULD REPLACE SaaS...'" → three
attempts, three failures: "AI-BULT", "CUT RECURENCE COSTS", a phantom row reading
"2 TO STBUT TOOLS", a dropped label. FLUX treats copy as vibes. If text matters, it
goes to gpt-image (with a structured spec) or to code. No fourth retry — the retry
budget is 2, then switch strategy.

## 2. Summarizing a reference into "style words" and calling it reproduction
First reproduction of a 15-element reference diagram silently rendered 6 elements —
looked complete, wasn't. The spec-writer is the lossy component, not the renderer.
Counted inventory + QA diff (Reference Reproduction Protocol) is mandatory; simplifying
a reference is a user decision, never a silent default.

## 3. Assuming a model or provider exists because it plausibly should
`gpt-5.6` — rejected upstream ("not supported when using Codex with a ChatGPT account").
zenmux — catalog lists `openai/gpt-image-2` but the images endpoint has no zenmux driver.
`flux.1-schnell` — catalogued, fails upstream. Capability truth comes from a live probe,
not from the catalog, the model name, or memory.

## 4. Using the CLI or MCP for image payloads
The MCP has no image tool; the CLI prints `[object Object]` and has no `--json`.
Time spent there is wasted — direct HTTP POST only (via `scripts/omniroute_image.py`).

## 5. Bare `npx playwright screenshot`
Resolves the latest playwright, which demands a browser build absent from the cache
(`chromium_headless_shell-1228`). Use `scripts/html_to_png.mjs`.

## 6. Delivering by printing a path
Relative paths and `C:\` paths are dead links in the user's Remote-WSL VS Code, and
scratchpad paths die with the session. Copy to a durable location and OPEN the file
(`code <abs-wsl-path>`). "What is the fun in providing the files if they do not open?"

## 7. Shipping unreviewed output
Every render gets Read and checked against the spec/inventory word-by-word before
delivery. FLUX failures look plausible at a glance; the 6-of-15 loss looked complete.
Status is stated explicitly: draft vs reviewed.

## 8. Regenerating when the code track could just be edited
Label overlapping an arrow in an HTML/SVG render is a one-line coordinate fix and a
re-screenshot — deterministic and free. Regeneration is the lottery; editing is the
workflow.

## 9. Trusting prose-only guidance to avoid "generic AI" for an original design
Avoided all three of `frontend-design`'s named defaults (cream+serif+terracotta,
near-black+neon, broadsheet columns) and still landed on a 4th, unnamed one — pale
blue-gray background, white cards, one saturated blue accent, system sans. User:
"this does not look good at all." Correct. The 9px "signature" corner-ticks were also
invisible at delivery size, so they weren't functioning as a signature element at all.
Fix: rebuilt the identical content grounded in one real Awwwards capture instead of
prose alone — immediately more distinctive (warm gradient, bold visible signature
device, restrained accent). See `assets/fail-generic-original-design.png` vs
`assets/success-awwwards-grounded-original.png`, and `reference.md` "A 4th generic
default" for the full writeup. Lesson: for original designs, ground the plan in a
real capture; treat prose-only as a fallback, not the default.
