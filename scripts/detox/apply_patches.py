#!/usr/bin/env python3
"""Rebuild the patched /detox skill from your own copy of Ben AI's original zip.

The detox skill is Ben AI's work (free download, no licence), so this public repo
does not carry it. It carries only these patches. Run this on each machine to
build the skill into vendor/detox/ (gitignored), then let dual-host link it:

    python3 scripts/detox/apply_patches.py --zip /mnt/c/Users/<you>/Downloads/detox.zip
    ln -s "$PWD/vendor/detox" ~/.claude/skills/detox        # dual-host: symlink on WSL

What it does, in order, and it stops on the first problem:
  1. checks the zip's SHA-256 against manifest.json (the exact original we patched),
  2. extracts it to a temp folder, refusing any entry outside detox/,
  3. applies three patch steps (Windows paths and UTF-8; app-folder detection;
     WSL terminal mode, symlinked skills, repo-owned skill safety),
  4. adds PATCHES.md, then checks every output file's SHA-256 against manifest.json,
  5. moves the result to --out. An existing folder is moved aside, never deleted.

Stdlib only. Exit 0 ok, 1 a check failed, 2 usage.
"""
import argparse
import hashlib
import json
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
MANIFEST = HERE / "manifest.json"


class PatchError(Exception):
    pass


def sub(text, old, new, count=1):
    """Replace `old` exactly `count` times, or fail: the original must be the one we patched."""
    n = text.count(old)
    if n != count:
        raise PatchError(f"expected {count} of {old[:60]!r}, found {n}")
    return text.replace(old, new)


