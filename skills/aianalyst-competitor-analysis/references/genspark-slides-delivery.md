# Genspark Slides Delivery Protocol

Use this protocol when the competitor-analysis workflow uses hosted Genspark AI Slides. This is the hosted generation and capture stage, not the complete final client package by itself.

## Default Tool Choice

- Use `genspark-slides` / hosted Genspark AI Slides when the user asks for hosted Genspark generation, wants a Genspark project to edit, or benefits from Genspark's slide ideation.
- Treat the Genspark project/viewer as the hosted editable source and reference artifact.
- Treat recovered HTML, screenshots, contact sheets, and image-based PPTX exports as QA/reference artifacts unless a separate native PowerPoint rebuild is explicitly performed.
- Final client delivery still requires recreating the evidence-clean deck through `genspark-branded-deck` from owned HTML/CSS unless the user explicitly says the hosted Genspark project alone is sufficient.
- Use `branded-pptx-deck` only when the user explicitly needs native editable PowerPoint shapes/charts rather than hosted Genspark editability.

## Input Discipline

Before invoking Genspark AI Slides, provide a validated slide spine, not a broad launch-report prompt.

Required inputs:

- target company and competitive decision
- audience and outcome
- final slide spine with assertion titles
- allowed evidence ledger rows or summarized claim IDs
- supported numeric datapoints and their source labels
- confidence labels and caveats
- banned unsupported datapoints, if already known
- instruction that unsupported numbers must not be invented

Do not ask Genspark to infer market sizes, ROI, pricing, revenue, ARR, growth rates, usage counts, implementation timelines, or competitor benchmarks unless those numbers are in the evidence ledger or explicitly labeled as assumptions.

## Generation Loop

Use a bounded generation loop.

1. Generate the deck from the validated spine and evidence pack.
2. Capture or recover the generated slides using the `genspark-slides` workflow.
3. If the slide count is materially below the required scope, request one expansion pass with the missing sections named.
4. If evidence issues remain after the first correction pass, stop regenerating and fix the recovered artifact deterministically.

Do not repeatedly regenerate the deck to fix unsupported datapoints. Regeneration can create new hallucinated metrics and makes QA harder to audit.

## Evidence-Cleaning Standard

After capture, run a visible-content QA pass against recovered slide HTML or extracted slide text.

Create an allowed-number list:

| Field | Requirement |
|---|---|
| Number | Exact visible form or normalized regex |
| Meaning | What the number represents |
| Source basis | `claim_id`, official source, third-party source, or vendor-published claim |
| Allowed label | Wording required near the number, such as `vendor-published` or `to validate` |
| Use | Slide(s) or section(s) where the number may appear |

Create a blocked-pattern list for likely unsupported metrics:

- ROI, revenue, ARR, payback, margin, market size, CAGR, TAM, SAM, SOM
- pricing ranges, implementation cost, consultant counts, seat counts
- arbitrary competitor scores, percentages, adoption rates, growth rates
- unsupported `X+`, `X%`, `$X`, or `X-month` claims

Then scan visible text for unsupported patterns. Example pattern:

```bash
rg -n ">[^<]*(\$[0-9]|ARR|ROI|TAM|SAM|SOM|CAGR|[0-9]+%|[0-9]+\\+|[0-9]+-[0-9]+)[^<]*<" \
  runs/<run>/client-package/<genspark-capture>/html
```

The scan is not enough by itself. Manually inspect the matches and distinguish:

- supported numbers that should stay
- supported numbers that need clearer labels
- unsupported numbers that must be removed or replaced
- structural numbers such as slide numbers, dates, or roadmap day labels

## Deterministic Cleanup

When unsupported datapoints are found after capture:

- plug in supported numbers from the evidence ledger where available
- preserve source labels such as `vendor-published`, `third-party`, `official`, `secondary`, or `to validate`
- replace unsupported numbers with qualitative statements when no supported number exists
- remove false precision instead of weakening it into vague but still numeric claims
- keep a cleanup note or manifest listing removed/replaced claims
- rerun the visible-text scan after cleanup

Supported numbers must not be omitted merely because cleanup is in progress. If a number is supported and strategically relevant, use it with the correct caveat. If a number is unsupported, remove it.

## Handoff To Branded Final Deck

After evidence cleanup, hand off to `genspark-branded-deck`.

Required handoff:

- final slide spine
- recovered Genspark slide references, when useful
- evidence-clean text
- allowed-number list
- upstream AI Analyst artifact references for every visible number
- unsupported datapoints removed
- visual direction and brand notes
- required slide count
- editability target: `hybrid_editable` or `native_powerpoint`

The branded deck must be recreated in `deck.html` and rendered through the local branded workflow. Do not use the recovered Genspark export or an image-only PPTX as the final client deck unless the user explicitly waives editability.

## Export and QA

For local PPTX export from recovered slides or branded recreation:

- render screenshots or slide images only after the evidence-clean scan passes
- build contact sheets for human review
- run OfficeCLI QA when producing a PPTX artifact
- mark status `reviewed` only when render QA and OfficeCLI QA pass
- mark status `draft` or `partial` if OfficeCLI screenshots are blocked by environment but validation/issues/html checks pass
- document whether the PPTX is hybrid-editable or native-editable for final delivery; image-based exports must remain draft/reference unless editability is explicitly waived

Do not represent an image-based PowerPoint export as a final editable slide deck. If final PPTX uses `genspark-branded-deck` hybrid mode, declare it as hybrid-editable text over rendered backgrounds. If fully native/re-layoutable editability is needed, rebuild with `branded-pptx-deck`.

## Windows Desktop Delivery

When the user asks to open the deck on Windows Desktop from WSL:

1. Copy the chosen file directly to a Windows path such as `/mnt/c/Users/sheke/OneDrive/Desktop/<filename>.pptx`.
2. Open the Windows path with PowerShell:

```bash
powershell.exe -NoProfile -Command "Start-Process 'C:\Users\sheke\OneDrive\Desktop\<filename>.pptx'"
```

Avoid routing through WSL network paths or invoking `wslpath` inside PowerShell. The simple copy-then-open path is more reliable and easier to audit.

## Manifest Requirements

The delivery manifest must distinguish:

- hosted Genspark project URL or project ID
- recovered HTML path
- local rendered references or contact sheets
- branded deck source path
- exported PPTX path
- PPTX editability status
- OfficeCLI status
- evidence-clean scan status
- unsupported datapoints removed or unresolved
- whether the branded deck and HTML artifacts were recreated from evidence-clean content

If the hosted Genspark project cannot be patched after deterministic cleanup of recovered HTML, state that the final branded deck and HTML are evidence-clean but the hosted editable source may need manual synchronization.
