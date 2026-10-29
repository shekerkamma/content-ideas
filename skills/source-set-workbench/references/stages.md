# Stages

Twelve stages. Ten are adapted from the source playbook; two — **Frame** and
**Verify** — are additions this repo requires and that playbook lacks.

Every stage prompt below assumes the source manifest is loaded and that every
factual line in the reply carries an `[Sn]` citation. That requirement is not
decoration: `scripts/check_output.py` enforces it, and an output that fails it
is not delivered.

---

## Stage 0 — Frame

Runs once, before any source is read. Skipping it is how a source set becomes a
pile.

Answer all four in `brief.md`:

1. What am I trying to figure out?
2. What information do I already have?
3. What information am I missing?
4. What do I want created at the end?

**The test for question 1:** "Research the US market" fails. "Decide whether we
enter the US in the next 12 months" passes. The difference is that the second
one can be wrong, so it can be checked.

**One source set = one job.** A set named after a decision stays useful. A set
named after a company becomes a junk drawer within a week.

**Gate:** `brief.md` has a decision in question 1 and a named artifact in
question 4. Neither is `TBD`.

---

## Stage 1 — Audit

The first instinct is to ask for the answer. Resist it for one turn. A model
handed thin sources will still produce a confident recommendation, and you
will not be able to tell that from a good one.

> Review every source in the manifest. My objective is: **[OBJECTIVE]**.
>
> Before any recommendation, give me:
>
> 1. What we know with reasonable confidence — cite `[Sn]` per line
> 2. What we are assuming — state the assumption, name what would confirm it
> 3. Which conclusions more than one source supports — name the sources
> 4. Where sources disagree — quote both sides, do not average them
> 5. What is missing
> 6. Which unanswered questions could change the decision
>
> Rank the missing information by how much it would move the decision, not by
> how easy it is to find.
>
> Do not give me the recommendation yet.

**Where sources disagree, keep both.** Averaging two conflicting numbers
produces a third number no source supports.

**Gate:** every line in 1 and 3 cites a manifest ID. Section 5 is non-empty —
if the model claims nothing is missing, the audit failed.

---

## Stage 2 — Rank the gaps, then fill them

> From the manifest as it stands, what important information is still missing?
>
> Sort into **Critical** (needed before deciding), **Important** (raises
> confidence), **Nice to have** (will not change the decision).
>
> For each gap: what is missing, why it matters, the exact question to answer,
> and the source type that would settle it — not a search term, a source type.
>
> Do not recommend research for the sake of more sources. If a gap cannot
> change the decision, put it in Nice to have and leave it there.

Then fill the Critical tier, in this order (repo-wide Research Tool Order):

1. **Local files** — never search for what is already in `sources/`
2. **GBrain** — `gbrain search "<topic>"` before any external call
3. **Exa** — `web_search_exa`, then `web_fetch_exa` for full text
4. **Firecrawl** — `firecrawl-pp-cli scrape --url <u> --max-age 0` for full-page
   ingestion; `--max-age 0` forces a live fetch instead of cache
5. **Specialist MCPs** — Microsoft Learn, GitHub, Notion, Drive
6. **WebSearch** — last, never first

Every fetched source lands in `sources/` and gets a manifest row with its
origin URL and retrieval date. A source you cannot cite by ID does not exist.

**Gate:** re-run `init_source_set.py` to index new sources. Every Critical gap
is either closed or explicitly carried into the output's Limitations section.

---

## Stage 3 — Falsify

Assembling sources for an idea you already like builds a confirmation-bias
machine, and it will pass every other stage.

> Assume this is wrong: **[HYPOTHESIS]**.
>
> Build the strongest evidence-based case against it from the manifest.
>
> 1. Strongest evidence against — cite `[Sn]`
> 2. The biggest assumptions we are making
> 3. Realistic failure scenarios, with the conditions that trigger them
> 4. What we still do not know
> 5. What evidence would flip the decision completely
>
> Do not write weak objections for the sake of balance. If the strongest case
> against is genuinely weak, say so and show why — that is a finding, not a
> failure.

