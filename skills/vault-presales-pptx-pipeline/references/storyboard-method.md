# Storyboard method — where the storyline comes from

Written after a rebuild that took four attempts because this rule was ignored.

---

## RULE 0 — If a reference deck was provided, IT IS THE STORYLINE

**When the user hands you a reference document, they are handing you the storyboard.**
Do not invent an arc. Do not "improve" the structure. Extract its storyline and follow it
beat for beat.

> *"Why did I provide the reference deck, if you do not follow storyline — what for it is?"*

**What went wrong (2026-07-16):** given DeepGrid's 33-page Information Memorandum, an
adversarial IC arc was invented instead — *Conditional Proceed → the wedge inverts → eight
proofs → verdict*. It shared almost no structure with the reference. Three rounds of fixes
followed (visual variety, card density, jargon) and **none of them helped**, because the
defect was structural, not cosmetic. Rebuilding to the reference's arc fixed it in one pass.

**The tell you are about to make this mistake:** you are writing slide titles before you
have written down the reference's slide list.

### Do this first, always

```bash
python3 - << 'PY'
import fitz, re
d = fitz.open("<reference>.pdf")
for i, pg in enumerate(d, 1):
    t = pg.get_text().strip()
    if len(t) < 20:                       # image-only page → render and LOOK at it
        pg.get_pixmap(dpi=150).save(f"page_{i:02d}.png"); print(f"{i:>2}  [render page_{i:02d}.png]")
        continue
    lines = [l.strip() for l in t.split('\n') if l.strip()]
    print(f"{i:>2}  {lines[0][:70]}")
PY
```

Design-rich decks are mostly image-only pages — **render and read them**, don't trust the
text layer. Write the extracted storyline out as a numbered list *before* building anything,
and map every slide you plan onto one of its beats.

---

## Which storyline applies

| Situation | Storyline source |
|---|---|
| User provided a reference deck | **The reference. Rule 0. Not negotiable.** |
| Deck packet from vault notes, no reference | `references/deck-types.md` + `presales-story.md` spine |
| User explicitly asks for a different genre | Ask which arc, then follow that one |
| Genuinely no guidance | The IM arc below is a safe default for fundraising |

## The IM arc (extracted from the DeepGrid reference — reusable)

A fundraising Information Memorandum runs:

1. **Cover** — company, one-line identity, the ask, 3–4 proof KPIs
2. **What the company is** — plain identity + the 3–4 pillars that make it viable
3. **The platform** — the value chain, one asset → many revenue lines
4. **Five reasons this wins** — the investment thesis, numbered
5. **Market opportunity** — demand, and why it is structural (mandate/regulation) not hoped-for
6. **The solution** — what is actually sold, in 3 columns
7. **Product architecture / the moat** — the technical claim, with the headroom or margin proof
8. **Use case** — one concrete deployment, drawn
9. **Pricing family** — the ladder, with the primary lane marked
10. **Unit architecture** — how one investment yields many revenues
11. **The differentiator** — the thing competitors cannot copy from a spec sheet
12. **Proof of execution** — what is DONE, what is CONTRACTED, what the raise buys
13. **Competitive positioning** — where we win, and where we don't pretend to
14. **Financials** — revenue + margin trajectory, and what converts it
15. **Unit economics** — the numbers investors habitually confuse, separated
16. **The ask + use of proceeds + milestones**
17. **Team & governance**
18. **Close** — the mission restated, reasons to move now, exit vectors

**Act rhythm:** identity (1–3) → thesis (4–6) → proof (7–12) → judgment (13–15) → ask (16–18).

## Arc integrity — the check that catches real defects

Read the titles in sequence, ignoring the bodies. Then test:

- **Does any evidence sit downstream of the action it supports?** Fatal. Evidence → judgment
  → action, always. (Caught exactly this in a v2: the diligence plan sat at 15 with three
  more evidence slides after it, then the verdict at 19.)
- Does the resolution sit immediately before the ask, or is it buried mid-deck?
- Is any beat doing a job an earlier beat already did?
- If a reader stopped after slide 2, would they know the answer?

## Upgrading someone else's deck (`genspark-upgrade` deck type)

You are rebuilding **their** deck, in **their** voice, arguing **their** case — with the
defects fixed. You are not writing a critique of it.

**Corrections belong on the slide, stated openly.** Do not silently fix and do not hide.
A withdrawn claim, named as withdrawn, is stronger than one quietly deleted — because the
reader will check, and being first to your own bad news buys credibility for everything else.

Pattern that works:

> *"Earlier versions of this memorandum cited GSR 184(E) as live from April 2026. That date
> comes from a March-2025 draft and was superseded by the ministerial reply above. We present
> the operative dates — October 2027 and January 2028 — because the tape-out clock still fits
> inside them, and because an investor will check."*

**Correction ledger from the DeepGrid rebuild — the shape to copy:**

| Source deck | Rebuild | Handling |
|---|---|---|
| Mandate "live April 2026" | Oct 2027 / Jan 2028 | Corrected + **stated as withdrawn on the slide** |
| ₹1,128 Cr cover vs ₹1,388 Cr in its own P&L | ₹1,388 Cr | Corrected + the discrepancy named |
| NRE $2.42M / ~$3M / $630K, unreconciled | $630K MPW = line item **inside** $2.42M | Relationship stated |
| Competitor prices ₹5–18L, uncited | **Removed** | Removal explained on-slide |
| Uncited TAM | Marked management estimate | Or cut |
| *(absent)* | **+₹45 Cr DLI incentives** | **Added — strengthens their ask** |
| *(absent)* | ISO 26262 gap | **Added — "what we are not claiming"** |

The last two rows are the point: **an upgrade should argue better than the original.** Their
deck omitted ₹45 crore of official non-dilutive capital available against their own ₹45 crore
ask. Finding that is worth more than any layout fix.

## Verify corrections held

A corrected figure must appear **only** as a withdrawal — never asserted. Always context-check:

```python
for i,s in enumerate(p.slides,1):
    for x in s.shapes:
        if x.has_text_frame and ('April 2026' in x.text_frame.text or '1,128' in x.text_frame.text):
            print(i, x.text_frame.text[:200])     # must read as "earlier versions said…"
```

A raw count is not enough — a banned figure legitimately appears inside its own disavowal.
Same trap applies to scans generally: Mobileye's *real filed quarters* ("Q4 2024") will hit a
"fabricated date" regex. **Print the surrounding text before calling anything a defect.**

## Slide language

- **Titles are assertions**, never topic labels. "The chip was never the expensive part" —
  not "Cost Analysis".
- **No insider jargon.** "Wedge", "BLUF", "price-fit", "conditional proceed" are *your*
  vocabulary, not the reader's. A cover title that needs a glossary has failed. 13 uses of
  "wedge" survived into a deck before this was caught.
- **Plain, concrete, cold-readable.** If the first slide doesn't land on someone who knows
  nothing, nothing after it will.

## Anti-patterns

- Inventing an arc when a reference was supplied. **Rule 0.**
- Polishing visuals to fix a structural problem. Card heights never fixed a broken arc.
- One layout repeated (v1 was L12 ×10 of 20 slides — "table + two cards", over and over).
- Stating a proportion in words instead of drawing it (`proportion()` exists for this).
- Fixed-height cards. `'auto'` or it reads as junk.
- A deck that critiques its subject when the job was to rebuild its subject's pitch.
