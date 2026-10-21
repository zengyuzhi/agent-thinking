# Thinking Methods (27)

| # | Method | In one line | Best for |
|---|---|---|---|
| **I. Understand the Problem** | | | |
| 1 | First Principles | Understand the problem itself first | Fixing bugs, before long tasks |
| 2 | Socratic Questioning | Ask until it is clear, then act | Vague requirements |
| 3 | Step-Back Prompting (paper) | Ask about the underlying principle first, then solve the specific problem | Complex reasoning |
| 4 | The Map Is Not the Territory | Docs and memory may be outdated; the current code is the truth | Reading docs, taking over a project |
| 5 | Divide and Conquer (MECE) | Split into parts with no overlaps and no gaps | Large tasks, research |
| 6 | Least-to-Most Decomposition (paper) | Solve the easiest subproblem first, then work upward | Tasks with sequential dependencies |
| **II. Design the Approach** | | | |
| 7 | Occam's Razor | Build the simplest version that works first | All implementation |
| 8 | High Cohesion, Low Coupling | Draw clear module boundaries | Changing code, splitting modules |
| 9 | Inversion and Pre-Mortem | Assume it already failed, and ask why | Designing solutions, before launch |
| 10 | Second-Order Thinking | And then what? | Changing interfaces, metrics, processes |
| 11 | Chesterton's Fence | Before you remove it, find out why it is there | Deleting code, deleting rules |
| 12 | One-Way and Two-Way Doors | Make reversible decisions fast and irreversible ones slowly | Deciding when to ask a human |
| **III. Debug and Find Root Causes** | | | |
| 13 | The Scientific Method | Hypothesis, prediction, experiment, observation | Debugging |
| 14 | Five Whys | Keep asking why until you reach the root cause | Incident reviews |
| 15 | Bayesian Updating | Judge with a confidence level and adjust it with evidence | Diagnosis, research |
| **IV. Verify and Review** | | | |
| 16 | Pareto Improvement | Make one thing better without breaking anything else | Acceptance criteria |
| 17 | Goodhart's Law | When a measure becomes a target, it stops being a good measure | Writing tests, setting acceptance criteria |
| 18 | Adversarial Review | Get an agent whose only job is to find faults | Review |
| 19 | Independent Judgment | Judge first, then look at other answers | Multi-agent work |
| 20 | Self-Consistency (paper) | Solve independently several times and check whether the answers agree | Judgments that must be highly reliable |
| 21 | Steelmanning | Before you argue against a view, state it in its strongest form | Choosing between solutions |
| 22 | Critical Thinking | Always check the evidence | All analysis |
| 23 | Chain-of-Verification (paper) | Write a draft first, then check each claim independently | Reducing factual errors |
| 24 | Rubber Duck Debugging | Explain it line by line, and the problem shows itself | Self-checking code |
| **V. Deliver and Improve** | | | |
| 25 | List Every Uncertainty | Give uncertainty a place to show up | At delivery |
| 26 | Checklists | Write down what "done" means and check each item | Before delivery |
| 27 | Ablation Study | Remove one thing and see if it still works | Tuning prompts and configuration |

The four methods marked "paper" come from LLM research papers. Most of these papers tested models from 2022 to 2023. Many current models have built-in deep reasoning, so the gains from these techniques may be smaller now. Before you rely on one, compare it on your own task first. See method 27 for how.

---

## I. Understand the Problem

### 1. First Principles

> Understand the problem itself first

**What it is**

Go back to the most basic facts and reason step by step from those facts to a conclusion. Put experience, analogies and other people's conclusions aside for now.

**Why it matters for agents**

Agents easily start fixing right away without confirming that the problem really exists. Long tasks have another risk: after tens or hundreds of turns, the agent forgets what it was originally asked to do and starts solving a problem that has drifted.

**How**

- Reproduce the problem before fixing it. Record the reproduction steps and the actual result.
- Find the root cause before you change anything. A change that only removes the symptom does not count as a fix.
- After the fix, run the same steps again and compare the results before and after.
- At the start of a long task, write the goal into a file such as `TASK.md`, and have the agent reread it before each phase.

**Prompt**
```
Before you change anything, go back to the facts:
1. Reproduce the problem. Give the reproduction steps and the actual output. If you cannot reproduce it, stop and tell me.
2. Find the root cause, and explain how you confirmed it is the root cause.
3. After the fix, run the same steps again and show the results before and after the fix.
After each phase, reread TASK.md and confirm you are still solving the original problem.
```

