# Codex — HyperFrames test prompts

Copy-paste prompts to test the **HyperFrames** skill inside **Codex (running in WSL)**.

## Status / setup (done 2026-06-22)
- Plugin installed + enabled from the official curated marketplace:
  `codex plugin add hyperframes@openai-curated` → `[plugins."hyperframes@openai-curated"]`.
- Runtime hardened so any Codex shell works:
  - `~/.bashrc` sources nvm (interactive shells → Node v22).
  - `~/.local/bin/hyperframes` wrapper runs the WSL Node-22 CLI in **any** shell type
    (shadows the Windows `AppData/Roaming/npm` stub; pins Node 22 for render subprocesses).
- Verified: `hyperframes --version` → 0.7.0, ffmpeg present, `hyperframes lint` runs clean.

## How to invoke
1. **Restart the Codex session** so the plugin loads.
2. Paste a prompt below. The `hyperframes` router maps intent → workflow
   (product-launch-video / website-to-video / faceless-explainer / motion-graphics / …).
3. If Codex doesn't auto-pick it: *"Read and follow the hyperframes plugin's SKILL.md."*
4. Use **`hyperframes …` directly, not `npx hyperframes`** — the wrapper guarantees Node 22;
   `npx` in a non-nvm shell can grab system Node 18 and fail.
5. Keep early runs **silent** (no TTS/BGM creds needed). Add a music bed afterward.

---

## 1) Smoke test (fastest — confirms the whole toolchain)

```
Use the hyperframes skill (the HyperFrames Codex plugin) to prove the toolchain works
end-to-end. Run in WSL/bash. Work in phases; after each, print PASS/FAIL + key output.
If anything fails, STOP and show the exact error — don't work around it.

PHASE 0 — runtime: run `hyperframes --version`, `node --version`, `ffmpeg -version | head -1`.
  PASS only if hyperframes prints a version and ffmpeg is present. (Use the `hyperframes`
  command directly — it's a wrapper that pins Node 22; do NOT use `npx hyperframes`.)

PHASE 1 — skill: read the hyperframes skill's SKILL.md, and in 2 lines say which workflow
  you'd use for a short title/motion graphic (expected: motion-graphics or general-video).

PHASE 2 — build a tiny composition in ~/hf-smoketest/:
  `hyperframes init ~/hf-smoketest --non-interactive --skip-skills --example=blank`
  Then edit index.html into a ~6-second title card: near-black #080b11 background, a single
  centered headline "hyperframes works." in teal #2dd4bf that fades + scales in (GSAP,
  paused timeline registered on window.__timelines["main"]). No external fonts/CDNs except
  the gsap script tag already in the scaffold.

PHASE 3 — QA: run `hyperframes lint` (fix to 0 errors), `hyperframes validate`,
  `hyperframes snapshot --at 3`. Open the snapshot and confirm the teal headline renders.

PHASE 4 — render: `hyperframes render --quality high --output ~/hf-smoketest/out.mp4`,
  then `ffprobe` it and print the path + duration. Report DONE.

Start with PHASE 0.
```

---

## 2) Full build (a real, sellable 30s promo — Dental)

Grounded in `runs/2026-06-16-openhands-business-proposals/02-dental-practices.md`.
Output should match the `dental-ai.mp4` built in WSL — a good correctness check.

```
Use the hyperframes skill to produce a 30-second landscape promo, Aurora Glass style,
SILENT (no narration). Run in WSL/bash. Use the `hyperframes` command directly (Node-22
wrapper), not npx. Phases with PASS/FAIL; STOP on any error.

BRIEF (no website to capture — use the brief/no-capture path):
  PRODUCT: DataStaq AI — done-for-you AI engineering for SMBs.
  ANGLE:   Dental Practices AI suite. Sell business OUTCOMES, not AI patterns. No slop.
  AESTHETIC: dark Aurora Glass — canvas #080b11, TEAL #2dd4bf lone accent, aurora gradient
    (teal->sky->magenta) only on the hero word, IBM Plex Mono UPPERCASE labels, big lowercase
    Barlow headlines, hairline dividers, flat (no shadows). Local @font-face only (no Google
    Fonts <link> — it fails lint). Exactly one root index.html with data-composition-id.
  STORY (7 beats): hook "fill every chair. automatically." -> five lanes (recall recovery,
    no-show reduction, insurance verification, cost estimates, new-patient intake; each =
    buyer + one-line outcome) -> spotlight recall ("recover the chair time you already earned",
    flow: pull overdue list->sequenced outreach->online booking->auto-confirm->rebook no-shows)
    -> spotlight insurance verification ("take hold music off the front desk") -> the math
    (payback 11 days, $6,725/mo net, $224,500 / 3yr) -> stack "built, not bought" (your PMS:
    Dentrix/Eaglesoft stays the system of record; OpenHands orchestration; MCP tools; BAA/HIPAA)
    -> CTA "start with recall, expand to intake."

GATES: `hyperframes lint` to 0 errors -> `validate` -> `inspect --strict-layout` ->
  `snapshot --at 2,7,13,18,23,28` and SHOW me the contact sheet. WAIT for my "approved"
  before `hyperframes render --quality high --output renders/dental-promo.mp4`. ffprobe + report path.
```

---

## Swap the vertical
Replace the BRIEF block in prompt #2 with content from the matching proposal in
`runs/2026-06-16-openhands-business-proposals/`:

| Vertical | Proposal file | Hook / payback |
|---|---|---|
| Real Estate | `01-real-estate-brokerages.md` | "the brokerage, automated." · live dashboard demo |
| Dental | `02-dental-practices.md` | "fill every chair." · payback 11 days |
| Law Firms | `06-law-firms.md` | "convert the intake. bill the hour." · $59,400 recovered |
| Med Spas | `07-med-spas.md` | "fill the cancellation." · payback 21 days |
| HVAC / Plumbing | `08-hvac-plumbing.md` | "answer every call." · payback 6 days |

Rule of thumb: lead each lane with **buyer + workflow pain + measurable outcome**; never
generic AI-pattern explainers. Use the business-case ("the math") scene instead of a fake
dashboard unless a real screenshot exists.
