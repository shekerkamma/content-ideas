---
name: notebooklm
description: Use when the user wants to turn research, architecture docs, or any written content into an interactive Gemini Notebook (formerly NotebookLM) with AI-generated explanations, audio overviews, or Q&A. Triggers on "upload to NotebookLM", "upload to Gemini Notebook", "create a notebook from this", "generate a briefing doc", "add this to my notebook", or any request for audio overview, FAQ, or study guide from a document. Invoked as sub-task by architecture-to-everything and architecture-presentation. Amplifies any research or content skill output.
---

# Gemini Notebook Skill

Drive Gemini Notebook in the browser: open the app, create or select a notebook,
upload a source, and trigger content generation.

> **Renamed.** NotebookLM became **Gemini Notebook** on 2026-07-16. Same product,
> same notebooks, same links. This skill keeps the directory name `notebooklm`
> because existing routing and orchestrators reference it; the product name in
> the UI is Gemini Notebook.

> **Domain moved.** The app now lives at **`notebook.google.com`**.
> `notebooklm.google.com` returns a permanent redirect (301, verified
> 2026-08-15). Google published no announcement of this move — no blog post, no
> Workspace Updates entry, no Help Center article. Navigate to the new domain
> directly; do not rely on the redirect surviving indefinitely.

---

## Tools required

- A browser-automation MCP. **Check which one is actually loaded before
  planning an automated run** — this varies by host and session:
  - `mcp__Claude_in_Chrome__*` — the original target of this skill
  - `mcp__playwright__*` — commonly what is available instead
- If neither is present, go straight to the manual fallback below. Do not
  announce an automated attempt you cannot make.

---

## Auth: never trust `auth refresh`'s exit code

`notebooklm auth refresh` (notebooklm-py 0.8.1) can print an empty
`Unexpected error:` and exit 2 **after the refresh has already succeeded**.
Observed 2026-08-15: that message appeared, and `auth check` immediately
reported "Authentication is valid" with live API calls working.

Use the wrapper instead of the bare command:

```bash
python3 "$SKILL_DIR/scripts/auth_refresh.py"             # refresh, verify, exit truthfully
python3 "$SKILL_DIR/scripts/auth_refresh.py" --check-only
python3 "$SKILL_DIR/scripts/auth_refresh.py" --json
```

It runs the refresh, **ignores the exit code**, and verifies observable session
state. Exit 0 means usable; exit 1 means an interactive login is genuinely
required.

**Never trigger `notebooklm login` off that exit code.** Login is an
interactive Google auth flow — sending the user through it because of a false
negative is the expensive mistake this prevents.

Mechanism, as far as it was narrowed: cookies are synced to
`storage_state.json` *before* the "Identifying Google account" step runs, so
the real work is done by the time that step can fail;
`cli/services/playwright_login.py:150` catches only
`(OSError, ValueError, RuntimeError, httpx.HTTPError)` and lets anything else
propagate; `cli/error_handler.py:450` then renders `str(e.args[0])`, so an
exception carrying an empty-string arg prints a blank message and exits 2. The
exact exception was **not identified** — it stopped reproducing once auth was
healthy. The wrapper does not depend on knowing it.

---

## What the account tier controls

Verified against Google's Help Center, *Use chat in Gemini Notebook*
(`support.google.com/gemininotebook/answer/16179559`), 2026-08-15:

| Capability | Availability |
|---|---|
| Upload sources, chat, citations, Audio Overview, briefing/FAQ/study guide | All tiers |
| Agentic chat: **running code**, web search, downloadable files | **Google AI Ultra & Pro only, desktop only** |
| Generated outputs: png/svg charts, PDF, Word, Markdown, text, images, CSV, json, **xlsx**, **pptx** | Ultra & Pro, desktop only |

Free tier gets the notebook, not the cloud computer. If a user on the free tier
asks for a spreadsheet or a deck out of a notebook, say plainly that their tier
cannot produce it rather than trying and failing.

