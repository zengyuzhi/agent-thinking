---
name: agent-thinking
description: Make an agent's work verifiable. Pick the few thinking methods that guard against this task's likely failures, prove "done" with evidence, or write a self-contained prompt for another agent.
argument-hint: "a task; or \"write a prompt: ...\"; or \"which methods fit?\"; or name a method, e.g. \"pre-mortem\""
disable-model-invocation: true
---

# Agent Thinking

The twelve method cards below are all you need in most cases. Each one says what to do and what evidence it leaves. Two reference files hold the long versions; read a section there only when a step below sends you to it.

- [references/methods.md](references/methods.md) holds 27 thinking methods with background and copy-paste prompts, each under a `### N. Name` heading. Each card lists the numbers it draws on.
- [references/techniques.md](references/techniques.md) holds prompting techniques by task type in sections A to G, and ends with a combined prompt for CLAUDE.md or AGENTS.md.

Reply in the language the user writes in. Prompts you produce follow the same language unless the user asks otherwise.

## 1. Pick the mode

Read the text the user attached when invoking this skill. Claude Code fills it in here: $ARGUMENTS. In other agents it is the user message that invoked the skill. With no attached text, the subject is the task currently under way in the conversation.

- **Apply**. The text describes something to do. You do it yourself, using the picked cards. See step 4.
- **Write a prompt**. The text asks for a prompt, a hand-off to another agent, or rules for CLAUDE.md or AGENTS.md. You produce the prompt only and do not run the task. See step 5.
- **Named**. The text names one or more methods. Use only those. If a name matches a card, use the card; otherwise grep methods.md for its heading and read only that section. Skip step 2.
- **Advise**. The text asks which methods or approach fit, without asking you to act. Run step 2, then step 6. Change nothing.

When the task is to dispatch other agents, you are in Apply mode as the orchestrator, and each agent's brief follows step 5.

If you cannot restate the task and the mode in one sentence, ask the user one question before going on.

## 2. Pick the cards

Answer each question for this task. Each yes makes the card a candidate.

| Question | Card |
|---|---|
| Is the request vague, or open to several readings? | Clarify |
| Are you fixing a bug or a reported failure? | Reproduce |
| Is the cause unknown, with several candidates? | Diagnose |
| Will you act on docs, notes, a past summary, or a remembered API? | Territory |
| Is the task large, with parts to split or order? | Decompose |
| Will you add new code, a feature, or a dependency? | Simplest |
| Will you delete or rewrite code, checks, or config that look unnecessary? | Fence |
| Could the change break something that works, or do tests or metrics define done? | Baseline |
| Will it ship, change an interface others use, or is failure costly? | Pre-mortem |
| Are you choosing between approaches, or should someone else check the work? | Review |
| Will the work span sessions, context compaction, or handoffs? | Task record |

Keep at most three candidates, five when you dispatch agents. Keep the ones guarding against the likeliest costly failure. Drop a card when the project's instructions or another kept card already require its action. The Ledger card always applies and does not count.

**When the task has its own runnable check** (tests, a verifier, a build) **and fits in about ten tool calls**, keep only the Ledger and say so in one line. The other cards pay off when there is no runnable check, a destructive or outward-facing step, several agents, an unknown cause, or work that spans sessions.

Before any further tool call, send the picks as a message of their own in this form, then continue without waiting:

```
Picks
- Reproduce: guards against fixing a symptom I never saw. Adds: run the failing case before editing. Evidence: command and output, before and after.
- Ledger: every acceptance criterion marked verified, failed, or unverified.
```

## 3. Cards

**Clarify** (methods 2). List your reading of the request and the terms or scope you are unsure of. Settle what you can from code, tests, and history. Ask the user only questions whose answer would change the implementation, one at a time, most important first. Evidence: the questions and answers, or the assumptions you chose and why.

**Reproduce** (1, 3). Before changing anything, reproduce the failure and record the command and the actual output. If you cannot reproduce it, stop and report. Say how you confirmed the cause is the cause and not a symptom. After the fix, rerun the same command. Evidence: the reproduction command with output before and after.

**Diagnose** (13, 14, 15). State at least two competing hypotheses. Record each round as hypothesis, prediction (what a command will show if it is true), command run, observation, verdict. Choose experiments that tell the hypotheses apart. Once the direct cause is found, keep asking why until you reach a cause whose fix prevents this class of failure; list the branches when there are several. A search that finds nothing is weak evidence, so say how likely it was to miss. Evidence: the rounds.

**Territory** (4). Before acting on docs, comments, notes, a past session's summary, or a remembered API, check it against the current code, config, or command output. Check third-party APIs against the docs for the installed version. When docs and code disagree, the code shows what happens, not what was intended: settle it with the requirements, tests, callers, and history, and list the disagreement. Evidence: each claim you relied on, with what you checked it against.

