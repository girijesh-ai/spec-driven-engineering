# retro

**Status:** stable

## What it does

After a branch is finished, it lists what went wrong, from evidence:
review findings, reverted commits, failed checks, user corrections. Each
item becomes a change to the environment the next session works in, not
a lesson in a summary. A rule a tool could check becomes a check (a
test, a lint rule, a validator). A judgement call becomes a quoted line
in the file that should have caught it. You pick which to apply, and
each one lands as its own commit.

## When to reach for it

- After `finish-branch`, when the work had rework, a reverted change, a
  review that found the same kind of issue twice, or a near-miss.
- When someone says "this keeps happening".
- Skip it when the session went cleanly. Don't invent findings.

## Common questions

**Why a check instead of a note?**
A note gets read sometimes. A check runs every time. If a tool can catch
the mistake, the tool should catch it.

**What if nothing would have caught it?**
That's a finding in itself: "no guardrail at all". It goes in the table
either way, even when the fix is only a sentence.

**Does it apply everything it finds?**
No. It shows the table and asks. Only the items you approve land.

**How was it proven?**
On the `feat/promote-plain-technical-writing` branch. It found 7 items:
2 mechanical, 4 judgement calls, and 1 gap with no guardrail. One
mechanical item was live during the run: three docs said `stable` while
their SKILL.md said `draft`, and `scripts/validate.py` still passed. The
approved guardrail, `check_promotion_state` plus 5 tests, landed in
`4b1fac0`. It flagged those three skills until their promotion was
finished.

## It's working if

- Every item names where it showed up: a commit, a review, a check
  output.
- Each mechanical item becomes a check in a named file, and each
  judgement item becomes a quoted line.
- Only approved guardrails land, one commit each.
