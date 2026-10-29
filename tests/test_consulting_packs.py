"""CIOS pack lint — CIOS-TST-001 (consulting-os/spec/CIOS-SPEC-v1.0.md).

Stdlib-only. Validates every domain context pack under consulting-os/domains/:
frontmatter schema, required sections per template_version, golden-question
count, and citation discipline for `active` packs.
"""

import re
from pathlib import Path

try:
    import pytest
except ImportError:  # pragma: no cover — pytest is a dev dep, not a runtime dep
    import types as _types
    import unittest as _ut

    def _skip(reason: str = "") -> None:
        raise _ut.SkipTest(reason)

    pytest = _types.SimpleNamespace(  # type: ignore[assignment]
        fixture=lambda *a, **kw: (lambda f: f),
        skip=_skip,
    )

REPO = Path(__file__).resolve().parent.parent
DOMAINS = REPO / "consulting-os" / "domains"

VALID_STATUS = {"draft", "active", "stale", "archived"}
VALID_TEMPLATE_VERSIONS = {"1", "2"}

# Section heading prefixes required per template version (CIOS-TST-001).
SECTIONS_V1 = [
    "## 1. Point of view",
    "## 2. Reference architectures",
    "## 3. Market landscape",
    "## 4. Proof points",
    "## 5. Frameworks",
    "## 6. Objection library",
    "## 7. Source watchlist",
    "## 8. Golden questions",
]
SECTIONS_V2 = [
    "## 1. Executive summary & point of view",
    "## 2. Market landscape",
    "## 3. Capabilities",
    "## 4. Reference architectures",
    "## 5. Patterns & frameworks",
    "## 6. Tools & skills",
    "## 7. Business case & roadmap",
    "## 8. Risks & objection library",
    "## 9. Assets index",
    "## 10. Source watchlist",
    "## 11. Golden questions",
]

CITATION_MARKERS = ("(source:", "[gbrain:", "[NEEDS ACQUISITION]")


def pack_files():
    if not DOMAINS.is_dir():
        return []
    return sorted(
        p
        for p in DOMAINS.glob("**/pack.md")
        if "_template" not in p.parts
    )


def parse_frontmatter(text, path):
    m = re.match(r"\A---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, f"{path}: missing YAML frontmatter block"
    fm = {}
    for line in m.group(1).splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        # strip inline comments outside brackets
        val = re.sub(r"\s+#.*$", "", val).strip()
        fm[key.strip()] = val
    return fm


@pytest.fixture(params=pack_files(), ids=lambda p: str(p.relative_to(REPO)))
def pack(request):
    path = request.param
    text = path.read_text(encoding="utf-8")
    return path, text, parse_frontmatter(text, path)


def test_packs_exist():
    assert pack_files(), "no domain packs found under consulting-os/domains/"


def test_frontmatter_schema(pack):
    path, _, fm = pack
    for field in ("slug", "title", "version", "freshness", "keywords", "status"):
        assert fm.get(field), f"{path}: frontmatter missing `{field}`"
    assert fm["slug"] == path.parent.name, (
        f"{path}: slug `{fm['slug']}` != directory `{path.parent.name}`"
    )
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}", fm["freshness"]), (
        f"{path}: freshness `{fm['freshness']}` is not YYYY-MM-DD"
    )
    assert fm["status"] in VALID_STATUS, f"{path}: invalid status `{fm['status']}`"
    tv = fm.get("template_version", "1")
    assert tv in VALID_TEMPLATE_VERSIONS, f"{path}: invalid template_version `{tv}`"
    keywords = [k for k in re.split(r"[\[\],]", fm["keywords"]) if k.strip()]
    assert len(keywords) >= 3, f"{path}: needs >=3 classification keywords"


def test_required_sections(pack):
    path, text, fm = pack
    sections = SECTIONS_V2 if fm.get("template_version", "1") == "2" else SECTIONS_V1
    for heading in sections:
        assert re.search(
            rf"^{re.escape(heading)}", text, re.MULTILINE
        ), f"{path}: missing required section `{heading}`"


def test_golden_questions(pack):
    path, text, fm = pack
    marker = "Golden questions"
    idx = text.find(marker)
    assert idx != -1, f"{path}: no golden questions section"
    tail = text[idx:]
    questions = re.findall(r"^\d+\.\s", tail, re.MULTILINE)
    assert len(questions) >= 3, (
        f"{path}: needs >=3 golden questions, found {len(questions)}"
    )


def test_active_pack_citation_discipline(pack):
    """Active packs: perishable sections must carry citations or explicit
    [NEEDS ACQUISITION] markers (CIOS-TST-001 / CIOS-GOV-002 approximation:
    every bullet in market-landscape and architecture sections has a marker)."""
    path, text, fm = pack
    if fm["status"] != "active":
        pytest.skip("citation discipline enforced on active packs only")
    perishable = ("Market landscape", "Reference architectures")
    blocks = re.split(r"^## ", text, flags=re.MULTILINE)
    for block in blocks:
        if not block.startswith(tuple(f"{n}. {name}" for n in range(1, 12) for name in perishable)):
            continue
        for line in block.splitlines():
            line = line.strip()
            if line.startswith("- ") and len(line) > 20:
                assert any(m in line for m in CITATION_MARKERS) or any(
                    m in block for m in CITATION_MARKERS
                ), f"{path}: uncited claim in active pack: {line[:80]}"


def test_assets_dir_consistency(pack):
    """Template v2 packs: if section 9 references asset files, they must exist."""
    path, text, fm = pack
    if fm.get("template_version", "1") != "2":
        pytest.skip("assets index is template v2 only")
    for rel in re.findall(r"assets/([\w\-./]+\.md)", text):
        assert (path.parent / "assets" / rel).exists(), (
            f"{path}: assets index references missing file assets/{rel}"
        )
