# Evidence contract

What "grounded in your sources" means mechanically, so it can be checked
instead of asserted.

## The manifest is the boundary

`SOURCES.md` defines what exists. A source in the folder but not in the table
cannot be cited. A citation pointing at an ID the table does not define is a
hard failure, not a typo.

| Column | Meaning |
|---|---|
| `ID` | `S1`, `S2`, … — stable for the life of the source set. Never renumber; append only. |
| `Title` | The filename, or the document's real title if clearer. |
| `Type` | `pdf`, `csv`, `md`, `vtt`, … — signals whether it can be computed on. |
| `Origin` | Local path, plus the URL it came from when it came from the web. |
| `Retrieved` | ISO date. A web source without a retrieval date is undated, not current. |
| `Trust` | `primary`, `secondary`, `vendor`, `unrated`. See below. |

Renumbering breaks every citation already written. Append only.

## Trust ratings

- **primary** — the thing itself: the filing, the raw export, the transcript,
  the vendor's own product documentation for a claim about that vendor.
- **secondary** — someone's reading of a primary source. Usable, but a chain of
  secondaries is a rumor with footnotes.
- **vendor** — a marketing page or announcement. Fine for "what the vendor
  says," never sufficient for "what is true," and never for a performance
  number the vendor measured about itself.
- **unrated** — the default from the scaffold. Rate before Stage 1.

When a vendor source carries a self-measured performance claim, cite it *and*
say who measured it. "65% win rate" and "65% win rate in the vendor's own
evaluation against its own prior version" are different claims.

## Citations

Put `[Sn]` on the same line as the claim. Multiple sources: `[S1][S3]`.

The gate flags a line as unsourced when it contains a magnitude — currency, a
percentage, a multiplier, a decimal, or a number of two or more digits — and no
citation. Single-digit counts, ISO dates, fenced code, inline code, and link
URLs are ignored, so ordinary prose does not trip it.

Waive a specific line when the number genuinely is not a claim:

```markdown
Roughly 1,200 accounts, illustratively <!-- unsourced: hypothetical example -->
```

Waivers are visible in the file and reviewable in the diff. That is the point —
a silent exception is indistinguishable from an oversight.

## Sentinels

Two markers, taken from the source playbook and made mechanical:

- `INPUT REQUIRED` — a model or dataset needs a number no source provides.
- `HUMAN INPUT REQUIRED` — a process step no source documents.

They are correct behavior, not defects. A model full of sentinels is more
useful than one full of plausible invented figures, because you can see exactly
where your knowledge stops.

They must be resolved or consciously accepted before delivery.
`check_output.py --strict` makes any surviving sentinel fatal — run it that way
on anything client-facing.

## Running the gate

```bash
# during drafting — sentinels warn, unsourced claims fail
python3 scripts/check_output.py outputs/report.md --manifest SOURCES.md

# before delivery — sentinels are fatal too
python3 scripts/check_output.py outputs/*.md --manifest SOURCES.md --strict

# machine-readable, for chaining
python3 scripts/check_output.py outputs/report.md --manifest SOURCES.md --json
```

| Check | Fatal | Meaning |
|---|---|---|
| `unsourced` | yes | magnitude claim, no citation |
| `dangling` | yes | cites an ID the manifest does not define |
| `empty` | yes | no citation anywhere in a non-trivial output |
| `sentinel` | with `--strict` | unresolved `INPUT REQUIRED` |
| `unused` | no | indexed source nothing cites — either irrelevant, or a gap in the analysis |

`unused` is worth reading rather than dismissing. A source you gathered and
never cited usually means one of two things: it did not belong in the set, or
the analysis skipped something you thought mattered enough to collect.

## What the gate does not do

It checks that a number is attributed. It does not check that the number is
**in** the cited source. Only Stage V does that, by re-deriving from the source
without looking at the draft. Passing this gate means the output is
well-formed, not that it is true.