def step1_windows_paths_and_utf8(root):
    """gather_local.py / build_page.py / SKILL.md: OS app folder, slash-safe paths, UTF-8, no-grep scan."""
    # ---------------- gather_local.py ----------------
    g = root / "scripts/gather_local.py"
    t = g.read_text(encoding="utf-8")

    t = sub(t, '''HOME = Path.home()
APP = HOME / "Library/Application Support/Claude"
''', '''HOME = Path.home()


def claude_app_dir():
    """Claude desktop app data folder for this OS.

    macOS: ~/Library/Application Support/Claude
    Windows: %APPDATA%\\\\Claude (Roaming), else %LOCALAPPDATA%\\\\Claude
    Linux: $XDG_CONFIG_HOME/Claude or ~/.config/Claude
    DETOX_CLAUDE_APP_DIR overrides all of these.
    """
    override = os.environ.get("DETOX_CLAUDE_APP_DIR")
    if override:
        return Path(override)
    if sys.platform == "darwin":
        return HOME / "Library/Application Support/Claude"
    if os.name == "nt":
        for var in ("APPDATA", "LOCALAPPDATA"):
            base = os.environ.get(var)
            if base and (Path(base) / "Claude").exists():
                return Path(base) / "Claude"
        return Path(os.environ.get("APPDATA") or HOME / "AppData/Roaming") / "Claude"
    return Path(os.environ.get("XDG_CONFIG_HOME") or HOME / ".config") / "Claude"


def norm(p):
    """Path as a forward-slash string, so the same checks work on Windows."""
    return str(p).replace("\\\\", "/")


APP = claude_app_dir()
HOME_S = norm(HOME)
''')

    # explicit UTF-8 everywhere (Windows defaults to cp1252)
    t = sub(t, 'd = json.loads(f.read_text())', 'd = json.loads(f.read_text(encoding="utf-8"))')
    t = sub(t, 'frontmatter(sk.read_text())', 'frontmatter(sk.read_text(encoding="utf-8", errors="replace"))')
    t = sub(t, 'json.loads((base / "switches.json").read_text())', 'json.loads((base / "switches.json").read_text(encoding="utf-8"))')
    t = sub(t, 'json.loads(pj.read_text())', 'json.loads(pj.read_text(encoding="utf-8"))')
    t = sub(t, '(HOME / ".claude/settings.json").read_text()', '(HOME / ".claude/settings.json").read_text(encoding="utf-8")')
    t = sub(t, 'read_text(errors="replace")', 'read_text(encoding="utf-8", errors="replace")', 3)
    t = sub(t, '(out / name).write_text(json.dumps(data, indent=1, default=list))',
            '(out / name).write_text(json.dumps(data, indent=1, default=list), encoding="utf-8")')
    t = sub(t, 'text=True, errors="replace")', 'text=True, encoding="utf-8", errors="replace")')

    # grep_lines: pure-Python fallback when neither rg nor grep exists (stock Windows)
    t = sub(t, '''    if cmd is None:
        cmd = ["grep", "-rhE", "--include", include, TOOL_RE] + roots
        exe = None
''', '''    if cmd is None and shutil.which("grep"):
        cmd = ["grep", "-rhE", "--include", include, TOOL_RE] + roots
        exe = None
    if cmd is None:
        pat = re.compile(TOOL_RE)
        for r in roots:
            for f in Path(r).rglob(include):
                try:
                    with open(f, encoding="utf-8", errors="replace") as fh:
                        for line in fh:
                            if pat.search(line):
                                yield line
                except OSError:
                    continue
        return
''')

    # find_skill_files: normalise dirpath before the slash checks
    t = sub(t, '''            if "/.claude/projects" in dirpath or "/scheduled-tasks" in dirpath:''',
            '''            dp = norm(dirpath)
            if "/.claude/projects" in dp or "/scheduled-tasks" in dp:''')

    # location_of / plugin_prefix: compare forward-slash strings
    t = sub(t, '''def location_of(path):
    s = str(path)
    if "/local-agent-mode-sessions/skills-plugin/" in s:
        return "desktop-harness"
    if s.startswith(str(HOME / ".claude/skills")):
        return "global"
    if s.startswith(str(HOME / ".claude/plugins")):''', '''def location_of(path):
    s = norm(path)
    if "/local-agent-mode-sessions/skills-plugin/" in s:
        return "desktop-harness"
    if s.startswith(HOME_S + "/.claude/skills/"):
        return "global"
    if s.startswith(HOME_S + "/.claude/plugins/"):''')
    t = sub(t, 'm = re.search(r"/plugins/(?:cache|marketplaces|synced)/[^/]+/([^/]+)/", str(path))',
            'm = re.search(r"/plugins/(?:cache|marketplaces|synced)/[^/]+/([^/]+)/", norm(path))')

    # skills.json path field: keep forward slashes so build_page target_key strips /SKILL.md
    t = sub(t, '"path": str(p),\n            "description"', '"path": norm(p),\n            "description"')
    g.write_text(t, encoding="utf-8")

    # ---------------- build_page.py ----------------
    b = root / "scripts/build_page.py"
    t = b.read_text(encoding="utf-8")
    t = sub(t, 'with open(p) as f:', 'with open(p, encoding="utf-8") as f:')
    t = sub(t, 'for line in open(path):', 'for line in open(path, encoding="utf-8", errors="replace"):')
    t = sub(t, 'open(os.path.join(here, "..", "assets", "page.html")).read()', 'open(os.path.join(here, "..", "assets", "page.html"), encoding="utf-8").read()')
    t = sub(t, 'open(os.path.join(here, "..", "assets", "logo.svg")).read()', 'open(os.path.join(here, "..", "assets", "logo.svg"), encoding="utf-8").read()')
    t = sub(t, 'with open(os.path.join(out, "index.html"), "w") as f:', 'with open(os.path.join(out, "index.html"), "w", encoding="utf-8") as f:')
    t = sub(t, 'with open(os.path.join(out, "state.json"), "w") as f:', 'with open(os.path.join(out, "state.json"), "w", encoding="utf-8") as f:')
    t = sub(t, '''    if isinstance(ref, str) and ref.endswith("/SKILL.md"):
        ref = ref[: -len("/SKILL.md")]''', '''    if isinstance(ref, str):
        ref = ref.replace("\\\\", "/")
        if ref.endswith("/SKILL.md"):
            ref = ref[: -len("/SKILL.md")]''')
    b.write_text(t, encoding="utf-8")

    # ---------------- SKILL.md ----------------
    s = root / "SKILL.md"
    t = s.read_text(encoding="utf-8")
    t = sub(t, '''Run them from the user's main active folder.''', '''On Windows, use `python` if `python3` is not on PATH. The Code tab runs these in Git Bash, which has `perl`.

Check `skill_doctor.txt` before using it. It must be the built-in skill usage table (skills, context cost, uses, last used). Some setups have their own skill named `skill-doctor` that does something else, such as repairing corrupted skill files. If the output is not the usage table, ignore the file and use `skills.json` and `context_usage.txt` only. Say so in the skills `note`.

Run them from the user's main active folder.''')
    t = sub(t, '''Make the run folder: `detox-runs/YYYY-MM-DD/raw/` inside the current folder.''',
            '''Make the run folder: `detox-runs/YYYY-MM-DD/raw/` inside the current folder. If the current folder is a git repository, tell the user and suggest adding `detox-runs/` to its `.gitignore`. Do not edit `.gitignore` without a yes.''')
    t = sub(t, '''| `manual_only` | add `disable-model-invocation: true` to the SKILL.md front matter |''',
            '''| `manual_only` | add `disable-model-invocation: true` to the SKILL.md front matter. If the file is inside a git repository, say so first: the repo may keep copies that must match |''')
    s.write_text(t, encoding="utf-8")


