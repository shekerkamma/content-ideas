# SimpleBrain Pattern

Reference model: `BuildGreatProducts/SimpleBrain`

Core shape:

- `raw/` — inbox for captured notes, links, PDFs, screenshots, and scraps
- `wiki/` — clean markdown notes written and maintained by the agent
- `projects/` — active project folders, each with its own `README.md`
- `archive/` — processed raw inputs moved here as a permanent record

Core operating loop:

1. Capture into `raw/`
2. Translate into `wiki/`
3. Move the source input into `archive/`

Important behavioral rules:

- The second brain is a knowledge system, not a coding repo.
- Read `README.md` first inside the target repo.
- Never overwrite a wiki note blindly; read and merge.
- Never mutate archived files.
- Keep everything in git so the history stays inspectable.
