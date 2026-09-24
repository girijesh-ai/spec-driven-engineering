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
7. **Write a plain-language summary of what shipped.** Invoke the `simple`
   skill to produce a companion explainer for the non-technical audience
   (PM, leadership, an engineer picking this up cold). Its primary source
   is the **code that actually landed** — the merged diff and the current
   state of the changed files. That's the one source that can't be stale or
   aspirational: a spec states intent, but the diff is what shipped, and the
   two drift. Read the diff, describe what it *does*. Use the spec/plan only
   for the **why** — motivation and success criteria the code can't state
   itself — and never let that intent override what the code actually says.
   - Summarize what the change **is and does**, grounded in the diff — not
     the path taken to it. False starts, reverts, and debugging detours are
     session noise, not part of what shipped — leave them out. (A confident
     "here's what we did" narrated from memory is exactly the fabrication
     `simple` forbids.)
   - Keep the altitude right: explain what the shipped behavior is and why
     it matters, not a function-by-function walk of the code. The audience
     reads outcomes, not diffs.
   - If the change is too small to warrant an explainer, say so and skip —
     don't manufacture one.
   - The explainer is a companion, never a replacement: it links back to
     the PR/commit (and the spec, if there is one) as the source of truth.

## Common mistakes

| Mistake | Fix |
|---|---|
| Trusting an earlier READY after more commits landed | Re-run review-code against the branch's current state before finishing |
| Treating an open Success Criterion as a PR-description footnote | Go back to implement — it's not done until every criterion is met or explicitly N/A |
| Discarding unexpected uncommitted changes to get a clean status | Investigate first — it may be someone's in-progress work |
| Force-pushing or rewriting shared history without asking | Confirm with the user before any destructive git operation |
| Writing the PR description from memory instead of the spec | Pull Context and Goals straight from the spec — it's already the accurate version |
| Writing the plain-language summary as a session recap ("first we tried X, then fixed Y") | Summarize what shipped, sourced from the merged diff — the path taken is session noise, and narrating it from memory is the fabrication `simple` forbids |
| Summarizing from the spec's intent instead of the code that landed | The diff is what shipped; the spec is only what was hoped for. Read the code for *what*, use the spec only for *why* |

## Next

Nothing — this closes the spine. If new work surfaces during finishing
(scope was bigger than the spec covered), that's a new pass through
`spec-from-idea`, not an addition bolted onto this one.