def step2_app_folder_detection(root):
    """Windows Store install folder, DETOX_CLAUDE_APP_DIR, and a visible app_dir line."""
    g = root / "scripts/gather_local.py"
    t = g.read_text(encoding="utf-8")
    t = sub(t, '''    if os.name == "nt":
        for var in ("APPDATA", "LOCALAPPDATA"):
            base = os.environ.get(var)
            if base and (Path(base) / "Claude").exists():
                return Path(base) / "Claude"
        return Path(os.environ.get("APPDATA") or HOME / "AppData/Roaming") / "Claude"
''', '''    if os.name == "nt":
        roaming = Path(os.environ.get("APPDATA") or HOME / "AppData/Roaming")
        local = Path(os.environ.get("LOCALAPPDATA") or HOME / "AppData/Local")
        # Classic installer, then the Store/MSIX install, which keeps its data in a package folder.
        cands = [roaming / "Claude", local / "Claude"]
        cands += sorted(local.glob("Packages/Claude_*/LocalCache/Roaming/Claude")) if local.exists() else []
        for c in cands:
            if (c / "claude-code-sessions").exists():
                return c
        for c in cands:
            if c.exists():
                return c
        return roaming / "Claude"
''')
    t = sub(t, '''    print(json.dumps({"out": str(out), "seconds": round(time.time() - t0, 1),''',
     '''    if not CODE_SESSIONS.exists():
        print(f"warning: no Code-tab sessions folder at {CODE_SESSIONS}. Chat and scheduled-task "
              "tables will be empty. Set DETOX_CLAUDE_APP_DIR to the Claude app data folder.",
              file=sys.stderr)
    print(json.dumps({"out": str(out), "app_dir": str(APP), "seconds": round(time.time() - t0, 1),''')
    g.write_text(t, encoding="utf-8")
    # SKILL.md: tell Claude to read the warning
    s = root / "SKILL.md"
    t = s.read_text(encoding="utf-8")
    t = sub(t, '''On Windows, use `python` if `python3` is not on PATH.''', '''`gather_local.py` prints `app_dir`, the Claude app data folder it read. If it warns that there is no sessions folder, tell the user the interface and scheduled parts will be empty, and ask for the right folder (it goes in `DETOX_CLAUDE_APP_DIR`). On Windows, use `python` if `python3` is not on PATH.''')
    s.write_text(t, encoding="utf-8")


