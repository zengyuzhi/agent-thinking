#!/usr/bin/env python3
"""A/B test agent-thinking on a sample of SkillsBench tasks.

Arms:
  control    the task as published, no skills
  treatment  agent-thinking deployed, and one line prepended to the task
             instruction telling the agent to invoke it
  nudge      no skills, and one generic "verify your work" line prepended,
             to tell the skill's effect apart from the effect of any extra line

Usage:
  python3 bench/run.py run --tasks bench/tasks-pilot.txt --trials 1
  python3 bench/run.py summarize bench/results/<run-id>
"""

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BENCH = REPO / "bench"
WORK = BENCH / ".work"
SKILLSBENCH = WORK / "skillsbench"
SKILL_SRC = REPO / "skills" / "agent-thinking"
# BenchFlow's own interpreter, so bench_shim.py can import benchflow
BENCH_PYTHON = os.environ.get(
    "BENCH_PYTHON", str(Path.home() / ".local/share/uv/tools/benchflow/bin/python")
)

INVOKE_LINE = (
    "Before you start, invoke the `agent-thinking` skill and follow it in Apply mode "
    "for the task below.\n\n"
)
NUDGE_LINE = (
    "Before you finish, verify your work: check each requirement of the task below "
    "and show the output that proves it.\n\n"
)
PREPEND = {"control": "", "treatment": INVOKE_LINE, "nudge": NUDGE_LINE}


def load_env():
    env_file = REPO / ".env"
    if not env_file.exists():
        sys.exit("missing .env; copy .env.example and fill in ANTHROPIC_API_KEY")
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ.setdefault(k.strip(), v.strip())
    if not os.environ.get("ANTHROPIC_API_KEY"):
        sys.exit("ANTHROPIC_API_KEY is empty in .env")


def build_treatment_skill() -> Path:
    """Copy the skill with manual-only invocation removed, so the agent can load it."""
    root = WORK / "skills"
    dst = root / "agent-thinking"
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(SKILL_SRC, dst)
    skill_md = dst / "SKILL.md"
    text = skill_md.read_text()
    text = re.sub(r"^disable-model-invocation:.*\n", "", text, flags=re.M)
    assert "disable-model-invocation" not in text
    skill_md.write_text(text)
    return root


def prepend_instruction(task_dir: Path, line: str):
    """Insert line at the start of the instruction body."""
    instruction = task_dir / "instruction.md"
    if instruction.exists():
        instruction.write_text(line + instruction.read_text())
        return
    task_md = task_dir / "task.md"
    text = task_md.read_text()
    m = re.match(r"(---\n.*?\n---\n)(.*)", text, flags=re.S)
    if not m:
        sys.exit(f"cannot find frontmatter in {task_md}")
    task_md.write_text(m.group(1) + "\n" + line + m.group(2).lstrip("\n"))


CA_NAME = "bench-extra-ca.crt"
CA_DOCKER = f"""COPY {CA_NAME} /usr/local/share/ca-certificates/{CA_NAME}
RUN mkdir -p /etc/ssl/certs && cat /usr/local/share/ca-certificates/{CA_NAME} >> /etc/ssl/certs/ca-certificates.crt
ENV NODE_EXTRA_CA_CERTS=/usr/local/share/ca-certificates/{CA_NAME} \\
    SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt \\
    REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\
    PIP_CERT=/etc/ssl/certs/ca-certificates.crt \\
    UV_NATIVE_TLS=true
"""


def inject_ca(task_dir: Path, ca: Path):
    """Trust an extra root CA (e.g. a corporate TLS proxy) in the task image. Applied to both arms."""
    env_dir = task_dir / "environment"
    shutil.copy(ca, env_dir / CA_NAME)
    dockerfile = env_dir / "Dockerfile"
    lines = dockerfile.read_text().splitlines(keepends=True)
    out = []
    for line in lines:
        out.append(line)
        if re.match(r"\s*FROM\s", line, flags=re.I):
            out.append(CA_DOCKER)
    dockerfile.write_text("".join(out))


def set_verifier_timeout(task_dir: Path, seconds: int):
    """Raise the verifier timeout in task.md frontmatter (BenchFlow refuses to override it at run time)."""
    task_md = task_dir / "task.md"
    text = task_md.read_text()
    new, n = re.subn(r"(^verifier:\n(?:[ \t].*\n)*?[ \t]+timeout_sec:[ \t]*)[0-9.]+", rf"\g<1>{seconds}", text, count=1, flags=re.M)
    if n != 1:
        sys.exit(f"cannot find verifier.timeout_sec in {task_md}")
    task_md.write_text(new)


