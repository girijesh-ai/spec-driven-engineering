---
name: handoff
description: Use when a conversation or session needs to end but the work isn't finished — compacts the current state into a handoff document another agent or session can pick up from without re-deriving everything.
---

# handoff
Status: stable

## Overview

A session boundary is not a work boundary. This skill turns "what's true
right now" into something the next session can load and continue from,
instead of the next session re-exploring the codebase and re-asking
questions already answered here.

## When to use

- A session is ending (context limit, time, explicit stop) with work still
  in progress
- Work is being handed to a different agent/person mid-task

Not every session boundary needs one. If the spec, plan, and commits
already carry the state, a fresh session can start from them — see
`dev-workflow`'s phase boundaries. Write a handoff when something must
travel that the artifacts don't hold: a new harness or directory, a
colleague, a side task interrupting a phase.

If you're told what the next session is for ("hand off for the review",
"for the migration step"), shape the doc around that: lead with what that
session needs and drop what it doesn't.

## What goes in a handoff doc

A colleague may read it cold. Call the Skill tool with
`plain-technical-writing` and follow it: lead with where things stand,
keep every SHA, command, and path exact.

```markdown
# Handoff: <topic>

## Where this is in the spine
<e.g. "spec approved, plan-from-spec done, implement on step 3 of 5">

## What's done
Concretely — commits (SHAs), plan steps marked done, review status if any.

## Working tree
Branch, `git status` summary, and any uncommitted or untracked changes —
with what each one is, so the next session doesn't discard live work.

## Verification
The exact commands that check this work and their last result
(`pytest tests/test_x.py` → 14 passed, 1 failed: `test_expiry`).

## Approvals
What the user has explicitly approved, and where that's recorded (spec
sign-off, plan approval, "ok to merge"). Anything not listed here is not
approved.

## What's next
The specific next action, not a restated task description.

## Decisions already made
Anything that was debated and resolved — so it doesn't get re-litigated.

## Open questions
Anything genuinely still unresolved, and what's needed to resolve it.

## Links
Spec path, plan path, branch name, relevant PR/issue. Reference these by
path — don't paste their contents; a copy goes stale the moment the
original changes.
```

## Process

1. **State exactly where the work sits in the spine** — this is the single
   most useful line, since it tells the next session which skill to invoke
   next via `dev-workflow`.
2. **List what's actually done**, verified — not "mostly done," a concrete
   state.
3. **Separate decisions already made from open questions.** A decision
   restated as an open question forces the next session to redo work that's
   already finished.
4. **Skip narrative.** No "then I tried X, which didn't work, so I tried
   Y" — only what's true now and what's next.
5. **Redact.** Replace secrets, tokens, and personal data in commands and
   outputs with `<REDACTED>` before writing the file.
6. **Save it outside the repo** — the OS temp directory, unless the user
   names a place — so it isn't committed with the work. Give the user the
   full path.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing a narrative of the session instead of current state | State what's true now, not the path taken to get there |
| Omitting the spec/plan link | Without it, the next session can't verify anything against Success Criteria |
| Listing a resolved decision as an open question | Forces redundant re-litigation — be explicit about what's settled |
| Vague "what's next" ("continue implementation") | Name the specific next step and which skill handles it |
| Pasting the spec or plan into the handoff | Link by path; the file is the source of truth |
| Leaving out uncommitted changes | List them with what each is — otherwise the next session may discard live work |

## Next

Whoever receives the handoff calls the Skill tool with `dev-workflow`, using the "Where
this is in the spine" line to route to the right skill. The receiver
treats only what the **Approvals** section (or a durable artifact) records
as approved — never an approval remembered from, or implied by, an
earlier conversation.
