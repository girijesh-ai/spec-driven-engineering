---
name: handoff
description: Use when a conversation or session needs to end but the work isn't finished — compacts the current state into a handoff document another agent or session can pick up from without re-deriving everything.
---

# handoff
Status: draft

## Overview

A session boundary is not a work boundary. This skill turns "what's true
right now" into something the next session can load and continue from,
instead of the next session re-exploring the codebase and re-asking
questions already answered here.

## When to use

- A session is ending (context limit, time, explicit stop) with work still
  in progress
- Work is being handed to a different agent/person mid-task

## What goes in a handoff doc

```markdown
# Handoff: <topic>

## Where this is in the spine
<e.g. "spec approved, plan-from-spec done, implement on step 3 of 5">

## What's done
Concretely — files changed, tests passing, review status if any.

## What's next
The specific next action, not a restated task description.

## Decisions already made
Anything that was debated and resolved — so it doesn't get re-litigated.

## Open questions
Anything genuinely still unresolved, and what's needed to resolve it.

## Links
Spec path, plan path, branch name, relevant PR/issue.
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

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing a narrative of the session instead of current state | State what's true now, not the path taken to get there |
| Omitting the spec/plan link | Without it, the next session can't verify anything against Success Criteria |
| Listing a resolved decision as an open question | Forces redundant re-litigation — be explicit about what's settled |
| Vague "what's next" ("continue implementation") | Name the specific next step and which skill handles it |

## Next

Whoever receives the handoff starts with `dev-workflow` using the "Where
this is in the spine" line to route to the right skill.
