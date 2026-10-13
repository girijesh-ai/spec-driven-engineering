---
name: retro
description: Use when a session or branch has finished and mistakes, rework, or near-misses happened along the way — turns each one into a change to the project's environment so the next session can't repeat it.
---

# retro
Status: draft

## Overview

A retro here doesn't improve the agent's memory; it improves the
environment the next agent works in. A mistake caught by a lint rule
never happens twice; a mistake recorded only in a summary happens again.
Adapted from mattpocock/skills' `retro`. Runs after `finish-branch`.

## When to use

- After `finish-branch`, when the work involved rework, a reverted
  change, a review that found the same kind of issue twice, or a
  near-miss
- When the user says something like "this keeps happening"

Skip when the session went cleanly — don't manufacture findings.

## Process

1. **List what went wrong**, from evidence: review findings, reverted
   commits, failed verifications, floor-guard hits, user corrections.
   One line each, with where it showed up. No narrative.
2. **Classify each item:**
   - **Mechanical** — a rule a tool could check (an import direction, a
     forbidden call, a missing test file, a format).
   - **Judgement** — needs a person or agent to decide (a naming choice,
     a design trade-off, when to ask).
3. **Propose the guardrail:**
   - Mechanical → a deterministic check: lint rule, pre-commit hook, CI
     step, test, or a floor-guard rule. Name the exact file it goes in.
   - Judgement → a written standard: the project's `CLAUDE.md`,
     `CONSTRAINTS.md`, `engineering-standards`, or the skill that should
     have caught it. Quote the line to add.
4. **Flag gaps.** An item where nothing in the environment would have
   caught it is itself a finding: "no guardrail at all".
5. **Present, then ask.** Show the table and ask which to apply. Apply
   only the approved ones, each as its own commit.

## Output

```markdown
## Retro: <branch or topic>

| What went wrong | Where | Kind | Guardrail | Goes in |
|---|---|---|---|---|
| Import from api/ into core/ | review of step 3 | Mechanical | import-linter contract | `.importlinter` |
| Asked the user a fact the repo answers | spec interview | Judgement | "Look facts up before asking" | `CLAUDE.md` |
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing lessons learned as prose | Each item becomes a check or a quoted rule with a file location |
| Encoding a mechanical rule as a written standard | If a tool can check it, make the tool check it |
| Applying every proposed change without asking | Present the table; apply only what's approved |
| Inventing findings for a clean session | Say it went cleanly and stop |

## Next

Approved guardrails land as their own commits. If one needs real design
work, call the Skill tool with `spec-from-idea` for it.
