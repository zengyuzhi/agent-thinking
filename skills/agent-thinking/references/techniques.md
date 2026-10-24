# Prompting Techniques by Task Type

| Task type | The single most important technique |
|---|---|
| All tasks | Treat the agent as a smart new colleague who lacks context. Say what you want and why |
| Explaining and teaching | First say who the reader is and how deep to go |
| Writing code | Give it a check it can run itself, such as tests, a build, or a screenshot |
| Architecture diagrams | One abstraction level per diagram, use a text format, render and check when done |
| Long tasks | Write progress to files. Start fresh when the context gets messy |
| Research | First define what counts as an answer. Require cross-checking across several sources |
| Output format | Tell it what to do, not what not to do |
| Interface copy | Say what happens, in the user's words. Let the layout do the explaining |
| Visual design | Give numbers you can count, not adjectives. Propose directions before building |

---

## A. General Techniques

**1. The colleague test**

Anthropic's prompting guide has a golden rule: show your prompt to a colleague who does not know the task. If they would be confused, the agent will be too. Think of the agent as a brilliant but new employee who does not know your norms.

**2. Explain the reason behind a rule**

If you only give a rule, the agent follows its literal wording. If you explain the reason, it can generalize to similar cases.

| Less effective | More effective |
|---|---|
| Never use ellipses | Your response will be read aloud by a text-to-speech engine. The engine does not know how to pronounce ellipses, so do not use them |

**3. If you want more than the minimum, say so**

Newer models follow instructions literally. If you want it to do more, write that out directly.

| Less effective | More effective |
|---|---|
| Create an analytics dashboard | Create an analytics dashboard. Include as many relevant features and interactions as possible. Make it a fully featured implementation, not just the basics |

**4. Use examples, and choose them well**

Examples are the most reliable way to control format, tone, and structure. The official guidance suggests 3 to 5 examples. They should be close to real use cases and differ from each other. Otherwise the agent picks up shared traits you did not intend. Wrap examples in `<example>` tags to keep them apart from the instructions.

**5. Use XML tags to separate content**

When a prompt contains instructions, context, examples, and input data together, separate them with tags such as `<instructions>`, `<context>`, and `<input>`. This reduces misreading.

**6. Give it a role**

One sentence is enough, for example "You are a senior security engineer."

**7. Let it say "I don't know"**

