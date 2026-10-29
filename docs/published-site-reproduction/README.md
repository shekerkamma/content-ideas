# Published-site reproduction gate

A check that a source tree rebuilds the bytes a host is actually serving, rather
than merely building without error.

**This is a reference, not a loaded skill.** It gates a job that recurs whenever a
static site's source is recovered, re-uploaded, or handed to someone else, which
is rare enough that it should not cost a catalog entry every session. Promote it
— add a `SKILL.md`, copy to the skill trees — if site recovery becomes routine.

## Run it

```bash
# 1. collect what the host is serving right now
python3 docs/published-site-reproduction/check_reproduction.py manifest.json --fetch live-bytes

# 2. build from source, then compare
python3 docs/published-site-reproduction/check_reproduction.py manifest.json
# 0 clean, 1 blocked, 2 findings
```

Fixtures: `fixtures/clean` passes, `fixtures/broken` fires eight findings across
six defect classes, and `fixtures/empty` isolates the population guard so that
branch is proven rather than assumed. `tests/test_published_site_reproduction.py`
keeps all three honest.

## The manifest

```json
{
  "site": "https://user.github.io/project/",
  "published": "live-bytes",
  "rebuilt": "dist",
  "build_env": ["VITE_RERANK_ENDPOINT"],
  "artifacts": [
    {"role": "stylesheet", "published": "assets/index-*.css", "expect": "identical"},
    {"role": "retrieval-index", "published": "assets/knowledge-index-*.js",
     "expect": "explained", "max_differing_bytes": 32,
     "reason": "the generator embeds its own build timestamp; unit count and score match"}
  ]
}
```

`published` and `rebuilt` are directories. Each artifact is matched by glob inside
both, because a bundler names files by content hash and a pinned name breaks on
the next build instead of measuring it. `base_path` strips a GitHub Pages project
prefix during `--fetch`; `entry` defaults to `index.html`.

## What it enforces

- **A difference must be explained per artifact, with a reason and a byte cap.**
  `expect: identical` means what it says. `expect: explained` is the only way to
  pass with a difference, and an empty `reason` fails.
- **A waiver that excuses nothing is reported.** An artifact declared `explained`
  that comes back byte-identical fires a finding, because a rule that went green
  without anyone knowing why has stopped measuring.
- **A size delta is never rounding.** It is reported separately from a
  same-size difference and the message names every variable in `build_env`,
  because that is what a size delta almost always is.
- **A glob matching zero files is a finding, and so is a manifest with no
  artifacts.** An empty population otherwise passes every check.
- **`--fetch` follows dynamic imports.** The entry document names only statically
  loaded assets, so walking the HTML alone silently collects a partial set.

## Why each rule exists

Measured on 2026-09-12 recovering the source of two published DeepGrid sites.

**A build-time variable can delete a code path and leave a clean build behind.**
The live bundle was 1,502,679 bytes; the first rebuild from the recovered source
came out at 1,501,652 with no error, no warning, and a working page. The missing
1,027 bytes were a reranking client whose endpoint arrives through
`VITE_RERANK_ENDPOINT`, documented in that project's own source as optional and
degrading safely. Nothing else in the tree names the endpoint, so an unset shell
produces something that looks exactly like a successful reproduction. The size
delta was the only tell, which is why it is a first-class finding here.

**Content-hash filenames make byte-identity the wrong question at the file level.**
The correct rebuild differed from the published bundle in 8 bytes out of 1.5 MB:
the name of a chunk it imports dynamically. That chunk in turn differed in 10
bytes out of 991,068 — its generator's embedded build timestamp — while its
retrieval unit count and relevance score matched exactly. Two files "differ" and
the site is reproduced. Writing that down as a capped, reasoned explanation is
the point; leaving it in prose is how it gets forgotten.

**Prose about a rebuild drifts from the rebuild.** Running this gate against the
real case immediately contradicted a hand-written claim that the bundle was
byte-identical. It was not, by 8 bytes, for a reason that was fine. The gate
turned a loose sentence into a declared cap.

**A partial fetch reads as a passing comparison.** The first `--fetch` collected
two assets because the entry document referenced two. The third, a 991 KB
retrieval index, is reached only through a dynamic `import()` inside the bundle
and would never have been compared at all.

## What it does not check

Runtime behaviour, and any media the page loads from somewhere else. Both
DeepGrid pages load their films from a directory on a different repository's
`gh-pages` branch, which no comparison of build output can see. Reproducing the
bytes is not the same as the page working.
