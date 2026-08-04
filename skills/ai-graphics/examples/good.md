# ai-graphics — worked examples (both produced correct output on the first render)

## Example 1 — Track B: organic style + typography → gpt-image

Whiteboard infographic. Note the anatomy: quoted verbatim copy, one zone per line,
closing RULES contract. This exact spec rendered with zero typos after three raw-prompt
FLUX attempts had all failed.

```
Render this design specification exactly as a whiteboard-style infographic image.

DESIGN SPEC
Canvas: vertical portrait poster, clean white dry-erase whiteboard background, subtle marker texture.
Style: hand-drawn dry-erase marker illustration; black, red and blue marker ink; neat legible
marker handwriting; every word spelled exactly as specified.

LAYOUT (top to bottom):
1. HEADER — bold black marker lettering, two lines, centered:
   Line 1: "3 REASONS TO REPLACE SaaS"
   Line 2: "WITH AI-BUILT TOOLS"
   A single hand-drawn blue underline beneath the header.
2. ROW 1 — a black hand-drawn circle containing the numeral "1"; beside it a red dollar-sign
   doodle with a small downward-trending curve; label in red marker: "CUT RECURRING COSTS"
3. ROW 2 — ... numeral "2"; blue padlock doodle; label in blue marker: "OWN YOUR SOFTWARE"
4. ROW 3 — ... numeral "3"; red puzzle-piece doodle; label in red marker: "BUILT EXACTLY FOR YOU"
5. FOOTER — small black marker arrow pointing right with the words "START SMALL. BUILD ONE TOOL."

RULES: exactly three numbered rows, no extra rows, no extra text, no logos, no watermark;
all spelling must match the spec exactly.
```

Command: `omniroute_image.py --provider codex --model codex/gpt-5.5 --size 1024x1536 --quality medium`

## Example 2 — Track A: reference reproduction → HTML/SVG → screenshot

Reference: an editorial three-tier orchestration diagram (cream paper, serif, one caramel
accent node). The protocol steps as actually executed:

**1. Inventory (counted):** 15 text items — title "Meta LOOP with Fable 5, GPT-5.6 and
Gemini 3.5 Flash"; captions "Chief Operator (GPT 5.6)", "Board Advisor (Fable 5)" +
"(On-demand consulted critic – not in hot path)"; orchestrator box (3 strings); advisor
box (3 strings); annotations "Main hot path: Plan → Delegate → Verify → Synthesize",
"premium 'taste and judgment' loop", "cheap parallel labor"; edge labels "Strategic &
Critique Consultation", "Delegated subtasks", "Results for verification", "Labor Layer:
Parallel cheap execution subtasks", "Team (Gemini Flash)"; 4 worker boxes (2 strings
each). Visual grammar: white rounded boxes w/ thin black border; ONE caramel box with
dashed dark-brown border; solid tan arrow out + DASHED grey return arrow; grey
self-loop on orchestrator; BIDIRECTIONAL arrow pairs to each of 4 workers.

**2. Code, data-first:** single inline SVG; every string is a `<text>` element, every
connector an explicit `<line>`/`<path>` with the correct dash/marker. Sampled colors:
bg `#f5ecdc`, node fill `#fbf6ea`, accent `#b5793a` / border `#6f4416`, arrows `#b3833f`,
muted grey `#9a8a72`. Fonts: Georgia/Times serif stack.

**3. Render:** `node scripts/html_to_png.mjs meta-loop.html out.png 1600x1000`

**4. QA diff:** Read the PNG, tick all 15 strings + all connector styles against the
inventory. First pass (before this protocol existed) shipped 6 of 15 items — the
counted checklist is what catches that.

Deliverable = PNG **plus** the HTML file (the editable template).