Point 5 is the one to keep. A decision with no stated falsifier is a
preference wearing evidence as a costume.

**Gate:** point 5 names a specific, observable condition.

---

## Stage 4 — Data

> Analyze the datasets in the manifest. Objective: **[OBJECTIVE]**.
>
> **Before calculating anything**, report: missing values, duplicate records,
> inconsistent naming, date ranges that do not align, formatting problems,
> suspicious values, and any pair of datasets that should not be joined.
>
> Do not silently drop questionable rows. Show me what you would exclude and
> why, then let me decide.
>
> Then calculate what the data supports: **[METRICS]**.
>
> Close with: best and worst performers, anomalies, opportunities, problems to
> investigate, decisions this data supports, and **decisions this data does not
> support**.
>
> Show the derivation for every number.

**Route:** for anything beyond a single-file summary, hand off to `ai-analyst`
— it carries a source-tieout agent (pandas vs. SQL on foundational metrics,
halt on mismatch) and an independent validation agent. Do not re-implement
those here.

**Gate:** the quality pass is reported before any metric. The "does not
support" list is non-empty.

---

## Stage 5 — Deck

**Route, do not generate.** This repo has hard rules for client-facing PPTX and
this stage does not get to bypass them.

1. Route through the `present` skill to `branded-pptx-deck`.
2. Use `BRANDED_PPTX_TEMPLATE`, falling back to
   `~/.claude/templates/branded-template.pptx`. If neither resolves, stop and
   report the deck blocked. Do not ship an unbranded substitute.
3. Run `pptx-design-quality/scripts/check_claim_evidence.py` as a mechanical
   pre-pass, then `lint_pptx.py`, then review `preview_pptx.py` contact sheets.
4. Deliver with an explicit status and a matching filename suffix:
   `*-draft.pptx`, `*-reviewed.pptx`, `*-blocked.txt`. Only the reviewed file
   goes to `CLIENT_DELIVERY_DIR`.

Content contract per slide: an action-title verdict, real structure
(cards/table/scorecard), and evidence with its citation. Slide titles are
verdicts, not topics. Numbers beat adjectives.

> Build the deck for **[AUDIENCE]**, who must decide **[DECISION]**.
>
> Executive summary · current situation · key findings · the numbers ·
> opportunity · risks · options · recommendation · implementation · next steps.
>
> One idea per slide. Separate fact from assumption from recommendation
> visually, not just verbally. Use only evidence in the manifest, and carry the
> `[Sn]` citation onto the slide.

**Gate:** the four PPTX QA rules above, all four.

---

## Stage 6 — Model

> Build a financial model from the manifest's figures.
>
> Sheets: **Inputs** (every assumption, editable, one per row) · **Revenue** ·
> **Fixed costs** · **Variable costs** · **Unit economics** (gross margin,
> contribution margin, CAC, LTV, payback period, revenue per customer) ·
> **Scenarios** (conservative / base / aggressive, with the changed assumptions
> named per scenario).
>
> Never invent a missing number. Write `INPUT REQUIRED` in the cell.
>
> Close by naming which three assumptions move profitability most, and by how
> much.

That last instruction is the point of the stage. Most models are wrong about
the market and right about the software bill; the sensitivity ranking tells you
which error would actually cost you.

**Implementation:** `openpyxl` 3.1.5 is available system-wide. Write formulas,
not computed constants — a model whose cells are hardcoded values is a report.

**Gate:** `INPUT REQUIRED` appears wherever a source is silent. The sensitivity
ranking is present and ordered.

---

## Stage 7 — Report

