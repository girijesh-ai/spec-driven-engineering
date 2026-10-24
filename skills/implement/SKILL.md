---
name: implement
description: Use when writing or changing code for a plan step, feature, or bugfix — including a small one-off change asked for with no spec or plan, such as adding a function to an existing file — turns it into committed, verified code.
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

0. **Start from a clean baseline.** Run `git status --porcelain`. If it
   shows changes other than the spec and plan, stop and ask whether to
   commit, stash or keep them: a step's commit must not absorb someone
   else's work. Then discover the project's test, build, and typecheck
   commands (read the repo — never assume `npm test`), run the suite once,
   and note the result. If it's already red, say so and ask before
   building on it — otherwise a failure later can't be blamed on the step
   that caused it.
1. **Take one step at a time.** Never start a step whose dependencies (per
   the plan) aren't done. Call the Skill tool with `engineering-standards`
   once per session and write against it as you go —
   naming, error handling, security, layer boundaries, and necessity
   (does this code need to exist, is this the simplest correct solution)
   — rather than treating any of that as something only `review-code`
   checks after the fact. Catching your own over-engineering while writing
   is cheaper than catching it in review.
2. **Test-first.** Call the Skill tool with `test-driven-development` for
   the step: write the failing test that encodes the step's verification,
   watch it fail for the right reason, write the minimal code to pass,
   refactor. Run typecheck and the single test file often; the full suite
   at each plan checkpoint and before the final review. If you've written
   about 100 lines without running a test, stop and run one.
   For a plan step, a subagent does this part: see **Modes** below.
3. **Stay inside the step.** Anything you notice outside the step's scope —
   a bug, a smell, a missing test — goes in a list, not in this diff:

   ```
   NOTICED BUT NOT TOUCHING:
   - <file:line> — <what and why it matters>
   → Want me to add these as plan steps or follow-ups?
   ```
4. **Check the step's verification** (from the plan, traced to the spec's
   Success Criteria & Evals) by running its command yourself before
   considering the step done. "The code compiles" is not verification;
   "the linked criterion's command ran and passed" is.
5. **Stop the line on an unexpected failure.** A verification that fails
   for a reason you don't understand, or a build that breaks, is not
   something to push past to the next step. Preserve the output, call the
   Skill tool with `debug-systematically`, and resume only once it's green.
6. **Call the Skill tool with `review-code` before each commit** — not
   just at the end of the whole plan. Catching a standards or
   spec-compliance problem one step late is cheaper than catching it after
   five steps built on top of it.
7. **Mark the step done** in the plan file (`Status: done`). The plan
   file, not your memory, is the record a resumed session starts from.
8. **Commit** only after review passes (or documented findings are
   addressed). Stage only this step's files plus the plan's status line,
   so the tree is clean before the next step; `git blame` on the status
   line gives the step's commit. Keep each commit revertable on its own:
   the code compiles at every commit, and never delete an old
   implementation and add its replacement in the same commit.

## Modes

For a plan step only. An ad-hoc change with no plan is coded in the
main session, as above.

**Ask the mode.** After the user's yes on the plan, ask once, before any
code edit: "code-auto (default: I code each step; you look at the
checkpoints) or code-journey (before each step I write a plain unit file
for you to read; after it, a plain note on what changed)?" If the user
already named one, use it. Switching modes partway needs the user's ask.

**Delegate the coding.** For each step, call the Agent tool with `model`
set to the step's `Model:` line (`sonnet` or `opus`). The brief holds the
step text, the spec lines it cites, the files to touch, the pattern to
follow and known gotchas, and ends: "Write the failing test first, then
the code. Don't commit, run review, or start subagents. Report the files
changed, the test output, and anything you noticed but didn't touch."
The rest stays in the main session: re-run the step's verification
yourself (the subagent's "tests pass" is a claim), the floor guard,
`review-code`, the status line and the commit. agent-skills leaves model
choice to the harness; this plugin picks per step so routine steps run on
a cheaper model. On OpenCode, which can't pick a model per call, say so
once and code each step in the main session.

**When a step's check fails.** A failed check is your re-run of the
verification failing, or `review-code` returning NEEDS FIXES. Send the
failure output back to a subagent on the same model. After 2 failed
checks, send it to `opus` instead. After 2 failures on `opus`, stop: show
the failures and ask the user. Don't start a fifth call. The step stays open
while it retries, so this is still stopping the line (Process step 5):
nothing moves on. When you stop, offer `debug-systematically`.

## Reuse before writing

Before writing new code for a step, check what the plan already flagged as
reusable, and grep the codebase for existing implementations of the same
concern. Building a second version of something that exists is a bug, not a
feature.

## Common rationalizations

| Rationalization | Reality |
|---|---|
| "I'll write all the steps, then test at the end" | Test-first per step is what makes each step's verification mean anything |
| "There's no plan, so TDD and review are optional" | Ad-hoc affects traceability only; test-first and review-before-commit still apply |
| "One review at the end is enough" | One step's problem is cheap; five steps stacked on it are not |
| "While I'm here I'll fix this too" | It goes in NOTICED BUT NOT TOUCHING. An unplanned change has no criterion to check it against |
| "The failure is probably flaky, I'll move on" | Stop the line. A failure you don't understand is a bug until proven otherwise |
| "The subagent / tool said tests pass" | Run the verification command yourself. A claim is not evidence |
| "This already exists but mine is cleaner" | Reuse first; a second version of the same concern is a bug |

## Red flags

- More than ~100 lines written since the last test run
- A diff touching files the plan step doesn't name
- A commit that deletes old code and adds its replacement together
- Starting a step while the suite is red
- No "no spec/plan found — proceeding ad-hoc" line when there's no plan

## Verification

Per step, before marking it done:

- [ ] The step's verification command ran in this session and passed (paste the result)
- [ ] `review-code` returned READY for this step's diff
- [ ] Only this step's files and the plan's status line are staged
- [ ] Out-of-scope finds are listed under NOTICED BUT NOT TOUCHING, not fixed
- [ ] The plan file shows `Status: done`, in the same commit, and `git status` is clean after it

## Next

After all steps pass review, call the Skill tool with `finish-branch`.
