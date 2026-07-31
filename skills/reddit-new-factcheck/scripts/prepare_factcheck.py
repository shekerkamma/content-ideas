#!/usr/bin/env python3
"""Prepare a Reddit-backed fact-check run from a document.

This script is dependency-free. It normalizes text from common document formats,
extracts claim candidates, and optionally scores existing Reddit thread JSON
against those claims. It does not perform Reddit discovery or final judgment.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable
from xml.etree import ElementTree as ET
from zipfile import ZipFile


STOPWORDS = {
    "about",
    "after",
    "again",
    "against",
    "already",
    "also",
    "and",
    "any",
    "are",
    "because",
    "been",
    "before",
    "being",
    "between",
    "but",
    "can",
    "cannot",
    "could",
    "does",
    "from",
    "have",
    "into",
    "its",
    "more",
    "must",
    "not",
    "our",
    "should",
    "that",
    "the",
    "their",
    "them",
    "then",
    "there",
    "these",
    "this",
    "those",
    "through",
    "with",
    "without",
    "will",
    "would",
}

DOMAIN_GENERIC = {
    "agent",
    "agents",
    "agentic",
    "ai",
    "artificial",
    "intelligence",
    "validation",
    "validate",
    "validated",
    "authority",
}

NOISE_SUBREDDITS = {
    "aitah",
    "askreddit",
    "entertainment",
    "gaming",
    "movies",
    "music",
    "news",
    "politics",
    "television",
    "todayilearned",
    "wallstreetbets",
    "worldnews",
}

WORKFLOW_PROFILES = [
    {
        "name": "property_management",
        "claim_terms": {
            "appfolio",
            "buildium",
            "landlord",
            "maintenance",
            "property",
            "rent",
            "tenant",
            "vendor",
            "yardi",
        },
        "subreddits": {"landlord", "propertymanagement", "realestateinvesting", "realestate"},
        "persona_terms": {"landlord", "manager", "owner", "property", "tenant"},
        "workflow_terms": {
            "appfolio",
            "buildium",
            "door",
            "doors",
            "expense",
            "maintenance",
            "manager",
            "property",
            "rent",
            "rental",
            "tenant",
            "vendor",
            "yardi",
        },
    },
    {
        "name": "hotel_operations",
        "claim_terms": {"booking", "bookings", "guest", "hotel", "hotels", "reservations"},
        "subreddits": {"askhotels", "hotel", "hotels", "talesfromthefrontdesk"},
        "persona_terms": {"clerk", "desk", "front", "guest", "hotel", "manager", "staff"},
        "workflow_terms": {"booking", "bookings", "calls", "desk", "front", "guest", "reservation", "rooms"},
    },
    {
        "name": "therapy_clinic_operations",
        "claim_terms": {
            "clinic",
            "clinics",
            "clinical",
            "front-office",
            "patient",
            "patients",
            "refills",
            "scheduling",
            "therapist",
            "therapists",
            "therapy",
        },
        "subreddits": {
            "allaboutpt",
            "askdocs",
            "medicine",
            "nursing",
            "physicaltherapy",
            "psychotherapy",
            "therapists",
        },
        "persona_terms": {"clinician", "clinic", "desk", "doctor", "patient", "therapist", "therapy"},
        "workflow_terms": {
            "appointment",
            "billing",
            "calls",
            "charting",
            "client",
            "clinic",
            "follow-up",
            "front",
            "intake",
            "notes",
            "patient",
            "refill",
            "scheduling",
            "texts",
        },
    },
    {
        "name": "finance_operations",
        "claim_terms": {
            "accounting",
            "accounts",
            "ap",
            "ar",
            "cash",
            "close",
            "finance",
            "invoice",
            "payable",
            "receivable",
        },
        "subreddits": {"accounting", "bookkeeping", "cfo", "consulting", "smallbusiness"},
        "persona_terms": {"accountant", "bookkeeper", "controller", "finance"},
        "workflow_terms": {
            "accounting",
            "ap",
            "ar",
            "billing",
            "cash",
            "close",
            "invoice",
            "month-end",
            "payable",
            "receivable",
        },
    },
    {
        "name": "insurance_claims",
        "claim_terms": {"adjuster", "claims", "insurance", "insurers", "mga", "tpa"},
        "subreddits": {"adjusters", "insurance", "insurancepros"},
        "persona_terms": {"adjuster", "claim", "claims", "insurer", "tpa"},
        "workflow_terms": {"adjuster", "claim", "claims", "coverage", "estimate", "fnol", "loss", "policy"},
    },
    {
        "name": "mortgage_servicing",
        "claim_terms": {"borrower", "borrowers", "loan", "mortgage", "servicing"},
        "subreddits": {"loanoriginators", "mortgage", "realestate", "realestateinvesting"},
        "persona_terms": {"borrower", "lender", "loan", "mortgage", "servicer"},
        "workflow_terms": {"borrower", "escrow", "loan", "mortgage", "payment", "servicing", "underwriting"},
    },
    {
        "name": "construction_review",
        "claim_terms": {
            "builder",
            "construction",
            "contractor",
            "drawings",
            "homebuilding",
            "project",
            "rework",
        },
        "subreddits": {"architecture", "construction", "contractor", "homebuilding"},
        "persona_terms": {"architect", "builder", "contractor", "owner", "pm", "subcontractor"},
        "workflow_terms": {
            "architectural",
            "build",
            "builder",
            "construction",
            "contract",
            "draw",
            "drawings",
            "framing",
            "permit",
            "punch",
            "rework",
            "schedule",
        },
    },
    {
        "name": "consumer_lending",
        "claim_terms": {"borrower", "collections", "consumer", "lending", "loan", "repayment"},
        "subreddits": {"banking", "credit", "loans", "personalfinance"},
        "persona_terms": {"borrower", "collector", "lender", "loan"},
        "workflow_terms": {"borrower", "collection", "collections", "credit", "lending", "loan", "payment", "repayment"},
    },
]

PAIN_TERMS = {
    "awkward",
    "backlog",
    "busy",
    "chaotic",
    "complaint",
    "confusing",
    "constant",
    "delay",
    "delays",
    "difficult",
    "drowning",
    "fail",
    "fails",
    "fragmented",
    "friction",
    "hard",
    "inconsistent",
    "manual",
    "missing",
    "overloaded",
    "pain",
    "problem",
    "problems",
    "rework",
    "rushed",
    "spreadsheet",
    "spreadsheets",
    "stuck",
    "too many",
    "workaround",
}

GENERIC_REDDIT_SIGNAL_TERMS = {
    "adoption",
    "agent",
    "agents",
    "audit",
    "blocker",
    "blockers",
    "deployment",
    "governance",
    "logs",
    "production",
    "risk",
    "switch",
    "switches",
}

PRIMARY_RE = re.compile(
    r"(\b\d+(?:\.\d+)?\s*(?:%|percent|billion|million|k|m|b)\b|\$[\d,.]+|"
    r"\b(?:19|20)\d{2}\b|\bQ[1-4]\s+(?:19|20)\d{2}\b|"
    r"\b(?:SR|OCC|FDIC|Fed|Federal Reserve|Gartner|Forrester|IDC|NIST|ISO)\b)",
    re.I,
)
REDDIT_RE = re.compile(
    r"\b(pain|complain|complaint|sentiment|users|operators|practitioners|"
    r"trust|risk|quality|support|governance|blocker|objection|demand|"
    r"language|community|reddit|buyer|adoption)\b",
    re.I,
)


@dataclass
class Segment:
    locator: str
    text: str
    source: str


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.lower()).strip("-")
    return slug[:80] or "document"


def strip_yaml_frontmatter(text: str) -> str:
    if not text.startswith("---"):
        return text
    match = re.search(r"\n---\s*\n", text[3:])
    if not match:
        return text
    return text[match.end() + 3 :]


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def read_text_segments(path: Path) -> list[Segment]:
    text = path.read_text(encoding="utf-8", errors="replace")
    text = strip_yaml_frontmatter(text)
    slide_parts = re.split(r"(?m)^---\s*$", text)
    if len(slide_parts) > 1:
        return [
            Segment(locator=f"Section {i}", text=part.strip(), source=str(path))
            for i, part in enumerate(slide_parts, 1)
            if part.strip()
        ]
    headings = re.split(r"(?m)^(?=#{1,3}\s+)", text)
    return [
        Segment(locator=f"Section {i}", text=part.strip(), source=str(path))
        for i, part in enumerate(headings, 1)
        if part.strip()
    ] or [Segment(locator="Document", text=text.strip(), source=str(path))]


def pptx_slide_number(name: str) -> int:
    match = re.search(r"slide(\d+)\.xml$", name)
    return int(match.group(1)) if match else 0


def extract_xml_text(xml_bytes: bytes) -> str:
    ns = {"a": "http://schemas.openxmlformats.org/drawingml/2006/main"}
    root = ET.fromstring(xml_bytes)
    texts: list[str] = []
    for node in root.findall(".//a:t", ns):
        if node.text and node.text.strip():
            texts.append(node.text.strip())
    for node in root.findall(".//*[@descr]"):
        descr = node.attrib.get("descr", "").strip()
        if descr:
            texts.append(descr)
    return compact(" ".join(texts))


def sidecar_markdown(path: Path) -> Path | None:
    candidates = [
        path.with_suffix(".md"),
        path.parent / "deck.md",
        path.parent / f"{path.stem}.md",
    ]
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return candidate
    return None


def read_pptx_segments(path: Path) -> tuple[list[Segment], str]:
    segments: list[Segment] = []
    with ZipFile(path) as zf:
        slide_names = sorted(
            [name for name in zf.namelist() if re.match(r"ppt/slides/slide\d+\.xml$", name)],
            key=pptx_slide_number,
        )
        for name in slide_names:
            text = extract_xml_text(zf.read(name))
            if text:
                segments.append(
                    Segment(
                        locator=f"Slide {pptx_slide_number(name)}",
                        text=text,
                        source=str(path),
                    )
                )
    if segments:
        return segments, "pptx-text"
    sidecar = sidecar_markdown(path)
    if sidecar:
        return read_text_segments(sidecar), f"sidecar:{sidecar.name}"
    return [], "pptx-image-only"


def read_pdf_segments(path: Path) -> tuple[list[Segment], str]:
    pdftotext = shutil.which("pdftotext")
    if not pdftotext:
        return [], "pdf-text-unavailable"
    try:
        result = subprocess.run(
            [pdftotext, "-layout", str(path), "-"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (subprocess.CalledProcessError, OSError) as exc:
        return [Segment(locator="PDF extraction error", text=str(exc), source=str(path))], "pdf-error"
    pages = result.stdout.split("\f")
    return [
        Segment(locator=f"Page {i}", text=page.strip(), source=str(path))
        for i, page in enumerate(pages, 1)
        if page.strip()
    ], "pdftotext"


def read_document(path: Path) -> tuple[list[Segment], str]:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt"}:
        return read_text_segments(path), "plain-text"
    if suffix == ".pptx":
        return read_pptx_segments(path)
    if suffix == ".pdf":
        return read_pdf_segments(path)
    raise ValueError(f"Unsupported input type: {suffix}")


def split_claim_lines(text: str) -> Iterable[str]:
    lines: list[str] = []
    for raw_line in text.splitlines():
        line = re.sub(r"^\s*[-*#>\d.)]+\s*", "", raw_line).strip()
        if line:
            lines.append(line)
    joined = " ".join(lines)
    for sentence in re.split(r"(?<=[.!?])\s+", joined):
        candidate = sentence.strip(" -")
        if 30 <= len(candidate) <= 260:
            yield candidate


def looks_like_claim(text: str) -> bool:
    if PRIMARY_RE.search(text) or REDDIT_RE.search(text):
        return True
    if re.search(r"\b(is|are|was|were|has|have|will|must|should|cannot|can't)\b", text, re.I):
        return bool(re.search(r"\b[A-Z][a-zA-Z0-9&.-]{2,}\b", text))
    return False


def token_list(text: str) -> list[str]:
    tokens = [t.lower() for t in re.findall(r"[a-zA-Z][a-zA-Z0-9-]{2,}", text)]
    return [t for t in tokens if t not in STOPWORDS and t not in DOMAIN_GENERIC]


def named_tokens(text: str) -> set[str]:
    terms = set()
    tokens = re.findall(r"\b[A-Z][A-Za-z0-9&.-]{3,}\b", text)
    for index, token in enumerate(tokens):
        lowered = token.lower().strip(".")
        if index == 0 and token[:1].isupper() and not token.isupper():
            continue
        if lowered not in STOPWORDS and lowered not in DOMAIN_GENERIC:
            terms.add(lowered)
    for token in re.findall(r"\b[A-Z]{2,}\b", text):
        lowered = token.lower()
        if lowered not in DOMAIN_GENERIC:
            terms.add(lowered)
    return terms


def claim_kind(text: str) -> str:
    primary = bool(PRIMARY_RE.search(text))
    reddit = bool(REDDIT_RE.search(text))
    if primary and reddit:
        return "mixed"
    if primary:
        return "primary_required"
    return "reddit_evidence"


def make_query(claim: str, topic: str) -> str:
    tokens = token_list(f"{topic} {claim}")
    seen: set[str] = set()
    ordered = []
    for token in tokens:
        if token not in seen:
            ordered.append(token)
            seen.add(token)
    return " ".join(ordered[:14])


def extract_claims(segments: list[Segment], topic: str, max_claims: int) -> list[dict]:
    claims: list[dict] = []
    seen: set[str] = set()
    for segment in segments:
        for line in split_claim_lines(segment.text):
            normalized = compact(line.lower())
            if normalized in seen or not looks_like_claim(line):
                continue
            seen.add(normalized)
            kind = claim_kind(line)
            claims.append(
                {
                    "id": f"claim-{len(claims) + 1:03d}",
                    "claim": line,
                    "locator": segment.locator,
                    "source": segment.source,
                    "evidence_need": kind,
                    "reddit_query": make_query(line, topic),
                    "primary_source_required": kind in {"primary_required", "mixed"},
                }
            )
            if len(claims) >= max_claims:
                return claims
    return claims


def excerpt(text: str, limit: int = 320) -> str:
    text = compact(text)
    return text if len(text) <= limit else text[: limit - 3].rstrip() + "..."


def iter_reddit_items(path: Path) -> Iterable[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    post = data.get("post") or {}
    if post:
        yield {
            "kind": "post",
            "id": post.get("id") or "post",
            "author": post.get("author", ""),
            "score": post.get("score", 0) or 0,
            "depth": 0,
            "text": compact(f"{post.get('title', '')} {post.get('content', '')}"),
            "source_json": str(path),
            "source_url": post.get("url") or post.get("permalink") or "",
            "permalink": post.get("permalink") or post.get("url") or "",
            "subreddit": post.get("subreddit", ""),
        }
    for comment in data.get("comments") or []:
        yield {
            "kind": "comment",
            "id": comment.get("id", ""),
            "author": comment.get("author", ""),
            "score": comment.get("score", 0) or 0,
            "depth": comment.get("depth", 0) or 0,
            "text": comment.get("text", "") or "",
            "source_json": str(path),
            "source_url": comment.get("source_url") or comment.get("url") or "",
            "permalink": comment.get("permalink") or comment.get("source_url") or comment.get("url") or "",
            "subreddit": comment.get("subreddit", ""),
        }


def norm_subreddit(value: str) -> str:
    return value.lower().removeprefix("r/").strip()


def infer_workflow_profiles(claim: dict) -> list[dict]:
    haystack = set(token_list(f"{claim.get('claim', '')} {claim.get('reddit_query', '')}"))
    profiles = []
    for profile in WORKFLOW_PROFILES:
        if haystack & profile["claim_terms"]:
            profiles.append(profile)
    return profiles


def has_phrase_or_token(text: str, terms: set[str]) -> bool:
    lowered = text.lower()
    tokens = set(token_list(text))
    return bool(tokens & {term for term in terms if " " not in term}) or any(
        term in lowered for term in terms if " " in term
    )


def qualification_for(claim: dict, item: dict) -> dict:
    """Return fail-closed Reddit evidence qualification metadata.

    Raw Reddit is only evidence when it matches the claim's workflow context,
    practitioner/persona surface, and an operational pain or workaround.
    """
    text = item.get("text", "")
    item_tokens = set(token_list(text))
    subreddit = norm_subreddit(item.get("subreddit", ""))
    profiles = infer_workflow_profiles(claim)

    if subreddit in NOISE_SUBREDDITS:
        return {"qualified": False, "reason": f"rejected_noise_subreddit:{subreddit}"}

    if profiles:
        for profile in profiles:
            subreddit_ok = not subreddit or subreddit in profile["subreddits"]
            workflow_ok = bool(item_tokens & profile["workflow_terms"])
            persona_ok = bool(item_tokens & profile["persona_terms"]) or subreddit_ok
            pain_ok = has_phrase_or_token(text, PAIN_TERMS)
            if subreddit_ok and workflow_ok and persona_ok and pain_ok:
                return {
                    "qualified": True,
                    "reason": f"qualified:{profile['name']}",
                    "profile": profile["name"],
                    "signals": {
                        "subreddit": subreddit_ok,
                        "workflow": workflow_ok,
                        "persona": persona_ok,
                        "pain": pain_ok,
                    },
                }
        return {
            "qualified": False,
            "reason": "rejected_missing_workflow_persona_or_pain",
            "profiles_checked": [profile["name"] for profile in profiles],
        }

    claim_tokens = set(token_list(f"{claim.get('claim', '')} {claim.get('reddit_query', '')}"))
    shared = claim_tokens & item_tokens
    pain_ok = has_phrase_or_token(text, PAIN_TERMS | GENERIC_REDDIT_SIGNAL_TERMS)
    if len(shared) >= 3 and pain_ok:
        return {
            "qualified": True,
            "reason": "qualified:generic_claim_overlap_with_pain",
            "profile": "generic",
            "signals": {"shared_terms": sorted(shared)[:8], "pain": pain_ok},
        }
    return {"qualified": False, "reason": "rejected_generic_overlap_without_pain"}


def evidence_score(claim: dict, item: dict) -> float:
    qualification = qualification_for(claim, item)
    if not qualification["qualified"]:
        return 0.0
    claim_tokens = set(token_list(claim["claim"]))
    if len(claim_tokens) < 4:
        claim_tokens = set(token_list(f"{claim['claim']} {claim['reddit_query']}"))
    item_tokens = set(token_list(item.get("text", "")))
    if not claim_tokens or not item_tokens:
        return 0.0
    shared = claim_tokens & item_tokens
    required_names = named_tokens(claim["claim"])
    if required_names and not (required_names & item_tokens):
        return 0.0
    if len(shared) < 2 and len(claim_tokens) > 3:
        return 0.0
    overlap = len(shared) / max(6, len(claim_tokens))
    score_bonus = min(max(float(item.get("score") or 0), 0.0), 500.0) / 5000.0
    return overlap + score_bonus


def reddit_verdict(claim: dict, top: list[dict]) -> str:
    if claim.get("primary_source_required") and claim.get("evidence_need") == "primary_required":
        return "requires_primary_source_corroboration"
    if not top:
        return "no_qualified_reddit_evidence"
    best = top[0]["score"]
    if claim.get("evidence_need") == "mixed":
        return "qualified_reddit_signal_primary_source_required" if best >= 0.22 else "weak_qualified_reddit_support_primary_source_required"
    if best >= 0.28 and len(top) >= 2:
        return "qualified_reddit_support"
    if best >= 0.18:
        return "weak_qualified_reddit_support"
    return "no_qualified_reddit_evidence"


def build_evidence_pack(claims: list[dict], reddit_json: list[Path]) -> dict:
    items = [item for path in reddit_json for item in iter_reddit_items(path)]
    claim_evidence = []
    for claim in claims:
        scored = [
            (evidence_score(claim, item), item)
            for item in items
            if item.get("text")
        ]
        top = [
            {
                "score": round(score, 3),
                "kind": item["kind"],
                "id": item["id"],
                "author": item["author"],
                "reddit_score": item["score"],
                "depth": item["depth"],
                "source_json": item["source_json"],
                "source_url": item.get("source_url", ""),
                "permalink": item.get("permalink", ""),
                "subreddit": item.get("subreddit", ""),
                "qualification": qualification_for(claim, item),
                "excerpt": excerpt(item["text"]),
            }
            for score, item in sorted(scored, key=lambda pair: pair[0], reverse=True)
            if score >= 0.18
        ][:5]
        rejected_count = sum(1 for item in items if item.get("text") and not qualification_for(claim, item)["qualified"])
        claim_evidence.append(
            {
                "claim_id": claim["id"],
                "evidence_count": len(top),
                "items_considered": len([item for item in items if item.get("text")]),
                "items_rejected_by_qualification_gate": rejected_count,
                "suggested_reddit_verdict": reddit_verdict(claim, top),
                "evidence": top,
            }
        )
    return {"claims": claim_evidence, "source_files": [str(path) for path in reddit_json]}


def write_json(path: Path, data: object) -> None:
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_report(source: Path, extraction_method: str, claims: list[dict], evidence_pack: dict | None) -> str:
    lines = [
        "# Reddit Fact-Check Report",
        "",
        f"- Status: {'draft' if claims else 'blocked'}",
        f"- Source: `{source}`",
        f"- Extraction method: `{extraction_method}`",
        f"- Claims extracted: {len(claims)}",
        "",
        "## Method",
        "",
        "Reddit evidence is treated as community/operator evidence. Raw Reddit matches are not evidence until they pass the qualification gate: relevant subreddit or source context, matching persona/workflow language, and concrete pain/workaround signal. Numeric, regulatory, market-size, funding, adoption, and date claims remain primary-source-required unless the claim only asks whether Reddit discusses the issue.",
        "",
        "## Claim Inventory",
        "",
    ]
    evidence_by_id = {}
    if evidence_pack:
        evidence_by_id = {item["claim_id"]: item for item in evidence_pack.get("claims", [])}
    for claim in claims:
        evidence = evidence_by_id.get(claim["id"], {})
        verdict = evidence.get("suggested_reddit_verdict", "pending_reddit_evidence")
        lines.extend(
            [
                f"### {claim['id']} - {claim['locator']}",
                "",
                f"Claim: {claim['claim']}",
                "",
                f"- Evidence need: `{claim['evidence_need']}`",
                f"- Reddit query: `{claim['reddit_query']}`",
                f"- Primary source required: `{str(claim['primary_source_required']).lower()}`",
                f"- Reddit evidence status: `{verdict}`",
                f"- Reddit qualification rejects: `{evidence.get('items_rejected_by_qualification_gate', 0)}`",
                "",
            ]
        )
        for item in evidence.get("evidence", [])[:3]:
            location = item.get("permalink") or item.get("source_url") or item["source_json"]
            lines.extend(
                [
                    f"  - Reddit {item['kind']} `{item['id']}` score {item['reddit_score']} from `{location}`",
                    f"    - {item['excerpt']}",
                ]
            )
        if evidence.get("evidence"):
            lines.append("")
    if not claims:
        lines.extend(
            [
                "No claims were extracted. If this was an image-only PPTX or scanned PDF, run OCR or provide a text/Markdown sidecar.",
                "",
            ]
        )
    lines.extend(
        [
            "## Follow-Up",
            "",
            "- Extract or provide Reddit thread URLs for every high-priority query.",
            "- Use official sources for all `primary_required` and `mixed` claims.",
            "- Have the agent review evidence excerpts before marking the report reviewed.",
            "",
        ]
    )
    return "\n".join(lines)


def default_out_dir(input_path: Path) -> Path:
    return Path("runs") / f"{date.today().isoformat()}-reddit-factcheck-{slugify(input_path.stem)}"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to .md, .txt, .pptx, or .pdf")
    parser.add_argument("--topic", default="", help="Topic context for Reddit queries")
    parser.add_argument("--out-dir", default="", help="Run output directory")
    parser.add_argument("--max-claims", type=int, default=40)
    parser.add_argument("--reddit-json", action="append", default=[], help="Existing reddit_thread_extractor JSON output")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    input_path = Path(args.input).expanduser()
    if not input_path.exists():
        sys.stderr.write(f"Input not found: {input_path}\n")
        return 2
    out_dir = Path(args.out_dir) if args.out_dir else default_out_dir(input_path)
    out_dir.mkdir(parents=True, exist_ok=True)

    try:
        segments, extraction_method = read_document(input_path)
    except ValueError as exc:
        sys.stderr.write(str(exc) + "\n")
        return 2

    segment_rows = [
        {"id": f"segment-{i:03d}", "locator": s.locator, "source": s.source, "text": s.text}
        for i, s in enumerate(segments, 1)
        if s.text.strip()
    ]
    claims = extract_claims(segments, args.topic or input_path.stem, args.max_claims)
    evidence_pack = None
    reddit_paths = [Path(p).expanduser() for p in args.reddit_json]
    if reddit_paths:
        missing = [str(path) for path in reddit_paths if not path.exists()]
        if missing:
            sys.stderr.write("Reddit JSON not found: " + ", ".join(missing) + "\n")
            return 2
        evidence_pack = build_evidence_pack(claims, reddit_paths)
        write_json(out_dir / "reddit-evidence-pack.json", evidence_pack)

    write_json(
        out_dir / "document-segments.json",
        {
            "source": str(input_path),
            "extraction_method": extraction_method,
            "segments": segment_rows,
        },
    )
    write_json(
        out_dir / "claim-pack.json",
        {
            "source": str(input_path),
            "topic": args.topic,
            "claims": claims,
        },
    )
    (out_dir / "reddit-factcheck-report.md").write_text(
        render_report(input_path, extraction_method, claims, evidence_pack),
        encoding="utf-8",
    )
    print(out_dir)
    if extraction_method in {"pptx-image-only", "pdf-text-unavailable"}:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
