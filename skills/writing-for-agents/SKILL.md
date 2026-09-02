---
name: writing-for-agents
description: Use when writing or editing a SKILL.md, CLAUDE.md, or any other document an agent will read and act on — governs how this repo's own skills, and any project's agent-facing docs, are written so they get followed correctly.
---

# writing-for-agents
Status: stable

## Overview

An agent reading a doc mid-task behaves differently from a person reading
it end to end. This skill states the rules that make the difference, and
governs every `SKILL.md` and doc in this repo.

## Rules

**Description leads with the trigger.** A `SKILL.md` frontmatter
`description` must lead with when to use the skill. A single trailing clause
naming the outcome is fine ("— turns an idea into a spec"), but never
enumerate the skill's steps or name its internal process phases: a
description that summarizes the workflow becomes a shortcut an agent takes
instead of reading the body — it acts on the summary and misses whatever the
body actually says to do.

**State the rule, not just the goal.** "Write good tests" gives an agent
nothing to check itself against. "Never mock the unit under test" does.
Prefer checkable, specific statements over aspirational ones throughout.

**Put reference weight where it's used.** Heavy detail (100+ lines) goes in
a separate `references/*.md` file linked from the main doc, not inline —
keeps the frequently-loaded document scannable, and keeps the reference
available when actually needed.

**Cross-reference by name, mark the requirement level.** "See
`review-code`" is ambiguous about whether it's optional. State it:
"Calls `review-code` before each commit" (required) vs. "can also invoke
`grill-me`" (optional). Never force-load another doc's full content inline
just to reference it — link by name.

**Tables and checklists over prose for anything scannable.** A rule someone
needs to check against later belongs in a table row, not buried in a
paragraph.

**No narrative examples.** "In session X, we found that..." is too
specific to generalize from and won't still be true later. One clean,
general example beats a war story.

**Common Mistakes tables earn their place.** They convert "don't do X" into
"here's what X looks like and here's the fix" — the format that's actually
checkable against real behavior, not just a prohibition to negotiate with
under pressure.

## Common mistakes

| Mistake | Fix |
|---|---|
| Description that enumerates the skill's steps or process phases | Keep the trigger; trim the tail to at most a single outcome clause |
| A rule stated as an aspiration ("be careful with resources") | Restate as a checkable action ("trace every early-return path for resource cleanup") |
| Inlining a 200-line reference table into the main doc | Move it to `references/`, link from the main doc |
| A cross-reference with no stated requirement level | State whether it's required or optional explicitly |

## Next

Applies to every skill and doc in this repo — used while authoring, not
invoked mid-task by another skill.
