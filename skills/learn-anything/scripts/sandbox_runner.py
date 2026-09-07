#!/usr/bin/env python3
"""
Run a Step 5 test scaffold in an isolated Docker container.

Usage:
    python3 sandbox_runner.py --task /tmp/learn-sandbox/<slug>/step5-task.json

Reads step5-task.json, runs the scaffold in Docker, writes step5-result.json
to the same directory. Exits 0 on any completed Docker run (pass or fail);
exits 1 only if Docker itself cannot be invoked.
"""

import argparse
import json
import pathlib
import shutil
import subprocess
import sys

IMAGE_MAP = {
    "python":      "python:3.12-slim",
    "js":          "node:20-slim",
    "sql":         "python:3.12-slim",
    "claude-code": "python:3.12-slim",
    "bash":        "alpine:3.20",
}

ENTRYPOINT_MAP = {
    "python":      ["python", "/workspace/step5_scaffold.py"],
    "js":          ["node", "/workspace/step5_scaffold.js"],
    "sql":         ["python", "/workspace/step5_scaffold.py"],
    "claude-code": ["python", "/workspace/step5_scaffold.py"],
    "bash":        ["sh", "/workspace/step5_scaffold.sh"],
}

EXT_MAP = {
    "python":      ".py",
    "js":          ".js",
    "sql":         ".py",
    "claude-code": ".py",
    "bash":        ".sh",
}

TIMEOUT_SECONDS = 60


def check_docker() -> str | None:
    """Return None if Docker is available, or an error string if not."""
    if not shutil.which("docker"):
        return "docker binary not found on PATH"
    try:
        result = subprocess.run(
            ["docker", "info"],
            capture_output=True, timeout=10
        )
        if result.returncode != 0:
            return "docker daemon not running (docker info failed)"
    except subprocess.TimeoutExpired:
        return "docker info timed out — daemon may be starting"
    except Exception as e:
        return f"docker check failed: {e}"
    return None


def run(task_path: pathlib.Path) -> dict:
    task = json.loads(task_path.read_text())
    slug = task["slug"]
    tech = task.get("tech_context", "python")
    scaffold = task["scaffold"]
    sandbox_dir = task_path.parent

    # Write the scaffold file
    ext = EXT_MAP.get(tech, ".py")
    scaffold_file = sandbox_dir / f"step5_scaffold{ext}"
    scaffold_file.write_text(scaffold)

    image = IMAGE_MAP.get(tech, "python:3.12-slim")
    entrypoint = ENTRYPOINT_MAP.get(tech, ["python", f"/workspace/step5_scaffold.py"])

    docker_cmd = [
        "docker", "run", "--rm",
        "--network", "none",
        "--memory", "512m",
        "-v", f"{sandbox_dir}:/workspace",
        image,
    ] + entrypoint

    result = {
        "slug": slug,
        "tech_context": tech,
        "exit_code": None,
        "stdout": "",
        "stderr": "",
        "timed_out": False,
        "docker_error": None,
    }

    try:
        proc = subprocess.run(
            docker_cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
        )
        result["exit_code"] = proc.returncode
        result["stdout"] = proc.stdout
        result["stderr"] = proc.stderr
    except subprocess.TimeoutExpired as e:
        result["timed_out"] = True
        result["exit_code"] = -1
        result["stdout"] = (e.stdout or b"").decode(errors="replace")
        result["stderr"] = f"Killed after {TIMEOUT_SECONDS}s timeout"
    except Exception as e:
        result["docker_error"] = str(e)
        result["exit_code"] = -1

    out_path = sandbox_dir / "step5-result.json"
    out_path.write_text(json.dumps(result, indent=2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--task", required=False, help="Path to step5-task.json")
    parser.add_argument("--check", action="store_true", help="Only check Docker availability")
    args = parser.parse_args()

    docker_err = check_docker()

    if args.check:
        if docker_err:
            print(json.dumps({"available": False, "reason": docker_err}))
            sys.exit(1)
        else:
            print(json.dumps({"available": True}))
            sys.exit(0)

    if not args.task:
        print("ERROR: --task is required when not using --check", file=sys.stderr)
        sys.exit(1)

    if docker_err:
        error_result = {"docker_error": docker_err, "exit_code": -1,
                        "stdout": "", "stderr": "", "timed_out": False}
        task_path = pathlib.Path(args.task)
        (task_path.parent / "step5-result.json").write_text(json.dumps(error_result, indent=2))
        print(f"ERROR: {docker_err}", file=sys.stderr)
        sys.exit(1)

    task_path = pathlib.Path(args.task)
    if not task_path.exists():
        print(f"ERROR: task file not found: {task_path}", file=sys.stderr)
        sys.exit(1)

    result = run(task_path)
    # Print summary to stdout so SKILL.md instructions can read it directly
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
