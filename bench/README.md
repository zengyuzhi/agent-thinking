# Benchmark: does agent-thinking help?

An A/B test of the `agent-thinking` skill on a sample of [SkillsBench](https://github.com/benchflow-ai/skillsbench) tasks, run with the [BenchFlow](https://github.com/benchflow-ai/benchflow) CLI and Claude Code (`claude-agent-acp`) in local Docker.

| Arm | Skills | Instruction |
|---|---|---|
| control | none (the task's own bundled skills are stripped too) | as published |
| treatment | only `agent-thinking` | one line prepended: invoke `agent-thinking` in Apply mode |
| nudge (optional) | none | one generic line prepended: verify each requirement and show the output |

The treatment copies the skill with `disable-model-invocation` removed, because a manual-only skill is invisible to the agent. Each task's verifier scores the result, so the main metric is pass rate. Tool calls, tokens, and time are recorded as cost.

The nudge arm separates the skill from the effect of adding any instruction at all: if treatment beats control but not nudge, a one-line reminder would do. Arms run in alternating order across trials, so a slow network or API spell does not land on one arm.

## What it does not measure

Pass rate only. Two things the skill aims at, visible evidence for each method and prompts written for other agents, are not scored here. A null result does not mean the skill is useless; a drop in pass rate means it is getting in the way.

## Setup

```bash
uv tool install benchflow
git clone --depth 1 https://github.com/benchflow-ai/skillsbench.git bench/.work/skillsbench
cp .env.example .env   # fill in ANTHROPIC_API_KEY
```

Docker must be running. Use an API key from the Console organization linked to a Max or Team plan, so runs draw from the monthly API credits.

## Run

```bash
python3 bench/run.py run --tasks bench/tasks-pilot.txt --trials 1     # 3 tasks, pipeline check
python3 bench/run.py run --tasks bench/tasks-sample.txt --trials 3    # 9 tasks
python3 bench/run.py run --tasks bench/tasks-sample.txt --trials 3 --arms control,treatment,nudge
python3 bench/run.py summarize bench/results/<run-id>
```

Behind a TLS-inspecting proxy (Zscaler and the like), containers fail npm, pip, and curl. Export the proxy's root CA and pass it, and give slow verifiers more time; both changes apply to both arms equally:

```bash
security find-certificate -a -c Zscaler -p /Library/Keychains/System.keychain > bench/.work/extra-ca.crt   # macOS
python3 bench/run.py run --tasks bench/tasks-pilot.txt --extra-ca bench/.work/extra-ca.crt --verifier-timeout 900
```

Results go to `bench/results/<run-id>/` (gitignored), with `meta.json` recording the model, task list, and the commits of SkillsBench and the skill. `summarize` writes `summary.md` with per-task pass counts for both arms.

## Files

| File | Contents |
|---|---|
| `run.py` | builds both arms, runs them, and summarizes results |
| `bench_shim.py` | runs BenchFlow with a newer `claude-agent-acp`; BenchFlow 0.7.11 pins one whose Claude Code is too old for `claude-opus-5-5` |
| `tasks-pilot.txt` | 3 quick tasks to check the pipeline and cost |
| `tasks-sample.txt` | 9 tasks close to the skill's purpose, plus two non-coding contrasts; a tenth needs 16 GB of Docker memory and is commented out |
