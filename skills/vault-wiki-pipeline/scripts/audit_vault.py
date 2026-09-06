#!/usr/bin/env python3
"""Audit and optionally improve an Obsidian vault wiki."""

from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path


EXCLUDE_PARTS = {".git", ".claude", ".obsidian"}
RAW_ARCHIVE_PARTS = {"Clippings"}
TECH_HINTS = {
    "ai", "api", "app", "apps", "azure", "aws", "cli", "cloud", "code", "copilot",
    "desktop", "docker", "framework", "github", "google", "gpt", "hubspot",
    "instagram", "langchain", "langgraph", "linkedin", "mcp", "model", "n8n",
    "openai", "platform", "python", "rag", "salesforce", "sap", "shopify",
    "slack", "studio", "supabase", "telegram", "tiktok", "tool", "vercel",
    "youtube", "zapier",
}
CONCEPT_HINTS = {
    "agent", "agentic", "architecture", "automation", "context", "engineering",
    "enterprise", "governance", "memory", "pattern", "pre-sales", "prompt",
    "protocol", "research", "strategy", "workflow",
}
KNOWN_TECH = {
    "azure ai search", "claude opus", "claude opus 4.7", "clickup", "facebook",
    "gmail", "mcp agent", "meta ads", "microsoft copilot studio",
    "nano banana", "oauth 2.0", "obsidian web clipper", "perplexity", "quickbooks",
    "skool", "windsurf",
}
KNOWN_PEOPLE = {"ben ai", "patrick dang", "chris ashby"}


def is_note(path: Path, include_clippings: bool) -> bool:
    if path.suffix.lower() != ".md":
        return False
    parts = set(path.parts)
    if parts & EXCLUDE_PARTS:
        return False
    if not include_clippings and parts & RAW_ARCHIVE_PARTS:
        return False
    return True


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="utf-8", errors="ignore")


def frontmatter_block(text: str) -> str:
    if not text.startswith("---"):
        return ""
    end = text.find("\n---", 3)
    if end == -1:
        return ""
    return text[3:end]


def aliases_from_frontmatter(text: str) -> set[str]:
    block = frontmatter_block(text)
    if not block:
        return set()
    aliases: set[str] = set()
    lines = block.splitlines()
    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("aliases:"):
            value = stripped.split(":", 1)[1].strip()
            if value.startswith("[") and value.endswith("]"):
                for item in value.strip("[]").split(","):
                    clean = item.strip().strip("'\"")
                    if clean:
                        aliases.add(clean)
            elif value:
                aliases.add(value.strip("'\""))
            else:
                j = i + 1
                while j < len(lines) and lines[j].startswith((" ", "-")):
                    clean = lines[j].strip().lstrip("-").strip().strip("'\"")
                    if clean:
                        aliases.add(clean)
                    j += 1
    return aliases


def wikilinks(text: str) -> list[str]:
    found = []
    for match in re.finditer(r"\[\[([^\]|#]+)(?:[\|#][^\]]*)?\]\]", text):
        target = match.group(1).strip()
        if target:
            found.append(target)
    return found


def kebab(name: str) -> str:
    out = re.sub(r"[^A-Za-z0-9]+", "-", name).strip("-").lower()
    return out or "untitled"


def classify_target(target: str) -> tuple[str, str]:
    lower = target.lower()
    words = set(re.findall(r"[a-z0-9]+", lower))
    if lower in KNOWN_PEOPLE:
        return "People", "person"
    if lower in KNOWN_TECH:
        return "technologies", "technology"
    if "/" in target:
        return "Knowledge", "knowledge"
    if any(hint in words or hint in lower for hint in TECH_HINTS):
        return "technologies", "technology"
    if any(hint in words or hint in lower for hint in CONCEPT_HINTS):
        return "Knowledge", "knowledge"
    if re.match(r"^[A-Z][A-Za-z.\-]+(?:\s+[A-Z][A-Za-z.\-]+){1,3}$", target):
        return "People", "person"
    return "Knowledge", "knowledge"


def build_stub(title: str, tag: str) -> str:
    return (
        "---\n"
        f"title: {title}\n"
        f"tags: [{tag}, stub]\n"
        "---\n\n"
        f"# {title}\n\n"
        f"{title} is a recurring wiki target in this vault.\n\n"
        "## Relevance\n"
        "- Captured as a high-frequency unresolved link.\n"
        "- Expand when reviewing related source notes.\n\n"
        "## Related\n"
        "- [[Content Research MOC]]\n"
    )


