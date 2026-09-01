---
name: implement
description: Use when writing the actual code for a plan step, feature, or bugfix — drives test-driven development at each seam, checks each step's verification before moving on, and runs review-code before committing.
---

# implement
Status: stable

## Overview

Executes a plan (from `plan-from-spec`) step by step: test-first at every
seam, the step's verification checked before moving on, `review-code` run
before each commit. This skill doesn't own TDD or review logic itself — it
calls `test-driven-development` and `review-code` as sub-steps, so each stays
independently usable and independently improvable.

## When to use

- A plan exists and it's time to write code
- A single well-understood bugfix or small change, where the "plan" is one
  step held in your head rather than a written document

## No-spec / no-plan fallback

If no plan or spec is found, do not silently proceed as if one exists.
State plainly: **"No spec/plan found — proceeding ad-hoc."** Then implement
the change directly, still test-first, still reviewed before commit. The
fallback affects traceability, not code quality — ad-hoc mode still gets the
same TDD and review discipline, it just has no Success Criteria to check
against beyond what's obviously implied by the request.

## Process

1. **Take one step at a time.** Never start a step whose dependencies (per
   the plan) aren't done. Write against `engineering-standards` as you go —
   naming, error handling, security, layer boundaries, and necessity
   (does this code need to exist, is this the simplest correct solution)
   — rather than treating any of that as something only `review-code`
   checks after the fact. Catching your own over-engineering while writing
   is cheaper than catching it in review.
2. **Test-first.** Invoke `test-driven-development` for the step: write the
   failing test that encodes the step's verification, watch it fail for the
   right reason, write the minimal code to pass, refactor.
3. **Check the step's verification** (from the plan, traced to the spec's
   Success Criteria & Evals) before considering the step done. "The code
   compiles" is not verification; "the linked criterion is now checkable
   and passes" is.
4. **Run `review-code` before each commit** — not just at the end of the
   whole plan. Catching a standards or spec-compliance problem one step
   late is cheaper than catching it after five steps built on top of it.
5. **Commit** only after review passes (or documented findings are
   addressed).
6. **Move to the next step.**

## Reuse before writing

Before writing new code for a step, check what the plan already flagged as
reusable, and grep the codebase for existing implementations of the same
concern. Building a second version of something that exists is a bug, not a
feature.

## Common mistakes

| Mistake | Fix |
|---|---|
| Writing all steps' code, then testing at the end | Test-first per step — this is what makes each step's verification meaningful |
| Treating "ad-hoc mode" as license to skip TDD/review | Ad-hoc affects traceability only; test-first and review-before-commit still apply |
| Running review-code once at the very end | Run it per step, before each commit — cheaper to fix one step's problem than five stacked on it |
| Silently proceeding when no plan exists | State "no spec/plan found — proceeding ad-hoc" out loud, every time |
| Re-implementing something the plan already flagged as reusable | Check the plan's reuse notes and grep first |

## Next

After all steps pass review, hand off to `finish-branch`.
