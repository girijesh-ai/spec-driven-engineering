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
   One line each, with where it showed up. No narrative. Also look past
   outright mistakes:
   - **Navigation** — the agent took long to find a file or fact; a
     pointer would have saved it.
   - **Tool economy** — an expensive or repeated tool call that a
     script or narrower command would replace.
   - **No-ops** — lines in `CLAUDE.md` or a skill that changed nothing
     the agent did.
   - **Information access** — something the agent needed and couldn't
     see (server logs, a read-only view of a service).
   - **Steering size** — a large `CLAUDE.md` whose rules belong in
     checks or `CONSTRAINTS.md`.
2. **Classify each item:**
   - **Mechanical** — a rule a tool could check (an import direction, a
     forbidden call, a missing test file, a format).
   - **Judgement** — needs a person or agent to decide (a naming choice,
     a design trade-off, when to ask).
3. **Propose the guardrail:**
   - Mechanical → a deterministic check: lint rule, pre-commit hook, CI
     step, test, or a floor-guard rule. Name the exact file it goes in.
     Read the repo's own check commands first (`package.json` scripts,
     `Makefile`, CI workflow): a check that exists but isn't wired in, or
     is silently broken, is the finding, not a new check.
   - Judgement → a rule the reviewer enforces, since the reviewer has the
     least context pressure: the project's `CONSTRAINTS.md` (which
     `review-code` checks), or the skill that should have caught it.
     Quote the line to add. `CLAUDE.md` loads into every session, so use
     it only for navigation pointers ("auth rules live in
     `docs/auth.md`"), not rules.
4. **Flag a repo with no guardrail.** No pre-commit hook and no CI job
   running the lint, typecheck or test command is itself a finding,
   whatever went wrong in the session.
5. **Present, then ask.** Show the table, most severe first, and ask
   which to apply. Apply
   only the approved ones, each as its own commit.

## Output

```markdown
## Retro: <branch or topic>

| What went wrong | Where | Kind | Guardrail | Goes in |
|---|---|---|---|---|
| Import from api/ into core/ | review of step 3 | Mechanical | import-linter contract | `.importlinter` |
| Hand-rolled retry instead of `lib/retry` | review of step 2 | Judgement | "Use `lib/retry` for any retried call" | `CONSTRAINTS.md` |
```

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing lessons learned as prose | Each item becomes a check or a quoted rule with a file location |
| Encoding a mechanical rule as a written standard | If a tool can check it, make the tool check it |
| Putting a judgement rule in `CLAUDE.md` | Put it where the reviewer reads it; `CLAUDE.md` holds navigation pointers |
| Proposing a new check the repo already has | Read its check commands and CI first; an unwired check is the finding |
| Applying every proposed change without asking | Present the table; apply only what's approved |
| Inventing findings for a clean session | Say it went cleanly and stop |

## Next

Approved guardrails land as their own commits. If one needs real design
work, call the Skill tool with `spec-from-idea` for it.
