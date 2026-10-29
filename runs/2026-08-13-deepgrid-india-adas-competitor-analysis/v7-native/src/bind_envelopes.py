#!/usr/bin/env python3
"""bind_envelopes.py — bind the 73 dossier slides to the seven adapted prompt templates.

Deliverable 2, stage 1. The prompt-template deck declares a TYPED CONTENT ENVELOPE
per pattern (rungs / matrix / stages / positions / phases / steps / claims). This
projects each slide's extracted evidence into the envelope its pattern requires,
then validates it against that pattern's stated rules.

A slide that cannot satisfy its pattern's rules is NOT forced. It falls back to
P4 Bounded Argument, which every envelope can satisfy honestly because P4's own
WHEN TO USE is "no structured evidence exists — the reasoning is the exhibit".
Every fallback is recorded with its reason, so the deck never claims a structure
its evidence cannot draw.

    python3 src/bind_envelopes.py
"""
import json
import re
import sys
from collections import Counter, defaultdict

RUN = "."
RATINGS = ["HIGHEST", "HIGH", "MEDIUM-HIGH", "MEDIUM", "LOW-MEDIUM", "LOW", "NONE"]
STATUS_CONF = {
    "verified fact": 0.92,
    "attributed claim": 0.68,
    "qualified interpretation": 0.46,
    "insufficient evidence": 0.22,
}
STATUS_ORDER = list(STATUS_CONF)
ARENA_RE = re.compile(r"(PSU|OEM|Tier-?1|Fleet|Mining|Govern?ment|Govt|Yard|N2/N3|Retrofit)", re.I)
SECTION_WORDS = re.compile(
    r"^(verified facts?|competitive reading|strategic action|trigger|owner|decision|"
    r"uncertain|signals?|governance|evidence requirements?|action items?|comparison rule|"
    r"required bridge|value chain|sprint|gate criteria)", re.I)
MONEY = re.compile(r"^[+-]?[$₹]\s?[\d,.]+[kKmMbB]?$")


def words_label(text, limit=30):
    """A short topical label taken from the head of a claim."""
    t = re.sub(r"\s+", " ", str(text)).strip().strip("·-—:")
    t = re.sub(r"^(the|a|an)\s+", "", t, flags=re.I)
    out = []
    for w in t.split(" "):
        if len(" ".join(out + [w])) > limit:
            break
        out.append(w)
    if not out:
        out = t.split(" ")[:2]
    return " ".join(out).strip(" ,.;:·")


def is_rating(s):
    return str(s).strip().upper() in RATINGS


def cap(s, n):
    s = re.sub(r"\s+", " ", str(s)).strip()
    return s if len(s) <= n else s[: n - 1].rstrip() + "…"


# ─────────────────────────────────────────────────────────────── P1 ladder ──
def bind_ladder(s):
    blocks = [b for b in s["evidence_blocks"] if len(b.get("claim", "")) > 12]
    by_status = defaultdict(list)
    for b in blocks:
        by_status[b.get("status", "qualified interpretation")].append(b)
    for k in by_status:
        by_status[k].sort(key=lambda b: -len(b["claim"]))

    picked = []
    for st in STATUS_ORDER:
        if by_status.get(st):
            picked.append((st, by_status[st][0]))
    # top up to four from the richest tiers, preserving status order
    if len(picked) < 4:
        pool = [(st, b) for st in STATUS_ORDER for b in by_status.get(st, [])[1:]
                if len(b["claim"]) >= 45]
        pool += [(st, b) for st in STATUS_ORDER for b in by_status.get(st, [])[1:]
                 if len(b["claim"]) < 45]
        picked += pool[: 4 - len(picked)]
        picked.sort(key=lambda p: STATUS_ORDER.index(p[0]))
    picked = picked[:4]

    rungs = []
    for i, (st, b) in enumerate(picked):
        rungs.append({
            "label": words_label(b["claim"], 28).upper(),
            "text": cap(b["claim"], 160),
            "status": st,
            "confidence": round(max(0.14, STATUS_CONF[st] - i * 0.02), 2),
            "raises_it": b.get("gap") or "",
            "evidence_ids": [b.get("evidence_id", "")],
        })
    # the ladder must show where it stops being evidence
    if not any(r["status"] == "insufficient evidence" for r in rungs):
        if len(rungs) == 4:
            rungs.pop()
        rungs.append({
            "label": "NOT YET EVIDENCED",
            "text": cap(s.get("falsifier") or s.get("counterargument") or "", 160),
            "status": "insufficient evidence",
            "confidence": 0.18,
            "raises_it": "", "evidence_ids": [],
        })
    for i in range(1, len(rungs)):                       # force strict descent
        if rungs[i]["confidence"] >= rungs[i - 1]["confidence"]:
            rungs[i]["confidence"] = round(rungs[i - 1]["confidence"] - 0.06, 2)

    if len(rungs) < 3 or not rungs[0]["text"]:
        return None, "fewer than three usable evidence tiers"
    gap = s.get("falsifier", "") or ""
    if gap and rungs and cap(gap, 160) == rungs[-1]["text"]:
        gap = ""                      # already shown as the weakest rung
    return {"pattern": "evidence-ladder",
            "observable_position": s["executive_answer"],
            "rungs": rungs,
            "gap": gap}, None


