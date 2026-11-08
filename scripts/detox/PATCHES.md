# Local patches to Ben AI's /detox skill (2026-11-08)

The original was built for macOS. These patches make it work on Windows (and Linux) without changing what it does on a Mac.

- `scripts/gather_local.py`
  - Finds the Claude app data folder per OS: macOS `~/Library/Application Support/Claude`,
    Windows `%APPDATA%\Claude`, `%LOCALAPPDATA%\Claude` or the Store install's
    `%LOCALAPPDATA%\Packages\Claude_*\LocalCache\Roaming\Claude`, Linux `~/.config/Claude`.
    `DETOX_CLAUDE_APP_DIR` overrides it. Prints `app_dir` and warns when no sessions folder is found.
  - Path checks use forward slashes, so plugin, project and desktop skills are no longer
    labelled "not loaded" on Windows.
  - Reads and writes UTF-8 explicitly (Windows defaults to cp1252).
  - Scans transcripts in pure Python when neither `rg` nor `grep` is installed.
- `scripts/build_page.py`: UTF-8 file I/O; one skill counts once whether its path uses `\` or `/`.
- `SKILL.md`: checks that `/skill-doctor` output is the built-in usage table (a user skill with
  the same name can shadow it), warns before writing `detox-runs/` into a git repo, and warns
  before `manual_only` edits a SKILL.md inside a git repo.

## WSL / terminal mode (2026-11-08, second pass)

- `gather_local.py` follows symlinked skill folders (WSL links `~/.claude/skills/<name>` into a
  repo) with a loop guard, and also scans the current folder and the active folders.
- Without the desktop app it reads Claude Code CLI sessions from `~/.claude/projects` and prints
  `"mode": "terminal"`.
- Each skill row records `symlink_to` and `in_git_repo`. `checks.md` forbids `manual_only` and
  moving the real folder of a repo-owned skill; only the symlink may be moved. Repo mirrors are
  not reported as duplicates.
- `SKILL.md` has a terminal-mode section: what runs in the CLI, how to take ticks in chat when
  there is no Artifact tool, and which apply kinds work.