def audit(vault: Path, include_clippings: bool = False) -> dict:
    files = [p for p in vault.rglob("*.md") if is_note(p.relative_to(vault), include_clippings)]
    resolvable: set[str] = set()
    missing_frontmatter = []
    folder_counts = Counter()
    all_links = Counter()

    for path in files:
        rel = path.relative_to(vault)
        text = read_text(path)
        stem = path.stem
        resolvable.add(stem.lower())
        resolvable.add(str(rel.with_suffix("")).replace("\\", "/").lower())
        for alias in aliases_from_frontmatter(text):
            resolvable.add(alias.lower())
        if not text.startswith("---"):
            missing_frontmatter.append(str(rel).replace("\\", "/"))
        folder_counts[rel.parts[0] if len(rel.parts) > 1 else "_root"] += 1
        all_links.update(wikilinks(text))

    unresolved = Counter()
    for target, count in all_links.items():
        if target.lower() not in resolvable:
            unresolved[target] = count

    boards = {}
    for board in ("Boards/Work.md", "Boards/Personal.md"):
        path = vault / board
        if path.exists():
            text = read_text(path)
            boards[board] = {
                "open_tasks": len(re.findall(r"^- \[ \]", text, flags=re.MULTILINE)),
                "done_tasks": len(re.findall(r"^- \[x\]", text, flags=re.MULTILINE)),
            }

    return {
        "date": date.today().isoformat(),
        "markdown_notes": len(files),
        "with_frontmatter": len(files) - len(missing_frontmatter),
        "missing_frontmatter": missing_frontmatter,
        "folder_counts": dict(sorted(folder_counts.items())),
        "unique_wiki_targets": len(all_links),
        "resolvable_targets": len(all_links) - len(unresolved),
        "unresolved_targets": len(unresolved),
        "top_unresolved": unresolved.most_common(50),
        "boards": boards,
    }


def write_review(vault: Path, data: dict) -> Path:
    reviews = vault / "Reviews"
    reviews.mkdir(exist_ok=True)
    path = reviews / f"{data['date']} - Vault Wiki Audit.md"
    lines = [
        "---",
        f"title: {data['date']} - Vault Wiki Audit",
        "tags: [review, vault, wiki-audit]",
        "---",
        "",
        f"# {data['date']} - Vault Wiki Audit",
        "",
        "## Summary",
        f"- Markdown notes: {data['markdown_notes']}",
        f"- With frontmatter: {data['with_frontmatter']}",
        f"- Missing frontmatter: {len(data['missing_frontmatter'])}",
        f"- Unique wiki targets: {data['unique_wiki_targets']}",
        f"- Resolvable targets: {data['resolvable_targets']}",
        f"- Unresolved targets: {data['unresolved_targets']}",
        "",
        "## Top Unresolved",
        "| Target | Count |",
        "|---|---:|",
    ]
    for target, count in data["top_unresolved"][:25]:
        lines.append(f"| [[{target}]] | {count} |")
    lines += ["", "## Missing Frontmatter"]
    if data["missing_frontmatter"]:
        lines.extend(f"- {item}" for item in data["missing_frontmatter"][:50])
    else:
        lines.append("- None")
    lines += ["", "## Related", "- [[AI Agent Systems MOC]]", "- [[Claude Code Skills MOC]]"]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def create_stubs(vault: Path, data: dict, limit: int, min_count: int) -> list[str]:
    created = []
    for target, count in data["top_unresolved"]:
        if len(created) >= limit or count < min_count:
            continue
        folder, tag = classify_target(target)
        directory = vault / folder
        directory.mkdir(exist_ok=True)
        path = directory / f"{target}.md"
        if path.exists():
            continue
        path.write_text(build_stub(target, tag), encoding="utf-8")
        created.append(str(path.relative_to(vault)).replace("\\", "/"))
    return created


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vault", default=".")
    parser.add_argument("--include-clippings", action="store_true")
    parser.add_argument("--write-review", action="store_true")
    parser.add_argument("--create-stubs", action="store_true")
    parser.add_argument("--limit", type=int, default=20)
    parser.add_argument("--min-count", type=int, default=5)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    vault = Path(args.vault).resolve()
    data = audit(vault, include_clippings=args.include_clippings)

    if args.create_stubs:
        data["created_stubs"] = create_stubs(vault, data, args.limit, args.min_count)
        data = audit(vault, include_clippings=args.include_clippings) | {"created_stubs": data["created_stubs"]}

    if args.write_review:
        data["review_path"] = str(write_review(vault, data).relative_to(vault)).replace("\\", "/")

    if args.json:
        print(json.dumps(data, indent=2))
    else:
        print(f"Markdown notes: {data['markdown_notes']}")
        print(f"With frontmatter: {data['with_frontmatter']}")
        print(f"Resolvable targets: {data['resolvable_targets']}")
        print(f"Unresolved targets: {data['unresolved_targets']}")
        for target, count in data["top_unresolved"][:15]:
            print(f"{count:>4}  {target}")
        if "created_stubs" in data:
            print("Created stubs:")
            for item in data["created_stubs"]:
                print(f"- {item}")
        if "review_path" in data:
            print(f"Review: {data['review_path']}")


if __name__ == "__main__":
    main()
