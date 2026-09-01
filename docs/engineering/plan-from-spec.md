# plan-from-spec

**Status:** stable

## What it does

Converts a spec into an ordered, dependency-sequenced implementation plan.
Each step names the files it touches and carries a verification action
pulled directly from the spec's Success Criteria & Evals — so the plan isn't
just a task list, it's a checkable one.

## When to reach for it

- Right after a spec is approved (from `spec-from-idea`) and before any code
  gets written.
- A task feels too large to implement in one pass and needs breaking into
  independently verifiable steps.
- You want implementation order to reflect real dependencies, not just the
  order ideas came up in conversation.

## Common questions

**What if there's no spec, just a quick task?**
Say so explicitly, then either do a short in-chat plan for something small
and well understood, or go back to `spec-from-idea` if it turns out bigger
than it looked.

**Why does every step need a "Verification" line?**
Because that's what makes the plan an artifact `implement` and `review-code`
can actually check against, instead of a to-do list that just gets marked
"done" on faith.

**What if a step doesn't map to any Success Criterion in the spec?**
That's a signal, not something to paper over — either the step isn't
necessary, or the spec is missing a criterion. Resolve which before
continuing.

## It's working if

- Every step in the plan has a Verification line traceable to the spec.
- `implement` can pick up any step and know exactly what files to touch and
  how to know it's done, without re-reading the whole spec.
- Steps are ordered so nothing depends on work a later step hasn't done yet.
