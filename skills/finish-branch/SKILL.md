---
name: finish-branch
description: Use when implementation is complete and review-code has returned READY — decides how the work gets integrated (merge, PR, rebase) and confirms nothing is left uncommitted or unverified before doing so.
---

# finish-branch
Status: stable

## Overview

The last link in the spine. Once `implement` is done and `review-code` has
returned READY, this skill decides how the work actually lands — and checks
the things that are easy to forget in the moment: uncommitted changes,
unresolved spec criteria, a branch that's drifted from its base.

## When to use

- All plan steps are implemented and `review-code` returned READY
- Before merging, pushing, or opening a PR

Do not use if `review-code` hasn't run, or returned NEEDS FIXES — go back to
`implement` first.

## Process

1. **Confirm review status.** If `review-code` hasn't been run against the
   final state of the branch (not just an earlier step), run it now. Do not
   proceed on a stale READY.
2. **Confirm every spec Success Criterion is either met or explicitly
   marked not applicable.** An open criterion is a reason to go back to
   `implement`, not a footnote in the PR description.
3. **Check for uncommitted or untracked changes** (`git status`). Anything
   unexpected there might be in-progress work — investigate before
   deciding what to do with it, never discard by default.
4. **Check the branch is current** against its base (main/master) or an
   explicit upstream — flag if it's drifted enough that a rebase or merge
   is needed before integration.
5. **Pick the integration path** and confirm with whoever owns the
   decision if it's ambiguous:
   - **Direct merge** — small, low-risk, no review process required beyond
     `review-code`.
   - **Pull request** — anything visible to others, anything following a
     team's standard review process.
   - **Rebase then merge/PR** — branch has drifted and history should stay
     linear.
6. **Write the commit/PR description from the spec**, not from memory —
   the spec's Context and Goals sections are the "why," the plan's steps
   are the "what."

## Common mistakes

| Mistake | Fix |
|---|---|
| Trusting an earlier READY after more commits landed | Re-run review-code against the branch's current state before finishing |
| Treating an open Success Criterion as a PR-description footnote | Go back to implement — it's not done until every criterion is met or explicitly N/A |
| Discarding unexpected uncommitted changes to get a clean status | Investigate first — it may be someone's in-progress work |
| Force-pushing or rewriting shared history without asking | Confirm with the user before any destructive git operation |
| Writing the PR description from memory instead of the spec | Pull Context and Goals straight from the spec — it's already the accurate version |

## Next

Nothing — this closes the spine. If new work surfaces during finishing
(scope was bigger than the spec covered), that's a new pass through
`spec-from-idea`, not an addition bolted onto this one.