**Quickest tier test:** upload a small table and ask for a spreadsheet. A
downloadable file means the cloud computer is active; a prose description of
the numbers means it is not. There is no setting to toggle.

Google labels these agentic functions "experimental and in early development."

---

## Workflow

### Step 1 — Prepare the source file
If the content is only in memory, write it to a file first. Markdown and plain
text are the safest; PDF and Word are also accepted. Limits: 500,000 words and
200 MB per source.

### Step 2 — Open Gemini Notebook
```
navigate → https://notebook.google.com
```
Wait for the page to load. If the user is not signed in, stop and ask them to
sign in to their Google account — do not attempt to handle login.

### Step 3 — Create a new notebook or open an existing one
**New:** click "New notebook", give it a name tied to the job it serves.
**Existing:** find it by name in the list and open it.

One notebook per job. A notebook that accumulates everything stops answering
anything well.

### Step 4 — Add the source
- Click "Add source" (or the + in the Sources panel)
- Choose "Upload file" and select the prepared file
- Wait for processing to finish (spinner disappears)

### Step 5 — Generate content

| User wants | Action |
|---|---|
| Overview / summary | "Notebook guide" → "Table of contents" or "Briefing doc" |
| Audio overview | "Audio overview" → "Generate" |
| FAQ / Q&A | "Notebook guide" → "FAQ" |
| Study guide | "Notebook guide" → "Study guide" |
| Just explore | Leave it — ready for the user to query |

**This skill does not drive the chat panel.** Everything above is a button.
Typing prompts into chat and reading replies back is not implemented here — if
that is what the user needs, say so rather than improvising clicks.

### Step 6 — Report back
Tell the user the notebook name, what was generated, and that they can query it
in the chat panel.

---

## Architecture Documentation variant

When used after generating an architecture document or draw.io diagram:

1. Write a structured markdown file with:
   - Title and one-paragraph summary
   - Layer-by-layer breakdown (what each component does and why)
   - Key data flows in plain English
   - Design decisions and trade-offs
2. Upload that file
3. Generate a **Briefing doc** — a professional written overview with context
4. Tell the user what they can now ask, for example:
   - "Why does the Tool Executor connect to MCP servers?"
   - "What happens when a user types a command?"
   - "Explain the Permission Manager's role"

---

## Manual fallback

Browser automation against this app fails often — the domain has historically
been restricted for Chrome MCP, the app moved domains in July 2026, and the
required MCP may not be loaded at all. Whenever automation is unavailable or
fails, hand the user these steps instead of retrying:

1. Open **https://notebook.google.com**
2. **"New notebook"** → name it
3. **"Add source"** → **"Upload file"** → select the file
4. Wait for the spinner to disappear
5. **"Notebook guide"** → **"Briefing doc"** (or FAQ / Study guide)

Then tell them what to ask in the chat panel.

---

## Mistakes to avoid
- Do NOT attempt to log in or handle Google auth — stop and ask the user to sign in
- Do NOT upload credentials, `.env` files, or API keys — check contents when in doubt
- Do NOT click "Generate audio" unless explicitly asked — it takes several minutes
- If a spinner is visible, wait — do not click again
- If upload fails, use "Paste text" instead
- Do NOT promise xlsx, pptx, or chart output without confirming the user is on Ultra or Pro

## You're done when
- The notebook exists with at least one source
- The requested content type has been triggered or generated
- The user knows the notebook name and what to do next

---

## Custom notebook skill template

To create a focused variant for one specific notebook:

```
Create a skill for me. Use the notebooklm skill as the foundation
but focused on the task below:

Skill Name:
Go to This Notebook: [paste the notebook.google.com URL]
Take this action: [e.g. "add today's research doc and generate a briefing"]
Mistakes to avoid: [anything specific]
You're done when: [completion condition]
Response to send: [what to say to the user when done]
```

---

## Skill Relationships

