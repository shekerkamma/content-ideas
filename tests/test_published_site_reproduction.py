"""Static and behavioural guards for the published-site reproduction gate.

Lives in docs/ rather than skills/: it checks whether a source tree rebuilds a
published site, a job that recurs only when a site's source is recovered, so it
is kept findable without loading into every session.

Every assertion here pins a defect class the gate was written to catch. The
broken fixture is the negative control: a clean run on a clean fixture is not
evidence the gate works, that fixture is.
"""
import ast
import json
import pathlib
import subprocess
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "published-site-reproduction"
GATE = DOC / "check_reproduction.py"
FIX = DOC / "fixtures"


def run(fixture, *args):
    r = subprocess.run(
        [sys.executable, str(GATE), str(FIX / fixture / "manifest.json"), *args],
        capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def test_script_parses():
    ast.parse(GATE.read_text(), filename=str(GATE))


def test_clean_fixture_passes():
    code, out, err = run("clean")
    assert code == 0, out + err
    assert "UNVERIFIED" in out, "a reproduced build must still disclaim runtime and media"


def test_broken_fixture_fires_every_defect_class():
    code, _, err = run("broken")
    assert code == 2
    for expect in (
        "size differs by -14 bytes",              # a size delta is a missing build input
        "VITE_RERANK_ENDPOINT",                   # ... and the message must name it
        "no explanation is declared",             # an undeclared difference never passes
        "the waiver is stale",                    # an explanation that excuses nothing
        "needs a non-empty reason",               # evidence-gated, not a bare waiver
        "cannot have been compared",              # a glob matching nothing is a finding
        "pins a content-hash filename",           # a pinned name breaks instead of measuring
    ):
        assert expect in err, f"missing finding: {expect}\n{err}"


def test_empty_manifest_does_not_pass():
    """An empty population otherwise passes every check."""
    code, _, err = run("empty")
    assert code == 2
    assert "passes everything" in err


def test_missing_manifest_is_blocked_not_clean():
    r = subprocess.run([sys.executable, str(GATE), str(FIX / "nope.json")],
                       capture_output=True, text=True)
    assert r.returncode == 1, "a gate that cannot read its input must block, never report clean"
    assert "BLOCKED" in r.stderr


def test_hash_name_warning_is_not_duplicated():
    """published and rebuilt default to the same pattern; warn once, not twice."""
    _, _, err = run("broken")
    assert err.count("pins a content-hash filename") == 1


def test_fetch_follows_dynamic_imports(tmp_path):
    """The entry document names only static assets, so HTML-only collection is partial.

    Served from a local http.server rather than asserted against the source text:
    a test that greps the gate for the word "import" would pass on a gate that
    never crawls.
    """
    import functools
    import http.server
    import threading

    root = FIX / "site"
    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        manifest = tmp_path / "manifest.json"
        manifest.write_text(json.dumps({
            "site": f"http://127.0.0.1:{server.server_port}/",
            "published": "live",
            "rebuilt": "live",
            "artifacts": [{"role": "app", "published": "assets/app.js", "expect": "identical"}],
        }))
        r = subprocess.run([sys.executable, str(GATE), str(manifest), "--fetch", "live"],
                           capture_output=True, text=True)
        assert r.returncode == 0, r.stdout + r.stderr
    finally:
        server.shutdown()

    fetched = tmp_path / "live"
    assert (fetched / "assets" / "app.js").exists(), "static asset not collected"
    assert (fetched / "assets" / "app.css").exists(), "stylesheet not collected"
    assert (fetched / "assets" / "lazy-chunk.js").exists(), (
        "dynamically imported chunk not collected — the fetch stopped at the entry document")


def test_fixtures_are_wired_to_the_defects_they_claim():
    """A fixture that drifted from its manifest stops being a control."""
    for name in ("clean", "broken", "empty"):
        manifest = json.loads((FIX / name / "manifest.json").read_text())
        for key in ("published", "rebuilt"):
            assert (FIX / name / manifest[key]).is_dir(), f"{name}: missing {key} directory"
    broken = json.loads((FIX / "broken" / "manifest.json").read_text())
    roles = {a["role"] for a in broken["artifacts"]}
    assert {"app-bundle", "stylesheet", "retrieval-index", "worker", "legend", "pinned-name"} <= roles
