# agent-thinking

English | [中文](README.zh-CN.md)

An Agent Skill for Claude Code, Codex, pi, and other agents that support `SKILL.md`. It picks the right few of 27 thinking methods for the task at hand and applies them, or writes a prompt for another agent.

The methods include First Principles, Socratic Questioning, Pre-Mortem, Chesterton's Fence, scientific debugging, Adversarial Review, Chain-of-Verification, and Ablation Study. A second reference collects prompting techniques by task type: explaining, writing code, architecture diagrams, long tasks, research, and output format.

## Install

Install with the [skills CLI](https://github.com/vercel-labs/skills). `-g` installs to your user directory for all projects; drop it to install into the current project only. List the agents you use after `-a`.

```bash
npx skills add zengyuzhi/agent-thinking -g -a claude-code codex pi
```

Claude Code reads skills from `.claude/skills/`; Codex and pi share `.agents/skills/`. You can also clone by hand.

```bash
git clone https://github.com/zengyuzhi/agent-thinking.git ~/.claude/skills/agent-thinking   # Claude Code
git clone https://github.com/zengyuzhi/agent-thinking.git ~/.agents/skills/agent-thinking   # Codex, pi
```

Start a new session after installing.

## Usage

The skill is manual-only: the model never loads it on its own, so it costs no context until you call it.

| Agent | Invoke | What turns off automatic invocation |
|---|---|---|
| Claude Code | `/agent-thinking <task>` | `disable-model-invocation: true` in `SKILL.md` |
| pi | `/skill:agent-thinking <task>` | same field; pi honors it too |
| Codex | `$agent-thinking <task>` | `allow_implicit_invocation: false` in `agents/openai.yaml` |

Agents that ignore both fields can still use the skill, but may load it automatically.

```
/agent-thinking fix the bug where users can't log back in after a session timeout
/agent-thinking write a prompt: have a subagent review this payment change
/agent-thinking pre-mortem
/agent-thinking which methods fit the current situation?
```

| Mode | Triggered by | What it does |
|---|---|---|
| Apply | a task description, or nothing | picks up to five methods by task stage, does the task, and leaves evidence for each method in the conversation |
| Write a prompt | asking for a prompt, a hand-off to an agent, or rules for CLAUDE.md or AGENTS.md | produces one self-contained prompt and does not run the task |
| Named | naming a method | uses only the named methods |
| Advise | asking which methods fit, e.g. "which approach is best here?" | recommends methods with reasons and first steps, changes nothing, then asks whether to go ahead |

The agent replies in the language you write in.

## Files

| File | Contents |
|---|---|
| [SKILL.md](SKILL.md) | the steps, and the stage-to-method picker |
| [references/methods.md](references/methods.md) | 27 thinking methods, each with a copy-paste prompt |
| [references/techniques.md](references/techniques.md) | prompting techniques by task type, and a combined prompt for CLAUDE.md or AGENTS.md |
| [agents/openai.yaml](agents/openai.yaml) | Codex UI metadata and invocation policy |

Both reference files read fine on their own, outside the skill. Each lists its sources at the end.
