# writing-for-agents

**Status:** draft

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

**What counts as "heavy reference" that should move to a separate file?**
Roughly 100+ lines of detail that isn't needed every time the skill is
read — full checklists, syntax references, API detail.

## It's working if

- No `SKILL.md` description in this repo restates its own process.
- Every cross-reference between skills states whether it's required or
  optional.