def build_task_dirs(tasks: list[str], arms: list[str], ca: Path | None = None, verifier_timeout: int | None = None) -> dict[str, Path]:
    src = SKILLSBENCH / "tasks"
    missing = [t for t in tasks if not (src / t).is_dir()]
    if missing:
        sys.exit(f"unknown tasks: {missing}")
    dirs = {}
    for arm in arms:
        root = WORK / f"tasks-{arm}"
        shutil.rmtree(root, ignore_errors=True)
        root.mkdir(parents=True)
        for t in tasks:
            shutil.copytree(src / t, root / t, symlinks=True)
            if ca:
                inject_ca(root / t, ca)
            if verifier_timeout:
                set_verifier_timeout(root / t, verifier_timeout)
            if PREPEND[arm]:
                prepend_instruction(root / t, PREPEND[arm])
        dirs[arm] = root
    return dirs


def cmd_run(args):
    load_env()
    if not SKILLSBENCH.is_dir():
        sys.exit(f"clone SkillsBench first: git clone https://github.com/benchflow-ai/skillsbench.git {SKILLSBENCH}")
    tasks = [l.strip() for l in Path(args.tasks).read_text().splitlines() if l.strip() and not l.startswith("#")]
    arms = args.arms.split(",")
    if not set(arms) <= PREPEND.keys():
        sys.exit(f"unknown arm in {arms}; choose from {sorted(PREPEND)}")
    skills_root = build_treatment_skill()
    ca = Path(args.extra_ca) if args.extra_ca else None
    if ca and not ca.is_file():
        sys.exit(f"extra CA not found: {ca}")
    task_dirs = build_task_dirs(tasks, arms, ca, args.verifier_timeout)
    run_id = datetime.now().strftime("%Y%m%d-%H%M%S")
    out = BENCH / "results" / run_id
    out.mkdir(parents=True)
    meta = {
        "run_id": run_id,
        "model": args.model or os.environ.get("BENCH_MODEL"),
        "tasks": tasks,
        "trials": args.trials,
        "arms": arms,
        "skillsbench_commit": subprocess.run(
            ["git", "-C", str(SKILLSBENCH), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
        ).stdout.strip(),
        "skill_commit": subprocess.run(
            ["git", "-C", str(REPO), "rev-parse", "--short", "HEAD"], capture_output=True, text=True
        ).stdout.strip(),
        "prepend": {a: PREPEND[a].strip() for a in arms},
        "extra_ca": str(ca) if ca else None,
        "verifier_timeout": args.verifier_timeout,
    }
    (out / "meta.json").write_text(json.dumps(meta, indent=2))

    for trial in range(1, args.trials + 1):
        # alternate arm order across trials so time-of-run effects (network, API load) do not favor one arm
        for arm in arms if trial % 2 else arms[::-1]:
            jobs = out / arm / f"trial-{trial}"
            cmd = [
                BENCH_PYTHON, str(BENCH / "bench_shim.py"), "eval", "run",
                "--tasks-dir", str(task_dirs[arm]),
                "--agent", "claude-agent-acp",
                "--model", meta["model"],
                "--sandbox", "docker",
                "--concurrency", str(args.concurrency),
                "--jobs-dir", str(jobs),
                "--quiet",
            ]
            if arm == "treatment":
                cmd += ["--skill-mode", "with-skill", "--skills-dir", str(skills_root)]
            print(f"[{arm} trial {trial}] {' '.join(cmd)}", flush=True)
            with open(out / f"{arm}-trial-{trial}.log", "w") as log:
                rc = subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT).returncode
            print(f"[{arm} trial {trial}] exit {rc}", flush=True)
    print(f"done: {out}")


def find_results(jobs: Path):
    """Yield (task, rollout_dir, result_dict) for each rollout under a jobs dir."""
    for f in jobs.rglob("result.json"):
        try:
            data = json.loads(f.read_text())
        except Exception:
            continue
        task = data.get("task_name") or f.parent.parent.name
        yield task, f.parent, data