---

### 2. Socratic Questioning

> Ask until it is clear, then act

**What it is**

The questioner does not give the answer directly. Instead, a series of follow-up questions clarifies concepts, checks assumptions and exposes contradictions. See [Appendix A](#appendix-a-socratic-questioning) for the full introduction.

**Why it matters for agents**

User requirements are often vague. By default, an agent fills in its own interpretation and executes it, and only at the end finds out the direction was wrong. Having the agent ask questions first, or question its own understanding first, catches misunderstandings before work starts.

**Two ways to use it**

- **Ask the user**. When the requirement is unclear, list the key questions first and start only after they are answered.
- **Ask yourself**. Before giving a conclusion, ask yourself what the premise of the claim is, whether there are counterexamples, and what follows if it is true.

**Prompt**
```
Before you start, clarify the task with questions:
1. List your understanding of this requirement, and the words or scope you are unsure about.
2. Ask only the questions that would change how you implement it, one at a time, ordered by importance.
3. Before giving your final conclusion, ask yourself three questions: What is the premise? Are there counterexamples? If it is true, what consequences follow?
```

---

### 3. Step-Back Prompting

> Ask about the underlying principle first, then solve the specific problem

**What it is**

A 2023 paper from Google DeepMind, published at ICLR 2024, called Step-Back Prompting. First have the model step back and state the general principle or concept behind the problem, then use that principle to derive the answer. The paper tested it on PaLM-2L and reported gains of 7% on physics questions and 11% on chemistry questions.

**Why it matters for agents**

This is one concrete way to apply first principles. For a specific bug, first ask what mechanism usually causes this kind of problem. For a specific design, first ask what the main constraints of this kind of system are.

**Prompt**
```
Before you answer this question, take a step back:
1. What general principles or concepts does this question involve?
2. Use those principles to derive the answer.
3. Check that the answer is consistent with the principles.
```

---

### 4. The Map Is Not the Territory

> Docs and memory may be outdated; the current code is the truth

**What it is**

A map is a simplified description of reality. Reality changes, and maps go out of date.

**Why it matters for agents**

Agents trust the README, comments, old notes, the summary from the last session, and even the API usage in their training data. Any of these may already be outdated. Be especially careful in long tasks and multi-session work: the state recorded last time may not match the state now.

**Prompt**
```
Docs, comments, notes and your memory may all be outdated. Before you base a decision on any of them, confirm it once against the current code, configuration or command output.
If the docs and the code disagree, the code shows what happens, not what was intended. Settle it with the requirements, tests, callers and history, and list the places where they disagree.
When you use a third-party library's API, check the official docs for the current version. Do not rely on memory.
```

---

### 5. Divide and Conquer (MECE)

> Split into parts with no overlaps and no gaps

**What it is**

Split a large problem into small problems and solve them one by one. MECE is McKinsey's splitting principle. It stands for Mutually Exclusive, Collectively Exhaustive: the parts do not overlap, and together they leave nothing out.

**Why it matters for agents**

Give an agent one big task at once and it tends to miss some parts or jump back and forth between them. Once the task is split into subtasks with no overlaps and no gaps, each piece can be verified on its own, and the pieces are easy to hand to several subagents in parallel.

**Prompt**
```
Before you start, split the task into subtasks:
- Subtasks do not overlap, and together they cover the whole task.
- For each subtask, state: the input, the output, and how to verify it is done.
- Mark the dependencies between subtasks and which ones can run in parallel.
Write the list into TODO.md and check off each item as you finish it.
```

---

### 6. Least-to-Most Decomposition

> Solve the easiest subproblem first, then work upward

**What it is**

A 2022 paper from Google, published at ICLR 2023, called Least-to-Most Prompting. Break a complex problem into a sequence of subproblems and start with the easiest. Each time one is solved, use its answer as input to the next subproblem.

**Why it matters for agents**

It is close to method 5, with one extra requirement about order: solve the simplest, most certain part first, then use its result to solve the next. It fits tasks with sequential dependencies.

**Prompt**
```
Break this problem into a sequence of subproblems, ordered from simple to complex. Later subproblems can use the answers to earlier ones.
Solve them one at a time. After each one, write down the answer, then move to the next.
```

---

## II. Design the Approach

### 7. Occam's Razor

> Build the simplest version that works first

**What it is**

Do not add entities beyond necessity. When several solutions all solve the problem, pick the simplest one.

**Why it matters for agents**

Agents love to over-engineer: adding abstraction layers, adding config options, writing code for scenarios that might come up later. That code raises review and maintenance costs and can introduce new bugs. If a script can do the job, get the script working first, and let the architecture evolve with real needs.

**Prompt**
```
First build the simplest version that solves the problem:
- If existing code, the standard library or an installed dependency can do it, do not write something new.
- Do not add features, config options or abstraction layers nobody asked for.
- If you think a more complex solution is needed, first explain where the simple one falls short, then give the complex one.
- At the end, list the things you deliberately did not do, one per line.
```

---

### 8. High Cohesion, Low Coupling

> Draw clear module boundaries

**What it is**

Keeping related logic together is high cohesion. Having modules work together through clear interfaces, with as few dependencies on each other as possible, is low coupling.

**Why it matters for agents**

An agent's context window is limited. The clearer the module boundaries, the less it has to understand to change one module, the easier it is to give it the right context, and the easier the change is to verify. With blurry boundaries, the agent either cannot see everything or breaks a whole area when it changes one spot.

**Prompt**
```
Respect module boundaries when you change code:
- Keep related logic in the same module. Do not scatter one feature across many places.
- Modules interact only through public interfaces. Do not reach into another module's internals.
- If this change has to cross several modules, explain why first, and assess whether that means the boundaries are drawn wrong.
- List every caller affected by this change.
```

---

### 9. Inversion and Pre-Mortem

> Assume it already failed, and ask why

**What it is**

Inversion first asks what would guarantee failure, then tries to avoid those things. A pre-mortem is one concrete way to do it: imagine the project has already failed and work backward to the causes. A commonly cited case is Wald in World War II. He recommended adding armor to the parts of returning planes that had no bullet holes, because the planes hit in those parts did not make it back.

**Why it matters for agents**

Agents tend to think along the line of "this will work" and rarely think about failure paths on their own. Inverted questions force them to list risks, then turn each risk into a test, a constraint or an explicitly accepted risk.

**Prompt**
```
Assume this solution failed completely one month after launch.
1. List the 5 most likely causes of the failure, ordered by likelihood.
2. For each cause, give a preventive measure you can take now: a test, a constraint, or a monitor.
3. Which risks do you think are acceptable? Explain why.
```

---

### 10. Second-Order Thinking

> And then what?

**What it is**

Look at the direct result of a decision, and also at the results that result causes. A commonly cited counterexample is the 1902 rat bounty in Hanoi. Officials paid a bounty per rat tail. Some people cut off the tails and released the rats to keep breeding, and later some people started farming rats.

**Why it matters for agents**

When agents change code, they usually only care whether the immediate problem is solved. They rarely think about the later effects of the change on callers, performance, data and user habits.

**Prompt**
```
Do a second-order analysis of this change:
- First order: what problem does it directly solve?
- Second order: what callers, data, performance or user behavior will it change?
- Third order: what will those changes lead to in turn?
List only effects you have grounds for, and mark the speculative ones.
```

---

### 11. Chesterton's Fence

> Before you remove it, find out why it is there

**What it is**

There is a fence across a road and you do not know what it is for. First find out why it was built. Only after you know that do you have the right to decide whether to remove it.

**Why it matters for agents**

Agents love to delete code that looks useless, checks that look redundant and config that looks odd. These things were often added to fix some past bug or handle some rare case.

**Prompt**
```
Before you delete or rewrite any code or config that looks redundant or odd:
1. Use git log / git blame to find when and why it was added, and whether there is a related issue or PR.
2. Search for every place that references it.
3. Explain in which situations things would break if you deleted it.
If the history is missing, use tests, callers and runtime behavior instead, and say what stays unknown.
If I asked for the deletion, use this to decide how to delete safely, not whether. Otherwise, if you cannot find a reason for it to exist, do not delete it. List it and let me decide.
```

---

### 12. One-Way and Two-Way Doors

> Make reversible decisions fast and irreversible ones slowly

**What it is**

This is Bezos's framing. A two-way door is a decision you can walk back through. You can make it fast, and if it is wrong, you go back. A one-way door cannot be walked back through once you pass it, so take it slowly and carefully.

**Why it matters for agents**

This helps an agent decide when to make the call itself and when to stop and ask a human. Changing code and running tests are two-way doors, so it can go ahead. Deleting data, pushing to production and sending messages to outside parties are one-way doors, so it must confirm first. The dangerous-operation confirmation in [C.9 in techniques.md](techniques.md#c-writing-code) follows the same idea.

**Prompt**
```
Before each decision, first judge whether it is reversible:
- Reversible (two-way door): local changes, running tests, creating branches. Just do it, no need to ask me.
- Irreversible (one-way door): deleting data, pushing to a shared branch or production, sending anything externally, changing permissions. Stop, explain the impact and the alternatives, and wait for my confirmation, unless I already approved this action. Ask again only if what you find goes beyond what I approved.
When in doubt, treat it as irreversible.
```

---

## III. Debug and Find Root Causes

### 13. The Scientific Method

> Hypothesis, prediction, experiment, observation

**What it is**

First form a hypothesis, predict what you should see if it is true, design an experiment to test it, then accept or reject the hypothesis based on what you observe. The 2023 AutoSD study applied this process to automated debugging with LLMs. After the model proposes a hypothesis, it must write a debugging script to test it. It cannot just guess the answer.

**Why it matters for agents**

When debugging, agents often start changing code as soon as they think of one cause, and switch to another cause if that was wrong. Following the scientific method puts evidence behind every step, and makes it easier to explain to a human how the bug was found.

**Prompt**
```
Debug with the scientific method. Record each round in this format:
- Hypothesis: I think the cause is...
- Prediction: if the hypothesis is true, running [some command/test] should show...
- Experiment: the command actually run
- Observation: the result actually seen
- Conclusion: hypothesis confirmed / rejected / need more information
Propose at least two competing hypotheses and use experiments to tell them apart before you change anything.
```

---

### 14. Five Whys

> Keep asking why until you reach the root cause

**What it is**

This method comes from the Toyota Production System. When something goes wrong, ask why. Then ask why about the answer. Usually by around the fifth level you find the root cause. For example, this chain:

1. The service went down. Why?
2. Memory ran out. Why?
3. The cache had no size limit. Why?
4. The original assumption was that the data would be small. Why?
5. The team had no capacity planning process.

**Why it matters for agents**

Agents tend to stop at the first-level cause: memory is full, so add memory. Forcing them to keep asking leads them to the place that really needs fixing.

**Limits**

It follows only one causal chain, while real problems often have several causes at once. It works best combined with the multiple hypotheses of method 13.

**Prompt**
```
Do a "Five Whys" analysis of this problem:
Start from the symptom. At each level, ask "why did this happen", and back every answer with evidence (logs, code, data).
Keep asking until you find a cause that can be fixed, and that, once fixed, stops this kind of problem from happening again.
If a level has several possible causes, list all the branches.
```

---

### 15. Bayesian Updating

> Judge with a confidence level and adjust it with evidence

**What it is**

Start with an initial judgment, called the prior. Each time you see new evidence, adjust the judgment according to how strong the evidence is, and get the posterior. Judgments come in degrees, not just two states of belief and disbelief. A commonly cited case is the search for Air France 447. The search team also recalculated the areas they had already searched without finding anything, taking into account that the black box beacons might both have failed, and found the wreckage within a week.

**Why it matters for agents**

An agent's conclusions are usually just yes or no, with nothing in between. Asking it to give a confidence level, and to say which piece of evidence changed that confidence, shows how sure it really is.

**Prompt**
```
For each candidate cause, give an initial confidence (as a percentage) and the reason.
Each time you get a new piece of evidence, update the confidence, and explain why that evidence made it go up or down.
Note: not finding evidence does not mean the evidence does not exist. Say how likely your checking method is to miss it.
```

---

## IV. Verify and Review

### 16. Pareto Improvement

> Make one thing better without breaking anything else

**What it is**

A change that makes at least one party better off while making no party worse off. See [Appendix B](#appendix-b-pareto-improvement) for the full introduction.

**Why it matters for agents**

When an agent fixes one bug, it often breaks something else along the way: other tests fail, interface behavior changes, performance drops. Using Pareto improvement as the acceptance criterion means requiring that every change has no losers. When a trade-off is truly needed, it must be stated openly, not happen quietly.

**Prompt**
```
This change must be a Pareto improvement:
1. Before the change, run the tests that cover the affected behavior, plus any checks the repository requires, and record the baseline (passed count, failed count, key performance metrics).
2. After the change, run it again and confirm that no previously passing test now fails and no metric got worse.
3. If something unavoidably gets worse (a trade-off), stop and list: who gets better, who gets worse, and by how much. I will decide whether to accept it.
```

---

### 17. Goodhart's Law

> When a measure becomes a target, it stops being a good measure

**What it is**

Once a measure is treated as the goal to chase, people find ways to make the number look good, while the thing it was meant to measure does not improve. The rat bounty in method 10 is also an example: officials counted tails, but what they wanted to reduce was rats.

**Why it matters for agents**

Give an agent the goal "make the tests pass" and it may hard-code test values, delete failing tests or skip checks. It needs to know the real effect the metric stands for. [C.6 in techniques.md](techniques.md#c-writing-code) has a matching prompt.

**Prompt**
```
Tests and metrics are only for verification. The real goal is: [one sentence stating the real effect to achieve].
- Do not modify, delete or skip any existing test, unless you can prove the test itself is wrong and you tell me first.
- Do not hard-code results that only work for the test data.
- If you find a conflict between hitting the metric and reaching the real goal, stop and tell me.
```

---

### 18. Adversarial Review

> Get an agent whose only job is to find faults

**What it is**

Have an agent that did not take part in the implementation review the result independently, looking specifically for counterexamples, omissions and failure scenarios.

**Why it matters for agents**

The agent that wrote the code tends to believe its own solution is right. A different agent that has not seen the implementation process, given only the result and the original requirement, is more likely to find problems. This is really multi-agent cross-checking.

**How**

- Keep the reviewer and the implementer separate, ideally without shared context from the implementation process.
- Give the reviewer only the original requirement and the final output.
- Every issue must come with evidence, such as reproduction steps, a code location or a counterexample input.

**Note**

Ask a reviewer to find problems and it will almost always report some, even when the code is fine. Fixing every one of them leads to over-engineering: extra abstraction layers, defensive code, and tests for cases that cannot happen. So limit it to reporting issues that affect correctness or the requirements, and treat the rest as optional. This point comes from Claude Code's official best practices.

**Prompt**
```
You are an independent reviewer and did not take part in this implementation. Your job is to prove it is wrong.
- Against the original requirement, find missing features, edge cases and failure scenarios.
- Construct counterexample inputs that make it fail.
- Every issue must come with evidence: a code location, reproduction steps, or a concrete input and output. List suspicions without evidence separately and mark them "unconfirmed".
- If you cannot find any issues, explain which aspects you checked.
- Report only issues that affect correctness or violate the requirements. Code style preferences do not count.
```

---

### 19. Independent Judgment

> Judge first, then look at other answers

**What it is**

Form your own judgment and reasons before you see anyone else's conclusion.

**Why it matters for agents**

In multi-agent work, when the first agent speaks first, the agents after it are easily anchored by it and just nod along, so several agents end up being worth one. Having each agent give its own conclusion first and only then discuss is what brings disagreements to the surface. The self-consistency research in method 20 supports this practice.

**How**

- Start several agents in parallel. Each gets only the original problem, and none can see the others' output.
- Collect all conclusions before combining them, and focus on where they disagree.
- When they disagree, have each side argue with evidence. Do not decide by vote.

**Prompt**
```
Make this judgment independently. Do not refer to other agents' answers:
1. Give your conclusion and the evidence that supports it.
2. State your confidence and your main grounds.
After that you will see other agents' conclusions. Change your position only if another agent gives evidence you did not consider, and say which piece of evidence changed your judgment.
```

---

### 20. Self-Consistency

> Solve independently several times and check whether the answers agree

**What it is**

A 2022 paper from Google, called Self-Consistency. Have the model solve the same problem several times independently with different lines of reasoning, and take the answer that appears most often. The correct answer can often be reached by several paths, while wrong answers tend to differ from each other.

**Why it matters for agents**

In practice, this means having several subagents each solve the same problem independently. If the answers agree, they are more trustworthy. If they disagree, the points of disagreement are exactly where a human most needs to look.

**Prompt**
```
Solve this problem independently with 3 different lines of reasoning. Each line must not refer to the conclusions of the others.
Then compare the three answers:
- They agree: give the answer.
- They disagree: list the points of disagreement, analyze which line of reasoning is more reliable, and give a final judgment with the reason.
```

---

### 21. Steelmanning

> Before you argue against a view, state it in its strongest form

**What it is**

A straw man argument twists the other side's view into its weakest version and then attacks that. Steelmanning goes the other way: first put the other side's view into its most convincing version, then judge it.

**Why it matters for agents**

When an agent compares solutions, it often writes up the one it prefers very well and makes the others look weak. Asking it to steelman each solution first makes the comparison fair. A reviewer can also steelman the design under review before looking for faults, so it does not find fault just for the sake of it.

**Prompt**
```
Before you compare these solutions, write the strongest case for each one: in what scenario is it the best choice? What would its supporters say?
Then compare the strengths and weaknesses of each solution, and give your recommendation with the reason.
If the solution you recommend is worse than another in some scenario, say so explicitly.
```

---

### 22. Critical Thinking

> Always check the evidence

**What it is**

Even when an argument is complete and well written, check the evidence behind each claim before deciding whether to believe it.

**Why it matters for agents**

Agents are good at writing analysis that reads logically, but reading well and being right are two different things. Make the agent separate observed facts from speculation, and say what evidence would overturn its judgment.

**Prompt**
```
In your analysis, clearly separate three kinds of content:
- [Fact] Directly observed: code, logs, test output, original doc text, with the source.
- [Inference] Derived from facts. Show the chain of reasoning.
- [Assumption] Not verified.
For your main conclusion, state: what evidence, if it appeared, would overturn it? Have you checked whether such evidence exists?
```

---

### 23. Chain-of-Verification

> Write a draft first, then check each claim independently

**What it is**

A 2023 paper from Meta, called Chain-of-Verification, or CoVe for short. It has four steps:

1. Write a first draft.
2. For the factual claims in the draft, list verification questions.
3. Answer the verification questions one by one. Do not look at the draft while answering, so it does not bias you.
4. Revise the draft based on the verification results.

The paper also found that open-ended verification questions work better than yes/no questions. Asking "What year was X released?" is more reliable than asking "Was X released in 2020?", because yes/no questions tend to make the model go along with the original claim and answer "yes".

**Why it matters for agents**

It fits writing docs, writing reports and answering factual questions, and can be combined with method 22.

**Prompt**
```
1. Write a first draft.
2. List every factual claim in the draft that can be checked, and write an open-ended verification question for each one (no yes/no questions).
3. Answer the verification questions one by one. Check the original sources (code, docs, command output) when you answer. Do not refer to the draft.
4. Revise the draft based on the verification results, and list what you changed.
```

---

### 24. Rubber Duck Debugging

> Explain it line by line, and the problem shows itself

**What it is**

A programmer explains to a rubber duck on the desk, line by line, what their code does. Partway through, the problem often shows itself, because to explain clearly you have to pay attention to details you normally skip.

**Why it matters for agents**

Having an agent explain its own changes section by section can surface problems it did not notice, such as a variable that is never actually used, a branch that can never be reached, or a condition that is written backward.

**Prompt**
```
Explain your change section by section: what each piece of code does, why it is needed, and which input cases it handles.
While explaining, if you find a piece of code whose reason for existing you cannot explain, or that does not behave as you expected, mark it and fix it.
```

---

## V. Deliver and Improve

### 25. List Every Uncertainty

> Give uncertainty a place to show up

**What it is**

Explicitly require the agent to say where it is not sure.

**Why it matters for agents**

Agents always sound confident, and right and wrong answers sound the same. Unless you give uncertainty its own place, it hides inside fluent text.

**Prompt**
```
At the end of your answer, add a separate "uncertainty list":
- Which conclusions lack direct evidence?
- Which scenarios are untested?
- Which parts are speculation or assumption?
- Which information might be outdated?
For each item, note which conclusion would be affected if it is wrong.
```

---

### 26. Checklists

> Write down what "done" means and check each item

**What it is**

The Checklist Manifesto makes the point that in complex fields, many failures come from a missed step, not from people who do not know how to do the work. Pilots and surgeons both rely on checklists to avoid these misses.

**Why it matters for agents**

An agent stops once things look done. With a checklist that spells out what "done" means, it can check each item before delivery, and you can see at a glance which item was not done.

**Prompt**
```
Before delivery, check each item and report its status (✅ / ❌ / N/A):
- [ ] The original problem was reproduced, and confirmed gone after the fix
- [ ] Relevant tests were run and passed, with output attached
- [ ] No previously passing test now fails
- [ ] Lint and type checks pass
- [ ] All callers have been checked
- [ ] Temporary files have been cleaned up
- [ ] Uncertain points have been listed
For any item marked ❌, explain why.
```

---

### 27. Ablation Study

> Remove one thing and see if it still works

**What it is**

An ablation study is the standard method in papers for showing that each component is useful. Keep everything else the same, remove one variable, and see how much the result changes.

**Why it matters for agents**

Prompts, rules and tools keep piling up, and nobody knows which ones really help. The only way to know whether a rule, a tool or a piece of prompt does anything is to remove it and run again.

**How**

- Fix the test cases and the scoring criteria.
- Remove only one element at a time and run the same tests.
- Record the results and delete the elements that have no effect.
- Agent output is random, so run each condition several times, so you do not mistake noise for an effect.

**Prompt**
```
Run an ablation study on this configuration:
1. First run the test set with the full configuration and record the baseline results.
2. Remove only one item at a time (one rule / one tool / one piece of prompt), keep everything else the same, and rerun the same test set.
3. Output a table: removed item, change in results, conclusion (required / can delete / unsure).
4. Run each condition at least N times and state the range of variation in the results, so random noise is not mistaken for an effect.
```

---

## Appendix A: Socratic Questioning

The method of the ancient Greek philosopher Socrates, recorded mainly in Plato's dialogues. The questioner does not give the answer directly. Through a series of follow-up questions, the other person examines their own view, finds the contradictions themselves, and reaches a clearer understanding.

**Basic process**

1. Have the other person state a view. For example, they say courage is not being afraid of danger.
2. Ask for definitions and examples. If someone who cannot swim jumps into rapids, is that courage?
3. Find the contradiction. They admit this is more like recklessness, so the original definition does not hold.
4. Revise the view. Courage should include judgment about danger.
5. Keep asking until the view is rigorous enough, or both sides admit they have not figured it out yet.

**Six common types of questions**

| Type | Example |
|---|---|
| Clarify concepts | What exactly do you mean by "success"? |
| Check assumptions | What is the premise of this conclusion? Does it always hold? |
| Ask for evidence | How do you know? What is it based on? |
| Change perspective | What would someone who disagrees say? |
| Trace consequences | If this view is true, what follows? |
| Question the question | Why are we discussing this question? |

**Limits**

Used badly, it comes across as aggressive. It is good for clarifying thinking and exposing contradictions, but it does not always reach a final answer. Many of the dialogues Plato recorded end without a conclusion.

---

## Appendix B: Pareto Improvement

A concept introduced by the Italian economist Vilfredo Pareto. When a change in how resources are allocated makes at least one person better off and nobody worse off, it is called a Pareto improvement. In other words, an improvement with no losers.

**Related concepts**

- **Pareto optimal**. A state where no Pareto improvement can be found anymore. To make anyone better off, you must make someone else worse off.
- **Kaldor-Hicks improvement**. Allows some people to lose, as long as the winners' gains are larger than the losers' losses. Most real-world policy evaluation uses this standard.

**Note**

- It measures efficiency, not fairness.
- Real changes with no losers at all are rare. It is used more as a theoretical baseline.

---

## Sources

- [Take a Step Back (Step-Back Prompting paper)](https://arxiv.org/abs/2310.06117), Zheng et al., Google DeepMind, ICLR 2024
- [Least-to-Most Prompting Enables Complex Reasoning in LLMs](https://arxiv.org/abs/2205.10625), Zhou et al., Google, ICLR 2023
- [Self-Consistency Improves Chain of Thought Reasoning in LLMs](https://arxiv.org/abs/2203.11171), Wang et al., Google, 2022
- [Chain-of-Verification Reduces Hallucination in LLMs](https://arxiv.org/abs/2309.11495), Dhuliawala et al., Meta, 2023
- [Explainable Automated Debugging via LLM-driven Scientific Debugging](https://arxiv.org/abs/2304.02195), AutoSD, Kang et al., 2023
- [How we made 163 mental models executable for AI agents](https://dev.to/bradju/how-we-made-163-mental-models-executable-for-ai-agents-3b97). The three cases of Wald, the Hanoi rat bounty and Air France 447 are cited from this article.
- [Inversion Thinking](https://concepts.dsebastien.net/concept/inversion-thinking/)
- [Chesterton's Fence](https://concepts.dsebastien.net/concept/chestertons-fence/)
