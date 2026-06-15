---
name: options
description: When the user wants to weigh approaches before implementing. Takes the user's instruction, presents multiple distinct options/ways to accomplish it with trade-offs, gives a clear recommendation, and waits for explicit approval before doing any implementation. Use when invoked as /options or when the user asks to "see options", "compare approaches", or "decide how before building".
---

# Options

Help the user **decide how** to do something before any code is written. Do NOT implement anything until the user explicitly approves an option.

Read the user's instruction. If the goal or constraints are genuinely ambiguous in a way that changes the options, ask 1–2 short clarifying questions first. Do only the light investigation needed to ground the options in reality (skim relevant files, check existing patterns/libraries); you are scoping approaches, not building.

Then present **2–4 genuinely distinct** ways to accomplish the task, no strawmen; each should be a defensible choice. For each, convey how it works, its trade-offs (effort, complexity, performance, maintainability, risk, blast radius), and roughly what it touches. Let the format fit the context. Follow with **your recommendation**: state which option you'd pick and why in 1–3 sentences, tied to the trade-offs that matter most here. Be decisive, don't hedge across all of them.

Use the `AskUserQuestion` tool to let the user choose, with your recommended option first and labelled "(Recommended)". **Wait for explicit approval before implementing**; this is the whole point. Once they pick, implement that option; if it isn't your recommendation, follow their choice without re-arguing (only flag a genuine correctness problem).

If the task is trivial with one obvious way, say so and confirm rather than inventing artificial alternatives. If a material fork comes up mid-implementation, surface it as a quick options check rather than guessing. Before forming options, search the codebase for whether this task, or a very similar one, was already done; if so, study how it was implemented and present that established pattern as your recommended option for consistency.
