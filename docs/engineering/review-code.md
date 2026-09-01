# review-code

**Status:** stable

## What it does

A two-axis review: does the change satisfy the spec's Success Criteria &
Evals (primary), and does it hold up against engineering standards and
architecture (secondary)? It reads full changed files, not just the diff,
and explicitly audits caller impact, resource cleanup on every early-return
path, and external-dependency failure modes — not just style.

## When to reach for it

- Before every commit within `implement`, not only at the very end.
- Before `git push` or opening a PR.
- Any time a change is about to be claimed "done."

## Common questions

**What if there's no spec to check against?**
The spec axis is reported as explicitly skipped, never silently treated as
passed. The standards axis still runs in full regardless.

**Isn't reading whole files instead of just the diff slower?**
Yes, and that's the point — most real bugs in a reviewed diff live in how
the change interacts with code around it, not in the changed lines
themselves.

**What's the actual bar for READY?**
Zero confirmed issues, and the spec axis either met or explicitly marked
not applicable. "Plausible issues" alone don't block READY, but they should
be surfaced, not dropped.

## It's working if

- A verdict of READY genuinely means safe to ship — no confirmed bug shows
  up in the next round of manual testing that this review should have
  caught.
- Every public interface change gets its callers checked, every time.
- Resource-leak and failure-path findings show up before production does.