**Decompose** (5, 6). Split the task into subtasks that do not overlap and together cover it. Give each an input, an output, and a check. Mark dependencies, and order dependent subtasks easiest first. Evidence: the list, checked off as you go; in TODO.md for long work.

**Simplest** (7). Use existing code, the standard library, or an installed dependency before writing new code. Add no feature, option, or layer nobody asked for. If you think more is needed, first say where the simple version falls short. Evidence: one line per thing you deliberately did not build.

**Fence** (11). Before deleting or rewriting something that looks unnecessary, find why it exists (git log or blame, the linked issue or PR) and every place that references it, and say what would break without it. If history is missing, use tests, callers, and runtime behavior, and state what stays unknown. If the user asked for the deletion, this check shapes how you delete, not whether. If you find no reason and the deletion was not requested, list the item and let the user decide. Evidence: the history and references found for each removed item.

**Baseline** (16, 17). Before the change, run the checks that cover the affected behavior plus any the repository requires, and record the results. After the change, rerun the same commands. Nothing that passed may fail and no metric may get worse; report a trade-off instead of making it quietly. Tests verify the goal and are not the goal: do not change, skip, or delete a test, or hard-code expected values, unless you show the test is wrong and say so. Evidence: before and after results of the same commands.

**Pre-mortem** (9, 10). Assume the change failed a month after shipping. List the likeliest causes, including second-order effects on callers, data, performance, and users. For each, add a test, guard, or monitor now, or say why the risk is accepted. Evidence: each cause with its measure, pointing to the added tests.

**Review** (18, 19, 20, 21). Have a reviewer who did not do the work check it against the original requirement and the final output only. It must try to prove the work wrong with counterexample inputs, code locations, or reproduction steps, and report only issues that affect correctness or the requirements. With no second agent, do it yourself as a separate pass: build at least one input meant to break the change, and run it. When choosing between approaches, first write the strongest case for each. When several agents judge the same thing, each answers before seeing the others; settle disagreements with a check that tells them apart, not a vote. Evidence: the findings with their evidence, or what was checked and found clean.

**Task record** (1; techniques E). Keep one record of the goal, acceptance criteria, the latest user decisions, assumptions that changed, the status of each criterion, blockers, and the next step. Reuse an existing task, plan, or progress file; create one only when the task already changes files. Update it at handoffs, before compaction, and when scope changes. When resuming, reread it and reconcile it with the current files before going on, and confirm at each phase that you are still solving the original problem. Evidence: the record, current at the end.

**Ledger** (22, 23, 25, 26; always). List the acceptance criteria from the request, the task, and the repository's rules. Mark each one verified, failed, or unverified, with the command, source, or file that shows it. A check counts only if it ran after the last edit that could affect it. In claims, keep what you observed apart from what you inferred. Say "done" only when every required criterion is verified; otherwise say what is left. End with the uncertainties: untested scenarios, assumptions, and information that may be outdated, each with what it would change. One result can back several criteria; point to it instead of repeating it.

## 4. Apply mode

Do the task, following the picked cards, and finish with the Ledger.

For explaining, diagrams, research, or long tasks, also read the matching techniques.md section (B, D, F, or E), found by its `## ` heading.

When you dispatch agents, give each one only the cards that fit its part, written as concrete rules, plus the files and interfaces it owns, what it must not touch, its checks, and the evidence its report must carry. You own the integration: rerun at least one check from each report yourself and test the combined result. A worker's "done" is a claim, not evidence. If you cannot dispatch, do the parts yourself in order.

## 5. Write-a-prompt mode

Produce one self-contained prompt with these parts, in order.

1. Goal and background, including the context the recipient does not have.
2. Scope: what to do, what not to do, and the files or systems it owns.
3. Acceptance criteria the recipient can check on its own.
4. The picked cards, written as rules with this task's details filled in.
5. The budget: when to stop and report instead of pressing on.
6. The report format: the Ledger, so each criterion comes back verified, failed, or unverified with its evidence, ending with the uncertainties.

When the target is CLAUDE.md or AGENTS.md, start from the combined prompt at the end of techniques.md and keep only the lines that fit this project.

Then run the colleague test: read the prompt as a colleague who knows nothing about the task. It passes only if they could start work right away. Deliver the prompt in one code block, followed by one line per card used and why.

## 6. Advise mode

For each picked card, give three lines: the failure it guards against here, the first concrete action, and the evidence it would leave. Then one line on cards you considered and rejected, and why. End by asking whether to go ahead in Apply mode.

## 7. Wrap up

End with one line naming the cards used.