def step3_wsl_terminal_mode(root):
    """CLI sessions from ~/.claude/projects, symlinked skills, repo-owned skill safety."""
    g = root / "scripts/gather_local.py"; t = g.read_text(encoding="utf-8")

    # 1. CLI sessions from ~/.claude/projects when there is no desktop app (WSL, Linux, terminal-only)
    t = sub(t, '''def gather_sessions():
    rows = read_sessions(CODE_SESSIONS)
''', '''def first_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        for b in content:
            if isinstance(b, dict) and b.get("type") == "text":
                return b.get("text") or ""
    return ""


def read_cli_sessions():
    """Claude Code CLI sessions (no desktop app): one transcript per session in ~/.claude/projects.

    Title = the summary line if there is one, else the first real user message.
    Last active = file modified time. These cannot be archived by a tool: rows are info or flag.
    """
    rows = []
    if not PROJECTS.exists():
        return rows
    for f in PROJECTS.glob("*/*.jsonl"):
        title, cwd, model, created = "", "", None, None
        try:
            with open(f, encoding="utf-8", errors="replace") as fh:
                for i, line in enumerate(fh):
                    if i > 200 or (title and cwd and model):
                        break
                    try:
                        d = json.loads(line)
                    except Exception:
                        continue
                    cwd = cwd or d.get("cwd") or ""
                    created = created or iso_to_epoch(d.get("timestamp") or "")
                    if d.get("type") == "summary" and d.get("summary"):
                        title = d["summary"]
                    m = d.get("message") if isinstance(d.get("message"), dict) else {}
                    if not title and d.get("type") == "user" and not d.get("isMeta"):
                        txt = first_text(m.get("content")).strip()
                        if txt and not txt.startswith("<"):
                            title = txt.splitlines()[0][:80]
                    if d.get("type") == "assistant" and m.get("model"):
                        model = model or m["model"]
            last = f.stat().st_mtime
        except OSError:
            continue
        rows.append({"id": f.stem, "title": title, "cwd": cwd, "source": "cli",
                     "created_days_ago": days_ago(created), "last_active_days_ago": days_ago(last),
                     "archived": False, "model": model, "scheduled_task": None, "error": "",
                     "transcript": norm(f), "_last": last})
    rows.sort(key=lambda r: -r["_last"])
    return rows


def gather_sessions():
    rows = read_sessions(CODE_SESSIONS)
    if not CODE_SESSIONS.exists():
        rows = read_cli_sessions()
''')

    # 2. follow symlinked skill folders (WSL links ~/.claude/skills/<name> into a repo), loop-safe,
    #    and also scan the current folder and the active folders
    t = sub(t, '''def find_skill_files():
    roots = [HOME / ".claude", HOME / "Documents", HOME / "dev", HOME / "Desktop", HOME / "Projects",
             APP / "local-agent-mode-sessions/skills-plugin"]
    seen = set()
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root):
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith("._")]''',
    '''def find_skill_files(extra_roots=()):
    roots = [HOME / ".claude", HOME / "Documents", HOME / "dev", HOME / "Desktop", HOME / "Projects",
             APP / "local-agent-mode-sessions/skills-plugin"] + [Path(r) for r in extra_roots]
    seen = set()
    walked = set()
    for root in roots:
        if not root.exists():
            continue
        for dirpath, dirnames, filenames in os.walk(root, followlinks=True):
            real = os.path.realpath(dirpath)
            if real in walked:
                dirnames[:] = []
                continue
            walked.add(real)
            dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS and not d.startswith("._")]''')

    # 3. mark skills whose real file sits in a git repo, and symlinks
    t = sub(t, '''def gather_skills(usage):
    rows = []
    for p in find_skill_files():''', '''def git_root(path):
    """Top folder of the git repository that holds `path`, or None."""
    p = Path(os.path.realpath(path)).parent
    for d in [p, *p.parents]:
        if (d / ".git").exists():
            return norm(d)
    return None


def gather_skills(usage, extra_roots=()):
    rows = []
    for p in find_skill_files(extra_roots):''')
    t = sub(t, '''            "md5": hashlib.md5(text.encode()).hexdigest(),
        })''', '''            "md5": hashlib.md5(text.encode()).hexdigest(),
            "symlink_to": norm(os.path.realpath(p.parent)) if os.path.islink(p.parent) else None,
            "in_git_repo": git_root(p),
        })''')
    t = sub(t, '''        "skills.json": {"skills": gather_skills(usage), "skill_calls_seen": usage},''',
            '''        "skills.json": {"skills": gather_skills(usage, [Path.cwd(), *active]), "skill_calls_seen": usage},''')
    t = sub(t, '''    if not CODE_SESSIONS.exists():
        print(f"warning: no Code-tab sessions folder at {CODE_SESSIONS}. Chat and scheduled-task "
              "tables will be empty. Set DETOX_CLAUDE_APP_DIR to the Claude app data folder.",
              file=sys.stderr)''', '''    if not CODE_SESSIONS.exists():
        print(f"note: no Claude desktop app data at {APP}. Read Claude Code CLI sessions from "
              f"{PROJECTS} instead (terminal mode). Set DETOX_CLAUDE_APP_DIR if the app is installed "
              "somewhere else.", file=sys.stderr)''')
    t = sub(t, '''"app_dir": str(APP),''', '''"app_dir": str(APP), "mode": "app" if CODE_SESSIONS.exists() else "terminal",''')
    g.write_text(t, encoding="utf-8")

    # ---- SKILL.md: terminal mode (WSL / Linux CLI) ----
    s = root / "SKILL.md"; t = s.read_text(encoding="utf-8")
    t = sub(t, '''If the session tools (`ccd_session_mgmt`, `ccd_sidebar`) are missing, this is Cowork or the web. Tell the user what will not work there: moving or archiving chats, sidebar sections, running /skill-doctor, reading Code-tab files. Suggest the Code tab in the Claude desktop app. If they stay, run only the parts that work.''',
    '''If the session tools (`ccd_session_mgmt`, `ccd_sidebar`) are missing, check whether this is the Claude Code CLI in a terminal (WSL, Linux, macOS terminal): there is a Bash tool and `~/.claude/projects` exists. Then run in **terminal mode** (below). Otherwise this is Cowork or the web: tell the user what will not work there (moving or archiving chats, sidebar sections, running /skill-doctor, reading Code-tab files), suggest the Code tab in the Claude desktop app, and if they stay, run only the parts that work.

### Terminal mode (Claude Code CLI, for example on WSL)

`gather_local.py` prints `"mode": "terminal"` and reads CLI sessions from `~/.claude/projects` instead of the desktop app. Say this in the first message. In terminal mode:

- Skills, memory and context: full, the same as in the app. These are the main value here.
- Connectors: use `context_usage.txt` (`/context`) and `connectors.json` for cost and use. There is no `ccd_connectors`, so every connector row is `flag` ("switch it off with `/mcp` or in settings"), never `connector_off`.
- Interface: CLI sessions are `info` rows only (idle 30+ days, test and one-off titles). No archive, delete, sections or pins. Skip `sidebar_sessions.json`, `sidebar.json`. Artifacts and mods only if those tools or folders exist.
- Scheduled: only the tasks `gather_local.py` finds on disk. Skip `RemoteTrigger` if the tool is missing.
- The page: if the `Artifact` tool exists, publish as in step 4. If not, build it, give the user the path of `<run>/page/index.html` to open in a browser (on WSL: `explorer.exe "$(wslpath -w <path>)"`), and take the ticks in chat: row ids, or "all of table <id>". Then go on from step 5.3.
- Apply kinds that work: `move_skill`, `manual_only`, `edit_file`, `create_file`, `mod_switch`, `mod_delete`, `none`. Any other kind: tell the user it needs the desktop app.''')
    t = sub(t, '''| `move_skill` | `mv` the skill folder to `~/.claude/detox-backup/YYYY-MM-DD/` |''',
            '''| `move_skill` | `mv` the skill folder to `~/.claude/detox-backup/YYYY-MM-DD/`. If the skill folder is a symlink, move the link only, never the folder it points to |''')
    s.write_text(t, encoding="utf-8")

    # ---- checks.md: never touch repo-owned skills ----
    c = root / "references/checks.md"; t = c.read_text(encoding="utf-8")
    t = sub(t, '''"Loaded" means /skill-doctor lists it''', '''Repo-owned skills: a row whose `in_git_repo` is set lives in a git repository (often reached through a symlink, `symlink_to`). Never offer `manual_only` on it, and never offer `move_skill` on its real folder: the repo may keep copies that must stay identical and tests that check them. Offer `move_skill` only on the symlink in `~/.claude/skills` (that unloads it without touching the repo), otherwise make the row `flag` with "change it in the repo". Copies of the same skill inside one repo (for example `skills/x` and `plugins/<name>/skills/x`) are intended mirrors, not duplicates: do not list them in the duplicates table.

"Loaded" means /skill-doctor lists it''')
    c.write_text(t, encoding="utf-8")


