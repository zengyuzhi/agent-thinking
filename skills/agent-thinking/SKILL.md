---
name: agent-thinking
description: Pick the right thinking methods for the current task and apply them, or write a high-quality prompt for another agent.
argument-hint: "a task; or \"write a prompt: ...\"; or \"which methods fit?\"; or name a method, e.g. \"pre-mortem\""
disable-model-invocation: true
---

# Agent Thinking

The method library lives in two files. Read only the parts you pick; never load a whole file.

- [references/methods.md](references/methods.md) holds 27 thinking methods, each under a `### N. Name` heading with a copy-paste prompt.
- [references/techniques.md](references/techniques.md) holds prompting techniques by task type in sections A to G, and ends with a combined prompt for CLAUDE.md or AGENTS.md.

Reply in the language the user writes in. Prompts you produce follow the same language unless the user asks otherwise.

## 1. Pick the mode

Read the text the user attached when invoking this skill. Claude Code fills it in here: $ARGUMENTS. In other agents it is the user message that invoked the skill. With no attached text, the subject is the task currently under way in the conversation.

- **Apply**. The text describes something to do. You do it yourself, using the picked methods.
- **Write a prompt**. The text asks for a prompt, a hand-off to another agent or subagent, or rules for CLAUDE.md or AGENTS.md. You produce the prompt only and do not run the task.
- **Named**. The text names one or more methods. Use only those and skip step 2.
- **Advise**. The text asks which methods or approach fit the situation, without asking you to act. Run steps 2 and 3, then 4c. Change nothing.

When the task is to dispatch other agents to do the work, you are in Apply mode as the orchestrator, and each agent's brief follows the Write-a-prompt rules in 4b.

Done when you can restate the task and the mode in one sentence. If you cannot, ask the user one question before going on.

## 2. Pick methods by stage

Decide which stages below the task actually passes through. From each relevant stage pick one or two methods, five at most in total. Each method lists the situation it fits: match on the situation, prefer methods whose situation fits the task, and rank general methods that fit everything last. Then pick the techniques.md sections that fit the task type.

**Understand the problem** (techniques.md A, C.5)
- 1 First Principles: fixing a bug, or confirming the goal before a long task
- 2 Socratic Questioning: the request is vague or reads several ways
- 3 Step-Back Prompting: a general principle sits behind the specific question
- 4 The Map Is Not the Territory: relying on docs, comments, old notes, or remembered APIs

**Break down the task** (E.3)
- 5 Divide and Conquer (MECE): a large task with several independent parts
- 6 Least-to-Most Decomposition: subproblems depend on each other in order

**Design the approach** (C.3, D)
- 7 Occam's Razor: writing new code or a new feature
- 8 High Cohesion, Low Coupling: the change crosses modules, or adds a module
- 9 Inversion and Pre-Mortem: the plan will ship, or failure is costly
- 10 Second-Order Thinking: changing an interface, metric, or process others depend on
- 21 Steelmanning: choosing between several approaches

**Make changes** (C.4, C.9)
- 11 Chesterton's Fence: deleting code, checks, or config that look unnecessary
- 12 One-Way and Two-Way Doors: deleting, pushing, sending anything outside, changing permissions

**Debug** (C.1)
- 13 The Scientific Method: the cause is unknown and there are several candidates
- 14 Five Whys: the direct cause is known and the root cause is not
- 15 Bayesian Updating: evidence is scattered and you must judge which cause is likelier

**Verify** (C.2, C.6)
- 16 Pareto Improvement: the change may break something that works today
- 17 Goodhart's Law: tests or metrics define "done"
- 24 Rubber Duck Debugging: you just wrote a change and should check it yourself

**Review** (F.2)
- 18 Adversarial Review: a change about to ship needs an independent check
- 19 Independent Judgment: several agents judge the same thing
- 20 Self-Consistency: the judgment must be highly reliable and can be solved several times
- 22 Critical Thinking: an analysis or report contains inferences
- 23 Chain-of-Verification: the output contains many checkable facts

**Deliver** (G)
- 25 List Every Uncertainty: any delivery
- 26 Checklists: the deliverable has several completion criteria

**Tune prompts and config** (E.9)
- 27 Ablation Study: rules, tools, or prompts keep piling up and nobody knows which ones help

Add B for explaining or teaching, E for long tasks, F for research.

Done when the user can see, in a message before any work starts, the picked method numbers and techniques.md sections, each with one sentence on why. Then continue without waiting; the user may redirect.

## 3. Read the picked entries

Grep for each picked method's `### N.` heading and read only that section. Read only the picked sections of techniques.md too. In Named mode, find the heading by method name.

## 4a. Apply mode

Do the task. Every picked method leaves **evidence** in the conversation that the user can inspect.

| Method | Evidence |
|---|---|
| First Principles | reproduction command and output, before-and-after comparison |
| Pre-Mortem | list of failure causes, each with a preventive measure |
| Chesterton's Fence | what git log or blame showed, and where the code is referenced |
| The Scientific Method | hypothesis, prediction, experiment, and observation for each round |
| Pareto Improvement | test baseline before and after the change |
| List Every Uncertainty | the uncertainty list at the end |

For methods not in the table, derive the evidence from that method's prompt in methods.md.

When you dispatch agents, write each picked method into their briefs as a concrete rule, and require each agent's report to carry that method's evidence. Your final message then points to where each method's evidence lives: a file, a report section, or this conversation.

Done when every picked method has evidence, or a stated reason why it could not.

## 4b. Write-a-prompt mode

Produce one self-contained prompt with these parts, in order.

1. Goal and background, including the context the recipient does not have.
2. Scope: what to do and what not to do.
3. A check the recipient can run on its own, or a clear completion criterion.
4. The picked methods' prompts, merged and de-duplicated, with placeholders filled in for this task.
5. The delivery format, ending with an uncertainty list.

When the target is CLAUDE.md or AGENTS.md, start from the combined prompt at the end of techniques.md and keep only the lines that fit this project.

Then run the colleague test: read the prompt as a colleague who knows nothing about the task. It passes only if they could start work right away. Deliver the prompt in one code block, followed by one line per method used and why.

## 4c. Advise mode

For each picked method, give three lines: why it fits this situation, the first concrete action it would mean here, and the evidence it would leave. Then one line on methods you considered and rejected, and why. End by asking whether to go ahead in Apply mode.

## 5. Wrap up

End with one line listing the method numbers used.
