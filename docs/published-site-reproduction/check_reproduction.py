#!/usr/bin/env python3
"""Gate a rebuilt static site against the bytes a host is actually serving.

Exit 0 clean, 1 blocked (cannot read the manifest or a directory), 2 findings.

A source tree that builds is not a source tree that reproduces. Every check here
exists because the defect it catches leaves a successful build behind: a missing
build-time variable that silently drops a code path, a waiver that outlived the
difference it excused, a glob that matched nothing and so proved nothing.

  check   compare a rebuilt directory against published bytes already on disk
  fetch   download the published bytes first, from the live entry document
"""
import argparse, fnmatch, hashlib, json, pathlib, re, sys

# --- editable policy ---
# A difference this small is plausibly a stamp (timestamp, build id, nonce).
# Anything larger must be explained per artifact, not waived wholesale.
DEFAULT_MAX_EXPLAINED_BYTES = 64
# Segments that look like content hashes: a name carrying one changes whenever
# the file does, so an artifact must be matched by glob and never by exact name.
HASHED_NAME = re.compile(r"[-.][A-Za-z0-9_-]{8,}\.(js|css|mjs)$")


def blocked(msg):
    print(f"BLOCKED: {msg}", file=sys.stderr)
    sys.exit(1)


def load(path):
    try:
        data = json.loads(pathlib.Path(path).read_text())
    except FileNotFoundError:
        blocked(f"no manifest at {path}")
    except json.JSONDecodeError as e:
        blocked(f"manifest is not valid JSON ({e})")
    if not isinstance(data, dict):
        blocked("manifest must be a JSON object")
    return data


def resolve(root, pattern, side, role, findings):
    """Match exactly one file. Zero matches is a finding, never a silent pass."""
    matches = sorted(
        p for p in root.rglob("*")
        if p.is_file() and fnmatch.fnmatch(str(p.relative_to(root)).replace("\\", "/"), pattern)
    )
    if not matches:
        findings.append(
            f"{role}: no {side} file matches {pattern!r} under {root} — "
            f"an artifact that was never found cannot have been compared")
        return None
    if len(matches) > 1:
        names = ", ".join(str(m.relative_to(root)) for m in matches[:4])
        findings.append(f"{role}: {pattern!r} matched {len(matches)} {side} files ({names}) — ambiguous")
        return None
    return matches[0]


def differing_bytes(a: bytes, b: bytes) -> int:
    return sum(1 for x, y in zip(a, b) if x != y) + abs(len(a) - len(b))


def check(manifest, manifest_dir):
    findings, rows = [], []

    published_dir = (manifest_dir / manifest.get("published", "")).resolve()
    rebuilt_dir = (manifest_dir / manifest.get("rebuilt", "")).resolve()
    for label, d in (("published", published_dir), ("rebuilt", rebuilt_dir)):
        if not d.is_dir():
            blocked(f"{label} directory does not exist: {d}")

    build_env = manifest.get("build_env") or []
    artifacts = manifest.get("artifacts") or []
    if not artifacts:
        # The population guard. A manifest with nothing in it must not report clean.
        findings.append("manifest declares no artifacts — a comparison of nothing passes everything")

    for i, art in enumerate(artifacts):
        role = art.get("role") or f"<artifact {i}>"
        pub_pat = art.get("published")
        reb_pat = art.get("rebuilt", pub_pat)
        expect = art.get("expect", "identical")

        if not pub_pat:
            findings.append(f"{role}: no published pattern")
            continue
        if expect not in ("identical", "explained"):
            findings.append(f"{role}: expect must be 'identical' or 'explained', got {expect!r}")
            continue
        for pat in dict.fromkeys([pub_pat, reb_pat]):
            if HASHED_NAME.search(pat) and "*" not in pat:
                findings.append(
                    f"{role}: {pat!r} pins a content-hash filename — match it by glob, "
                    f"or the gate breaks on the next build instead of measuring it")

        pub = resolve(published_dir, pub_pat, "published", role, findings)
        reb = resolve(rebuilt_dir, reb_pat, "rebuilt", role, findings)
        if pub is None or reb is None:
            continue

        pb, rb = pub.read_bytes(), reb.read_bytes()
        same = pb == rb
        delta = len(rb) - len(pb)
        ndiff = 0 if same else differing_bytes(pb, rb)
        rows.append((role, pub.name, reb.name, len(pb), delta, ndiff, expect, same))

        if same:
            if expect == "explained":
                # A waiver that no longer excuses anything is a rule that stopped
                # measuring. Make it say so rather than quietly staying green.
                findings.append(
                    f"{role}: declared 'explained' but reproduced byte-identical — "
                    f"the waiver is stale, remove it or say what changed")
            continue

        if delta != 0:
            hint = (f" Build-time inputs this site reads: {', '.join(build_env)}."
                    if build_env else "")
            findings.append(
                f"{role}: size differs by {delta:+d} bytes ({len(pb)} published, {len(rb)} rebuilt) — "
                f"a size delta is a missing or changed build input, not rounding.{hint}")
            continue

        if expect != "explained":
            findings.append(
                f"{role}: same size, {ndiff} byte(s) differ, and no explanation is declared")
            continue

        reason = (art.get("reason") or "").strip()
        if not reason:
            findings.append(f"{role}: 'explained' needs a non-empty reason")
        cap = art.get("max_differing_bytes", DEFAULT_MAX_EXPLAINED_BYTES)
        if ndiff > cap:
            findings.append(
                f"{role}: {ndiff} byte(s) differ, over the declared cap of {cap} — "
                f"reason on file is {reason!r}")

    return findings, rows


