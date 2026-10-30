#!/usr/bin/env python3
"""Wait for GitHub Pages workflow runs on several repos, then report every job.

Stdlib only; shells out to the `gh` CLI. Read-only: never cancels or reruns.

Exit codes: 0 all runs succeeded, 1 a run or job failed, 2 timed out, 3 no run found / gh error.
"""
import argparse
import json
import os
import subprocess
import sys
import time

DEFAULT_REPOS = "shekerkamma/deepgrid-dr-silicon-v11,shekerkamma/deepgrid-dr-silicon-v12"
WORKFLOW = "Build and deploy GitHub Pages"


def gh(*args):
    out = subprocess.run(["gh", *args], capture_output=True, text=True)
    if out.returncode != 0:
        raise RuntimeError(f"gh {' '.join(args)}: {out.stderr.strip()}")
    return json.loads(out.stdout) if out.stdout.strip() else None


def find_run(repo, sha, run_id, branch):
    if run_id:
        return int(run_id)
    args = ["run", "list", "-R", repo, "-w", WORKFLOW, "-L", "1", "--json", "databaseId,headSha"]
    if sha:
        args += ["--commit", sha]
    else:
        args += ["--branch", branch, "--event", "push"]
    runs = gh(*args)
    return runs[0]["databaseId"] if runs else None


def main():
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--repos", default=os.environ.get("PAGES_WATCH_REPOS", DEFAULT_REPOS),
                   help="comma-separated owner/name list")
    p.add_argument("--sha", help="commit SHA (full or short) whose runs to watch")
    p.add_argument("--run", action="append", default=[],
                   help="explicit run id, one per repo in --repos order")
    p.add_argument("--branch", default="main", help="branch for the latest push run when no --sha/--run")
    p.add_argument("--timeout", type=float, default=95, help="minutes to wait (Pages runs take ~70 min)")
    p.add_argument("--poll", type=int, default=60, help="seconds between checks")
    a = p.parse_args()

    repos = [r.strip() for r in a.repos.split(",") if r.strip()]
    runs = {}
    try:
        for i, repo in enumerate(repos):
            rid = find_run(repo, a.sha, a.run[i] if i < len(a.run) else None, a.branch)
            if rid is None:
                print(f"{repo}: no '{WORKFLOW}' run found for {a.sha or a.branch}")
                return 3
            runs[repo] = rid
            print(f"watching {repo} run {rid}", flush=True)
    except RuntimeError as e:
        print(e)
        return 3

    deadline = time.time() + a.timeout * 60
    done = {}
    while True:
        for repo, rid in runs.items():
            if repo in done:
                continue
            try:
                v = gh("run", "view", str(rid), "-R", repo,
                       "--json", "status,conclusion,headSha,url,jobs")
            except RuntimeError as e:
                print(e, flush=True)
                continue
            if v["status"] == "completed":
                done[repo] = v
                print(f"{repo} run {rid} finished: {v['conclusion']}", flush=True)
        if len(done) == len(runs) or time.time() > deadline:
            break
        time.sleep(a.poll)

    ok = True
    print("\n| repo | run | commit | job | result |\n|---|---|---|---|---|")
    for repo, rid in runs.items():
        v = done.get(repo)
        if not v:
            ok = False
            print(f"| {repo} | {rid} | – | (whole run) | still running at timeout |")
            continue
        for j in v["jobs"]:
            res = j["conclusion"] or j["status"]
            ok &= res in ("success", "skipped")
            print(f"| {repo} | {rid} | {v['headSha'][:7]} | {j['name']} | {res} |")
        ok &= v["conclusion"] == "success"
    if len(done) < len(runs):
        return 2
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
