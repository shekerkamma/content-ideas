#!/usr/bin/env python3
"""Keep a running log of what every paid generation cost, against a budget.

Paid models add up fast, and a quoted price is not always the charged price. Log each job when
you submit it, then correct it with what the account was really charged.

  credit_log.py start --budget 800                       set the budget (once per project)
  credit_log.py add --model kling4_0 --what "shot 4, take 1" --quoted 18.75 --job 1a2b3c4d
  credit_log.py add --model nano_banana_pro --what "keyframe 3" --quoted 4 --charged 0 --verdict "refused, refunded"
  credit_log.py set 12 --charged 150 --verdict "kept"    correct row 12 after checking the account
  credit_log.py total                                    spent, left, and a warning near the limit
  credit_log.py can-spend 150                            exit code 1 if this would go over budget

The log is a JSON file (credits.json) plus a readable table (credits.md) written next to it.
Run can-spend before any job that costs more than a few credits, and stop if it says no.

Needs: nothing but Python.
"""
import argparse
import datetime
import json
import os
import sys


def load(path):
    if os.path.exists(path):
        return json.load(open(path))
    return {"budget": None, "jobs": []}


def cost(job):
    return job["charged"] if job.get("charged") is not None else job.get("quoted", 0.0)


def save(path, log):
    json.dump(log, open(path, "w"), indent=1)
    spent = sum(cost(j) for j in log["jobs"])
    lines = ["# Credit log", ""]
    if log["budget"] is not None:
        lines.append(f"Budget: {log['budget']:g} credits. Spent: {spent:g}. Left: {log['budget'] - spent:g}.")
    else:
        lines.append(f"Spent: {spent:g} credits. No budget set.")
    lines += ["", "| # | Time | Model | What | Quoted | Charged | Running total | Job | Verdict |", "|---|---|---|---|---|---|---|---|---|"]
    running = 0.0
    for i, j in enumerate(log["jobs"], 1):
        running += cost(j)
        charged = "" if j.get("charged") is None else f"{j['charged']:g}"
        lines.append(f"| {i} | {j['time']} | `{j['model']}` | {j['what']} | {j.get('quoted', 0):g} | {charged} | {running:g} | {j.get('job', '')} | {j.get('verdict', '')} |")
    open(os.path.splitext(path)[0] + ".md", "w").write("\n".join(lines) + "\n")
    return spent


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--log", default="credits.json", help="the log file (default credits.json in the current folder)")
    sub = p.add_subparsers(dest="command", required=True)
    s = sub.add_parser("start", help="set the budget")
    s.add_argument("--budget", type=float, required=True)
    s = sub.add_parser("add", help="log one job")
    s.add_argument("--model", required=True)
    s.add_argument("--what", required=True, help="what the job was for")
    s.add_argument("--quoted", type=float, default=0.0, help="the price quoted before it ran")
    s.add_argument("--charged", type=float, help="the price really charged (0 if refunded)")
    s.add_argument("--job", default="", help="the job id")
    s.add_argument("--verdict", default="", help="kept, rejected and why, refunded...")
    s = sub.add_parser("set", help="correct a row")
    s.add_argument("row", type=int)
    s.add_argument("--charged", type=float)
    s.add_argument("--verdict")
    sub.add_parser("total", help="show spent and left")
    s = sub.add_parser("can-spend", help="check a price against what is left")
    s.add_argument("amount", type=float)
    a = p.parse_args()

    log = load(a.log)
    if a.command == "start":
        log["budget"] = a.budget
        save(a.log, log)
        print(f"Budget set to {a.budget:g} credits.")
        return
    if a.command == "add":
        log["jobs"].append({"time": datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), "model": a.model, "what": a.what,
                            "quoted": a.quoted, "charged": a.charged, "job": a.job, "verdict": a.verdict})
    elif a.command == "set":
        if not 1 <= a.row <= len(log["jobs"]):
            sys.exit(f"There is no row {a.row}.")
        if a.charged is not None:
            log["jobs"][a.row - 1]["charged"] = a.charged
        if a.verdict is not None:
            log["jobs"][a.row - 1]["verdict"] = a.verdict
    spent = save(a.log, log)
    budget = log["budget"]
    if a.command == "can-spend":
        if budget is None:
            sys.exit("No budget set. Run: credit_log.py start --budget N")
        left = budget - spent
        if a.amount > left:
            print(f"NO. {a.amount:g} credits would go over budget: {left:g} left of {budget:g}. Stop and ask.")
            sys.exit(1)
        print(f"Yes. {a.amount:g} fits: {left:g} left of {budget:g}.")
        return
    line = f"Spent {spent:g} credits over {len(log['jobs'])} jobs."
    if budget is not None:
        line += f" {budget - spent:g} left of {budget:g}."
        if spent > budget:
            line += " OVER BUDGET: stop and ask."
        elif spent > 0.8 * budget:
            line += " More than 80% used: say so before the next paid job."
    print(line)


if __name__ == "__main__":
    main()
