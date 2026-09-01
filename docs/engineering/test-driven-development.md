# test-driven-development

**Status:** stable

## What it does

The red-green-refactor loop `implement` and `debug-systematically` both
drive their code changes through: write a failing test that encodes the
requirement, write the minimum code to pass it, refactor with that test as
a safety net.

## When to reach for it

- Any time new implementation code is about to be written for a plan step.
- Any time a bug fix is about to be written — the reproduction becomes the
  failing test.

## Common questions

**What if I'm confident I know what the code should do?**
Write the test first anyway — the test is the check that the requirement is
actually understood precisely, not a ritual.

**What if I already tested it manually and it works?**
Manual verification doesn't survive the next refactor or the next person's
change. It needs to be in the suite.

**Isn't this slower for small changes?**
For a one-line fix, "minimum code to pass" is often the whole fix — the
loop doesn't add meaningful overhead there, it just makes the eventual
regression test exist instead of not existing.

## It's working if

- Every non-trivial change has a test that existed before the
  implementation code did, and that test failed for the right reason first.
- Refactors don't quietly change behavior, because the test would catch it.
