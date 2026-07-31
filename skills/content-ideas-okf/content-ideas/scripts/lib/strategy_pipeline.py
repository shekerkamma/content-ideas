"""Repo-local Stage 0/1 pipeline runner for strategy-mode use cases."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

from .env import content_home
from . import gbrain


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_RUNS_DIR = REPO_ROOT / "runs"


@dataclass
class PipelineContext:
    feed_path: Path
    run_dir: Path
    use_case: dict
    gbrain_used: bool
    recall_note_path: Path | None
    recall_mode: str


def latest_strategy_feed(root=None):
    """Return the latest feed-data.json that contains strategy-mode useCases."""
    research_root = Path(root or content_home()) / "research"
    candidates = []
    if not research_root.exists():
        raise FileNotFoundError(f"research directory not found: {research_root}")
    for child in research_root.iterdir():
        if not child.is_dir():
            continue
        feed_path = child / "feed-data.json"
        if not feed_path.exists():
            continue
        try:
            data = json.loads(feed_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        if data.get("useCases"):
            candidates.append((child.name, feed_path, data))
    if not candidates:
        raise FileNotFoundError(f"no strategy-mode feed-data.json found in {research_root}")
    _, feed_path, data = sorted(candidates, key=lambda item: item[0])[-1]
    return feed_path, data


def format_use_case_list(use_cases):
    lines = ["Use cases:"]
    for idx, item in enumerate(use_cases, start=1):
        confidence = str(item.get("confidence", "")).upper() or "UNKNOWN"
        signals = len(item.get("signals") or [])
        lines.append(f"{idx}. {item.get('title', 'Untitled')} ({confidence}, {signals} signals)")
    return "\n".join(lines)


def select_use_case(use_cases, selector):
    """Select a use case by 1-based index, id, or fuzzy title/vertical match."""
    if not selector:
        raise ValueError("selector is required")
    if selector.isdigit():
        idx = int(selector) - 1
        if idx < 0 or idx >= len(use_cases):
            raise ValueError(f"use case index out of range: {selector}")
        return use_cases[idx]

    lowered = selector.strip().lower()
    for item in use_cases:
        if lowered == str(item.get("id", "")).lower():
            return item

    def _score(item):
        fields = [
            str(item.get("title", "")).lower(),
            str(item.get("verticalName", "")).lower(),
        ]
        best = 0
        for field in fields:
            if lowered == field:
                return 100
            if lowered in field:
                best = max(best, len(lowered))
        return best

    ranked = sorted((( _score(item), item) for item in use_cases), key=lambda pair: pair[0], reverse=True)
    if not ranked or ranked[0][0] <= 0:
        raise ValueError(f"no use case matched selector: {selector}")
    return ranked[0][1]


def slugify(text):
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug or "untitled-use-case"


def _tokenize(text):
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def today_utc():
    return datetime.now(timezone.utc).date().isoformat()


def default_query_for(use_case):
    parts = [
        use_case.get("verticalName") or use_case.get("title") or "",
        "automation",
        "workflow",
    ]
    return " ".join(part for part in parts if part).strip()


def _candidate_recall_notes():
    return list(DEFAULT_RUNS_DIR.glob("*/research-notes/*gbrain*.md"))


def reuse_prior_recall_note(use_case, run_dir):
    """Reuse the best prior repo-local gbrain recall note when live recall stalls."""
    target_tokens = _tokenize(
        " ".join(
            [
                str(use_case.get("title", "")),
                str(use_case.get("verticalName", "")),
            ]
        )
    )
    best = None
    best_score = 0
    for path in _candidate_recall_notes():
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        score = len(target_tokens & _tokenize(text))
        if score > best_score:
            best_score = score
            best = (path, text)
    if not best or best_score < 2:
        return False, None

    src_path, src_text = best
    note_path = run_dir / "research-notes" / "01-gbrain-recall.md"
    lines = src_text.rstrip().splitlines()
    if "source_ref:" in src_text:
        reused = src_text.rstrip() + f"\n\n- Reused prior repo-local GBrain recall artifact: `{src_path}`\n"
    else:
        if lines[:1] == ["---"]:
            try:
                end_idx = lines[1:].index("---") + 1
                lines.insert(end_idx, f"source_ref: {src_path}")
                reused = "\n".join(lines) + "\n\n- Reused prior repo-local GBrain recall artifact.\n"
            except ValueError:
                reused = src_text.rstrip() + f"\n\nSource ref: `{src_path}`\n"
        else:
            reused = src_text.rstrip() + f"\n\nSource ref: `{src_path}`\n"
    note_path.write_text(reused, encoding="utf-8")
    return True, note_path


def create_run_dir(use_case, runs_dir=None, date_str=None):
    base = Path(runs_dir or DEFAULT_RUNS_DIR)
    run_dir = base / f"{date_str or today_utc()}-{slugify(use_case.get('title', 'use-case'))}"
    run_dir.mkdir(parents=True, exist_ok=True)
    (run_dir / "research-notes").mkdir(parents=True, exist_ok=True)
    return run_dir


def build_recall_note(use_case, run_dir, query_text=None, timeout=30):
    """Attempt GBrain recall and write the standard note if available."""
    if not gbrain.gbrain_available():
        reused, note_path = reuse_prior_recall_note(use_case, run_dir)
        return reused, note_path, "repo-reuse" if reused else "unavailable"

    query_text = query_text or default_query_for(use_case)
    title = f"GBrain Recall - {use_case.get('title', 'Use Case')}"
    note_path = run_dir / "research-notes" / "01-gbrain-recall.md"
    try:
        response = gbrain.recall(query_text, mode="query", timeout=timeout)
    except Exception:  # noqa: BLE001
        reused, reused_path = reuse_prior_recall_note(use_case, run_dir)
        return reused, reused_path, "repo-reuse" if reused else "timeout"
    gbrain.write_recall_note(note_path, title=title, query_text=query_text, response_text=response)
    return True, note_path, "live"


def write_research_index(run_dir):
    note_files = sorted(
        path for path in (run_dir / "research-notes").glob("*.md") if path.name != "INDEX.md"
    )
    lines = ["# Research Notes", ""]
    for idx, path in enumerate(note_files, start=1):
        lines.append(f"{idx}. [{path.name}](./{path.name})")
    lines.append("")
    (run_dir / "research-notes" / "INDEX.md").write_text("\n".join(lines), encoding="utf-8")


def render_content_research(use_case, feed_path, gbrain_used, recall_mode):
    lines = [
        f"# Content Research: {use_case.get('title', 'Untitled Use Case')}",
        "",
        "## Selected Use Case",
        f"- Feed source: `{feed_path}`",
        f"- Use case id: `{use_case.get('id', '')}`",
        f"- Vertical: `{use_case.get('verticalName', use_case.get('title', ''))}`",
        f"- Confidence: `{use_case.get('confidence', 'unknown')}`",
        "",
        "## GBrain Recall",
    ]
    if recall_mode == "live":
        lines.append("- Semantic retrieval executed before fresh content-research synthesis.")
    elif recall_mode == "repo-reuse":
        lines.append("- Prior repo-local GBrain recall artifact reused to seed Stage 1 before fresh synthesis.")
    else:
        lines.append("- GBrain recall unavailable in this host context; Stage 1 continued with feed-grounded local context only.")

    lines.extend(
        [
            "",
            "## Feed-Grounded Context",
            "",
            "### Challenge",
            *[f"- {item}" for item in (use_case.get("challenge") or [])],
            "",
            "### Solution",
            *[f"- {item}" for item in (use_case.get("solution") or [])],
            "",
            "### Workflow",
            *[f"{idx}. {item}" for idx, item in enumerate(use_case.get("how") or [], start=1)],
            "",
            "### Source URLs",
            *[f"- {url}" for url in (use_case.get("sourceUrls") or [])],
            "",
            "### Signals",
            *[
                f"- {signal.get('signalType', 'signal')}: {signal.get('postTitle', signal.get('postUrl', ''))}"
                for signal in (use_case.get("signals") or [])
            ],
            "",
            "## Stage 1 Output",
            "- This artifact is the repo-local Stage 1 handoff for downstream strategy work.",
            "- The next stages consume this run folder rather than reconstructing the use case from scratch.",
            "",
        ]
    )
    return "\n".join(lines)


def write_pipeline_status(run_dir, title, gbrain_used, source_count, recall_mode):
    if recall_mode == "live":
        gbrain_detail = "semantic retrieval executed before fresh synthesis"
    elif recall_mode == "repo-reuse":
        gbrain_detail = "prior repo-local GBrain recall artifact reused"
    else:
        gbrain_detail = "not available in this host"
    lines = [
        "# Pipeline Status",
        "",
        f"PIPELINE: {title}",
        "=============================================",
        "",
        f"- {'✓' if gbrain_used else '◻'} GBrain Recall      {gbrain_detail}",
        f"- ✓ Content Research   {source_count} feed-grounded source references compiled into local run artifacts",
        "- ◻ Vertical Score     (pending)",
        "- ◻ Strategy Brief     (pending)",
        "- ◻ PPTX Deck          (pending)",
        "- ◻ Full Strategy      (pending)",
        "- ◻ Deal Prep          (pending)",
        "- ◻ GBrain Write-back  (pending)",
        "",
    ]
    (run_dir / "pipeline-status.md").write_text("\n".join(lines), encoding="utf-8")


def write_run_manifest(run_dir, feed_path, use_case):
    manifest = {
        "feed_path": str(feed_path),
        "use_case_id": use_case.get("id"),
        "title": use_case.get("title"),
        "verticalName": use_case.get("verticalName"),
        "sourceUrls": use_case.get("sourceUrls") or [],
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    (run_dir / "selected-use-case.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")


def run_stage1_pipeline(selector, *, content_root=None, runs_dir=None, query_text=None):
    """Create a repo-local Stage 1 run from the latest strategy-mode feed."""
    feed_path, data = latest_strategy_feed(content_root)
    use_case = select_use_case(data["useCases"], selector)
    run_dir = create_run_dir(use_case, runs_dir=runs_dir)
    gbrain_used, recall_note_path, recall_mode = build_recall_note(use_case, run_dir, query_text=query_text)
    (run_dir / "content-research.md").write_text(
        render_content_research(use_case, feed_path, gbrain_used, recall_mode),
        encoding="utf-8",
    )
    write_pipeline_status(
        run_dir,
        use_case.get("title", "Untitled Use Case"),
        gbrain_used,
        len(use_case.get("sourceUrls") or []),
        recall_mode,
    )
    write_run_manifest(run_dir, feed_path, use_case)
    write_research_index(run_dir)
    return PipelineContext(
        feed_path=feed_path,
        run_dir=run_dir,
        use_case=use_case,
        gbrain_used=gbrain_used,
        recall_note_path=recall_note_path,
        recall_mode=recall_mode,
    )
