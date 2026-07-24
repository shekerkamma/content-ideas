#!/usr/bin/env python3
"""Build a staged OKF bundle from the Hyundai Obsidian vault.

The source vault is read-only. Generated files are written under this run
folder so the bundle can be validated before anything is synced back.
"""
from __future__ import annotations

import re
import shutil
from urllib.parse import quote
from pathlib import Path

VAULT = Path("/mnt/c/Users/sheke/Documents/hyundai-ai-vault")
RUN = Path(__file__).resolve().parent
BUNDLE = RUN / "bundle"
TODAY = "2026-07-04"

USE_CASES = [
    "UC-01 Visual Inspection.md",
    "UC-02 Variant Confirmation.md",
    "UC-03 Component Validation.md",
    "UC-04 SOP Compliance.md",
    "UC-05 Predictive Quality.md",
    "UC-06 Predictive Maintenance.md",
    "UC-07 Safety Monitoring.md",
    "UC-08 Digital Traceability.md",
]
ARCHITECTURE = [
    "architecture/Edge Deployment.md",
    "architecture/OPC-UA Integration.md",
    "architecture/MES Integration.md",
    "architecture/MLOps Pipeline.md",
    "architecture/Claude-Supply-Chain-Agent-SAP-Integration.md",
]
TECHNOLOGIES = [
    "repos/anomalib.md",
    "repos/ultralytics.md",
    "repos/PaddleOCR.md",
    "repos/mmpose.md",
    "repos/SlowFast.md",
    "repos/XGBoost.md",
    "repos/lifelines.md",
    "repos/Neo4j.md",
    "repos/ByteTrack.md",
    "repos/supervision.md",
    "repos/MediaPipe.md",
    "repos/librosa.md",
    "repos/jetson-inference.md",
    "repos/pypylon.md",
    "repos/mmdetection.md",
    "repos/mmpretrain.md",
]


def slugify(value: str) -> str:
    value = value.lower().replace("&", " and ")
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def split_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    lines = text.splitlines()
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter: dict[str, str] = {}
            for raw in lines[1:i]:
                match = re.match(r"^([A-Za-z_][A-Za-z0-9_-]*):\s*(.*)$", raw)
                if match:
                    frontmatter[match.group(1)] = match.group(2).strip()
            return frontmatter, "\n".join(lines[i + 1 :]).lstrip("\n")
    return {}, text


def title_from(path: Path, frontmatter: dict[str, str], body: str) -> str:
    if frontmatter.get("title"):
        return frontmatter["title"].strip("'\"")
    match = re.search(r"^#\s+(.+)$", body, re.M)
    return match.group(1).strip() if match else path.stem


def description_from(body: str) -> str:
    for para in re.split(r"\n\s*\n", body):
        stripped = para.strip()
        if not stripped or stripped.startswith("#") or stripped.startswith("```"):
            continue
        stripped = re.sub(r"\s+", " ", stripped)
        return stripped[:220]
    return ""


def extract_tags(raw: str) -> list[str]:
    raw = raw.strip()
    if raw.startswith("[") and raw.endswith("]"):
        return [v.strip().strip("'\"") for v in raw[1:-1].split(",") if v.strip()]
    return [v.strip().strip("'\"") for v in raw.split() if v.strip()]


def yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    return "\n" + "\n".join(f"- {item}" for item in items)


def markdown_path(path: Path) -> str:
    return quote(path.as_posix(), safe="/:")


def windows_path(path: Path) -> str:
    rel = path.relative_to(VAULT).as_posix()
    return "C:\\Users\\sheke\\Documents\\hyundai-ai-vault\\" + rel.replace("/", "\\")


def windows_file_uri(path: Path) -> str:
    rel = path.relative_to(VAULT).as_posix()
    return "file:///C:/Users/sheke/Documents/hyundai-ai-vault/" + quote(rel, safe="/:")


def relpath(from_file: Path, to_file: Path) -> str:
    return Path("../" * (len(from_file.parent.relative_to(BUNDLE).parts))).joinpath(
        to_file.relative_to(BUNDLE)
    ).as_posix()


def source_copy_path(src: Path) -> Path:
    return BUNDLE / "source-vault" / src.relative_to(VAULT)


