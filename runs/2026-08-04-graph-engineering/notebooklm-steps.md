# NotebookLM manual steps (optional)

Config has `include_notebooklm: true`. This is a manual step — no NotebookLM API is
available from this environment.

1. Go to https://notebooklm.google.com and create a new notebook.
2. Add these run artifacts as sources:
   - `transcript.txt` (full timestamped transcript)
   - `research.md` (grounding research)
   - `graph-engineering-story-architect-pack.md` (narrative spine)
3. Optional: generate an Audio Overview for a spoken-form recap of the deck's argument
   before sharing it with stakeholders.
4. Optional: ask NotebookLM follow-up questions against the transcript + research sources
   directly if a reviewer wants deeper source verification than the deck itself carries.
