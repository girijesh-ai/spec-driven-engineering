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

**What if a plan file for this topic already exists?**
If any of its steps are marked done, the skill stops and asks whether to
extend it, re-cut the remaining steps, or start a new file. It never
overwrites a record of work that already shipped.

**Why put the riskiest step first?**
If an assumption behind the plan is wrong, you want to find out on step 1,
not after five other steps have been built on it.

**What if a step doesn't map to any Success Criterion in the spec?**
It's dropped by default. If you want it kept, the skill asks you first and
adds the criterion to the spec before the plan, so the spec can't grow
quietly to fit the plan. Two kinds of step change no behaviour on
purpose and are kept differently: a prefactor step names the step it makes
possible (`Enables: step 3`), and the final contract step of a migration
names the steps it finishes (`Completes: steps 2-4`) and is kept so the
old code doesn't live on beside the new.

**How does it avoid over-engineering the plan?**
Every step gets a deletion test: "if this step were dropped, which
criterion would fail?" If none would, the step goes. Small changes stay
one or two steps, and a plan of three steps or fewer skips the in-between
checkpoints.

**What is the `Model:` line on each step?**
The model that codes the step: `sonnet` by default, `opus` for a step that
is large, hard to get right, or costly if wrong. A reason in brackets says
which. `implement` hands the step to a subagent on that model, in both
code-auto and code-journey. Change it when you approve the plan.

## It's working if

- Every step in the plan has a Verification line traceable to the spec.
- `implement` can pick up any step and know exactly what files to touch and
  how to know it's done, without re-reading the whole spec.
- Steps are ordered so nothing depends on work a later step hasn't done yet,
  and the riskiest ready step comes first.
- No step is sized XL, and each one fits in a fresh session.
- Every step names its model, and the `opus` ones are the hard or risky ones.