# ────────────────────────────────────────────────────────────── P2 heatmap ──
def bind_heatmap(s):
    sb = s.get("supporting_blocks") or []
    arenas, arena_head = [], []
    for b in sb[:7]:
        cand = b.get("label", "").strip() or b.get("text", "")
        c = re.sub(r"\s+", " ", cand).strip()
        if c and len(c) < 26 and ARENA_RE.search(c) and not is_rating(c) and c not in arenas:
            arenas.append(c)
            arena_head.append(b)
    arenas, arena_head = arenas[:3], arena_head[:3]
    if len(arenas) < 3:
        return None, "fewer than three arenas in the source matrix"

    head_ratings = [(b.get("tags") or [None])[0] for b in arena_head]
    rows, cur = [], None
    start = sb.index(arena_head[-1]) + 1
    for b in sb[start:]:
        lab = re.sub(r"\s+", " ", b.get("label", "")).strip()
        if is_rating(lab):
            if cur is not None and len(cur["cells"]) < len(arenas):
                cur["cells"].append({"rating": lab.upper(), "note": cap(b.get("text", ""), 46)})
        elif (lab and not SECTION_WORDS.match(lab) and len(lab) < 30
              and lab not in arenas):
            if cur and len(cur["cells"]) == len(arenas):
                rows.append(cur)
            cur = {"label": lab, "cells": [], "note": cap(b.get("text", ""), 46)}
    if cur and len(cur["cells"]) == len(arenas):
        rows.append(cur)

    # the header row's own tags are the first entity's ratings in this source shape
    if all(r and is_rating(r) for r in head_ratings) and len(head_ratings) == len(arenas):
        first = None
        for b in sb[start:]:
            lab = re.sub(r"\s+", " ", b.get("label", "")).strip()
            if (lab and not is_rating(lab) and not SECTION_WORDS.match(lab)
                    and len(lab) < 30 and lab not in arenas):
                first = lab
                break
        if first and not any(r["label"] == first and r["cells"] for r in rows):
            rows.insert(0, {"label": first,
                            "cells": [{"rating": head_ratings[i].upper(),
                                       "note": cap(arena_head[i].get("text", ""), 46)}
                                      for i in range(len(arenas))]})
    rows = [r for r in rows if len(r["cells"]) == len(arenas)][:4]
    # One competitor rated across three arenas is a valid P2 exhibit — that is
    # literally its WHEN TO USE ("a competitor's power differs by who is buying").
    if len(rows) < 1:
        return None, "no complete row of ratings"
    return {"pattern": "threat-arena",
            "matrix": {"arenas": arenas, "rows": rows},
            "variance_mechanism": s["logic"].get("mechanism", ""),
            "defend": arenas[0], "concede": arenas[-1],
            "inversion_signal": s.get("trigger", "")}, None


# ───────────────────────────────────────────────── P3 staged move / P5 plan ──
def numbered_nodes(s):
    """Both the staged move and the dated plan are numbered sequences in source."""
    sb = s.get("supporting_blocks") or []
    nodes, expect = [], False
    for b in sb:
        txt = re.sub(r"\s+", " ", b.get("text", "")).strip()
        lab = re.sub(r"\s+", " ", b.get("label", "")).strip()
        tags = b.get("tags") or []
        if not lab and re.fullmatch(r"[1-9]", txt) and tags:
            expect = True
            continue
        if expect and lab and len(lab) < 60:
            nodes.append({"label": lab, "text": cap(txt, 190), "tags": tags})
            expect = False
    if len(nodes) < 3:                                    # labelled blocks, unnumbered
        seen, nodes = set(), []
        for b in sb:
            lab = re.sub(r"\s+", " ", b.get("label", "")).strip()
            txt = re.sub(r"\s+", " ", b.get("text", "")).strip()
            if (lab and len(lab) < 46 and len(txt) > 40 and not is_rating(lab)
                    and not SECTION_WORDS.match(lab) and lab not in seen):
                seen.add(lab)
                nodes.append({"label": lab, "text": cap(txt, 190), "tags": b.get("tags") or []})
    return nodes[:4]


