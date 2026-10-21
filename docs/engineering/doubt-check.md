# doubt-check

**Status:** stable

## What it does

Hands one decision to a fresh subagent whose only job is to find what's
wrong with it. The subagent gets the claim, the artifact, and the
contract it must meet. It doesn't get the reasoning behind the decision,
because reasoning invites agreement. Each objection is then accepted or
refuted with evidence: a command, a line of code, or a criterion. It
stops after 3 cycles, or after 2 cycles in a row with nothing actionable.

## When to reach for it

- A design choice other steps will build on: a data shape, an interface,
  a concurrency approach.
- A root-cause conclusion from `debug-systematically`, before the fix
  lands.
- A claim that a Success Criterion is met when the evidence is indirect.
- Skip it for decisions an approved spec already covers, and for anything
  cheap to reverse.

## Common questions

**Why not just review it myself?**
The agent that made a decision has its context full of the reasons for
it. It finds reasons to agree. A fresh subagent with no reasoning finds
the failure cases.

**What counts as refuting an objection?**
Evidence: a command run, a line of code, or a criterion. "I think it's
fine" isn't a refutation, so accept the objection or find the line.

**What if the doubter is wrong?**
Then the refutation is easy, and it goes in the output. In the dry run,
3 of the 12 objections in cycle 3 rested on wrong claims about the eval
harness. The harness source refuted each one.

**How was it proven?**
On whether SC-1 to SC-5 of the sequential-dispatch spec can be checked
with `claude plugin eval`. That was an open decision `plan-from-spec`
would build on. Three cycles found 22, 15, and 12 objections. 46 were
accepted and 3 refuted, in commits `65af924`, `bfcaae7` and `8a5af64`.
The record is
[`docs/specs/2026-10-19-sequential-dispatch-doubt-check.md`](../specs/2026-10-19-sequential-dispatch-doubt-check.md).

## It's working if

- The doubter's prompt holds the claim, artifact, and contract, and
  nothing about why the decision was made.
- Every objection ends as accepted with a change or refuted with
  evidence.
- The run stops at 3 cycles, or at 2 empty cycles in a row.
