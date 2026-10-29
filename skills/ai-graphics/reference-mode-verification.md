# Verifying the reference modes

`codex_image_edit.py` claims Images 2.0 honors an attached reference. That claim
is only worth what its test is worth, and the obvious test does not work.

## Why a single render proves nothing

Render with `--ref`, look at the output, see the reference reflected in it —
and you have learned nothing, because the model also read your prompt, and your
prompt describes the same thing. "Honored the reference" and "read my prompt
back to me" produce the same picture.

The fix is an **asymmetric spec plus a control arm**:

1. The spec names only what the control needs to draw anything at all (the box
   labels: Orchestrator, Advisor, Worker A-D).
2. The spec deliberately does **not** enumerate the model captions
   (`GPT-5.6`, `Gemini 3.5 Flash`, `Fable 5`) or the connector labels
   (`Labor Layer: Parallel cheap execution subtasks`, `Main hot path`,
   `premium taste and judgment loop`). Those strings exist only inside the
   reference image.
3. Both arms run the identical spec — one with `--ref`, one without.

Their presence in the with-ref arm and absence in the control is the evidence.
`tests/test_reference_modes.py::test_specs_do_not_leak_what_only_the_reference_knows`
enforces the asymmetry so a later edit cannot quietly destroy it.

## Running it

```bash
python3 scripts/verify_reference_modes.py --mode edit --out-dir runs/imgverify
python3 scripts/verify_reference_modes.py --mode style --wait-until 14:25
```

The ChatGPT plan cap stops image renders for hours (hit twice on 2026-09-08),
so `--wait-until` holds for a reset rather than burning retries against a wall.
**Read both images.** The palette metric supports the judgement; it never
replaces it.

## Judging `--mode style`

Style has no absolute pass mark, so `scripts/palette_distance.py` is
comparative: the with-ref arm must score **lower** than the control against the
reference palette. A fixed threshold would fail a correct render whenever the
new subject legitimately shifts the histogram — which is exactly what a style
test asks the subject to do. A test guards against a threshold creeping back in.

The metric carries its own negative control: identical palettes score 0.00,
deliberately opposite ones 348.61 (synthetic) and 13.80 (the two real design
references). A metric that cannot separate navy from cream would pass a style
test that transferred nothing.

**Pillow is not in the repo venv**, so the two metric tests `importorskip` and
show as skipped under `uv run pytest`. They pass on any interpreter with
Pillow (verified against system `python3`, PIL 12.2.0). A skipped gate is not a
passing gate — run them there before trusting a style result.

## Status

| Mode | Verified | Evidence |
|---|---|---|
| `edit` | ✅ 2026-09-08 | with-ref reproduced all reference-only captions, connector labels, page chrome and the full table at 1283x1226 (reference 1280x1222); control invented GPT-4o / Claude 3.5 Sonnet / Gemini 1.5 Pro / Llama 3.1 70B, flattened the topology and defaulted to 1536x1024. Host `gpt-5.6-sol`. |
| `style` | ⏳ pending | blocked on the plan cap; runs on `gpt-6-astra` |
| `variation` | ⏳ pending | blocked on the plan cap; runs on `gpt-6-astra` |

The `edit` arm ran on `gpt-5.6-sol` before the default moved to `gpt-6-astra`,
so the two pending arms will exercise a different host than the verified one.
Note that when reading their results.