STEPS = (step1_windows_paths_and_utf8, step2_app_folder_detection, step3_wsl_terminal_mode)


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def default_zip():
    import getpass
    import os
    cands = [os.environ.get("DETOX_ZIP"), Path.home() / "Downloads/detox.zip"]
    for user in {getpass.getuser(), os.environ.get("USER", ""), "sheke"} - {""}:
        cands.append(Path(f"/mnt/c/Users/{user}/Downloads/detox.zip"))
    for c in cands:
        if c and Path(c).is_file():
            return Path(c)
    return None


def build(zip_path, manifest):
    """Extract, patch and verify into a temp folder. Returns the patched detox/ path."""
    got = sha256(zip_path)
    if got != manifest["original_zip_sha256"]:
        raise PatchError(f"{zip_path} is not the detox.zip these patches were made for "
                         f"(sha256 {got}). Re-download it, or update the patches.")
    tmp = Path(tempfile.mkdtemp(prefix="detox-build-"))
    with zipfile.ZipFile(zip_path) as z:
        for name in z.namelist():
            p = Path(name)
            if p.is_absolute() or ".." in p.parts or p.parts[0] != "detox":
                raise PatchError(f"unexpected zip entry {name!r}")
        z.extractall(tmp)
    root = tmp / "detox"
    for step in STEPS:
        step(root)
    shutil.copyfile(HERE / "PATCHES.md", root / "PATCHES.md")
    want = manifest["patched_files_sha256"]
    have = {p.relative_to(root).as_posix(): sha256(p) for p in root.rglob("*") if p.is_file()}
    if have != want:
        diff = sorted(k for k in set(want) | set(have) if want.get(k) != have.get(k))
        raise PatchError(f"patched output does not match manifest.json: {diff}")
    return root


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--zip", type=Path, help="Ben AI's original detox.zip (default: DETOX_ZIP or ~/Downloads)")
    ap.add_argument("--out", type=Path, default=REPO / "vendor/detox", help="where to put the patched skill")
    a = ap.parse_args(argv)
    zip_path = a.zip or default_zip()
    if not zip_path or not zip_path.is_file():
        print("error: pass --zip <path to Ben AI's detox.zip>", file=sys.stderr)
        return 2
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    try:
        built = build(zip_path, manifest)
    except PatchError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    out = a.out.resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    if out.exists() or out.is_symlink():
        aside = out.with_name(f"{out.name}.bak-{time.strftime('%Y%m%d-%H%M%S')}")
        out.rename(aside)
        print(f"previous {out.name} moved to {aside}")
    shutil.move(str(built), str(out))
    print(f"built {out} ({len(manifest['patched_files_sha256'])} files, all match manifest.json)")
    print("link it on WSL (dual-host rule for skills):")
    print(f'  ln -s "{out}" ~/.claude/skills/detox')
    print("Windows Claude cannot follow a WSL symlink; copy the folder there if you want it on Windows.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
