#!/usr/bin/env python3
"""Check a LinkedIn post draft against the experiment-to-linkedin post rules.

Reads the `## Draft` section of the file (or the whole file if there is none) and prints
PASS/WARN/FAIL lines. Exits 1 if any FAIL. Stdlib only.

Usage: python3 check_post.py <linkedin-post-draft.md>
"""
import re
import sys

BANNED = [
    "delve", "leverage", "utilize", "robust", "seamless", "comprehensive", "cutting-edge",
    "game-changer", "game changer", "transformative", "transformational", "unlock", "harness",
    "elevate", "streamline", "powerful", "crucial", "journey", "landscape", "synergy",
    "deep dive", "here's the thing", "honestly", "excited to share", "thrilled to",
    "it's important to note", "at the end of the day", "let's unpack", "in today's",
]
HOOK_LIMIT = 210


def draft_text(raw: str) -> str:
    m = re.search(r"^## Draft\s*\n(.*?)(?=^## |\Z)", raw, re.S | re.M)
    return (m.group(1) if m else raw).strip()


def main(path: str) -> int:
    text = draft_text(open(path, encoding="utf-8").read())
    body = re.sub(r"(?m)^#\w.*$", "", text).strip()  # drop the hashtag line for counts
    words = len(body.split())
    results = []

    def add(level, msg):
        results.append((level, msg))

    add("PASS" if 100 <= words <= 200 else "WARN", f"words: {words} (target 100-200)")
    add("PASS" if len(text) <= 1300 else "WARN", f"characters: {len(text)}")
    first_para = body.split("\n\n")[0]
    add("PASS" if len(first_para) <= HOOK_LIMIT else "FAIL",
        f"first paragraph {len(first_para)} chars (must fit the ~{HOOK_LIMIT}-char 'see more' cut)")
    low = text.lower()
    hits = [b for b in BANNED if b in low]
    add("FAIL" if hits else "PASS", f"banned words/phrases: {hits or 'none'}")
    dashes = text.count("—")
    add("FAIL" if dashes > 1 else "PASS", f"em dashes: {dashes} (max 1)")
    lines = [l.strip() for l in body.splitlines() if l.strip()]
    add("FAIL" if lines and lines[-1].endswith("?") else "PASS", "closer is not a question")
    code = re.search(r"`|\(\)\s*\{|\$\(|=\S+\s+\w+\s+\"\$@\"", text)
    add("FAIL" if code else "PASS", "no code in the post body (put it on a slide)")
    emoji = re.findall(r"[\U0001F300-\U0001FAFF☀-➿]", text)
    add("FAIL" if len(emoji) > 1 else "PASS", f"emoji: {len(emoji)} (max 1)")
    arrows = text.count("→")
    add("WARN" if arrows > 1 else "PASS", f"arrows: {arrows} (an outline of arrows reads as slide notes)")
    numbered = len(re.findall(r"(?m)^\d+\.\s", body))
    add("WARN" if numbered >= 3 else "PASS", f"numbered lines: {numbered} (prefer sentences)")
    long_paras = [p for p in body.split("\n\n") if len(re.findall(r"[.!?](\s|$)", p)) > 3]
    add("WARN" if long_paras else "PASS", f"paragraphs over 3 sentences: {len(long_paras)}")

    for level, msg in results:
        print(f"{level:4}  {msg}")
    return 1 if any(l == "FAIL" for l, _ in results) else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(__doc__)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