### Category
Business Automation

### Dependencies
- A browser-automation MCP (`mcp__Claude_in_Chrome__*` or `mcp__playwright__*`)
- Falls back to manual steps whenever no MCP is loaded or navigation fails

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `architecture-to-everything` | Orchestrated by | Stage 4 of full pipeline | receives `<system>-architecture.md` as upload source |
| `architecture-presentation` | Orchestrated by | Step 4 of the presentation pipeline | receives `<name>-architecture.md` as upload source |
| `content-research` | Amplifier | optional post-research enrichment | any `.md` research brief output |
| `openkb` | Amplifier | optional post-KB-compile enrichment | compiled wiki `.md` files |
| `source-set-workbench` | Peer | when claims must trace to sources and pass a gate | `SOURCES.md` manifest + `outputs/` |
| `research-to-deck` | Domain cluster | same research → structured output goal | — |

### Runtime Preamble
At invocation:
- "Checking which browser MCP is loaded — if none is, I'll give you the manual steps."
- "Make sure you're signed in to your Google account in the browser before I start."
- "Do you want a Briefing Doc, Audio Overview, FAQ, or Study Guide? (Default: Briefing Doc)"

---

## Gotchas

- **Automation is unreliable here.** The domain has been blocked at the domain
  level for Chrome MCP historically, and that claim has not been retested
  against the new `notebook.google.com`. Always have the manual fallback ready;
  never fail silently.
- **Agentic replies can leave your sources.** Google's Help Center states the
  Ultra/Pro chat experience works "with or without sources" and can search the
  web. Output may blend uploaded material with web content, so a notebook answer
  is not automatically source-grounded. Verify before reusing it as evidence —
  `source-set-workbench` exists for exactly this check.
- **Never attempt Google login.** Stop and ask the user to sign in manually.
- **Do NOT generate audio unless asked** — several minutes per run.
- **Source formats:** Markdown, text, PDF, and Word upload cleanly. `.drawio`
  does not — convert diagrams to markdown or PNG first. Cap: 500,000 words or
  200 MB per source; copy-protected PDFs are rejected.
- **Wait for the spinner.** Double-clicking creates duplicate sources.
- **Never upload credentials, env files, or API keys.**

---

## Verification

Checked 2026-08-15:

- `curl` confirmed `notebooklm.google.com` → **301** → `notebook.google.com`. PASS
- Tier and output-format table taken verbatim from Google's Help Center article
  *Use chat in Gemini Notebook* (`support.google.com/gemininotebook/answer/16179559`). PASS
- Rename date confirmed against the Google Workspace Updates post of 2026-07-16. PASS
- **NOT EXECUTED:** no browser run was performed against the new domain. Whether
  Chrome MCP is still blocked at `notebook.google.com`, and whether the Step 5
  button labels survived the rebrand, are both untested. Treat the click paths
  as a hypothesis until a real run is recorded here.

Executed 2026-08-15 against a live account via `notebooklm-py` 0.8.1 (a
programmatic path, not the browser path above):

- Tier confirmed **live**, not from Google's announcements: a chat request for a
  computed workbook produced artifact `marketing_channel_performance.xlsx`
  (type `File`, status `completed`). Code execution is active on this account.
- Its arithmetic was re-derived independently from the source table — aggregate
  CPL $39.56, CAC $354.90, ROAS 7.75x, Google Ads ROAS 5.50x — all four correct.
- `scripts/auth_refresh.py` verified on both branches: a stubbed exit-2 refresh
  with a valid session exits 0 and suppresses the false negative; a genuinely
  unauthenticated session exits 1 and directs the user to `notebooklm login`. PASS
- **Known CLI gap:** `notebooklm download` handles only named artifact types
  (audio, slide-deck, report, data-table, quiz, mind-map). A chat-generated
  `File` artifact has no download subcommand at 0.8.1 — retrieve it with
  `artifact export` or from the web UI.
