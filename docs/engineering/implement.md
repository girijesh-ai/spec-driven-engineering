# implement

**Status:** stable

## What it does

Drives the actual coding: one plan step at a time, test-first via
`test-driven-development`, each step's verification checked before moving
on, `review-code` run before every commit. It's the execution engine of the
spine — it doesn't define TDD or review rules itself, it calls the skills
that do.

## When to reach for it

- A plan from `plan-from-spec` exists and it's time to write code.
- A small, well-understood bugfix where the "plan" is one step you're
  holding in your head rather than a written document.

## Common questions

**What if there's no plan or spec at all?**
It still runs — but it says so out loud: "No spec/plan found — proceeding
ad-hoc." Code quality doesn't drop (still test-first, still reviewed before
commit), only traceability does.

**Does it write all the code first and test after?**
No — test-first per step, every step. That's what makes "the step is done"
mean something concrete rather than "the code exists."

**What happens to problems I notice outside the current step?**
They go in a NOTICED BUT NOT TOUCHING list, and you decide whether they
become new plan steps or follow-ups. The current step's diff stays about
the current step.

**What if a test fails and I don't know why?**
The skill stops the line: it keeps the failing output and calls
`debug-systematically` instead of moving on to the next step.

**Why run review-code per step instead of once at the end?**
A standards or spec-compliance problem found one step late is cheap to fix.
Found five steps late, after other code was built on top of it, it's not.

**What are code-auto and code-journey?**
After you approve a plan, `implement` asks which to use. In both, each
step is coded by a subagent on the model the plan names, and the main
session re-runs the check, runs `review-code` and commits.
- **code-auto** (the default) works through the steps and stops at the
  plan's checkpoints.
- **code-journey** stops twice per step. Before the code, it writes a
  plain unit file (`docs/plans/<plan>/units/NN-<slug>.md`) for you to read
  and say go. After it, it adds a plain "What changed" note and waits for
  next. The unit file is committed with the code. code-journey is
  **draft** until a dry run on a real task shows engineers understand the
  unit files.

They're named so they don't clash with Claude Code's Auto Mode.

**What if a step keeps failing?**
After 2 failed checks it moves to `opus`; after 2 failures there, it stops
and asks you.

## It's working if

- Every commit corresponds to one plan step, test-first, reviewed, and the
  plan file marks that step done in the same commit.
- Work starts from a suite that was green (or explicitly accepted as red).
- Ad-hoc mode is always announced, never silent.
- Nothing gets re-implemented that the plan or a codebase grep already
  showed exists.
