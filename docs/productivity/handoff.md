# handoff

**Status:** stable

## What it does

Compacts an in-progress session into a handoff document: where the work
sits in the spine, what's concretely done, what's next, decisions already
made versus genuinely open questions, and links to the spec/plan/branch.

## When to reach for it

- A session is ending with work still in progress.
- Work is moving to a different agent or person.

## Common questions

**Should this be a narrative of what happened this session?**
No — state what's true now and what's next. A narrative forces the reader
to reconstruct current state from a story instead of reading it directly.

**What's the single most useful line in a handoff doc?**
"Where this is in the spine" — it tells the next session exactly which
skill (via `dev-workflow`) to invoke next.

## It's working if

- The next session can pick up without re-exploring the codebase or
  re-asking anything already answered here.
- No decision that was already settled gets redone because it was
  mislabeled as an open question.