def reward_of(data) -> float | None:
    r = data.get("rewards") or {}
    v = r.get("reward") if isinstance(r, dict) else None
    return float(v) if isinstance(v, (int, float)) else None


def loaded_skill(rollout: Path) -> bool:
    """BenchFlow's n_skill_invocations misses ACP 'Load skill' calls, so read the trajectory."""
    traj = rollout / "trajectory" / "acp_trajectory.jsonl"
    return traj.exists() and '"skill": "agent-thinking"' in traj.read_text()


def cmd_summarize(args):
    out = Path(args.run_dir)
    meta = json.loads((out / "meta.json").read_text())
    arms = meta.get("arms", ["control", "treatment"])
    rows = {}
    for arm in arms:
        for task, rollout, data in find_results(out / arm):
            rows.setdefault(task, {}).setdefault(arm, []).append((rollout, data))

    def stats(runs):
        scored = [(r, d) for r, d in runs if reward_of(d) is not None]
        failed = len(runs) - len(scored)  # infra failures that were retried or never scored
        fm = [d.get("final_metrics") or {} for _, d in scored]
        n = len(scored) or 1
        return {
            "pass": sum(reward_of(d) for _, d in scored),
            "n": len(scored),
            "failed": failed,
            "tools": sum(d.get("n_tool_calls") or 0 for _, d in scored) / n,
            "in_k": sum(m.get("total_prompt_tokens") or 0 for m in fm) / n / 1000,
            "out_k": sum(m.get("total_completion_tokens") or 0 for m in fm) / n / 1000,
            "secs": sum((d.get("timing") or {}).get("agent_execution") or 0 for _, d in scored) / n,
            "skill": sum(loaded_skill(r) for r, _ in scored),
        }

    lines = [
        f"# Run {meta['run_id']}",
        "",
        f"Model `{meta['model']}`, {meta['trials']} trial(s), SkillsBench `{meta['skillsbench_commit']}`, skill `{meta['skill_commit']}`.",
        "Per-arm averages are over scored rollouts; `infra` counts rollouts that failed before scoring and were retried.",
        "",
        "| Task | Arm | Pass | Tool calls | Input tokens (k) | Output tokens (k) | Agent time (s) | Skill loaded | Infra |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    totals = {arm: [] for arm in arms}
    for task in sorted(rows):
        for arm in arms:
            runs = rows[task].get(arm, [])
            if not runs:
                continue
            st = stats(runs)
            totals[arm].append(st)
            lines.append(
                f"| {task} | {arm} | {st['pass']:g}/{st['n']} | {st['tools']:.0f} | {st['in_k']:.0f} | "
                f"{st['out_k']:.1f} | {st['secs']:.0f} | {st['skill']}/{st['n']} | {st['failed']} |"
            )
    lines += ["", "| Arm | Pass rate | Avg tool calls | Avg input tokens (k) | Avg output tokens (k) | Avg agent time (s) |", "|---|---|---|---|---|---|"]
    for arm, sts in totals.items():
        n = sum(s["n"] for s in sts)
        if not n:
            continue
        w = lambda k: sum(s[k] * s["n"] for s in sts) / n
        lines.append(f"| {arm} | {sum(s['pass'] for s in sts):g}/{n} | {w('tools'):.1f} | {w('in_k'):.0f} | {w('out_k'):.1f} | {w('secs'):.0f} |")
    summary = "\n".join(lines) + "\n"
    (out / "summary.md").write_text(summary)
    print(summary)


def main():
    p = argparse.ArgumentParser()
    sub = p.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--tasks", required=True, help="file with one task name per line")
    r.add_argument("--trials", type=int, default=1)
    r.add_argument("--model", help="defaults to BENCH_MODEL in .env")
    r.add_argument("--concurrency", type=int, default=2)
    r.add_argument("--arms", default="control,treatment",
                   help="comma-separated arms to run: control, treatment, nudge")
    r.add_argument("--verifier-timeout", type=int,
                   help="override verifier timeout (s), for slow networks; applied to both arms")
    r.add_argument("--extra-ca", default=os.environ.get("BENCH_EXTRA_CA_CERT"),
                   help="PEM root CA to trust inside task images, for networks behind a TLS-inspecting proxy")
    r.set_defaults(func=cmd_run)
    s = sub.add_parser("summarize")
    s.add_argument("run_dir")
    s.set_defaults(func=cmd_summarize)
    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
