#!/usr/bin/env python3
"""Validate and rank baseline versus Impeccable visual-asset treatments."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

DIMENSIONS = (
    "asset_prominence", "crop_and_focus", "context_binding", "hierarchy",
    "legibility", "visual_distinctiveness", "source_fidelity",
    "cross_slide_coherence", "editability", "asset_authenticity",
)
GUARDRAILS = ("source_fidelity", "legibility", "asset_authenticity")


def validate(data: dict) -> None:
    treatments = data.get("treatments")
    if not isinstance(treatments, list) or len(treatments) < 2:
        raise ValueError("treatments must contain baseline and at least one alternative")
    names = {item.get("name") for item in treatments}
    if "baseline" not in names:
        raise ValueError("one treatment must be named baseline")
    for treatment in treatments:
        scores = treatment.get("scores", {})
        for dimension in DIMENSIONS:
            record = scores.get(dimension)
            if not isinstance(record, dict):
                raise ValueError(f"{treatment.get('name')}.{dimension} is missing")
            score = record.get("score")
            if not isinstance(score, (int, float)) or not 1 <= score <= 5:
                raise ValueError(f"{treatment.get('name')}.{dimension}.score must be 1..5")
            if not record.get("reason") or not isinstance(record.get("slides"), list):
                raise ValueError(f"{treatment.get('name')}.{dimension} needs reason and slides")


def rank(data: dict) -> dict:
    validate(data)
    weights = {dimension: 1.0 for dimension in DIMENSIONS}
    weights.update(data.get("weights", {}))
    baseline = next(item for item in data["treatments"] if item["name"] == "baseline")
    baseline_scores = {d: baseline["scores"][d]["score"] for d in DIMENSIONS}
    results = []
    for treatment in data["treatments"]:
        total = sum(treatment["scores"][d]["score"] * weights[d] for d in DIMENSIONS)
        eligible = treatment["name"] == "baseline" or all(
            treatment["scores"][d]["score"] >= baseline_scores[d] for d in GUARDRAILS
        )
        results.append({"name": treatment["name"], "weighted_total": round(total, 3), "eligible": eligible})
    eligible = [item for item in results if item["eligible"]]
    winner = max(eligible, key=lambda item: item["weighted_total"])
    return {**data, "dimensions": list(DIMENSIONS), "guardrails": list(GUARDRAILS), "results": results, "winner": winner["name"]}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = rank(data)
    Path(args.out).write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(f"winner: {result['winner']}")


if __name__ == "__main__":
    main()
