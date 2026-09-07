---
name: notebooklm
description: Use when the user wants to turn research, architecture docs, or any written content into an interactive NotebookLM notebook with AI-generated explanations, audio overviews, or Q&A. Triggers on "upload to NotebookLM", "create a notebook from this", "generate a briefing doc", "add this to NotebookLM", or any request for audio overview, FAQ, or study guide from a document. Invoked as sub-task by architecture-to-everything and architecture-presentation. Amplifies any research or content skill output.
---

# NotebookLM Skill

Automate NotebookLM using the Chrome browser. You navigate to notebooklm.google.com, create or open a notebook, add a source, and trigger content generation.

---

## Tools required
- `mcp__Claude_in_Chrome__*` — all browser automation tools

---

## Workflow

### Step 1 — Prepare the source file
If the content is in memory (not yet saved), write it to a `.md` or `.txt` file in the working directory first. NotebookLM accepts uploaded files.

### Step 2 — Open NotebookLM
```
navigate → https://notebooklm.google.com
```
Wait for the page to load. If the user is not signed in, stop and ask them to sign in to their Google account first — do not attempt to handle login.

### Step 3 — Create a new notebook or open existing
**New notebook:**
- Click "New notebook" button
- Give it a meaningful name related to the content

**Existing notebook:**
- Find it by name in the notebook list and click it

### Step 4 — Add the source
- Click "Add source" (or the + button in the Sources panel)
- Choose "Upload file" and select the prepared `.md` or `.txt` file
- Wait for the source to finish processing (spinner disappears)

### Step 5 — Generate content (pick one based on user request)

| User wants | Action |
|---|---|
| Overview / summary | Click "Notebook guide" → "Table of contents" or "Briefing doc" |
| Audio overview | Click "Audio overview" → "Generate" |
| FAQ / Q&A | Click "Notebook guide" → "FAQ" |
| Study guide | Click "Notebook guide" → "Study guide" |
| Just explore | Leave it — the notebook is ready for the user to query |

### Step 6 — Report back
Tell the user:
- The notebook name
- What was generated
- That they can now ask questions in the chat panel on the right

---

## Architecture Documentation variant

When used after generating an architecture document or draw.io diagram, do this:

1. Write a structured markdown file with:
   - Title and one-paragraph summary
   - Layer-by-layer breakdown (what each component does and why)
   - Key data flows explained in plain English
   - Design decisions and trade-offs

2. Upload that file to NotebookLM

3. Generate a **Briefing doc** — this gives a professional written overview with context

4. Tell the user they can ask questions like:
   - "Why does the Tool Executor connect to MCP servers?"
   - "What happens when a user types a command?"
   - "Explain the Permission Manager's role"

---

## Known Limitation — Chrome MCP Domain Restriction
The Chrome MCP (`mcp__Claude_in_Chrome__navigate`) **cannot navigate to notebooklm.google.com** — it is blocked at the domain level. If navigation fails, stop and give the user these manual steps:

1. Open Chrome → go to **https://notebooklm.google.com**
2. Click **"New notebook"** → name it
3. **"Add source"** → **"Upload file"** → select the `.md` file
4. Wait for spinner to disappear
5. **"Notebook guide"** → **"Briefing doc"** (or FAQ / Study guide)

Then tell them what questions they can ask in the chat panel.

---

## Mistakes to avoid
- Do NOT attempt to log in or handle Google auth — stop and ask the user to sign in first
- Do NOT upload sensitive files (credentials, env files, API keys)
- Do NOT click "Generate audio" unless the user explicitly asks — it takes several minutes
- If a spinner is visible, wait — do not click again
- If the source fails to upload, try copy-pasting the text directly using "Paste text" option instead

## You're done when
- The notebook is created with at least one source added
- The requested content type (briefing, FAQ, audio, etc.) has been triggered or generated
- You've told the user the notebook name and what to do next

---

## Custom notebook skill template

To create a focused variant of this skill for a specific notebook, use this prompt:

```
Create a skill for me. Use the notebooklm skill as the foundation 
but focused on the task below:

Skill Name:
Go to This Notebook: [paste the NotebookLM URL]
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
- `mcp__Claude_in_Chrome__*` browser automation tools (for automated path)
- Falls back to manual steps when Chrome MCP cannot reach `notebooklm.google.com`

### Relationships
| Skill | Pattern | Condition | Handoff Artifact |
|---|---|---|---|
| `architecture-to-everything` | Orchestrated by | Stage 4 of full pipeline | receives `<system>-architecture.md` as upload source |
| `architecture-presentation` | Orchestrated by | Step 4 of the presentation pipeline | receives `<name>-architecture.md` as upload source |
| `content-research` | Amplifier | optional post-research enrichment | any `.md` research brief output |
| `openkb` | Amplifier | optional post-KB-compile enrichment | compiled wiki `.md` files |
| `research-to-deck` | Domain cluster | same research → structured output goal | — |

### Runtime Preamble
At invocation:
- "I'll attempt to automate this via Chrome MCP — but `notebooklm.google.com` is often blocked at the domain level. If automation fails, I'll give you 5 manual steps."
- "Make sure you're signed in to your Google account in Chrome before I start."
- "Do you want a Briefing Doc, Audio Overview, FAQ, or Study Guide? (Default: Briefing Doc)"

---

## Gotchas

- **Chrome MCP domain restriction:** `mcp__Claude_in_Chrome__navigate` cannot reach `notebooklm.google.com`. Always have the 5-step manual fallback ready — do not attempt automation silently and then fail without giving the user a path forward.
- **Never attempt Google login:** If the user is not signed in, stop immediately and ask them to sign in manually. Do not try to handle auth flows.
- **Do NOT generate audio overview unless explicitly asked:** Audio generation takes several minutes and costs the user time. Default to Briefing Doc.
- **Upload `.md` or `.txt` only:** NotebookLM does not accept `.drawio`, `.pptx`, or other binary formats as sources. Convert to markdown first.
- **Wait for spinner to complete:** After upload, do not click again until the spinner disappears. Double-clicking can create duplicate sources or corrupt the upload.
- **Never upload credentials, env files, or API keys:** Check file contents before upload if there's any doubt.
