# Frame evidence — what the captions could not carry

The first cut of this brief was built from `watch --detail transcript`: **zero frames.**
The video is a screencast; its substance is on screen, and the narration is the weakest
of the three evidence tiers this repo ranks (*execution → on-screen text → narration*).

Re-pulled at 1080p. The default download offers **only format 18, 640×360**, at which
none of the text below is legible; the format ladder needs
`--extractor-args "youtube:player_client=default,mweb,web_embedded"`.

---

## f_0319 — the slash-command menu (03:19)

- **Five design commands, not one:** `design`, `design-sync`, `design-revoke`,
  `design-consent`, plus `artifact-design` and `frontend-design`. The narration mentions
  only `/design`.
- **The full skill description is legible on screen** and states what the walkthrough
  never says: *"published as an Artifact… You DRAFT the design as .dc.html artboards laid
  out on one pan/zoom canvas; where saving is enabled for the user's account… Save
  publishes a new version for everyone, otherwise they get a view-and-export (PNG/PDF)
  preview."* He reads the first six words aloud and moves on.
- Host is the **Claude desktop app** (New / Artifacts / Routines / Customize), model
  **Opus 5**, effort **High**.

## f_0436 — the build log (04:36)

Five artboards, written as files, each announced:

| File | Lines | The agent's own words |
|---|---|---|
| `Editorial.dc.html` | +199 | "Direction 1 done. Now the terminal direction." |
| `Terminal.dc.html` | +196 | "Two down. Next: the brutalist poster grid." |
| `Brutalist.dc.html` | +176 | "Three down. Now the atmospheric dark direction." |
| `Aurora.dc.html` | +168 | "Four down. Last one: the Swiss spec-sheet." |
| `SpecSheet.dc.html` | +215 | — |
| `canvas.json` | +28 | "Now the entry artboard — a reference recreation of the current live site to compare against." |

- **954 lines of `.dc.html`** plus the manifest.
- *"Heredoc quoting is fighting the content; switching to the file writer."* — the agent
  hits a real tooling problem and adapts, on camera.
- *"Checks out. Loading the capability roster, then saving it."* → **Ran skill
  `/artifact-capabilities`** — the exact first-publish step the shipped skill prescribes.
- Published to `https://claude.ai/code/artifact/6d74e446-c21c-4ff6-82cc-4259be9a2564`.
- *"deliberately spread far apart rather than being shades of the same idea."*

## f_0750 — the properties panel (07:50)

Not "similar to Figma" — a DOM inspector:

- Tabs **Edit · Code · Tweaks** (the video never opens Code or Tweaks).
- **Sizing** Width/Height with `Hug | Fixed | Fill`; **Position** `Inline | Absolute`;
  **Padding**/**Margin** `None | All | X & Y | Individual`; **Appearance** background,
  radius, overflow, opacity; *Add: shadow · text shadow · transform · filter*.
- **Debug: `{"tid":25,"tag":"span","parent":"h1","attrs":{"class":"mark"}}`** — proof the
  artboard is real DOM, not a canvas drawing.
- **The Save button is visible top-right from 07:50** — four minutes before he "discovers"
  it at 11:53.

Claude's response text on the left is richer than anything narrated: it names `03a —
Brutalist, blue` and `03b — Brutalist, recomposed`, says *"Kept in orange so you're
comparing arrangement, not colour,"* reports **four bugs it found and fixed** in the
earlier boards, and **declines one change**: *"the 168px 'BRENDAN' … renders fine, and
shrinking it would change the look you picked, so I'd rather you eyeball it than have me
quietly reduce it."*

## f_1202 — the recovery (12:02)

The narration: *"the one thing I forgot to do is just to save the canvas."* The screen:

- *"Your save came through as a new version (`1787190748`, up from `1787189090`), which is
  why the earlier reads genuinely had nothing: the previous fetches were reading the older
  published version, not a cache. **I diffed all eight artboards; only `03a` changed, and
  only in three places**"* — then a table of the three edits, each marked applied.
- **It fixed a responsive bug in the human's edit:** the name block was fixed at
  789×148px against 168px type; re-expressed in `em` so it computes to exactly 789×148 at
  168px and scales. *"Verified at desktop and at 375px, no overflow either way."*
- **It flagged an accessibility defect and refused to auto-fix it:** white on `#FFCF2F` is
  *"about 1.5:1 contrast — effectively unreadable, especially at 13px… Your edit only
  changed the background, so I left the text colour alone rather than assume."*
- **It apologised for its own diagnosis:** *"I leaned on 'you probably didn't save' when
  the more useful move was to just ask you to save and re-check."*
- Version identity is explicit and addressable: `1787190748-9864`; local site
  `http://localhost:4173`.

---

## Why this matters for the brief

The transcript supports a deck about a command and a button. The frames support a deck
about an agent that writes named files, publishes versioned artifacts, diffs them to read
your hand-edits back, reviews your work, and declines to guess. Roughly **85% of the
substance is on screen and absent from the captions.**
