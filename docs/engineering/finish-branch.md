# finish-branch

**Status:** stable

## What it does

Closes out the spine: confirms review is current, confirms every spec
Success Criterion is actually resolved, checks for stray uncommitted work
and branch drift, then picks the right integration path (direct merge, PR,
or rebase-then-merge) and writes the description from the spec rather than
memory. Last, it produces a plain-language summary of what shipped (via the
`simple` skill) for the non-technical audience — sourced from the code that
actually landed, not the spec's intent or a retelling of the session.

## When to reach for it

- All plan steps are implemented and `review-code` last returned READY.
- You're about to merge, push, or open a PR.

Not for: getting a READY in the first place — that's `review-code`'s job.
This skill assumes READY already happened and checks it's still true.

## Common questions

**What if review-code passed a few commits ago but more landed since?**
Re-run it against the branch's current state. A stale READY isn't a real
READY.

**What if there's an open Success Criterion but the work feels "mostly
done"?**
That's not done. Go back to `implement`, or if the criterion turns out to
be out of scope, that's a spec change — revisit `spec-from-idea`, don't
quietly drop it.

**Merge, PR, or rebase — how is that decided?**
By risk and visibility: low-risk and no team review process needed → direct
merge. Anything others should see or a team review gate applies to → PR.
Branch has drifted from its base → rebase first, either way.

**Doesn't the plain-language summary just repeat the PR description?**
No — the PR description is for reviewers who read diffs; the summary is for
people who don't (PMs, leadership, someone onboarding). Same facts, plainer
form, more pictures. It's sourced from the **code that landed** (the merged
diff), with the spec supplying only the *why* — never narrated from the
session, and never from the spec's intent alone, since intent and shipped
code drift. "What shipped," not "what we hoped for" or "what we did." If the
change is too small to be worth explaining, skip it rather than manufacture
one.

## It's working if

- Nothing merges on a stale review.
- PR/commit descriptions read like they came from the spec, because they
  did.
- No destructive git operation happens without an explicit go-ahead.
- The stakeholder summary describes what shipped and traces every claim to
  the code that landed — no session play-by-play, no behavior the diff
  doesn't actually contain (even if the spec called for it).
