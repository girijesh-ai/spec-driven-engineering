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

**Prompt the positive target.** Naming a forbidden behaviour puts it in
front of the reader and primes it. "Run the verification command
yourself" works better than "don't trust the subagent's claim". Use a
prohibition only when there's no positive form, and pair it with the
positive rule.

**Give every task a completion criterion.** The reader must know when
it's done (clarity) and must be required to show it (demand): "done when
the command exits 0 and you've pasted its output", not "make sure it
works".

**Lead with the word that carries the instruction.** Start steps and
bullets with the operative verb or term in bold — **Stop**, **Run**,
**Never overwrite** — so a reader skimming mid-task lands on it.

**Two loads, two budgets.** *Context load* is how much text the doc puts
in the window; *cognitive load* is how much the reader must hold in mind
to follow it. Cut both: a short doc full of cross-conditions is still
heavy.

**Progressive disclosure.** Order by what the reader needs first: when to
use, the process, then edge cases. Heavy detail (100+ lines) goes in a
`references/*.md` file the body points to at the step that needs it —
"see `references/feedback-loops.md`" in step 1, not a reading list at the
top.

**Context pointers over copies.** Point at the file, section, or command
that holds the truth (`spec §Approach`, `pyproject.toml [tool.pytest]`)
instead of restating it. A copy goes stale; a pointer can't.

**Call skills explicitly.** When a skill must load another, say so as an
action: "Call the Skill tool with `review-code`". Naming a skill in prose
("run review-code") doesn't reliably load it. Two skills means two calls,
said as two. Prose that only mentions a skill for a human reader (a
routing table, a credits line) stays a plain label. Mark the requirement
level either way: "before each commit" (required) vs. "can also" (optional).

**Tables and checklists over prose for anything scannable.** A rule someone
needs to check against later belongs in a table row, not buried in a
paragraph.

**No narrative examples.** "In session X, we found that..." is too
specific to generalize from and won't still be true later. One clean,
general example beats a war story.

**Discipline skills carry three closing sections.** Skills that hold a
line under pressure (`spec-from-idea`, `implement`, `review-code`,
`test-driven-development`, `debug-systematically`) end with:
- **Common rationalizations** — `| Rationalization | Reality |`: the
  agent's own excuse, quoted, then the rule that answers it, stated
  positively.
- **Red flags** — observable signs the skill is being skipped.
- **Verification** — the evidence checklist for "done".

`scripts/validate.py` enforces all three on those skills. Other skills
keep a `| Mistake | Fix |` table.

**Prune.** Keep one source of truth per fact. Don't restate what the
environment already tells the agent (tool output, file contents). Delete
lines that change no behaviour, and clear sediment: rules added for a
problem that no longer exists.

## Common mistakes

| Mistake | Fix |
|---|---|
| Description that enumerates the skill's steps or process phases | Keep the trigger; trim the tail to at most a single outcome clause |
| A rule stated as an aspiration ("be careful with resources") | Restate as a checkable action ("trace every early-return path for resource cleanup") |
| Inlining a 200-line reference table into the main doc | Move it to `references/`, link from the main doc |
| A cross-reference with no stated requirement level | State whether it's required or optional explicitly |
| "Run `x`" or "see `x`" where the skill must actually load | "Call the Skill tool with `x`" |
| A step with no way to tell it's finished | Add the completion criterion and the evidence to show |
| A rule phrased only as "don't…" | Lead with the positive action; keep the prohibition as a second clause if needed |

## Next

Applies to every skill and doc in this repo — used while authoring, not
invoked mid-task by another skill.