> Turn the completed analysis into an executive report for **[AUDIENCE]**. The
> reader should not need the sources to follow it — but every claim carries its
> `[Sn]`.
>
> Executive summary · key numbers (only decision-relevant ones) · main findings
> · business impact · recommendations (what, why, evidence, expected impact,
> risk) · **limitations** · next steps.
>
> No generic recommendations. If a recommendation does not trace to a manifest
> source, cut it.

**Limitations is mandatory**, and it is where Stage 2's unclosed Critical gaps
go. A report that lists none is hiding them.

**Gate:** `check_output.py --strict`.

---

## Stage 8 — SOP

The company already knows how the process works; the knowledge is just spread
across Slack, transcripts, and one person's head. Reconstruct before you
prescribe.

> From everything in the manifest about **[PROCESS]**, first reconstruct how it
> works today:
>
> - **Documented process** — what the official docs say happens
> - **Actual process** — what transcripts, messages, and tickets show happens
> - **Contradictions** — where those two disagree, quoted, both sides
> - **Undocumented steps** — things people evidently do that no doc mentions
> - **Bottlenecks** — repeated manual work, duplicate entry, waiting, approval
>   delays, unclear ownership, unnecessary handoffs
>
> Then write the improved SOP: trigger · owner · inputs · steps · tools ·
> decision points · exceptions · quality checks · completion criteria.
>
> Where the sources cannot tell you, write `HUMAN INPUT REQUIRED`. Do not
> smooth over a gap with a plausible step.

The Documented-vs-Actual split is the whole value. An SOP written only from
docs describes a process nobody follows.

**Gate:** Contradictions is non-empty, or the reason it is empty is stated.

---

## Stage 9 — Call intelligence

> Compare closed-won against closed-lost conversations in the manifest.
>
> Differences in: problems named, urgency, objections, pricing reaction,
> competitors mentioned, decision-maker presence, company size, desired
> outcomes, stated reasons for delay and for buying.
>
> Then: what recurs in wins, what recurs in losses, **which objections actually
> correlate with losing versus which appear in both and therefore do not**,
> the customers' own words for their problem, what sales should change, what
> marketing should take.

The objection split is the finding worth having. Teams spend quarters
rehearsing rebuttals to objections that show up just as often in deals they
won.

**Caution:** won/lost pattern differences are correlational and the sample is
usually small and self-selected. Report counts, not percentages, below ~30
calls per side.

**Gate:** counts reported per pattern. No causal language on correlational
findings.

---

## Stage 10 — Chain

The stages compound; that is where the value is. Run them in order against one
manifest, one stage per turn.

> We will run this in stages. Do not skip ahead.
>
> 1 Audit · 2 Gaps, then fill · 3 Falsify · 4 Data · 5–7 Artifacts · V Verify
>
> Objective: **[OBJECTIVE]**. Start with Stage 1 only, then stop.

**Resumability:** the manifest, `brief.md`, and `outputs/` hold all the state.
A chain interrupted at Stage 4 resumes at Stage 4 with nothing in context.

---

## Stage V — Verify

**This stage does not exist in the source playbook. It is the one that catches
what the others miss.**

Rebuild the claim set **from the sources**, then compare it to the draft. Do
not audit the draft against itself — a checklist derived from an artifact
confirms the artifact, including its errors. This repo has already been burned
by exactly that: a 639-row evidence ledger built from slide headlines passed
every check, and rebuilt from the underlying sources it falsified the deck.

Procedure:

1. Run `check_output.py --strict` over every file in `outputs/`.
2. Take each of the draft's top claims. Open the cited source and re-derive the
   number **without looking at the draft**.
3. Any claim that does not survive re-derivation is cut or corrected — not
   softened with a hedge.
4. Record what you ran and what it found in the output's Verification section,
   with the date.

Ranking when evidence conflicts: **executed result, then primary source text,
then narration or summary.** An unexecuted claim is a hypothesis regardless of
how many stages it has passed.

**Gate:** the Verification section names the command, the date, and the count
of claims re-derived. `NOT VERIFIED` is an acceptable value; a missing section
is not.