Tell the agent clearly that it may say it is unsure when it is unsure. This reduces made-up answers. Combine this with [method 25 in methods.md](methods.md#25-list-every-uncertainty).

**8. Investigate before answering**
```
<investigate_before_answering>
Never speculate about code you have not opened. If the user mentions a specific file, you must read that file before answering.
Before answering questions about the codebase, investigate and read the relevant files.
</investigate_before_answering>
```

---

## B. Explaining and Teaching

**1. Set the reader and the depth first**

Say who the reader is (a beginner, a peer, or a manager), how much background they have, and how deep to go. The same concept is written completely differently for a product manager than for an engineer.

**2. Put the conclusion first**

OpenAI's guide suggests specifying the order of content directly. For example: conclusion first, then reasons, then caveats. Also give a word limit.

**3. Explain in layers**

This is one use of the Feynman technique. Ask the agent to explain the same concept at several depths: from an analogy a child can follow, to a professional explanation, to a one-sentence summary. As you read, notice the layer where you start nodding but cannot restate it yourself. That is where you did not understand.

**4. Say where an analogy breaks down**

Analogies help people understand quickly, but every analogy has points where it does not fit. Ask the agent to say where the analogy fails. Otherwise readers walk away with a wrong understanding.

**5. First decide which kind of document it is**

The Diátaxis framework divides technical documentation into four types. Each is written differently. If you mix them, none of the needs is met well.

| Type | What the reader wants | How to write it |
|---|---|---|
| Tutorial | To get started for the first time | Walk them through step by step, and make sure they succeed |
| How-to guide | To complete a specific task | Give only the steps, no theory |
| Reference | To look up a specific fact | Complete, accurate, consistent structure |
| Explanation | To understand why | Cover background, principles, and trade-offs |

**6. Turn it around and test the reader**

Ask the agent to play a beginner student. You explain, and it points out where your explanation is unclear. You can also ask it to write two or three questions after its explanation, to test whether the reader really understood.

**7. Format serves understanding**

Use paragraphs by default. Use tables and lists only when you need comparison, ranking, or quick scanning. Agents often cut content into many short bullet points. It looks tidy, but the logical links between sentences are lost.

**Prompt**
```
Explain [concept] to [reader, e.g. a product manager with no backend experience].
- Give the conclusion in one sentence first, then expand.
- Start with an everyday analogy, then say where the analogy does not hold.
- Walk through the full process with one concrete example.
- Do not use terms you have not explained. If you must use a term, explain it the first time it appears.
- Keep it under [N] words.
- End with 2 questions the reader can use to check whether they understood.
```

---

## C. Writing Code

**1. Give it a check it can run itself**

The Claude Code docs put this first. The agent stops when the work looks done to it. Without a check it can run, you become the only verification step, and every mistake waits for you to find it.

| Less effective | More effective |
|---|---|
| Write a function that validates email addresses | Write a validateEmail function. Test cases: user@example.com returns true, invalid returns false, user@.com returns false. Run the tests when done |
| Make the dashboard look better | [paste screenshot] Implement this design. After implementing, take a screenshot and compare it to the original. List the differences and fix them |
| The build is failing | The build fails with this error: [paste error]. Fix it and verify the build succeeds. Address the root cause, do not suppress the error |

**2. Ask for evidence**

Ask the agent to show test output, the commands it ran and their results, or screenshots. A sentence like "it's fixed now" does not count. Reading evidence is much faster than rerunning things yourself.

**3. Explore, plan, implement, commit**

First have the agent only read code, with no changes. Then have it write a plan, and you review the plan. Then implement, checking against the plan while doing so. Finally, commit.

When you can describe the change in one sentence, such as fixing a typo or adding a log line, have it do the change directly. No plan needed.

**4. Give specific context**

| Strategy | Less effective | More effective |
|---|---|---|
| Scope the task | Add tests for foo.py | Write a test for foo.py that covers the case where the user is logged out. Do not use mocks |
| Point to sources | Why is this API designed so strangely? | Look through the git history of ExecutionFactory and summarize how its API evolved into its current form |
| Reference existing patterns | Add a calendar widget | Look at how existing widgets on the home page are implemented. HotDogWidget.php is a good example. Follow the same pattern to implement the calendar widget |
| Describe the symptom | Fix the login bug | Users report that login fails after a session timeout. Check the token refresh logic in src/auth/. First write a failing test that reproduces the issue, then fix it |

**5. For a large feature, let it interview you first**
```
I want to build [brief description]. Interview me in detail by asking questions.
Ask about technical implementation, UI and interaction, edge cases, concerns, and trade-offs. Do not ask obvious questions. Dig into the hard parts I might not have thought about.
Keep asking until everything is covered, then write the complete spec to SPEC.md.
```

Once SPEC.md is written, start a new session to implement it. The new session has a clean context. A good spec states which files and interfaces are involved, what is out of scope, and how to verify the result end to end.

**6. Do not just make the tests pass**
```
Write a general, correct solution. Do not hard-code values from the tests, and do not write code that only works for the test cases.
Tests are there to verify correctness, not to define the solution.
If the task is unreasonable, or a test is itself wrong, tell me instead of working around it.
```

For the reasoning behind this, see [method 17 in methods.md](methods.md#17-goodharts-law).

**7. Make requirements traceable**

OpenAI's guide suggests that an implementation plan list, for each requirement, where it is implemented, which files and APIs are involved, how failures are handled, and which questions are still open.

**8. Say so when checks cannot run**
```
After making changes, run the most relevant verification: unit tests for the changed behavior, type checks, lint, and the build.
If you cannot run verification, explain why and give the next best way to check.
```

**9. Confirm dangerous actions first**
```
Consider the reversibility and blast radius of each action. Local, reversible actions (editing files, running tests) can be done directly.
For actions that are hard to undo, affect shared systems, or are destructive, ask me first, unless I already approved that action:
- Deleting files or branches, dropping database tables, rm -rf
- git push --force, git reset --hard, amending published commits
- Actions others can see: pushing code, commenting on PRs or issues, sending messages
When you hit an obstacle, do not take shortcuts with destructive actions. For example, do not use --no-verify to skip checks.
```

**10. Clean up temporary files**
```
If you created temporary files or scripts for debugging, delete them at the end of the task.
```

**11. Change only what the request needs**
```
Every changed line should trace to the request. Do not "improve" nearby code, comments, or formatting.
If you notice unrelated dead code or bugs, mention them; do not change them.
Remove only the imports, variables, and functions that your own change left unused.
```

This follows the CLAUDE.md that collects Andrej Karpathy's notes on coding agents; Codex's default system prompt says the same about unrelated bugs. The first line is a check you can run on the diff: a line that does not trace to the request should go.

**12. Let errors show**
```
Do not add broad try/catch blocks, silent defaults, or fallbacks that make a failure look like success. Let errors propagate, or report them explicitly.
```

From OpenAI's Codex prompting guide. A swallowed error makes a broken run look done, which is the failure the Ledger card exists to catch.

**13. Tidy first, then change behavior**
```
Never mix structural and behavioral changes in one commit. When both are needed, make the structural change first, and run the tests before and after it to show behavior did not change.
```

From Kent Beck's system prompt for augmented coding. His older line says the same: "make the change easy (warning: this may be hard), then make the easy change." The reviewer then reads a refactor the tests vouch for, and a separate, small behavior change.

**14. Red, then green**

"Use red/green TDD" is enough on its own. Simon Willison notes that current models read it as: write the tests first, and confirm they fail before implementing the change. A test that never failed has not shown that it can catch anything.

**15. Stop after three failed fixes**
```
If three fixes for the same problem have failed, stop. Do not try a fourth.
Report what each attempt ruled out, and question the design before going on.
```

From the systematic-debugging skill in superpowers (Jesse Vincent): three failures usually mean the problem is in the structure, not in the next patch. It pairs with the Diagnose card's log.

---

## D. Architecture Diagrams

**1. Use text-based diagrams**

Ask the agent to output Mermaid, PlantUML, or Structurizr DSL code. Do not let it describe a diagram in words. A text format can go into git, can be diffed, and can be rendered automatically.

**2. Specify the diagram type and level**

A prompt like "draw an architecture diagram of my project" works poorly. Say which kind of diagram to draw.

| Question you want to answer | Diagram to use |
|---|---|
| What parts make up the whole system, and who uses it | C4 system context diagram, or Mermaid `flowchart TD` |
| What services and databases are inside one system | C4 container diagram |
| What steps a request goes through | Sequence diagram `sequenceDiagram` |
| What states an object has | State diagram `stateDiagram` |
| How database tables relate | ER diagram `erDiagram` |

**3. One abstraction level per diagram**

The agent's most common mistake is mixing levels, for example drawing specific classes in a service-level diagram. Several rules from the C4 model can go straight into the prompt. A system context diagram shows only people and systems. Every element has a name and a one-sentence description. Containers are labeled with their technology stack. The same element keeps the same name across diagrams.

**4. Base it on the code**

Require every node to map to a module that really exists in the code, with its file path. Without this requirement, the agent may draw the ideal architecture it imagines.

**5. Render and check when done**

Render it once with a tool such as Mermaid CLI. Check for syntax errors, overlapping layout, and truncated text. OpenAI's guide also suggests rendering visual output first, then revising until it meets the requirements.

**6. Add a legend**

If the diagram uses different colors, line styles, or shapes, add a legend that says what they mean.

**Prompt**
```
Based on the codebase, draw a [C4 container diagram / sequence diagram / ...] in Mermaid format.
- The question this diagram must answer: [e.g. which services an order request passes through]
- Draw only the [container] level. Do not mix in classes or functions.
- Each node: name + one-sentence description + technology stack + corresponding code path.
- Nodes must map to modules that really exist in the code. Mark anything you are unsure of as "inferred".
- Add a legend explaining what the colors and line styles mean.
- When done, render it once with mermaid-cli and fix syntax errors and layout problems.
```

---

## E. Long Tasks and Context Management

**1. Context is the most important resource**

The Claude Code docs say that most best practices come from one constraint. The context window fills up fast, and the fuller it gets, the worse the model performs. It starts to forget earlier instructions. The "forgot the task after 100 turns" problem mentioned in [method 1 in methods.md](methods.md#1-first-principles) comes from this.

**2. If two corrections do not fix it, start over**

Once you have corrected the same problem more than twice, the context is full of failed attempts. Clear the session, write what you learned into a better initial prompt, and start again. The docs' experience is that a clean session with a better prompt almost always beats a long session with many corrections.

**3. Write progress to files**

- Use JSON for structured state, such as `tests.json` for test results.
- Use plain text for free-form progress notes, such as `progress.txt`.
- Use git to record what was done, so you can roll back at any time.

`progress.txt` can look like this.
```
Session 3 progress:
- Fixed authentication token validation
- Updated user model to handle edge cases
- Next: investigate user_management test failures (test #2)
- Note: do not delete tests, or functionality will be missed
```

**4. How to start a new session**
```
Run pwd. You can only read and write files in this directory.
First read progress.txt, tests.json, and the git log.
Before starting a new feature, manually run a basic integration test.
```

**5. Tell it about automatic compaction so it does not stop early**

When the agent senses the context is nearly full, it tends to wrap up hastily. If your tool compacts context automatically, tell it.
```
Your context will be compacted automatically when it nears its limit, so do not end the task early because you worry about running out of tokens.
When you approach the limit, first save your current progress and state to a file.
```

**6. Specify what to keep during compaction**

Add a line to CLAUDE.md: "When compacting context, always keep the full list of modified files and the test commands."

**7. Hand research to subagents**

Research reads many files and fills up the main session's context. Let a subagent do the investigation and bring back only a summary.
```
Use a subagent to investigate how our authentication system handles token refresh, and whether there are existing OAuth utilities we can reuse.
```

**8. Do not overuse subagents either**
```
Use subagents when tasks can run in parallel, need isolated context, or are independent workstreams.
For simple tasks, sequential operations, single-file edits, or tasks that need context kept across steps, do the work directly.
```

**9. Keep CLAUDE.md short**

For each line, ask yourself: would removing this line make the agent make mistakes? If not, delete it. When CLAUDE.md is too long, important rules get buried. If a rule keeps being ignored, add "IMPORTANT" to that one line. If too many lines are emphasized, nothing is emphasized. Rules that must be followed 100% of the time belong in a hook, not just in the prompt.

---

## F. Research and Information Gathering

**1. First define what counts as an answer**

Without a success criterion, the agent does not know when to stop. It either searches too shallowly or keeps searching forever.

**2. Require cross-checking across sources**

Confirm disputed or consequential facts in at least two independent sources. Prefer official documentation and primary data.

**3. Keep several hypotheses at once**
```
Research in a structured way. As you gather information, keep several competing hypotheses.
Record your confidence in each hypothesis in your notes.
Regularly reflect on your approach and plan. Write the hypothesis tree or research notes to a file.
```

**4. Limit the scope**

If you only say "look into X" without setting a scope, the agent may read hundreds of files. Say where to look and when to stop.

---

## G. Output Format and Writing

**1. Tell it what you want**

| Less effective | More effective |
|---|---|
| Don't use markdown | Write in flowing paragraphs, not bullet points |

**2. The style of the prompt affects the style of the output**

If the prompt is full of markdown lists, the reply will be full of lists too. If you want a reply in paragraphs, write the prompt itself in paragraphs.

**3. State the reader, length, and order**

For example: "For a tech lead, under 300 words. Conclusion first, then reasons, then risks."

**4. When editing text, first say what to keep**

When you ask the agent to revise a passage, it tends to make it longer and change the original structure. First say to keep the original genre, length, and structure, and name the one specific problem to fix.

**5. If you want a process summary, ask for it**

Newer models may go straight to the next step after a tool call, without a summary. If you want to see what it did, add a line.
```
After completing a task that involves tool calls, briefly summarize what you did.
```

**6. Use a schema for structured output**

When you need JSON, prefer the API's built-in Structured Outputs feature. Avoid describing the format in words in the prompt.

**7. Translate by rewriting**
```
Keep the original meaning and formatting, and rewrite the following in [target language]:
```

Asking for a rewrite instead of a translation stops the output from copying the source's sentence structure. 宝玉 (baoyu) uses this one line in place of the multi-step translate, reflect, and re-translate prompts that earlier models needed. The test: does it read as if it was written in the target language?

**8. Learn the voice from your own edits**

When everyone uses the same "make it sound less like AI" prompt, the output just moves to a new shared template; 宝玉 argues that all such prompts are wrong. Instead, edit an AI draft yourself, then give both versions back:
```
Compare the two texts below. The first is the AI draft; the second is my edited version. List the kinds of changes I made, state the rule behind each, and add the rules to my writing-style notes.
```
After a few rounds the notes describe your own voice, and later drafts start from it.

**9. Proofread without rewriting**
```
Proofread this text before it is published. List the problems; do not fix them:
1. Spelling mistakes and typos
2. Grammar mistakes
3. Repeated words or sentence patterns
4. Logic errors and factual mistakes
5. Weak arguments that could be made stronger
6. Empty or placeholder links
```
Adapted from Simon Willison's proofreading prompt. Because the agent only points, the text keeps the author's voice; see G.4.

---

## H. Interface Copy

**1. Write for the glance, not the read**

Steve Krug's first law of usability is "Don't make me think": a screen should be self-evident, and where it cannot be, self-explanatory. Robin Williams's four principles for non-designers are contrast, repetition, alignment, and proximity. For menus and feature text this means: a label says what happens, in the user's words; items that belong together sit together and follow one pattern; every needless word goes. Krug's rule of thumb: remove half the words, then half of what is left. Layout explains before words do: grouping, order, and position already say what belongs together and what matters most, so a secondary label or description that repeats them is noise. The most common needless one is a small label above a heading, often called an eyebrow; the impeccable design skill bans it outright, because the heading carries itself.

**2. Rewrite menus and feature text**
```
You are a product manager and a copywriter in the Apple style. Rewrite every menu item and feature description in this admin interface by the principles of "Don't Make Me Think" and "The Non-Designer's Design Book":
- A user understands each label at a glance, without reading it twice.
- Everyday words. No internal names, no technical terms.
- A button says what happens when it is pressed: "Save changes," not "Submit." An action keeps one name through the flow: a "Publish" button leads to a "Published" message.
- If a line could appear in an ad, rewrite it until it sounds like product UI.
- Names: one to three words. Descriptions: under twelve words.
- Items of the same kind follow one pattern: same part of speech, same word order.
- Avoid unnecessary secondary labels and descriptions. Let the layout do the explaining.
Deliver a table: current text, new text (or "removed"), what changed and why. Flag every item whose meaning you had to guess.
```

**3. Rewrite error messages**
```
Rewrite each error message in three parts:
- A title of five to eight words: what happened.
- One sentence: why, in plain words.
- One action: what the user can do next, with a workaround if there is one.
Name the specific field or component. No error codes users would not recognize, no passive voice, no blame ("you failed to..."), no "please."
```

Adapted from the Siemens iX design system's prompt for error messages.

**4. Check it the way a user would**

Give the new labels, without their descriptions, to someone or to a fresh agent session that has not seen the product, and ask what each one does. A label that needs its description to be understood is not done. Then cover each secondary label and description in turn: if the screen still reads without it, remove it. Last, read only the headings, labels, and numbers, as OpenAI's frontend guide suggests: the screen should still make sense.

---

## I. Visual Design

**1. Give numbers, not adjectives**

Anthropic's prompting guide notes that generic instructions such as "don't use that color" or "make it clean and minimal" tend to shift the model to a different fixed palette instead of producing variety. What works is a concrete spec, or options to pick from. So state limits you can count and checks you can run, not a mood.

**2. Propose directions before building**
```
Before building, propose 4 distinct visual directions for this brief, each as background color, accent color, and typeface, plus a one-line reason. Ask me to pick one, then build only that direction.
```

**3. Design rules you can count**
```
- One H1, two typefaces at most, one neutral base and one accent color, one primary button per screen.
- Four or five font sizes and weights in total. Spacing in multiples of 4px.
- Build the hierarchy in grayscale first, with size, weight, and spacing. Add color last. Squint at the result: what matters most should still stand out.
- On a colored background, tint secondary text from that color, not gray.
- Use a card only when it holds something the user acts on. If removing its border, shadow, background, or radius hurts neither use nor understanding, remove them.
- Emphasize a whole heading, not one word in it. Labels in sentence case, not all caps. Numbered markers (01, 02, 03) only for real sequences.
- Animate only to show cause and effect. Keep it under 300ms, exits about 20% faster than entrances, ease-out for elements entering or leaving, and scale from 0.95, not from 0.
```

These come from OpenAI's frontend guides (the counts, the spacing, and the card test), Anthropic's frontend-design skill (the typographic habits that give a generated page away), *Refactoring UI* (grayscale first, tinted text), Emil Kowalski (motion timing), and Vercel's Web Interface Guidelines (animate only to show cause and effect). Keep the rules that fit the brief; a brand's own design system overrides them.

**4. Walk every state**

A screenshot of the default state hides most problems. Check hover, focus, active, loading, empty, and error states, and try short, average, and very long content. When there is motion, replay it at 10% speed in the browser's animation panel: what looks off when slowed down is what feels subtly wrong at full speed. This extends the screenshot loop in C.1.

---

## Combined Prompt

You can put the block below straight into CLAUDE.md or AGENTS.md. As E.9 suggests, after adding it, watch whether the agent's behavior changes, and delete lines that have no effect.

```
Working principles:
1. Reproduce the problem and find the root cause before changing anything. After the change, show a before/after comparison. On long tasks, reread the task goal at each stage.
2. When requirements are unclear, ask first. Only ask questions that would change the implementation.
3. Docs, comments, and memory may be outdated. Confirm against the current code before making decisions.
4. Build the simplest version that works first. Do not add features or abstractions nobody asked for.
5. Before deleting code that looks redundant, find out why it exists.
6. Do reversible actions directly. Ask me before irreversible actions such as deleting data, pushing, or sending anything externally, unless I already approved them.
7. Changes must not make anything that worked before worse. When there is a trade-off, stop and explain it. Do not hard-code to pass tests.
8. Separate facts, inferences, and assumptions. Cite sources for facts. Say what evidence would overturn your conclusion.
9. At the end of each answer, list: conclusions lacking evidence, untested scenarios, and parts that are guesses.
```

---

## Sources

- [Claude Code best practices](https://code.claude.com/docs/en/best-practices), Anthropic
- [Claude prompting best practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices), Anthropic
- [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents), Anthropic Engineering Blog
- [Best practices for prompt engineering](https://claude.com/resources/articles/best-practices-for-prompt-engineering), Anthropic
- [GPT-5.5 guide](https://developers.openai.com/api/docs/guides/gpt-5.5), OpenAI
- [Comparing LLMs for creating architecture diagrams](https://icepanel.io/blog/comparison-llms-for-creating-software-architecture-diagrams), IcePanel
- [Generating architecture diagrams from source code with Codex CLI](https://codex.danielvaughan.com/2026/05/13/codex-cli-architecture-diagrams-mermaid-c4-plantuml-source-code-visualisation/)
- [The Feynman Technique Prompt](https://dev.to/blobxiaoyao/the-feynman-technique-prompt-how-to-make-ai-explain-anything-in-4-layers-of-depth-3076), DEV Community
- [Diátaxis documentation framework](https://diataxis.fr/)
- Steve Krug, *Don't Make Me Think, Revisited*, 3rd edition, New Riders, 2014
- Robin Williams, *The Non-Designer's Design Book*, 4th edition, Peachpit Press, 2014
- Adam Wathan and Steve Schoger, *Refactoring UI*, 2018
- [Designing delightful frontends with GPT-5.4](https://developers.openai.com/blog/designing-delightful-frontends-with-gpt-5-4), OpenAI
- [GPT-5 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5_prompting_guide) and [Codex prompting guide](https://github.com/openai/openai-cookbook/blob/main/examples/gpt-5/codex_prompting_guide.ipynb), OpenAI Cookbook
- [Prompting Claude Sonnet 5](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-sonnet-5), Anthropic
- [frontend-design skill](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md), Anthropic
- [andrej-karpathy-skills CLAUDE.md](https://github.com/forrestchang/andrej-karpathy-skills/blob/main/CLAUDE.md), based on Andrej Karpathy's notes
- Kent Beck, [Augmented coding: beyond the vibes](https://newsletter.kentbeck.com/p/augmented-coding-beyond-the-vibes), 2025
- Simon Willison, [Red/green TDD](https://simonwillison.net/guides/agentic-engineering-patterns/red-green-tdd/) and [Prompts](https://simonwillison.net/guides/agentic-engineering-patterns/prompts/), Agentic Engineering Patterns
- Jesse Vincent, [systematic-debugging skill](https://github.com/obra/superpowers/blob/main/skills/systematic-debugging/SKILL.md), superpowers
- 宝玉 (baoyu), [on translating with LLMs](https://baoyu.io/blog/llm-translation-better-idiom), 2025, and [on removing the AI flavor from writing](https://baoyu.io/blog/2026-02-14/remove-ai-writing-flavor), 2026
- [AI and UX writing](https://ix.siemens.io/docs/guidelines/language/support-and-resources/AI-and-UX-writing), Siemens iX design system
- Paul Bakaus, [impeccable](https://github.com/pbakaus/impeccable)
- Emil Kowalski, [Agents with taste](https://emilkowal.ski/ui/agents-with-taste)
- [Web Interface Guidelines](https://vercel.com/design/guidelines), Vercel
- Jakub Krehel, [make-interfaces-feel-better](https://github.com/jakubkrehel/make-interfaces-feel-better)
