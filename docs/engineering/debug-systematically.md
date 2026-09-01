# debug-systematically

**Status:** stable

## What it does

A reproduce → minimize → hypothesize → instrument → root-cause loop for any
bug, failing test, or unexpected behavior — designed to stop fixes from
landing on the symptom a report happened to describe while every sibling
code path stays broken.

## When to reach for it

- Any bug report or test failure, before writing a fix.
- Especially when the fix "feels obvious" — that's exactly when an
  unconfirmed guess is most likely to slip through.

## Common questions

**Isn't this overkill for an obvious bug?**
The loop scales with the bug — for something genuinely obvious, reproduce
and confirm take seconds. The discipline is cheap; a wrong guess that ships
isn't.

**Why grep all callers before fixing?**
Because the report names one symptom, and if the root cause lives in a
function with five callers, four of them are still broken after a fix
scoped only to the one the report named.

## It's working if

- Every fix has a regression test built from the minimized repro.
- Fixes land in the shared function all callers route through, not in the
  one caller the original report happened to mention.
