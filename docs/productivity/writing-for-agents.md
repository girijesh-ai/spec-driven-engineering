# writing-for-agents

**Status:** stable

## What it does

The house style for this repo's own `SKILL.md` and doc files: descriptions
that state triggers rather than summarize workflow, checkable rules instead
of aspirational ones, heavy reference content moved out of the main doc,
explicit requirement levels on cross-references.

## When to reach for it

- Writing or editing any `SKILL.md` or doc in this repo.
- Writing a `CLAUDE.md` or similar agent-facing doc in any other project.

## Common questions

**Why does the description rule matter so much?**
Because an agent decides whether to read the full skill based on the
description alone — if the description already summarizes the workflow, the
agent may act on that summary and never read the parts that would have
corrected it.

**How should one skill call another?**
As an action: "Call the Skill tool with `review-code`". Naming a skill in
prose doesn't reliably load it.

**Why do some skills have a Rationalizations table instead of Common
Mistakes?**
The five discipline skills (`spec-from-idea`, `implement`, `review-code`,
`test-driven-development`, `debug-systematically`) are the ones agents are
most tempted to cut corners on. Each closes with the excuses an agent
tends to make, the rule that answers each one, red flags, and a
verification checklist. `scripts/validate.py` enforces this.

**What counts as "heavy reference" that should move to a separate file?**
Roughly 100+ lines of detail that isn't needed every time the skill is
read — full checklists, syntax references, API detail.

## It's working if

- No `SKILL.md` description in this repo restates its own process.
- Every cross-reference between skills states whether it's required or
  optional.