def bind_staged(s):
    nodes = numbered_nodes(s)
    if len(nodes) < 3:
        return None, "fewer than three sequenced blocks"
    stages = []
    for i, n in enumerate(nodes):
        stages.append({
            "n": i + 1,
            "label": cap(re.sub(r"^\d+\s*[·.\-]\s*", "", n["label"]), 30),
            "text": n["text"],
            "reversible": i < len(nodes) - 1,
            "commitment": ["low", "medium", "medium", "high"][min(i, 3)],
            "evidence_ids": [],
        })
    stages[-1]["label"] = cap(stages[-1]["label"], 18) + " · decision gate"
    return {"pattern": "staged-move",
            "their_mechanism": s["logic"].get("mechanism", ""),
            "stages": stages,
            "escalate_when": s.get("trigger", ""),
            "abandon_when": s.get("stop_or_escalate_rule", "")}, None


def bind_plan(s):
    nodes = numbered_nodes(s)
    if len(nodes) < 3:
        return None, "fewer than three phase blocks"
    phases = []
    for n in nodes:
        m = re.match(r"^(Weeks?\s*[\d–\-]+|Q[1-4]|Days?\s*[\d–\-]+|Month[s]?\s*[\d–\-]+)", n["label"], re.I)
        when = m.group(1) if m else cap(n["label"], 14)
        span = 2
        nums = [int(x) for x in re.findall(r"\d+", when)]
        if re.match(r"^Q", when, re.I):
            span = 13
        elif len(nums) >= 2:
            span = max(1, nums[1] - nums[0] + 1)
        elif nums:
            span = nums[0]
        parts = re.split(r"\s*[—–]\s*", n["label"], maxsplit=1)
        label = (parts[1] if len(parts) > 1 else n["label"]).strip()
        phases.append({"when": when, "span_weeks": span, "label": cap(label, 34),
                       "artifact": n["text"], "owner": s.get("owner", ""),
                       "gate": (n["tags"] or [""])[0]})
    return {"pattern": "dated-plan",
            "target_outcome": s["executive_answer"],
            "phases": phases,
            "stops_if": s.get("stop_or_escalate_rule", "")}, None


# ─────────────────────────────────────────────────────────── P6 cost bridge ──
COST_LABELS = ["FPGA module", "NRE (design)", "Yield / package", "Qualification", "ASIC module"]


def bind_bridge(s):
    sb = s.get("supporting_blocks") or []
    amounts = []
    for b in sb:
        for t in (b.get("tags") or []):
            if MONEY.match(str(t).strip()) and str(t).strip() not in amounts:
                amounts.append(str(t).strip())
        lab = str(b.get("label", "")).strip()
        if MONEY.match(lab) and lab not in amounts:
            amounts.insert(0, lab)
    amounts = [a for a in amounts if not a.startswith(("+", "-"))][:5]
    if len(amounts) < 3:
        return None, "fewer than three costed steps in the source"
    steps = []
    for i, a in enumerate(amounts):
        val = float(re.sub(r"[^\d.]", "", a) or 0)
        steps.append({"label": COST_LABELS[i] if i < len(COST_LABELS) else f"Step {i+1}",
                      "amount": a, "value": val,
                      "kind": "base" if i == 0 else ("target" if i == len(amounts) - 1 else "add"),
                      "verified": False})
    return {"pattern": "cost-bridge",
            "steps": steps,
            "comparability_rule": "A projected die price is not comparable to a system price.",
            "capital_gate": s.get("decision", "")}, None


# ──────────────────────────────────────────────────── P7 confidence register ──
BAND = {"high": (3, 3, "high"), "medium": (3, 2, "medium"), "low": (3, 1, "low-contested"),
        "verified": (3, 3, "high"), "attributed": (3, 2, "medium"), "qualified": (2, 2, "medium"),
        "insufficient": (3, 1, "low-contested")}