def main() -> int:
    BUNDLE.mkdir(parents=True, exist_ok=True)
    for generated in ["use-cases", "architecture", "technologies", "source-vault"]:
        if (BUNDLE / generated).exists():
            shutil.rmtree(BUNDLE / generated)
    for generated in ["index.md", "log.md", "okf-cli.py"]:
        if (BUNDLE / generated).exists():
            (BUNDLE / generated).unlink()
    for folder in ["use-cases", "architecture", "technologies", "source-vault"]:
        (BUNDLE / folder).mkdir(parents=True, exist_ok=True)

    pages: list[dict[str, object]] = []
    selected = (
        [(Path(p), "use_case", "use-cases") for p in USE_CASES]
        + [(Path(p), "architecture", "architecture") for p in ARCHITECTURE]
        + [(Path(p), "technology", "technologies") for p in TECHNOLOGIES]
    )

    link_map: dict[str, Path] = {}
    parsed: list[dict[str, object]] = []
    for rel, page_type, out_dir in selected:
        src = VAULT / rel
        text = src.read_text(encoding="utf-8", errors="replace")
        fm, body = split_frontmatter(text)
        title = title_from(src, fm, body)
        out = BUNDLE / out_dir / f"{slugify(title)}.md"
        source_copy = source_copy_path(src)
        item = {
            "src_rel": rel.as_posix(),
            "src": src,
            "source_copy": source_copy,
            "out": out,
            "type": page_type,
            "title": title,
            "tags": extract_tags(fm.get("tags", "")),
            "body": body,
            "description": description_from(body),
        }
        parsed.append(item)
        for key in {src.stem, title, slugify(title)}:
            link_map[key.lower()] = out

    def convert_links(body: str, current: Path) -> str:
        def repl(match: re.Match[str]) -> str:
            raw = match.group(1)
            target, _, label = raw.partition("|")
            label = label or target
            clean_target = target.split("#", 1)[0].strip().lower()
            dest = link_map.get(clean_target) or link_map.get(slugify(clean_target))
            if not dest:
                return label
            return f"[{label}]({relpath(current, dest)})"

        parts = body.split("```")
        for i in range(0, len(parts), 2):
            parts[i] = re.sub(r"\[\[([^\]]+)\]\]", repl, parts[i])
        for i in range(1, len(parts), 2):
            parts[i] = re.sub(r"\[\[([^|\]#]+)(?:#[^|\]]+)?(?:\|([^\]]+))?\]\]", lambda m: m.group(2) or m.group(1), parts[i])
        return "```".join(parts)

    for item in parsed:
        out = item["out"]
        assert isinstance(out, Path)
        tags = item["tags"]
        assert isinstance(tags, list)
        body = item["body"]
        assert isinstance(body, str)
        title = str(item["title"])
        page_type = str(item["type"])
        src_rel = str(item["src_rel"])
        src = Path(str(item["src"]))
        source_copy = Path(str(item["source_copy"]))
        source_copy.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, source_copy)
        description = str(item["description"])
        frontmatter = [
            "---",
            f"type: {page_type}",
            f"title: {title!r}",
            f"description: {description!r}",
            f"source_path: {src_rel!r}",
            f"tags:{yaml_list(tags)}",
            f"timestamp: '{TODAY}'",
            "---",
            "",
            f"> Original source (local copy): [{src_rel}]({relpath(out, source_copy)})",
            f"> Original source (WSL): [{src_rel}]({markdown_path(src)})",
            f"> Original source (Windows): [open in editor]({windows_file_uri(src)})",
            f"> Windows path: `{windows_path(src)}`",
            "",
        ]
        out.write_text("\n".join(frontmatter) + convert_links(body, out) + "\n", encoding="utf-8")
        pages.append(item)

    def section_index(folder: str, title: str, intro: str) -> None:
        rows = [f"# {title}", "", intro, ""]
        for item in sorted([p for p in pages if Path(str(p["out"])).parent.name == folder], key=lambda p: str(p["title"])):
            out = Path(str(item["out"]))
            rows.append(f"* [{item['title']}]({out.name}) - {item['description']}")
        (BUNDLE / folder / "index.md").write_text("\n".join(rows) + "\n", encoding="utf-8")

    section_index("use-cases", "Use Cases", "Hyundai plant-operations use cases staged from the Obsidian vault.")
    section_index("architecture", "Architecture", "Architecture notes that support the Hyundai AI plant-operations use cases.")
    section_index("technologies", "Technologies", "Technology and repository notes linked from the Hyundai use cases.")

    root = [
        "---",
        'okf_version: "0.1"',
        "---",
        "",
        "# Hyundai AI Plant Operations OKF Bundle",
        "",
        "A staged Open Knowledge Format bundle generated from Sheker's Obsidian vault.",
        "The source vault was not modified.",
        "",
        "## Sections",
        "",
        "* [use-cases/](use-cases/index.md) - 8 Hyundai plant-operations AI use cases",
        "* [architecture/](architecture/index.md) - edge, MES, OPC-UA, MLOps, and supply-chain architecture notes",
        "* [technologies/](technologies/index.md) - repositories and technology references used by the use cases",
        "* [source-vault/](source-vault/) - local copies of source notes for editor-friendly links",
        "",
        "## Answering Flow",
        "",
        "1. Start with this index.",
        "2. Use `python3 okf-cli.py find \"<topic>\"`.",
        "3. Read only the relevant pages with `python3 okf-cli.py read <path>`.",
        "4. Cite `source_path` when answering from this derived bundle.",
        "",
    ]
    (BUNDLE / "index.md").write_text("\n".join(root), encoding="utf-8")

    (BUNDLE / "log.md").write_text(
        "# Update Log\n\n"
        f"## {TODAY}\n"
        "* **Creation**: Generated staged OKF bundle from Hyundai Obsidian vault.\n"
        f"* **Scope**: {len(USE_CASES)} use cases, {len(ARCHITECTURE)} architecture notes, {len(TECHNOLOGIES)} technology notes.\n"
        "* **Safety**: Source vault was read only; generated files live under the repo run folder.\n",
        encoding="utf-8",
    )

    shutil.copyfile(
        Path("/home/shekerk/content-ideas/runs/2026-07-04-cole-okf-cross-host/bundle/okf-cli.py"),
        BUNDLE / "okf-cli.py",
    )
    cli = BUNDLE / "okf-cli.py"
    cli_text = cli.read_text(encoding="utf-8")
    cli_text = cli_text.replace(
        'RESERVED = {"index.md", "log.md", "README.md", "AGENTS.md", "CLAUDE.md"}',
        'RESERVED = {"index.md", "log.md", "README.md", "AGENTS.md", "CLAUDE.md"}\nEXCLUDED_DIRS = {"source-vault"}',
    )
    cli_text = cli_text.replace(
        '    for md in sorted(ROOT.rglob("*.md")):\n        if md.name in RESERVED:',
        '    for md in sorted(ROOT.rglob("*.md")):\n        if any(part in EXCLUDED_DIRS for part in md.relative_to(ROOT).parts):\n            continue\n        if md.name in RESERVED:',
    )
    cli.write_text(cli_text, encoding="utf-8")
    print(f"Generated {len(pages)} OKF pages in {BUNDLE}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