def fetch(manifest, manifest_dir, into):
    """Download the live entry document and every local asset it references."""
    from urllib.parse import urljoin
    from urllib.request import urlopen

    site = manifest.get("site")
    if not site:
        blocked("manifest has no 'site' to fetch from")
    if not site.endswith("/"):
        site += "/"
    entry = manifest.get("entry", "index.html")
    out = (manifest_dir / into).resolve()
    out.mkdir(parents=True, exist_ok=True)

    html = urlopen(urljoin(site, entry), timeout=30).read()
    (out / entry).write_bytes(html)
    text = html.decode("utf-8", "replace")

    base_path = manifest.get("base_path", "")
    refs, seen = [], set()
    for ref in re.findall(r'(?:src|href)="([^"?#]+)"', text):
        if ref.startswith(("http://", "https://", "//", "data:", "mailto:")):
            continue
        rel = ref[2:] if ref.startswith("./") else ref
        if base_path and rel.startswith(base_path.strip("/") + "/"):
            rel = rel[len(base_path.strip("/")) + 1:]
        rel = rel.lstrip("/")
        if not rel or rel in seen:
            continue
        seen.add(rel)
        refs.append(rel)

    if not refs:
        blocked(f"{entry} references no local assets — nothing to compare against")

    # The entry document names only statically loaded assets. A dynamically
    # imported chunk appears nowhere in the HTML, so walking the document alone
    # collects a partial set and the missing chunk is never compared. Follow
    # relative import specifiers out of each fetched script until nothing new
    # turns up.
    queue, fetched = list(refs), []
    while queue:
        rel = queue.pop(0)
        dest = out / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(urlopen(urljoin(site, rel), timeout=60).read())
        fetched.append(rel)
        print(f"  fetched {rel}")
        if not rel.endswith((".js", ".mjs")):
            continue
        body = dest.read_bytes().decode("utf-8", "replace")
        parent = rel.rsplit("/", 1)[0] + "/" if "/" in rel else ""
        for spec in re.findall(r"""import\(\s*["'`]\./([^"'`]+)["'`]""", body):
            nxt = parent + spec
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)

    print(f"\n{len(fetched)} published asset(s) saved under {out}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("manifest")
    ap.add_argument("--fetch", metavar="DIR",
                    help="download published bytes from the live site into DIR, then stop")
    a = ap.parse_args()

    manifest_dir = pathlib.Path(a.manifest).resolve().parent
    manifest = load(a.manifest)

    if a.fetch:
        return fetch(manifest, manifest_dir, a.fetch)

    findings, rows = check(manifest, manifest_dir)

    print(f"{manifest.get('site', '<no site declared>')}")
    print(f"{len(rows)} artifact(s) compared")
    for role, pub_name, reb_name, size, delta, ndiff, expect, same in rows:
        if same:
            verdict = "identical"
        elif delta:
            verdict = f"size {delta:+d}"
        else:
            verdict = f"{ndiff}B differ"
        rename = "" if pub_name == reb_name else f"  ({pub_name} -> {reb_name})"
        print(f"  {role:<16} {size:>9,}B  {verdict:<12} {expect}{rename}")

    if findings:
        sys.stdout.flush()
        print(f"\n{len(findings)} finding(s):", file=sys.stderr)
        for x in findings:
            print(f"  - {x}", file=sys.stderr)
        return 2

    print("\nrebuild reproduces the published bytes. "
          "Runtime behaviour and externally hosted media remain UNVERIFIED.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
