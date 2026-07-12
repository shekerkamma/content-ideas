# Genspark Branded Deck Validation

Status: reviewed

Reviewed output: `claude-code-course-genspark-branded-reviewed.pptx`

Slide count: 32

QA completed:
- Rendered all slides at 2560x1440 through the Genspark HTML/CSS workflow.
- Built image-per-slide PPTX from the rendered PNGs.
- Confirmed PPTX structure contains 32 slides and 32 media images.
- Generated three contact sheets and visually checked for blank slides, collisions, clipping, and incoherent layout.
- Scanned visible source text for internal production language and removed the flagged wording.

Narrative structure:
- Opens with the thesis that Claude Code is a delivery system, not a tool lesson.
- Builds through setup, command surface, project rules, skills, website delivery, automations, enterprise dashboards, support agents, and planning discipline.
- Closes with pricing logic, sales discipline, a practical 30-day rollout, and a decision slide.

Editability note:
- This is a client-ready rendered PPTX. PowerPoint slides are image-based.
- Source edits should be made in `deck.html`, `theme.css`, and `deck.css`, then rerendered through the same workflow.