def bind_register(s):
    sb = s.get("supporting_blocks") or []
    claims = []
    for b in sb:
        lab = re.sub(r"\s+", " ", b.get("label", "")).strip()
        txt = re.sub(r"\s+", " ", b.get("text", "")).strip()
        tags = [str(t).lower() for t in (b.get("tags") or [])]
        key = next((k for k in BAND if k in lab.lower() or any(k in t for t in tags)), None)
        if not key or len(txt) < 20:
            continue
        imp, ev, band = BAND[key]
        claims.append({"claim": cap(txt, 120), "importance": imp, "evidence": ev,
                       "band": band, "evidence_ids": []})
    if len(claims) < 3:
        return None, "fewer than three banded claims"
    purge = [c["claim"] for c in claims if c["importance"] >= 2 and c["evidence"] == 1]
    return {"pattern": "confidence-register",
            "claims": claims[:6],
            "purge_list": purge,
            "publication_rule": s.get("stop_or_escalate_rule", "")}, None


# ───────────────────────────────────────────────────── P4 bounded argument ──
def bind_argument(s):
    taken = s.get("executive_answer", "").strip()
    opposing = s.get("counterargument", "").strip()
    bounded = (s.get("implication") or s["logic"].get("mechanism") or "").strip()
    # a few source implications carry a leading section label
    bounded = re.sub(r"^(analytical conclusion|implication|portfolio implication)[:\s·-]*",
                     "", bounded, flags=re.I).strip()
    if not (taken and opposing and bounded):
        return None, "missing one of answer / counterargument / implication"
    return {"pattern": "bounded-argument",
            "positions": [
                {"stance": "taken", "claim": taken,
                 "rests_on": cap(s["logic"].get("mechanism", ""), 90), "supported": True},
                {"stance": "opposing", "claim": opposing,
                 "rests_on": cap(s.get("falsifier", ""), 90), "supported": False},
                {"stance": "bounded", "claim": bounded,
                 "rests_on": cap(s.get("trigger", ""), 90), "supported": False}],
            "overturned_by": s.get("falsifier", "")}, None


BINDERS = {"ladder": ("P1", bind_ladder), "heatmap": ("P2", bind_heatmap),
           "chain": ("P3", bind_staged), "argument": ("P4", bind_argument),
           "rail": ("P5", bind_plan), "waterfall": ("P6", bind_bridge),
           "register": ("P7", bind_register)}
SPINE = ["slide_id", "archetype", "action_title", "analytical_question", "executive_answer",
         "counterargument", "falsifier", "implication", "decision", "owner", "trigger",
         "stop_or_escalate_rule", "source_note"]


def main():
    env = json.load(open(f"{RUN}/slide-envelopes.json"))
    mapping = json.load(open(f"{RUN}/slide-exhibit-map.json"))
    out, report = [], Counter()
    for s in env["slides"]:
        sid = str(s["slide_id"])
        want = mapping.get(sid, "argument")
        pid, fn = BINDERS[want]
        typed, why = fn(s)
        status, reason = "bound", ""
        if typed is None:
            status, reason = "fallback", why
            pid, typed = "P4", bind_argument(s)[0]
            want = "argument"
            if typed is None:
                status, reason = "blocked", "no pattern could be satisfied"
        report[f"{status}:{pid}"] += 1
        spine = {k: s.get(k) for k in SPINE}
        spine["logic"] = s.get("logic", {})
        spine["evidence_ids"] = [b.get("evidence_id") for b in s.get("evidence_blocks", [])]
        out.append({"slide_id": s["slide_id"], "pattern_id": pid, "exhibit": want,
                    "bind": {"status": status, "requested": mapping.get(sid), "reason": reason},
                    "spine": spine, "typed": typed})

    json.dump({"contract_version": "bound-1.0", "slide_count": len(out), "slides": out},
              open(f"{RUN}/bound-envelopes.json", "w"), indent=1, ensure_ascii=False)

    print(f"bound {len(out)} slides -> bound-envelopes.json")
    per = Counter(o["pattern_id"] for o in out)
    for pid in sorted(per):
        print(f"  {pid}: {per[pid]:>3}")
    print("\nbind status:")
    for k in sorted(report):
        print(f"  {k:<18} {report[k]}")
    fb = [o for o in out if o["bind"]["status"] != "bound"]
    if fb:
        print(f"\n{len(fb)} slide(s) fell back to P4 Bounded Argument:")
        for o in fb:
            print(f"  {o['slide_id']:>3} (wanted {o['bind']['requested']}): {o['bind']['reason']}")
    return 0 if not any(o["bind"]["status"] == "blocked" for o in out) else 1


if __name__ == "__main__":
    sys.exit(main())
